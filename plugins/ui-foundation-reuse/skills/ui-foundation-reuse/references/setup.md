# Standalone setup for Codex and Claude Code

The complete `ui-foundation-reuse/` folder includes the reusable effect code:
`assets/ui-foundation.tgz` contains built modules, original TypeScript source,
type declarations, the MIT license and attribution notices. No library download,
account or source checkout is needed. Node.js, React and optional rendering peers
are separate prerequisites.

## 1. Install the whole skill folder

Extract the shared skill archive. Keep `SKILL.md`, `LICENSE`, `assets/`, `scripts/`
and `references/` together. Copy the entire folder to the desired agent location:

| Scope | Codex destination | Claude Code destination |
| --- | --- | --- |
| Project/team | `.agents/skills/ui-foundation-reuse/` | `.claude/skills/ui-foundation-reuse/` |
| Personal, all local projects | `~/.agents/skills/ui-foundation-reuse/` | `~/.claude/skills/ui-foundation-reuse/` |

For example, from the directory containing the extracted `ui-foundation-reuse/`,
these POSIX-shell commands install personal copies without replacing existing skills:

```sh
for destination in "$HOME/.agents/skills/ui-foundation-reuse" "$HOME/.claude/skills/ui-foundation-reuse"; do
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Back up the existing skill at %s before replacing it.\n' "$destination" >&2
    exit 1
  fi
done
test -f ui-foundation-reuse/assets/ui-foundation.tgz || exit 1
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
cp -R ui-foundation-reuse "$HOME/.agents/skills/"
cp -R ui-foundation-reuse "$HOME/.claude/skills/"
```

For team setup, copy to the project destinations and commit those folders. On
Windows use file copy or PowerShell `Copy-Item -Recurse` with the current user's
home directory. Keep both copies identical. A shared folder and discovery symlinks
also work where symlinks are supported.

These locations follow [Codex's discovery rules](https://developers.openai.com/codex/skills/#where-to-save-skills)
and [Claude Code's skill locations](https://code.claude.com/docs/en/skills#choose-where-skills-load).
Install separately on other execution hosts. If discovery does not update, verify
the folder and frontmatter, check for duplicate same-named skills, and restart the agent.

## 2. Add the included runtime to an application

First check whether the app already has a compatible `@sigmastudioz/ui-foundation`.
Reuse that installation when appropriate; do not replace its version silently.
For a new installation, run the staging helper from the actual installed skill
location, passing the consuming app directory. For a project-scoped Codex copy,
run this from the app directory containing `package.json`:

```sh
node .agents/skills/ui-foundation-reuse/scripts/stage-runtime.mjs .
npm install ./vendor/ui-foundation/ui-foundation.tgz
```

For a personal Codex copy, use this staging command from the app directory instead:

```sh
node "$HOME/.agents/skills/ui-foundation-reuse/scripts/stage-runtime.mjs" .
```

For Claude Code, substitute `.claude` for `.agents` in the helper path. The helper
only checks the bundle and copies it into the app; it does not download anything,
modify `package.json`, or run a package manager. The subsequent install uses a
local file dependency, preserving ordinary public imports:

```json
{
  "dependencies": {
    "@sigmastudioz/ui-foundation": "file:vendor/ui-foundation/ui-foundation.tgz"
  }
}
```

Use the app's existing npm, pnpm or Yarn workflow to install the local archive and
update its lockfile. Commit `vendor/ui-foundation/ui-foundation.tgz` plus the normal
manifest and lockfile changes; other developers and CI then use the app's vendored
archive independently of the agent installation.

The archive metadata records the included version and SHA-256. The helper refuses
a damaged bundle or a different existing vendored archive. To upgrade, review the
version and changes, back up/replace the old archive deliberately, and regenerate
the dependency lock entry using the package manager. Updating this skill alone
does not upgrade existing apps.

## 3. External peers and assets

React must satisfy the bundled manifest's peer range. A React web app normally
already supplies React and React DOM. For 3D features, add compatible `three` and
`@react-three/fiber` versions for that app's React version. Physics and native
features have their own optional peers; inspect the included manifest. Do not
add heavy renderers just to use 2D effects.

The UI implementation is included, but its external peers are not. A fully offline
install also needs those peers already available locally. Photos, fonts, video,
audio and downloaded models are not bundled; provide the app's own assets when
needed. Taste, Impeccable and img2threejs are independent companion skills and
are not installed by this skill.

## 4. Verify and invoke

From the consuming app, check the resolved local installation:

```sh
node -p "require.resolve('@sigmastudioz/ui-foundation/package.json')"
node -p "require('@sigmastudioz/ui-foundation/package.json').version"
```

Run within the correct consuming workspace in a monorepo; use `yarn node` for
Yarn Plug'n'Play where needed. Inspect the resolved exports, declarations and
bundled `src/` before implementing a helper. For example, in a React client component:

```tsx
import { Gradient } from '@sigmastudioz/ui-foundation/gradient';

export function Backdrop() {
  return <Gradient preset="ocean" style={{ height: 320 }} />;
}
```

In Codex:

```text
$ui-foundation-reuse Use the included runtime to add a glass scene to this React app. Reuse its scene helpers and motion lifecycle.
```

In Claude Code:

```text
/ui-foundation-reuse Use the included runtime to add a glass scene to this React app. Reuse its scene helpers and motion lifecycle.
```

For a read-only check, ask either agent to inspect `assets/bundle.json` and extract
the runtime to a temporary directory, list its exports and peer requirements, and
make no app changes. This checks the API without installing a dependency.

For consistent routing, add this instruction to `AGENTS.md` for Codex and
`CLAUDE.md` for Claude Code, preserving existing instructions:

```text
For compatible React effects and scene work, including Taste, Impeccable and
img2threejs tasks, apply ui-foundation-reuse before implementation. Reuse an
existing compatible runtime or install its included local archive when the library
is absent. Inspect the resolved version, exports, declarations and peer requirements.
Keep layouts, branding and custom geometry in the app. Honor platform compatibility,
explicit user choices and review-only scope. Report missing or damaged skill assets
instead of inventing imports or silently rebuilding an existing effect.
```

## Maintenance and redistribution

Keep `LICENSE` and [third-party notices](third-party-notices.md) with the skill and
the vendored runtime. Source and compiled code are bundled together; no playground
media, dependency installations or maintainer filesystem is included.

Maintainers run `npm run build` in the library repository after capability/API changes
to refresh the runtime, source, license, checksum metadata and shareable
`dist/ui-foundation-reuse.zip`. Registered agent folders and shared ZIP paths in
the repository's ignored `.reuse-skill.local.json` synchronize during the same build;
the repository README documents registration. `npm run dev` automatically repeats
the full build and synchronization when effects, exports or authored skill files change.
CI creates the ZIP without writing to agent home folders. `npm run check:skill`
verifies payload, ZIP and registered-copy freshness without modifying them, and
`npm run test:skill` checks local-only installation, distribution and watch behavior.
Consumers need only the distributed skill folder; maintainer build tooling is not
required for using the included runtime.
