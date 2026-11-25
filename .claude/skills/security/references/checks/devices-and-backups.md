# Check: Devices and backups

**Answers for the owner:** do work computers and phones keep themselves updated and locked, and could you get your files back if a laptop died or got locked by a scam?

**Needs:** the owner's answers (a guided checklist). Nothing is installed. On a Mac or Windows computer you can confirm a few things with them on screen.
**Feeds areas:** 4 (Keep computers and phones updated), 6 (Lock down the browser), 8 (Backups).
**Time:** 10 minutes.

## How to run it

Ask about each work device in `Stack.md`. One question at a time. If there are many staff, ask about the setup in general ("Do you manage the laptops, or does everyone sort their own?") and then spot-check one device together.

### Computers and phones

1. "Are automatic updates switched on?"
   - Mac: Apple menu, System Settings, General, Software Update, then the (i) next to Automatic Updates. All switches on, including "Install Security Responses and system files".
   - Windows: Settings, Windows Update. "Get the latest updates as soon as they're available" on, and no long pause.
   - iPhone: Settings, General, Software Update, Automatic Updates. Android: Settings, System (or Software update).
2. "Is any work computer or phone more than about 6 or 7 years old?" Old devices stop getting security updates. If unsure, ask for the model and year and check the maker's support page.
3. "Is the disk encrypted, so a stolen laptop can't be read?" Mac: System Settings, Privacy and Security, FileVault is On. Windows: Settings, Privacy and security, Device encryption (or BitLocker) is On.
4. "Does each computer and phone lock with a password, PIN or face after a few minutes?"
5. "Do people log in as themselves, or is there a shared login on any computer?"
6. Browser: "Any browser extensions you don't recognise?" (Chrome: the puzzle piece, Manage extensions.) Anything that can "read and change all your data on all websites" and nobody knows why it's there is a finding. Chrome: Settings, Privacy and security, Safe Browsing on (Standard or Enhanced).

### Backups

1. "If your laptop died tonight, what would you lose?"
2. "What's backed up, and where?" Cover: the books (usually safe in Xero or MYOB), email (Google or Microsoft keep it, but deleted is deleted), files, photos and job records, the website, any app database.
3. "Is the backup automatic?"
4. "Is there a copy a scammer or a mistake can't delete?" Sync alone (Google Drive, OneDrive, iCloud Drive, Dropbox) **isn't a backup**: if files get deleted or scrambled, the sync copies the damage. Look for version history, a separate backup service, Time Machine to a drive kept unplugged, or a cloud backup with its own login.
5. **"Has anyone actually tried getting a file back from the backup?"** Backups that have never been tested often don't work. This is the question that matters most.
6. Website and app: "If the website disappeared, could your host or web person put it back? When did they last check?"

If they're willing, test a restore together right now: pick one file from last week and get it back from version history or the backup. Five minutes, and it turns amber into green.

## Red, amber, green

**Area 4, Devices updated:**
- **Green:** auto-updates on for every work device, every device still supported, disks encrypted, screens lock.
- **Amber:** updates on but often put off, one or two devices unknown, or encryption off on a device that stays in the office.
- **Red:** a work device that no longer gets security updates, or a laptop that leaves the office with encryption off.

**Area 6, Browser:** see `essential-eight.md`. Unknown extension that can read every page = red.

**Area 8, Backups:**
- **Green:** important files and records backed up automatically, at least one copy that a normal login can't delete or change, and a restore has been tested in the last year.
- **Amber:** backups exist but nobody has tested a restore, or only some things are covered, or sync is the only "backup".
- **Red:** no backup, or the only copy is on the same laptop.

## Plain-English fixes

1. **Updates off (high if the device holds email or banking).** Turn on automatic updates (paths above). Restart once a week.
2. **Device too old for updates (high).** Plan to replace it. Until then, don't use it for email, banking or customer records.
3. **Disk not encrypted on a laptop (medium).** Turn on FileVault or Device encryption. Save the recovery key in the password manager, not on the laptop.
4. **No screen lock (medium).** Set a short auto-lock.
5. **Unknown browser extension that reads everything (high).** Remove it. If it had been there a while, change the email password.
6. **No backup (high).** Pick one: a backup service that suits their stack, Time Machine to an external drive for a single Mac, or their Google or Microsoft plan's retention and version history plus a separate backup for anything critical. We don't sell any of these.
7. **Never tested a restore (medium).** Do one together now, or book 15 minutes this month.
8. **Sync only (medium).** Add a real backup with its own login, or at least turn on version history and check how long deleted files are kept.

## Credit

Questions in our own words, informed by the ACSC Essential Eight, UK NCSC Small Business Guide (backups, devices) and CISA Secure Our World.
