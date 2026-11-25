# Check: Microsoft 365 settings

> **Status: documented, not yet tested on a real client.** Ready for when the first Microsoft client asks. On the first run, go slowly, follow Maester's own current guide (maester.dev) if anything differs, and update this file with what you learn.

**Answers for the owner:** are your Microsoft 365 settings safe (two-step login, admin accounts, outside sharing, email protections, Office macros)?

**Needs:** a Microsoft 365 **Global Administrator** approves read-only access once, on their own computer. We never hold their login.
**Feeds areas:** 1, 2, 5, 6, 7 (macros), 9, 11.
**Time:** first setup 30 to 45 minutes with the admin. Then about 10 minutes a month.

## The tool

| Tool | What it does | Made by | Licence |
|---|---|---|---|
| **Maester** | Runs a few hundred read-only tests against Microsoft 365 (including CISA's SCuBA baseline tests, CIS-style checks and its own), and writes an HTML and JSON report. Works on Mac, Windows and Linux | Maester team (open source) | MIT |
| ScubaGear | CISA's own Microsoft 365 checker | CISA | CC0. Windows PowerShell only. Optional for Windows clients; we default to Maester |

Not bundled. Installed by the admin from the PowerShell Gallery into their own user account. Nothing system-wide.

**Version pin:** use the **2.x release** (2.3.0 tested by the Maester team as of 2026-10-09). Maester 3.0 became a preview build on 8 October 2026 with breaking changes. Don't use `-AllowPrerelease`. Check maester.dev for the current stable version before the first run and update this line.

## Plain words for the owner

> Microsoft's settings are checked by a free open-source tool called Maester. You sign in once and approve it to read your settings. It can only read. The results stay on your computer. You can remove its access afterwards.

## Setup (admin's computer)

1. **PowerShell 7.** Windows: from the Microsoft Store ("PowerShell") or Microsoft's installer. Mac: Microsoft's installer package from their PowerShell docs page (no Homebrew needed). Open it with `pwsh`.
2. **Install Maester for this user only:**
   ```powershell
   Install-Module -Name Maester -Scope CurrentUser -RequiredVersion 2.3.0
   md ~/FounderOS-security-tools/maester-tests
   cd ~/FounderOS-security-tools/maester-tests
   Install-MaesterTests
   ```
   PowerShell may ask to trust the PowerShell Gallery. That's Microsoft's official module store. Say yes for this install.
3. **Sign in and approve (once):**
   ```powershell
   Connect-Maester
   ```
   A browser opens. The Global Administrator signs in. Microsoft shows the permissions Maester asks for: they're "Read" permissions (directory, policies, reports). Read them together, then Accept. After this first approval, a person with the **Global Reader** role can run it.
   - Exchange Online and Teams tests need extra connections (`Connect-Maester -Service All`). Start with the default; add them on the monthly runs once the basics are fixed. Maester's README warns against version 3.9.2 of the ExchangeOnlineManagement module; check that note before adding Exchange.
4. **Run it:**
   ```powershell
   Invoke-Maester
   ```
   It writes a report (HTML and JSON) in a `test-results` folder and opens it.

## Reading the results

Each test is Passed, Failed, Skipped or Not run. Turn Failed tests into findings, mapped to our areas:

| Maester / SCuBA area | Our area |
|---|---|
| MFA, Conditional Access, Security Defaults, phishing-resistant methods, legacy sign-in blocked | 1 |
| Global admins (2 to 4, named), privileged roles, break-glass account, PIM if licensed | 2 |
| App registrations, enterprise apps and user consent to apps | 5 |
| Defender preset policies, safe links and attachments, browser and device settings | 6 |
| Office macros from the internet blocked (Intune, or the guided check below) | 7 |
| Exchange: SPF, DKIM, DMARC, auto-forwarding to outside blocked | 9 and 6 |
| SharePoint and OneDrive external sharing, anyone links, Teams external access | 11 |

Not every test suits a small business, and some need licences they don't have (Entra ID P1 or P2, Intune). Note "needs a licence you don't have" rather than failing them. Two-step login missing is always high, whatever the licence: Security Defaults are free.

## Without the tool (guided)

If PowerShell isn't an option, walk through these with the admin and rate anything not looked at as "not checked":

1. entra.microsoft.com, Identity, Overview, Properties, Manage security defaults: **On**, or Conditional Access policies requiring MFA for everyone (area 1).
2. admin.microsoft.com, Users, Active users, Multifactor authentication: who isn't registered (area 1).
3. admin.microsoft.com, Roles, Global Administrator: two to four named people, nobody who's left (area 2).
4. entra.microsoft.com, Enterprise applications, Consent and permissions: users can't consent to unknown apps; review apps with mail or files access (area 5).
5. SharePoint admin centre, Policies, Sharing: "Anyone" links off or expiring; OneDrive matches (area 11).
6. Exchange admin centre, Mail flow, Remote domains (and Defender, Anti-spam outbound policy): automatic forwarding to outside off (area 6).
7. Defender portal (security.microsoft.com), Email and collaboration, Policies, Preset security policies: Standard protection on (area 6).
8. Defender portal, Email authentication settings, DKIM: enabled for the domain (area 9). SPF and DMARC are covered by `email-spoofing.md` from outside.
9. Office macros: Microsoft blocks macros in files from the internet by default in current Microsoft 365 Apps. Ask: "Has anyone changed macro settings, or do you use old Office versions?" Old versions, or macros unblocked, on machines that open supplier files = red (area 7).
10. admin.microsoft.com, Health, Message centre and the Microsoft Secure Score page (security.microsoft.com, Secure score): note the score and the top 3 suggestions.

## Removing access afterwards

entra.microsoft.com, Enterprise applications, find "Microsoft Graph Command Line Tools" (the app Maester signs in through), Permissions: review, or remove the user's consent. Then delete `~/FounderOS-security-tools/maester-tests`.

## Plain-English fixes

Check Microsoft's current help page for click paths (they move often). Say "the menu may look a little different."

1. **Two-step login not required (high).** Turn on Security Defaults (free) or a Conditional Access policy requiring MFA for all users. Give staff a week's notice and help them set up Microsoft Authenticator.
2. **Too many global admins, or an ex-staff admin (high).** Remove the role from everyone who doesn't need it. Keep two named admins plus one emergency account with a long password in a safe place.
3. **Users can approve any app (medium).** Turn off user consent, or allow only verified publishers.
4. **Anyone links in SharePoint or OneDrive (medium to high).** Restrict to "New and existing guests" or "Only people in your organisation", or make anyone links expire in 7 days.
5. **Auto-forwarding to outside allowed (medium).** Block it in the outbound anti-spam policy. Scammers who get into one mailbox forward everything out.
6. **Preset security policies off (medium).** Turn on Standard protection.
7. **Macros unblocked (high if staff open outside attachments).** Re-enable the default block, or set it through Intune if licensed.

## Credit

Maester (MIT, maester365 team). ScubaGear and the SCuBA Microsoft 365 baselines (CISA, public domain). Steps summarised in our own words.
