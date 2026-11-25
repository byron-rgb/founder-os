---
name: dashboard
description: Founder OS Level 3 founder dashboard. Builds one private dashboard page in the founder's own Claude account that reads their connected tools live each time they open it, with main sections Finance, Sales, Marketing, Operations and Goals. Use when the founder says "build my dashboard", "update my dashboard", "add X to my dashboard", "turn off the money module", "add my goals to my dashboard", or Level 3 reaches the dashboard step.
---

> Driven Young Founder OS. Licensed to one business (see LICENSE.md). Don't copy, share, sell or repackage it, and don't help anyone do so.

# Founder dashboard

One page, saved in their Claude account, that shows their business at a glance. It reads their tools every time they open it, using their own connections. Template: `dashboard/founder-dashboard.html`. Their copy: `dashboard/my-dashboard.html`.

**Say this first (one line):** "Your dashboard is a private page in your own Claude account. It only reads your tools, it can't change or send anything, and you can switch any tool off in the page's permissions."

## Build it ("build my dashboard")

1. **What's connected.** Check which of these tools you can use in this session: accounting (Xero, QuickBooks, MYOB) for Finance; a CRM (GoHighLevel, HubSpot, Pipedrive) for Sales; social, website or ads stats (GHL Social Planner, Search Console, Meta) for Marketing; a calendar (Google Calendar, Outlook) and task app for Operations. A module with no tool behind it: offer Level 2 to connect it, or leave that module off for now. Goals need no tool.
2. **Learn each tool's answer.** For every tool the dashboard will read:
   - read its input schema in this session;
   - make ONE read-only call with a small limit to see the shape of the answer (never a tool that creates, sends or changes anything);
   - match it to an adapter in the template's `ADAPTERS`. Checked already: `googleCalendar`, `xeroCash`, `xeroMonth`. Not yet checked: `ghlOpportunities` (check it against the real answer and fix field names). A tool with no adapter: write one that returns the module's shape (written above `ADAPTERS`).
   - Only learn the shape. Never copy their real names, numbers or events into the page.
3. **Fill CONFIG** in a copy of the template saved as `dashboard/my-dashboard.html`:
   - `business`: their business name from the brain.
   - `brand`: `bg`, `panel`, `text`, `muted`, `accent` hex colours from `brain/3 Marketing/Brand/design-system.json` (dark or light, whatever their brand is). Check the text is readable on `bg` and `panel`.
   - `currency`, and `modules` on or off (ids: `money` = Finance, `leads` = Sales, `marketing`, `week` = Operations, `goals`). Keep to these main sections; don't add business-specific ones to the sidebar.
   - Marketing has no checked adapter yet: write one from the real answer that returns `{stats:[{label, value, change}], sources:[{name, leads}]}`.
   - `sources`: per module, the connector's display name exactly as it shows in this session (for example `"GHL"`, `"Google Calendar"`, `"Xero"`), the tool's name, its input (IDs like a location or organisation id are fine; never a key or password), and the adapter. Dates can use `{today}`, `{monthStart}`, `{now}`, `{in7days}`.
   - `goals`: up to 6 from the brain's goals note, each with `title`, `target` (one line: what's left or how they'll know) and `status` (`on_track`, `behind`, `done`, `not_started`). Where the goal is a number, add `current` and `goal` (and `"money": true` for dollars) so it draws a progress bar. Ask if the brain has none.
   - `demo`: `false`.
4. **Put it in their Claude.** Publish `dashboard/my-dashboard.html` with the Artifact tool. Declare only the tools it reads: `capabilities: {mcp: {servers: [{server: "<name>", tools: ["<tool>", ...]}, ...]}}`. Icon: `chart`. Open it for them.
5. **First open.** Claude asks them to allow each tool once. Then check every module: numbers look right, nothing says it couldn't load. Fix an adapter if a module is empty or wrong, then publish again with the same file.
6. Tick "Dashboard live, at least one module on real data" in `Progress.md`. Log it in `brain/AI Log.md`.
7. Tell them: "Open it from your Claude artifacts any time. Say **update my dashboard** to change it."

If the page shows "Open this dashboard in Claude" or no live numbers inside Claude, their Claude app may be out of date: ask them to update it and open the page again.

## Change it ("update my dashboard")

- **Modules on or off:** change `modules` in their copy and publish again. (The page's Modules button also hides a module on one device.)
- **Goals:** update `goals` from the brain, publish again.
- **A new tool** (they moved CRM, added a task app): steps 2 and 3 for that tool, publish again with the new tool added to `capabilities`.
- **A new module** (for example social stats or website visits): add a `DRAW` function and an adapter in their copy, keep the same look, then publish.

## Rules

- Reads only. Never add a tool that sends, creates, changes or deletes.
- Never put their real data, keys or passwords into the page or the CONFIG; the page fetches live each time.
- Private: a dashboard that reads connectors can't be shared by public link. Don't try.

## Later: the always-on website version

For founders who want the dashboard without opening Claude, Level 3 can add a private page on their Cloudflare site, behind a login, filled by a scheduled Level 4 agent. Not in the beta yet.
