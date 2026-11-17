# UI Foundation Reuse

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · plugin version 1.4.0.

Reuse compatible React effects and scene infrastructure without a library download. This
plugin includes the complete `ui-foundation-reuse` skill and the bundled
`@sigmastudioz/ui-foundation` 0.13.2 runtime: CJS/ESM modules, TypeScript declarations,
original source and license notices. React and optional rendering peers are external.

## Changes in 1.4.0

Refresh the bundled runtime to 0.13.2 (104 public export entries, 3,011 files) and its
matching source, types, checksum metadata and skill guide. 0.13.2 adds the pieces for a 3D
product configurator:

- `/three` `Model materials` recolours named parts of a loaded model per option, with
  `createMaterialVariants` and `resolveMaterialOverride` for a scene loaded another way.
- `/product-config` (React only, no Three peer): `useProductConfig`, `priceConfiguration`,
  `resolveSelection`, `selectionMaterials`, `defaultOptionFor` and `formatPrice`. Prices are
  whole minor units and are display values; charge from the server's own price list.
- The skill guide gains a product configurator section covering spin, recolour, price and
  page structure.

0.13.1 changed no source: it was the release of the gesture, baked-lighting and Three.js 0.187
work already described under 1.3.0. The staging helper and its credential boundary are unchanged.

## Changes in 1.3.0

Refresh the bundled runtime to 0.13.0 (103 public export entries, 2,986 files) and its
matching source, types, checksum metadata and skill guide. This moves the plugin forward two
library releases:

- 0.12.0 adds `/page-flip` (`PageFlip`), `/card-ring` (`CardRing`), `/type-refraction`
  (`TypeRefraction`), `/shard-burst` (`ShardBurst`) and `/swing-rail` (`SwingRail`).
- 0.13.0 adds `/core` `useDragGesture` (one press-drag-release gesture with a cancel that is
  never mistaken for a tap) and `/three` `Model lightmap` (baked lighting from a lighting-only
  OpenEXR bake, with `applyLightmap`). `PageFlip` and `CardRing` write animation frames
  straight to the DOM.
- Fixes carried in the runtime: a touch that becomes a page scroll no longer turns a
  `PageFlip` page, its mid-turn copies are inert, `TypeRefraction` follows a CSS theme change,
  a controlled `CardRing` follows `index`, `Portal` content stays in place on a scaled surface
  under recent Three.js, and the 3D peers load in Node from the CommonJS build.

The runtime is built and tested against Three.js 0.187; its peer range is unchanged
(`three >= 0.160`). The staging helper and its credential boundary are unchanged.

## Changes in 1.2.3

Explicitly declares an empty MCP server map in the Claude manifest. This skill has no
MCP server, credential variable, hook or secret input. The staging helper reads only
the local bundle metadata/archive and the selected application's manifest; it neither
reads a credential store nor opens a network connection. Credential-boundary regressions
protect that contract. The bundled 0.11.0 runtime and its checksum are unchanged.

Anthropic previously reported `MCP_FORWARDS_CREDENTIAL_ENV` against this metadata-only
manifest despite its having no server or environment configuration. An explicit empty map
documents the actual behavior; it does not establish removal of the remote warning.
The separate archive-inspection and Verified-organization restrictions still require review.

## Changes in 1.2.1

Adds the independent critique loop to the skill: real screenshots of rest, mid-animation,
reduced-motion, light and dark states reviewed by a fresh critic each round, three rounds by
default, with a change of approach when a defect returns. The bundled runtime is rebuilt from
the same 0.11.0 release with that guide.

## Changes in 1.2.0

Refresh the bundled runtime to 0.11.0 (98 public export entries, 2,871 files) and its
matching source, types and checksum metadata. 0.11.0 adds `/scroll-layout`
(`StackingCards`, `HorizontalScroll`, `VelocityMarquee`, `ScrollColor`), `/scroll-nav`
(`HideOnScroll`, `useScrollDirection`, `useScrollSpy`), entrance components in `/scroll-reveal`
(`Reveal`, `SplitReveal`, `Typewriter`, `CountUp`, `TextFill`) and `/refractive-glass`
(`RefractiveGlass`, `GlassLens`). 0.10.0 added `/blob-track`, `/gooey-reveal`,
`/flip-card`, `/dot-matrix`, `/zoom-blur` and `/reaction-diffusion`. Guidance also covers `/dither` (Bayer and
error diffusion), `/image-particles`, `/glitch`, `ImageFilter` presets (night vision,
receipt print, flash), the magenta phosphor preset and `PixelateTransition`, plus the
0.8.0 shape patterns, rain-on-glass and iridescent ribbon contracts. It adds a
text-behind-subject scroll recipe, common-name mappings, an aesthetic style dictionary
and a UX-laws critique pass. Inventory counts and unit/SSR checks do not establish visual
correctness in every consuming application; existing app-vendored versions stay pinned.

## Changes in 1.1.1

Completes the guide to existing runtime 0.7.0 exports, including retro image treatments,
geometric fields, grain/tilt-shift, additional reveals/media surfaces and native adapters.
The runtime archive, types, source, licenses and checksum are unchanged. Existing applications
remain pinned. [Pressure scenarios](skills/ui-foundation-reuse/tests/README.md) retain historical
baseline limitations and portable inputs; no new native or visual rendering claim is implied.

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

## Changes in 1.1.0

Refresh the bundled runtime to 0.7.0 and its matching source, types and checksum metadata.
Guidance now covers image distortion facades, thermal color ramps, iridescent ribbons,
rain-on-glass, native foil composition and current scene/physics loading constraints.
Inspect platform peers and actual public exports before selecting an effect. The runtime
contains 85 public export entries and 2,431 files; these inventory counts do not establish
visual correctness, native-agent efficacy or compatibility with every consuming application.
Existing app-vendored versions remain pinned until deliberately upgraded.

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

## Distribution boundary

The runtime skill retains its guidance and functional helpers. Executable synthetic evaluation
fixtures live in the collection’s [test area](https://github.com/sigmastudioz/agent-skills/tree/main/tests/fixtures/ui-foundation-reuse), outside this installable plugin.
Historical scenario summaries retain their original dates and hashes. This packaging change does
not establish Anthropic organization verification or clearance of separate directory findings.
