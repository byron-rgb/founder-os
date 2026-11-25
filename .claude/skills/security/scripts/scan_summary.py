#!/usr/bin/env python3
"""
scan_summary.py: turn gitleaks and OSV-Scanner reports into a short, safe summary.

What it does
  gitleaks  Reads a gitleaks JSON report and lists what kind of key was found,
            in which file and line. It NEVER prints the key itself: the Secret,
            Match and Line fields are dropped even if the report wasn't redacted.
  osv       Reads an OSV-Scanner JSON report and lists each building block
            (package) with known holes: how many, the worst severity score, and
            the version that fixes it where OSV knows one.

What it touches
  Reads the report file you give it. No network. Standard library only.

Usage
  python3 -I scan_summary.py gitleaks gitleaks-report.json --delete-report
  python3 -I scan_summary.py osv osv-report.json --json out.json

Part of the Founder OS security module (Driven Young). Read-only.
"""
import argparse
import json
import os
import re
import sys

DROP = {"Secret", "Match", "Line", "Fingerprint"}


def gitleaks(path):
    data = json.load(open(path)) or []
    items = []
    for f in data:
        items.append({"type": f.get("RuleID") or f.get("Description"), "file": f.get("File"),
                      "line": f.get("StartLine"), "commit": (f.get("Commit") or "")[:10] or None,
                      "date": f.get("Date") or None})
    by_type = {}
    for i in items:
        by_type[i["type"]] = by_type.get(i["type"], 0) + 1
    print(f"Leaked keys: {len(items)} found" + (f" ({', '.join(f'{k} {v}' for k, v in sorted(by_type.items()))})" if items else ""))
    for i in items:
        where = f"{i['file']}:{i['line']}" + (f" (in history, commit {i['commit']})" if i["commit"] else "")
        print(f"  - {i['type']} in {where}")
    return {"count": len(items), "by_type": by_type, "items": items}


def vkey(v):
    """Sort versions numerically (4.17.21 after 4.17.3)."""
    return [int(x) if x.isdigit() else 0 for x in re.split(r"[^0-9]+", v) if x != ""]


def sev_score(vuln_groups):
    best = None
    for g in vuln_groups or []:
        try:
            s = float(g.get("max_severity") or 0)
        except ValueError:
            continue
        best = s if best is None else max(best, s)
    return best


def label(score):
    if score is None:
        return "unknown"
    if score >= 9:
        return "critical"
    if score >= 7:
        return "high"
    if score >= 4:
        return "medium"
    return "low"


def osv(path):
    d = json.load(open(path))
    pkgs = []
    for r in d.get("results", []) or []:
        src = (r.get("source") or {}).get("path")
        for p in r.get("packages", []) or []:
            vulns = p.get("vulnerabilities", []) or []
            if not vulns:
                continue
            fixed = set()
            for v in vulns:
                for aff in v.get("affected", []) or []:
                    for rng in aff.get("ranges", []) or []:
                        for ev in rng.get("events", []) or []:
                            if "fixed" in ev:
                                fixed.add(ev["fixed"])
            score = sev_score(p.get("groups"))
            pkgs.append({"package": p["package"]["name"], "version": p["package"].get("version"),
                         "ecosystem": p["package"].get("ecosystem"), "holes": len(vulns),
                         "worst_score": score, "worst": label(score),
                         "fixed_in": max(fixed, key=vkey) if fixed else None, "lockfile": src})
    pkgs.sort(key=lambda x: -(x["worst_score"] or 0))
    counts = {}
    for p in pkgs:
        counts[p["worst"]] = counts.get(p["worst"], 0) + 1
    print(f"Building blocks with known holes: {len(pkgs)}" + (f" ({', '.join(f'{k} {v}' for k, v in counts.items())})" if pkgs else ""))
    for p in pkgs:
        fix = f", fixed in {p['fixed_in']}" if p["fixed_in"] else ""
        print(f"  - {p['package']} {p['version']}: {p['holes']} known hole(s), worst {p['worst']}{fix}")
    return {"count": len(pkgs), "by_worst": counts, "packages": pkgs}


def main():
    ap = argparse.ArgumentParser(description="Summarise gitleaks / OSV-Scanner JSON reports safely")
    ap.add_argument("kind", choices=["gitleaks", "osv"])
    ap.add_argument("report")
    ap.add_argument("--json")
    ap.add_argument("--delete-report", action="store_true", help="delete the raw report after summarising (recommended for gitleaks)")
    a = ap.parse_args()
    out = gitleaks(a.report) if a.kind == "gitleaks" else osv(a.report)
    if a.delete_report:
        os.remove(a.report)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(out, fh, indent=2)


if __name__ == "__main__":
    sys.exit(main())
