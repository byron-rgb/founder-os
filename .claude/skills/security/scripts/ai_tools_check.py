#!/usr/bin/env python3
"""
ai_tools_check.py: a first look at the AI skills, plugins and Claude settings on this computer.

What it does
  1. Lists the skills in a folder (default ~/.claude/skills) and the installed
     Claude plugins, and for each one notes: does it come with a licence, do we
     know where it came from, does it include scripts.
  2. Looks for warning signs in the files (our own short list, adapted from the
     AI Scout checks): reaching out to the internet, running downloaded code,
     reading passwords or keys, hidden or scrambled text, and text that tries to
     tell the AI to ignore its rules. These are "worth a look" flags, not proof.
  3. If SkillSpector (NVIDIA, Apache-2.0) is installed, runs its static scan
     (no AI pass) on each skill and adds up the results.
  4. Reads Claude's settings files and flags risky choices (skip-all-permission
     mode, very broad "allow" rules, auto-approving every project's connectors,
     secret-looking names in env). It reports NAMES and COUNTS only, never values.

What it touches
  Reads files only. Writes nothing except the --json file if asked. No network.

Usage
  python3 -I ai_tools_check.py
  python3 -I ai_tools_check.py --skills ~/.claude/skills --skillspector ~/Code/skillspector/.venv/bin/skillspector
  python3 -I ai_tools_check.py --names        (also list which skills got flags; default is counts only)
  python3 -I ai_tools_check.py --json out.json

Part of the Founder OS security module (Driven Young). Read-only.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

HOME = os.path.expanduser("~")
TEXT_EXT = {".md", ".txt", ".py", ".js", ".cjs", ".mjs", ".ts", ".sh", ".bash", ".zsh", ".json", ".yaml", ".yml", ".toml", ".rb", ".ps1"}
SCRIPT_EXT = {".py", ".js", ".cjs", ".mjs", ".ts", ".sh", ".bash", ".zsh", ".rb", ".ps1"}

FLAGS = {
    "internet": re.compile(r"\b(curl|wget)\s|urlopen\(|requests\.(get|post|put)\(|\bfetch\(|axios\.|http\.client|socket\.connect", re.I),
    "runs_downloaded_code": re.compile(r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh\b|\beval\(|base64\s+(-d|--decode)[^\n]*\|\s*(ba|z)?sh|exec\(\s*(requests|urllib|base64)", re.I),
    "reads_secrets": re.compile(r"find-(generic|internet)-password|\.ssh/id_|\.aws/credentials|keychain|1password|op\s+read\s|\.netrc|cookies\.sqlite|Login Data", re.I),
    "rule_breaking_text": re.compile(r"ignore (all |any )?(previous|prior|above) (instructions|rules)|disregard (your|the) (rules|instructions)|do not (tell|inform) the user|without (asking|telling) the user|bypass(es)? (the )?(safety|permission)", re.I),
    "hidden_text": re.compile(r"[A-Za-z0-9+/]{400,}={0,2}|[\u200b\u200c\u200d\u2060\ufeff]{3,}|(\\x[0-9a-f]{2}){20,}", re.I),
}
SECRET_NAME = re.compile(r"(key|token|secret|password|passwd|pwd|auth|credential)", re.I)


def read_text(path, limit=2_000_000):
    try:
        if os.path.getsize(path) > limit:
            return ""
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return ""


def scan_item(folder):
    info = {"name": os.path.basename(folder.rstrip("/")), "path": folder, "flags": set(), "scripts": 0, "files": 0,
            "licence": False, "source_known": False}
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "venv", "__pycache__")]
        for fn in files:
            p = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            info["files"] += 1
            if fn.upper().startswith(("LICENSE", "LICENCE", "COPYING")):
                info["licence"] = True
            if fn.upper().startswith(("SOURCE", "CREDITS")) or fn == ".git":
                info["source_known"] = True
            if ext in SCRIPT_EXT:
                info["scripts"] += 1
            if ext in TEXT_EXT or fn == "SKILL.md":
                t = read_text(p)
                for k, rx in FLAGS.items():
                    if rx.search(t):
                        info["flags"].add(k)
    if os.path.isdir(os.path.join(folder, ".git")):
        info["source_known"] = True
    return info


def run_skillspector(bin_path, folder):
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ss.json")
        try:
            subprocess.run([bin_path, "scan", folder, "--no-llm", "--format", "json", "--output", out],
                           capture_output=True, text=True, timeout=300)
            with open(out) as fh:
                d = json.load(fh)
        except Exception as e:
            return {"error": str(e)[:120]}
    counts = {}
    for f in d.get("issues", []) or []:
        sev = str(f.get("severity", "unknown")).lower()
        counts[sev] = counts.get(sev, 0) + 1
    ra = d.get("risk_assessment", {}) or {}
    return {"counts": counts, "score": ra.get("score"), "recommendation": ra.get("recommendation")}


def settings_check(claude_dir, claude_json):
    out = {"files": [], "flags": []}
    paths = [os.path.join(claude_dir, "settings.json"), os.path.join(claude_dir, "settings.local.json")]
    for p in paths:
        if not os.path.exists(p):
            continue
        try:
            d = json.load(open(p))
        except Exception:
            out["flags"].append(f"{os.path.basename(p)}: couldn't read it")
            continue
        out["files"].append(os.path.basename(p))
        perm = d.get("permissions", {}) or {}
        mode = perm.get("defaultMode")
        if mode == "bypassPermissions" or d.get("skipDangerousModePermissionPrompt"):
            out["flags"].append(f"{os.path.basename(p)}: Claude is set to skip all permission checks (bypass mode)")
        allow = perm.get("allow", []) or []
        broad = [a for a in allow if a in ("Bash", "Bash(*)", "Bash(:*)", "Write", "Edit", "WebFetch") or re.fullmatch(r"Bash\((sudo|rm|curl|ssh|python3?|node|sh|bash|zsh)[ :]?\*\)", a)]
        if broad:
            out["flags"].append(f"{os.path.basename(p)}: {len(broad)} very broad 'allow' rule(s) that let Claude run things without asking")
        if d.get("enableAllProjectMcpServers"):
            out["flags"].append(f"{os.path.basename(p)}: every project's connectors (MCP servers) are approved automatically")
        env = d.get("env", {}) or {}
        secretish = [k for k in env if SECRET_NAME.search(k)]
        if secretish:
            out["flags"].append(f"{os.path.basename(p)}: {len(secretish)} secret-looking setting(s) stored in plain text (names only checked, values not read out)")
        hooks = d.get("hooks", {}) or {}
        n_hooks = sum(len(v) for v in hooks.values()) if isinstance(hooks, dict) else 0
        if n_hooks:
            out.setdefault("hooks", 0)
            out["hooks"] += n_hooks
    # MCP servers configured at user level (names counted only)
    cj = claude_json
    if os.path.exists(cj):
        try:
            d = json.load(open(cj))
            out["user_mcp_servers"] = len(d.get("mcpServers", {}) or {})
        except Exception:
            pass
    return out


def plugins_list(claude_dir):
    p = os.path.join(claude_dir, "plugins", "installed_plugins.json")
    try:
        d = json.load(open(p))
        plugs = d.get("plugins", d)
        return sorted(plugs.keys()) if isinstance(plugs, dict) else []
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser(description="AI tools first look (read-only, counts only by default)")
    ap.add_argument("--skills", action="append", help="skills folder (repeatable). Default ~/.claude/skills")
    ap.add_argument("--skillspector", help="path to the skillspector command (optional; adds a static scan of each skill)")
    ap.add_argument("--claude-dir", default=os.path.join(HOME, ".claude"), help="Claude settings folder (default ~/.claude)")
    ap.add_argument("--claude-json", default=os.path.join(HOME, ".claude.json"), help="Claude user config file (default ~/.claude.json)")
    ap.add_argument("--names", action="store_true", help="also list which items got flags")
    ap.add_argument("--json")
    a = ap.parse_args()
    claude_dir = os.path.expanduser(a.claude_dir)
    claude_json = os.path.expanduser(a.claude_json)
    folders = a.skills or [os.path.join(claude_dir, "skills")]
    items = []
    for base in folders:
        base = os.path.expanduser(base)
        if os.path.isfile(os.path.join(base, "SKILL.md")):
            items.append(scan_item(base))
            continue
        for name in sorted(os.listdir(base)) if os.path.isdir(base) else []:
            p = os.path.join(base, name)
            if os.path.isdir(p) and not name.startswith("."):
                items.append(scan_item(p))
    ss = os.path.expanduser(a.skillspector) if a.skillspector else None  # opt-in: about 10-30 seconds per skill
    ss_totals = {}
    ss_items_with_high = []
    if ss:
        for it in items:
            res = run_skillspector(ss, it["path"])
            it["skillspector"] = res
            for sev, n in (res.get("counts") or {}).items():
                ss_totals[sev] = ss_totals.get(sev, 0) + n
            if any((res.get("counts") or {}).get(s) for s in ("high", "critical")):
                ss_items_with_high.append(it["name"])

    flag_counts = {k: sum(1 for i in items if k in i["flags"]) for k in FLAGS}
    summary = {
        "skills": len(items),
        "with_scripts": sum(1 for i in items if i["scripts"]),
        "no_licence_file": sum(1 for i in items if not i["licence"]),
        "source_unknown": sum(1 for i in items if not i["source_known"]),
        "flags": flag_counts,
        "skillspector": {"ran": bool(ss), "totals": ss_totals, "items_with_high_or_critical": len(ss_items_with_high)},
        "plugins_installed": len(plugins_list(claude_dir)),
        "settings": settings_check(claude_dir, claude_json),
    }
    print(f"AI tools first look: {summary['skills']} skills, {summary['plugins_installed']} plugins installed")
    print(f"  {summary['with_scripts']} include scripts | {summary['no_licence_file']} have no licence file | "
          f"{summary['source_unknown']} have no record of where they came from")
    print("  Warning signs (worth a look, not proof): " + ", ".join(f"{k.replace('_', ' ')} {v}" for k, v in flag_counts.items()))
    if ss:
        print(f"  SkillSpector (static): {ss_totals or 'no findings'}; {len(ss_items_with_high)} item(s) with high or critical")
    else:
        print("  SkillSpector not found: static scan skipped (see references/checks/ai-tool-vetting.md)")
    st = summary["settings"]
    print(f"  Claude settings: {len(st['flags'])} flag(s); {st.get('user_mcp_servers', '?')} user-level connectors; {st.get('hooks', 0)} hooks")
    for fl in st["flags"]:
        print("    - " + fl)
    if a.names:
        for i in items:
            if i["flags"] or i["name"] in ss_items_with_high:
                print(f"    {i['name']}: {', '.join(sorted(i['flags']))}" + (" + SkillSpector high" if i["name"] in ss_items_with_high else ""))
    if a.json:
        summary["items"] = [{**{k: v for k, v in i.items() if k != "path"}, "flags": sorted(i["flags"])} for i in items] if a.names else []
        with open(a.json, "w") as fh:
            json.dump(summary, fh, indent=2)


if __name__ == "__main__":
    sys.exit(main())
