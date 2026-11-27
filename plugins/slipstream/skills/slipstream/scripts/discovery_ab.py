#!/usr/bin/env python3
"""Discovery A/B: does a fresh agent still find the right skill with a lean listing?

Runs each task headless in two arms and records which skill was loaded (Skill tool call or
SKILL.md read), whether it matches the expected skill, and total input tokens.
  FULL: your normal setup, run from --full-dir
  LEAN: project-only settings in --lean-dir (core skills + skill-library router), plugins off
Usage: python3 discovery_ab.py --lean-dir DIR --full-dir DIR --settings lean.json [--model sonnet]
"""
import argparse, json, os, re, subprocess, sys

TASKS = [  # (prompt, accepted skill names) — first five are catalog-only, last five are core
    ("Help me detect Kerberoasting attacks in our Splunk logs.", {"detecting-kerberoasting-attacks"}),
    ("Set up localization for my Unity game's UI text.", {"localization"}),
    ("Write an Airflow DAG for our daily ETL job.", {"airflow-dag-patterns"}),
    ("Triage this NDA a vendor sent us before I sign it.", {"triage-nda", "nda-triage"}),
    ("Run QC on my single-cell RNA-seq dataset.", {"single-cell-rna-qc"}),
    ("Summarize what happens in demo.mp4 in this folder.", {"video-understanding"}),
    ("My test suite started failing after a refactor and I can't see why; help me find the cause.", {"systematic-debugging", "investigate", "investigate-first"}),
    ("Turn this folder of notes into a knowledge graph I can query.", {"graphify"}),
    ("Convert report.md into a nicely formatted PDF.", {"pdf", "make-pdf"}),
    ("Brainstorm a new feature for my app before we build anything.", {"brainstorming"}),
]
SUFFIX = ("\n\n(Evaluation run: load whichever skill you would normally use for this, then reply with "
          "one sentence naming the skill and your first step. Do not carry out the task.)")
SKILL_PATH = re.compile(r"/([^/]+)/SKILL\.md")


def run(prompt, cwd, extra, model, env):
    cmd = ["claude", "-p", prompt + SUFFIX, "--model", model, "--output-format", "stream-json", "--verbose",
           "--max-turns", "8", "--strict-mcp-config", "--allowedTools", "Skill", "Read", "Grep", "Glob",
           "Bash(python3:*)", "Bash(grep:*)", "Bash(ls:*)"] + extra
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, timeout=600)
    loaded, tokens, turns = [], 0, 0
    for line in p.stdout.splitlines():
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("type") == "assistant":
            for b in ev["message"].get("content", []):
                if b.get("type") != "tool_use":
                    continue
                inp = b.get("input", {})
                if b["name"] == "Skill":
                    loaded.append(inp.get("skill", "").split(":")[-1])
                elif b["name"] == "Read" and "SKILL.md" in inp.get("file_path", ""):
                    m = SKILL_PATH.search(inp["file_path"])
                    if m and m.group(1) != "skill-library":
                        loaded.append(m.group(1))
        if ev.get("type") == "result":
            u = ev.get("usage", {})
            tokens = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            turns = ev.get("num_turns", 0)
    return loaded, tokens, turns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean-dir", required=True); ap.add_argument("--full-dir", required=True)
    ap.add_argument("--settings", required=True); ap.add_argument("--model", default="sonnet")
    ap.add_argument("--json"); ap.add_argument("--arms", default="FULL,LEAN")
    ap.add_argument("--tasks", help="JSON list of [prompt, [accepted skills]]; 'prefix-*' wildcards allowed")
    a = ap.parse_args()
    env = dict(os.environ)
    arms = {"FULL": (a.full_dir, []),
            "LEAN": (a.lean_dir, ["--setting-sources", "project", "--settings", a.settings])}
    arms = {k: v for k, v in arms.items() if k in a.arms.split(",")}
    tasks = [(t, set(ok)) for t, ok in json.load(open(a.tasks))] if a.tasks else TASKS
    rows, tot = [], {k: [0, 0] for k in arms}
    for prompt, ok in tasks:
        row = {"task": prompt[:50]}
        for arm, (cwd, extra) in arms.items():
            loaded, tokens, turns = run(prompt, cwd, extra, a.model, env)
            hit = any(s in ok or any(o.endswith("*") and s.startswith(o[:-1]) for o in ok) for s in loaded)
            tot[arm][0] += hit; tot[arm][1] += tokens
            row[arm] = {"hit": hit, "loaded": loaded[:3], "tokens": tokens, "turns": turns}
        rows.append(row)
        print(f"{row['task']:52} " + " | ".join(f"{k} {'✓' if row[k]['hit'] else '✗'} {row[k]['tokens']:>7} {row[k]['loaded'][:2]}" for k in arms), flush=True)
    for arm, (hits, toks) in tot.items():
        print(f"{arm}: {hits}/{len(tasks)} correct skill, {toks:,} input tokens")
    if a.json:
        json.dump({"model": a.model, "rows": rows, "totals": tot}, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
