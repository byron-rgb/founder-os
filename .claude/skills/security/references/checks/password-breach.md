# Check: Password leaks

**Answers for the owner:** is a password you use on a known list of leaked passwords?

**Needs:** nothing. The owner types each password into their own Terminal. **The password never leaves their computer, and Claude never sees it.**
**Feeds area:** 12 (Passwords and leaked keys).
**Time:** a few minutes.

## How it keeps the password private

Have I Been Pwned (HIBP) keeps a free list of over a billion passwords from real leaks. Our script scrambles the password on the owner's computer, sends only the first 5 characters of the scramble, and gets back hundreds of possible matches (padded so even the reply size gives nothing away). The match is checked on the owner's computer. HIBP can't tell which password was checked. This is called "k-anonymity" and it's how password managers do the same check.

Say it simply: "The password stays on your computer. Only a tiny scrambled piece goes out, and it matches hundreds of passwords, so nobody can work out yours."

## Hard rules

- **Never ask the owner to type a password into the chat.** If they do, say "Best change that one now, since it's been shared in a chat," and never write it anywhere. Write `[removed]`.
- **Never pass a password to the script as a command option** (it would end up in history). The script has no option for it on purpose. It asks with hidden typing.
- **Never send a full password or a full scramble (hash) anywhere.** Only the 5-character prefix goes out, and only to `api.pwnedpasswords.com`.
- Record counts only: "4 checked, 1 on a leak list". Never which account or which password.

## How to run it

1. Explain the privacy bit above in two lines.
2. Ask the owner to open Terminal themselves (Mac: Spotlight, type Terminal) and run:
   ```
   python3 -I "PATH_TO_SKILL/scripts/password_check.py" --many
   ```
   Give them the full path to this skill's `scripts/` folder. They type each password they use for email, banking, the CRM, the books and the website login, pressing Enter after each. A blank line finishes.
3. Ask them to read out only the last line: "Summary for the report: N checked, M on a leak list."
4. If Python isn't there: their password manager very likely does the same check (1Password Watchtower, Bitwarden reports, Apple Passwords "Security Recommendations", Google Password Manager "Password Checkup"). Walk them to it instead. Same privacy method.

## Even better: the password manager check

If they already use a password manager, its built-in check covers every saved password at once, plus reused and weak ones. Prefer it. Ask for the counts only (compromised, reused, weak).

## Red, amber, green (area 12, password part)

- **Green:** a password manager in use, and none of the checked passwords are on a leak list.
- **Amber:** no password manager yet, or a leaked or reused password that they've already changed.
- **Red:** a password still in use that is on a leak list, or the same password on email and banking.

Combine with `leaked-keys.md` (keys in files) and the accounts check for the final area 12 rating.

## Plain-English fixes

1. **Leaked password still in use (high).** "Change it today on every account that uses it. Let a password manager make the new one." Start with email, because email resets everything else.
2. **No password manager (medium).** Suggest the one that fits their stack: Apple Passwords (built in, all-Apple teams), Google Password Manager (built into Chrome and Android), 1Password or Bitwarden (teams, sharing logins safely). We don't sell any of them.
3. **Shared logins (medium).** "Give each person their own login. If a tool truly can't, share it through the password manager, never by text or a spreadsheet."

## Staff email breach search (paid add-on, documented only)

HIBP can also say which staff email addresses turned up in which breaches. That needs a paid HIBP API key and domain verification, so it isn't part of the standard check. If a client wants it:
- They buy the key themselves on haveibeenpwned.com (their account, their key) and verify their domain there. HIBP's own domain search dashboard needs no code at all and has been free for small domains: check the current pricing on haveibeenpwned.com and suggest that first.
- We never hold the key. Never paste it into the chat or a file in the brain folder.
- Report counts and breach names only, not a list of people.

## Credit

Pwned Passwords by Troy Hunt, haveibeenpwned.com. Data licensed CC BY 4.0: credit HIBP in the report.
