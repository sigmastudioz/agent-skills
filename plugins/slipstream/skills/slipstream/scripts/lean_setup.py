#!/usr/bin/env python3
"""Lean setup: keep every skill reachable, pay for the listing only of the ones you use.

  python3 lean_setup.py               # dry run: print the plan, change nothing
  python3 lean_setup.py --apply       # do it; writes a manifest + settings backup
  python3 lean_setup.py --undo        # reverse the last --apply exactly
  python3 lean_setup.py --refresh     # weekly (auto via SessionStart): promote/archive by usage, relearn

Plan (data-driven, from your own logs):
  1. Core = personal skills used >= --min-uses times in --days days, plus --keep and any skill
     named in ~/.claude/CLAUDE.md or ~/.codex/AGENTS.md. Everything else in ~/.claude/skills moves
     to ~/.claude/skill-library/archive/ (moved, never deleted).
  2. Install the skill-library router + slipstream skill; build the catalog of every skill
     (archive, plugins, marketplaces) so archived skills stay one search away.
  3. Disable settings.json plugins with zero uses in the window (their files stay; catalog
     still indexes their skills).
  4. Register hooks: context meter + skill hint (UserPromptSubmit), poll guard (PreToolUse Bash).
  5. Codex: install the router + slipstream into ~/.codex/skills, append a 3-line rule block to
     ~/.codex/AGENTS.md.
"""
import argparse, datetime, glob, json, os, re, shutil, subprocess, sys

HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)  # slipstream package root
LIB = f"{HOME}/.claude/skill-library"
ARCH = f"{LIB}/archive"
MANIFEST = f"{LIB}/lean-manifest.json"
SETTINGS = f"{HOME}/.claude/settings.json"
CODEX_AGENTS = f"{HOME}/.codex/AGENTS.md"
RULES_TAG = "<!-- slipstream -->"
CODEX_RULES = f"""
{RULES_TAG}
- Tokens: every call re-sends the whole context. Never poll with sleep/wait tools; wait inside one shell call with `~/.codex/skills/slipstream/scripts/wait_for.sh --timeout 900 --every 15 -- <check>`.
- One task per thread; past ~100K of conversation, write a 40-line handoff and continue in a fresh thread.
- Specialist skills not listed live in a catalog: `python3 ~/.codex/skills/skill-library/scripts/find_skill.py "<task words>"`, then read the SKILL.md it returns.
{RULES_TAG}
"""


def usage(days):
    out = subprocess.run([sys.executable, f"{HERE}/skill_usage.py", "--days", str(days), "--json", "/dev/stdout"],
                         capture_output=True, text=True).stdout
    try:
        data = json.loads(out[: out.rindex("}") + 1])
    except Exception:
        sys.exit("could not read skill usage; run skill_usage.py manually to see the error")
    return dict(data["combined"])


def plan(a):
    used = usage(a.days)
    named = ""
    for f in (f"{HOME}/.claude/CLAUDE.md", CODEX_AGENTS):
        if os.path.exists(f):
            named += open(f, encoding="utf-8", errors="ignore").read()
    # general file skills are requested by synonym ("Excel", "slides"), not by name: keep listed
    keep = set(a.keep) | {"skill-library", "slipstream", "xlsx", "docx", "pptx", "pdf"}
    sys.path.insert(0, HERE)
    from closure import closure
    roots = (f"{HOME}/.claude/skills", ARCH)
    paths = {n: f"{r}/{n}/SKILL.md" for r in roots if os.path.isdir(r) for n in os.listdir(r)
             if not n.startswith(".") and os.path.exists(f"{r}/{n}/SKILL.md")}
    seed = {n for n in paths if used.get(n, 0) >= a.min_uses or n in keep or re.search(rf"\b{re.escape(n)}\b", named)}
    want = closure(seed, paths, named) | {n for n in os.listdir(f"{HOME}/.claude/skills") if not os.path.exists(f"{HOME}/.claude/skills/{n}/SKILL.md")}
    moves, core, restore = [], [], []
    for name in sorted(os.listdir(f"{HOME}/.claude/skills")):
        src = f"{HOME}/.claude/skills/{name}"
        if name.startswith(".") or not (os.path.isdir(src) or os.path.islink(src)):
            continue
        (core if name in want else moves).append(name)
    if os.path.isdir(ARCH):
        restore = sorted(n for n in os.listdir(ARCH) if n in want)  # archived skills back in use
    st = json.load(open(SETTINGS)) if os.path.exists(SETTINGS) else {}
    plugin_off = []
    for key, on in st.get("enabledPlugins", {}).items():
        if not on:
            continue
        pname = key.split("@")[0]
        roots = [r for r in (f"{HOME}/.claude/plugins/cache/{key.split('@')[-1]}/{pname}",) if os.path.isdir(r)]
        skills, behavior = set(), False
        for r in roots:
            for dp, dn, fn in os.walk(r):
                # hooks, output styles and MCP servers change behaviour even when never "invoked"
                if {"hooks.json", ".mcp.json"} & set(fn) or os.path.basename(dp) in ("hooks", "output-styles"):
                    behavior = True
                if "SKILL.md" in fn:
                    skills.add(os.path.basename(dp))
                skills |= {os.path.splitext(x)[0] for x in fn if x.endswith(".md") and x.upper() not in ("README.MD", "LICENSE.MD", "CHANGELOG.MD")}
        hits = sum(used.get(s, 0) + used.get(f"{pname}:{s}", 0) + used.get(f"agent:{s}", 0) + used.get(f"agent:{pname}:{s}", 0)
                   for s in skills) + used.get(f"mcp:{pname}", 0)
        content = bool(skills)  # README/LICENSE are already excluded from `skills`
        if not hits and not behavior and content and pname not in keep:  # pure-content plugins only
            plugin_off.append(key)
    return core, moves, plugin_off, restore


