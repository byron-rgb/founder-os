# The Essential Eight, for a small business

The Essential Eight is the Australian Government's list of eight basics that stop most cyber attacks (from the ACSC, cyber.gov.au). It was written for bigger organisations. Below is our own plain-English version for a small service business, with what red, amber and green mean, and which of our checks feed each one.

We aim small businesses at the first level ("Maturity Level One" in ACSC terms): the basics done well. Don't push owners toward enterprise tools they don't need.

The report uses these eight areas, plus five extra areas that matter a lot for small businesses and the Essential Eight doesn't cover directly.

Rating rules for every area:
- **Green:** checked, and it meets the green line below.
- **Amber:** checked, partly there.
- **Red:** checked, and it's missing or something is exposed now.
- **Not checked:** we couldn't look. Never rate it green.

Score: green = 2 points, amber = 1, red = 0. Score out of 100 = points earned divided by (2 x areas checked), times 100, rounded. Areas not checked don't count. Always show how many areas were checked next to the score ("72 / 100, 9 of 13 areas checked").

---

## The eight

### 1. Two-step login (ACSC: multi-factor authentication)
Plain English: a password plus a code on your phone, so a stolen password alone isn't enough.
- **Green:** on for every person on email, payments, the books, the CRM and the website login. Uses an app or security key, not just text messages, for admins.
- **Amber:** on for the owner and the main tools, but missing for some staff or one tool, or text-message only for admins.
- **Red:** off on email or payments for anyone, or off for the admin account.
- Fed by: Accounts and two-step login, Google Workspace settings, Microsoft 365 settings.

### 2. Limit admin access (ACSC: restrict administrative privileges)
Plain English: only one or two people can change settings or add users, and the admin login is only used for admin jobs.
- **Green:** two admins at most (one can be a trusted IT person), no shared admin login, nobody who has left still has access.
- **Amber:** three or more admins, or the owner doesn't know who the admins are.
- **Red:** someone who has left still has admin access, or the admin login is shared.
- Fed by: Accounts, Google Workspace settings, Microsoft 365 settings, stack interview (team and admin answers).

### 3. Keep apps updated (ACSC: patch applications)
Plain English: browsers, apps and website plugins get updated soon after fixes come out.
- **Green:** browsers and apps update automatically. Website plugins (WordPress) are up to date. Code dependencies have no known high-risk holes.
- **Amber:** some manual updates, or a few things a month or more behind.
- **Red:** an app or plugin with a known serious hole, or software that no longer gets updates.
- Fed by: Code check (OSV-Scanner), website answers, owner answers.

### 4. Keep computers and phones updated (ACSC: patch operating systems)
Plain English: Mac, Windows and phone updates are switched on, and no one uses a device too old to get them.
- **Green:** auto-updates on for every work device, and every device still gets updates.
- **Amber:** updates on but often put off, or one or two devices unknown.
- **Red:** a work device that no longer gets security updates.
- Fed by: stack interview (devices), guided checklist.

### 5. Only approved apps (ACSC: application control)
Plain English: people only install software and add-ons the business has agreed on. For AI tools this means skills, plugins and connected apps too.
- **Green:** the owner knows what's installed and connected, and anything new gets a quick check first.
- **Amber:** a few unknown add-ons or connected apps, none risky.
- **Red:** an add-on, skill or connected app that can read email or files and nobody knows who made it, or one that fails our AI tool check.
- Fed by: AI tool check, Google Workspace settings (connected apps), Microsoft 365 settings.

### 6. Lock down the browser and apps (ACSC: user application hardening)
Plain English: switch off the risky bits people don't need, like old plugins and pop-up permissions, and keep the browser's safe browsing on.
- **Green:** safe browsing on, no odd browser extensions, managed browser settings where the suite allows.
- **Amber:** a few unknown browser extensions.
- **Red:** an extension or add-on that can read every page or every email and nobody knows why it's there.
- Fed by: Google Workspace settings, Microsoft 365 settings, guided checklist.

