# Credits

The security module stands on other people's work. This file lists every tool, service and guide we use, with its licence. Updated 2026-10-09 (build step 8, plugin 0.4.0).

Rules:
- We only bundle code licensed MIT, Apache-2.0, BSD or CC0, and we keep its licence and credit.
- Tools are downloaded at run time from the official release, pinned by version and checksum, rather than copied into this plugin (`scripts/fetch_tool.py`, `references/install.md`).
- Anything else is "link only": the owner installs it themselves, or we skip it.
- Our scripts in `scripts/` and all reference files are written by Driven Young.

## Bundled in this plugin

| What | Where | Made by | Licence | Version |
|---|---|---|---|---|
| Cloudflare security-audit skill | `addons/cloudflare-security-audit/` (unchanged, with its `LICENSE` and our `SOURCE.md`) | Cloudflare, Inc. | MIT | commit c1c8a8c (2026-09-14), every file checked against it |

## Downloaded at run time (not bundled)

| Tool | What we use it for | Made by | Licence | Pinned | Check |
|---|---|---|---|---|---|
| gitleaks | Passwords and keys in folders, exports and code | Zachary Rice and contributors | MIT | 8.30.1, SHA-256 checked | Leaked keys, Code check |
| OSV-Scanner | Known holes in code building blocks | Google | Apache-2.0 | 2.6.0, SHA-256 checked | Code check |
| checkdmarc (optional) | Deeper email protection checks | Sean Whalen (domainaware) | Apache-2.0 | 6.0.3 | Email spoofing |
| SkillSpector | Scanning AI skills and connectors | NVIDIA | Apache-2.0 | 2.12.0 (commit 3527006) | AI tool check |
| ScubaGoggles | Google Workspace settings against CISA's baselines | CISA | CC0 | v1.0.1 (latest on 2026-10-09) | Google Workspace settings |
| GAM7 | Read-only lists of users, two-step login, connected apps, shared files | GAM team | Apache-2.0 | 7.48.24, SHA-256 checked (macOS) | Google Workspace settings, File sharing |
| Maester | Microsoft 365 settings (documented, untested) | Maester team | MIT | 2.3.0 | Microsoft 365 settings |
| ScubaGear (optional, Windows only) | Microsoft 365 settings | CISA | CC0 | not pinned, link only for now | Microsoft 365 settings |

## Linked, not bundled (open licence, not vetted for bundling yet)

| Tool | Made by | Licence | Why linked |
|---|---|---|---|
| Sentry skills `skill-scanner` and `claude-settings-audit` (github.com/getsentry/skills) | Sentry | Apache-2.0 | Useful second opinions. Not reviewed line by line yet, so owners install from Sentry's repo if they want them |

## Services we call (not bundled)

| Service | What we use it for | Terms |
|---|---|---|
| MDN HTTP Observatory API v2 | Website grade A+ to F | Free public API, no key. Credit Mozilla in reports |
| Have I Been Pwned: Pwned Passwords | Password leak check. Only the first 5 characters of a scrambled password are sent, never the password | Free, no key. Credit HIBP (CC BY 4.0). Staff email breach search needs a paid key: documented as an add-on only |
| rdap.org | Domain transfer lock, expiry, DNSSEC | Free public RDAP bootstrap service |
| crt.sh | Finding subdomain names in public certificate logs (optional) | Free public search (Sectigo) |
| Cloudflare 1.1.1.1 DNS-over-HTTPS | DNS lookups when `dig` isn't available | Free public resolver |
| osv.dev (via OSV-Scanner) | Vulnerability database | Free, Google. Only package names and versions are sent |

## Guides and ideas we build on

| Guide | Made by | Licence | How we use it |
|---|---|---|---|
| Essential Eight and small business guides | Australian Signals Directorate's Australian Cyber Security Centre (cyber.gov.au) | CC BY 4.0 (confirmed 2026-10-09 on cyber.gov.au/copyright; logo and Coat of Arms excluded). Attribution: © Commonwealth of Australia 2026 | Report backbone. Rewritten in our own words in `references/essential-eight.md` |
| SCuBA secure configuration baselines | CISA | Public domain | The "why" behind Google and Microsoft findings |
| Secure Our World | CISA | Public domain | The four-habit summary |
| Small Business Guide | UK NCSC | Open Government Licence v3 | Wording for UK clients, with credit |
| CIS Controls v8 (IG1) | Center for Internet Security | CC BY-NC-ND | Named and mapped only. Never copy the text |
| Community app-security checklist ("Audit your app's security in 2 minutes", shared with Byron, author and licence unknown) | unknown | unknown | Ideas only, no text copied: the 48-item code quick score (`references/code-quick-score.md`), the owner "ask me" questions in `checks/accounts-and-2sv.md`, and the public domain checks in `checks/domain-dns.md` |
| AI Scout steps | Driven Young (in-house) | ours | The "one item" vetting steps in `checks/ai-tool-vetting.md` |

## Link only (not bundled)

| Tool or guide | Why it's link only |
|---|---|
| TruffleHog, SSLyze | AGPL-3.0 |
| testssl.sh, ScoutSuite | GPL-2.0 |
| Lynis | GPL-3.0 |
| Semgrep rules and Semgrep skills | Semgrep Rules License: internal business use only, can't be used in a service for clients |
| Trail of Bits skills | CC-BY-SA-4.0: share-alike would force our bundle open |
| Anthropic `claude-security` plugin | Proprietary. Owners can install it from the official marketplace |
| OWASP ASVS and Top 10 | CC-BY-SA-4.0. Cite, don't copy |
| openai/skills `security-best-practices` | No licence |
| Qualys SSL Labs API | Terms unclear, needs registration. Avoided |
| canarytokens.org | Mentioned as an optional advanced idea only. Free service by Thinkst |
