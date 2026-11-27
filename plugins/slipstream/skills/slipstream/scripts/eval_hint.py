#!/usr/bin/env python3
"""Offline evaluation of the skill-hint hook on mined history (zero model tokens).
  recall_archived: prompts whose loaded skill would be archived (not core) -> hinted correctly?
  recall_all:      stress test with nothing listed: every positive must be found by the hint
  noise:           share of no-skill prompts that still get a hint, and tokens spent on hints
Usage: python3 eval_hint.py --pairs pairs.jsonl --core-dir DIR [--catalog PATH] [--show 15]"""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks"))
import slip_hint as sh

ap = argparse.ArgumentParser()
ap.add_argument("--pairs", required=True); ap.add_argument("--core-dir", required=True)
ap.add_argument("--catalog", default=os.environ.get("SKILL_CATALOG", os.path.expanduser("~/.claude/skill-library/catalog.tsv")))
ap.add_argument("--show", type=int, default=15); ap.add_argument("--json")
ap.add_argument("--before", help="test only on prompts at/after this date; core = skills loaded >=2x before it")
ap.add_argument("--neg-sample", type=int, default=0)
a = ap.parse_args()
idx = sh.load_index(a.catalog)
names = {r[0] for r in idx["rows"]}
core = set(os.listdir(a.core_dir))
rows = [json.loads(l) for l in open(a.pairs)]
if a.before:
    from collections import Counter
    train = Counter(r["skills"][0] for r in rows if r["skills"] and r.get("ts", "") < a.before)
    core = {s for s, n in train.items() if n >= 2} | {"skill-library", "slipstream", "xlsx", "docx", "pptx", "pdf"}
    rows = [r for r in rows if r.get("ts", "") >= a.before]
    print(f"train-derived core: {len(core)} skills; test prompts: {len(rows)}")
pos = [r for r in rows if r["skills"] and r["skills"][0] in names and r["skills"][0] != "skill-library"]
neg = [r for r in rows if not r["skills"]]
if a.neg_sample:
    import random; random.seed(7); neg = random.sample(neg, min(a.neg_sample, len(neg)))
res, misses = {}, []
for label, listed, subset in (("recall_archived", core, [r for r in pos if r["skills"][0] not in core]),
                              ("recall_all", set(), pos)):
    hit = 0
    for r in subset:
        got = [h[2] for h in sh.match(r["prompt"], idx, listed)]
        ok = r["skills"][0] in got
        hit += ok
        if not ok and label == "recall_all":
            misses.append((r["skills"][0], r["prompt"][:110], got))
    res[label] = f"{hit}/{len(subset)}" + (f" ({100 * hit / len(subset):.0f}%)" if subset else "")
fired, tok = 0, 0
for r in neg:
    h = sh.match(r["prompt"], idx, core)
    if h:
        fired += 1
        tok += 40 + sum(len(x[3][:110]) + len(x[4]) for x in h) // 4
import re as _re
follow = lambda t: len(t.split()) <= 6 or _re.match(r"(?i)\s*(yes|yeah|yep|ok|okay|no|sure|go|do it)\b", t)
sub = [r for r in pos if r["skills"][0] not in core and not follow(r["prompt"])]
res["recall_archived_excl_followups"] = f"{sum(r['skills'][0] in [h[2] for h in sh.match(r['prompt'], idx, core)] for r in sub)}/{len(sub)}"
res["noise"] = f"{fired}/{len(neg)} no-skill prompts hinted ({100 * fired / max(len(neg), 1):.1f}%), ~{tok // max(fired, 1)} tokens each"
print(json.dumps(res, indent=1))
for m in misses[: a.show]:
    print("MISS", m)
if a.json:
    json.dump({"results": res, "misses": misses}, open(a.json, "w"), indent=1)
