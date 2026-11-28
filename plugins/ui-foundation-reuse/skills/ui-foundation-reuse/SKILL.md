---
name: ui-foundation-reuse
description: Reuse bundled ui-foundation effect code and scene helpers alongside Taste, Impeccable, img2threejs or the visualizer in compatible React projects. Works without a library download using the included local runtime archive. Prefer existing effects before rebuilding shaders, scroll motion or scene infrastructure; maintain the bundle when library capabilities change.
---

# Reuse ui-foundation

Prefer the project's existing `@sigmastudioz/ui-foundation` implementations before writing equivalent effects or scene infrastructure. Apply this alongside Taste, Impeccable, img2threejs and the visualizer while preserving their design, reconstruction and video workflows.

This skill includes reusable implementation code in `assets/ui-foundation.tgz`: built CJS/ESM modules, TypeScript declarations, original TypeScript source, the MIT license and third-party notices. `assets/bundle.json` records the included version and checksum. No library download or maintainer checkout is required. React and optional rendering peers remain external dependencies; photos, models, video and other app assets are not included.

Read [setup](references/setup.md) for Codex/Claude installation and local runtime setup, and [license notices](references/third-party-notices.md) when redistributing the code. Resolve relative skill paths from the directory containing this `SKILL.md`, not the app's working directory.

## Before first use: check what staging needs

The plugin ships its own built library archive and staging script; it bundles no Node.js,
package manager or third-party package and downloads nothing. Staging needs Node.js and the
consuming app's own package manager:

```bash
node --version   # and the app's manager, e.g. npm --version / pnpm --version / yarn --version
```

If something is missing, tell the user what is missing, which features need it and the
install route for their system. Install only after they say yes; never install silently.
Install Node.js from nodejs.org or `brew install node` (macOS), `winget install OpenJS.NodeJS.LTS`
(Windows), or the distribution package (Linux). Peer packages are installed by the app's package
manager only when the user authorizes it. If the user declines, read the bundled API guidance
and write against the documented exports without staging.

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
An export missing one option or default is a library gap: bridge with exported `/core` primitives; name the missing option as the demonstrated gap.

If the archive is missing or damaged, report an incomplete skill installation instead of trying to download the library. If local installation or a required peer is unavailable, report that specific gap and continue independent design work where possible. Never invent working imports, assume access to another machine, change an existing dependency source silently, or substitute a duplicate effect without explaining the gap. Respect review-only scope.

## Capability search map

Before choosing an effect, read the [capability search map](references/capability-map.md).
It maps requested behavior to existing public exports, including web/native peer requirements
and scene/runtime failure boundaries. Then read the linked effect API section before configuring it.

## Recipes and common names

**Text behind the subject (scroll hero).** Scrub the footage with `ScrollScrubFrames`
(or `ScrollScrubVideo`) from `/scroll-scrub`. Drive a second, frame-matched matte
sequence with `useFrameSequence({ frames, progress })` at the same progress, and pass
its `image` to `ChromaKeyOverlay channel="alpha"` around the headline. With `alpha`,
the overlay's children show where the matte is opaque, so the matte must be opaque
background with the subject transparent, at the footage's framing (the overlay masks
with center cover). Precompute those alpha frames offline (matting/rotoscoping);
the library does not segment video at runtime. The overlay is `aria-hidden`, so keep
the real heading as accessible text elsewhere. Pin a plain heading with
`StickyReveal` (`/scroll-reveal`) and change scenes with `SceneCover`. Blue/green
`channel` keys a chroma-backed frame instead of a precomputed matte.

**Common names → existing exports.** Figma/Paper-style image shaders: lens, bulge or
fisheye → `LensDistortion`; liquid blobs → `MovingBlobs`; sliced/strip offset →
`SliceShift`; pixel/line stretch or drag → `PixelStretch`; halftone dots →
`Halftone`; image warp/twist → `ImageWarp`; mosaic/8-bit → `Pixelate` (animated:
`PixelateTransition`). Hyperspeed starfield → `/warp` (not an image warp). Infinite
draggable/pannable board or moodboard field → `/spatial-canvas`: `SpatialCanvas`,
`Draggable`. Letters forming a face → `/text-portrait`. Scratch card → `/scratch-reveal`.

## Style dictionary

