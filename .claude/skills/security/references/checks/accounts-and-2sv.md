# Check: Accounts and two-step login

**Answers for the owner:** does every account that matters have two-step login, and does anyone still have access who shouldn't?

**Needs:** the owner's answers, walking through each tool in `Stack.md`. Plus connector or admin data where we have it (Google: `workspace-settings.md` gives the exact list of who has two-step login on).
**Feeds areas:** 1 (Two-step login), 2 (Limit admin access), 9 (registrar part), 12 (Passwords: shared logins).
**Time:** 10 to 15 minutes.

## How to run it

Go tool by tool through `Stack.md`, most important first. **One question at a time.** Never ask for a password or a code. If they read one out, say "Best change that one now," and write `[removed]`.

Order (this is the order scammers go after them):
1. Email (Google or Microsoft): it resets every other password.
2. The domain registrar and DNS host: whoever controls these controls email and the website.
3. Bank and payments (Stripe, Square, PayPal, the bank).
4. The books (Xero, MYOB, QuickBooks).
5. CRM (GoHighLevel, HubSpot, ServiceM8, Tradify, simPRO).
6. Website login (Wix, Squarespace, Shopify, WordPress) and hosting (Cloudflare, the host).
7. Social media and ad accounts (Meta Business, Google Ads).
8. AI tools (Claude, ChatGPT), and the password manager if they have one.
9. If they have code: GitHub, the database and the cloud account.

For each tool ask:
1. "Is two-step login on? What do you use for the code: an app, a text message, or a key?"
2. "Who else can log in? Anyone who's left, or an old contractor?"
3. "Who's the admin or owner on this account?"
4. "Is the login shared between people?"

Where you can confirm it yourself, do:
- **Google:** with the admin route (`workspace-settings.md`), `scripts/gam_summary.py --users` gives the exact list without asking. Without it, the admin can open Admin console, Directory, Users, and add the "2-step verification enrolment" column, then read you the count.
- **Their own Google account:** myaccount.google.com, Security, "2-Step Verification" says On or Off. Google's Security Checkup at myaccount.google.com/security-checkup lists devices and third-party access.
- **Screenshots:** for tools with no connector, ask for a screenshot of the users or team page. Read names and roles only. Don't save the screenshot into the brain.

## Questions only the owner can answer

Ask these too. They aren't visible from outside or from code. One at a time.

1. **Spend alerts.** "If someone got into your cloud, AI or payments accounts and ran up a bill, would you hear about it? Are spending alerts or limits on?" (Stripe, Google Cloud, AWS, the AI tools, SMS credits in the CRM.) Off = medium. Feeds area 5.
2. **Registrar.** "Where do you pay for the domain? Is two-step login on there? Is the domain locked against transfers?" (`domain-dns.md` checks the lock from outside.) Two-step off = high. Feeds area 9.
3. **Website protection.** "Is there a service in front of the website, like Cloudflare, that blocks bad traffic?" Not having one is low for a simple brochure site, medium for a site with logins or payments. Feeds area 10.
4. **Admin pages.** "Can anyone on the internet reach your website's admin login page, or is it limited (by a second login, a set list of locations, or the host's protection)?" For WordPress: is `/wp-admin` behind two-step login? Feeds area 2.
5. **Last outside review.** "Has anyone tested or reviewed your website or app's security in the last 12 months?" Only matters if they have custom code or take payments on their own site. No = low. Feeds area 3.
6. **Tripwires (optional, advanced).** Only if they have code or IT help: "Do you have any tripwires, like a fake key that alerts you if someone uses it?" (canarytokens.org is free.) Never push this on a small business. Absent = not a finding.

Backups ("is it running, and has anyone tested getting files back?") are in `devices-and-backups.md`.

## Red, amber, green

**Area 1, Two-step login** (also see `essential-eight.md`):
- **Green:** on for every person on email, payments, the books, the CRM, the registrar and the website login. Admins use an app or a key, not text messages.
- **Amber:** on for the owner and the main tools, but missing for some staff or one lower-risk tool, or text-message codes for admins.
- **Red:** off on email, payments, the bank or the registrar for anyone, or off on any admin account.

**Area 2, Limit admin access:**
- **Green:** two admins at most per tool, no shared admin login, nobody who has left has access.
- **Amber:** three or more admins, or the owner isn't sure who they are.
- **Red:** someone who has left still has access, or the admin login is shared.

**Shared logins** (area 12): a shared login on payments, the bank or email is red. Elsewhere amber.

## Plain-English fixes

Check the vendor's current help page for the click path. Say "the menu may look a little different" if you can't.

1. **Two-step login off on email (high).** Google: myaccount.google.com, Security, 2-Step Verification, Get started. Then the admin forces it for everyone: Admin console, Security, Authentication, 2-Step Verification, "Allow users to turn on" and set Enforcement to On from a date a week away. Microsoft: Security defaults or Conditional Access (see `microsoft-365.md`).
2. **Off on payments, bank or the books (high).** Each tool's security or profile page. Use an authenticator app (Google Authenticator, Microsoft Authenticator, or the password manager's).
3. **Someone who left still has access (high).** Remove them today. Google: Admin console, Directory, Users, suspend first (keeps their files), then transfer the files and delete. Change any shared passwords they knew.
4. **Too many admins (medium).** Downgrade everyone who doesn't add users or change settings to a normal user.
5. **Shared login (medium).** Separate logins where the tool allows. Where it doesn't, keep it in a password manager's shared vault and turn on two-step login with the code in that vault.
6. **Text message codes for admins (low).** Switch to an authenticator app. SIM-swap scams can steal text codes.
7. **No spend alerts (medium).** Set a monthly budget alert in each cloud, AI and payments tool. Stripe: Settings, notifications. Google Cloud: Billing, Budgets and alerts.
8. **Registrar without two-step login (high).** Turn it on in the registrar account today.
9. **Admin page open to the world (medium).** Two-step login on every admin account first. Then the host's protection, or a plugin that limits login attempts.
