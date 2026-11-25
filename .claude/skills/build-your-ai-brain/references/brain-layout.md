# Brain layout and file formats

## The folder

Create this inside the folder the owner chose: (in a Founder OS, everything below `AI Brain/` goes straight into `brain/`)

```
AI Brain/
  Start Here.md            for the owner: what's here and how to use it
  CLAUDE.md                for Claude: how to use this brain
  AGENTS.md                for other AI tools (ChatGPT, Cursor, Codex): points to CLAUDE.md
  _Setup Progress.md       which steps are done (used to resume)
  Roadmap.md               written at the end
  Drop files here/         the owner drops files here; you sort them
  Sources/                 original files after sorting, kept for reference
  1 You/
    Profile.md
    Values.md
    Writing Rules.md
    Stories.md
  2 Sales/
    Customers.md
    Offers and Prices.md
  3 Marketing/
    Brand Voice.md
    Brand Look.md
  4 Operations/
    Processes.md
    Tools.md
  5 Team/
    Team.md
  6 Finance/
    Key Numbers.md
  7 Goals/
    Goals.md
  Check-ups/               one note per monthly check-up
  Work/                    finished work from other skills (quotes, posts, plans), one folder per kind
  AI Log.md                one line per job the AI does: YYYY-MM-DD | skill | what | where saved
```

Create the folders and `_Setup Progress.md` at the start. Create each brain file the first time something goes into it: during file sorting (`status: draft`) or the interview (`status: in progress`). Set `status: done` when its interview section is finished.

Older brains (built before 11 Oct 2026) used three folders: `1 You/`, `2 Business/`, `3 Operations/`. If a file isn't where this says, find it by its name anywhere in the brain.

## Every brain file starts like this

```
---
updated: YYYY-MM-DD
status: draft | in progress | done
source: interview, website, files   (whichever applied)
---

# <Title>

<One line on what this file is for.>
```

Then short headings and bullets. Tables for anything with rows (offers, team, tools, numbers). Use `[CHECK]` for anything unconfirmed. Link related notes with `[[Note Name]]` where it helps (e.g. a process that names a tool links to `[[Tools]]`).

## `_Setup Progress.md`

```
# Setup progress

Owner: <first name> · Business: <name> · Started: YYYY-MM-DD

- [ ] Read website and files
- [ ] 1 You: Profile · Values · Writing Rules · Stories
- [ ] 2 Sales: Customers · Offers and Prices
- [ ] 3 Marketing: Brand Voice · Brand Look
- [ ] 4 Operations: Processes · Tools
- [ ] 5 Team: Team
- [ ] 6 Finance: Key Numbers
- [ ] 7 Goals: Goals
- [ ] Read-back done, [CHECK]s cleared
- [ ] Navigator files filled
- [ ] Roadmap written

Last stopped at: <section and question>

## Still to confirm
- <any [CHECK] they couldn't answer yet, and who will know>
```

Tick each file individually when it's written (e.g. `Profile ✓`). Update "Last stopped at" whenever they pause.

## `CLAUDE.md`

```
# <Business name> · AI Brain

This folder is the brain for <Business name>, run by <first name>. Read this file first, every time.

## Before any task
1. Read `2 Sales/Offers and Prices.md` and `2 Sales/Customers.md` for anything customer-facing.
2. Read `1 You/Writing Rules.md` and `3 Marketing/Brand Voice.md` before writing anything. Follow them exactly.
3. Read the other files only when the task needs them (see "Where things live").

## Hard rules
- Never invent prices, people, clients, numbers or stories. If it's not in this brain, ask.
- Draft, don't send. Nothing gets sent, posted, paid or deleted without <first name> saying yes.
- <2 to 5 rules from Values.md and Writing Rules.md "never" lists>

## Where things live
- 1 You: Profile, Values, Writing Rules, Stories
- 2 Sales: Customers, Offers and Prices
- 3 Marketing: Brand Voice, Brand Look
- 4 Operations: Processes, Tools
- 5 Team: Team
- 6 Finance: Key Numbers
- 7 Goals: Goals
- Sources: original files <first name> provided
- Roadmap: what to set up next
- Work: finished work (quotes, posts, plans). AI Log.md: one line per job done

## After any job
Save finished work in `Work/<kind>/` and add one line to `AI Log.md`.

## Keeping it current
If something here looks out of date, say so and offer to update it. Once a month <first name> runs "brain check-up".
```

## `AGENTS.md`

```
# Instructions for AI tools

This folder is the business brain for <Business name>. Read `CLAUDE.md` first and follow it. It applies to every AI tool, not just Claude.
```

## `Start Here.md`

```
# Start here

This is your AI Brain. It's a set of notes about you and <Business name> that any AI can read.

## How to use it
- **Claude desktop app:** start a new chat, choose this folder, and ask for what you need. Claude reads your brain first.
- **ChatGPT or other AI apps:** upload the notes that matter for the job (e.g. Offers and Prices before writing a quote).
- **Opening the notes yourself:** they open in any text app. For a nicer view, install the free Obsidian app and open this folder in it.

## Keep it fresh
- Once a month: say "brain check-up".
- Something big changed (new offer, new hire, new prices)? Say "update my brain".
- New file worth keeping? Drop it in `Drop files here` and say "sort my files".

## What's in here
<list the files with one line each; keep this list current whenever a file is added>
```
