#!/usr/bin/env python3
"""
diff_runs.py: what changed since the last security check?

What it does
  Compares two run folders (Security/runs/YYYY-MM-DD/), each holding the JSON
  files the helper scripts wrote (email.json, domain.json, website.json,
  ai.json, keys.json, deps.json...). Matches findings by check + issue, then
  prints what's new, what's gone (likely fixed), what's still open, and any
  rating that moved. Ends with the one-line owner summary, for example:
    "Security check 2026-10-16: 2 new, 1 fixed, 5 still open. Website went amber to green."

What it touches
  Reads the two folders. Writes only --json if asked. No network.
  Never reads or prints secrets (the helper scripts never save them).

Usage
  python3 -I diff_runs.py "Security/runs/2026-10-09" "Security/runs/2026-10-16"
  python3 -I diff_runs.py --latest "Security/runs"          (compares the two newest folders)

Part of the Founder OS security module (Driven Young). Read-only. Standard library only.
"""
import argparse
import json
import os
import re
import sys

NAMES = {"email": "Email spoofing", "domain": "Domain and DNS", "website": "Website", "ai": "AI tools",
         "keys": "Leaked keys", "deps": "Building blocks", "gam": "Google accounts"}


def norm(text):
    """Stable key for an issue: drop numbers and dates that change week to week."""
    t = re.sub(r"\d+", "#", str(text).lower())
    return re.sub(r"\s+", " ", t).strip()[:140]


def load_run(folder):
    findings, ratings = {}, {}
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".json"):
            continue
        check = fn[:-5]
        try:
            data = json.load(open(os.path.join(folder, fn)))
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            label = NAMES.get(check, check) + (f" ({item.get('host') or item.get('domain')})" if len(items) > 1 else "")
            if "rating" in item:
                ratings[label] = item["rating"]
            for f in item.get("findings", []) or []:
                key = (label, norm(f.get("issue", "")))
                findings[key] = {"check": label, "severity": f.get("severity", "?"), "issue": f.get("issue", "")}
            # Summaries from scan_summary.py / gam_summary.py: count-type results
            for k in ("items", "packages"):
                for x in item.get(k, []) or []:
                    if isinstance(x, dict):
                        desc = x.get("type") or x.get("package")
                        where = x.get("file") or x.get("version")
                        key = (label, norm(f"{desc} {where}"))
                        findings[key] = {"check": label, "severity": x.get("worst", "high"), "issue": f"{desc} in {where}"}
    return findings, ratings


def main():
    ap = argparse.ArgumentParser(description="Compare two security check runs")
    ap.add_argument("old", nargs="?")
    ap.add_argument("new", nargs="?")
    ap.add_argument("--latest", help="runs folder: compare its two newest dated subfolders")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.latest:
        runs = sorted(d for d in os.listdir(a.latest) if re.match(r"\d{4}-\d{2}-\d{2}", d) and os.path.isdir(os.path.join(a.latest, d)))
        if len(runs) < 2:
            print(f"Only {len(runs)} run(s) so far. Nothing to compare yet.")
            return 0
        a.old, a.new = os.path.join(a.latest, runs[-2]), os.path.join(a.latest, runs[-1])
    if not (a.old and a.new):
        ap.print_help()
        return 1
    old_f, old_r = load_run(a.old)
    new_f, new_r = load_run(a.new)
    new = [new_f[k] for k in new_f if k not in old_f]
    gone = [old_f[k] for k in old_f if k not in new_f]
    still = [new_f[k] for k in new_f if k in old_f]
    moved = [(c, old_r[c], new_r[c]) for c in new_r if c in old_r and old_r[c] != new_r[c]]
    date = os.path.basename(os.path.normpath(a.new))
    order = {"high": 0, "critical": 0, "medium": 1, "low": 2}
    for lst in (new, gone, still):
        lst.sort(key=lambda x: order.get(str(x["severity"]).lower(), 3))
    print(f"Compared {os.path.basename(os.path.normpath(a.old))} with {date}")
    for title, lst in (("New", new), ("Gone (check they're really fixed)", gone), ("Still open", still)):
        print(f"{title}: {len(lst)}")
        for x in lst:
            print(f"  [{x['severity']}] {x['check']}: {x['issue']}")
    for c, o, n in moved:
        print(f"Rating moved: {c} {o} -> {n}")
    line = f"Security check {date}: {len(new)} new, {len(gone)} fixed, {len(still)} still open."
    if moved:
        line += " " + "; ".join(f"{c} went {o} to {n}" for c, o, n in moved) + "."
    top_new = next((x for x in new if str(x["severity"]).lower() in ("high", "critical")), None)
    if top_new:
        line += f" Worth a look this week: {top_new['issue'][:90]}"
    print("\nOwner line: " + line)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump({"new": new, "gone": gone, "still_open": still, "ratings_moved": moved, "owner_line": line}, fh, indent=2)


if __name__ == "__main__":
    sys.exit(main())
