#!/usr/bin/env python3
"""Build a searchable one-line-per-skill catalog of every skill on this machine.
Output TSV: name <TAB> source <TAB> description(<=160 chars) <TAB> path
Usage: python3 build_catalog.py [--out ~/.claude/skill-library/catalog.tsv]"""
import argparse, glob, os, re
HOME = os.path.expanduser("~")
FM = re.compile(r"^---\s*\n(.*?)\n---", re.S)

def meta(p):
    try: t = open(p, encoding="utf-8", errors="ignore").read(6000)
    except OSError: return None
    m = FM.match(t)
    if not m: return None
    fm = m.group(1); name = re.search(r"^name:\s*(.+)$", fm, re.M)
    d = re.search(r"^description:\s*(.*?)(?=^\S[\w-]*:|\Z)", fm, re.M | re.S)
    desc = re.sub(r"\s+", " ", (d.group(1) if d else "")).strip().strip("'\"|>")
    return (name.group(1).strip().strip("'\"") if name else os.path.basename(os.path.dirname(p))), desc[:160]

def latest(paths):
    best = {}
    for p in paths:
        parts = p.split("/skills/")[0].split("/")
        key = "/".join(parts[:-1]) + "|" + os.path.basename(os.path.dirname(p))
        if key not in best or os.path.getmtime(p) > os.path.getmtime(best[key]): best[key] = p
    return best.values()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=f"{HOME}/.claude/skill-library/catalog.tsv")
    ap.add_argument("--roots", nargs="*", default=[f"{HOME}/.claude/skills", f"{HOME}/.claude/skill-library/archive", f"{HOME}/.agents/skills", f"{HOME}/.codex/skills"])
    a = ap.parse_args(); rows, seen = [], set()
    for r in a.roots:
        for p in sorted(glob.glob(f"{r}/**/SKILL.md", recursive=True)):
            m = meta(p)
            if m and os.path.realpath(p) not in seen:
                seen.add(os.path.realpath(p)); rows.append((m[0], os.path.basename(r), m[1], p))
    plug = glob.glob(f"{HOME}/.claude/plugins/cache/*/*/*/skills/*/SKILL.md")
    synced = sorted(glob.glob(f"{HOME}/.claude/plugins/synced/*"), key=os.path.getmtime)[-1:]
    for d in synced: plug += glob.glob(f"{d}/*/skills/*/SKILL.md")
    plug += glob.glob(f"{HOME}/.claude/plugins/marketplaces/**/skills/*/SKILL.md", recursive=True)
    names = {r[0] for r in rows}
    for p in latest(plug):
        if any(x in p for x in ("/temp_git_", "/.trash/", "/fixtures/", "/tests/")): continue
        m = meta(p)
        if m and os.path.realpath(p) not in seen and m[0] not in names:
            seen.add(os.path.realpath(p)); names.add(m[0])
            src = re.search(r"/(?:cache/[^/]+|synced/[^/]+|marketplaces/(?:[^/]+/)*?plugins|marketplaces)/([^/~]+)", p)
            rows.append((m[0], "plugin:" + (src.group(1) if src else "?"), m[1], p))
    os.makedirs(os.path.dirname(os.path.expanduser(a.out)), exist_ok=True)
    with open(os.path.expanduser(a.out), "w") as f:
        for r in rows: f.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
    print(f"{len(rows)} skills -> {a.out}")

if __name__ == "__main__": main()
