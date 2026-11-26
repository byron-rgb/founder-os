// Where a visit came from, in plain words. Shared by /api/hit and /api/lead.
// Input: the raw clues the page sends (utm tags, ad click ids, the referring site).
// Output: { source, medium, campaign, ref }  e.g. { source: 'Google ads', medium: 'ads', ... }
const AI = ['chatgpt.com', 'chat.openai.com', 'perplexity.ai', 'claude.ai', 'gemini.google.com', 'copilot.microsoft.com', 'you.com', 'phind.com'];
const has = (host, list) => list.some((d) => host === d || host.endsWith('.' + d));
const cut = (v, n) => String(v ?? '').replace(/[\u0000-\u001f<>"]/g, '').trim().slice(0, n);

export function classify(raw = {}, ownHost = '') {
  const us = cut(raw.us, 60).toLowerCase(), um = cut(raw.um, 60).toLowerCase();
  const campaign = cut(raw.uc, 100) || null;
  let ref = cut(raw.r, 120).toLowerCase().replace(/^www\./, '');
  if (ref && ownHost && (ref === ownHost.replace(/^www\./, ''))) ref = '';
  const paid = raw.g || raw.f || /cpc|ppc|paid|ads?$/.test(um);
  const out = (source, medium) => ({ source, medium, campaign, ref: ref || null });

  if (raw.g || (paid && /google/.test(us))) return out('Google ads', 'ads');
  if (raw.f || (paid && /(facebook|fb|instagram|ig|meta)/.test(us))) return out('Meta ads', 'ads');
  if (paid && /(bing|microsoft)/.test(us)) return out('Bing ads', 'ads');
  if (paid) return out(us ? `${us} ads` : 'Other ads', 'ads');
  if (/^(email|newsletter)$/.test(um) || /(mailchimp|klaviyo|newsletter)/.test(us)) return out('Email', 'email');
  if (has(ref, AI) || /(chatgpt|perplexity|claude|gemini|copilot)/.test(us)) return out('AI assistants', 'ai');
  if (/(^|\.)google\./.test(ref) || us === 'google') return out('Google', 'search');
  if (has(ref, ['bing.com', 'duckduckgo.com', 'search.yahoo.com', 'ecosia.org'])) return out('Other search', 'search');
  if (has(ref, ['instagram.com']) || /^(ig|instagram)$/.test(us)) return out('Instagram', 'social');
  if (has(ref, ['facebook.com', 'fb.com', 'm.facebook.com', 'l.facebook.com']) || /^(fb|facebook)$/.test(us)) return out('Facebook', 'social');
  if (has(ref, ['linkedin.com', 'lnkd.in'])) return out('LinkedIn', 'social');
  if (has(ref, ['tiktok.com', 'youtube.com', 'youtu.be', 'x.com', 't.co', 'pinterest.com', 'reddit.com'])) return out('Other social', 'social');
  if (us) return out(us, 'other');
  if (ref) return out('Other websites', 'referral');
  return out('Direct', 'direct');
}

// Crawlers and previews are not visitors.
export const isBot = (ua = '') => /bot|crawl|spider|slurp|preview|headless|lighthouse|pingdom|uptime|monitor|curl|wget|python|axios|node-fetch/i.test(ua);
export const device = (ua = '') => (/mobile|iphone|android(?!.*tablet)/i.test(ua) ? 'phone' : /ipad|tablet/i.test(ua) ? 'tablet' : 'computer');

// Save one row in the founder's own Cloudflare database (binding STATS). No IP address,
// no browser details, no cookies: only what page, where from, roughly what device, which country.
export async function record(env, request, kind, path, src, isNew) {
  if (!env.STATS) return; // tracking not switched on yet
  const now = new Date();
  await env.STATS.prepare(
    'INSERT INTO events (ts, day, kind, path, source, medium, campaign, ref, new_visit, device, country) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
  ).bind(now.getTime(), now.toISOString().slice(0, 10), kind, cut(path, 200) || '/', src.source, src.medium, src.campaign, src.ref,
    isNew ? 1 : 0, device(request.headers.get('user-agent') || ''), cut(request.cf?.country, 2) || null).run();
}
