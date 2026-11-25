# The stack interview

Short. About 5 minutes if they talk. One question at a time. Reflect each answer back in one line. If `brain/4 Operations/Tools.md` exists, read it first and confirm what's there ("Looks like you're on Google for email and Xero for the books. Still right?") instead of asking again.

Never ask for passwords, logins or codes. We only want to know which tools they use and who's in charge of them.

---

## The questions

1. **Email and files.** "What do you use for email and files? Google (Gmail, Drive), Microsoft (Outlook, OneDrive), or something else?"
   - Follow-up: "Is your email on your own business name, like you@yourbusiness.com.au, or a Gmail or Hotmail address?" Note the domain.
   - Follow-up: "Where do you pay for the domain name each year, and who manages its settings?" (GoDaddy, Crazy Domains, VentraIP, Cloudflare, the web designer, don't know.)
2. **Customers and leads (CRM).** "Where do you keep track of customers and leads?" (GoHighLevel, HubSpot, ServiceM8, Tradify, simPRO, a spreadsheet, nothing.)
3. **Getting paid.** "How do customers pay you?" (Stripe, Square, PayPal, bank transfer, through the CRM, through the accounting app.)
4. **The books.** "What do you use for the books?" (Xero, MYOB, QuickBooks.) "Does your bookkeeper or accountant have their own login?"
5. **Website.** "Have you got a website? What's it built on, and who built it?" (Wix, Squarespace, Shopify, WordPress, custom, an agency, a mate.) "Who can still log in to it?"
6. **App code.** "Do you have any app or custom software of your own, or did someone build code for you?" If yes: "Where does the code live?" (GitHub, the developer's computer, don't know.)
7. **AI tools.** "Which AI tools does the team use?" (ChatGPT, Claude, Copilot, Gemini, others.) "Any add-ons, skills or plugins installed in them? Anything connected to your email or files?"
8. **Team size.** "How many people log in to your business tools? Include contractors, bookkeepers and anyone who's left in the last year."
9. **Who's the admin.** "Who's in charge of the accounts? Who can add or remove people in Google or Microsoft?" If it's an outside IT person or agency, note their name and company.
10. **Computers and phones.** "What do people work on? Macs, Windows, phones, a mix? Any shared computers?"
   - Follow-up: "Does anyone use Word or Excel installed on the computer, or is it all in the browser?"
11. **Backups.** "If your laptop died tonight, what would you lose? Is anything backed up?"

That's it. Say: "Thanks. That's all I need to know which checks fit you."

---

## How answers map to checks

| Answer | Checks that fit | Notes |
|---|---|---|
| Any business email domain | Email spoofing, Domain and DNS | Gmail or Hotmail address only: skip both, and suggest a business domain as a low fix |
| Google Workspace | File sharing (Drive), Google Workspace settings, Accounts | Deep checks need the Google admin to approve read-only access |
| Microsoft 365 | Microsoft 365 settings, Accounts | Guided checklist until the Microsoft check is built |
| Other email (Zoho, cPanel, Apple) | Accounts (guided checklist) | No deep settings check |
| Any CRM | Accounts (two-step login, who has access, old staff) | GHL: also check sub-account users and API keys shared in the CRM |
| Any payments tool | Accounts (two-step login, team roles, payout bank changes) | Payment tools are the top target. Always high if two-step login is off |
| Any accounting tool | Accounts (two-step login, advisor and bookkeeper access) | Old advisors with access = medium |
| Website, any builder | Website grade, Domain and DNS, Accounts (who can log in, old builders) | Wix, Squarespace and Shopify handle most patching themselves |
| Website on WordPress | Website grade, plus plugin updates under "Patch apps" | Owner or developer answers |
| Website or app with custom code | Code check (add-on), Leaked keys | Only with the owner's OK and access to the code |
| AI tools in use | AI tool check | Claude: skills, plugins, connectors, settings. ChatGPT and others: connected apps, custom GPTs, data-training setting |
| Team size over 1 | Accounts (shared logins, people who've left) | Shared logins = medium, ex-staff with access = high |
| Outside admin or IT | Accounts (who holds the top admin login) | Owner should hold, or at least know, the top admin login |
| Desktop Word or Excel | Macros in Office files (Microsoft 365 settings, or guided) | Browser only or no Office: rate green, note "no desktop Office" |
| Computers and phones | Devices and backups (guided) | Auto-updates on, old devices that no longer get updates |
| Backups | Devices and backups (guided) | "Nothing" = high |
| Every owner | Password leaks | Always runs |

---

## Save it: `Security/Stack.md`

Write this file as soon as the interview is done. Use their words. `[CHECK]` anything you're unsure of and ask at the end.

```markdown
---
file: security-stack
updated: YYYY-MM-DD
---

# Our tools (for the security check)

## Business
- Business name:
- Owner:
- Domain (for email and website):

## Tools
| Area | Tool | Who has a login | Notes |
|---|---|---|---|
| Email and files | | | |
| Domain (registrar, DNS host) | | | |
| Customers and leads (CRM) | | | |
| Getting paid | | | |
| The books | | | |
| Website (built on, built by) | | | |
| App code | | | |
| AI tools (and add-ons) | | | |

## People
- People with logins (incl. contractors):
- Left in the last year:
- Admin (who can add and remove people):
- Outside IT or agency:

## Devices and backups
- Computers and phones:
- Backups:

## Checks that fit
| Check | Fits? | Why | Access needed |
|---|---|---|---|

## Changes
- YYYY-MM-DD: first interview.
```

Re-ask a section when the owner says a tool changed, someone joined or left, or every six months at a monthly check.
