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
| Shader backgrounds, liquid metal/glass, glass distortion | `/gradient`, `/liquid-metal`, `/liquid-glass`, `/fluted-glass`, `/iridescence`, `/iridescent-ribbon` |
| Video/frame scrubbing, scroll chapters, depth and parallax | `/scroll-scrub`, `/scroll-3d`, `/scroll-reveal`, `/mouse-parallax`, `/camera-journey` |
| Pointer attraction, particles, fluid motion, text effects | `/magnetic`, `/particle-form`, `/particles`, `/fluid-field`, `/kinetic-text` |
| Image transitions, filters and material treatments | `/image-transition`, `/image-filter`, `/heatmap`, `/foil-surface`, `/light-glow`, `/text-portrait` |
| Image refraction, liquid bulges, strip displacement and localized stretch | `/lens-distortion`: `LensDistortion`; `/moving-blobs`: `MovingBlobs`; `/slice-shift`: `SliceShift`; `/pixel-stretch`: `PixelStretch`; `/image-warp`: `ImageWarp` |
| Print dots and square image cells | `/halftone`: `Halftone`; `/pixelate`: `Pixelate` |
| Media layouts, panels and transitions | `/media-strip`, `/media-carousel`, `/scene-panel`, `/layout-morph`, `/object-stack`, `/media-disclosure` |
| Spatial interfaces, floating objects and tactile media | `/spatial-canvas`, `/floating-objects`, `/crt-surface`, `/disc-carousel` |
| Paper, brush and aperture reveals | `/paper-motion`, `/aperture-reveal` |
| Audio-reactive and environmental effects | `/visualizer`, `/cymatics`, `/weather` |
| Rain beads and sliding drops refracting a blurred still image | `/rain-on-glass`: `RainOnGlass` |
| 3D hosting, staging and models | `/three`: `Scene`, `World`, `Model`, `Float`, `GlassMaterial`, `Portal`, `ReflectiveFloor`, `SoftShadows`, `Bloom`, `Caustics`, `ExplodedAssembly`, `useSceneMotion`. `Model` and `Float` accept `onError` when their runtime cannot load. `World` then shows its install fallback. |
| Rigid-body scene content | `/physics`: `BallPit` loads `@react-three/rapier` on mount and accepts `onError`. `/physics/rapier`: `Physics`, `RigidBody`, `CuboidCollider`, `BallCollider`, `CapsuleCollider` (this subpath evaluates the peer at import). |
| Shared lifecycle, visibility, interaction and quality policy | `/core`: `EffectsProvider`, `useEffectsSettings`, `useRafLoop`, `useReducedMotion`, `useInView`, `usePageVisible`, `useWebGLEffect`, `useScrollProgress`, `useInteraction`, `useAdaptiveQuality` |

Search the full installed exports if the selective map has no match. Inspect `/presets` when available for existing configurations and composition patterns.

The seven image-effect facades above share `/image-filter`'s WebGL 1 texture pass;
they work in React DOM (React >=18.2), require no Three peers, and are SSR-safe.
Each requires `src` and `alt`; use an empty description for decorative artwork.
All accept `intensity`, `paused`, `style`, `className` and `onError`. The ordinary
image remains the SSR/loading/error/context-loss fallback; remote textures require
CORS. Images use center-cropped cover fitting and clamp outside-image samples.
Distortion `center` uses normalized top-left `[x,y]`; `radius` is .05–2 times the
shorter side; `distortion` is 0–1; angles are clockwise degrees (0 right, 90 down).
Lens `offset` and Halftone/Pixelate `cellSize` use CSS pixels. Slice Shift exposes
`slices` (2–128); angle 0 uses vertical strips displaced horizontally.
Moving Blobs animates by default; the other four distortions opt in with `animated`.
`speed` is 0–3. Halftone and Pixelate are static. The shared lifecycle freezes
animation for reduced motion, offscreen/hidden state, pause or zero speed, while
redrawing changed controls. `ImageWarp` processes a still image; `/warp` remains the
unrelated hyperspeed starfield. These are visual recreations with no original
Figma code, media or temporal image feedback. The seven also exist as `ImageFilter`
kinds; facade defaults differ intentionally from the generic host defaults.

