# SigmaStudioz Agent Skills

**By [Lex from SigmaStudioz](https://github.com/sigmastudioz). Licensed under [MIT](LICENSE).**

A growing collection of reusable agent skills and plugins for Claude Code, Cursor and Codex.
Each plugin owns its version and can contain one skill or a cohesive group of related skills.
Users install only what they need; future plugins do not force a shared release version.

## Available plugins

| Plugin | Purpose | Validation |
| --- | --- | --- |
| [Principal Driven Domain Design](plugins/domain-driven-design/README.md) 1.0.6 | Principal domain ownership, reusable engines, explicit handoffs and connected-path gap tracing | Fresh Claude Code: 16/16 feature checks, 2/2 regressions, one teammate |

**Principal Driven Domain Design** is the first skill: principal-level domain-driven design for
AI coding agents. Its package and invocation identifier remains `domain-driven-design`, so
existing installation commands continue to work.

The full DDD skill folder is **597 lines**, including its metadata and optional helper.

## Installation

Claude Code users register the collection and select the plugin:

```sh
claude plugin marketplace add sigmastudioz/agent-skills
claude plugin install domain-driven-design@sigmastudioz --scope user
```

For Codex, clone the collection and register the clone:

```sh
git clone https://github.com/sigmastudioz/agent-skills.git
codex plugin marketplace add ./agent-skills
```

Install the chosen plugin from the SigmaStudioz source in the plugin directory. Cursor users can
install a native skill or load the plugin locally; see [SETUP.md](SETUP.md) and the platform docs.
Official directory submissions have their own review process; repository publication is not a
claim that Claude, Cursor or OpenAI has approved a listing.

For ordinary coding tasks to apply the baseline without trigger words, follow the one-time,
user-approved global setup. Installing this catalog does not silently rewrite global settings.
Remote/cloud agents and hosts that disable user instructions need separate accessible setup.

## Validation and limitations

1.0.6 is a branding release. The engineering instructions and helper behavior match 1.0.5;
only the instruction title, display metadata and documentation changed. Native evidence remains
tied to its recorded 1.0.5 baseline, rather than being relabeled as a new test.

The fresh 1.0.5 Claude Code test used the unchanged ordinary coding request, a clean billing
monorepo fixture and exactly one implementation teammate. The coordinator integrated its work,
ran 20 local tests and repaired an authority-field bug. Independent held-out checks passed 16/16
feature cases and 2/2 original regressions, including compound-identity collisions.

The optional Claude helper delivered the full baseline before the task brief. Its 21 tests cover
handoff validation, explicit teammate budgets, rejected attempts, parallel pending calls and worker
resumption. It does not infer authorization or guarantee semantic correctness. Historical Claude
failures are retained in the [validation receipt](docs/validation.json), not rewritten as passes.

The earlier Cursor CLI run also passed 16/16 + 2/2; its recorded baseline differs from 1.0.5.
Cursor desktop, cloud runtimes and production concurrency/performance were not exercised.
Instruction guidance and scoped tests do not guarantee every future model follows every rule.

## Adding future skills

Add owned plugin folders under `plugins/`, register them once in `catalog.json`, and generate all
three native catalogs plus per-plugin file hashes with `tools/build_catalogs.py`. See
[CONTRIBUTING.md](CONTRIBUTING.md) for independent versions, author attribution and checks.
The public entrypoints are `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`
and `.agents/plugins/marketplace.json`; generated catalogs are checked for drift.

## Data, support and attribution

This skill has no publisher-hosted backend or telemetry. The optional helper reads native session
history locally. Host-agent data handling follows the user's provider settings. Read
[PRIVACY.md](PRIVACY.md) and use [GitHub Issues](https://github.com/sigmastudioz/agent-skills/issues)
for support; do not post private code, credentials or session logs.

Author bylines and manifests credit **Lex from SigmaStudioz**. Directory publisher labels also
use the platform's verified identity. [MIT](LICENSE) permits reuse, modification and commercial
distribution with the copyright and license notice preserved. Each plugin includes its notice.
