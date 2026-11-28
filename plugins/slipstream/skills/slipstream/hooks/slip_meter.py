#!/usr/bin/env python3
"""UserPromptSubmit hook: measure live context from the transcript and nudge a handoff.

Never blocks. Silent below the threshold. Above it, once per +STEP band, it tells the agent
the measured size and to hand off at the next task boundary (never mid-step). The handoff
route follows the app the session runs in (read from the transcript): the desktop app gets
a one-click fresh-session card, the terminal gets the /clear step, anything else a file.
Env: SLIPSTREAM_GROWTH (default 100000), SLIPSTREAM_STEP (default 50000)."""
import json, os, sys, tempfile

GROWTH = int(os.environ.get("SLIPSTREAM_GROWTH", 100000))
STEP = int(os.environ.get("SLIPSTREAM_STEP", 50000))


def ctx_of(u):
    return (u.get("input_tokens", 0) or 0) + (u.get("cache_read_input_tokens", 0) or 0) + (u.get("cache_creation_input_tokens", 0) or 0)


def measure(path):
    first = last = 0
    app = None
    epoch = 0  # compactions seen: a call whose context drops 30%+ below the previous one
    with open(path, "rb") as fh:
        for raw in fh:
            if app is None and b'"entrypoint"' in raw:
                try:
                    app = json.loads(raw).get("entrypoint")
                except Exception:
                    pass
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
                if last and c < 0.7 * last:
                    epoch += 1
                last = c
    return first, last, app, epoch


WRITE = ("Finish the current step. At the next task boundary (never mid-step), write a handoff of 40 lines "
         "or fewer (goal, decisions and why, files touched, state, next step, verify command, and 'Skills in use:' "
         "with exact skill names so the next session reloads them) to the project's tracker or HANDOFF.md. ")


def route(app, first, last):
    """How the user continues fresh: the step this app can actually take."""
    if app == "claude-desktop":
        return ("Then, in the same turn, offer the fresh session as one click: call the app's start-session tool "
                "(mcp__ccd_session__start_session; load it with ToolSearch first if it is deferred) with initiation "
                "\"own_initiative\", context \"fresh\", a short title, and a brief that names the handoff file and "
                "contains its text. Do not start it yourself. Tell the user in one line that the card continues "
                f"the work at about {first // 1000}K per call instead of {last // 1000}K, and that ignoring it keeps "
                "this session going. ")
    if app == "cli":
        return ("Then tell the user, in one line, to run /clear and type 'continue from <handoff path>': the next "
                f"call starts near {first // 1000}K instead of {last // 1000}K. ")
    return "Then suggest continuing in a fresh session that starts from the handoff file. "


def main():
    try:
        ev = json.load(sys.stdin)
        first, last, app, epoch = measure(ev["transcript_path"])
    except Exception:
        return  # a meter must never break the session
    growth = last - first
    if growth < GROWTH:
        return
    band = (growth - GROWTH) // STEP
    state = os.path.join(tempfile.gettempdir(), f"slipstream-{ev.get('session_id', 'x')}")
    try:
        seen = open(state).read().split() if os.path.exists(state) else []
        if len(seen) == 2 and int(seen[0]) == epoch and int(seen[1]) >= band:
            return  # already nudged at this size since the last compaction
        open(state, "w").write(f"{epoch} {band}")
    except OSError:
        pass
    note = (f"slipstream: this session now re-sends ~{last // 1000}K tokens on every call "
            f"({growth // 1000}K of conversation on top of a {first // 1000}K start). " + WRITE + route(app, first, last)
            + "If the user's next request is unrelated, suggest a new session first.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": note},
                      "systemMessage": f"slipstream: context ~{last // 1000}K per call. A fresh session with a handoff would be cheaper."}))


if __name__ == "__main__":
    main()
