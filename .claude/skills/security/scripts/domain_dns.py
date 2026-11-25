#!/usr/bin/env python3
"""
domain_dns.py: is the business's domain name locked down?

What it does (all public lookups, no login)
  1. Registrar lock: asks the public RDAP service (rdap.org, the modern WHOIS)
     whether the domain has "transfer prohibited" set, when it expires, and
     whether DNSSEC is on.
  2. CAA records: checks the domain says which companies may issue its padlock
     certificates.
  3. Dangling DNS: for a list of likely subdomains (www, shop, blog, mail...,
     plus any the owner names, plus optional names from public certificate logs),
     finds ones that point (CNAME) at an outside service whose address no longer
     exists. A scammer can often claim that service and run a site on your name.
  Rates the "Domain and DNS" part of area 9 using references/checks/domain-dns.md.

What it touches
  Public DNS (dig, or DNS-over-HTTPS at Cloudflare), rdap.org, and with --ct
  the public certificate log search at crt.sh. No connection to the subdomains
  themselves, no scanning.

Usage
  python3 -I domain_dns.py example.com.au
  python3 -I domain_dns.py example.com.au --subdomains bookings,portal --ct --json out.json

Idea credit: a community app-security checklist (ideas only, no text copied).
Part of the Founder OS security module (Driven Young). Read-only. Standard library only.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

COMMON_SUBS = ["www", "mail", "webmail", "shop", "store", "blog", "app", "portal", "bookings", "book",
               "admin", "dev", "staging", "test", "old", "new", "beta", "help", "support", "docs",
               "go", "link", "links", "news", "events", "members", "login", "pay", "my", "crm",
               "email", "click", "track", "info", "landing", "promo", "api", "cdn", "status"]

# Services where an unclaimed name can usually be taken over (CNAME target suffixes)
TAKEOVER_PRONE = ["herokuapp.com", "herokudns.com", "github.io", "azurewebsites.net", "cloudapp.net",
                  "trafficmanager.net", "blob.core.windows.net", "cloudfront.net", "s3.amazonaws.com",
                  "s3-website", "elasticbeanstalk.com", "netlify.app", "netlify.com", "vercel.app",
                  "pages.dev", "workers.dev", "surge.sh", "bitbucket.io", "ghost.io", "myshopify.com",
                  "wpengine.com", "pantheonsite.io", "zendesk.com", "helpscoutdocs.com", "readme.io",
                  "webflow.io", "wixdns.net", "squarespace.com", "unbouncepages.com", "leadpages.net",
                  "fly.dev", "onrender.com", "firebaseapp.com", "web.app", "framer.app", "carrd.co"]


def https_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "FounderOS-security-check/1.0", **(headers or {})})
    for cafile in (None, "/etc/ssl/cert.pem"):
        if cafile and not os.path.exists(cafile):
            continue
        try:
            ctx = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                return json.loads(r.read())
        except urllib.error.URLError as e:
            if cafile is None and "CERTIFICATE_VERIFY_FAILED" in str(e):
                continue
            raise
    raise RuntimeError("secure connection failed")


def dns(name, rtype):
    """Return (status, answers). status: NOERROR / NXDOMAIN / other. Answers for the exact type only."""
    if shutil.which("dig"):
        try:
            out = subprocess.run(["dig", "+noall", "+answer", "+comments", "+time=3", "+tries=2", rtype, name],
                                 capture_output=True, text=True, timeout=15).stdout
            m = re.search(r"status: (\w+)", out)
            status = m.group(1) if m else "UNKNOWN"
            ans = []
            for line in out.splitlines():
                if line.startswith(";") or not line.strip():
                    continue
                parts = line.split(None, 4)
                if len(parts) == 5 and parts[3].upper() == rtype.upper():
                    ans.append(parts[4].strip())
            return status, ans
        except Exception:
            pass
    q = urllib.parse.urlencode({"name": name, "type": rtype})
    d = https_json("https://cloudflare-dns.com/dns-query?" + q, {"accept": "application/dns-json"})
    status = {0: "NOERROR", 3: "NXDOMAIN", 2: "SERVFAIL"}.get(d.get("Status"), str(d.get("Status")))
    tnum = {"A": 1, "CNAME": 5, "CAA": 257, "AAAA": 28}.get(rtype.upper())
    return status, [a.get("data", "") for a in d.get("Answer", []) or [] if a.get("type") == tnum]


def rdap(domain):
    try:
        d = https_json("https://rdap.org/domain/" + urllib.parse.quote(domain))
    except Exception as e:
        return {"error": str(e)[:160]}
    status = [s.lower() for s in d.get("status", [])]
    exp = next((e.get("eventDate") for e in d.get("events", []) if e.get("eventAction") == "expiration"), None)
    registrar = None
    for ent in d.get("entities", []) or []:
        if "registrar" in (ent.get("roles") or []):
            for item in (ent.get("vcardArray") or [None, []])[1]:
                if item and item[0] == "fn":
                    registrar = item[3]
    return {"status": status, "expires": exp, "registrar": registrar,
            "dnssec": bool((d.get("secureDNS") or {}).get("delegationSigned"))}


def ct_names(domain):
    try:
        rows = https_json("https://crt.sh/?q=%25." + urllib.parse.quote(domain) + "&output=json", timeout=40)
    except Exception:
        return []
    names = set()
    for r in rows:
        for n in str(r.get("name_value", "")).splitlines():
            n = n.strip().lower().lstrip("*.")
            if n.endswith("." + domain):
                names.add(n[: -len(domain) - 1])
    return sorted(names)[:200]


def check(domain, extra_subs, use_ct):
    r = {"domain": domain, "findings": []}
    f = r["findings"]

    def add(sev, issue, fix):
        f.append({"severity": sev, "issue": issue, "fix": fix})

    # 1. Registrar lock (RDAP)
    rd = rdap(domain)
    r["rdap"] = rd
    if "error" in rd:
        r["rdap_note"] = "Registry lookup didn't answer. Ask the owner to check the lock in their registrar account."
    else:
        if not any("transfer prohibited" in s for s in rd["status"]):
            add("medium", "The domain isn't locked against transfers. Someone who gets into your registrar account, or tricks the registrar, can move it.",
                "In your domain registrar (where you pay for the domain), turn on 'domain lock' or 'transfer lock'. Also turn on two-step login there.")
        if rd.get("expires"):
            try:
                days = (dt.datetime.fromisoformat(rd["expires"].replace("Z", "+00:00")) - dt.datetime.now(dt.timezone.utc)).days
                r["domain_days_left"] = days
                if days < 0:
                    add("high", "The domain registration has expired.", "Renew it today with your registrar.")
                elif days <= 30:
                    add("high", f"The domain expires in {days} days. If it lapses, your email and website stop and someone else can buy it.",
                        "Renew it and turn on auto-renew with a card that won't expire.")
                elif days <= 60:
                    add("low", f"The domain expires in {days} days.", "Check auto-renew is on with your registrar.")
            except ValueError:
                pass
        if not rd.get("dnssec"):
            add("low", "DNSSEC is off (a tamper seal on your domain's records).",
                "Optional. If your DNS host offers one-click DNSSEC (Cloudflare does), turn it on.")

    # 2. CAA
    st, caa = dns(domain, "CAA")
    r["caa"] = caa
    if not caa:
        add("low", "No CAA record, so any certificate company can issue a padlock certificate for your domain.",
            "Add CAA records naming the certificate companies your host uses (your host's help page lists them).")

    # 3. Dangling DNS
    subs = list(dict.fromkeys(COMMON_SUBS + extra_subs + (ct_names(domain) if use_ct else [])))
    r["subdomains_checked"] = len(subs)
    dangling, prone = [], []
    for s in subs:
        name = f"{s}.{domain}"
        st, cn = dns(name, "CNAME")
        if not cn:
            continue
        target = cn[0].rstrip(".").lower()
        tst, ta = dns(target, "A")
        _, taaaa = dns(target, "AAAA") if not ta else (None, ["x"])
        if tst == "NXDOMAIN" or (not ta and not taaaa):
            dangling.append({"name": name, "points_to": target})
        elif any(target.endswith(p) or p in target for p in TAKEOVER_PRONE):
            prone.append({"name": name, "points_to": target})
    r["dangling"] = dangling
    r["outside_services"] = prone
    for d in dangling:
        svc = next((p for p in TAKEOVER_PRONE if p in d["points_to"]), None)
        add("high" if svc else "medium",
            f"{d['name']} points to {d['points_to']}, which doesn't exist any more. "
            + ("Someone could claim that name on the service and put up a site on your domain." if svc else "It's a loose end."),
            f"Delete the {d['name']} record in your DNS, or set the service back up if you still need it.")

    sevs = [x["severity"] for x in f]
    r["rating"] = "red" if "high" in sevs else "amber" if "medium" in sevs else "green"
    return r


def main():
    ap = argparse.ArgumentParser(description="Domain and DNS check (public lookups only)")
    ap.add_argument("domain")
    ap.add_argument("--subdomains", help="extra subdomain names, comma separated (e.g. bookings,portal)")
    ap.add_argument("--ct", action="store_true", help="also find subdomain names in public certificate logs (crt.sh)")
    ap.add_argument("--json")
    a = ap.parse_args()
    domain = a.domain.strip().lower().removeprefix("https://").removeprefix("http://").split("/")[0]
    extra = [s.strip().lower() for s in a.subdomains.split(",")] if a.subdomains else []
    r = check(domain, extra, a.ct)
    rd = r.get("rdap", {})
    print(f"Domain and DNS check for {domain}: {r['rating'].upper()}")
    print(f"  Transfer lock: {'on' if any('transfer prohibited' in s for s in rd.get('status', [])) else 'off or unknown'} | "
          f"expires: {rd.get('expires', '?')} | DNSSEC: {'on' if rd.get('dnssec') else 'off'} | CAA: {'set' if r['caa'] else 'none'}")
    print(f"  Subdomains checked: {r['subdomains_checked']} | dangling: {len(r['dangling'])} | pointing at outside services: {len(r['outside_services'])}")
    for x in r["findings"]:
        print(f"  [{x['severity']}] {x['issue']}\n      Fix: {x['fix']}")
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(r, fh, indent=2)


if __name__ == "__main__":
    sys.exit(main())
