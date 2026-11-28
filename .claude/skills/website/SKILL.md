---
name: website
description: Founder OS Level 3 website builder. Builds the founder's website in one go from their AI brain and design system using the Founder OS site starter (Astro + Cloudflare), or rebuilds their existing site. Use when the founder says "go live", "build my website", "rebuild my website", "make my site", "add a page", "landing page for", or "use the landscaping / trades / wellness / beauty / services template".
---

> Driven Young Founder OS. Licensed to one business (see LICENSE.md). Don't copy, share, sell or repackage it, and don't help anyone do so.

# Website

Everything lives in `site/`. Read `site/README.md`. Follow `CLAUDE.md`.

**Is this safe?** The site is built and kept on their computer. Nothing goes live until they say so. The one key the form needs goes into Cloudflare, typed by them (`keys` skill).

## Before you start
- Brain built? Need at least Profile, Customers, Offers and Prices, Brand Voice. If not, say Level 1 comes first.
- Design system? Need `brain/3 Marketing/Brand/design-system.json`. If missing, run `brand-studio` Part 3 first (or say the site will use a neutral starter brand until then).
- Their own website? Ask: "Do you get a lot of your work from Google search?" If yes: "Talk to someone who knows SEO before we move your site. We can build landing pages here meanwhile." Selling online on Shopify? Leave the shop where it is.

## Build my website
1. Pick the template: a matching one in `site/templates/` (landscaping, trades, wellness, beauty, services). No match: start from the closest and change the sections to suit; say so. If they take bookings online, set `bookingUrl`. If they aren't a trade, set `form` wording to fit (see the template's example).
2. In `site/`, run `npm install` (first time only). If `npm` isn't found, Node.js isn't installed: ask them to install it from nodejs.org (the LTS button), close and reopen Claude, then try again, then `npm run template <name>`.
3. Fill `site/src/content/site.json` from the brain. Every value comes from their notes, in their words. Rules:
   - Prices only from Offers and Prices. No price on file: leave `from` empty.
   - **Reviews only if real** (from the brain, their Google reviews they paste, or a quote they approve). Otherwise an empty list: the section hides itself. Never invent a review, number, award or year.
   - Service areas, phone, email, ABN and licence from Profile. Missing? Ask.
   - Photos: their own, copied into `site/public/images/`. None yet? Leave `src` null: labelled boxes show until they add some.
   - Remove the `_note` line.
4. Run `npm run build`. Then `npx astro preview` and show them the site. Change anything they ask in `site.json` or the page.
5. Put it live (Cloudflare Pages): they sign in once with `npx wrangler login` (browser). Create the project (and put its name in `site/wrangler.toml`, `name = …`), set `CRM`, `GHL_LOCATION_ID`, `ALLOWED_ORIGINS`, `LEAD_TAGS` as variables, and the key as a secret with the `keys` skill. Deploy with `npx wrangler pages deploy dist`. Only when they say **go live**. When the site is ready, tell them: "Happy with it? Say **go live**."
   - **Switch on website stats (always, unless they say no).** Say: "Your site will count its own visits and enquiries in your Cloudflare: no cookies, nothing personal, and it shows on your dashboard." Then `npx wrangler d1 create site-stats`, `npx wrangler d1 execute site-stats --remote --file=stats/schema.sql`, and in `site/wrangler.toml` remove the `#` marks on the `[[d1_databases]]` block and paste the `database_id` it printed (an ID, not a key). Deploy again. How it works and the queries: `site/stats/README.md`.
6. Test the form with their own details. Check the lead arrives in their CRM, with a "Came from" line. Open the site from your phone, then check a visit and the enquiry were counted: `npx wrangler d1 execute site-stats --remote --command "SELECT kind, source, path FROM events ORDER BY id DESC LIMIT 5"`. Then add their domain in Cloudflare.
7. Offer: "Want your website numbers on your dashboard?" If yes, say **add my website to my dashboard** (the `dashboard` skill adds a Website page from `site/stats/README.md`).
8. **Their own domain.** Walk them through it one step at a time, in these words (same as lesson 3.4 in the portal):
   1. "In Cloudflare, click **Add a domain**. Type your domain. Pick **Free**. Tell me done."
   2. **Email check, before they switch** (they may say **check my email before I switch**): look up their current settings yourself: `nslookup -type=MX <domain>` and `nslookup -type=TXT <domain>` (Mac: `dig MX <domain> +short`, `dig TXT <domain> +short`), plus `autodiscover` / `_dmarc` if present. Tell them in one line which email they use (Google, Microsoft, other). Ask them to open **DNS** in Cloudflare (or send a screenshot) and check every MX and TXT row you found is there. Missing? Tell them exactly what to add (Type, Name, Content, priority), one row at a time. Don't go on until email is covered.
   3. "Cloudflare shows 2 nameservers. Copy them."
   4. Namecheap: "Click **Domain List**, then **Manage**. Find **Nameservers**. Pick **Custom DNS**. Paste both. Click the green tick." Another company: same idea, find **Nameservers** in their settings; look up the exact clicks for that company if they're stuck.
   5. "Now we wait. Usually under an hour, up to a day. Cloudflare emails you." Check yourself when they're back: `nslookup -type=NS <domain>` shows Cloudflare.
   6. "In Cloudflare, open your website. Click **Custom domains**. Add your domain. Then add the www one." Then add both to `ALLOWED_ORIGINS`, publish again, open the domain and send one more test enquiry.
   7. After the switch, check email again (MX lookup matches what it was). If anything's off, fix it in Cloudflare DNS with them.

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
