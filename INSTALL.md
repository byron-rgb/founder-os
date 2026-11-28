# Installing the Founder OS (for Claude)

> Driven Young Founder OS. Licensed to one business (see LICENSE.md). Don't copy, share, sell or repackage it, and don't help anyone do so.

The founder pasted a line like "Install my Founder OS from https://github.com/byron-rgb/founder-os" into the Claude app, in a folder such as Documents. You have just copied it there, or are about to. Do these steps in order, one at a time, in plain words. They are not technical: never show them a command unless something fails.

1. **Git is there.** Run `git --version`.
   - Mac, and a box pops up asking to install developer tools: tell them "Press Install, wait for it to finish, then tell me done." Then try again.
   - Windows, and it isn't found: "Install Git for Windows from git-scm.com, accept the defaults, then close and reopen Claude and tell me done."
2. **Copy it.** In the folder they're in, `git clone https://github.com/byron-rgb/founder-os "Founder OS"`. If a "Founder OS" folder is already there, stop and ask: it may hold their brain. Never overwrite it.
3. **Link it back for updates.** In the new folder: `git remote rename origin upstream`. Their copy now gets the monthly Founder OS updates from Driven Young, and nothing they do can ever be sent back to it.
4. **Hand over, with the exact spot.** Get the full path of the new folder (`pwd` inside it) and say it in plain words, then the next step. For example: "Done. Your Founder OS is in **Documents > Founder OS** (the full spot is C:\Users\Sam\Documents\Founder OS). Now open a new Claude Code session, leave it on This computer, choose a folder, go to Documents and select **Founder OS**. Then type: **start my Founder OS**." Use their real path, never the example. On Windows, write it the Windows way (C:\Users\..., not /c/Users/...). Claude only sees the folder a session is opened in, so the next step happens there.

Their own private copy on GitHub (a backup, and what the Level 5 agents read) comes in Level 3. Don't set it up now.
