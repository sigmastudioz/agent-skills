# SigmaStudioz Agent Skills

**By [Lex from SigmaStudioz](https://github.com/sigmastudioz).**

A growing collection of reusable agent skills and plugins for Claude Code, Cursor, and Codex.
One repository can hold many independently installable plugins. A plugin can contain one skill or
a cohesive group of related skills. Each plugin owns its version, documentation and compatibility.

## Available plugins

| Plugin | Purpose | Status |
| --- | --- | --- |
| [domain-driven-design](plugins/domain-driven-design/README.md) | Principal domain ownership, reusable engines, explicit handoffs and connected-path gap tracing | Preview; Cursor CLI 16/16, Claude 15/16 with agent-count noncompliance |

More skills can be added without renaming this repository or forcing users to install everything.
The domain-driven-design skill folder remains 598 lines including its metadata and helper.

## Installation

Claude Code users register the catalog once and choose a plugin:

```sh
claude plugin marketplace add sigmastudioz/agent-skills
claude plugin install domain-driven-design@sigmastudioz --scope user
```

For Codex, clone the repository and register the clone:

```sh
git clone https://github.com/sigmastudioz/agent-skills.git
codex plugin marketplace add ./agent-skills
```

Install the chosen plugin from the SigmaStudioz source in the plugin directory. Cursor users can
install a skill in its native skills directory or load a plugin locally; public marketplace listing
requires the platform's separate review process. See [SETUP.md](SETUP.md) for global automatic use.

Plugin discovery is separate from a user-approved global baseline setup. Installing this catalog
does not silently rewrite global instructions. Hosts that disable user instructions can limit it.

## Repository layout

```text
catalog.json                     # Maintained list of plugins
plugins/
  domain-driven-design/
    plugin.json                  # Portable identity, author, version and presentation
    .claude-plugin/plugin.json
    .cursor-plugin/plugin.json
    .codex-plugin/plugin.json
    skills/domain-driven-design/
      SKILL.md
      agents/openai.yaml
      scripts/guard_handoff.py
tools/build_catalogs.py           # Generates three host catalogs from catalog.json
tests/test_catalogs.py            # Exercises multiple plugins and cross-host consistency
```

The three root catalog files are generated. Add new plugin folders and registry entries as described
in [CONTRIBUTING.md](CONTRIBUTING.md); do not maintain three different plugin inventories by hand.
No empty future skill folders or placeholder implementations are included.

## Status and attribution

Published at [sigmastudioz/agent-skills](https://github.com/sigmastudioz/agent-skills) under the
[MIT license](LICENSE), copyright 2026 Lex from SigmaStudioz. Each distributed plugin includes its
license notice. This repository is a direct-install catalog; official marketplace-directory
listings require separate submission and approval.

The initial plugin has 16/16 held-out feature checks and 2/2 payment regressions from a fresh Cursor
Agent CLI experiment. A completed fresh Claude Code run passed 15/16 feature checks and 2/2
payment regressions, but used four teammates despite the requested agent count of one. Its NUL
delimiter compound key failed a collision check. Automatic loading and guarded handoff delivery
worked; full behavioral validation did not pass. See the plugin README for coverage.
These results do not guarantee every model, desktop mode, or remote/cloud host follows every rule.

Author bylines and plugin publisher metadata credit **Lex from SigmaStudioz**. Official directory
publisher names also depend on the platform's verified developer identity. Each future plugin should
preserve its actual authorship and attribution rather than inherit incorrect creator claims.

See [PUBLISHING.md](PUBLISHING.md) for distribution and licensing details.

## License

[MIT](LICENSE). Reuse, modification and commercial distribution are permitted with the copyright
and license notice preserved. Author metadata credits Lex from SigmaStudioz.
