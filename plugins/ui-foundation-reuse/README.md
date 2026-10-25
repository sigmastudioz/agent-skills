# UI Foundation Reuse

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · plugin version 1.0.0.

Reuse compatible React effects and scene infrastructure without a library download. This
plugin includes the complete `ui-foundation-reuse` skill and the bundled
`@sigmastudioz/ui-foundation` 0.5.0 runtime: CJS/ESM modules, TypeScript declarations,
original source and license notices. React and optional rendering peers are external.

## Install

```sh
npx skills add sigmastudioz/agent-skills --skill ui-foundation-reuse
```

For Claude Code, register this repository and select `ui-foundation-reuse@sigmastudioz`.
Claude, Cursor and Codex manifests are included. This repository distribution does not
establish approval or activation in an official directory. Do not create a duplicate
submission when updating an existing entry.

Read [standalone setup](skills/ui-foundation-reuse/references/setup.md) for manual
Codex/Claude installation and application setup. Keep the whole skill folder together.
The [staging helper](skills/ui-foundation-reuse/scripts/stage-runtime.mjs) verifies the
archive and copies it into the selected application's `vendor/ui-foundation/`; it does
not download packages, rewrite a manifest or install dependencies. Install that local
file with the app's normal package manager only within the authorized task.

## Scope and compatibility

Inspect an existing installation's actual version, public exports, types and peers first;
do not silently replace a compatible installation. App layouts, branding, custom geometry,
assets and video timelines remain app-owned. Effects that animate in a browser are not
necessarily seekable at arbitrary export timestamps; verify their clock contract and
encoded output before promising deterministic video capture.

Taste, Impeccable, img2threejs and Visualizer are independent companion skills. This
plugin neither installs them nor requires React for a non-React task. A missing peer,
damaged archive or unsupported renderer must be reported rather than hidden.

## Data and licenses

The helper reads its local bundle and chosen app manifest, then stores a local vendored
archive. There is no publisher service, telemetry or credential store. Host-authorized
package managers or other external tools use their own provider policies; this plugin
has no required external service. See [Privacy](../../PRIVACY.md).

The skill and runtime implementation are MIT-licensed. Bundled head/brain geometry retains
its CC BY notices; MIT does not replace them. Preserve [LICENSE](LICENSE) and
[third-party attribution](skills/ui-foundation-reuse/references/third-party-notices.md).
The runtime's metadata records its exact version and SHA-256. Publication/package checks
are distinct from native-agent efficacy or visual correctness in a consuming application.
