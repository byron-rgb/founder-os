# Your website (Level 3)

The Founder OS site starter: plain Astro (free, open source), live on Cloudflare, styled from your design system, with a quote form that sends leads to your CRM.

## Say this to Claude
- **build my website**: picks the template that fits, fills it from your brain, puts your brand on it
- **rebuild my website from <your address>**: reads your current site, keeps what works, rebuilds it here
- **add a page for <offer or event>**

## How it fits together
- `templates/`: ready-made starting points: `landscaping`, `trades` (electricians, plumbers, builders, painters), `wellness` (clinics, physio, PT, studios), `beauty` (salons, barbers, skin, nails), `services` (agencies, consultants, accountants, coaches). Each has a `site.example.json` showing every field. Booking businesses can set `bookingUrl` so every Book button goes to their booking system, and `form` changes the form's wording.
- `src/content/site.json`: your words (filled from your brain). `npm run template <name>` starts it.
- `scripts/brand.mjs`: reads `brain/3 Marketing/Brand/design-system.json` and makes your colours, fonts and sizes. Change your brand there, never in the site.
- `functions/api/lead.js`: the form. Sends leads to GoHighLevel, or any other CRM through a webhook. Its settings live in Cloudflare, never in files.

## Keys
The form needs a GoHighLevel key (or a webhook link for another CRM). Say **help me with a key**. You put it in Cloudflare yourself; it never goes in the chat or these files.

## Damn Good Funnels
Using GoHighLevel and want a ready-made kit with more page designs? Damn Good Funnels (damngoodfunnels.com) is free for your own business: download it yourself from its author's GitHub. It isn't included here, and its licence doesn't allow it to be shared.

---
Driven Young Founder OS · licensed to one business · see LICENSE.md
