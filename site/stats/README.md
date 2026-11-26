# Website stats

> Driven Young Founder OS. Licensed to one business (see LICENSE.md).

Every site built from the Founder OS counts its own visits and enquiries, into a small database in the founder's own Cloudflare. No cookies, no IP addresses, no names: counts only. Browsers that ask not to be tracked aren't counted.

## How it works
- `src/layouts/Site.astro`: a few lines on every page send the page and where the visitor came from to `/api/hit`.
- `functions/api/hit.js`: saves one row per visit. Bots and other sites are ignored.
- `functions/api/lead.js`: when the quote form sends, saves an `enquiry` row, and adds "Came from: Google ads, campaign …" to the lead in their CRM.
- `functions/_lib/source.js`: turns the clues into plain sources: Google, Google ads, Meta ads, Bing ads, Instagram, Facebook, LinkedIn, Other social, AI assistants, Email, Other search, Other websites, Direct.
- `stats/schema.sql`: the one table, `events`.
- Without the database connected, nothing breaks: visits just aren't counted.

## Switch it on (the website skill does this at go-live)
```
npx wrangler d1 create site-stats
npx wrangler d1 execute site-stats --remote --file=stats/schema.sql
```
Then in `wrangler.toml` remove the `#` marks on the `[[d1_databases]]` block and paste the `database_id` the first command printed (an ID, not a key). Deploy as usual.

## Read it (the dashboard's Website page)
The dashboard reads these through Cloudflare. Each query takes a start and end day (`YYYY-MM-DD`, UTC) as `?1` and `?2`.

**Headline numbers**
```sql
SELECT
  SUM(kind = 'view' AND new_visit = 1) AS visits,
  SUM(kind = 'view')                   AS page_views,
  SUM(kind = 'enquiry')                AS enquiries,
  ROUND(100.0 * SUM(kind = 'enquiry') / MAX(SUM(kind = 'view' AND new_visit = 1), 1), 1) AS enquiry_rate_pct
FROM events WHERE day BETWEEN ?1 AND ?2;
```

**Visits and enquiries by day**
```sql
SELECT day, SUM(kind = 'view' AND new_visit = 1) AS visits, SUM(kind = 'enquiry') AS enquiries
FROM events WHERE day BETWEEN ?1 AND ?2 GROUP BY day ORDER BY day;
```

**Where visitors come from** (and which sources turn into enquiries)
```sql
SELECT source, SUM(kind = 'view' AND new_visit = 1) AS visits, SUM(kind = 'enquiry') AS enquiries
FROM events WHERE day BETWEEN ?1 AND ?2 GROUP BY source ORDER BY visits DESC;
```

**Top pages**
```sql
SELECT path, COUNT(*) AS views FROM events
WHERE kind = 'view' AND day BETWEEN ?1 AND ?2 GROUP BY path ORDER BY views DESC LIMIT 10;
```

**Ads that brought enquiries**
```sql
SELECT source, COALESCE(campaign, '(no campaign name)') AS campaign,
       SUM(kind = 'view' AND new_visit = 1) AS visits, SUM(kind = 'enquiry') AS enquiries
FROM events WHERE medium = 'ads' AND day BETWEEN ?1 AND ?2
GROUP BY source, campaign ORDER BY enquiries DESC, visits DESC;
```

**Phone or computer**
```sql
SELECT device, SUM(new_visit) AS visits FROM events
WHERE kind = 'view' AND day BETWEEN ?1 AND ?2 GROUP BY device ORDER BY visits DESC;
```

**Tidy up** (optional, keeps two years)
```sql
DELETE FROM events WHERE day < date('now', '-730 days');
```

Not covered yet: the Google searches people found the site with (Google Search Console has no clean Claude connection yet).
