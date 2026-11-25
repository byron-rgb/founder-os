# Check: Google Workspace settings

**Answers for the owner:** are your Google settings safe, and which outside apps can read your staff's email and files?

**Needs:** the Google **super admin** (often the owner) approves read-only access once, on their own computer. We never hold their login or the access file.
**Feeds areas:** 1, 2, 5, 6, 11 (and 9 for Gmail's spoofing settings).
**Time:** first setup 30 to 45 minutes with the admin (on the setup call). After that, about 5 minutes a month.
**When:** monthly (the deeper check), and at the first check if they're on Google Workspace.

## Two tools, both free and open

| Tool | What it answers | Made by | Licence |
|---|---|---|---|
| **ScubaGoggles** | Are the Google settings in line with the US Government's (CISA's) secure baseline? Covers Gmail, Drive, Calendar, Meet, Chat, Groups, Sites, Classroom and the admin settings | CISA | CC0 (public domain) |
| **GAM** | Lists: who has two-step login, who's an admin, which outside apps are connected to whose account and what they can do, which files are open to anyone with the link | GAM team | Apache-2.0 |

Neither is bundled in this plugin. The admin installs them in a private folder on their own computer from the official releases, pinned to a version and checked (`references/install.md`). GAM can also change settings: **this check only ever runs its "print" (read) commands.** Never run a GAM command that creates, updates, deletes, suspends, transfers or shares anything.

## Plain words for the owner

> Google has a free checker made by the US Government's cyber agency that compares your settings to their safe list. To run it, you create a small "key" in your own Google account that lets it read your settings. It can't change anything we don't tell it to, and we only tell it to read. The key stays on your computer. You can delete it when we're done.

## Before you start

- Confirm the admin is a **super admin** (Admin console, Account, Admin roles; or ask "can you add and delete users?").
- A Mac or Windows computer with Python 3.10 or newer (`python3 --version`). If they don't have it, skip to "Without the tools" below.
- About 45 minutes, a browser, and the admin present. Do it on the setup call.
- Explain: Google will show a screen listing what the checker can read. Read it together before clicking Allow.

## Part A: ScubaGoggles (settings against the safe list)

Follow ScubaGoggles' own current guide if a screen looks different (github.com/cisagov/ScubaGoggles, docs folder). Our summary, in order:

**A1. Install it in a private folder** (the admin types these in Terminal, one at a time):
```
mkdir -p ~/FounderOS-security-tools && cd ~/FounderOS-security-tools
python3 -m venv scuba-env
source scuba-env/bin/activate
pip install scubagoggles
scubagoggles setup
```
`scubagoggles setup` asks where to save reports and downloads a helper it needs (Open Policy Agent). Accept the defaults, except put the output folder inside `~/FounderOS-security-tools/`.

