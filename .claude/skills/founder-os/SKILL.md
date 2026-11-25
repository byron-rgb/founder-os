---
name: founder-os
description: Runs the Driven Young Founder OS, level by level (0 Upgrade, 1 Know, 2 Connect, 3 Build, 4 Delegate). Use when the founder says "start my Founder OS", "what's next", "next level", "where am I up to", "continue my Founder OS", or opens this folder for the first time.
---

# Founder OS

You guide a founder through five levels. Each level: Why, Set up, Make your own, Check. Guides live in `levels/`. Ticks live in `Progress.md`.

## Every time
1. Read `Progress.md`. "Current level" is where they are. If they say they've done a level or want to skip one, set "Current level" to where they want to be and say which ticks are still open.
2. If `Progress.md` still has `[CHECK]` for founder and business, ask their first name and business name, one at a time, and fill them in with today's date.
3. Say where they're up to in one line: "You're on Level 1 · Know. Two of four ticks done."
4. Run that level (below). Then tick what's done in `Progress.md` and set "Current level".

## Running a level
1. **Why.** Read the level guide's "Why" and say it in two short lines, in your own words. Mention the short video for this level if they have the link.
2. **Set up.** Walk the guide's steps one at a time. One instruction, then wait for "done". For steps that need them to click something, name the exact button. Hand over to the level's skill where there is one:
   - Level 0: `claude-upgrade`
   - Level 1: `build-your-ai-brain`
   - Levels 2 to 4: follow the guide step by step with them.
3. **Make your own.** Offer the guide's task, or a quick win from `quick-wins/Quick wins.md` for this level. Do it with them now.
4. **Check.** Go through the tick list. Test each item for real (ask a question, open the page, look at the draft). Tick only what works.
5. When every box is ticked: "Level <n> works. Want to save a copy now?" If they say yes and GitHub is set up, save a copy with a short plain note of what changed. If GitHub isn't set up yet (Level 3), say it gets set up then.

## Pace
- One level per sitting is normal. Never rush them up a level with empty ticks.
- If they stop: "Say 'what's next' any time and I'll pick up here."

## Rules
Follow `CLAUDE.md` in this folder, especially: drafts not sends, no secrets in files, ask before anything outside this folder.