def synced_report(used):
    """Desktop-app plugins synced from the claude.ai account: report only (managed in claude.ai)."""
    d = sorted(glob.glob(f"{HOME}/.claude/plugins/synced/*"), key=os.path.getmtime)[-1:]
    idle = []
    for pl in sorted(glob.glob(f"{d[0]}/*/")) if d else []:
        name = os.path.basename(pl.rstrip("/")).split("~")[0]
        sk = [os.path.basename(os.path.dirname(p)) for p in glob.glob(pl + "skills/*/SKILL.md")]
        sk += [os.path.splitext(os.path.basename(p))[0] for p in glob.glob(pl + "commands/*.md")]
        if not sum(used.get(x, 0) + used.get(f"{name}:{x}", 0) for x in sk) + used.get(f"mcp:{name}", 0):
            idle.append(f"{name} ({len(sk)})")
    if idle:
        print(f"\nclaude.ai-synced plugins with zero uses (turn off in your claude.ai plugin settings to shrink "
              f"the desktop listing and its connectors): {', '.join(idle)}")


def learn():
    """Rebuild catalog + learned triggers from history. Local files only."""
    subprocess.run([sys.executable, f"{HERE}/build_catalog.py", "--out", f"{LIB}/catalog.tsv"], check=True)
    subprocess.run([sys.executable, f"{HERE}/mine_pairs.py", "--days", "90", "--out", f"{LIB}/pairs.jsonl"], check=True)
    subprocess.run([sys.executable, f"{HERE}/learn_aliases.py", "--pairs", f"{LIB}/pairs.jsonl",
                    "--catalog", f"{LIB}/catalog.tsv", "--out", f"{LIB}/aliases.json"], check=True)
    open(f"{LIB}/last-refresh", "w").write(datetime.datetime.now().isoformat())


def refresh(a):
    """Weekly: promote archived skills that came back into use, archive newly idle ones, relearn."""
    if not os.path.exists(MANIFEST):
        sys.exit("not installed (no manifest); run --apply first")
    m = json.load(open(MANIFEST))
    core, moves, _, restore = plan(a)
    for name in restore:
        src, dst = f"{ARCH}/{name}", f"{HOME}/.claude/skills/{name}"
        if not os.path.lexists(dst):
            shutil.move(src, dst)
            m["moved"] = [x for x in m["moved"] if x[1] != src]
            m.setdefault("promoted", []).append(name)
    for name in moves:
        src, dst = f"{HOME}/.claude/skills/{name}", f"{ARCH}/{name}"
        if name in ("skill-library", "slipstream") or os.path.lexists(dst):
            continue
        shutil.move(src, dst)
        m["moved"].append([src, dst])
    json.dump(m, open(MANIFEST, "w"), indent=1)
    learn()
    print(f"refresh: promoted {len(restore)} {restore}, archived {len(moves)}")


def hooks_block():
    py = sys.executable
    return {
        "UserPromptSubmit": [{"hooks": [{"type": "command", "command": f'"{py}" "{LIB}/slipstream/hooks/slip_meter.py"'},
                                        {"type": "command", "command": f'"{py}" "{LIB}/slipstream/hooks/slip_hint.py"'}]}],
        "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": f'"{py}" "{LIB}/slipstream/hooks/slip_guard.py"'}]}],
        "SessionStart": [{"hooks": [{"type": "command", "command": f'"{py}" "{LIB}/slipstream/hooks/auto_refresh.py"'}]}],
    }


