# Dashboard blocks (for Claude)

> Driven Young Founder OS. Licensed to one business (see LICENSE.md).

How `dashboard-template.html` is put together, so Claude can build any page a business needs. The founder never needs to read this.

## The three parts of CONFIG

```json
{
  "business": "Their business name",
  "logo": null,
  "demo": false,
  "currency": "AUD",
  "brand": { "bg": "#F7F7F5", "panel": "#FFFFFF", "text": "#17191E", "muted": "#6B6F76", "accent": "#2F5BEA", "line": "#E6E6E2" },
  "periods": ["month", "quarter", "year"],
  "sources": { "<key>": { "server": "Xero", "tool": "get_cash_position", "input": {}, "adapter": "xeroCash" } },
  "pages": [ { "id": "finance", "title": "Finance", "icon": "wallet", "group": "Business", "intro": "", "blocks": [] } ],
  "goals": []
}
```

- **sources**: one entry per tool call. `server` is the connector's display name exactly as it shows in the session. `adapter` names a function in `ADAPTERS` that turns the tool's answer into plain data. Inputs can use `{from}` and `{to}` (follow the period picked at the top of the page), `{today}`, `{monthStart}`, `{now}`, `{in7days}`, `{yearAgo}`, and `{prevFrom}`/`{prevTo}` (the same stretch of the period before, for "% on last period"). A source with an empty `server` shows "Not connected yet".
- **pages**: one page per section. They show in the sidebar in this order. `group` puts a small heading above a run of pages (Business, Growth, Running, Team...). `icon` is a Phosphor icon name from the list below.
- **blocks**: what's on the page, top to bottom. Every block takes `title`, an optional `note` (small grey text on the right of the title), `width` (12 full, 8, 6 or 4; stacks on phones) and `empty` (what to say when there's nothing).

- **worked-out sources**: `{ "derive": "unitEconomics", "from": { "revenue": "pnl12.income", "customers": "customers.active", "newCustomers": "customers.newThisPeriod", "marketing": "spend.total" } }`. No tool of its own: it reads the paths in `from`, then runs a function in `DERIVE` whenever one of them arrives. If one of them fails, the block shows that tool's message. Use it for any number that mixes tools.

Blocks read data by **path**: `"pnl.income"` means source `pnl`, then the `income` field of what its adapter returned. Only the sources the open page uses are read, so add as many pages as the business wants.

## Blocks

| type | reads | shows |
|---|---|---|
| `stats` | `items: [{label, value, format, sub, change, invert, tone, good, icon}]` | A row of headline numbers. `value`, `sub` and `change` can be paths. `change` = % on last period (green up, red down; `invert: true` when down is good, like spend). `tone`: `sign` (green or red by sign), `accent`, or `atLeast` with `good` (green at or above it, red below; LTV:CAC uses 3). |
| `kv` | `data` → `[{label, value, format}]`, or `items` with paths | A label and value list ("Spend and return"). |
| `list` | `data` → `[{title, sub, value, tag, tone}]`, `total` (path), `format`, `limit` | People, invoices, bills, tasks. `tone` on the tag: `good`, `bad`, `warn`, `acc`. |
| `bars` | `data` → `[{label, value}]`, `format`, `limit` | Ranked bars (spend by category, pipeline by stage, leads by source). |
| `chart` | `data` → `{labels, series: [{name, values}]}`, `format`, `stacked`, `table` | Bar chart by month or week. `stacked: true` stacks the series. `table: true` adds the numbers underneath with a total row. |
| `table` | `data` → `{columns: [{label, align: "r", format}], rows: [[...]], total: [...]}`, `limit` | Any table (profit per job, deals, clients). |
| `funnel` | `data` → `[{label, value, cost}]`, `format`, `costLabel` | Leads to sales, with the % between steps and the cost per step. |
| `week` | `data` → `{events: [{title, start, end, allDay}]}` | The next few days from a calendar. |
| `goals` | CONFIG `goals` | Goal cards. Each goal: `title`, `target` (one line), `status` (`on_track`, `behind`, `done`, `not_started`), optional `current` + `goal` numbers for a progress bar, `money: true` for dollars. |
| `text` | `text` | A short note. |

Formats: `money`, `number`, `percent` (give 0 to 100, not 0 to 1), `ratio` (6.7x). Text values show as they are.

## Adapters

One function per tool, in `ADAPTERS`. It gets the tool's answer (`payload`) and returns an object with the fields the blocks read. Rules:

- Write it from ONE real, read-only call made in the founder's session with a small limit. Learn the shape only; never copy their names or numbers into the page.
- **Throw** if the answer isn't the shape you expect (the list or field is missing). The block then says "answered in a way this block doesn't understand" instead of showing zeros.
- Lists from tools usually stop at 100. For a count, ask for 1 result and read the tool's total.
- Big areas (jobs, bookings, orders): write one shared helper like `shapeDeals` that turns a list into everything the page reads, and point every adapter for that area at it.
- Return numbers as numbers. Do the maths in the adapter (totals, % change, grouping by month), not in the blocks.
- CRMs: build a list of deals `{name, stage, value, updated, late}` and pass it to `shapeDeals(deals, wonValue)`; it returns everything the Sales page reads.
- Mark each adapter in a comment: "Checked <date>" or "NOT yet checked".
- Already checked: `xeroCash`, `xeroPnl` (totals, last period, categories, marketing), `googleCalendar`, `ghlOpportunities`/`ghlWon`/`ghlCount` (answer shape). Not yet checked: `xeroReceivables`, `xeroPayables`, GHL date filters. Money in and out by month needs one P&L call per month (six sources, or a worked-out source over them).

## Worked-out numbers

`DERIVE.unitEconomics` gives `ltv`, `cac`, `ratio`, `newCustomers` and the small text under each. Same maths as the Driven Young dashboard: LTV = 12 months' income ÷ customers who paid, CAC = marketing spend ÷ new customers. `from` points at `pnl12.income`, `customers.count`, `won.count` and `pnl.marketing` by default.

## Demo data

`DEMO()` returns made-up data for every source key, so the page shows something before anything is connected (`"demo": true`). When adding a new source, add a demo entry with obviously made-up names. Turn `demo` off for the founder's own copy.

## Icons

house, wallet, handshake, megaphone, calendar-blank, target, users-three, chart-line-up, chart-bar, briefcase, gear, currency-circle-dollar, storefront, star, clipboard-text, truck, heart, graduation-cap, package, user-circle, buildings, receipt, envelope-simple, instagram-logo, globe, phone, wrench, calendar-check, shopping-cart. Anything else shows a plain square: add its SVG to `ICONS` from `@phosphor-icons/core` (regular weight).

## A new kind of block

Add a function to `BLOCKS` that draws into a card, keep the same look (cards, muted labels, one accent), and list it in this file. Values from tools always go in with `textContent`, never as HTML.
