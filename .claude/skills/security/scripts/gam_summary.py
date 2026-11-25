#!/usr/bin/env python3
"""
gam_summary.py: turn GAM's spreadsheet exports into plain-English findings.

What it does
  Reads the CSV files the Google admin made with GAM's read-only "print"
  commands (see references/checks/workspace-settings.md) and counts:
    users.csv    people without two-step login, admins, suspended or never-used
                 accounts, accounts not used in 90+ days
    tokens.csv   outside apps connected to staff accounts, and which of them can
                 read or send email, or read or change files
    drive.csv    files shared with "anyone with the link" or public on the web
  Prints counts by default. --names adds who and what, for the owner's own
  report only (it stays in their brain folder, never sent anywhere).

What it touches
  Reads the CSV files you point it at. No network, no Google access of its own.
  Column names are matched loosely, because GAM's headings vary a little by version.

Usage
  python3 -I gam_summary.py --users users.csv --tokens tokens.csv --drive drive.csv
  python3 -I gam_summary.py --users users.csv --names --json out.json

Part of the Founder OS security module (Driven Young). Read-only. Standard library only.
"""
import argparse
import csv
import datetime as dt
import json
import sys

RISKY_SCOPES = {
    "mail": ("https://mail.google.com/", "gmail.modify", "gmail.readonly", "gmail.send", "gmail.compose", "gmail.insert"),
    "files": ("auth/drive", "drive.readonly", "drive.file", "documents", "spreadsheets"),
    "admin": ("admin.directory", "admin.reports", "apps.groups", "cloud-platform"),
}
TRUTHY = {"true", "yes", "1", "y"}


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def col(row, *names):
    """Find a value by loose column name match."""
    low = {k.lower().replace("_", "").replace(".", ""): v for k, v in row.items() if k}
    for n in names:
        n = n.lower().replace("_", "").replace(".", "")
        if n in low:
            return low[n]
    for n in names:
        n = n.lower()
        for k, v in low.items():
            if n in k:
                return v
    return ""


def days_since(value):
    if not value or value.startswith("1970") or value.lower() in ("never", "none"):
        return None
    try:
        t = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=dt.timezone.utc)
        return (dt.datetime.now(dt.timezone.utc) - t).days
    except ValueError:
        return None


def users_summary(path):
    out = {"total": 0, "active": 0, "no_2sv": [], "admins": [], "suspended": 0, "never_logged_in": [], "idle_90": []}
    for r in rows(path):
        email = col(r, "primaryEmail", "email")
        out["total"] += 1
        if col(r, "suspended").lower() in TRUTHY or col(r, "archived").lower() in TRUTHY:
            out["suspended"] += 1
            continue
        out["active"] += 1
        if col(r, "isEnrolledIn2Sv").lower() not in TRUTHY:
            out["no_2sv"].append(email)
        if col(r, "isAdmin").lower() in TRUTHY or col(r, "isDelegatedAdmin").lower() in TRUTHY:
            out["admins"].append(email)
        last = col(r, "lastLoginTime")
        d = days_since(last)
        if d is None and last:
            out["never_logged_in"].append(email)
        elif d is not None and d >= 90:
            out["idle_90"].append(email)
    return out


def tokens_summary(path):
    apps = {}
    for r in rows(path):
        name = col(r, "displayText", "displayName", "clientId") or "unknown app"
        user = col(r, "user", "primaryEmail")
        scopes = col(r, "scopes")
        a = apps.setdefault(name, {"users": set(), "mail": False, "files": False, "admin": False})
        a["users"].add(user)
        for k, needles in RISKY_SCOPES.items():
            if any(n in scopes for n in needles):
                a[k] = True
    return apps


def drive_summary(path):
    out = []
    for r in rows(path):
        out.append({"name": col(r, "name", "title"), "owner": col(r, "owners0emailAddress", "owners", "owner", "Owner"),
                    "type": col(r, "mimeType")})
    return out


def main():
    ap = argparse.ArgumentParser(description="Summarise GAM read-only exports")
    ap.add_argument("--users")
    ap.add_argument("--tokens")
    ap.add_argument("--drive")
    ap.add_argument("--names", action="store_true", help="include who and what (for the owner's report only)")
    ap.add_argument("--json")
    a = ap.parse_args()
    result = {}
    if a.users:
        u = users_summary(a.users)
        result["users"] = u
        print(f"People: {u['active']} active accounts ({u['suspended']} suspended)")
        print(f"  Without two-step login: {len(u['no_2sv'])}")
        print(f"  Admins: {len(u['admins'])}")
        print(f"  Never signed in: {len(u['never_logged_in'])} | not used in 90+ days: {len(u['idle_90'])}")
        if a.names:
            for k in ("no_2sv", "admins", "never_logged_in", "idle_90"):
                if u[k]:
                    print(f"    {k}: {', '.join(u[k])}")
    if a.tokens:
        apps = tokens_summary(a.tokens)
        mail = [n for n, v in apps.items() if v["mail"]]
        files = [n for n, v in apps.items() if v["files"]]
        result["apps"] = {n: {**v, "users": len(v["users"])} for n, v in apps.items()}
        print(f"Connected apps: {len(apps)} | can read or send email: {len(mail)} | can read or change files: {len(files)}")
        if a.names:
            for n, v in sorted(apps.items(), key=lambda x: -len(x[1]["users"])):
                tags = [k for k in ("mail", "files", "admin") if v[k]]
                print(f"    {n}: {len(v['users'])} people{(' | ' + ', '.join(tags)) if tags else ''}")
    if a.drive:
        files = drive_summary(a.drive)
        result["drive_public"] = len(files)
        print(f"Files open to anyone with the link or public: {len(files)}")
        if a.names:
            for f in files[:200]:
                print(f"    {f['name']} ({f['owner']})")
            result["drive_public_files"] = files
    if not result:
        ap.print_help()
        return 1
    if a.json:
        if not a.names and "users" in result:
            result["users"] = {k: (len(v) if isinstance(v, list) else v) for k, v in result["users"].items()}
        with open(a.json, "w") as fh:
            json.dump(result, fh, indent=2, default=list)


if __name__ == "__main__":
    sys.exit(main())
