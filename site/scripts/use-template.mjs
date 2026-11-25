// Usage: npm run template landscaping
// Copies templates/<name>/page.astro to src/pages/index.astro and, if src/content/site.json
// doesn't exist yet, the template's example content (every line marked EXAMPLE).
import { cpSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const name = process.argv[2];
const list = readdirSync(join(root, 'templates'));
if (!name || !list.includes(name)) { console.log(`Pick a template: ${list.join(', ')}`); process.exit(1); }
const t = join(root, 'templates', name);
cpSync(join(t, 'page.astro'), join(root, 'src', 'pages', 'index.astro'));
const content = join(root, 'src', 'content', 'site.json');
if (!existsSync(content)) cpSync(join(t, 'site.example.json'), content);
console.log(`template: ${name} in place. Fill src/content/site.json from the brain.`);