**A2. Make a Google Cloud project** (free, the admin's own):
1. Go to console.cloud.google.com and sign in as the admin.
2. Top bar, project picker, New project. Name it "Security check". Create.

**A3. Turn on four Google services** in that project: menu (three lines), APIs and Services, Enabled APIs and services, + Enable APIs and services. Search for and enable each: **Admin SDK API**, **Groups Settings API**, **Cloud Identity API**, **Enterprise License Manager API**.

**A4. Make the key (an "OAuth client")**:
1. Menu, APIs and Services, OAuth consent screen, Get started.
2. App name "Security check", support email the admin's. Audience: **Internal** (only people in their business can use it). Contact email. Agree, Create.
3. Branding, Authorized domains, add their business domain, Save.
4. Menu, APIs and Services, Credentials, + Create credentials, **OAuth client ID**.
5. Application type **Web application**. Under Authorized redirect URIs add `http://localhost` and `http://localhost:8080/` (the slash at the end matters).
6. Create, then **Download JSON**. Move the file into `~/FounderOS-security-tools/` and rename it `google-credentials.json`.
7. Tell ScubaGoggles where it is: `scubagoggles setup --credentials ~/FounderOS-security-tools/google-credentials.json`

**Never** paste the contents of that file into the chat, email it, or save it in the brain folder. It's a key.

**A5. If they've restricted outside apps** (some businesses have): Admin console, Security, Access and data control, API controls, Manage third-party app access, Configure new app, search the client ID from Credentials, set it to Trusted for the whole organisation.

**A6. Run it:**
```
cd ~/FounderOS-security-tools && source scuba-env/bin/activate
scubagoggles gws
```
A browser window opens asking the admin to sign in and allow. The screen lists what it will read. Most are "view" (read-only) permissions. Two of them (licences and group settings) are listed by Google without a read-only version. ScubaGoggles only reads with them, but say so honestly. Click Allow.

It takes a few minutes, then opens a report in the browser and saves an HTML and a JSON file in a folder named `GWSBaselineConformance_<date and time>`.

**A7. Read the results with the owner.** Open the JSON results file in that folder (read it, don't upload it anywhere). Each policy has a result: Pass, Fail, Warning, or Manual (needs a human to check). Turn the Fails and Warnings into findings:

| ScubaGoggles product | Our area |
|---|---|
| Common Controls: 2-step verification, phishing-resistant keys, login challenges, password rules | 1 |
| Common Controls: super admins, admin roles, account recovery | 2 |
| Common Controls: third-party app access, Marketplace apps, Google Takeout | 5 |
| Common Controls: Chrome and device settings, less secure access | 6 |
| Drive and Docs, Sites, Groups (external sharing, link sharing defaults) | 11 |
| Gmail: SPF, DKIM, DMARC, auto-forwarding to outside, attachment and link safety | 9 and 6 |
| Calendar, Meet, Chat (outside sharing) | 11 |

Not every CISA baseline item suits a 5-person business. Use judgement and the Essential Eight targets at "level one": a missing hardware key requirement for staff is low, two-step login not enforced is high, Drive defaults open to "anyone with the link" is high, auto-forwarding to outside addresses allowed is medium. Say "the government's list is strict; here's what matters for a business your size."

## Part B: GAM (who has what)

GAM's own wiki has the current steps: github.com/GAM-team/GAM/wiki. Our summary:

**B1. Download GAM7** from the official release page (github.com/GAM-team/GAM/releases), the file for their computer (for example `gam-<version>-macos26.6-arm64.tar.xz` on a recent Apple-chip Mac), into `~/FounderOS-security-tools/gam/`. Check the file's fingerprint matches the one GitHub shows next to the download (`shasum -a 256 <file>`). Unpack it. See `references/install.md` for the exact pinned version and fingerprint we last checked. Avoid the "one-line installer" that pipes a script into the shell.

**B2. Set it up** (the admin signs in when asked):
```
cd ~/FounderOS-security-tools/gam/gam7
./gam create project
./gam oauth create
```
`gam create project` makes its own small Google Cloud project and key. `gam oauth create` shows a list of permissions with numbers: **choose the read-only options** where offered, and deselect write ones you don't need. For the Drive-wide file list it also needs a service account step (`./gam user ADMIN@THEIRDOMAIN check serviceaccount`), which asks the admin to authorise it in the Admin console: choose read-only Drive where offered. Skip the Drive part if the admin isn't comfortable; the Drive connector check covers their own files.

**B3. Run the read-only reports** (each writes a spreadsheet file):
```
./gam redirect csv ./users.csv print users fields primaryemail,isadmin,isdelegatedadmin,isenrolledin2sv,isenforcedin2sv,suspended,lastlogintime,creationtime
./gam redirect csv ./tokens.csv all users print tokens
./gam redirect csv ./admins.csv print admins
./gam redirect csv ./drive-public.csv multiprocess all users print filelist query "visibility='anyoneWithLink' or visibility='anyoneCanFind'" fields id,name,mimetype,owners.emailaddress
```
If GAM says a field name isn't recognised, check its wiki for the current spelling. Never run any other GAM command in this check.

**B4. Summarise:**
```
python3 -I PATH_TO_SKILL/scripts/gam_summary.py --users users.csv --tokens tokens.csv --drive drive-public.csv --names
```
It prints: people without two-step login, admins, accounts never used or idle 90+ days, connected apps and which can read or send email or touch files, and public files. Names go in the owner's report only.

**B5. Turn it into findings:**
- Anyone active without two-step login: area 1, high for admins and anyone on email with customer data.
- More than two admins, or an admin who's left or idle: area 2.
- Never-used or 90-day idle accounts: area 2, medium (often ex-staff or test accounts; they still cost a licence).
- Connected apps that can read or send email, or read or change files: area 5. Ask the owner about each one: "Do you know what FreeQuoteAI is? It can read Jess's email." Unknown plus mail access = high.
- Public files: area 11, see `drive-sharing.md` for how to rate.

## After the check

- Leave the tools in place for the monthly check, or remove access: delete the "Security check" project in console.cloud.google.com (removes the key), and for GAM delete its project the same way. Then delete `~/FounderOS-security-tools/`.
- The access files (`google-credentials.json`, GAM's `oauth2.txt`, `oauth2service.json`) are keys. They stay in that private folder on the admin's computer only. Never in the brain folder, the chat, email or a shared drive.
- Write in `Stack.md` under "Checks that fit": "Google admin access approved YYYY-MM-DD by NAME, tools in ~/FounderOS-security-tools."

## Without the tools (guided)

If Python isn't available or the admin would rather not, walk the Admin console together and check the ten that matter most. Rate anything not checked as "not checked".

1. Security, Authentication, 2-Step Verification: allowed and enforced for everyone (area 1).
2. Directory, Users, add the "2-step verification enrolment" and "Admin role" columns: who's missing it, how many admins (areas 1, 2).
3. Account, Admin roles, Super Admin: two at most, both named people (area 2).
4. Security, Access and data control, API controls, Manage third-party app access: anything unknown with Gmail or Drive access (area 5).
5. Apps, Google Workspace, Drive and Docs, Sharing settings: outside sharing warning on, new files default to Restricted (area 11).
6. Apps, Google Workspace, Gmail, End user access, Automatic forwarding: off, or only to approved addresses (area 6).
7. Apps, Google Workspace, Gmail, Authenticate email: DKIM set up (area 9).
8. Apps, Google Workspace, Gmail, Safety: the attachment, link and spoofing protections switched on (area 6).
9. Security, Overview or Alert centre: anything unread and serious (all areas).
10. Directory, Users: anyone who's left still active (area 2).

## Credit

ScubaGoggles by CISA (CC0), based on CISA's SCuBA Google Workspace secure configuration baselines (public domain). GAM by the GAM team (Apache-2.0). Steps summarised in our own words from their documentation.
