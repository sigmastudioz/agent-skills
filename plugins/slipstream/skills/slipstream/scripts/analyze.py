#!/usr/bin/env python3
"""slipstream: measure where tokens actually go across Claude Code and Codex logs.

Usage: python3 analyze.py [--days 30] [--json out.json]
Reads only local log files. Prints aggregate numbers, never message content.
"""
import argparse, json, os, sys, time, glob
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor

HOME = os.path.expanduser("~")


def claude_session(path):
    s = dict(tool="claude", path=path, calls=0, inp=0, cread=0, cwrite=0, out=0,
             first_ctx=None, max_ctx=0, ctx=[], tool_result_chars=0, big_results=0,
             tools=Counter(), sidechain_calls=0, compactions=0, user_turns=0)
    seen = set()
    try:
        with open(path, "rb") as fh:
            for raw in fh:
                if b'"usage"' not in raw and b'tool_result' not in raw and b'compact' not in raw and b'"user"' not in raw:
                    continue
                try:
                    d = json.loads(raw)
                except Exception:
                    continue
                if d.get("type") == "system" and "compact" in str(d.get("subtype", "")):
                    s["compactions"] += 1
                m = d.get("message") or {}
                if d.get("type") == "user":
                    c = m.get("content")
                    if isinstance(c, str):
                        s["user_turns"] += 1
                    elif isinstance(c, list):
                        for b in c:
                            if isinstance(b, dict) and b.get("type") == "tool_result":
                                n = len(json.dumps(b.get("content", "")))
                                s["tool_result_chars"] += n
                                if n > 20000:
                                    s["big_results"] += 1
                            elif isinstance(b, dict) and b.get("type") == "text":
                                s["user_turns"] += 1
                u = m.get("usage")
                if d.get("type") == "assistant" and u:
                    rid = d.get("requestId") or d.get("uuid")
                    for b in m.get("content") or []:
                        if isinstance(b, dict) and b.get("type") == "tool_use":
                            s["tools"][b.get("name", "?")] += 1
                    if rid in seen:
                        continue
                    seen.add(rid)
                    i, cr, cw, o = (u.get("input_tokens", 0) or 0, u.get("cache_read_input_tokens", 0) or 0,
                                    u.get("cache_creation_input_tokens", 0) or 0, u.get("output_tokens", 0) or 0)
                    ctx = i + cr + cw
                    s["calls"] += 1
                    s["inp"] += i; s["cread"] += cr; s["cwrite"] += cw; s["out"] += o
                    if d.get("isSidechain"):
                        s["sidechain_calls"] += 1
                    elif s["first_ctx"] is None:
                        s["first_ctx"] = ctx
                    s["max_ctx"] = max(s["max_ctx"], ctx)
                    s["ctx"].append(ctx)
    except OSError:
        return None
    return s if s["calls"] else None


def codex_session(path):
    s = dict(tool="codex", path=path, calls=0, inp=0, cread=0, cwrite=0, out=0,
             first_ctx=None, max_ctx=0, ctx=[], tool_result_chars=0, big_results=0,
             tools=Counter(), sidechain_calls=0, compactions=0, user_turns=0, subagent=False)
    last_total = None
    try:
        with open(path, "rb") as fh:
            for raw in fh:
                if b'session_meta' in raw and b'parent_thread_id' in raw:
                    s["subagent"] = True
                if b'"compacted"' in raw or b'context_compacted' in raw:
                    s["compactions"] += 1
                if b'function_call_output' in raw or b'custom_tool_call_output' in raw:
                    try:
                        p = json.loads(raw).get("payload", {})
                        n = len(str(p.get("output", "")))
                        s["tool_result_chars"] += n
                        if n > 20000:
                            s["big_results"] += 1
                    except Exception:
                        pass
                    continue
                if b'"type":"function_call"' in raw or b'"type":"custom_tool_call"' in raw:
                    try:
                        s["tools"][json.loads(raw)["payload"].get("name", "?")] += 1
                    except Exception:
                        pass
                    continue
                if b'"user_message"' in raw:
                    s["user_turns"] += 1
                    continue
                if b'"token_count"' not in raw or b'"info":null' in raw:
                    continue
                try:
                    info = json.loads(raw)["payload"]["info"]
                except Exception:
                    continue
                lt, tt = info.get("last_token_usage") or {}, info.get("total_token_usage") or {}
                key = tt.get("total_tokens")
                if key == last_total:
                    continue
                last_total = key
                i = lt.get("input_tokens", 0) or 0
                c = lt.get("cached_input_tokens", 0) or 0
                s["calls"] += 1
                s["inp"] += i - c; s["cread"] += c; s["out"] += lt.get("output_tokens", 0) or 0
                if s["first_ctx"] is None:
                    s["first_ctx"] = i
                s["max_ctx"] = max(s["max_ctx"], i)
                s["ctx"].append(i)
    except OSError:
        return None
    return s if s["calls"] else None


