#!/usr/bin/env python3
"""
website_grade.py: what grade does the website get, and when does its padlock certificate run out?

What it does
  1. Asks Mozilla's free HTTP Observatory (MDN, API v2) to grade the site A+ to F,
     then reads which of its tests failed and explains them in plain English.
  2. Opens one normal secure connection to the site to read the certificate's
     expiry date (Python ssl), the same thing a browser does.
  Rates area 10 (Website) red, amber or green using references/checks/website-grade.md.

What it touches
  observatory-api.mdn.mozilla.net (public, no key) and one HTTPS visit to the
  site's home page. No logins, no form posts, no attack traffic. The Observatory
  result is public and is cached by Mozilla for a few minutes.

Usage
  python3 -I website_grade.py example.com.au
  python3 -I website_grade.py example.com.au www.example.com.au --json out.json

Credit: grading by the MDN HTTP Observatory (Mozilla). Standard library only.
Part of the Founder OS security module (Driven Young). Read-only.
"""
import argparse
import datetime as dt
import json
import os
import socket
import ssl
import sys
import urllib.error
import urllib.request

API = "https://observatory-api.mdn.mozilla.net/api/v2"

PLAIN = {
    "content-security-policy": ("Content rules (CSP)", "A list of where your site is allowed to load code from. Stops injected scripts.",
                                "Ask your web person to add a Content-Security-Policy header, or tighten it (remove 'unsafe-inline' if the site allows)."),
    "strict-transport-security": ("Always-secure (HSTS)", "Tells browsers to only ever use the padlock version of your site.",
                                  "Turn on HSTS in your host (Cloudflare: SSL/TLS, Edge Certificates, HSTS) or ask your web person."),
    "redirection": ("Padlock redirect", "Visitors who type http:// should be sent to the secure https:// version.",
                    "Turn on 'Always use HTTPS' in your host (Cloudflare: SSL/TLS, Edge Certificates) or site builder."),
    "x-frame-options": ("Clickjacking guard", "Stops other sites hiding your pages inside theirs to trick clicks.",
                        "Add X-Frame-Options: SAMEORIGIN, or frame-ancestors 'self' in the CSP."),
    "x-content-type-options": ("File type guard", "Stops browsers guessing file types, a known trick.",
                               "Add the header X-Content-Type-Options: nosniff."),
    "referrer-policy": ("Referrer policy", "Controls what your page addresses leak to other sites.",
                        "Add Referrer-Policy: strict-origin-when-cross-origin."),
    "cookies": ("Cookies", "Login cookies should be marked Secure and HttpOnly.",
                "Ask your web person to set Secure, HttpOnly and SameSite on cookies."),
    "subresource-integrity": ("Outside scripts", "Scripts loaded from other sites should be pinned so they can't be swapped.",
                              "Ask your web person to add integrity= to outside scripts, or host them yourself."),
    "cross-origin-resource-sharing": ("Data sharing (CORS)", "Other sites shouldn't be able to read your site's data.",
                                      "Ask your web person to limit Access-Control-Allow-Origin."),
}


def http(method, url, timeout=30):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "FounderOS-security-check/1.0"})
    for ctx in (ssl.create_default_context(),
                ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else None):
        if ctx is None:
            continue
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                return json.loads(r.read())
        except urllib.error.URLError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e):
                continue
            raise
    raise RuntimeError("Could not make a secure connection (certificate store problem on this computer).")


def cert_days(host, port=443):
    """Days until the certificate expires, plus issuer. Raises on a bad or expired certificate."""
    last = None
    for cafile in (None, "/etc/ssl/cert.pem"):
        try:
            ctx = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
            with socket.create_connection((host, port), timeout=15) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as s:
                    c = s.getpeercert()
            exp = dt.datetime.fromtimestamp(ssl.cert_time_to_seconds(c["notAfter"]), dt.timezone.utc)
            issuer = dict(x[0] for x in c.get("issuer", ())).get("organizationName", "unknown")
            return (exp - dt.datetime.now(dt.timezone.utc)).days, exp.date().isoformat(), issuer
        except ssl.SSLCertVerificationError as e:
            last = e
            if "unable to get local issuer" in str(e):
                continue
            raise
    raise last


