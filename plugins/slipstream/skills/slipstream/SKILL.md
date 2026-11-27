---
name: slipstream
description: Cut token burn in Claude Code, Codex or Cursor by shrinking per-call context, not output, without losing skills. Use when usage limits hit, sessions get long, or the user asks to save tokens or audit usage.
---

# Slipstream
*S.L.I.P. — Skills Loaded In Precisely. Go further on less fuel.*
By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

**Law:** total tokens ≈ Σ over calls of (preamble + conversation so far). Output is a rounding
error (under 0.3% of input in the publisher's measured Claude Code and Codex logs), so terse-output tricks optimize the
wrong term. Lower the **base** (what loads before the first word), the **growth** (what each call
adds) and the **count** of calls made at high context, while keeping every capability reachable.

## 0. Before first use: check what the tools need

The plugin ships only its own scripts. It bundles no runtime or package and downloads nothing.
Before running any script, check once per machine:

```bash
python3 --version   # needs 3.9+; scripts use the standard library only
bash --version      # only for scripts/wait_for.sh
```

If one is missing or too old, tell the user what is missing, which features need it, and the
install command for their system. Install only after they say yes; never install silently.

| System | Python 3 | bash |
|---|---|---|
| macOS | `brew install python` (or python.org installer) | built in |
| Windows | `winget install Python.Python.3.12` | use WSL or Git Bash; hooks and `wait_for.sh` need it |
| Debian/Ubuntu | `sudo apt install python3` | built in |
| Fedora | `sudo dnf install python3` | built in |

If the user declines, continue in **guidance-only mode**: apply sections 3 and 4 by hand and
explain section 2's lean-listing method. Say plainly that the measurements, the lean setup
and the hooks need Python, so the measured savings will not apply.

## 1. Measure (scripts/, read-only)

| Script | Answers |
|---|---|
| `analyze.py --days 14` | Where input goes: input:output, first-call context, long-session share, polling |
| `skill_usage.py --days 30` | Which skills, agents and MCP plugins were actually used |
| `preamble.py` | What loads before the first word, biggest first |
| `replay.py --days 14` | Modelled saving of a smaller base + session handoffs (identity-checked) |
| `discovery_ab.py` | Whether a fresh agent still finds the right skill in a lean layout (live, costs tokens) |
| `mine_pairs.py` + `eval_rolling.py` | Replays real history: is every skill you used still listed or hinted? (free) |
| `eval_hint.py --before DATE` | Hint recall and noise on a time split: learn from older, test on newer (free) |
| `analyze_cursor_csv.py` | Cursor usage from the account's CSV export (Cursor keeps no real usage locally) |
Real preamble: `claude -p "Reply OK" --output-format json`, then sum the usage fields.

## 2. Base: lean listing, nothing lost

`scripts/lean_setup.py` (dry run by default; `--apply`; exact `--undo` from a manifest):
- **Core listing** = skills used at least once in 30 days (listing is cheap: 141 skills measured
  +2K tokens, because the app truncates descriptions), plus any named in CLAUDE.md/AGENTS.md, plus
  every skill those skills reference by name (process skills are reached by chaining, not
  by prompt words), plus xlsx/docx/pptx/pdf. The rest move (never delete) to
  `~/.claude/skill-library/archive/`.
- **New skills are safe:** a skill installed in the last 30 days (`--grace`) always stays listed;
  usage decides only after that. Installing a skill or enabling a plugin triggers a catalog
  rebuild at the next session start.
- **Self-correcting:** `--refresh` runs weekly (SessionStart hook, in the background): an archived
  skill used in the last 30 days is promoted back, idle ones are archived, triggers are relearned.
- **Catalog** (`build_catalog.py`): one line per installed skill (personal, archived, enabled and account-synced
  plugins; never uninstalled marketplace content). Costs nothing until searched.
- **Skill hint hook** (`hooks/slip_hint.py`, ~0.2 s): matches the user's own words (no pasted
  blocks, summaries or machine notifications) against the catalog and injects one line with the
  SKILL.md path when it finds an exact skill name, a named skill ("the social media skill"), a
  word unique to one skill name ("kerberoasting"), most of a skill's name, or a trigger word learned from
  the user's own history. The model no longer has to remember to search. The `skill-library` router skill remains
  for manual search (`find_skill.py "task words"`).
- **Plugins:** disables only pure-content plugins (skills/agents/commands) with zero recorded
  use. Never touches plugins that ship hooks, output styles, MCP or LSP. Desktop-synced plugins
  are managed in the claude.ai account, not settings.json.

## 3. Growth: small additions per call (agent rules)

- Bound reads: search before reading, read line ranges, `head`/`tail`/`wc -l`/`--stat`; never
  dump logs, lockfiles, minified or generated files. Don't re-read unchanged files.
- Wide exploration goes to a subagent; only its conclusion enters the main context.
- Browser: page text or accessibility tree before screenshots.
- A knowledge graph (`graphify query`) is optional. Use it when one exists.

## 4. Count: fewer calls at high context

- **Context meter** (`hooks/slip_meter.py`): silent until conversation growth passes ~100K,
  then once per +50K it gives the measured size and asks for a handoff **at the next task
  boundary**, never mid-step. Handoff: ≤40 lines (goal, decisions and why, files touched, state,
  next step, verify command) to the project tracker or HANDOFF.md, then a fresh session.
- **No polling:** `hooks/slip_guard.py` denies a bare `sleep N` step; wait inside one call
  with `scripts/wait_for.sh --timeout 900 --every 15 -- <check>` or a background job that
  notifies on completion. In-command loops (`until …; do sleep; done`) are allowed.
- Batch independent tool calls; match model and effort to the task.

## Cross-tool

- **Codex:** `lean_setup.py` installs the router and this skill into `~/.codex/skills` and
  appends a 3-line rule block to `AGENTS.md` (wait_for.sh, thread handoff, catalog search).
- **Cursor:** no local token logs. Same rules: new chat per task, @-mention files instead of the
  codebase, trim rules and MCP servers.

## Limits (and what covers each)

- First-ever use of a skill phrased with no shared words: ~2% of real uses in replay. In a live
  run on exactly those requests, the lean setup chose correctly 3/3 (router skill + listing).
- Bare follow-ups ("yes, draft them") are never hinted; the skill is chosen from conversation.
- Hints fire on ~12% of no-skill messages (~100 tokens each); the model may ignore them.
- Session savings are a replay on real calls; handoff cost (14K median, 19K p90) is measured.
- Desktop plugins synced from claude.ai stay listed regardless of settings.json (the idle 14
  cost ~11.5K tokens per call plus 134 connectors); the installer names them, the user turns
  them off in their claude.ai account.
- Cursor keeps no usage locally (editor and CLI stores checked); parse the account CSV export.
  Its two input columns are disjoint ("w/o Cache Write" = input, "w/ Cache Write" = cache write).
- Cache reads are cheaper per token but still count toward plan limits. Never change the user's
  configuration without consent.
