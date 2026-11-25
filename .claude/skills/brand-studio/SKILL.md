---
name: brand-studio
description: Founder OS Brand Studio. Turns the founder's brand (brain/3 Marketing/Brand) into a design system, offers a brand refresh, then shows what it can do by making real slides, social graphics, a poster and a flyer on brand. Use when the founder says "brand studio", "refresh my brand", "make my design system", "show me what my brand can do", "make slides", "make a poster", "make a flyer", "make a social post", or "make a graphic".
---

# Brand Studio

The founder's brand lives in `brain/3 Marketing/Brand/`. This skill makes it powerful: one design system that everything Claude makes follows, an optional refresh, and a showcase that proves it.

Follow `CLAUDE.md` in the Founder OS. One step at a time. Plain words: say "your brand", "your design file", never "tokens" or "CSS".

**Is this safe?** Everything stays in their brand folder on their computer. Nothing is posted or printed for them. Their logo artwork is never redrawn or changed.

## Pick the job
- "Refresh my brand" → Part 2.
- "Make my design system" → Part 3.
- "Make slides / a poster / a flyer / a post" → check Part 1, then Part 4 for that one thing.
- "Brand studio" or "show me what my brand can do" → Parts 1 to 4 in order.

## Part 1. Check the brand folder
Read `Brand/Brand Guidelines.md`. If it's missing or thin (no colours, no fonts, no logo file), run `build-your-ai-brain/references/brand-file.md` first, then come back.

## Part 2. Refresh (optional, about 15 minutes)
Ask: "Want a quick brand refresh while we're here? I'll keep your logo and suggest small upgrades. You pick, or keep what you have."
If yes:
1. Review against these, one line each: text is easy to read on its background; one clear accent colour; no more than two fonts; a dark-background logo exists; the look matches who they sell to ([[Customers]]) and how they sound ([[Brand Voice]]).
2. Make two directions on one page, `Brand/Refresh options.html`: A "Tidy" (same feel, fixed problems) and B "Step up" (same logo, bolder colours and type). Each shows swatches, fonts, a sample headline, a button and a sample post.
3. They pick A, B, or keep. Copy the old guidelines to `Brand/Archive/Brand Guidelines YYYY-MM-DD.md` first, then update `Brand Guidelines.md` and remake `Brand Board.html`.
4. Logo needs real work? Say so, and suggest a designer. Never redraw it.

## Part 3. Design system
Turn the guidelines into a design system every page follows:
1. Write `Brand/design-system.json`: colours (name, hex, use), fonts (role, family, weight, where to get it), type sizes (headline, subhead, body, small), spacing (4 steps), corners (square or a radius), button style.
2. Write `Brand/Design System.html`: one page showing colours with hex codes and readable pairs, the type scale, buttons, a card, a form field, and the logo on light and dark. Fonts load from Google Fonts where they're free; otherwise a close free match, noted in the guidelines.
3. Add to `brain/CLAUDE.md` under hard rules: "Anything visual: read `3 Marketing/Brand/Brand Guidelines.md` and `design-system.json` first."
4. If their Claude can make artifacts with a **Design System** type, offer: "Want this as a design system inside Claude too, so every artifact you make uses it?" On yes, create it from these files. If not available, skip it without fuss: the files do the job.

## Part 4. Showcase (the fun part)
Say: "Let's see it work. I'll make four real things for your business, all on brand." Use their real offer, words and photos from the brain. Make each as an HTML file at the exact size, in `brain/Work/Brand Studio/`:
1. **Social post** (1080 x 1350) for their main offer, plus a **story** (1080 x 1920).
2. **Poster** (A3 portrait) or **flyer** (A5), whichever suits the business (a flyer for letterboxes, a poster for a studio wall).
3. **Five-slide deck** (16:9): who we are, the problem, the offer, how it works, next step. If their Claude has a **Slides** type, offer to make it there instead so they can present it.
4. One extra they pick: a quote cover page, an email header, a business card, a price list.

Then show them how to save each:
- Images: open the file, take a screenshot of the page (Cmd + Shift + 4, then Space, click the window), or ask Claude to save it as a PNG.
- Poster, flyer, deck: open in the browser, **File**, **Print**, **Save as PDF**.

## Rules
- Real content only. No made-up reviews, numbers, awards or clients. Missing a fact? Ask.
- Their own photos from `Brand/Photos/` only. No AI images of real people pretending to be them or their customers.
- Never post, print, send or order anything. They do that.
- Log each thing made in `brain/AI Log.md`.
