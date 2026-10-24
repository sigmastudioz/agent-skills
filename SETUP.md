# Automatic baseline setup

By Lex from SigmaStudioz.

A one-time user-approved global setup is separate from routine skill discovery. The instructions
below are for the user's own execution host. Resolve the actual home/install paths on that host;
remote/cloud agents need their own installation. Preserve existing instruction files and hooks.

## Choose the execution surface

The plugin's skill is `plugins/domain-driven-design/skills/domain-driven-design/` in this checkout.
Each host can discover a native skill in its user skills directory:

- Codex: `~/.codex/skills/domain-driven-design/`.
- Claude Code: `~/.claude/skills/domain-driven-design/`.
- Cursor: `~/.cursor/skills/domain-driven-design/`.

For one installation serving all three, use `~/.agents/skills/domain-driven-design/` as the canonical
folder and native aliases pointing there where supported. Inspect any existing destination before
installing; preserve its local changes instead of replacing it blindly. Keep distribution snapshots
separate from this maintained canonical copy. Preserve the plugin LICENSE alongside copied skill
folders or in their parent distribution directory when installing manually.

## Route ordinary coding tasks automatically

Resolve the canonical skill's absolute SKILL.md path. Add a managed global instruction block that
says to read/apply it before planning/editing production code; keep explicit task scope, read-only
reviews and small fixes proportional. Include baseline context, ownership, trace obligations and
return evidence in already-authorized teammate assignments. No routine trigger phrase is required.

Use each host's supported global surface:

- Codex: `~/.codex/AGENTS.md`; the bundled skill metadata keeps implicit invocation enabled.
- Claude Code: `~/.claude/CLAUDE.md`; import the baseline with `@/absolute/path/to/SKILL.md`.
- Cursor: a global `.mdc` rule with `alwaysApply: true`, pointing at the absolute skill path.

Do not copy paths from the publisher's machine. Merge with existing instructions and preserve a
backup. Host-managed settings or disabled user instructions can limit application.

## Optional Claude handoff guard

Requires Python 3 and a complete skill directory. Merge this hook into existing Claude settings;
do not replace the settings file or its unrelated hooks. This shell example uses a POSIX host and
a canonical installation under the user's own home; adapt the interpreter/path on other systems.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Task|Agent",
      "hooks": [{
        "type": "command",
        "command": "python3 \"$HOME/.agents/skills/domain-driven-design/scripts/guard_handoff.py\"",
        "timeout": 5
      }]
    }]
  }
}
```

The helper checks coding handoffs in recognized code workspaces, rejects malformed or missing
context, and adds a compact reminder to read the installed baseline and relevant linked guidance.
It does not embed the full skill in every worker prompt. Explicit numeric or supported word-form
agent limits are cumulative within a budget; repeated or changed limits retain prior usage. Only
an explicit `Start a new delegation budget: use N agents` instruction resets it. Quoted, fenced or
negated examples cannot increase the cap. Hook-rejected attempts do not consume a slot; resuming
an existing worker does not allocate another. The host must validate resumed agent identities.

A handoff into a different workspace must include an `isolation` object with `confirmed: true`,
the matching absolute `workspace`, and a nonblank `reason`. Verify the actual checkout and its
authority before making that declaration. Missing history, unsupported wording, permissions and
semantic correctness remain coordinator responsibilities. The guard preserves other tool arguments
and native permission decisions. Run the packaged regressions with:

```sh
python3 -B plugins/domain-driven-design/skills/domain-driven-design/scripts/test_guard_handoff.py
```

Start fresh sessions after setup. Test an ordinary coding request without the skill name and inspect
loading, actual handoffs, changed paths, checks and limits. Do not substitute metadata validation for
a real coding test or claim that a local setup automatically installs on cloud agents.

References: [Claude imports](https://code.claude.com/docs/en/memory),
[Claude hooks](https://code.claude.com/docs/en/hooks),
[Cursor skills](https://cursor.com/docs/skills),
[Cursor local plugins](https://cursor.com/docs/plugins#test-plugins-locally),
[Codex skills](https://developers.openai.com/codex/skills).

## Project continuity

The skill discovers `.principal-ddd/index.md` at the owning repository root. That index links the
project's established tracker or the DDD-owned `.principal-ddd/gap-trace.md`; it does not replace
other task systems. Create records only when current work needs them. Existing projects use the
packaged [migration guidance](plugins/domain-driven-design/skills/domain-driven-design/references/project-records.md)
to preserve active writers, relative links, heading anchors and rollback. A hidden folder provides
organization, not privacy or automatic build exclusion.
