#!/usr/bin/env python3
"""Rank catalog skills for a task. Usage: find_skill.py "task words" [--n 8] [--catalog PATH]"""
import argparse, os, re
STOP = set("a an the and or for to of in on with my me i we use using how do can this that it is be from into by".split())
ap = argparse.ArgumentParser(); ap.add_argument("query"); ap.add_argument("--n", type=int, default=8)
ap.add_argument("--catalog", default=os.environ.get("SKILL_CATALOG", os.path.expanduser("~/.claude/skill-library/catalog.tsv")))
a = ap.parse_args()
words = [w for w in re.findall(r"[a-z0-9+#.]+", a.query.lower()) if w not in STOP and len(w) > 1]
stems = {w: w[:max(4, len(w) - 3)] for w in words}
import math
rows = [l.rstrip("\n").split("\t") for l in open(a.catalog, encoding="utf-8", errors="ignore")]
rows = [r for r in rows if len(r) >= 4]
texts = [(r[0].lower().replace("-", " ") + " " + r[1].lower(), r[2].lower()) for r in rows]
idf = {st: math.log((len(rows) + 1) / (1 + sum(st in n or st in d for n, d in texts))) for st in stems.values()}
scored = []
for (name, src, desc, path, *_), (n, d) in zip(rows, texts):
    s = round(sum(idf[st] * (3 * (st in n) + (st in d)) for st in stems.values()), 1)
    if s: scored.append((s, name, src, desc, path))
for s, name, src, desc, path in sorted(scored, key=lambda r: -r[0])[: a.n]:
    print(f"{s:3} {name} [{src}]\n    {desc}\n    {path}")
