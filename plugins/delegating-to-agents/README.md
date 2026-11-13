# Delegating to Agents

Adapted by **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** from
[davidondrej/skills](https://github.com/davidondrej/skills) · MIT · version 1.0.0.

Hand bounded work to another AI agent CLI or TUI (Codex, Cursor, Pi, Claude Code, Hermes) and
keep control of it: a complete brief, an isolated git worktree when others have uncommitted
work, progress lines you can watch as events, `BLOCKED` questions forwarded to whoever owns the
decision, and results reviewed before they are reported back up the chain.

What a brief must contain comes from the
[domain-driven-design handoff guide](../domain-driven-design/skills/domain-driven-design/references/handoffs.md);
this skill covers the mechanics of driving each agent.

## Changes in 1.0.0

First release in this collection. Adds Cursor agent CLI usage, sandboxed modes instead of
run-everything flags, worktree isolation, a progress-file and monitor pattern, and reporting
back to the delegating agent. Personal account details from the earlier local copy were removed.

## Install

`npx skills add sigmastudioz/agent-skills --skill delegating-to-agents`

Guidance only: no executable helper or required service. Driving another agent runs commands
on your machine; the skill asks for approval before commands, remote access or file changes.