Map an aesthetic word to prompt cues and to the export that realises it. "No export"
means compose app-owned CSS, type, layout or artwork; do not claim an effect exists.

| Name | Prompt cues | Realised by |
| --- | --- | --- |
| CRT | scanlines, barrel glass, phosphor bloom, interference | `PhosphorGhost`, `/crt-surface` |
| Pink phosphor | magenta emission on violet-black tube | `PhosphorGhost preset="magenta"` |
| Night vision | green intensifier, shot noise, vignette | `ImageFilter preset="night-vision"` |
| Receipt / thermal print | warm 1-bit dots, paper, faded ink | `ImageFilter preset="receipt"`, `Dither` |
| 1-bit dither | ordered or diffused black/white pixels | `Dither` (`newsprint`, `blueprint`, `algorithm`) |
| Game Boy | four-tone green LCD dither | `Dither preset="gameboy"` |
| Flash light | direct flash, blown center, dark corners, bloom | `ImageFilter preset="flash"`, `/light-glow` |
| Datamosh | smeared macroblocks, motion-vector drift | `Glitch kind="datamosh"` |
| Glitch / RGB split | channel offset, row tears, band jumps | `Glitch` (`rgb-split`, `block-shift`) |
| Heatmap / thermal camera | false-color luminance ramp | `Heatmap`, `ThermalNoise` |
| Depth map | near/far parallax from a grayscale map | `ImageParticles depthSrc`, `/mouse-parallax`, `/scroll-3d` |
| Blob tracking | boxed/outlined moving subjects with labels | `BlobTrack` (`signal` `motion` on video); `MovingBlobs` is a liquid distortion, not tracking |
| LED sign / dot matrix | glowing round LEDs, marquee text, dim unlit dots | `DotMatrix` |
| Turing pattern / coral | organic spots, stripes and mazes | `ReactionDiffusion` (`coral`, `maze`, `spots`) |
| Slime mould / physarum | branching trail networks | `ReactionDiffusion model="physarum"` |
| Speed / zoom burst | radial streaks, glowing highlights, sharp center | `ZoomBlur` (`spin` for rotation) |
| Particles / dust | image dissolving or assembling as points | `ImageParticles`, `/particle-form`, `/particle-nebula` |
| Halftone | dot screen by tone | `Halftone`, `StippleDuotone` |
| Risograph | two-ink grain, misregistration | `StippleDuotone`, `XeroxCollage`; spot-color layering is app-owned |
| Xerox / photocopy | threshold ink, grain, torn seams | `XeroxCollage` |
| Collage | cut paper, mixed scraps, tape | `XeroxCollage`, `/paper-motion`; composition is app-owned |
| ASCII | glyph-mapped tone | `ImageFilter kind="ascii"`, `GlyphGrid`, `/text-portrait` |
| Teletext | 2×3 mosaic blocks, broadcast palette | `TeletextPattern` |
| Posterized / pop | few flat tones | `Posterize` |
| Liquid chrome / Y2K | chrome, iridescence, gloss, blobs | `/liquid-metal`, `/iridescence`, `/iridescent-ribbon`; Y2K type/layout is app-owned |
| Claymorphism | soft inflated 3D, pastel, inner shadow | `/three` staging for real 3D; CSS shading is app-owned |
| Gzhel | cobalt-on-white floral porcelain | No export; app-owned palette/illustration (`Dither` or `Posterize` with a cobalt palette can tint photos) |
| Visual kei | dramatic gothic contrast, lace, roses | No export; app-owned art direction (`Posterize preset="noir"`, `Grain` support it) |
| Adventure pulp | aged paper, halftone print, bold type | `Halftone`, `Grain`; type and illustration are app-owned |
| Retro gorpcore | outdoor-gear palette, utilitarian labels | No export; app-owned tokens/type |
| Art deco | geometric symmetry, gold lines, fans | `/shape-pattern` (`arcs`, `rings`, `chevron`); ornament/type is app-owned |
| Swiss | grid, sans-serif, asymmetric layout | No export; app-owned layout/type |
| Liquid glass cards | frosted refractive panels, rainbow edge light, stacked cards | `/liquid-glass` over live DOM; `/refractive-glass` for true refraction over an image or video |
| Fluted / ripple glass | figure seen through reeded or wet glass, broken into droplets | `/fluted-glass`; `RefractiveGlass` over media |
| Grain gradient | soft blurred multi-colour field, film grain, brand-mark centred | `/gradient` plus `Grain`; the brand mark and type are app-owned |
| Editorial lookbook commerce | large model imagery, thin serif or grotesk, wide margins, product rail | No export; app-owned layout, type and product grid |

