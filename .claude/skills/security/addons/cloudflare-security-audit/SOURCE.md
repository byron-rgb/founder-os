# Source of this folder

- **What:** Cloudflare's `security-audit` skill, bundled unchanged for the Founder OS security module's code check add-on.
- **From:** https://github.com/cloudflare/security-audit-skill, folder `skills/security-audit`, commit `c1c8a8c` (2026-09-14).
- **Licence:** MIT, Copyright (c) 2025-2026 Cloudflare, Inc. See `LICENSE` in this folder. Keep it with the files.
- **Checked:** 2026-10-09, every file's SHA-256 matched that commit. Nothing edited.
- **How we use it:** only through `references/checks/code-audit.md`, and only when the owner has code and asks for the code check. It is not loaded as a skill of its own.
- **Scanner note:** SkillSpector flags this folder, because it is a security guide that describes attacks so they can be found. The flags were read and are the guide's own teaching text, not instructions to an AI. See `.skillspector-baseline.yaml` at the top of the security skill.
- **Updating:** copy the new `skills/security-audit` folder from the official repo, record the new commit and date here, re-run SkillSpector, and read any new findings before accepting them.
