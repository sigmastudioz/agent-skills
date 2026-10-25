---
name: ui-foundation-reuse
description: Reuse bundled ui-foundation effect code and scene helpers alongside Taste, Impeccable, img2threejs or visualization-videos in compatible React projects. Works without a library download using the included local runtime archive. Prefer existing effects before rebuilding shaders, scroll motion or scene infrastructure; maintain the bundle when library capabilities change.
---

# Reuse ui-foundation

By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Prefer the project's existing `@sigmastudioz/ui-foundation` implementations before writing equivalent effects or scene infrastructure. Apply this alongside Taste, Impeccable, img2threejs and visualization-videos while preserving their design, reconstruction and video workflows.

This skill includes reusable implementation code in `assets/ui-foundation.tgz`: built CJS/ESM modules, TypeScript declarations, original TypeScript source, the MIT license and third-party notices. `assets/bundle.json` records the included version and checksum. No library download or maintainer checkout is required. React and optional rendering peers remain external dependencies; photos, models, video and other app assets are not included.

Read [setup](references/setup.md) for Codex/Claude installation and local runtime setup, and [license notices](references/third-party-notices.md) when redistributing the code. Resolve relative skill paths from the directory containing this `SKILL.md`, not the app's working directory.

## Reuse an installed runtime or stage the included one

Work from the consuming application's directory, including the correct workspace in a monorepo. Inspect its manifest, lockfile, existing wrappers, and scene host. Resolve the actual installation rather than assuming a `node_modules` layout or a source checkout:

```sh
node -p "require.resolve('@sigmastudioz/ui-foundation/package.json')"
```

Use the project's Node runner when required by its package manager, such as `yarn node` for Yarn Plug'n'Play. The returned manifest's parent is the package root. Read its `version`, `exports`, `peerDependencies`, and `peerDependenciesMeta`, its bundled `README.md`, and the relevant declaration files selected by `exports` (for example, `exports['./three'].import.types`). Follow declaration re-exports to the component props and hooks. The compiled implementation is available at the corresponding runtime export when behavior needs investigation. Discovery does not require importing React, Three, or the renderer.

Treat the resolved exports and declarations as the API authority. The map below describes capabilities to search for, not a guarantee that every version includes them. Reuse an existing compatible installation; do not replace it silently with the bundled version.

If the package is absent and implementation is authorized, read `assets/bundle.json`, then run the included staging helper from its actual skill location:

```sh
node "<skill-directory>/scripts/stage-runtime.mjs" "<application-directory>"
```

The helper verifies the archive checksum and copies it to `vendor/ui-foundation/ui-foundation.tgz` in the app without editing its manifest or downloading anything. It refuses a conflicting existing archive. From the app directory, use its normal package manager to install that local file; for npm:

```sh
npm install ./vendor/ui-foundation/ui-foundation.tgz
```

This resolves the same public package name entirely from bundled code. Commit the vendored archive and normal manifest/lockfile changes with the consuming app so builds do not depend on the agent's skill directory. Other dependencies can still require normal package-manager access. Inspect React and optional peer compatibility before adding them; do not bundle another copy of React or add Three for 2D-only work.

For read-only investigation, inspect `assets/bundle.json` and extract the included archive to a temporary directory instead of changing the app. The archive's `package.json`, `lib/` declarations and `src/` contain the API and implementation; no external source tree, examples or playground is required. If an explicitly available workspace checkout is used, unreleased source does not override the installed contract.

Match the requested behavior to an existing export, preset, or composition. Import through a public package subpath and add only the app-specific composition or adapter that is missing. Keep the bundled package cohesive rather than copying isolated files and breaking its shared imports. Do not recreate its shader, animation loop, renderer, loader, or lifecycle hooks.

If the archive is missing or damaged, report an incomplete skill installation instead of trying to download the library. If local installation or a required peer is unavailable, report that specific gap and continue independent design work where possible. Never invent working imports, assume access to another machine, change an existing dependency source silently, or substitute a duplicate effect without explaining the gap. Respect review-only scope.

## Capability search map

Subpaths below are relative to `@sigmastudioz/ui-foundation`. Confirm availability in the installed manifest before using them.

| Requested behavior | Inspect these public subpaths first |
| --- | --- |
| Shader backgrounds, liquid metal/glass, glass distortion | `/gradient`, `/liquid-metal`, `/liquid-glass`, `/fluted-glass`, `/iridescence` |
| Video/frame scrubbing, scroll chapters, depth and parallax | `/scroll-scrub`, `/scroll-3d`, `/scroll-reveal`, `/mouse-parallax`, `/camera-journey` |
| Pointer attraction, particles, fluid motion, text effects | `/magnetic`, `/particle-form`, `/particles`, `/fluid-field`, `/kinetic-text` |
| Image transitions, filters and material treatments | `/image-transition`, `/image-filter`, `/heatmap`, `/foil-surface`, `/light-glow`, `/text-portrait` |
| Media layouts, panels and transitions | `/media-strip`, `/media-carousel`, `/scene-panel`, `/layout-morph`, `/object-stack`, `/media-disclosure` |
| Spatial interfaces, floating objects and tactile media | `/spatial-canvas`, `/floating-objects`, `/crt-surface`, `/disc-carousel` |
| Paper, brush and aperture reveals | `/paper-motion`, `/aperture-reveal` |
| Audio-reactive and environmental effects | `/visualizer`, `/cymatics`, `/weather` |
| 3D hosting, staging and models | `/three`: `Scene`, `World`, `Model`, `Float`, `GlassMaterial`, `Portal`, `ReflectiveFloor`, `SoftShadows`, `Bloom`, `Caustics`, `ExplodedAssembly`, `useSceneMotion` |
| Shared lifecycle, visibility, interaction and quality policy | `/core`: `EffectsProvider`, `useEffectsSettings`, `useRafLoop`, `useReducedMotion`, `useInView`, `usePageVisible`, `useWebGLEffect`, `useScrollProgress`, `useInteraction`, `useAdaptiveQuality` |

