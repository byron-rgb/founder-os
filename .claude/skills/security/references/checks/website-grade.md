# Check: Website grade

**Answers for the owner:** what grade does your website get for security (A+ to F), and is the padlock certificate about to run out?

**Needs:** the website address (from `Stack.md`). No login. Public lookups only.
**Feeds area:** 10 (Website).
**Time:** about a minute per site.

## What it is

Mozilla runs a free public grader, the MDN HTTP Observatory. It looks at the safety settings a website sends to browsers (the "headers"), not at the content. A site can look great and still get an F. Most small business sites score C or D. Most fixes are a setting in the host or a job for the web person.

The certificate is the padlock. If it runs out, browsers show a full-page warning and customers leave.

## How to run it

1. Get the website address(es) from `Stack.md`. Include the booking or shop site if it's separate, and any customer login portal.
2. Run:
   ```
   python3 -I scripts/website_grade.py theirsite.com.au www.theirsite.com.au --json "Security/runs/TODAY/website.json"
   ```
   The script asks the Observatory to grade each site (one request to `observatory-api.mdn.mozilla.net`, API v2), reads which tests failed, then opens one normal secure connection to read the certificate's expiry. That's all. No logins, no forms, nothing a normal visitor wouldn't do.
3. Without Python: open `https://developer.mozilla.org/en-US/observatory/analyze?host=theirsite.com.au` in a browser for the grade, and click the padlock in the address bar, then "Connection is secure", then the certificate, to see the expiry date.
4. Never run attack or "pen test" tools against the site in this check. That's the code check add-on, and only with written OK.

## How to read the result

| Failed test | Plain words | Who fixes it |
|---|---|---|
| Content rules (CSP) | No list of where the site may load code from | Web person. Often a bigger job; a starter policy is fine |
| Always-secure (HSTS) | Browsers aren't told to always use the padlock | Host setting (Cloudflare: one switch) |
| Padlock redirect | Typing `http://` doesn't go to the secure version | Host setting ("Always use HTTPS") |
| Clickjacking guard | Other sites can frame the pages | Web person or host |
| File type guard (nosniff) | Browser may guess file types | Web person or host |
| Cookies | Login cookies missing safety flags | Web person |
| Outside scripts (SRI) | Scripts from other sites aren't pinned | Web person |

Site builders: Wix, Squarespace and Shopify control most headers themselves. If they're on one of those and the grade is low, say so plainly: "This is mostly set by Wix. It's not something you did wrong." Rate it, note it, keep the severity at low, and focus on what they can change (certificate, redirect, their own add-ons).

## Red, amber, green (area 10)

- **Green:** grade B- or better, and the certificate has more than 30 days left.
- **Amber:** grade C+ to D-, or the certificate runs out within 30 days.
- **Red:** grade F, no working padlock, or the certificate has expired or runs out within 14 days.
- **Not checked:** the Observatory didn't answer and you couldn't read the certificate.

If there are several sites, rate the area by the worst one and list each in the report.

## Plain-English fixes

1. **Certificate expiring or expired (high).** "Your host normally renews this by itself. Log in to your host and check auto-renew is on." Cloudflare, Wix, Squarespace and Shopify renew automatically, so an expiry warning there usually means the site has moved or the domain isn't pointing where they think.
2. **Padlock redirect missing (medium).** Cloudflare: SSL/TLS, Edge Certificates, turn on "Always Use HTTPS". WordPress hosts: usually a "Force HTTPS" switch in the hosting panel.
3. **HSTS missing (medium).** Cloudflare: SSL/TLS, Edge Certificates, HSTS, enable with a 6 month max age. Only once the whole site works on https. Otherwise ask the web person.
4. **CSP, clickjacking, nosniff (medium for C/D, low for B).** A note to forward to the web person, in plain words, listing the failed tests and linking the Observatory results page. Draft it for the owner; they send it.
5. **Low grade on a hosted builder (low).** Nothing to do now. Check again monthly.

## Credit

Grading by the MDN HTTP Observatory (Mozilla). Free public API, no key. Credit Mozilla in the report under "Checks run".
