#!/usr/bin/env python3
"""Inventory what every Claude Code / Codex session pays for before the first word.

Read-only. Estimates listing cost from skill/agent frontmatter descriptions (~4 chars/token)
plus always-loaded instruction files. Prints the biggest contributors first.
Usage: python3 preamble.py [--top 25]
"""
import argparse, glob, json, os, re

HOME = os.path.expanduser("~")
FM = re.compile(rb"^---\s*\n(.*?)\n---", re.S)


def listing_chars(md_path):
    """Chars of name+description, which is what a skill/agent listing injects."""
    try:
        head = open(md_path, "rb").read(8000)
    except OSError:
        return 0
    m = FM.match(head)
    if not m:
        return 0
    fm = m.group(1)
    keep = [l for l in fm.splitlines() if l.startswith((b"name:", b"description:")) or l.startswith(b"  ")]
    return sum(len(l) for l in keep) + 20


def scan(root, pattern):
    files = glob.glob(os.path.join(root, pattern), recursive=True)
    return len(files), sum(listing_chars(f) for f in files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()
    rows = []
    n, c = scan(f"{HOME}/.claude/skills", "*/SKILL.md")
    rows.append(("claude personal skills (~/.claude/skills)", n, c))
    n, c = scan(f"{HOME}/.claude/agents", "*.md")
    rows.append(("claude personal agents (~/.claude/agents)", n, c))
    settings = json.load(open(f"{HOME}/.claude/settings.json")) if os.path.exists(f"{HOME}/.claude/settings.json") else {}
    enabled = [k for k, v in settings.get("enabledPlugins", {}).items() if v]
    cache = f"{HOME}/.claude/plugins/cache"
    for key in enabled:
        name, _, market = key.partition("@")
        roots = glob.glob(f"{cache}/{market}/{name}/*") or glob.glob(f"{cache}/*/{name}/*")
        root = sorted(roots)[-1] if roots else None
        if not root:
            rows.append((f"plugin {key} (not in cache)", 0, 0)); continue
        sn, sc = scan(root, "**/skills/*/SKILL.md")
        an, ac = scan(root, "**/agents/*.md")
        cn, cc = scan(root, "**/commands/*.md")
        rows.append((f"plugin {key}  [{sn} skills, {an} agents, {cn} cmds]", sn + an + cn, sc + ac + cc))
    for f in (f"{HOME}/.claude/CLAUDE.md", f"{HOME}/.codex/AGENTS.md"):
        if os.path.exists(f):
            txt = open(f, encoding="utf-8", errors="ignore").read()
            extra = 0
            for imp in re.findall(r"^@(\S+)", txt, re.M):
                p = os.path.expanduser(imp)
                extra += os.path.getsize(p) if os.path.exists(p) else 0
            rows.append((f"always-loaded {f.replace(HOME, '~')} (+@imports)", 1, len(txt) + extra))
    n, c = scan(f"{HOME}/.codex/skills", "*/SKILL.md")
    rows.append(("codex skills (~/.codex/skills)", n, c))
    cj = f"{HOME}/.claude.json"
    mcp = list(json.load(open(cj)).get("mcpServers", {})) if os.path.exists(cj) else []
    rows.sort(key=lambda r: -r[2])
    total = sum(r[2] for r in rows)
    print(f"{'source':72} {'items':>6} {'~tokens':>8}")
    for label, n, c in rows[: a.top]:
        print(f"{label[:72]:72} {n:6} {c // 4:8}")
    print(f"\nestimated listing+instructions: ~{total // 4} tokens, every call, every session")
    print(f"enabled plugins: {len(enabled)}; user MCP servers: {mcp} (each adds tool names/schemas)")
    print("Measure the real number: claude -p 'Reply OK' --output-format json  -> usage (input+cache_*)")


if __name__ == "__main__":
    main()
