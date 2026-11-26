// Cloudflare Pages Function: POST /api/hit
// Counts one page visit in the founder's own Cloudflare database (D1, binding STATS).
// Sent by the small script in src/layouts/Site.astro. No cookies, no IP address, no personal details.
// Without the STATS database connected it does nothing, so the site works either way.
import { classify, isBot, record } from '../_lib/source.js';

export async function onRequestPost({ request, env }) {
  const done = new Response(null, { status: 204, headers: { 'cache-control': 'no-store' } });
  try {
    const origin = request.headers.get('origin') || '';
    if (origin && new URL(request.url).origin !== origin) return done;          // other sites can't add visits
    if (isBot(request.headers.get('user-agent') || '')) return done;
    if (Number(request.headers.get('content-length') || 0) > 2000) return done;
    const b = JSON.parse((await request.text()).slice(0, 2000) || '{}');
    if (typeof b.p !== 'string' || !b.p.startsWith('/')) return done;
    await record(env, request, 'view', b.p, classify(b, new URL(request.url).hostname), !!b.n);
  } catch (e) {
    console.error('hit: not saved', e.message);
  }
  return done; // never shows the visitor an error
}
