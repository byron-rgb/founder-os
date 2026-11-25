---
name: claude-upgrade
description: Level 0 of the Founder OS. Installs the Claude Upgrade pack, a hand-picked set of free, open-source skills, each from its own public source, and explains each in one line. Use when the founder says "install my Claude Upgrade", "upgrade my Claude", "Level 0", or "what skills should I have".
---

# Claude Upgrade

Install these skills for the founder so every later level is sharper. Each one comes from its own public GitHub page at a checked version. Driven Young picks them; we never copy or re-share anyone's files.

## Before you start
- Say: "I'll install about ten free skills that make me plan better, write like a person and build things that look designed. Each comes from its author's own page. OK to go?" Wait for yes.
- Install into the founder's own skills folder: `~/.claude/skills/<name>/`. If a skill with that name is already there, skip it and say so.

## How to install one
1. Download the source at the pinned version into a new empty temporary folder (`git clone`, then `git checkout <version>`).
2. Copy only the skill's folder (the folder holding its `SKILL.md`, at the path below) to `~/.claude/skills/<name>/`. Never install plugin hooks, background services or anything that runs on every message.
3. Write `SOURCE.txt` in that folder: source link, version, today's date, "installed by Founder OS Claude Upgrade".
4. Delete the temporary folder.
5. Tell them in one line what it does for them (the "For you" column).

If a download fails or the path isn't there, skip that skill, say so plainly, and carry on.

## The pack

| Name | Source | Version | Path | For you |
| --- | --- | --- | --- | --- |
| grilling | github.com/mattpocock/skills | d81f3a1 | skills/productivity/grilling | Asks sharp questions until a plan is thought through |
| grill-me | github.com/mattpocock/skills | d81f3a1 | skills/productivity/grill-me | Same, started by saying "grill me" |
| humanizer | github.com/blader/humanizer | 225a6f3 | (top folder) | Takes the AI tone out of your writing |
| find-skills | github.com/vercel-labs/skills | 3694740 | skills/find-skills | Finds a skill when you need one |
| prompt-master | github.com/nidhinjs/prompt-master | 2bd9251 | (top folder) | Writes prompts for other AI apps (images, video) |
| design-taste-frontend | github.com/leonxlnx/taste-skill | ce26fc2 | skills/taste-skill | Pages that look designed, not generated |
| impeccable | github.com/pbakaus/impeccable | 508d7e8 | .claude/skills/impeccable | Polishes design and layout |
| diagram-design | github.com/cathrynlavery/diagram-design | f903933 | (top folder) | Turns a process into a clean diagram |
| verification-before-completion | github.com/obra/superpowers | 8ca22db | skills/verification-before-completion | I prove things work before I say "done" |
| content-principles | github.com/aiwithremy/content-principles | latest | (top folder) | What makes short videos and posts hold attention |
| watch (optional) | github.com/bradautomates/claude-video | 03ceb42 | skills/watch | I can watch a video link. Needs extra Mac tools; skip unless they want it |

## Official plugins (they click, you guide)
These come from Claude's own plugin store. Walk them through it: Claude settings, **Plugins** (or type `/plugin`), find each, **Install**.
- **frontend-design** (from claude-plugins-official): better pages and dashboards
- **security-guidance** (from claude-plugins-official): warns about risky code
- **cloudflare** (from cloudflare/skills): needed in Level 3 to put things live

## One house rule to add
After installing grilling, add this line to `CLAUDE.md` in the Founder OS folder, under "How you talk":
`- When grilling, ask one question at a time with clickable options and your recommended answer first.`

## Finish
- Tick "Upgrade pack installed" in `Progress.md`.
- Say: "Done. Try it now: say **grill me on the one decision I keep putting off**." That's the Make your own step for Level 0.
