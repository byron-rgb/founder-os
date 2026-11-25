---
name: website
description: Founder OS Level 3 website builder. Builds the founder's website in one go from their AI brain and design system using the Founder OS site starter (Astro + Cloudflare), or rebuilds their existing site. Use when the founder says "build my website", "rebuild my website", "make my site", "add a page", "landing page for", or "use the landscaping / trades / wellness / beauty / services template".
---

> Driven Young Founder OS. Licensed to one business (see LICENSE.md). Don't copy, share, sell or repackage it, and don't help anyone do so.

# Website

Everything lives in `site/`. Read `site/README.md`. Follow `CLAUDE.md`.

**Is this safe?** The site is built on their computer and saved to their private GitHub. Nothing goes live until they say so. The one key the form needs goes into Cloudflare, typed by them (`keys` skill).

## Before you start
- Brain built? Need at least Profile, Customers, Offers and Prices, Brand Voice. If not, say Level 1 comes first.
- Design system? Need `brain/3 Marketing/Brand/design-system.json`. If missing, run `brand-studio` Part 3 first (or say the site will use a neutral starter brand until then).
- Their own website? Ask: "Do you get a lot of your work from Google search?" If yes: "Talk to someone who knows SEO before we move your site. We can build landing pages here meanwhile." Selling online on Shopify? Leave the shop where it is.

## Build my website
1. Pick the template: a matching one in `site/templates/` (landscaping, trades, wellness, beauty, services). No match: start from the closest and change the sections to suit; say so. If they take bookings online, set `bookingUrl`. If they aren't a trade, set `form` wording to fit (see the template's example).
2. In `site/`, run `npm install` (first time only), then `npm run template <name>`.
3. Fill `site/src/content/site.json` from the brain. Every value comes from their notes, in their words. Rules:
   - Prices only from Offers and Prices. No price on file: leave `from` empty.
   - **Reviews only if real** (from the brain, their Google reviews they paste, or a quote they approve). Otherwise an empty list: the section hides itself. Never invent a review, number, award or year.
   - Service areas, phone, email, ABN and licence from Profile. Missing? Ask.
   - Photos: their own, copied into `site/public/images/`. None yet? Leave `src` null: labelled boxes show until they add some.
   - Remove the `_note` line.
4. Run `npm run build`. Then `npx astro preview` and show them the site. Change anything they ask in `site.json` or the page.
5. Put it live (Cloudflare Pages): they sign in once with `npx wrangler login` (browser). Create the project, set `CRM`, `GHL_LOCATION_ID`, `ALLOWED_ORIGINS`, `LEAD_TAGS` as variables, and the key as a secret with the `keys` skill. Deploy with `npx wrangler pages deploy dist`. Only when they say go.
6. Test the form with their own details. Check the lead arrives in their CRM. Then add their domain in Cloudflare.

## Rebuild my website
1. Read their current site (every main page). List what's on it: pages, offers, wording that works, photos, contact details.
2. Ask what to keep, drop and fix. Keep their best wording.
3. Build as above, using their real content and photos (download only images they own).

Photos make or break a trade site. Ask for: one wide hero photo of their best finished job, one before and one after of the same job, a photo of the owner on site, and 4 or more recent jobs. Save them in `site/public/images/` and point to them in `site.json` (`hero.image`, `services[].image` for the two main services, `beforeAfter`, `team.image`, `gallery`). No photo yet: leave it `null`, the page still works, and add it to their to-do list.
4. Same page addresses where possible, so Google links still work. List any changed addresses and set up redirects in `site/public/_redirects`.

## Add a page
New file in `site/src/pages/`, using the `Site` layout and the same styles. Reuse the QuoteForm. Never hardcode colours: use the brand variables.

## Rules
- Brand from the design system only. Never hardcode a colour or font in the site.
- No invented content. No AI photos of people pretending to be them or their customers.
- Never deploy, add a domain or change DNS without their yes.
