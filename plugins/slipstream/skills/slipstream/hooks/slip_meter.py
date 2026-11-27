#!/usr/bin/env python3
"""UserPromptSubmit hook: measure live context from the transcript and nudge a handoff.

Never blocks. Silent below the threshold. Above it, once per +STEP band, it tells the agent
the measured size and to offer a handoff at the next task boundary (not mid-task).
Env: SLIPSTREAM_GROWTH (default 100000), SLIPSTREAM_STEP (default 50000)."""
import json, os, sys, tempfile

GROWTH = int(os.environ.get("SLIPSTREAM_GROWTH", 100000))
STEP = int(os.environ.get("SLIPSTREAM_STEP", 50000))


def ctx_of(u):
    return (u.get("input_tokens", 0) or 0) + (u.get("cache_read_input_tokens", 0) or 0) + (u.get("cache_creation_input_tokens", 0) or 0)


def measure(path):
    first = last = 0
    with open(path, "rb") as fh:
        for raw in fh:
            if b'"usage"' not in raw or b'"isSidechain":true' in raw:
                continue
            try:
                d = json.loads(raw)
            except Exception:
                continue
            u = (d.get("message") or {}).get("usage")
            if d.get("type") == "assistant" and u:
                c = ctx_of(u)
                first = first or c
                last = c
    return first, last


def main():
    try:
        ev = json.load(sys.stdin)
        first, last = measure(ev["transcript_path"])
    except Exception:
        return  # a meter must never break the session
    growth = last - first
    if growth < GROWTH:
        return
    band = (growth - GROWTH) // STEP
    state = os.path.join(tempfile.gettempdir(), f"slipstream-{ev.get('session_id', 'x')}")
    try:
        if os.path.exists(state) and int(open(state).read() or -1) >= band:
            return
        open(state, "w").write(str(band))
    except OSError:
        pass
    note = (f"slipstream: this session now re-sends ~{last // 1000}K tokens on every call "
            f"({growth // 1000}K of conversation on top of a {first // 1000}K start). Finish the current step. "
            "At the next task boundary, write a handoff of 40 lines or fewer (goal, decisions and why, files touched, "
            "state, next step, verify command, and 'Skills in use:' with exact skill names so the next session "
            "reloads them) to the project's tracker or HANDOFF.md, and suggest continuing in a "
            "fresh session. If the user's next request is unrelated, suggest a new session first.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": note},
                      "systemMessage": f"slipstream: context ~{last // 1000}K per call. A fresh session with a handoff would be cheaper."}))


if __name__ == "__main__":
    main()