def apply(a):
    core, moves, plugin_off, _ = plan(a)
    print(f"core skills kept listed: {len(core)}\nskills moved to archive (still searchable): {len(moves)}\n"
          f"plugins disabled (zero uses in {a.days:g} days): {len(plugin_off)} {plugin_off}")
    if not a.apply:
        print("\ncore:", " ".join(core))
        synced_report(usage(a.days))
        print("\nDry run only. Re-run with --apply to make these changes (reversible with --undo).")
        return
    if os.path.exists(MANIFEST):
        sys.exit(f"{MANIFEST} exists: run --undo first, or remove it if you already undid by hand")
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    m = {"stamp": stamp, "moved": [], "installed": [], "settings_backup": f"{LIB}/settings.backup-{stamp}.json",
         "codex_rules": False}
    os.makedirs(ARCH, exist_ok=True)
    shutil.copy2(SETTINGS, m["settings_backup"])
    # 1. archive unused skills
    for name in moves:
        src, dst = f"{HOME}/.claude/skills/{name}", f"{ARCH}/{name}"
        if os.path.lexists(dst):
            continue
        shutil.move(src, dst)
        m["moved"].append([src, dst])
    # 2. install router + slipstream (library copy is the canonical one hooks point at)
    for dst in (f"{LIB}/slipstream", f"{HOME}/.claude/skills/skill-library", f"{HOME}/.claude/skills/slipstream",
                f"{HOME}/.codex/skills/skill-library", f"{HOME}/.codex/skills/slipstream"):
        if os.path.lexists(dst):
            continue
        src = f"{PKG}/router" if dst.endswith("skill-library") else PKG
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("evidence", "router", "__pycache__"))
        m["installed"].append(dst)
    for d in (f"{HOME}/.codex/skills/skill-library", f"{HOME}/.claude/skills/skill-library"):
        if os.path.isdir(d):
            # Point the router at the shared catalog.
            p = f"{d}/scripts/find_skill.py"
            s = open(p).read().replace('"~/.claude/skill-library/catalog.tsv"', f'"{LIB}/catalog.tsv"')
            open(p, "w").write(s)
    learn()
    # 3 + 4. settings: disable unused plugins, add hooks (merge, never replace)
    st = json.load(open(SETTINGS))
    for key in plugin_off:
        st["enabledPlugins"][key] = False
    for ev, entries in hooks_block().items():
        st.setdefault("hooks", {}).setdefault(ev, []).extend(entries)
    m["plugins_disabled"] = plugin_off
    json.dump(st, open(SETTINGS, "w"), indent=2)
    # 5. codex rules
    if os.path.exists(CODEX_AGENTS) and RULES_TAG not in open(CODEX_AGENTS).read():
        open(CODEX_AGENTS, "a").write(CODEX_RULES)
        m["codex_rules"] = True
    json.dump(m, open(MANIFEST, "w"), indent=1)
    print(f"\nApplied. Manifest: {MANIFEST}\nUndo anytime: python3 {os.path.abspath(__file__)} --undo")
    synced_report(usage(a.days))


def undo():
    if not os.path.exists(MANIFEST):
        sys.exit("nothing to undo (no manifest)")
    m = json.load(open(MANIFEST))
    for src, dst in reversed(m["moved"]):
        if os.path.lexists(dst) and not os.path.lexists(src):
            shutil.move(dst, src)
    for d in m["installed"]:
        shutil.rmtree(d, ignore_errors=True)
    st = json.load(open(SETTINGS))
    for key in m.get("plugins_disabled", []):
        st.setdefault("enabledPlugins", {})[key] = True
    ours = json.dumps(hooks_block())
    for ev in ("UserPromptSubmit", "PreToolUse", "SessionStart"):
        if ev in st.get("hooks", {}):
            st["hooks"][ev] = [e for e in st["hooks"][ev] if json.dumps(e) not in ours]
            if not st["hooks"][ev]:
                del st["hooks"][ev]
    if "hooks" in st and not st["hooks"]:
        del st["hooks"]
    json.dump(st, open(SETTINGS, "w"), indent=2)
    if m.get("codex_rules") and os.path.exists(CODEX_AGENTS):
        t = open(CODEX_AGENTS).read()
        open(CODEX_AGENTS, "w").write(re.sub(rf"\n{re.escape(RULES_TAG)}.*?{re.escape(RULES_TAG)}\n", "", t, flags=re.S))
    os.rename(MANIFEST, MANIFEST + ".undone")
    print(f"Undone: {len(m['moved'])} skills restored, {len(m.get('plugins_disabled', []))} plugins re-enabled, hooks removed. "
          f"Settings backup kept at {m['settings_backup']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true"); ap.add_argument("--undo", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--days", type=float, default=30); ap.add_argument("--min-uses", type=int, default=1)
    ap.add_argument("--keep", nargs="*", default=[])
    a = ap.parse_args()
    undo() if a.undo else refresh(a) if a.refresh else apply(a)
