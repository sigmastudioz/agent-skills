#!/usr/bin/env python3
"""PreToolUse(Bash) hook: stop model-driven polling. A bare `sleep N` (N >= 5) as its own
step means the next call re-sends the whole context just to check again. Deny it and point
to wait_for.sh, which does the waiting inside the shell in one call. Loops that wait inside a
single command (until ...; do sleep; done) are allowed: they cost one call."""
import json, re, sys

BARE = re.compile(r"^\s*(?:sleep\s+(\d+(?:\.\d+)?)\s*[smh]?)\s*(?:(?:&&|;)\s*(.+))?$", re.S)


def main():
    try:
        ev = json.load(sys.stdin)
        cmd = ev.get("tool_input", {}).get("command", "")
    except Exception:
        return
    if re.search(r"\b(until|while)\b", cmd):
        return
    m = BARE.match(cmd)
    if not m or float(m.group(1)) < 5:
        return
    reason = ("slipstream: polling with sleep re-sends the entire conversation on every check. Wait inside the shell "
              "in ONE call instead: `wait_for.sh --timeout 900 --every 15 -- <command that succeeds when ready>`, "
              "or run the job in the background and wait for its completion notification.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))


if __name__ == "__main__":
    main()
