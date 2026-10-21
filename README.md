# SigmaStudioz Agent Skills

**By [Lex from SigmaStudioz](https://github.com/sigmastudioz). Licensed under [MIT](LICENSE).**

[![Install on skills.sh](https://img.shields.io/badge/skills.sh-install-black)](https://skills.sh/sigmastudioz/agent-skills/domain-driven-design)

A collection of reusable skills by Lex from SigmaStudioz. Each plugin has its own version.

## Principal Driven Domain Design

Help coding agents organize code by domain, reuse shared behavior, and trace integration gaps
before handing work back. Apply principal-level engineering to the feature or fix at hand.

- **Clear ownership:** domain first, then services, adapters and scoped shared code.
- **Useful reuse:** shared domain packages and cohesive engines when real consumers need them.
- **Connected behavior:** follow callers, dependencies, failure paths and downstream consumers.
- **Complete handoffs:** carry scope, locations, contracts, checks and unresolved findings.

### Quick start

**1. Install.** Use the [Claude directory](https://claude.ai/customize/plugins/id/afb92b63-9b33-4c1a-8a78-f321fa1d1c4b%40anthropic-plugin-directory)
for the published Claude plugin, or install the skill in your project and choose your coding agent:

```sh
npx skills add sigmastudioz/agent-skills --skill domain-driven-design
```

Find the [live skills.sh listing](https://skills.sh/sigmastudioz/agent-skills/domain-driven-design)
or visit [sigmastudioz.com/skills](https://sigmastudioz.com/skills).

**2. Enable automatic use once.** Follow [the host-specific global setup](SETUP.md) for Claude Code,
Cursor or Codex. Point the host's global instructions at your actual installed `SKILL.md`, preserve
existing settings, and start a fresh session. The optional Claude handoff guard is separate.
Installing the skill alone does not configure automatic use across projects or remote hosts.

**3. Give an ordinary coding request.** In a billing project, for example:

> Add refund processing to the API and background job. Keep existing payment behavior working.
> Follow the current public contracts and run the relevant checks.

No skill name or architecture trigger is needed after automatic setup. Check the agent's actual
loading, changes and verification; instruction guidance does not guarantee model compliance.

### Watch the workflow

https://github.com/user-attachments/assets/cec0933f-4803-487a-8f6c-f92c24c257af

[Download the full HD demo](assets/ddd-demo.mp4?raw=true) ·
[Captions](assets/ddd-demo.srt) · [Run the synthetic coding example](assets/README.md) ·
[Editable sources](assets/ddd-demo-source.zip?raw=true)

The illustrated demo follows API and worker consumers into one billing capability, traces a
connection gap, visualizes the authority-boundary repair, and explains handoffs and checks.
The 50-second film combines 60fps paper animation, GPU-baked material lighting and an
original stereo score. Editable sources include a Three.js shader preview.
Authored by **Lex from SigmaStudioz**, it replays recorded evidence through animation. The fresh Claude Code 1.0.5 run passed
16 feature checks and 2 original regressions with one teammate. Versions 1.0.6 and 1.0.7
update branding and packaging; they do not establish a new coding-test baseline.
The included fixture is independently runnable and intentionally uses an in-memory store.

### Native plugin installation

For the full Claude Code plugin:

```sh
claude plugin marketplace add sigmastudioz/agent-skills
claude plugin install domain-driven-design@sigmastudioz --scope user
```

For Codex, register a local collection clone:

```sh
git clone https://github.com/sigmastudioz/agent-skills.git
codex plugin marketplace add ./agent-skills
```

Install the chosen plugin from the SigmaStudioz source. Cursor local loading and native skill
locations are covered in [SETUP.md](SETUP.md). Official directory reviews are separate from
these direct installation methods. Claude currently serves 1.0.6; the 1.0.7 metadata update
awaits reviewer activation. Cursor, Codex and Antigravity publication is not yet confirmed.

### Available plugins

| Plugin | Purpose | Version |
| --- | --- | --- |
| [Principal Driven Domain Design](plugins/domain-driven-design/README.md) | Domain ownership, reusable engines, gap tracing and agent handoffs | 1.1.0 |

### Visual creation and analysis

| Plugin | Purpose | Version |
| --- | --- | --- |
| [SigmaStudioz Visualizer](plugins/visualizer/README.md) | React Three Fiber scenes, interactive visuals, simulations and visualization videos | 1.1.0 |
| [SigmaStudioz Video Analysis](plugins/video-analysis/README.md) | Timestamped visual/audio evidence, adaptive frame inspection and transcript correlation | 1.0.0 |

Install either skill with `npx skills add sigmastudioz/agent-skills --skill visualizer` or
`npx skills add sigmastudioz/agent-skills --skill video-analysis`. Both are by **Lex from SigmaStudioz**.
See their documentation for requirements and validation limits. Official marketplace review is separate.

The stable package identifier is `domain-driven-design`. Its updated skill folder contains
666 lines. This collection can host future plugins with independent versions.

## Validation and limitations

1.1.0 publishes the updated engineering instructions: cross-module edge checks, staged snapshot
and concurrent-writer review, candidate-disproof guidance, and early versus final gates. The
optional helper and UI metadata are unchanged. No fresh native-agent efficacy run is claimed.

1.0.7 adds display metadata, an original icon, discovery keywords and Cursor schema corrections;
1.0.6 introduced the public branding. Those versions’ engineering instructions and helper behavior match 1.0.5;
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
