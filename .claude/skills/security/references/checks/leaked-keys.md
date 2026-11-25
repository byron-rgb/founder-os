# Check: Leaked keys in files

**Answers for the owner:** are passwords, API keys or other secrets sitting in files where they shouldn't be: shared folders, old exports, downloads, notes, code?

**Needs:** a folder on their computer (or a synced Google Drive or OneDrive folder) that the owner points to, and gitleaks (MIT) set up in a private folder.
**Feeds area:** 12 (Passwords and leaked keys).
**Time:** a few minutes per folder.

## Rules

- The owner picks the folders. Don't scan the whole computer or anyone else's files.
- **Always run gitleaks with `--redact`**, and summarise with `scripts/scan_summary.py`, which drops the secret even if a report wasn't redacted. Never print, copy, store or repeat a found secret. Not in the chat, the report, Issues or anywhere.
- Report the kind of key and where it is (file and line). That's enough for the owner to fix it.
- The raw gitleaks report is deleted as soon as it's summarised (`--delete-report`). It lives in the private tools folder, never in a shared temp folder or the brain folder.
- A found key is treated as **already leaked**. The fix is always to change (rotate) it at the provider first. Deleting the file alone isn't enough.

## Setup (once)

```
python3 -I scripts/fetch_tool.py gitleaks
```
This downloads the pinned gitleaks release from GitHub, checks its fingerprint against the maker's published checksum, and unpacks it into `~/FounderOS-security-tools/gitleaks-<version>/`. No admin rights, nothing installed system-wide. See `references/install.md`.

## How to run it

1. Ask: "Which folders hold business files, exports or notes? For example Downloads, Desktop, Documents, your Google Drive folder, a shared team folder, any code folder."
2. For each folder:
   ```
   mkdir -p ~/FounderOS-security-tools/reports
   ~/FounderOS-security-tools/gitleaks-8.30.1/gitleaks dir "FOLDER" --redact --no-banner --report-format json --report-path ~/FounderOS-security-tools/reports/gitleaks.json
   python3 -I scripts/scan_summary.py gitleaks ~/FounderOS-security-tools/reports/gitleaks.json --delete-report
   ```
3. For a code folder that's a git project, also scan its history (keys that were deleted but are still in old versions):
   ```
   ~/FounderOS-security-tools/gitleaks-8.30.1/gitleaks git "CODE_FOLDER" --redact --no-banner --report-format json --report-path ~/FounderOS-security-tools/reports/gitleaks-git.json
   python3 -I scripts/scan_summary.py gitleaks ~/FounderOS-security-tools/reports/gitleaks-git.json --delete-report
   ```
4. Big folders (a whole Drive) can take a while. Start with Downloads and Desktop, where exports pile up.

Without gitleaks: ask the owner to search their files for words like "password", "API key", "secret", "token" and the names of their tools, and open each hit together. Slower, but it finds the obvious ones (the "passwords" spreadsheet).

## How to read the result

- **Type** (for example `stripe-access-token`, `github-pat`, `aws-access-token`, `generic-api-key`): which service the key belongs to. `generic-api-key` is a guess and is often a false alarm. Open the file with the owner (they look, you don't copy) to confirm.
- **In history:** the key was deleted from the file but is still in the project's history. Still counts.
- **Test keys** (often `test` or `sandbox` in the name) are low. Live keys are high.

## Red, amber, green (area 12, keys part)

- **Green:** no keys found in the folders checked.
- **Amber:** only test keys, or keys that have already been changed.
- **Red:** a working live key, or a passwords document, in a file or a code project's history.

## Plain-English fixes

1. **Live key found (high).** "Change it at the service it belongs to, today." Each service has a page for this (Stripe: Developers, API keys, roll key; GitHub: Settings, Developer settings, tokens; Google Cloud: Credentials). Then update wherever the key is legitimately used, then delete the file.
2. **Passwords spreadsheet or note (high).** Move them into a password manager, change the important ones (email, bank, payments first), then delete the file and empty the bin.
3. **Key in code history (high).** Change the key. That's the real fix. Cleaning the history is optional and a developer job.
4. **Test key (low).** Fine to leave, but tidy up.
5. **Stop it happening again (medium, for code).** Keys in a `.env` file that's excluded from the code project, or the host's secret settings, plus a secret scan before each commit (gitleaks has one). See `code-audit.md`.

## Credit

gitleaks by Zachary Rice and contributors (MIT), downloaded at run time, not bundled.