### 7. Macros in Office files (ACSC: configure Microsoft Office macro settings)
Plain English: Word and Excel files from outside can't run hidden code. This one mostly matters for Microsoft shops.
- **Green:** macros blocked for files from the internet, or the business doesn't use desktop Office.
- **Amber:** macros allowed but the team rarely opens outside Office files.
- **Red:** macros allowed for files from the internet on machines that open customer or supplier attachments.
- Fed by: Microsoft 365 settings. For Google-only businesses, rate green with the note "no desktop Office".

### 8. Backups (ACSC: regular backups)
Plain English: if a laptop dies or files get locked by a scam, you can get them back.
- **Green:** important files and the books are backed up automatically, at least one copy can't be changed or deleted by a normal login, and someone has tried a restore.
- **Amber:** backups exist but nobody has tested a restore, or only some things are covered.
- **Red:** no backup, or the only copy is on the same laptop.
- Fed by: stack interview (backups), guided checklist. Note: Google Drive and OneDrive sync isn't a backup on its own, because deletes sync too.

---

## Our extra areas

### 9. Email and domain protection
Plain English: stops scammers sending email that looks like it's from your business (how most fake invoice scams start), and keeps your domain name from being stolen, lapsing or having forgotten parts hijacked.
- **Green:** the domain has all three email protections set and the strictest one is on "reject" or "quarantine". Domain locked against transfers, renewing, no dangling subdomains, two-step login on the registrar.
- **Amber:** email protections only on "monitor", signature not confirmed, transfer lock off, or a loose subdomain on an ordinary host.
- **Red:** email protections missing or set up so anyone can send as you, a subdomain that can be claimed by a stranger, the domain about to expire, or no two-step login on the registrar.
- Fed by: Email spoofing check, Domain and DNS check, Accounts (registrar questions). Rate by the worse of the two checks.

### 10. Website
Plain English: your website's security grade and its padlock certificate.
- **Green:** grade B or better, certificate valid for more than 30 days.
- **Amber:** grade C or D, or the certificate runs out within 30 days.
- **Red:** grade F, no padlock, or the certificate has expired.
- Fed by: Website grade check.

### 11. File sharing
Plain English: who can see your files.
- **Green:** nothing sensitive open to "anyone with the link", outside sharing is only with people you know.
- **Amber:** some "anyone with the link" files, nothing sensitive in them.
- **Red:** customer details, invoices, passports, contracts or passwords open to "anyone with the link" or to people who've left.
- Fed by: File sharing check, Google Workspace settings, Microsoft 365 settings.

### 12. Passwords and leaked keys
Plain English: no reused or leaked passwords, and no passwords or keys sitting in files.
- **Green:** a password manager in use, no password on a known leak list, no keys found in files.
- **Amber:** no password manager yet, or a leaked password already changed.
- **Red:** a password in use that's on a leak list, a shared password in a document, or a working key found in a file.
- Fed by: Password leaks check, Leaked keys check, Accounts.

### 13. AI tools
Plain English: the AI tools the team uses are set up safely, and nothing installed in them is sneaky.
- **Green:** every skill, plugin and connection checked and clean, sensible settings (only needed connections, no training on business data where there's a choice).
- **Amber:** something unchecked, or a setting worth tightening.
- **Red:** a skill or plugin that fails the check, or an AI tool connected to email or files that nobody approved.
- Fed by: AI tool check.

---

## Other frameworks

- **CIS Controls (Implementation Group 1):** we map to it by name only. Its text is licensed noncommercial, so never copy it into reports.
- **CISA Secure Our World:** four habits (strong passwords, two-step login, updates, spotting scams). Handy as the one-line summary for the owner.
- **UK NCSC Small Business Guide:** five topics, useful wording for UK clients. Credit it if we quote it.
