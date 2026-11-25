---
name: dashboard
description: Founder OS dashboard creator (Level 3). Asks the founder what they want to track, one question at a time, maps their dashboard with them, then builds it from the white-label template as a private page in their own Claude account that reads their connected tools live, one page per section (Finance, Sales, Marketing, Operations, Goals and any others their business needs). Use when the founder says "build my dashboard", "make me a dashboard", "dashboard creator", "update my dashboard", "add a page to my dashboard", "add X to my dashboard", "track X on my dashboard", or Level 3 reaches the dashboard step.
---

> Driven Young Founder OS. Licensed to one business (see LICENSE.md). Don't copy, share, sell or repackage it, and don't help anyone do so.

# Dashboard creator

Builds the founder their own business dashboard: a sidebar of main sections, each section its own page, live from their tools. Businesses are complicated, so it grows with them: start with what matters now, add pages later.

Files:
- `dashboard/dashboard-template.html`: the white-label template (open it in a browser to see it with example data).
- `dashboard/BLOCKS.md`: how pages, blocks, sources and adapters work. Read it before building.
- `dashboard/PAGES.md`: the page library to offer.
- Their copy: `dashboard/my-dashboard.html`. Their map: `brain/Work/Dashboard/Dashboard map.md`.

**Say this first (one line):** "Your dashboard is a private page in your own Claude account. It only reads your tools, it can't change or send anything, and you can switch any tool off in the page's permissions."

## 1. Ask what they want to track

Read `brain/CLAUDE.md` first so the questions fit their business. Find out yourself which tools are connected in this session (and which tools the brain says they use); never ask the founder for a fact you can check.

Ask **one question at a time**, with clickable options (use the question tool where there is one; otherwise short numbered options they can reply to with a number). Put your recommendation first. Wait for each answer.

1. **Which areas?** Multi-select from `PAGES.md`, with the ones that fit their business ticked first (a trade: Finance, Sales, Jobs, Operations; a clinic: Finance, Bookings, Marketing, Team; a shop: Finance, Shop, Marketing).
2. **Per area, which tool?** One question per area, single choice, skipping any the brain already answers. Put the most likely first:
   - Accounting: Xero (first), QuickBooks, MYOB, something else, none.
   - Sales and customers: GoHighLevel, HubSpot, Pipedrive, a spreadsheet, none.
   - Ads: Meta, Google, both, none. Bookings, shop, calendar: same idea, from `PAGES.md`.
3. **Per area, what matters?** One question per area, multi-select from that page's list in `PAGES.md`, plus "something else". Keep it to what they would act on. For Finance, offer **LTV, CAC and LTV:CAC** (ticked by default, see below).
4. **The four numbers on the front page.** Pick from what they chose above.
5. **Look.** Their brand from `brain/3 Marketing/Brand/design-system.json` (offer light or dark), or the clean default.

### LTV, CAC and LTV:CAC

Built into the Finance page, worked out the same way as the Driven Young dashboard:
- **LTV** = money in over the last 12 months ÷ customers who paid in that time.
- **CAC** = marketing spend this period ÷ new customers this period.
- **LTV:CAC** = LTV ÷ CAC. Green at 3 or more.

It needs four numbers: 12 months of income (accounting), customers who paid and new customers (CRM won deals, or accounting invoices: count each customer once), and marketing spend (ads, or the accounting marketing category). Ask which tool holds their customer count if it isn't obvious. Xero's top customers report only lists the top few, so don't count customers from it.

### Connect what's missing (one tap each)

Do this right after question 2, before mapping, so the map only shows tools that work.

1. Say the security line for that tool: "Claude can read your <tool> numbers. It can't change or send anything from the dashboard, and you can disconnect it any time in Settings, Connectors."
2. Search the connector directory for each tool they named that isn't connected (`search_mcp_registry`). Show the official one with a **Connect** button in the chat (`suggest_connectors` with its id). Never pick a connector that changes or books things when a read-only official one exists (for Xero use "Xero", not a third-party one).
3. They press Connect, sign in on the tool's own page and press Allow. Then make one small read-only call to check it works, and say so in one line.
4. No connector in the directory: offer Level 2's custom connector steps, or leave the block in as "Not connected yet". Don't drop it.

