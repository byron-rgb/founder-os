// Founder OS site starter. Plain Astro, static output. Forms are handled by a
// Cloudflare Pages Function in functions/api/lead.js (no adapter needed).
import { defineConfig } from 'astro/config';
import { readFileSync, existsSync } from 'node:fs';

const file = new URL('./src/content/site.json', import.meta.url);
const site = existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : {};

export default defineConfig({
  site: site.url || 'https://example.com',
  output: 'static',
});
