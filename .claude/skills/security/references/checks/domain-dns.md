# Check: Domain and DNS

**Answers for the owner:** is your domain name locked down, so nobody can steal it, hijack a forgotten part of it, or get a padlock certificate for it?

**Needs:** the business's domain (from `Stack.md`). No login. Public lookups only.
**Feeds area:** 9 (Email and domain protection).
**Time:** about a minute.

## Why it matters, in one line each

- **Transfer lock:** if someone gets into the registrar account (or talks the registrar round), they can move the domain away. Email and website go with it.
- **Expiry:** a lapsed domain stops email and the website, and can be bought by someone else.
- **Dangling subdomains:** an old `shop.` or `promo.` that still points at a service you've cancelled. Scammers can often claim that service and run a real-looking site on your name.
- **CAA:** a short list of which companies may issue padlock certificates for you. Low priority, cheap to add.
- **DNSSEC:** a tamper seal on the domain's records. Optional for small businesses; on if it's one click.

## How to run it

```
python3 -I scripts/domain_dns.py theirdomain.com.au --json "brain/Security/runs/TODAY/domain.json"
```

Options:
- `--subdomains bookings,portal,old-shop` adds names the owner mentions (old campaign pages, booking sites, a shop).
- `--ct` also looks up subdomain names in public certificate logs (crt.sh). Finds forgotten ones. Slower, sometimes times out. Use it at the first check and monthly.

The script looks at public DNS (dig, or DNS-over-HTTPS), the public RDAP registry service (rdap.org, the modern WHOIS), and with `--ct` crt.sh. It does not connect to or scan the subdomains.

Without Python:
- Lock and expiry: `https://rdap.org/domain/theirdomain.com.au` in a browser. Look for "client transfer prohibited" under status, and the "expiration" date. (Some registries, including .au, may not show an expiry date. Then ask the owner to check in their registrar account.)
- CAA: `dig +short CAA theirdomain.com.au`.
- Dangling: `dig +short CNAME shop.theirdomain.com.au`, then `dig +short A` on whatever it points to. No answer means dangling.

## How to read the result

| Shows | Meaning |
|---|---|
| Transfer lock: off or unknown | Not locked, or the registry didn't say. For .au domains the lock may not show in RDAP: ask the owner to check in their registrar |
| expires within 30 days | Renew now and turn on auto-renew |
| dangling: N | Subdomains pointing at nothing. Each is listed as a finding |
| pointing at outside services: N | Fine if they're in use (a Shopify store, a Netlify site). Ask the owner if each is still live |
| CAA: none | Low fix |

## Red, amber, green (area 9, domain part)

- **Green:** transfer lock on, expiry more than 30 days away with auto-renew, no dangling subdomains.
- **Amber:** transfer lock off, or a dangling subdomain that points at an ordinary host.
- **Red:** a dangling subdomain on a service that can be claimed (Heroku, GitHub Pages, Azure, Netlify, Vercel, Shopify and similar), or the domain expires within 30 days or has expired.

Area 9 overall = the worse of this and `email-spoofing.md`.

## Ask the owner (can't be seen from outside)

Add these to the accounts check (`accounts-and-2sv.md`). One question at a time:
1. "Where do you pay for your domain (the registrar)? Is two-step login on there?" Off = high. This account controls email and website.
2. "Is auto-renew on, with a card that won't expire soon?"
3. "Who else can log in to the registrar or the DNS (an old web designer)?"

## Plain-English fixes

1. **Dangling subdomain (high or medium).** "Delete the `shop` record in your DNS settings." Wherever their DNS lives (Cloudflare, GoDaddy, Crazy Domains, VentraIP, their web builder). Double check with the owner first that it's not something they still use.
2. **Transfer lock off (medium).** In the registrar: look for "Domain lock", "Registrar lock" or "Transfer lock" and turn it on. Some .au registrars lock by default and don't show it.
3. **Expiring domain (high).** Renew and turn on auto-renew. Check the card on file.
4. **Two-step login off on the registrar (high).** Turn it on today. Use an authenticator app if offered.
5. **No CAA (low).** Add CAA records for the certificate companies their host uses. Cloudflare and most hosts list theirs in their help pages. If unsure, skip it: low value for most owners.
6. **DNSSEC off (low).** Cloudflare: DNS, Settings, enable DNSSEC, then add the record it gives at the registrar if the registrar isn't Cloudflare. Optional.

## Credit

Idea from a community app-security checklist (ideas only, no text copied). RDAP via rdap.org (public bootstrap service). Certificate logs via crt.sh (Sectigo, public).
