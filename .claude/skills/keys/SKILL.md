---
name: keys
description: Founder OS guide to API keys and secrets. Teaches the founder where a key comes from, where it lives (password manager, Cloudflare secret, local .env that never leaves the computer), and puts it in place without the key ever going through the chat. Use when the founder says "I need an API key", "where do I put this key", "add my GHL key", "set up my secrets", "is my key safe", "I pasted my key", or any setup step needs a key, token or secret (GoHighLevel Private Integration token, Google Maps key, and similar).
---

# Keys and secrets

A key (API key, token, secret) is a password for a program. Anyone who has it can act as the business in that tool. Treat it exactly like a password.

**The one rule: the key never goes through this chat.** The founder copies it straight from the tool into the safe place. You tell them where to click; you never see the value.

## Most of the Founder OS needs no keys
Say this first, it calms people down:
- Claude connectors (Gmail, Calendar, Drive, Xero and others): you sign in on the tool's page. No key.
- Cloudflare: you sign in once in the browser. No key.
- GitHub: you sign in once in the browser. No key.
- Scheduled agents: use your connectors. No key.

Keys only come up for a few things, mostly **your website's forms** (Level 3).

| What | Needs a key? | Where it lives |
| --- | --- | --- |
| Website forms to GoHighLevel | Yes: a GoHighLevel **Private Integration token** and your Location ID | Cloudflare secret (live site), `.env` on your computer (testing) |
| GoHighLevel in Claude | Only if it asks for a token instead of a sign-in | Claude's connector settings, never a file |
| Google Maps on your site | A public key, still restrict it to your domain | Cloudflare variable |
| Google Analytics ID | Not secret | Site settings |

## Where keys live
1. **Your password manager** (1Password or Apple Passwords). The master copy. Name it clearly: "GHL Private Integration: website forms".
2. **Cloudflare secrets** for the live site. Stored encrypted. Nobody can read them back, including you.
3. **`.env` file** on your computer, only for testing the site. It's on the Founder OS ignore list, so it is never saved to GitHub. Claude doesn't open it.

Never: in the chat, in the brain, in any other file, in an email, in a screenshot, in a shared doc.

## Make a key (GoHighLevel example)
1. GoHighLevel, **Settings**, **Private Integrations**, **Create new integration**.
2. Name it after the job ("Website forms"). Pick only the permissions it needs: **contacts.write** for forms. Less is safer.
3. Copy the token. Paste it into your password manager first.
4. Copy your **Location ID** from Settings, Business Profile (this one isn't secret).
Menus move: if it looks different, describe what you see and I'll find the current steps on GoHighLevel's help site.

## Put it on the live site (you type it, not me)
Open **Terminal**, go to your site folder, and run the command below. When it asks "Enter a secret value", paste the token. It stays hidden. Press Enter.
```
wrangler pages secret put GHL_API_KEY --project-name <your-project>
```
I'll give you the exact command with your project name filled in. You run it.

## Testing on your computer
Open `site/.env` yourself in TextEdit (I'll create it with blank lines), paste the token after `GHL_API_KEY=`, save, close. I'll check the form works without opening the file.

## If a key gets out
Pasted it in a chat, a file, a screenshot, or saved it to GitHub? No panic, fix it now:
1. Delete that key in the tool (GoHighLevel: Private Integrations, delete or rotate).
2. Make a new one, save it in your password manager, put it back in Cloudflare.
3. If it went to GitHub, say "security check" afterwards; the leaked-keys check scans for it.

## For Claude, always
- Never ask for a key's value. If they start to paste one, stop them: "Don't paste it here. Put it in your password manager, then I'll show you where it goes."
- If one is pasted anyway: don't repeat it, don't write it anywhere, tell them to replace it (steps above).
- Never read `.env`, `.dev.vars` or any secrets file. Never write a key into code, the brain, notes or a commit.
- Any setup guide (including a template's own setup command) that says "give me your API key": skip that step and use this skill instead.
- Least access: every key gets only the permissions its job needs, one key per job.
