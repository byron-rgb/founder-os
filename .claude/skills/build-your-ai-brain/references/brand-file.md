# Brand: the design file

Goal: one folder, `3 Marketing/Brand/`, that holds everything about how the business looks. Any AI building a page, post, PDF, slide or dashboard reads `Brand Guidelines.md` first and uses the files beside it. Nothing about the look lives anywhere else.

About 10 minutes. Most owners have bits of a brand scattered around: a Canva kit, a designer's PDF, a logo in their email, colours on the website. The job is to move it all in here.

## 1. Gather what exists (move it over)
Ask one at a time:
- "Got a brand guide or files from a designer? Drop them in `Drop files here`."
- "Do you use Canva? If you have a Brand Kit there, download your logos and note your colours and fonts. I'll walk you through it." (Canva: Brand, Brand Kit. Logos download from there; colours show their hex codes.)
- "Where's your logo? I need the actual file. A PNG with a see-through background is best. Got a version for dark backgrounds too?"
- If they have a website: read it for colours (hex codes) and fonts, and say what you found so they can confirm.

File logos in `Logos/`, font files in `Fonts/` (only if they own them), brand photos in `Photos/`. Use clear names: `logo-main.png`, `logo-white.png`, `icon.png`.

## 2. Fill the gaps
Only ask what's still missing:
- Brand colours: main, background, text, accent. Hex codes if they have them.
- Fonts: headings and body. No idea? Suggest a free Google Fonts pair that suits them and mark `[CHECK]`.
- Feel in three words (e.g. "earthy, calm, premium").
- Photos: real or stock? People or places? Any they love or hate?
- Never do: anything the AI should never do visually (e.g. "no neon", "never stretch the logo").

No brand at all yet? Say: "No stress. We'll set a simple starting brand now, and you can change it any time." Propose 2 options (colours + fonts + feel) from their business and voice, let them pick, mark it "Starter brand".

## 3. Write `Brand Guidelines.md`
Frontmatter as in `brain-layout.md`, then these sections:
- **Feel**: three words and one line on the overall look.
- **Logo**: table of files (File · Use · Background), minimum size, never do.
- **Colours**: table (Name · Hex · Use). Include text-on-background pairs that are easy to read.
- **Fonts**: table (Role · Font · Weight · Where to get it). Sizes for headline, subheading, body, small.
- **Buttons and shapes**: button colour, text colour, corners (square or rounded), spacing feel (airy or tight).
- **Photos and graphics**: style, examples in `Photos/`, never do.
- **Never do**: their list.
- Links: [[Brand Voice]], [[Offers and Prices]], [[Customers]].

## 4. Make `Brand Board.html`
One simple page that shows the brand: logo, colour swatches with hex codes, the fonts in use, a sample headline, a sample button, two photos if they have them. Plain HTML in the Brand folder, logos linked from `Logos/`. Tell them: "Open Brand Board.html to see your brand on one page." Fix anything they don't like in the guidelines first, then remake the board.

## 5. Done
Set `status: done`. Say: "Your brand's in one place now. Every page and post I make will start from it."

Rules: never invent a logo or claim a font is theirs. Don't store font files they don't have a licence for (most Google Fonts are free). Keep their designer's exact values.
