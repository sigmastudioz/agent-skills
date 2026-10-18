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

The helper checks coding handoffs in recognized code workspaces, rejects missing context, and
places the complete baseline before accepted worker prompts. It also checks explicit
`Use N teammates/agents/workers` limits against native user turns and pending dispatches, excludes
hook-rejected attempts, and permits resuming an existing worker. Missing history or other wording
leaves budget enforcement to the coordinator. It preserves other tool arguments and
native permission decisions. It cannot prove that the assignment is true or that the worker follows
every instruction. Review worker results and verify integrated behavior.

Start fresh sessions after setup. Test an ordinary coding request without the skill name and inspect
loading, actual handoffs, changed paths, checks and limits. Do not substitute metadata validation for
a real coding test or claim that a local setup automatically installs on cloud agents.

References: [Claude imports](https://code.claude.com/docs/en/memory),
[Claude hooks](https://code.claude.com/docs/en/hooks),
[Cursor skills](https://cursor.com/docs/skills),
[Cursor local plugins](https://cursor.com/docs/plugins#test-plugins-locally),
[Codex skills](https://developers.openai.com/codex/skills).
