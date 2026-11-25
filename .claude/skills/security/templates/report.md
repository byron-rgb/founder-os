---
file: security-report
date: {{DATE}}
business: {{BUSINESS}}
score: {{SCORE}}
areas_checked: {{CHECKED}} of 13
previous: {{PREVIOUS_REPORT or "first check"}}
---

# Security check, {{DATE}}

**Score: {{SCORE}} / 100** ({{CHECKED}} of 13 areas checked)
{{One line vs last time, e.g. "Up from 58. 3 fixed, 1 new." Leave out on the first check.}}

{{Three lines for the owner: how it looks overall, how many high fixes, the one thing to do first.}}

## How each area looks

| Area | Rating | What we found |
|---|---|---|
| 1. Two-step login | {{Red / Amber / Green / Not checked}} | |
| 2. Limit admin access | | |
| 3. Keep apps updated | | |
| 4. Keep computers and phones updated | | |
| 5. Only approved apps | | |
| 6. Lock down the browser and apps | | |
| 7. Macros in Office files | | |
| 8. Backups | | |
| 9. Email and domain protection | | |
| 10. Website | | |
| 11. File sharing | | |
| 12. Passwords and leaked keys | | |
| 13. AI tools | | |

Ratings follow `references/essential-eight.md`. "Not checked" means we couldn't look, not that it's fine.

## Top fixes

Highest severity first. Five at most. Each one gets an issue number from `Issues.md`.

### 1. {{Fix in plain words, e.g. "Turn on two-step login for Sarah's Google account"}} ({{high / medium / low}}, issue #{{N}})
**Why:** {{one line, with a real-world example}}
**Time:** {{about N minutes}}
**Steps:**
1. {{Where to go, e.g. "Open admin.google.com and sign in as the admin."}}
2. {{What to click, in the words on the screen}}
3. {{What to choose}}
4. {{How to know it worked}}

{{Check click paths against the vendor's current help page before writing them. If unsure, add: "The menu may look a little different. Look for ..."}}

### 2. ...

## Everything else we found

| Issue | Area | Severity | Source |
|---|---|---|---|

## Not checked this time

| Area or check | Why | What it needs |
|---|---|---|
| {{e.g. Google Workspace settings}} | {{e.g. admin hasn't approved read-only access yet}} | {{e.g. 2 minutes with the admin}} |

## Checks run

| Check | Result | Source |
|---|---|---|

## Next check
{{Date of the next weekly or monthly check, and the one thing to do before then.}}
