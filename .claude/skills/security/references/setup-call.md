# Setup call script

For Byron or Pieter, running the first security check with a client on a video call. About 60 to 75 minutes. The owner drives their own computer and clicks every button. We talk, Claude does the checks.

## Before the call (10 minutes, us)

- [ ] Plugin installed on their computer (`references/install.md`), or plan 10 minutes at the start to do it together.
- [ ] Ask them to have ready: their laptop with Claude open, their phone (for two-step login codes), and their Google or Microsoft admin login (or the person who has it on the call).
- [ ] Know their stack roughly from the sales call. Don't run anything on their domain before the call: the first results should be seen together.
- [ ] Remind them: "We'll never ask for your passwords. You'll type those yourself, if at all."

## Opening (3 minutes)

> "Today we'll look at how safe the business is online. Email, website, accounts, files and your AI tools. It's read-only: nothing gets changed unless you click it yourself. At the end you'll have a score, a short list of fixes, and we'll knock off the top few together. Most businesses your size score between 40 and 70 the first time. That's normal."

## 1. Stack interview (5 to 10 minutes)

They say "security check" in Claude. Claude runs the interview (`references/stack-interview.md`). Let them talk. Jump in only to clarify ("Is the web designer still able to log in?").

## 2. The quick wins on screen (10 minutes)

Claude runs the no-access checks first: email spoofing, domain and DNS, website grade, AI tools first look. Results in a few minutes. Talk through each in one line:
- "Can a scammer email your customers pretending to be you? Here's the answer."
- "Your website gets a C. That's mostly settings your web person can change."

## 3. The checks that need them (20 to 30 minutes)

In this order, skipping what doesn't fit their stack:
1. **Password leaks.** They open Terminal and run the password checker themselves (`checks/password-breach.md`). Explain the privacy bit first. Look away from their screen. Ask only for the summary line.
2. **Accounts and two-step login** (`checks/accounts-and-2sv.md`). Tool by tool, one question at a time. Include the "ask me" questions: spend alerts, registrar, website protection, admin pages, last review.
3. **Devices and backups** (`checks/devices-and-backups.md`). If they're keen, test one file restore live.
4. **Drive sharing.** They connect Google Drive in Claude (`checks/drive-sharing.md`). Claude lists likely-sensitive files and who they're shared with.
5. **Google admin** (if they're the admin and have 45 minutes): ScubaGoggles and GAM setup (`checks/workspace-settings.md`). If time's short, book a second 45-minute session for this. Don't rush the admin approval screens.
6. **Code** (only if they have code and said yes): leaked keys and building blocks now, quick score after the call.

## 4. The report (5 minutes)

Claude writes `Security/Report YYYY-MM-DD.md` and `Security/Issues.md`. Read the three-line summary aloud: score, number of high fixes, the one thing first.

## 5. Fix together (15 minutes)

Top fixes, highest first, one at a time (SKILL.md step 5). Usual first three:
1. Two-step login on email and payments.
2. A sensitive file open to anyone with the link, back to Restricted.
3. Email spoofing protection (if they control DNS and it's quick), or leave it for their web person with a note Claude drafts for them.

Stop when they've had enough. Re-score at the end if anything was fixed: "You came in at 52, you're leaving at 64."

## 6. Close (5 minutes)

- Offer the weekly and monthly re-checks (`references/weekly-run.md`). Set them up together.
- Offer the calendar reminder.
- Say what's next: "Your next full check is DATE. Before then, the one thing is X."
- For retainer clients: "We'll review this with you each quarter."

## Rules for us on the call

- Never take control of their computer to type a password, and never ask them to read one out.
- Never look at file contents beyond what's needed to judge if a file is sensitive.
- Don't promise a score or that they're "secure". Say "safer than last week" and "here's what's left".
- No prices on the call unless agreed beforehand. Security is included in Founder OS; extra work (code fixes, a second admin session) is quoted separately by Byron or Pieter.
- If something serious turns up (signs of an account already broken into, money moved), pause the check, help them secure email first (change the password, sign out all sessions, check forwarding rules), and suggest they call their bank and report at cyber.gov.au (ReportCyber, or 1300 CYBER1).