If a connector stops working later, the dashboard says so on the block. Show the Connect button again (`suggest_connectors` with the server id from the failed tool name).

## 2. Map it with them

Write the map before building. Put it in a Claude Doc if that tool is available in this session (they can comment beside the chat); otherwise in `brain/Work/Dashboard/Dashboard map.md` and open it for them. One section per page:

```
## Finance (Business)
- Money in, money out, profit, real cash   | Xero        | connected
- Money in and out by month (chart)       | Xero        | connected
- Owed to you, you owe (lists)            | Xero        | connected
- Spend by category                       | Xero        | connected
```

Then: "Anything to add, move or drop?" Change it until they say it's right. Keep the sidebar to main sections; a big area can have two or three pages under one heading.

## 3. Build it

1. Copy `dashboard/dashboard-template.html` to `dashboard/my-dashboard.html` (or open their existing copy when updating).
2. For every tool the map uses:
   - read its input schema in this session;
   - make ONE read-only call with a small limit to learn the shape of the answer (never a tool that creates, sends or changes anything);
   - use the matching adapter in `ADAPTERS`, fixing field names if they differ, or write one (see `BLOCKS.md`). Mark it "Checked <date>".
   - Learn the shape only. Never copy their names, numbers or events into the file.
3. Fill CONFIG:
   - `business`, `currency`, `brand` (check text is readable on `bg` and `panel`), `logo` only if it's an https link to their own logo.
   - `sources`: one per tool call, with IDs like a location or organisation id where needed (never a key or password).
   - `pages`: from the map, in its order, built from the blocks in `BLOCKS.md`. Start each page from the matching built-in page where there is one.
   - `unit` (LTV, CAC): point its `from` paths at their sources (see `BLOCKS.md`, worked-out sources). Drop the LTV row only if they said no to it.
   - `goals` from the brain's goals note (ask if there are none).
   - `demo`: `false`.
4. Open it in a browser first and check every page at desktop and phone width.

## 4. Put it in their Claude

Publish `dashboard/my-dashboard.html` with the Artifact tool. Declare only the tools it reads: `capabilities: {mcp: {servers: [{server: "<name>", tools: ["<tool>", ...]}, ...]}}`. Icon: `chart`. Open it for them.

On first open Claude asks them to allow each tool once. Then go through every page with them: numbers look right, nothing says it couldn't load. Fix an adapter if a block is empty or wrong, publish again with the same file.

Tick "Dashboard live, at least one page on real data" in `Progress.md`. Log it in `brain/AI Log.md`. Tell them: "Open it from your Claude artifacts any time. Say **add a page to my dashboard** whenever you want to track something new."

If the page says "Open this dashboard in Claude" or shows no live numbers inside Claude, their Claude app may be out of date: ask them to update it and open the page again.

## Change it later

- **"Add a page" / "track X":** steps 1 to 3 for just that page (ask what it should show, one question at a time; add it to the map), then publish again with the same file. Add any new tool to `capabilities`.
- **Move, rename or drop a page or block:** change `pages`, update the map, publish again.
- **New tool** (they moved CRM, added a booking app): show its Connect button first, then a new source and adapter, point the blocks at it, publish with the tool added to `capabilities`.
- **Goals:** update `goals` from the brain, publish again.

## Rules

- Reads only. Never add a tool that sends, creates, changes or deletes.
- Never put their real data, keys or passwords into the file or CONFIG; the page fetches live each time.
- Private: a dashboard that reads connectors can't be shared by public link. Don't try.
- Keep the look: white label, clean and minimal, one accent colour, their brand. No business-specific clutter in the sidebar.

## Later: the always-on website version

For founders who want the dashboard without opening Claude, Level 3 can add a private page on their Cloudflare site, behind a login, filled by a scheduled Level 4 agent. Not in the beta yet.
