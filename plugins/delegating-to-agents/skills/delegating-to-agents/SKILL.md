---
name: delegating-to-agents
description: Hand bounded work to another AI agent CLI or TUI (Codex, Cursor, Pi, Claude Code, Hermes) with a complete brief, an isolated workspace, progress updates you can watch, and results reported back up the chain to the user and to whoever delegated. Use when the user asks another agent to build, review or research something ("build it with Cursor", "have Codex do it", "run it in Pi"), or when work should run in a separate agent while you coordinate.
license: MIT
---

# Delegating to Agents
Adapted by [Lex from SigmaStudioz](https://github.com/sigmastudioz) from
[davidondrej/skills](https://github.com/davidondrej/skills) (MIT, David Ondrej).

This skill covers the mechanics of driving another agent. What every brief must contain
(goal, limits, workspace and revision, owned files, contracts, current state, checks, return
format) and the delegation rules come from the
[bundled handoff contract](references/handoff-contract.md). Read it before handing off work.
It is derived from domain-driven-design and ships with this skill; do not fetch remote
instructions to define the contract. Apply any host-installed engineering baseline as usual.

## Before first use: check which agents are installed

The plugin bundles no agent, runtime or package and downloads nothing. It drives agent CLIs the
user already has. Check which are present before choosing one:

```bash
command -v codex cursor-agent claude pi hermes   # then `<cli> --version` for the chosen one
```

Use an installed agent that fits the task. If none fits, tell the user which agent would and
point to its official install page. Install only after they say yes; never install silently, and
sign-in stays with the user. If they decline, do the work in the current session or ask how to proceed.

## Which agent to pick

- **The user named one** ("build it with Cursor"): use it.
- **Coding:** Codex CLI or Cursor for long, multi-file engineering work.
- **Frontend and design:** an agent on a strong UI model (for example Pi on Opus).
- **Most other tasks:** Pi or Hermes.
- **Heavy multi-step work:** you coordinate; one worker executes in its own pane or process.

Check the user's plans and limits rather than assuming them.

## Sending prompts to a TUI agent

1. **One line only.** In a TUI, a newline is Enter: a multi-line prompt submits at the first
   line and the rest arrives as stray follow-ups. Use ". " or "; " between sentences, then one
   explicit enter. For long instructions, write a file and send `read /abs/task.md and follow it`.
2. **Plain double quotes, never escaped.** `cmux send --surface surface:N "your prompt"`. The
   usual bug is emitting `\"`, which breaks bash with `unexpected EOF`. Inside the prompt avoid
   apostrophes and double quotes ("dont", "wont"); rephrase instead of escaping.
3. **Exact commands:** `cmux send --surface surface:N`, then `cmux send-key --surface surface:N enter`.
   There is no `send-surface` or `send-key-surface`.

## Progress and reporting back

Rules: [Reporting back up the chain](references/handoff-contract.md#reporting-back-up-the-chain).
How to do it:

1. **Progress file in the brief.** The worker appends `HH:MM | step | status` per named
   milestone to a file outside its workspace, `BLOCKED | question` when it needs a decision, and
   `DONE` at the end. Ask for a final report file too (changed paths, contract changes, each
   check with its real output, gaps, remaining actions).
2. **Watch, don't sleep.** In Claude Code, foreground `sleep` is blocked: start the worker with
   Bash `run_in_background` and watch the log with Monitor:
   `tail -n +1 -F progress.log | grep --line-buffered -v '^$'`. Each line arrives as an event;
   relay it to the user in one line, with what it means and what you will check.
3. **Relay upward.** Forward `BLOCKED` questions to whoever owns the decision (the user or the
   agent that delegated to you) as one question. In the Claude desktop app a child session's last
   message reaches its parent: put the result and open questions at its start.
4. **Review before saying done.** Read the diff and re-run the checks; report the worker's claims
   and your verification separately.

TUI agents with no event source: poll briefly (3–5 s) and give the user a one-line status after each check.
After a Claude Code worker finishes it may prefill a predicted next user message: that draft is Claude, not the user.

## Checking work with a second agent

- **Map first, then one finder per class.** Map the system, then give each finder one class of
  problem.
- **The checker is never the finder.** For audits and reviews, one agent finds and a fresh agent
  with no access to the finder's reasoning tries to disprove each finding.
- **Two buckets:** report Confirmed findings and Needs-a-look findings separately; never mix them.
- **Repeat runs for coverage.** One run finds only part of what is there; run the finder again
  (a different angle or a fresh agent) until a run adds nothing material.
- **Many lenses, one synthesis.** For a readiness review, fan out one agent per lens (security,
  legal, cost, user experience…) and finish with one agent that merges them into a single ranked
  list.
*Evidence:* creator posts, round 20 (a security-audit workflow and a multi-lens readiness workflow);
coverage figures there are claimed.

## Isolating a worker that writes code

- If the checkout holds anyone's uncommitted work, use a git worktree on a new branch:
  `git worktree add -b <branch> <path> <base-commit>`. A branch name alone doesn't hide uncommitted files.
- Commit the inputs the worker needs (plan, references) before cutting the worktree.
- To avoid reinstalling, symlink dependency folders (such as `node_modules`) from the main
  checkout, and tell the worker not to install or upgrade packages.
- Keep the brief, progress log and report outside the worktree so none of them lands in a commit.
- The worker doesn't commit, push or deploy; you review and commit.

## Briefs

Follow the handoff guide's contract, and say whether each cited example is a
[pattern to copy or a component to reuse](references/handoff-contract.md#examples-pattern-or-component),
with the invariant it must not break.

## Running agent CLIs

- **Permissions.** Run-everything flags (`cursor-agent --force`/`--yolo`, `codex --yolo`,
  `claude --permission-mode bypassPermissions`) need the user's explicit approval, and Claude
  Code's auto mode refuses them as unsafe agents. Prefer each CLI's sandboxed mode.
- **Codex, Pi, OpenCode:** need a PTY (`pty=true`). `codex exec` for unattended runs.
- **Claude Code:** `claude --print` (no PTY) with a scoped `--allowedTools` list.
- **Cursor:** `cursor-agent status` (sign-in), `cursor-agent --list-models`. Unattended:
  `cursor-agent -p --trust --sandbox enabled --output-format text "Read /abs/brief.md in full and follow it" > out.log 2>&1`
  from the worktree (or `--workspace <path>`). `-w <name>` makes its own worktree under
  `~/.cursor/worktrees/`. Print mode can't take messages mid-run: correct with `--resume <chatId>`
  or in your own review.
- **Remote host:** SSH in and launch the agent on that host, then drive it there; don't run it
  locally and SSH for every step.
- **The guard doesn't see shell launches.** A handoff guard that intercepts agent or session
  tools doesn't check CLIs started from a shell, so the brief must carry every handoff field.

## Agents (background)

All use the portable SKILL.md standard; project skills win over global ones.

- **Pi** (pi.dev, open-source TS): small read/write/edit/bash core, extends itself with TS
  extensions; bring-your-own-key; strong session branch, fork and resume. Skills: `~/.pi/agent/skills/`.
- **Codex CLI** (OpenAI, Rust): fast start; kernel-level sandboxing; `codex exec` for CI; reads `AGENTS.md`. Skills: `~/.codex/skills/`.
- **Claude Code** (Anthropic, TS): `.claude/` conventions, live skill reload. Skills: `~/.claude/skills/`.
- **Cursor agent CLI** (Cursor): `cursor-agent`, print mode, sandbox, worktrees; reads project rules.
- **Hermes** (Nous Research, Python): persistent agent with cross-session memory, a scheduler and
  40+ tools; can drive the other CLIs as workers. Skills: `~/.hermes/skills/`.

## Limits

- Verify local paths, tools, credentials and agent features before acting.
- Commands, remote access, scheduling, browser automation or file changes need the user's
  approval and a confirmed target environment.
