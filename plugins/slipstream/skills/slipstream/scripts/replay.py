#!/usr/bin/env python3
"""Counterfactual replay: re-price your real call history under leaner habits.

This is a model, not a measurement: it keeps every call you actually made and
recomputes the context each call would have carried if
  (1) the fixed preamble were smaller by --preamble-cut tokens, and/or
  (2) a session were handed off to a fresh one (with a --handoff token note)
      whenever accumulated conversation growth exceeded --cap tokens.
It does not model fewer calls, smarter tool use, or quality effects.
Usage: python3 replay.py [--days 14] [--preamble-cut 41000] [--cap 100000] [--handoff 8000]
"""
import argparse, glob, os, time, json
from analyze import claude_session, codex_session, run, HOME


def reprice(s, cut, cap, handoff):
    first = s["first_ctx"] or (s["ctx"][0] if s["ctx"] else 0)
    base = first - cut if first - cut >= 8000 else first  # never inflate a small preamble
    total, offset = 0, 0
    for c in s["ctx"]:
        raw = max(c - first, 0)
        growth = raw - offset
        if offset and growth < handoff:  # the real session compacted/shrank below our replay
            offset = max(raw - handoff, 0)
            growth = raw - offset
        if cap and growth > cap:
            offset += growth - handoff  # fresh session: keep only the handoff note + re-reads
            growth = handoff
        total += base + growth if c >= first else max(c - (first - base), 0)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=14)
    ap.add_argument("--preamble-cut", type=int, default=41000)
    ap.add_argument("--cap", type=int, default=100000)
    ap.add_argument("--handoff", type=int, default=8000)
    a = ap.parse_args()
    cut = time.time() - a.days * 86400
    sets = {
        "claude": run(claude_session, [p for p in glob.glob(f"{HOME}/.claude/projects/*/**/*.jsonl", recursive=True) if os.path.getmtime(p) >= cut]),
        "codex": run(codex_session, [p for p in glob.glob(f"{HOME}/.codex/sessions/**/*.jsonl", recursive=True) if os.path.getmtime(p) >= cut]),
    }
    out = {}
    for name, ss in sets.items():
        actual = sum(sum(s["ctx"]) for s in ss)
        identity = sum(reprice(s, 0, 0, 0) for s in ss)
        assert identity == actual, f"replay identity broken for {name}: {identity} != {actual}"
        pc = 0 if name == "codex" else a.preamble_cut  # preamble A/B was measured for Claude only
        rows = {
            "actual": actual,
            "preamble_only": sum(reprice(s, pc, 0, 0) for s in ss),
            "cap_only": sum(reprice(s, 0, a.cap, a.handoff) for s in ss),
            "both": sum(reprice(s, pc, a.cap, a.handoff) for s in ss),
        }
        out[name] = {k: {"tokens_B": round(v / 1e9, 2), "saved_pct": round(100 * (1 - v / max(actual, 1)), 1)} for k, v in rows.items()}
    print(json.dumps({"params": vars(a), **out}, indent=1))


if __name__ == "__main__":
    main()
