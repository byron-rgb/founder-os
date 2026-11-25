# Check: Email spoofing

**Answers for the owner:** can a scammer send an email that looks like it's from your business? This is how most fake invoice and "change of bank details" scams start.

**Needs:** the business's email domain (from `Stack.md`). No login, no access. Public DNS lookups only.
**Feeds area:** 9 (Email and domain protection).
**Time:** under a minute.

## Plain words to use

| Say this | Not this |
|---|---|
| sender list | SPF |
| digital signature on your email | DKIM |
| spoofing protection, or "what happens to fakes" | DMARC |
| monitor only | p=none |
| send fakes to junk / block fakes | p=quarantine / p=reject |

## How to run it

1. Get the domain from `Stack.md` (the part after the @ in their email). Skip this check if they only use a Gmail, Outlook.com or Hotmail address, and log a low fix: "Get email on your own business name."
2. Run the helper (in this skill's `scripts/` folder):
   ```
   python3 -I scripts/email_spoofing.py THEIRDOMAIN.com.au --json "Security/runs/TODAY/email.json"
   ```
   - If the owner can tell you the DKIM selector (see "Finding the DKIM selector" below), add `--selectors thatname`.
   - If `checkdmarc` (Apache-2.0, by Sean Whalen) is installed, the script uses it for deeper sender-list checks: add `--checkdmarc /path/to/checkdmarc`. Optional. See `references/install.md` for setting it up in a private folder.
3. If Python isn't available, do it by hand with the fallback below.
4. Repeat for any other domain they send email from (a second brand, an old domain that still has email).

### Fallback: by hand

Use the `dig` command, or DNS-over-HTTPS in a browser if there's no terminal:

| Record | Command | Browser alternative |
|---|---|---|
| Sender list | `dig +short TXT domain.com.au` (look for `v=spf1`) | `https://cloudflare-dns.com/dns-query?name=domain.com.au&type=TXT` with header `accept: application/dns-json` (or Google: `https://dns.google/resolve?name=domain.com.au&type=TXT`) |
| Spoofing protection | `dig +short TXT _dmarc.domain.com.au` | same, with name `_dmarc.domain.com.au` |
| Signature | `dig +short TXT google._domainkey.domain.com.au` (Google Workspace), `selector1._domainkey...` and `selector2._domainkey...` (Microsoft 365) | same |
| Mail servers | `dig +short MX domain.com.au` | type `MX` |

### Finding the DKIM selector

The script guesses the common names (Google, Microsoft, Mailchimp, SendGrid, Mailgun, Zoho and others). If it says "couldn't confirm", ask the owner to:
1. Send an email from their business address to themselves.
2. Open it. In Gmail: the three dots, then "Show original". In Outlook: File, Properties, or "View message source".
3. Find the line starting `DKIM-Signature:` and read out the bit after `s=` (for example `s=google`). It's not secret.

## How to read the result

| What the script shows | Meaning |
|---|---|
| `DMARC: missing` | Nothing stops fakes. Anyone can send as them. |
| `DMARC: none` | Monitor only. Fakes still land in inboxes. |
| `DMARC: quarantine` or `reject` | Fakes go to junk or get blocked. Good. |
| `(from parent.com.au)` | A subdomain covered by the main domain's setting. Fine. |
| `SPF: missing` | No sender list. |
| SPF ends `+all` | The list says "anyone can send". As bad as none. |
| SPF uses 9 or 10 lookups | One more email tool will break the list and real email starts going to junk. |
| DKIM `1024-bit` | Older, weaker key size. Low priority upgrade. |
| DKIM `not confirmed` | Couldn't find it. Not the same as missing. Ask for the selector. |
| No MX record | The domain doesn't receive email. If it doesn't send either, lock it fully. |

## Red, amber, green (area 9, email part)

- **Green:** sender list set and not `+all`, a signature found, spoofing protection on `quarantine` or `reject` for 100% of email.
- **Amber:** spoofing protection on `none` (monitor only), signature not confirmed, or sender list without an ending rule.
- **Red:** no spoofing protection, no sender list, `+all`, two sender lists, or a broken sender list (over 10 lookups).

Severity of each finding is printed by the script. Overall area 9 is the worse of this check and `domain-dns.md`.

## Plain-English fixes

Check the provider's current help page before giving click paths. Say "the menu may look a little different" if you can't.

1. **No spoofing protection (high).** "Add one line to your domain settings. If Google or Microsoft is the only thing that sends email as you, start straight at `p=quarantine`. If tools like your CRM, Mailchimp or Xero also send as you, start at `p=none` with a report address for two weeks, check the reports, then move to quarantine."
   - Record to add: name `_dmarc`, type `TXT`, value `v=DMARC1; p=quarantine; rua=mailto:dmarc@THEIRDOMAIN`.
   - Where: wherever their domain's DNS lives (Cloudflare, GoDaddy, Crazy Domains, VentraIP, their web builder). Ask who manages it.
2. **Monitor only (medium).** "Change `p=none` to `p=quarantine`." Before they do, confirm every tool that sends as them is in the sender list and signing.
3. **No sender list (high).** One `TXT` record starting `v=spf1`. Google: `v=spf1 include:_spf.google.com ~all`. Microsoft: `v=spf1 include:spf.protection.outlook.com ~all`. Add an `include:` for each other tool that sends as them (their help pages give it).
4. **Too many lookups (low to high).** Remove `include:` entries for tools they've stopped using.
5. **Signature not set up (medium).** Google Workspace: Admin console, Apps, Google Workspace, Gmail, Authenticate email, generate a 2048-bit key, add it to DNS, click Start authentication. Microsoft 365: Defender portal, Email authentication settings, DKIM, enable for the domain.
6. **1024-bit key (low).** Same screen as above: make a new 2048-bit key and switch.
7. **Domain that doesn't send email (low).** `v=spf1 -all` and `v=DMARC1; p=reject`.

## Credit

Deeper checks by checkdmarc (Apache-2.0, Sean Whalen / domainaware). DNS-over-HTTPS by Cloudflare 1.1.1.1 or Google Public DNS.
