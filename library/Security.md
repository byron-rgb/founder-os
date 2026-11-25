# Security

Plain English. No scare tactics. Here's what's safe, what to watch, and how to check.

## Is AI safe for my business?
Yes, set up properly. The Founder OS is built so that:
- **Claude only sees what you give it.** The folder you pick, the tools you connect. Nothing else.
- **Claude asks first.** Before it runs or changes anything, you get a box with Yes or No.
- **Claude never sees your passwords.** You sign in to each tool on its own page.
- **Agents draft, you send.** Nothing is emailed, paid, posted or deleted without you.
- **You own everything.** Your accounts, your files, your private GitHub.

## Five habits that stop most problems
1. **Two-step login** on email, Claude, GitHub, Cloudflare, your CRM and your bank.
2. **A password manager** (1Password or Apple Passwords). One strong, different password per account.
3. **No secrets in chats or files.** Never paste a password, card number or key into Claude. If you do, change it.
4. **Only install from the source.** Skills, plugins and connectors from the maker's own page. Never a link someone sent you.
5. **Press No when unsure.** If a permission box doesn't make sense, say No and ask Claude what it's for.

## API keys and secrets
Most of the Founder OS needs **no keys**: you sign in to Claude connectors, Cloudflare and GitHub in the browser. Keys only come up for a few things, mostly your website's forms sending leads to GoHighLevel.

When one does:
- **The key never goes in the chat.** You copy it from the tool into your password manager, then into the safe place. Claude tells you where to click and never sees it.
- **Three safe places:** your password manager (master copy), Cloudflare secrets (the live site, encrypted), and `site/.env` on your computer (testing only, never saved to GitHub).
- **Least access.** One key per job, with only the permissions that job needs.
- **Leaked one?** Delete it in the tool, make a new one, put it back. Then run a security check.

Say **help me with a key** and Claude walks you through it.

## Your security check
Say **security check**. About 30 minutes the first time. Claude asks what tools you use, then checks only what fits:
- Can scammers send email pretending to be you
- Your website's grade and certificate
- Whether your email shows up in known password leaks
- Two-step login on your key accounts
- Who your files are shared with
- The AI skills, plugins and connections you've installed
- Backups and devices
- Your Google or Microsoft admin settings, if you have them
- Your site's code, if you built one in Level 3

You get a score out of 100 on Australia's Essential Eight, a short list in order, and Claude walks you through each fix. Claude only looks; you click every button.

## Every week after
In Level 4 the **Security agent** runs a light check each week and a deeper one each month. You get one line: "2 new, 1 fixed."

## Is this skill, plugin or connector safe?
Before installing anything new, say: **is this safe: <link>**. Claude reads it and tells you what it can reach, who made it, and whether to install it.

## If something goes wrong
Say **I think I've been hacked**. Claude walks you through the first steps: change the password, sign out other devices, check recent activity, tell your bank if money is involved.

---
Driven Young Founder OS · licensed to one business · see LICENSE.md
