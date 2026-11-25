#!/usr/bin/env python3
"""
password_check.py: is this password on a known list of leaked passwords?

What it does
  The owner types a password (it's hidden as they type). This script scrambles
  it on their own computer (SHA-1), sends ONLY THE FIRST 5 CHARACTERS of the
  scramble to Have I Been Pwned's free Pwned Passwords service, gets back a list
  of every leaked scramble that starts the same way (hundreds of them, padded so
  the reply size gives nothing away), and checks for a match on this computer.
  This is HIBP's "k-anonymity" method: HIBP never sees the password or its full
  scramble, and can't work out which one was checked.

What it touches
  api.pwnedpasswords.com/range/<5 characters>, nothing else. No key needed.
  The password and its scramble are never printed, logged, saved or sent.

Rules for Claude
  The OWNER runs this in their own Terminal and types the password themselves.
  Claude never asks for, sees, or passes in a password. There is deliberately no
  command-line option for the password, so it can't end up in shell history.

Usage
  python3 -I password_check.py          (asks for the password, hidden)
  python3 -I password_check.py --many   (check several, one after another; blank line to stop)

Credit: Pwned Passwords by Troy Hunt, haveibeenpwned.com (CC BY 4.0).
Part of the Founder OS security module (Driven Young). Read-only.
"""
import argparse
import getpass
import hashlib
import os
import ssl
import sys
import urllib.error
import urllib.request

RANGE = "https://api.pwnedpasswords.com/range/"


def fetch_range(prefix):
    req = urllib.request.Request(RANGE + prefix, headers={
        "Add-Padding": "true",
        "User-Agent": "FounderOS-security-check/1.0",
    })
    for cafile in (None, "/etc/ssl/cert.pem"):
        if cafile and not os.path.exists(cafile):
            continue
        try:
            ctx = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.URLError as e:
            if cafile is None and "CERTIFICATE_VERIFY_FAILED" in str(e):
                continue
            raise
    raise RuntimeError("Could not reach Pwned Passwords securely.")


def times_seen(secret):
    """Return how many times this password appears in known leaks (0 = not found)."""
    digest = hashlib.sha1(secret.encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]
    del digest
    for line in fetch_range(prefix).splitlines():
        s, _, count = line.strip().partition(":")
        if s == suffix:
            n = int(count or 0)
            return n  # padding rows have a count of 0
    return 0


def check_one():
    secret = getpass.getpass("Type the password to check (hidden), then press Enter: ")
    if not secret:
        return None
    try:
        n = times_seen(secret)
    finally:
        secret = None  # drop our reference straight away
    if n:
        print(f"  LEAKED: this password is on known leak lists ({n:,} times). Stop using it everywhere, today.")
        print("  Fix: change it on every account that uses it, to a new one made by a password manager.")
    else:
        print("  Not found on any known leak list. Good. (That doesn't make a short or reused password safe.)")
    return n


def main():
    ap = argparse.ArgumentParser(description="Password leak check (k-anonymity, the password never leaves this computer)")
    ap.add_argument("--many", action="store_true", help="check several passwords in a row")
    a = ap.parse_args()
    print("Password leak check. Only 5 characters of a scramble leave this computer. Nothing is saved.")
    leaked = checked = 0
    while True:
        n = check_one()
        if n is None:
            break
        checked += 1
        leaked += 1 if n else 0
        if not a.many:
            break
    if checked:
        # The only thing worth telling Claude: counts, never the passwords.
        print(f"Summary for the report: {checked} checked, {leaked} on a leak list.")


if __name__ == "__main__":
    sys.exit(main())
