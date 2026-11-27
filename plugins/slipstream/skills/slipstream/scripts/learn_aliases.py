#!/usr/bin/env python3
"""Learn the local user's own trigger words per skill from history (prompt -> skill loaded).
A word becomes an alias for a skill when it appears in >= --min prompts that loaded that skill,
in at most --max-df of all prompts, and points to that skill in >= --purity of its positive uses.
Usage: python3 learn_aliases.py --pairs pairs.jsonl [--before YYYY-MM-DD] [--out aliases.json]"""
import argparse, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks"))
from slip_hint import STOP, own_words

ap = argparse.ArgumentParser()
ap.add_argument("--pairs", required=True); ap.add_argument("--before", default="9999")
ap.add_argument("--min", type=int, default=3); ap.add_argument("--max-df", type=float, default=0.002)
ap.add_argument("--purity", type=float, default=0.8)
ap.add_argument("--catalog", default=os.path.expanduser("~/.claude/skill-library/catalog.tsv"))
ap.add_argument("--out", default=os.path.expanduser("~/.claude/skill-library/aliases.json"))
a = ap.parse_args()
rows = [json.loads(l) for l in open(a.pairs)]
rows = [r for r in rows if r.get("ts", "") < a.before]
words = lambda t: {w for w in re.findall(r"[a-z0-9+#]+", own_words(t).lower()) if w not in STOP and len(w) >= 4}
df, per = Counter(), defaultdict(Counter)
for r in rows:
    ws = words(r["prompt"])
    df.update(ws)
    if r["skills"] and r["skills"][0] != "skill-library":
        per[r["skills"][0]].update(ws)
pos_total = Counter()
for sk, c in per.items():
    for w, n in c.items():
        pos_total[w] += n
aliases = {}
for sk, c in per.items():
    for w, n in c.items():
        if n >= a.min and df[w] <= a.max_df * len(rows) and n / pos_total[w] >= a.purity:
            if w not in aliases or n > per[aliases[w]][w]:
                aliases[w] = sk
# distinctive name words: unique to one skill name in the catalog AND rare in the user's prompts
names = [l.split("\t")[0] for l in open(a.catalog, encoding="utf-8", errors="ignore")]
ndf = Counter(t for n in names for t in set(re.split(r"[-_:\s]+", n.lower())) if len(t) >= 4)
descs = [set(re.findall(r"[a-z0-9]+", l.split("\t")[2].lower())) for l in open(a.catalog, encoding="utf-8", errors="ignore") if l.count("\t") >= 3]
ddf = Counter(w for d in descs for w in d)
unique = sorted(t for t, n in ndf.items() if n == 1 and ddf[t] <= 3 and t not in STOP)  # not generic English
json.dump({"aliases": aliases, "unique": unique}, open(a.out, "w"), indent=1, sort_keys=True)
print(f"{len(aliases)} aliases, {len(unique)} distinctive name words, from {len(rows)} prompts -> {a.out}")
print(", ".join(f"{w}->{s}" for w, s in sorted(aliases.items())[:40]))
