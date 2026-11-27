#!/usr/bin/env python3
"""Count skills actually invoked in Claude Code (Skill tool, /slash) and Codex (SKILL.md reads).
Usage: python3 skill_usage.py [--days 30]"""
import argparse, glob, json, os, re, time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
HOME = os.path.expanduser("~")
SK = re.compile(rb'skills/([A-Za-z0-9_.:-]+)/SKILL\.md')
CMD = re.compile(rb'<command-name>/?([A-Za-z0-9_.:-]+)</command-name>')

AG = re.compile(rb'"subagent_type":"([^"]+)"')
MCP = re.compile(rb'"name":"mcp__plugin_([a-z0-9-]+)_')

def claude(p):
    c = Counter()
    for raw in open(p, "rb"):
        if b'"type":"tool_use"' in raw:
            for m in AG.findall(raw): c["agent:" + m.decode()] += 1
            for m in MCP.findall(raw): c["mcp:" + m.decode()] += 1
        if b'"name":"Skill"' in raw:
            try:
                for b in json.loads(raw)["message"]["content"]:
                    if b.get("type") == "tool_use" and b.get("name") == "Skill":
                        c[b["input"].get("skill", "?").split(":")[-1]] += 1
            except Exception:
                pass
        for m in CMD.findall(raw):
            c[m.decode().split(":")[-1]] += 1
    return c

def codex(p):
    c = Counter()
    for raw in open(p, "rb"):
        if b'function_call"' in raw or b'custom_tool_call"' in raw:
            for m in set(SK.findall(raw)):
                c[m.decode()] += 1
    return c

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--days", type=float, default=30); ap.add_argument("--json")
    a = ap.parse_args(); cut = time.time() - a.days * 86400
    cl = [p for p in glob.glob(f"{HOME}/.claude/projects/*/**/*.jsonl", recursive=True) if os.path.getmtime(p) >= cut]
    cx = [p for p in glob.glob(f"{HOME}/.codex/sessions/**/*.jsonl", recursive=True) if os.path.getmtime(p) >= cut]
    with ProcessPoolExecutor() as ex:
        cc = sum(ex.map(claude, cl, chunksize=8), Counter()); xc = sum(ex.map(codex, cx, chunksize=8), Counter())
    tot = cc + xc
    res = {"claude": cc.most_common(), "codex": xc.most_common(), "combined": tot.most_common()}
    if a.json: json.dump(res, open(a.json, "w"), indent=1)
    print(f"distinct skills used: claude {len(cc)}, codex {len(xc)}, combined {len(tot)}")
    for k, v in tot.most_common(60): print(f"{v:6}  {k}")

if __name__ == "__main__": main()
