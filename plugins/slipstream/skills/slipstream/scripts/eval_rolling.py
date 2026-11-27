#!/usr/bin/env python3
"""Production-like replay of skill discovery on real history (zero model tokens).
For each prompt that loaded a skill, the listed set is what lean_setup would list on that day:
skills used >=2x in the prior 30 days + reference closure + file skills + kept plugin skills.
Reports listed / hinted / missed. Usage: eval_rolling.py --pairs P --catalog C [--since YYYY-MM-DD (default: 30 days ago)]"""
import argparse, datetime as dt, glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "hooks")]
import slip_hint as sh
from closure import closure

ap = argparse.ArgumentParser()
ap.add_argument("--pairs", required=True); ap.add_argument("--catalog", required=True)
ap.add_argument("--since", default=(dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=30)).strftime("%Y-%m-%d")); ap.add_argument("--plugin-off", default="")
ap.add_argument("--json"); ap.add_argument("--window", type=int, default=30); ap.add_argument("--min-uses", type=int, default=2)
a = ap.parse_args()
H = os.path.expanduser("~")
idx = sh.load_index(a.catalog)
paths = {r[0]: r[3] for r in idx["rows"]}
off = set(filter(None, a.plugin_off.split(",")))
st = json.load(open(f"{H}/.claude/settings.json"))
plug = set()
for k, v in st.get("enabledPlugins", {}).items():
    if v and k not in off:
        n, _, m = k.partition("@")
        plug |= {os.path.basename(os.path.dirname(p)) for p in glob.glob(f"{H}/.claude/plugins/cache/{m}/{n}/*/skills/*/SKILL.md")}
synced = sorted(glob.glob(f"{H}/.claude/plugins/synced/*"), key=os.path.getmtime)[-1:]
for d in synced:
    plug |= {os.path.basename(os.path.dirname(p)) for p in glob.glob(f"{d}/*/skills/*/SKILL.md")}
extra = "".join(open(f, errors="ignore").read() for f in (f"{H}/.claude/CLAUDE.md", f"{H}/.codex/AGENTS.md") if os.path.exists(f))
FIX = {"skill-library", "slipstream", "xlsx", "docx", "pptx", "pdf"}
P = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
rows = [r for r in (json.loads(l) for l in open(a.pairs)) if r.get("ts") and "(Evaluation run:" not in r["prompt"]]
pos = sorted((r for r in rows if r["skills"]), key=lambda r: r["ts"])
follow = lambda t: len(t.split()) <= 6 or re.match(r"(?i)\s*(yes|yeah|yep|ok|okay|no|sure|go|do it)\b", t)
cache, res, misses, sizes = {}, {"listed": 0, "hinted": 0, "in_session": 0, "missed": 0, "missed_followups": 0}, [], []
seen = {}  # session -> skills already loaded earlier in that conversation (still in context)
for r in pos:
    sk = r["skills"][0]
    if r["ts"] < a.since or sk not in paths or sk == "skill-library":
        continue
    t = P(r["ts"])
    win = [x["skills"][0] for x in pos if t - dt.timedelta(days=a.window) <= P(x["ts"]) < t]
    key = frozenset(s for s in set(win) if win.count(s) >= a.min_uses)
    if key not in cache:
        cache[key] = closure(key | FIX, paths, extra) | plug
    core = cache[key]; sizes.append(len(core))
    earlier = seen.setdefault(r.get("session"), set())
    loaded_here = set(r["skills"])
    if sk in core:
        res["listed"] += 1
    elif sk in earlier:
        res["in_session"] += 1
    elif sk in [h[2] for h in sh.match(r["prompt"], idx, core)]:
        res["hinted"] += 1
    else:
        res["missed"] += 1; res["missed_followups"] += bool(follow(r["prompt"])); misses.append((sk, r["prompt"][:90]))
    earlier |= loaded_here
n = res["listed"] + res["hinted"] + res["in_session"] + res["missed"]
res.update(total=n, reachable_pct=round(100 * (n - res["missed"]) / max(n, 1), 1),
           median_listed=sorted(sizes)[len(sizes) // 2] if sizes else 0, kept_plugin_skills=len(plug))
print(json.dumps(res, indent=1))
for m in misses:
    print("  MISS", m)
if a.json:
    json.dump({"results": res, "misses": misses}, open(a.json, "w"), indent=1)
