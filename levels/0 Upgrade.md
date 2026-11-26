# Level 0 · Upgrade

Claude, plus the skills that make it sharp.

## 1. Why
Out of the box Claude is good. With the right skills it plans with you, writes like a person and builds things that look designed. Every level after this uses them. About 20 minutes.

**Is this safe?** Yes. Claude only works inside the folder you give it, and it asks before it changes anything. Every skill here is free, public and checked by us first.

## 2. Set up

### Claude, two ways in
1. **Claude desktop app** (everyone). Install it from claude.ai/download and sign in on the **Pro** plan or higher. This is where you'll do most things.
2. **Claude in your Terminal** (optional, recommended). Same Claude, but it can also work with the rest of your computer when you let it: tidy files, run tools, set things up for you.
   - Open **Terminal** (press Cmd + Space, type Terminal, press Enter).
   - Paste this and press Enter:
     ```
     curl -fsSL https://claude.ai/install.sh | bash
     ```
   - Close Terminal, open a new one, type `claude` and press Enter. A browser page opens: sign in with the same Claude account.
   - **On Windows:** install **Git for Windows** first (free, git-scm.com, accept the defaults). Then open **PowerShell** (Start menu, type PowerShell) and paste `irm https://claude.ai/install.ps1 | iex` instead. The rest is the same.

### Pick Claude's folder
Claude can only see the folder you start it in. You choose how much it sees:
- **Your Founder OS folder** (recommended to start). Claude sees this folder and nothing else on your computer. In the app's **Code** tab, pick `Founder OS`. In Terminal: `cd "Founder OS"` then `claude`.
- **Your whole user folder** (later, if you want). Claude can help across all your files. It still asks before every change. This is how Byron runs his.

You can switch any time. Start small.

### Install the Upgrade
In your Founder OS folder, say: **install my Claude Upgrade**. Claude installs each skill from its own public source and tells you what each one does.

### What the permission boxes mean
Claude stops and asks before it runs a command or edits a file. You'll see the action and **Yes**, **Yes, and don't ask again**, or **No**. Read it, and press **No** whenever you're not sure. Nothing happens without a yes.

## 3. Make your own
Say: **grill me on the one decision I keep putting off.**

## 4. Check
- [ ] Claude app on Pro, signed in
- [ ] Claude in Terminal (optional)
- [ ] Claude's folder chosen
- [ ] Upgrade pack installed
- [ ] Official plugins installed
- [ ] Ran one grill

Next: Level 1 · Know.

---
Driven Young Founder OS · licensed to one business · see LICENSE.md
