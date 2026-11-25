#!/usr/bin/env python3
"""
email_spoofing.py: can a scammer send email that looks like it's from this domain?

What it does
  Looks up the public email protection records for one domain (SPF, DKIM,
  DMARC, plus MX, MTA-STS and TLS reporting) and rates them red, amber or green
  using the rules in references/checks/email-spoofing.md.

What it touches
  Public DNS only. Same lookups any mail server does when it gets an email from
  you. No login, no email sent, no connection to the mail servers themselves.
  Order of tools: checkdmarc (if installed, for deeper SPF checks), then the
  `dig` command, then DNS-over-HTTPS (Cloudflare 1.1.1.1). Standard library only.

Usage
  python3 -I email_spoofing.py example.com.au
  python3 -I email_spoofing.py example.com.au --selectors google,s1 --json out.json
  python3 -I email_spoofing.py example.com.au --checkdmarc ~/path/to/venv/bin/checkdmarc

Output
  A plain-English summary on screen, and (with --json) the raw results and
  ratings for the report. Never prints anything secret: these are public records.

Part of the Founder OS security module (Driven Young). Read-only.
"""
import argparse
import base64
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request

COMMON_SELECTORS = [
    "google",                      # Google Workspace
    "selector1", "selector2",      # Microsoft 365
    "k1", "k2", "k3",              # Mailchimp / Mandrill, Klaviyo
    "s1", "s2",                    # SendGrid
    "mx", "smtp", "mailo", "pic", "krs",  # Mailgun styles (GoHighLevel uses Mailgun)
    "default", "dkim", "mail", "zoho", "zmail",
    "protonmail", "protonmail2", "protonmail3",
    "everlytickey1", "everlytickey2", "cm", "hs1", "hs2", "sig1",
]