def grade_rank(g):
    order = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]
    return order.index(g) if g in order else len(order)


def check(host):
    r = {"host": host, "findings": []}
    f = r["findings"]

    def add(sev, issue, fix):
        f.append({"severity": sev, "issue": issue, "fix": fix})

    # Certificate
    try:
        days, exp, issuer = cert_days(host)
        r.update(cert_days_left=days, cert_expires=exp, cert_issuer=issuer)
        if days < 0:
            add("high", f"The padlock certificate expired on {exp}. Browsers show a big warning.", "Renew it today in your host or site builder.")
        elif days <= 14:
            add("high", f"The padlock certificate runs out in {days} days ({exp}).", "Renew it, or check auto-renew is on with your host.")
        elif days <= 30:
            add("medium", f"The padlock certificate runs out in {days} days ({exp}).", "Check auto-renew is on with your host.")
    except Exception as e:
        r["cert_error"] = str(e)[:200]
        add("high", "Couldn't make a secure (padlock) connection to the site.", "Check the site loads with https:// and ask your host about the certificate.")

    # Observatory grade
    try:
        scan = http("POST", f"{API}/scan?host={host}")
        r.update(grade=scan.get("grade"), score=scan.get("score"), tests_failed=scan.get("tests_failed"),
                 tests_quantity=scan.get("tests_quantity"), details_url=scan.get("details_url"))
        if scan.get("error"):
            r["observatory_error"] = scan["error"]
        try:
            det = http("GET", f"{API}/analyze?host={host}")
            failed = [k for k, t in (det.get("tests") or {}).items() if t.get("pass") is False]
            r["failed_tests"] = failed
            for k in failed:
                name, why, fix = PLAIN.get(k, (k, "", "See the Observatory page for this test."))
                add("low", f"{name} missing or weak. {why}", fix)
        except Exception as e:
            r["details_error"] = str(e)[:200]
    except Exception as e:
        r["observatory_error"] = str(e)[:200]

    g = r.get("grade")
    if g:
        rank = grade_rank(g)
        # Grade drives severity of the header findings: C/D = medium, F = high
        if rank >= grade_rank("F"):
            for x in f:
                if x["severity"] == "low":
                    x["severity"] = "high"
        elif rank >= grade_rank("C+"):
            for x in f:
                if x["severity"] == "low":
                    x["severity"] = "medium"

    sevs = [x["severity"] for x in f]
    if g is None and "cert_days_left" not in r:
        r["rating"] = "not checked"
    elif "high" in sevs or g == "F":
        r["rating"] = "red"
    elif "medium" in sevs or (g and grade_rank(g) > grade_rank("B-")):
        r["rating"] = "amber"
    else:
        r["rating"] = "green" if g else "amber"
    return r


def main():
    ap = argparse.ArgumentParser(description="Website grade + certificate check (public lookups only)")
    ap.add_argument("hosts", nargs="+")
    ap.add_argument("--json")
    a = ap.parse_args()
    out = []
    for h in a.hosts:
        h = h.strip().lower().removeprefix("https://").removeprefix("http://").split("/")[0]
        r = check(h)
        out.append(r)
        print(f"Website grade for {h}: {r.get('grade', '?')} ({r.get('score', '?')}/100), "
              f"certificate {r.get('cert_days_left', '?')} days left -> {r['rating'].upper()}")
        for x in r["findings"]:
            print(f"  [{x['severity']}] {x['issue']}\n      Fix: {x['fix']}")
        if r.get("details_url"):
            print("  Full results: " + r["details_url"])
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(out, fh, indent=2)


if __name__ == "__main__":
    sys.exit(main())
