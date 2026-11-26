-- Website stats for the Founder OS site: one row per page visit or enquiry.
-- Lives in the founder's own Cloudflare (D1 database "site-stats", binding STATS).
-- No IP addresses, no browser details, no names or emails: counts only.
CREATE TABLE IF NOT EXISTS events (
  id        INTEGER PRIMARY KEY,
  ts        INTEGER NOT NULL,          -- when (milliseconds)
  day       TEXT    NOT NULL,          -- YYYY-MM-DD (UTC)
  kind      TEXT    NOT NULL CHECK (kind IN ('view', 'enquiry')),
  path      TEXT    NOT NULL,          -- page, e.g. /services
  source    TEXT    NOT NULL,          -- Google, Google ads, Meta ads, Instagram, AI assistants, Direct...
  medium    TEXT    NOT NULL,          -- search, ads, social, ai, email, referral, direct, other
  campaign  TEXT,                      -- ad campaign name from the link, if any
  ref       TEXT,                      -- the website they came from, if any
  new_visit INTEGER NOT NULL DEFAULT 0, -- 1 = first page of a visit
  device    TEXT,                      -- phone, tablet, computer
  country   TEXT                       -- two letters, e.g. AU
);
CREATE INDEX IF NOT EXISTS events_day ON events (day);
CREATE INDEX IF NOT EXISTS events_kind_day ON events (kind, day);