## UX-laws critique pass

Run this pass after composing effects into a UI. Treat each law as a review
question, not a quota. Change only what the actual task and evidence support.

- **Hick:** is there one obvious primary action, with alternatives grouped or deferred?
- **Fitts:** are primary targets large and close to where attention lands? Aim for 44×44 CSS px.
- **Jakob:** do controls behave the way people expect (links, scroll, back, focus)?
- **Miller:** is information chunked into meaningful groups rather than one long run?
- **Doherty (~400 ms):** does feedback appear quickly, with honest loading states?
  Heavy effects must not block first input; prefer static/fallback frames until ready.
- **Von Restorff:** does exactly the thing that matters stand out? Effects on every
  element remove emphasis.
- **Serial position:** are the most important items first or last in sequences?
- **Peak–end:** is the strongest moment purposeful and does the flow end cleanly
  (for example, a transition that resolves to the readable image)?
- **Zeigarnik:** is unfinished progress visible so people can resume it?
- **Prägnanz:** does the layout read as simple shapes before the effect adds texture?
- **Tesler:** has the effect moved complexity onto the user (unreadable text, hidden
  controls)? Absorb it in the design instead.
- **Postel:** are inputs tolerant (pointer, touch, keyboard, reduced motion, no WebGL)?
- **Parkinson:** do intros and autoplay take only as long as they need?
- **Occam:** can a static image, `Pixelate` or CSS do the job instead of a heavier effect?

## Independent critique loop

Run this on what you build with the library, after its tests pass. Critique sits on top
of tests, type checks and browser checks; it never replaces them.

1. **Capture real frames** of the rendered component, not mock-ups: at rest, mid-animation,
   reduced motion, and light and dark colour schemes (plus a narrow viewport when layout
   matters). A Playwright page, the app's own browser tests or the library's
   `npm run critique:capture` (maintainers) all work.
2. **Brief a separate critic** when the user has authorized delegation and subagents are
   available: give it only the frames, the brief (intent, audience, states shown, known
   constraints such as reduced motion or no WebGL) and nothing of your reasoning. Pass no
   credentials, tokens or private data. Ask for ranked defects, each with state, what and
   where, not a score.
3. **Fix** the material defects, re-capture the same states, and use a **fresh** critic for
   the next round so it carries no memory of earlier fixes.
4. **Stop** when a round finds no material defect, after 3 rounds unless the user set a
   different budget, or when the user's budget is spent.
5. If a defect **returns after a fix**, change the approach (structure, technique or
   export) instead of tuning the same value again.

Report fixed and unfixed defects with the round each was found in. Without authorization to
delegate, or without subagents, run the same pass yourself and say it was a self-review.

## Integrate generated 3D assets correctly

Inspect the installed `/three` declarations for `Scene`, `World`, `Model`, and `useSceneMotion` before choosing a host. Confirm the following contracts against that version:

- A procedural `THREE.Group` factory is consumer-owned content. Create its instance on the client and mount it as an R3F `primitive` within a compatible existing Canvas or the library's `Scene`. Do not create a nested or second Canvas for it.
- `Model` loads `.glb`/`.gltf` URLs; it does not accept a `THREE.Group` or a factory. Use it for an actual exported model asset when that export is part of the requested workflow. Do not bypass img2threejs's code-only reconstruction or validation by substituting a downloaded asset.
- **Baked lighting.** `Model lightmap="/room.exr"` (or `{ src, intensity, channel, unlit }`) draws a static model from colour × a lighting-only OpenEXR bake made for its second UV set (`uv1`): Blender Cycles, Bake type Diffuse with Direct and Indirect on and Color off, into an image created as 32-bit float, non-colour data. Defaults: `intensity` π (Three.js divides a lightmap by π; at 1 the page shows about 0.3 of the bake), `unlit` true (baked surfaces ignore scene lights and environment, which would otherwise light them twice; emissive materials show their own emission). Use `flat` on the canvas (`canvasProps={{ flat: true }}`) to match an offline render made without a tone curve. Measured on the playground's `baked-room` page against its Cycles frame: mean difference 2.25 of 255, in Chromium and WebKit. Only `.exr` is accepted; a file that cannot load, or a model with no `uv1`, is reported through `onError` and the model renders unbaked. Materials are replaced and restored, never edited. `applyLightmap(three, root, texture, config)` with `prepareLightmap` and `resolveLightmapConfig` do the same for a scene you load yourself. Not for moving lights or objects that change the lighting.
- For an authored rig driven by custom controls, place `Model animation={false}` in a consumer-owned R3F group and resolve the asset's named bones/pivots from that group's ref after loading. Preserve rest quaternions and apply sampled offsets; do not accumulate rotations or run a baked mixer over the same joints. The consumer owns joint names, choreography and controls. `Model` clones the hierarchy/skeleton for each instance, shares cached geometry/materials, and releases instance bone textures on teardown; do not dispose the shared asset resources from custom pose code.
- Use `Float` for generic ambient floating, supported staging helpers for their effects, and `ExplodedAssembly` for authored part offsets. Keep custom pivots, geometry, interaction and storytelling in the app/model.
- Custom motion inside a library scene must honor the exported `useSceneMotion()` signal when available. Scene pause and demand-render policy alone does not make arbitrary child `useFrame` code obey reduced motion. For versions without that signal, inspect the supported pause/reduced-motion integration rather than inventing an import. Dispose resources owned by the generated instance on teardown; preserve shared/cached resources owned elsewhere.

## Preserve boundaries and verify reuse

The library owns reusable effects and shared lifecycle behavior. The app owns layouts, design tokens, branding, content, custom models and narratives. Preserve SSR safety, optional renderer isolation, reduced motion, offscreen suspension and resource cleanup. Do not add heavy renderers to unrelated imports or move app-specific assets into the library.

Reuse depends on stack, platform and behavior compatibility. Do not force React/WebGL onto unsupported native or non-React tasks; check exported native entrypoints where applicable. The user's explicit choice of another implementation takes precedence.

If no export meets a requirement, identify the missing behavior and implement the smallest authorized bridge or reusable extension at its owner, reusing the surrounding infrastructure. Do not expand a review or planning request into implementation.

End the handoff with:

```
Installed version: <from the resolved package.json>
Public exports reused: <subpath: export, ...>
Demonstrated gap: <missing behavior and owner, or none>
```

Verify actual browser rendering and relevant motion/fallback paths; import/build success alone does not establish visual correctness.


## Keep this guide current

When adding effects, helpers, public exports or reusable capabilities to the library, or changing/removing public APIs, update the maintained `skills/ui-foundation-reuse/` in the library repository in the same task before declaring completion. Follow that repository's instructions and verification gates.

Check actual exports, declarations and implementation. Update the map and material integration guidance: public import, purpose, compatibility/optional peers, lifecycle or motion constraints, and composition limits. Keep the map concise and distinguish working-checkout changes from installed releases. Consumer layouts and demo styling do not become library capabilities.

Run `npm run build` to regenerate the runtime/source archive, checksum metadata, license and `dist/ui-foundation-reuse.zip`. With `visualizerDirectory` registered in ignored `.reuse-skill.local.json` (or `UI_FOUNDATION_VISUALIZER_DIR` supplied), it also rebuilds `dist/sigmastudioz-visualizer-kit.zip` from both current skills, fresh bundled effects, licenses, setup instructions and per-file checksums. The build synchronizes registered Codex/Claude copies and standalone/combined ZIP mirrors; see the repository README. `npm run dev` watches effects, helpers, exports, authored reuse guidance and the external Visualizer source and repeats the full build/sync. Missing or invalid configured sources fail the build and leave the previous combined ZIP intact. CI ignores personal configuration and needs an explicit Visualizer input for the kit. `npm run check:skill` checks configured artifacts without modifying them; `npm run check:kit` requires combined-kit freshness. `npm run test:skill` exercises standalone installation, both distributions and watch behavior. Retain attribution and report refresh failures.

Consumer projects keep their vendored runtime pinned until a deliberate upgrade; updating an agent skill does not silently change an app. Never edit `node_modules` as the maintenance source. If the maintained repository or an agent installation is unavailable, explicitly report the pending update or refresh. Do not assume a particular user's home directory or that setup propagates to another host.
