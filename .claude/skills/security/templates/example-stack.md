---
file: security-stack
updated: 2026-10-09
example: true
---

# Our tools (for the security check)

> Example only. Sam's Plumbing is a made-up business, used to test the flow. The domain uses `.example` so no check ever hits a real site.

## Business
- Business name: Sam's Plumbing
- Owner: Sam
- Domain (for email and website): samsplumbing.example

## Tools
| Area | Tool | Who has a login | Notes |
|---|---|---|---|
| Email and files | Google Workspace (Gmail, Drive) | Sam, 3 plumbers, office manager | Email on the business domain |
| Customers and leads (CRM) | GoHighLevel | Sam, office manager | Marketing agency also has a login [CHECK which agency] |
| Getting paid | Stripe (card payments through GHL invoices) | Sam | Office manager uses Sam's login for refunds |
| The books | Xero | Sam, bookkeeper (own login) | Previous accountant may still have access [CHECK] |
| Website (built on, built by) | Wix, built by a freelancer in 2023 | Sam, freelancer | Freelancer still listed as a collaborator |
| App code | None | | |
| AI tools (and add-ons) | ChatGPT (Sam, office manager), Claude (Sam) | | ChatGPT connected to Gmail. Claude has the Founder OS plugin and the Google Drive connector |

## People
- People with logins (incl. contractors): 5 staff, bookkeeper, Wix freelancer, GHL agency
- Left in the last year: one apprentice (Mar 2026)
- Admin (who can add and remove people): Sam (Google admin, Xero adviser, GHL agency admin)
- Outside IT or agency: none for IT. GHL agency for marketing

## Devices and backups
- Computers and phones: Sam on a MacBook, office manager on a Windows laptop, plumbers on their own phones
- Backups: "It's all in Google." Nothing separate. Xero is in the cloud

## Checks that fit
| Check | Fits? | Why | Access needed |
|---|---|---|---|
| Email spoofing | Yes | Business domain on Google email | Domain only |
| Website grade | Yes | Wix site | Website address only |
| Password leaks | Yes | Every owner | None |
| AI tool check | Yes | ChatGPT connected to Gmail, Claude with a plugin and Drive connector | Sam's Claude settings, ChatGPT connected apps (screenshots) |
| Accounts and two-step login | Yes | Google, GHL, Stripe, Xero, Wix. Shared Stripe login. Ex-apprentice and old accountant to confirm | Owner answers, screenshots |
| File sharing | Yes | Google Drive | Google Drive connector, read-only |
| Google Workspace settings | Yes | Sam is the Google admin | Sam approves read-only access once |
| Leaked keys in files | Maybe | Only if Drive is synced to the Mac | A folder on Sam's Mac |
| Code check (add-on) | No | No code | |
| Microsoft 365 settings | No | Google shop | |
| Macros in Office files | Rate green | No desktop Office ("no desktop Office") [CHECK the Windows laptop] | |
| Devices and backups | Yes (guided) | Mac, Windows, staff phones. No backup outside Google | Owner answers |

## Changes
- 2026-10-09: first interview (example).
