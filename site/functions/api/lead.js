// Cloudflare Pages Function: POST /api/lead
// Takes the quote form and sends the lead to the founder's CRM.
// Settings live in Cloudflare (never in this file):
//   CRM              "ghl" (GoHighLevel) or "webhook" (any other CRM, Zapier, Make)
//   GHL_API_KEY      secret: GoHighLevel Private Integration token (contacts.write)
//   GHL_LOCATION_ID  GoHighLevel location ID
//   WEBHOOK_URL      secret: where to send leads when CRM is "webhook"
//   ALLOWED_ORIGINS  comma-separated, e.g. https://yourdomain.com.au,https://www.yourdomain.com.au
//   LEAD_TAGS        optional, comma-separated tags, e.g. website,quote
// Protections: same-site only, 10 KB limit, honeypot, field length limits, no secrets in replies.

const MAX_BYTES = 10_000;
const clean = (v, n = 200) => String(v ?? '').replace(/[\u0000-\u001f<>]/g, ' ').trim().slice(0, n);

export async function onRequestPost({ request, env }) {
  const origin = request.headers.get('origin') || '';
  const allowed = (env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  const sameHost = origin && new URL(request.url).origin === origin;
  if (!sameHost && !allowed.includes(origin)) return json({ ok: false, error: 'Not allowed' }, 403);

  const len = Number(request.headers.get('content-length') || 0);
  if (len > MAX_BYTES) return json({ ok: false, error: 'Too large' }, 413);
  let body;
  try { body = JSON.parse((await request.text()).slice(0, MAX_BYTES)); } catch { return json({ ok: false, error: 'Bad request' }, 400); }

  if (body.company_website) return json({ ok: true }); // honeypot: pretend success for bots

  const lead = {
    name: clean(body.name, 120), phone: clean(body.phone, 40), email: clean(body.email, 160),
    suburb: clean(body.suburb, 80), job: clean(body.job, 80), details: clean(body.details, 2000),
  };
  if (!lead.name || !(lead.email || lead.phone)) return json({ ok: false, error: 'Name and a phone or email are needed' }, 422);
  if (lead.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(lead.email)) return json({ ok: false, error: 'Check the email' }, 422);

  const tags = (env.LEAD_TAGS || 'website').split(',').map((t) => t.trim()).filter(Boolean);
  try {
    if ((env.CRM || 'ghl') === 'ghl') await toGhl(lead, tags, env);
    else await toWebhook(lead, tags, env);
    return json({ ok: true });
  } catch (e) {
    console.error('lead: CRM send failed', e.message); // shows in Cloudflare logs, not to the visitor
    return json({ ok: false, error: 'Could not send right now' }, 502);
  }
}

// Never overwrites an existing contact: the form isn't signed in, so anyone could type a
// customer's email. Existing contact -> add tags + an "unverified" note only.
// New contact -> create it.
async function toGhl(lead, tags, env) {
  if (!env.GHL_API_KEY || !env.GHL_LOCATION_ID) throw new Error('GHL settings missing');
  const api = 'https://services.leadconnectorhq.com';
  const headers = { Authorization: `Bearer ${env.GHL_API_KEY}`, Version: '2021-07-28', 'Content-Type': 'application/json', Accept: 'application/json' };
  const details = [lead.job && `Job: ${lead.job}`, lead.suburb && `Suburb: ${lead.suburb}`, lead.details && `Details: ${lead.details}`].filter(Boolean);

  let id = null;
  if (lead.email) {
    const r = await fetch(`${api}/contacts/search/duplicate?locationId=${encodeURIComponent(env.GHL_LOCATION_ID)}&email=${encodeURIComponent(lead.email)}`, { headers });
    if (r.ok) id = (await r.json().catch(() => ({})))?.contact?.id || null;
  }

  if (id) {
    await fetch(`${api}/contacts/${id}/tags`, { method: 'POST', headers, body: JSON.stringify({ tags }) });
    const note = ['Website quote request (unverified: sent from the public form, contact details not changed)',
      `Name given: ${lead.name}`, lead.phone && `Phone given: ${lead.phone}`, ...details].filter(Boolean).join('\n');
    const r = await fetch(`${api}/contacts/${id}/notes`, { method: 'POST', headers, body: JSON.stringify({ body: note }) });
    if (!r.ok) throw new Error(`GHL note ${r.status}`);
    return;
  }

  const [firstName, ...rest] = lead.name.split(' ');
  const res = await fetch(`${api}/contacts/`, {
    method: 'POST', headers,
    body: JSON.stringify({
      locationId: env.GHL_LOCATION_ID, firstName, lastName: rest.join(' ') || undefined,
      email: lead.email || undefined, phone: lead.phone || undefined, city: lead.suburb || undefined,
      tags, source: 'Website quote form',
    }),
  });
  if (!res.ok) throw new Error(`GHL create ${res.status}`);
  const newId = (await res.json().catch(() => ({})))?.contact?.id;
  if (newId && details.length) {
    await fetch(`${api}/contacts/${newId}/notes`, { method: 'POST', headers, body: JSON.stringify({ body: `Website quote request\n${details.join('\n')}` }) }).catch(() => {});
  }
}

async function toWebhook(lead, tags, env) {
  if (!env.WEBHOOK_URL) throw new Error('WEBHOOK_URL missing');
  const res = await fetch(env.WEBHOOK_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...lead, tags, source: 'Website quote form', at: new Date().toISOString() }) });
  if (!res.ok) throw new Error(`Webhook ${res.status}`);
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
}
