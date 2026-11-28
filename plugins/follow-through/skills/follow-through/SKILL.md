---
name: follow-through
description: Stop coding agents losing unfinished work. Keeps every task the user gives on a task tree saved on disk, so unfinished work survives pivots, side requests, branching and context compaction. Use whenever a request has more than one step, when the user changes topic mid-task, when work is routed into buckets or queues (links to watch, files to review, follow-ups), and at the start of a resumed or compacted session. A task closes only with evidence that its done-when check passed; a parent cannot close while a child is open.
license: MIT
---

# Follow-Through
Regression checks: `tests/test_follow_through.py` in the source repository.
By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

The conversation is not the record. Summaries drop details, plans get replaced on every pivot, and
"sorted into a bucket" gets mistaken for "done". This skill keeps the record in a file, and optional
hooks read it back at the moments context is lost. What it guarantees is **visibility**: unfinished
work keeps coming back into view until it is closed with evidence or the user drops it. It does not
force an agent to do the work, and evidence is the agent's own statement, so the user stays the judge.

## Before first use
The skill ships one standard-library script and bundles no runtime. Check once per machine:

```bash
python3 --version   # needs 3.8+ (Windows: py -3 --version)
```

If Python is missing or too old, tell the user, say that the script and hooks need it, and give the
install command for their system (macOS `brew install python`, Windows `winget install Python.Python.3.12`,
Debian/Ubuntu `sudo apt install python3`). Install only after they say yes; never install silently.
Without Python, follow the rules below by hand in a `TASKS.md` kept outside the repository.

Script: [follow_through.py](scripts/follow_through.py) (Python 3.8+, standard library only, no network).
Store: one JSON file per project in `~/.follow-through/`, named after the project folder plus a short hash
of its full path. The project is `CLAUDE_PROJECT_DIR` when set, else the enclosing git root, else the current
folder, so subfolders share their project's tree. Override with `FOLLOW_THROUGH_HOME`, or
`FOLLOW_THROUGH_FILE` for one exact file. It lives outside the repository, so it is never committed.

```
follow_through.py add "title" --done-when "observable check" [--parent ID]
follow_through.py start ID
follow_through.py park ID --resume "the exact next step"
follow_through.py block ID --on "what it waits for (usually the user's answer)"
follow_through.py close ID --evidence "what shows the check passed"
follow_through.py drop ID --reason "the user's words"
follow_through.py reopen ID
follow_through.py status [--all]
```

## Rules
1. **Every request with more than one step goes on the tree before work starts.** One node per thing the
   user asked for; children for its parts. The done-when check is observable: "all 18 posts watched,
   notes saved, media deleted", not "look at the links".
2. **Routing is not finishing.** When work is sorted into buckets (links to watch, files to review), each
   bucket that still needs action gets its own child node. The parent stays open until those close.
3. **A pivot parks, it never replaces.** When the user asks for something else mid-task, `park` the active
   node with the exact next step, then `add` and `start` the new one. Return to parked work, or report it.
4. **Close with evidence.** Name the file, count, command output or user reply that shows the check passed.
   A file that exists or a command that exited 0 is not evidence by itself; read the result back.
5. **Only the user drops work.** `drop` records the user's words. An agent does not decide a task no longer
   matters; if it seems obsolete, ask.
6. **Waiting on the user is `block`, not done.** Asked a question? Block the node on it; `start` it again
   when the answer comes.
7. **Report the open tree** in one or two lines when a turn ends with nodes still open.
8. **Keep it proportionate.** A one-step request or a question needs no node.

## Hooks (Claude Code, optional, installed by the owner)
Hooks change the host's settings, so the owner installs them; the agent does not add them on its own.
Merge these into `~/.claude/settings.json`, keeping existing hooks, with the script's installed path:

```json
{"hooks": {
  "SessionStart":     [{"hooks": [{"type": "command", "timeout": 5, "command": "python3 -I \"/path/to/follow_through.py\" hook-session"}]}],
  "UserPromptSubmit": [{"hooks": [{"type": "command", "timeout": 5, "command": "python3 -I \"/path/to/follow_through.py\" hook-prompt"}]}],
  "Stop":             [{"hooks": [{"type": "command", "timeout": 5, "command": "python3 -I \"/path/to/follow_through.py\" hook-stop"}]}]
}}
```

| Hook | Effect |
| --- | --- |
| SessionStart (startup, resume, compact) | Injects the open tree (capped at 60 lines) so a fresh or compacted context sees unfinished work |
| UserPromptSubmit | One line naming the open tasks, with a reminder to park before a pivot; also records which session is talking (in one shared `sessions.json`) |
| Stop | Sends the agent back once per turn while a task it started is still `active` |

All three print nothing when the tree is empty. The Stop hook honours `stop_hook_active`, so it never
loops, and only counts tasks started in the current session. Task text is flattened to one line, capped at
200 characters and labelled as data, so a pasted caption cannot pose as tree lines or instructions. Hooks
never create a tree file. On any error (unreadable store, lock held)
a hook writes one line to stderr and lets the session continue. On Windows use `py -3` in place of `python3`.

Other hosts (Cursor, Codex, any agent with a shell): use the script and the rules without hooks, and run
`status` at the start of each session.

## Limits
- The tree remembers only what was added to it. A task never added is still lost: rule 1 is the defence.
- One tree per project. Two sessions in the same project share it; a task belongs to the session that last
  sent a prompt when it was started, so in rare interleavings the Stop hook can name the other session's task.
- The Stop hook only checks `active` tasks. Parked and blocked work is shown on every prompt and at every
  session start, but nothing stops an agent from leaving it parked: the user sees it and decides.
- Closed tasks stay in the file as history. Very large trees (thousands of nodes) slow the hooks; move the
  file aside to start fresh.
- The policy for closing lives in one function, `can_close`; change it there.