Search the full installed exports if the selective map has no match. Inspect `/presets` when available for existing configurations and composition patterns.

## Apply alongside each design skill

- **Taste:** use its direction, composition and review process; implement matching motion and material effects with library exports. Its handwritten effect recipes are alternatives after the reuse check establishes a gap. Keep typography, brand tokens, page structure and content in the consuming app.
- **Impeccable:** refine composition, styling, effect configuration and accessibility around library components. Do not replace a reusable shader or scene helper merely to satisfy a generic aesthetic detector. Honor explicit visual intent; investigate correctness or performance problems at their owning layer. Keep reviews read-only.
- **img2threejs:** its staged pipeline owns subject-specific geometry, materials and reconstruction evidence. Reuse the library for hosting and generic staging instead of generating another Canvas, asset loader, orbit controller or ambient float implementation. Keep custom subject geometry and unmet material requirements in the generated asset.
- **Visualization Videos by SigmaStudioz (`visualization-videos`):** reuse compatible effects and scene helpers for React video previews and supported exports. The video project owns its storyboard, captions, custom geometry, canonical timeline and encoder. Check actual clock/seeking contracts before promising deterministic capture; live RAF animation or scene pause alone is not a frame-driven export API. Verify effects in the encoded video. Keep Pillow/FFmpeg and non-React renderers when appropriate; add only a demonstrated, authorized adapter or report the compatibility/export gap.

These companion skills are independent installations. This guide does not install them or require all of them to be present.

## Integrate generated 3D assets correctly

Inspect the installed `/three` declarations for `Scene`, `World`, `Model`, and `useSceneMotion` before choosing a host. Confirm the following contracts against that version:

- A procedural `THREE.Group` factory is consumer-owned content. Create its instance on the client and mount it as an R3F `primitive` within a compatible existing Canvas or the library's `Scene`. Do not create a nested or second Canvas for it.
- `Model` loads `.glb`/`.gltf` URLs; it does not accept a `THREE.Group` or a factory. Use it for an actual exported model asset when that export is part of the requested workflow. Do not bypass img2threejs's code-only reconstruction or validation by substituting a downloaded asset.
- Use `Float` for generic ambient floating, supported staging helpers for their effects, and `ExplodedAssembly` for authored part offsets. Keep custom pivots, geometry, interaction and storytelling in the app/model.
- Custom motion inside a library scene must honor the exported `useSceneMotion()` signal when available. Scene pause and demand-render policy alone does not make arbitrary child `useFrame` code obey reduced motion. For versions without that signal, inspect the supported pause/reduced-motion integration rather than inventing an import. Dispose resources owned by the generated instance on teardown; preserve shared/cached resources owned elsewhere.

## Preserve boundaries and verify reuse

The library owns reusable effects and shared lifecycle behavior. The app owns layouts, design tokens, branding, content, custom models and narratives. Preserve SSR safety, optional renderer isolation, reduced motion, offscreen suspension and resource cleanup. Do not add heavy renderers to unrelated imports or move app-specific assets into the library.

Reuse depends on stack, platform and behavior compatibility. Do not force React/WebGL onto unsupported native or non-React tasks; check exported native entrypoints where applicable. The user's explicit choice of another implementation takes precedence.

If no export meets a requirement, identify the missing behavior and implement the smallest authorized bridge or reusable extension at its owner, reusing the surrounding infrastructure. Do not expand a review or planning request into implementation.

In the handoff, identify the installed version, public exports reused, and any demonstrated gap requiring new code. Verify actual browser rendering and relevant motion/fallback paths; import/build success alone does not establish visual correctness.

## Keep this guide current

When adding effects, helpers, public exports or reusable capabilities to the library, or changing/removing public APIs, update the maintained `skills/ui-foundation-reuse/` in the library repository in the same task before declaring completion. Follow that repository's instructions and verification gates.

Check actual exports, declarations and implementation. Update the map and material integration guidance: public import, purpose, compatibility/optional peers, lifecycle or motion constraints, and composition limits. Keep the map concise and distinguish working-checkout changes from installed releases. Consumer layouts and demo styling do not become library capabilities.

Run `npm run build` to regenerate the runtime/source archive, checksum metadata, license and `dist/ui-foundation-reuse.zip`. The build also synchronizes local Codex/Claude skill folders and shared ZIP paths registered in the repository's ignored `.reuse-skill.local.json`; see the repository README for registration. `npm run dev` watches effects, helpers, exports and authored skill documentation and repeats the full build/sync after edits. CI creates the ZIP without synchronizing local installations. `npm run check:skill` checks payload, ZIP and registered-copy freshness without changing them, and `npm run test:skill` exercises standalone installation, distribution and watch behavior. Retain attribution when changing or redistributing bundled data. Report sync failures rather than treating a stale agent copy as updated.

Consumer projects keep their vendored runtime pinned until a deliberate upgrade; updating an agent skill does not silently change an app. Never edit `node_modules` as the maintenance source. If the maintained repository or an agent installation is unavailable, explicitly report the pending update or refresh. Do not assume a particular user's home directory or that setup propagates to another host.