For photographic false color, import `Heatmap` and `HEATMAP_RAMPS` from
`@sigmastudioz/ui-foundation/heatmap`. Web React only; uses WebGL with a semantic
original-image fallback and requires no Three peers. Choose `thermal`, `infrared`,
or `ember` with `preset`, or override with `colorRamp`: 2–16 evenly spaced #RGB or
#RRGGBB stops ordered from shadows to highlights. Invalid ramps use thermal.
`contrast` (0.1–3), `intensity` (0–1), and `invert` tune the luminance mapping;
source alpha is retained. It is static, with no RAF loop, and redraws on source,
size, or control changes. Give it `src`, descriptive `alt`, and an appropriate
height; remote textures require CORS. It does not measure temperature. The main
playground’s `#heatmap` study offers live stop editing and Copy React; its image
assets and layout are app-owned and are not included in the runtime bundle.

### Iridescent ribbon

Import `IridescentRibbon` and `resolveIridescentRibbonConfig` from
`@sigmastudioz/ui-foundation/iridescent-ribbon`. A pale, curved thin-film ribbon
frames a clear opening, with gathered spectral folds. Web React >=18.2 only;
WebGL 1, no textures or optional Three peers. Set explicit dimensions; portrait
ratios near 300/650 match the supplied wallet reference. Wider hosts stretch the
artwork; `rotation` rotates clockwise in degrees with aspect correction.
`width` (.5–2), `distortion` (0–1), `bands` (1–8), `hue` (0–360), `scale` (.5–2),
`intensity` (0–1), and hex `backgroundColor` tune the material. `speed` (0–3)
integrates without rewinding; zero freezes. Optional `time` (0–3600 seconds)
selects a deterministic frame, disables autoplay, and ignores speed. Returning
to autoplay resumes its retained phase. `paused`, provider pause, reduced motion,
offscreen and hidden-page state stop animation. Controls still redraw one frame.
Shared lifecycle owns adaptive DPR, context recovery and cleanup. Static SVG is
an approximate decorative SSR/initialization/error fallback, with unique IDs;
children stay readable and interactive above the canvas. Phone chrome, logo,
copy and actions are demo-owned. Distinct from the dark `/spectral-ribbon` and
full-surface `/iridescence`; this is an open ribbon on a white default ground.

### Rain on glass

Import `RainOnGlass` and `resolveRainOnGlassConfig` from
`@sigmastudioz/ui-foundation/rain-on-glass`. Web React >=18.2, WebGL 1;
no Three peers. Requires `src`, `alt` (empty for decorative artwork) and a host
height. A bounded CPU water model tracks individual volumes. Contact merges
drops, conserves water volume/momentum, and releases heavier drops under gravity;
swept contacts collect small beads without tunneling. Gathering necks and body
growth ease into one lens, while stationary tracks dry over five simulation
seconds. A private Canvas2D height/track map feeds the WebGL optics; both APIs
are required. Up to 2,200 drops use a spatial grid and fixed 120 Hz steps with
interpolated presentation; stalled-frame catch-up is capped at .25 simulation
seconds. This is a lightweight droplet model, not a general fluid solver.
`backgroundBlur` (0–40 CSS pixels, default 5)
uses a cached separable Gaussian; `dropletDensity` (0–1, default .8) controls
all three populations, with zero removing rain and stopping RAF. `dropletSize`
(.5–2, default 1), `refraction` (0–1, default .65), `speed` (0–3, default .7),
and deterministic `seed` (-10000–10000, default 7) tune the water. Scale is in
CSS pixels, independent of DPR. Speed changes integrate without jumping; zero
or `paused` freezes the current frame. Provider pause, reduced motion, hidden
tabs and offscreen state stop RAF; changed controls still draw a static frame.
Density, seed, droplet size and host-size changes restart the water layout;
blur/refraction changes and image swaps retain it. There is no public time-seek
API. Context restoration starts a fresh seeded layout. Offscreen/hidden/pause
time does not advance physics. The semantic image remains as the SSR/loading/renderer/context-loss fallback,
with CSS background blur. Context restoration reloads the texture; `onError`
reports initialization/context loss, image/CORS and rendering failures.
Same-origin, data/blob URLs or CORS-enabled remote still images are supported.
This does not refract arbitrary DOM or process video.
Children stay sharp and interactive above the glass. Background assets, timer,
navigation and scene switching in the Rain Atlas demo belong to the app.

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
- For an authored rig driven by custom controls, place `Model animation={false}` in a consumer-owned R3F group and resolve the asset's named bones/pivots from that group's ref after loading. Preserve rest quaternions and apply sampled offsets; do not accumulate rotations or run a baked mixer over the same joints. The consumer owns joint names, choreography and controls. `Model` clones the hierarchy/skeleton for each instance, shares cached geometry/materials, and releases instance bone textures on teardown; do not dispose the shared asset resources from custom pose code.
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