def run(fn, paths):
    with ProcessPoolExecutor() as ex:
        return [r for r in ex.map(fn, paths, chunksize=8) if r]


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else 0


def summarize(sessions, label):
    if not sessions:
        return {"label": label, "sessions": 0}
    ctx_in = sum(s["inp"] + s["cread"] + s["cwrite"] for s in sessions)
    out = sum(s["out"] for s in sessions)
    calls = sum(s["calls"] for s in sessions)
    firsts = [s["first_ctx"] for s in sessions if s["first_ctx"]]
    # Cost of the fixed preamble: first-call context re-sent on every call.
    fixed = sum((s["first_ctx"] or 0) * s["calls"] for s in sessions)
    # Long-tail: share of all input consumed by calls whose context > 150k.
    over = sum(c for s in sessions for c in s["ctx"] if c > 150_000)
    by_len = sorted(sessions, key=lambda s: -(s["inp"] + s["cread"] + s["cwrite"]))
    top10 = sum(s["inp"] + s["cread"] + s["cwrite"] for s in by_len[: max(1, len(by_len) // 10)])
    tools = Counter()
    for s in sessions:
        tools.update(s["tools"])
    return {
        "label": label, "sessions": len(sessions), "model_calls": calls,
        "input_tokens_total": ctx_in, "output_tokens_total": out,
        "input_per_output": round(ctx_in / max(out, 1), 1),
        "cache_read_share": round(sum(s["cread"] for s in sessions) / max(ctx_in, 1), 3),
        "cache_write_tokens": sum(s["cwrite"] for s in sessions),
        "median_first_call_context": pct(firsts, 0.5),
        "p90_first_call_context": pct(firsts, 0.9),
        "fixed_preamble_share": round(fixed / max(ctx_in, 1), 3),
        "calls_over_150k_input_share": round(over / max(ctx_in, 1), 3),
        "median_calls_per_session": pct([s["calls"] for s in sessions], 0.5),
        "p90_calls_per_session": pct([s["calls"] for s in sessions], 0.9),
        "top10pct_sessions_input_share": round(top10 / max(ctx_in, 1), 3),
        "subagent_or_sidechain_calls": sum(s["sidechain_calls"] for s in sessions) + sum(s["calls"] for s in sessions if s.get("subagent")),
        "tool_result_chars_total": sum(s["tool_result_chars"] for s in sessions),
        "tool_results_over_20k_chars": sum(s["big_results"] for s in sessions),
        "compactions": sum(s["compactions"] for s in sessions),
        "top_tools": tools.most_common(10),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=30)
    ap.add_argument("--json")
    a = ap.parse_args()
    cutoff = time.time() - a.days * 86400
    cl = [p for p in glob.glob(f"{HOME}/.claude/projects/*/**/*.jsonl", recursive=True) if os.path.getmtime(p) >= cutoff]
    cx = [p for p in glob.glob(f"{HOME}/.codex/sessions/**/*.jsonl", recursive=True) if os.path.getmtime(p) >= cutoff]
    res = {"days": a.days,
           "claude": summarize(run(claude_session, cl), "Claude Code"),
           "codex": summarize(run(codex_session, cx), "Codex")}
    print(json.dumps(res, indent=1))
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
