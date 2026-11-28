# Open the brain in Obsidian (for Claude)

> Driven Young Founder OS. Licensed to one business (see LICENSE.md). Don't copy, share, sell or repackage it, and don't help anyone do so.

Do this for them, so they never hunt for a folder. "The brain" is the brain folder's full path (in a Founder OS: `Founder OS/brain`).

1. **Installed?** Check yourself. Mac: `/Applications/Obsidian.app` or `~/Applications/Obsidian.app`. Windows: `%LOCALAPPDATA%\Programs\Obsidian\Obsidian.exe`. Not there? Ask once: "Obsidian shows your brain as notes and a map. It's free. Want me to install it?" On yes:
   - Windows: `winget install --id Obsidian.Obsidian -e --accept-source-agreements --accept-package-agreements`
   - Mac: `brew install --cask obsidian` if Homebrew is there. Otherwise download the latest `.dmg` from github.com/obsidianmd/obsidian-releases/releases/latest, attach it, copy Obsidian.app into Applications, detach it.
   - Install failed? Give them obsidian.md/download and wait for "done". They say no? Carry on without it; the brain works anyway.
2. Close Obsidian first, or it overwrites its list (Mac: `osascript -e 'quit app "Obsidian"'`; Windows: `taskkill /IM Obsidian.exe`; ignore "not running").
3. Its vault list: Mac `~/Library/Application Support/obsidian/obsidian.json`, Windows `%APPDATA%\obsidian\obsidian.json`. Missing? Create it as `{"vaults":{}}` (make the folder too).
4. Unless the brain's full path is already listed, add `"<16 random hex characters>": {"path": "<full path to Founder OS/brain>", "ts": <now in milliseconds>, "open": true}` inside `vaults`. Keep every other vault. Windows paths written the Windows way, with backslashes doubled in the file.
5. Open it: Mac `open "obsidian://open?path=<brain path, URL-encoded>"`; Windows `start "" "obsidian://open?path=<brain path, URL-encoded>"`. If that doesn't open the brain, start Obsidian normally; it opens the vault marked open.
6. Say: "Your brain is open in Obsidian. Click **Graph view** in the left sidebar to watch it grow." If it still won't open, fall back to: Open folder as vault, then the brain path you give them.
