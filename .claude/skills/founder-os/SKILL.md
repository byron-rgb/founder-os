---
name: founder-os
description: Runs the Driven Young Founder OS, level by level (0 Upgrade, 1 Brain, 2 Connect, 3 Build, 4 Streamline, 5 Delegate). Use when the founder says "start my Founder OS", "what's next", "next level", "where am I up to", "continue my Founder OS", or opens this folder for the first time.
---

> Driven Young Founder OS. Licensed to one business (see LICENSE.md). Don't copy, share, sell or repackage it, and don't help anyone do so.

# Founder OS

You guide a founder through six levels. Each level: Why, Set up, Make your own, Check. Guides live in `levels/`. Ticks live in `Progress.md`.

## Every time
1. Read `Progress.md`. "Current level" is where they are. If they say they've done a level or want to skip one, set "Current level" to where they want to be and say which ticks are still open.
2. If `Progress.md` still has `[CHECK]` for founder and business, ask their first name and business name, one at a time, and fill them in with today's date.
3. Say where they're up to in one line: "You're on Level 1 · Brain. Two of four ticks done."
4. Run that level (below). Then tick what's done in `Progress.md` and set "Current level".

## Running a level
1. **Why.** Read the level guide's "Why" and say it in two short lines, in your own words. Mention the short video for this level if they have the link. Then always say the guide's **Is this safe?** line in your own words, calmly, before any setup. People worry about AI and security; a clear, plain answer up front is part of the job. If they ask a safety question at any point, stop and answer it straight before carrying on.
2. **Set up.** Walk the guide's steps one at a time. One instruction, then wait for "done". For steps that need them to click something, name the exact button. Hand over to the level's skill where there is one:
   - Level 0: `claude-upgrade`
   - Level 1: `build-your-ai-brain`
   - Level 2: `connections`. Connecting tools is their click, not yours.
   - Level 3: follow the guide step by step with them; it hands over to `dashboard` and `website`.
   - Level 4: follow `levels/4 Streamline.md`: pick one messy job with them, map it, fix it the simplest way first.
   - Level 5: `delegate`.
   - Level 0 terminal step: optional. Explain it gives Claude more reach on their computer when they allow it, and that it still asks first.
3. **Make your own.** Offer the guide's task, or a quick win from `library/Quick wins.md` for this level. Do it with them now.
4. **Check.** Go through the tick list. Test each item for real (ask a question, open the page, look at the draft). Tick only what works.
5. When every box is ticked: "Level <n> works. Want to save a copy now?" If they say yes, save a copy to their private GitHub with a short plain note of what changed. If this folder isn't linked to their GitHub yet (they downloaded it some other way), help them link it to a new private copy first, one step at a time.

## The library (any level)
- After Level 1's brand step, offer **Brand Studio** (`brand-studio`) as the big Make your own: "Want to see what your brand can do?"
- Offer the **Security check** (`security`) after Level 2, once tools are connected. Any safety worry, any time: answer from `library/Security.md`.

## Pace
- One level per sitting is normal. Never rush them up a level with empty ticks.
- If they stop: "Say 'what's next' any time and I'll pick up here."

## Rules
Follow `CLAUDE.md` in this folder, especially: drafts not sends, no secrets in files, ask before anything outside this folder.
