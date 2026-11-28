#!/usr/bin/env python3
"""Read-only: did long sessions actually hand off after the context meter nudged them?

For every Claude Code session in the window that received the slipstream meter nudge, report
whether the agent wrote a handoff file, offered a fresh-session card, and whether a fresh
session started from a handoff; plus how many calls and how much context the old session kept
re-sending after the nudge (the cost of not handing off).
Usage: handoff_report.py [--days 7] [--root ~/.claude/projects]"""
import argparse, glob, json, os, re, time

NUDGE = b"slipstream: this session now re-sends"
HANDOFF_FILE = re.compile(r"handoff[^/]*\.md$", re.I)
# How a session that continues from a handoff begins: the desktop card's brief, or the terminal step.
FROM_HANDOFF = re.compile(r"^\s*(Background \(from the session|continue from \S*handoff)", re.I)


def ctx_of(u):
    return sum((u.get(k, 0) or 0) for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))


def scan(path):
    """One session: nudge position, follow-through and the cost after the nudge."""
    s = {"nudged": False, "wrote": False, "card": False, "after_calls": 0, "after_tokens": 0, "peak": 0,
         "first_prompt": None}
    with open(path, "rb") as fh:
        for raw in fh:
            try:
                d = json.loads(raw)
            except Exception:
                continue
            if d.get("isSidechain"):
                continue
            m = d.get("message") or {}
            if d.get("type") == "user" and s["first_prompt"] is None and isinstance(m.get("content"), str):
                s["first_prompt"] = m["content"][:2000]
            if NUDGE in raw:
                s["nudged"] = True
            if not s["nudged"] or d.get("type") != "assistant":
                continue
            u = m.get("usage")
            if u:
                c = ctx_of(u)
                s["after_calls"] += 1
                s["after_tokens"] += c
                s["peak"] = max(s["peak"], c)
            for b in m.get("content") or []:
                if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                    continue
                inp = b.get("input") or {}
                if b.get("name") in ("Write", "Edit") and HANDOFF_FILE.search(inp.get("file_path", "")):
                    s["wrote"] = True
                if b.get("name", "").endswith("start_session") or b.get("name", "").endswith("hand_off_to_session"):
                    s["card"] = True
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--root", default=os.path.expanduser("~/.claude/projects"))
    a = ap.parse_args()
    cut = time.time() - a.days * 86400
    sessions = [scan(p) for p in glob.glob(os.path.join(a.root, "*", "*.jsonl")) if os.path.getmtime(p) >= cut]
    nudged = [s for s in sessions if s["nudged"]]
    resumed = sum(1 for s in sessions if s["first_prompt"] and FROM_HANDOFF.search(s["first_prompt"]))
    print(f"{len(sessions)} sessions in {a.days:g} days; {len(nudged)} reached the handoff threshold")
    if not nudged:
        return
    n = len(nudged)
    print(f"  handoff file written:      {sum(s['wrote'] for s in nudged)}/{n}")
    print(f"  fresh-session card shown:  {sum(s['card'] for s in nudged)}/{n}")
    print(f"  sessions started from a card or handoff: {resumed}")
    calls = sum(s["after_calls"] for s in nudged)
    tok = sum(s["after_tokens"] for s in nudged)
    print(f"  kept going after the nudge: {calls} calls re-sending {tok / 1e6:.1f}M tokens "
          f"(peak {max(s['peak'] for s in nudged) // 1000}K per call)")


if __name__ == "__main__":
    main()