def https_get(url, headers=None, timeout=15):
    """GET with the system certificates, falling back to /etc/ssl/cert.pem (some Mac Pythons)."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" not in str(e) or not os.path.exists("/etc/ssl/cert.pem"):
            raise
        ctx = ssl.create_default_context(cafile="/etc/ssl/cert.pem")
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read()


def txt_lookup(name, rtype="TXT"):
    """Return a list of record strings. Tries dig, then DNS-over-HTTPS."""
    if shutil.which("dig"):
        try:
            out = subprocess.run(["dig", "+short", "+time=3", "+tries=2", rtype, name],
                                 capture_output=True, text=True, timeout=15).stdout
            lines = [l.strip() for l in out.splitlines() if l.strip() and not l.startswith(";")]
            if rtype == "TXT":
                # dig splits long TXT records into quoted chunks: join them
                return ["".join(re.findall(r'"([^"]*)"', l)) for l in lines if l.startswith('"')]
            return lines
        except Exception:
            pass
    q = urllib.parse.urlencode({"name": name, "type": rtype})
    data = json.loads(https_get("https://cloudflare-dns.com/dns-query?" + q,
                                {"accept": "application/dns-json"}))
    out = []
    for a in data.get("Answer", []) or []:
        if rtype == "TXT" and a.get("type") != 16:
            continue
        d = a.get("data", "")
        if rtype == "TXT" and d.startswith('"'):
            d = "".join(re.findall(r'"([^"]*)"', d))
        out.append(d)
    return out


def dkim_key_bits(record):
    """Rough RSA key size from the p= value (public data). None if unknown."""
    for part in record.split(";"):
        part = part.strip()
        if part.startswith("p="):
            p = part[2:].replace(" ", "")
            if not p:
                return 0  # empty p= means the key was revoked
            try:
                n = len(base64.b64decode(p + "=" * (-len(p) % 4)))
            except Exception:
                return None
            if n < 200:
                return 1024
            if n < 330:
                return 2048
            return 4096
    return None


def run_checkdmarc(path, domain):
    try:
        out = subprocess.run([path, domain], capture_output=True, text=True, timeout=120).stdout
        return json.loads(out)
    except Exception as e:
        return {"error": f"checkdmarc failed: {e}"}


def rate(domain, selectors, checkdmarc_path=None):
    r = {"domain": domain, "tool": "dns", "findings": []}
    f = r["findings"]

    def add(sev, text, fix):
        f.append({"severity": sev, "issue": text, "fix": fix})

    # dig +short follows CNAMEs and prints them: keep only real "priority host" MX lines
    r["mx"] = [m for m in txt_lookup(domain, "MX") if re.match(r"^\d+\s+\S+", m) and m.split()[-1] != "."]  # "0 ." = null MX, no email
    sends_email = bool(r["mx"])
    labels = domain.split(".")
    if not r["mx"] and not txt_lookup(domain, "NS") and not txt_lookup(domain, "SOA") and not txt_lookup(domain, "A") and not txt_lookup(domain):
        r["rating"] = "not checked"
        r["note"] = "This domain wasn't found in DNS. Check the spelling with the owner."
        return r

    # SPF
    spf = [t for t in txt_lookup(domain) if t.lower().startswith("v=spf1")]
    r["spf"] = spf
    if not spf and not sends_email and len(labels) > 2:
        add("low", "This subdomain has no SPF record. It doesn't handle email, so it's a small gap.",
            "Add an SPF record 'v=spf1 -all' on it, which says 'nobody sends email from here'.")
    elif not spf:
        add("high", "No SPF record, so there's no list of who's allowed to send email as you.",
            "Add an SPF record in your domain's DNS. Your email provider's help page gives the exact line.")
    elif len(spf) > 1:
        add("high", "Two SPF records. Mail servers treat that as broken.", "Merge them into one record.")
    else:
        s = spf[0].lower()
        if "+all" in s:
            add("high", "SPF ends in +all, which lets anyone in the world send as you.", "Change +all to ~all or -all.")
        elif "?all" in s or not any(x in s for x in ("~all", "-all", "redirect=")):
            add("medium", "SPF doesn't tell mail servers to distrust other senders.", "End the SPF record with ~all or -all.")

    # DMARC
    dmarc = [t for t in txt_lookup("_dmarc." + domain) if t.lower().startswith("v=dmarc1")]
    inherited = None
    # A subdomain without its own DMARC is covered by the main domain's record (its sp= value)
    i = 1
    while not dmarc and len(labels) - i >= 2:
        parent = ".".join(labels[i:])
        dmarc = [t for t in txt_lookup("_dmarc." + parent) if t.lower().startswith("v=dmarc1")]
        if dmarc:
            inherited = parent
        i += 1
    r["dmarc"] = dmarc
    r["dmarc_from"] = inherited or domain
    policy = None
    if not dmarc:
        add("high", "No DMARC record. Scammers can send email that looks exactly like it's from you, and nothing stops it.",
            "Add a DMARC record. Start at p=quarantine if your email provider is the only sender, or p=none for 2 weeks first if you use other tools that send email.")
    else:
        tags = {}
        for part in dmarc[0].split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                tags[k.strip().lower()] = v.strip()
        policy = tags.get("p", "").lower()
        if inherited:
            policy = tags.get("sp", policy).lower()
        r["dmarc_policy"] = policy + (f" (from {inherited})" if inherited else "")
        pct = tags.get("pct", "100")
        if policy == "none":
            add("medium", "DMARC is set to 'monitor only' (p=none). Fake emails still get delivered.",
                "Change p=none to p=quarantine once your real email tools are all passing.")
        elif policy not in ("quarantine", "reject"):
            add("high", "DMARC record is set up wrong, so it does nothing.", "Fix the p= value to quarantine or reject.")
        elif pct != "100":
            add("low", f"DMARC only applies to {pct}% of email.", "Remove pct= or set it to 100.")
        if "rua" not in tags:
            add("low", "DMARC has no report address, so you never see who's sending as you.",
                "Add rua=mailto:you@yourdomain to the DMARC record (or a free DMARC report service).")
        if tags.get("sp", "").lower() == "none" and policy in ("quarantine", "reject"):
            add("medium", "Subdomains are left on 'monitor only' (sp=none).", "Remove sp=none or set it to quarantine.")

    # DKIM
    found = {}
    for sel in selectors:
        recs = [t for t in txt_lookup(f"{sel}._domainkey.{domain}") if "p=" in t]
        if recs:
            found[sel] = dkim_key_bits(recs[0])
    live = {k: v for k, v in found.items() if v != 0}
    empty = [k for k, v in found.items() if v == 0]
    r["dkim_selectors_found"] = live
    r["dkim_empty_selectors"] = len(empty)
    if sends_email and not live:
        add("medium", "Couldn't confirm DKIM (the digital signature on your email). It may be there under a name we didn't guess.",
            "Send yourself an email, open 'Show original' and look for 's=' in the DKIM-Signature line. Run the check again with that selector.")
    if empty and live:
        add("low", f"{len(empty)} old DKIM key name(s) are empty (switched off).", "Fine to leave. Tidy them up in DNS if you like.")
    for sel, bits in live.items():
        if bits == 1024:
            add("low", f"DKIM key '{sel}' is the older 1024-bit size.",
                "In your email admin, make a new 2048-bit DKIM key, add it to DNS, then switch to it.")

    # Nice-to-haves (low)
    r["mta_sts"] = bool(txt_lookup("_mta-sts." + domain))
    r["tls_rpt"] = bool(txt_lookup("_smtp._tls." + domain))

    if not sends_email:
        r["note"] = "No MX record: this domain (or subdomain) doesn't receive email. If it never sends email either, SPF 'v=spf1 -all' and DMARC p=reject lock it down."

    # Deeper SPF checks via checkdmarc
    if checkdmarc_path:
        cd = run_checkdmarc(checkdmarc_path, domain)
        r["tool"] = "checkdmarc"
        spf_cd = cd.get("spf", {}) if isinstance(cd, dict) else {}
        r["spf_dns_lookups"] = spf_cd.get("dns_lookups")
        if spf_cd and spf_cd.get("valid") is False:
            add("high", "checkdmarc says the SPF record is broken: " + str(spf_cd.get("error", ""))[:160],
                "Fix the SPF record (often too many include: entries).")
        elif isinstance(spf_cd.get("dns_lookups"), int) and spf_cd["dns_lookups"] >= 9:
            add("low", f"SPF uses {spf_cd['dns_lookups']} of its 10 allowed lookups. One more email tool will break it.",
                "Remove include: entries for tools you no longer use.")
        for w in (cd.get("dmarc", {}) or {}).get("warnings", []) if isinstance(cd, dict) else []:
            add("low", "checkdmarc DMARC warning: " + str(w)[:160], "See the DMARC record.")

    # Area 9 rating (references/essential-eight.md)
    sevs = [x["severity"] for x in f]
    if "high" in sevs:
        r["rating"] = "red"
    elif "medium" in sevs:
        r["rating"] = "amber"
    else:
        r["rating"] = "green"
    return r


def main():
    ap = argparse.ArgumentParser(description="Email spoofing check (public DNS only)")
    ap.add_argument("domain")
    ap.add_argument("--selectors", help="extra DKIM selectors, comma separated")
    ap.add_argument("--checkdmarc", help="path to checkdmarc (optional, for deeper SPF checks)")
    ap.add_argument("--json", help="write full results to this file")
    a = ap.parse_args()
    domain = a.domain.strip().lower().removeprefix("http://").removeprefix("https://").split("/")[0]
    sels = COMMON_SELECTORS + ([s.strip() for s in a.selectors.split(",")] if a.selectors else [])
    cd = a.checkdmarc or shutil.which("checkdmarc")
    r = rate(domain, list(dict.fromkeys(sels)), cd)
    print(f"Email spoofing check for {domain}: {r['rating'].upper()} (via {r['tool']})")
    if r["rating"] == "not checked":
        print("  " + r["note"])
        return
    print(f"  SPF: {'set' if r['spf'] else 'missing'} | DMARC: {r.get('dmarc_policy') or 'missing'} | "
          f"DKIM found: {', '.join(f'{k} ({v}-bit)' if v else k for k, v in r['dkim_selectors_found'].items()) or 'not confirmed'}")
    for x in r["findings"]:
        print(f"  [{x['severity']}] {x['issue']}\n      Fix: {x['fix']}")
    if r.get("note"):
        print("  Note: " + r["note"])
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(r, fh, indent=2)


if __name__ == "__main__":
    sys.exit(main())