Run `npm run build` to regenerate the runtime/source archive, checksum metadata, license and `dist/ui-foundation-reuse.zip`. With `visualizerDirectory` registered in ignored `.reuse-skill.local.json` (or `UI_FOUNDATION_VISUALIZER_DIR` supplied), it also rebuilds `dist/sigmastudioz-visualizer-kit.zip` from both current skills, fresh bundled effects, licenses, setup instructions and per-file checksums. The build synchronizes registered Codex/Claude copies and standalone/combined ZIP mirrors; see the repository README. `npm run dev` watches effects, helpers, exports, authored reuse guidance and the external Visualizer source and repeats the full build/sync. Missing or invalid configured sources fail the build and leave the previous combined ZIP intact. CI ignores personal configuration and needs an explicit Visualizer input for the kit. `npm run check:skill` checks configured artifacts without modifying them; `npm run check:kit` requires combined-kit freshness. `npm run test:skill` exercises standalone installation, both distributions and watch behavior. Retain attribution and report refresh failures.

Consumer projects keep their vendored runtime pinned until a deliberate upgrade; updating an agent skill does not silently change an app. Never edit `node_modules` as the maintenance source. If the maintained repository or an agent installation is unavailable, explicitly report the pending update or refresh. Do not assume a particular user's home directory or that setup propagates to another host.

### Native foil laminate

`@sigmastudioz/ui-foundation/foil-surface/native` exports `FoilSurface` and
`NativeFoilSurfaceProps` for React Native >=0.77, React >=18.2. Pass explicit
`width`, `height`, `alt`, and image/content `children`; retain your existing
RemoteImage/FastImage loading, caching and fallback. The optional Skia peer
(>=1.12.4 <3) loads lazily for a transparent spectral laminate. Without it,
children and bounded perspective dragging still work; `onError` reports failure.
This native treatment tilts an intact card; DOM-only mesh bending, flipping, masks
and ticket tearing are not native APIs. Use the explicit native import for TS.
`intensity` and `hue` are 0–1, `borderRadius` defaults to 16. Drag horizontally
to acquire the gesture, then move in either direction; vertical swipes remain
with the parent ScrollView. Release/cancel settles to center. Multitouch never
adds rotation. `resetKey` resets when content changes. No idle frame loop: only
dragging/settling updates the shader. Set `visible` from navigation focus and
viewport visibility; `paused`, background, provider pause and OS Reduce Motion
remove the shader, reset the pose and retain the ordinary image.

For edge-to-edge square artwork on the web, `FoilSurface` accepts `inset={0}`
(default preserves the ticket demo's framing). Explicit inset is 0–.25, honored
by rendering, fallback and pointer projection. Set `aspectRatio={1}`,
`tearable={false}`, `idleMotion={0}` and a restrained `intensity` for album covers.
The touch action is confined to the artwork; keep scrollable controls outside it.

Native `renderFoil={false}` skips loading/mounting Skia while retaining the image
and perspective gesture; use it on unsupported renderers and Android emulators.

Foil shadows belong to the moving material: the DOM renderer projects the same
mesh for its shadow passes, and native draws a Skia drop-shadow underneath the
transformed card. Avoid an additional fixed wrapper box-shadow/elevation. Web
`shadowOpacity` (0–1, default .14) controls the projected shadow, and
`cornerRadius` (0–.25 in UV units, default 0) rounds both print and shadow.
Reserve canvas space with `inset` and a correspondingly larger centered surface;
keep the outer view unclipped so bending and shadows can extend past the cover.

The DOM foil suppresses the larger canvas hit-area outline on pointer focus;
keyboard navigation retains a visible ring inset around the printed material.

Both DOM and native foil accept `iridescence` (0–1, default 1) independently of
`intensity`: lower it to mute rainbow saturation while retaining metallic gloss.
Zero yields a neutral silver laminate, not a transparent/disabled effect.

DOM `imageFit="cover"` preserves portrait/landscape artwork proportions with
center cropping, matching ordinary album-cover images; default `stretch` keeps
existing ticket printing. Masks follow the same cropped artwork UVs.
