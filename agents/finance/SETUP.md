# Finance agent setup interview

> Driven Young Founder OS. Licensed to one business (see LICENSE.md).

Needs: accounting connected (Xero, QuickBooks or MYOB) and email (receipts, scam checks, reminder drafts).
Runs: weekly, in the cloud.

Ask one question at a time, clickable options, recommendation first. Skip any the brain already answers (the bookkeeper may be in `brain/5 Team/Team.md` or `brain/6 Finance/Key Numbers.md`).

1. **Which day and time?** Monday 9am (recommended), Friday 3pm.
2. **When should an invoice be chased?** 7 days overdue (recommended), 14 days, 30 days, never draft reminders.
3. **Receipt limit:** flag spending with no receipt over $50 (recommended), $100, everything.
4. **Do you have a bookkeeper or accountant?** Name and email, so their receipts list is drafted for them. The agent never emails them itself.
5. **Anything to watch?** Optional: a slow-paying client, a loan, BAS or tax dates.
6. **Where should the report go?** In Claude (recommended), a draft email to yourself, your task app.

Save to `brain/Agents/Finance.md`:
```
# Finance agent settings
Runs: Monday 9:00 (<their time zone>)
Accounts: Xero (<organisation name>)
Chase after: 7 days
Receipt limit: $50
Bookkeeper: <name>, <email>
Watch: ...
Report goes to: Claude
Tools: Xero, Gmail
Set up: <date>

## Your rules
(Every correction you give the finance agent lands here as one line, newest first. It follows these.)
```
