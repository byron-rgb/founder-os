# Installing the security check

For Byron, Pieter, or whoever runs the setup call. The owner doesn't need to read this.

## 1. The skill

The security check comes inside the Founder OS folder (`.claude/skills/security`). It's there as soon as they copy the Founder OS. Updates arrive with "pull the latest Founder OS".

Nothing to install separately. Open the Founder OS folder in Claude (Code tab or Terminal).

Check it worked: say "security check". Claude should start with the stack interview.

## 2. What the owner's computer needs

| Need | Why | Check |
|---|---|---|
| Python 3.10+ | Runs the helper scripts (standard library only, nothing to install) | `python3 --version` |
| Internet | Public lookups (DNS, Mozilla Observatory, HIBP, RDAP) | |
| `dig` | DNS lookups. Built into Mac and Linux. If missing, the scripts use DNS-over-HTTPS instead | `dig -v` |

No admin rights, no Homebrew, no system-wide installs. Everything optional goes in one private folder: `~/FounderOS-security-tools/`.

On Windows: Python from python.org or the Microsoft Store. `dig` isn't there, so the DNS-over-HTTPS fallback is used automatically.

## 3. Optional tools (install only the ones their stack needs)

All open licences, all downloaded from the official source at run time, pinned to a version. None are bundled in the plugin except the Cloudflare skill (see CREDITS.md).

| Tool | For | Install (into the private folder) | Pinned |
|---|---|---|---|
| checkdmarc (Apache-2.0) | Deeper email checks (optional) | `python3 -m venv ~/FounderOS-security-tools/venv && ~/FounderOS-security-tools/venv/bin/pip install checkdmarc==6.0.3` | 6.0.3 |
| gitleaks (MIT) | Leaked keys | `python3 -I scripts/fetch_tool.py gitleaks` (checks the SHA-256 fingerprint first) | 8.30.1 |
| OSV-Scanner (Apache-2.0) | Code building blocks | `python3 -I scripts/fetch_tool.py osv-scanner` | 2.6.0 |
| SkillSpector (Apache-2.0) | AI tool scans | `python3 -m venv ~/FounderOS-security-tools/skillspector-env && ~/FounderOS-security-tools/skillspector-env/bin/pip install "git+https://github.com/NVIDIA/skillspector.git@3527006"` | 2.12.0 (commit 3527006) |
| ScubaGoggles (CC0) | Google Workspace settings | See `checks/workspace-settings.md`, part A | latest release (v1.0.1 on 2026-10-09) |
| GAM7 (Apache-2.0) | Google accounts, apps, files | `python3 -I scripts/fetch_tool.py gam` (macOS), or the release page for other systems. Then `checks/workspace-settings.md`, part B | 7.48.24 |
| Maester (MIT) | Microsoft 365 (untested) | See `checks/microsoft-365.md` | 2.3.0 |

`fetch_tool.py` refuses to unpack anything whose fingerprint doesn't match the one recorded from the maker's published checksums. To update a pin: take the new version and SHA-256 from the official release page only, test on a sample client folder, then commit.

Tested on 2026-10-09 (Mac, Apple chip): checkdmarc 6.0.3, gitleaks 8.30.1 and OSV-Scanner 2.6.0 installed this way into a sandbox folder and ran on a made-up client (Sam's Plumbing). ScubaGoggles, GAM and Maester are documented from their official guides but not yet run on a real client.

## 4. Connectors (in Claude, owner's own account)

| Connector | For | Access |
|---|---|---|
| Google Drive | File sharing check | Owner signs in. Only read tools are used |
| Calendar (optional) | The weekly reminder backup | Only with the owner's yes, only their own calendar |

## 5. Removing it

- Skill: delete the `.claude/skills/security` folder from the Founder OS.
- Tools: delete `~/FounderOS-security-tools/`. For Google, also delete the "Security check" Cloud project (and GAM's project). For Microsoft, remove the Graph consent (see `checks/microsoft-365.md`).
- The owner's `Security/` notes stay in their brain folder. They're theirs.
