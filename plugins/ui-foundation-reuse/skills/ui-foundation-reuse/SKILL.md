---
name: ui-foundation-reuse
description: Reuse bundled ui-foundation effect code and scene helpers alongside Taste, Impeccable, img2threejs or the visualizer in compatible React projects. Works without a library download using the included local runtime archive. Prefer existing effects before rebuilding shaders, scroll motion or scene infrastructure; maintain the bundle when library capabilities change.
---

# Reuse ui-foundation

Prefer the project's existing `@sigmastudioz/ui-foundation` implementations before writing equivalent effects or scene infrastructure. Apply this alongside Taste, Impeccable, img2threejs and the visualizer while preserving their design, reconstruction and video workflows.

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
An export missing one option or default is a library gap: bridge with exported `/core` primitives; name the missing option as the demonstrated gap.

If the archive is missing or damaged, report an incomplete skill installation instead of trying to download the library. If local installation or a required peer is unavailable, report that specific gap and continue independent design work where possible. Never invent working imports, assume access to another machine, change an existing dependency source silently, or substitute a duplicate effect without explaining the gap. Respect review-only scope.

## Capability search map

Subpaths below are relative to `@sigmastudioz/ui-foundation`. Confirm availability in the installed manifest before using them.

| Requested behavior | Inspect these public subpaths first |
| --- | --- |
| Shader backgrounds, liquid metal/glass, glass distortion | `/gradient`, `/liquid-metal`, `/liquid-glass` (CSS/SVG, any content), `/fluted-glass`, `/iridescence`, `/iridescent-ribbon` |
| True-refraction liquid glass over a provided image or video (bevel, chromatic aberration, merging lenses) | `/refractive-glass`: `RefractiveGlass`, `GlassLens` (WebGL 1; refracts its own backdrop, not live DOM) |
| Video/frame scrubbing, scroll chapters, depth and parallax | `/scroll-scrub`, `/scroll-3d`, `/mouse-parallax`, `/camera-journey`; `/scroll-reveal`: `StickyReveal` (pinned heading) |
| Scroll entrance reveals, split text, typewriter, count-up, text fill | `/scroll-reveal`: `Reveal` (fade/slide/blur/clip/scale + `stagger`), `SplitReveal`, `Typewriter`, `CountUp`, `TextFill`, `useRevealTrigger`; low level: `/core` `useInView` (`inView` starts `true` until observed), `useScrollProgress` |
| Landing-page scroll layouts | `/scroll-layout`: `StackingCards`, `HorizontalScroll`, `VelocityMarquee`, `ScrollColor` |
| Scroll-aware navigation | `/scroll-nav`: `HideOnScroll`, `useScrollDirection`, `useScrollSpy` |
| Pointer attraction, particles, fluid motion, text effects | `/magnetic`, `/particle-form`, `/particles`, `/fluid-field`, `/kinetic-text`; `/luminous-trails`: `LuminousTrails`, `TRAIL_PATHS` (glowing parametric ribbons) |
| Procedural GPU volumes without Three: dust nebula, plasma ribbon, tree-to-brain fibers | `/particle-nebula`: `ParticleNebula`; `/plasma-vortex`: `PlasmaVortex`; `/neural-field`: `NeuralField`, `NEURAL_COLORS` |
| Headless 2D spring/collision simulation for app-drawn bodies | `/force-2d`: `useForceSim`, `stepForceSim`, `syncForceBodies`, `DEFAULT_FORCE_SIM_CONFIG` (paints through `onFrame`; reduced motion paints rest poses) |
| Image transitions, filters and material treatments | `/image-transition`, `/image-filter`, `/heatmap`, `/foil-surface`, `/light-glow`, `/text-portrait` |
| Image refraction, liquid bulges, strip displacement and localized stretch | `/lens-distortion`: `LensDistortion`; `/moving-blobs`: `MovingBlobs`; `/slice-shift`: `SliceShift`; `/pixel-stretch`: `PixelStretch`; `/image-warp`: `ImageWarp` |
| Print dots, dithering and square image cells | `/halftone`: `Halftone`; `/pixelate`: `Pixelate`, `PixelateTransition` (stepped pixel-resolution reveal), `pixelateTransitionFrame`; `/dither`: `Dither`, `DITHER_PRESETS`, `resolveDitherConfig`, `errorDiffuse` (Bayer 4/8, Floyd–Steinberg, Atkinson) |
| Glitch, datamosh, RGB split and block shift on still images | `/glitch`: `Glitch`, `glitchAmount`, `scrollGlitchEnvelope` |
| Image to particles: assemble, dissolve to dust, burst; depth-map parallax; audio-reactive | `/image-particles`: `ImageParticles`, `resolveImageParticlesConfig`, `buildParticleField`, `particleState`, `MAX_IMAGE_PARTICLES` |
| Blob-tracking HUD: bracketed boxes, IDs, crosshairs and links over moving or bright subjects | `/blob-track`: `BlobTrack`, `findBlobs`, `matchBlobs`, `signalField`, `motionField` (image or muted video; needs CORS-readable media) |
| Cursor-following gooey reveal of a second image | `/gooey-reveal`: `GooeyReveal`, `stepTrail`, `trailRadii` (SVG mask + goo filter, no WebGL) |
| Two-sided flip cards and a lanyard badge that swings when dragged | `/flip-card`: `FlipCard`, `LanyardBadge`, `stepPendulum`, `dragAngle` |
| LED dot-matrix sign or marquee | `/dot-matrix`: `DotMatrix`, `textColumns`, `matrixFrame`, `marqueeOffset` (built-in 5×7 font) |
| Radial zoom or spin blur with highlight glow | `/zoom-blur`: `ZoomBlur`; also `ImageFilter kind="zoom-blur"` with `blurMode` |
| Reaction-diffusion, Turing patterns and slime-mould (physarum) tiles | `/reaction-diffusion`: `ReactionDiffusion`, `GRAY_SCOTT_PRESETS`, `stepGrayScott`, `stepPhysarum`, `seededRandom` |
| Night vision, thermal receipt print and on-camera flash looks | `/image-filter`: `ImageFilter` with `preset` from `IMAGE_FILTER_PRESETS` (`night-vision`, `receipt`, `flash`); `bayerThreshold` mirrors the ordered-dither matrix |
| Retro print and signal still-image treatments (three presets each on the shared `/image-filter` host) | `/posterize`: `Posterize`; `/stipple-duotone`: `StippleDuotone`; `/glyph-grid`: `GlyphGrid`; `/thermal-noise`: `ThermalNoise`; `/phosphor-ghost`: `PhosphorGhost`; `/liquid-screen`: `LiquidScreen`; `/xerox-collage`: `XeroxCollage`; `/raster-lines`: `RasterLines`; `/solarized-streak`: `SolarizedStreak`; `/teletext-pattern`: `TeletextPattern`; each also exports its `*_PRESETS` (`PhosphorGhost` has four: cyan, green, amber, magenta) |
| Traced contour, Delaunay, dither and circle-chain fields from a photo or procedural source | `/geometric`: `Geometric`, `GEOMETRIC_PRESETS`, `resolveGeometricConfig`, `buildGeometricScene` |
| Film grain and miniature-focus overlays above live content | `/grain`: `Grain` (pointer-transparent noise overlay); `/tilt-shift`: `TiltShift` (masked backdrop blur; content stays clear without backdrop filtering) |
| Media layouts, panels and transitions | `/media-strip`, `/media-carousel`, `/scene-panel`, `/layout-morph`, `/object-stack`, `/media-disclosure`; `/recursive-viewport`: `RecursiveViewport`; `/adaptive-surface`: `AdaptiveSurface`; `/motion-video`: `MotionVideo` |
| Spatial interfaces, floating objects and tactile media | `/spatial-canvas`, `/floating-objects`, `/crt-surface`, `/disc-carousel` |
| Paper, brush and aperture reveals | `/paper-motion`, `/aperture-reveal` |
| Square-tile wipes, glyph curtains, scratch cards and pointer-scrubbed film | `/square-tile-reveal`: `SquareTileReveal`; `/glyph-curtain`: `GlyphCurtain`, `GlyphCurtainHandle`; `/scratch-reveal`: `ScratchReveal`, `ScratchRevealHandle`; `/cursor-video`: `CursorVideo` (silent; never plays audio) |
| Audio-reactive and environmental effects | `/visualizer`, `/cymatics`, `/weather`; React Native: `/visualizer/native`: `Visualizer`, `createSmoothedAudioSource`, `EffectsProvider` (Skia renderer, no DOM or microphone access) |
| React Native blur surfaces and remote images, with web counterparts | `/frosted-blur`, `/frosted-blur/native`: `FrostedBlur`, `resolveFrostedBlurType`; `/remote-image`, `/remote-image/native`: `RemoteImage`, `AnimatedRemoteImage`. Native entries accept app-injected blur/image backends; web entries render through the optional `react-native-web` peer and stay SSR-safe without it |
| Rain beads and sliding drops refracting a blurred still image | `/rain-on-glass`: `RainOnGlass` |
| 3D hosting, staging and models | `/three`: `Scene`, `World`, `Model`, `Float`, `GlassMaterial`, `Portal`, `ReflectiveFloor`, `SoftShadows`, `Bloom`, `Caustics`, `ExplodedAssembly`, `useSceneMotion`. `Model` and `Float` accept `onError` when their runtime cannot load. `World` then shows its install fallback. |
| Rigid-body scene content | `/physics`: `BallPit` loads `@react-three/rapier` on mount and accepts `onError`. `/physics/rapier`: `Physics`, `RigidBody`, `CuboidCollider`, `BallCollider`, `CapsuleCollider` (this subpath evaluates the peer at import). |
| Shared lifecycle, visibility, interaction and quality policy | `/core`: `EffectsProvider`, `useEffectsSettings`, `useRafLoop`, `useReducedMotion`, `useInView`, `usePageVisible`, `useWebGLEffect`, `useScrollProgress`, `useInteraction`, `useAdaptiveQuality` |

Every `/native` subpath (`/visualizer/native`, `/foil-surface/native`, `/frosted-blur/native`, `/remote-image/native`) requires the optional `react-native` peer (>=0.77) and the host app's native build; `/visualizer/native` and `/foil-surface/native` also lazy-load the optional `@shopify/react-native-skia` peer and keep a static fallback without it. The remaining subpaths are web React DOM entries that need no native or Three peers unless their row says so.

Search the full installed exports if the selective map has no match. Inspect `/presets` when available for existing configurations and composition patterns. `npm run check:skill` fails when a public export subpath is missing from this guide.

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

### Dither, glitch, image particles, filter presets and pixel transitions

All five are React DOM >=18.2, SSR-safe (the semantic `<img>` renders on the server
and remains the loading/error/CORS fallback) and need no Three peers. Each requires
`src` and `alt` (empty for decorative art). Remote images need CORS. Images use a
center-cropped cover fit. None process video: pass still images or poster frames.

- `/dither` `Dither`: `algorithm` `bayer4`/`bayer8` runs as the `dither` kind of the
  shared `/image-filter` WebGL 1 pass; `floyd`/`atkinson` diffuse error on the CPU
  through Canvas2D (bounded to 409,600 cells; larger frames get bigger cells). Both
  are static: no RAF loop; they redraw on source, size or control changes. `preset`
  `newsprint` (default, Bayer 8, 1-bit), `gameboy` (Bayer 4, four LCD greens) or
  `blueprint` (Atkinson, pale on blue). `levels` 2–16, `cellSize` 1–16 CSS pixels,
  `contrast` .1–3, `invert`, `intensity` 0–1 (CPU path blends by canvas opacity).
  `palette` (2–16 hex stops dark→light) beats `ink`/`paper`, which beat the preset.
  `errorDiffuse(light, columns, rows, 'floyd'|'atkinson', levels)` is the pure kernel.
- `/glitch` `Glitch`: `kind` `datamosh` (drifting macroblocks), `rgb-split` (default;
  channel offset plus seeded row tears, `offset` CSS px, `angle`) or `block-shift`
  (`slices` bands jump sideways). `intensity` 0–1 is the peak amount (it is not the
  image-filter blend). `trigger`: `always`, `hover` (pointer hover or focus within),
  `interval` (bursts at the end of every `interval` 1–30 animation seconds; phase zero
  is clean), `scroll` (full while entering the viewport, clean by its center) or
  `progress` (`intensity × progress`). Motion is a pure function of the gated phase,
  `seed` (0–1000) and position; `speed` 0–3 scales the phase. Zero amount pauses the
  loop and shows the original. Reduced motion, provider pause, offscreen and hidden
  tabs freeze the phase; starting under reduced motion keeps interval bursts clean.
  `cellSize` sets the datamosh block and tear-row size. Only `scroll` subscribes to
  scroll. The host div receives `className`/`style`; give it a height.
- `/image-particles` `ImageParticles`: Canvas2D particle field sampled from the image
  (one particle per `density` 2–24 CSS px, capped at 16,000; dark/transparent samples
  below `threshold` are skipped). `mode`: `gather` (scattered → image; autoplays over
  `duration`/`delay` ms once in view, `onComplete` once), `drift` (image dissolves
  upward) or `splash` (radial burst); drift/splash rest at progress 0 and are driven
  by controlled `progress` (for example from `useScrollProgress`). `depthSrc` (white =
  near; failure is reported and falls back to luminance) feeds `depth` 0–1 parallax,
  perspective size and splash spread. `pointer` repels within `pointerRadius`;
  `trails` 0–.95 fades instead of clearing; `ambient` 0–1 wander and `speed` 0–3.
  `audioSource` accepts a caller-owned `VisualizerAudioSource` (for example
  `createAudioAnalyser` from `/visualizer`); amplitude adds wander, bass enlarges.
  `colorMode` `source` (64 buckets) or `monochrome` with `color`; `backgroundColor`
  fills the host. Positions are a pure function of progress, phase, seed, pointer and
  audio (trails accumulate frames). The default `ambient` .15 keeps a gentle loop;
  with `ambient={0}` and no audio, trails, pointer hover or autoplay, no RAF runs.
  Reduced motion draws the formed image without pointer, audio or wander.
  Use it for still images; it is not a WebGL/GPU particle system or a 3D point cloud.
- `/image-filter` presets: `<ImageFilter preset="night-vision">` (green phosphor,
  heavy grain), `receipt` (thermal receipt printer: 2-px Bayer 8 dots, warm ink) and
  `flash` (centered exposure falloff, highlight bloom, dark corners). A preset sets
  the kind; any explicit prop, including `kind`, overrides it; undefined props do not.
  New generic kinds: `dither` (`ditherMatrix` 4/8, `levels`, `colorRamp` or
  `backgroundColor`→`color`, `cellSize` 1–64), `flash` (`distortion` exposure,
  `center`, `radius`, `glow`, `threshold`, `cellSize` bloom spread, `contrast`,
  `grain`) and `glitch` (`glitchMode`, `distortion`, `seed`, `interval`, `slices`,
  `offset`). The pink-phosphor monitor is `PhosphorGhost preset="magenta"`.
- `/pixelate` `PixelateTransition`: stepped pixel-resolution transition on the shared
  pass. `direction` `in` (coarse → clear, default) or `out`; `from` 8–128 CSS px,
  `steps` 2–12; autoplays over `duration`/`delay` ms once in view, or follows a
  controlled `progress`. React renders only on step changes; the end frame is the
  untouched image with no loop. Reduced motion shows the end frame and completes.
  `pixelateTransitionFrame(progress, { from, steps, direction })` is pure. `Pixelate`
  stays static.

### Blob tracking, gooey reveal, flip cards, dot matrix, zoom blur and reaction-diffusion

- `/blob-track` `BlobTrack`: `src`, `alt`, `media` `image` (default) or `video` (muted,
  looping, inline). `signal` `brightness` (default), `darkness` or `motion` (video only;
  stills fall back to brightness). `threshold` 0–1 (.7), `maxBlobs` 1–24 (8), `minArea`
  .0005–.2 of the frame (.004), `resolution` 32–160 analysis columns (96), `color`,
  `labels`, `crosshair`, `links`, `onBlobs(blobs)` with normalized boxes and stable IDs.
  Detection reads pixels, so cross-origin media needs CORS (`crossOrigin`); a tainted
  source calls `onError` and shows the media without a HUD. Video analysis pauses off-screen,
  when paused and under reduced motion (the first frame is analyzed once).
- `/gooey-reveal` `GooeyReveal`: `coverSrc`, `revealSrc`, `alt`, `revealAlt`; a chain of
  `trail` 0–12 (6) blobs of `radius` 12–240 px (70) follows the pointer at `follow`
  .05–1 (.32) and merges through a blur/alpha-threshold `goo` 2–40 (14). Enter/Space or
  controlled `revealed` + `onRevealedChange` reveal the whole image. The loop sleeps once
  settled; reduced motion uses one blob that snaps to the pointer.
- `/flip-card` `FlipCard`: `front`, `back`, required `label`; root is a toggle button with
  `aria-pressed`, so keep faces free of their own controls (or use controlled `flipped`
  with an app-owned button). `trigger` `click` (default) or `hover` (fine pointers preview),
  `axis` `y`/`x`, `duration` 150–2000 ms. The hidden face is inert; reduced motion
  crossfades. `LanyardBadge` hangs a `FlipCard` from a strap (`strapLength` 40–400,
  `strapColor`, `size`, `damping` .9–.999): drag swings a damped pendulum, a click or
  Enter flips, Arrow keys nudge. Physics is CSS-transform only (no physics engine).
- `/dot-matrix` `DotMatrix`: `text` in the built-in 5×7 font (A–Z, 0–9, common punctuation;
  lowercase maps to uppercase, others show a box), `columns` 16–240 (64), `padding` rows
  0–4 (1), `mode` `scroll` (marquee, `speed` 1–120 columns/s) or `static`, `color`,
  `background`, `offOpacity`, `glow`, `shape` `round`/`square`. Exposed as `role="img"`
  named by `label` or the text. Redraws only when the window moves a column; reduced
  motion renders static.
- `/zoom-blur` `ZoomBlur`: `mode` `zoom` (default, outward streaks) or `spin` around
  `center`; `distortion` strength (.55), `threshold` where glow starts (.7), `glow` (.6).
  Static by design: drive `distortion` or `center` from scroll/pointer for motion. Same pass
  as `ImageFilter kind="zoom-blur" blurMode=...`.
- `/reaction-diffusion` `ReactionDiffusion`: `model` `gray-scott` (default; `preset`
  `coral`, `mitosis`, `maze`, `spots`, `worms` or explicit `feed`/`kill`) or `physarum`
  (`agents` 500–20000). CPU grid of `resolution` 64–256 (128) on a torus, so `tiles` 1–6
  repeat seamlessly; `stepsPerFrame`, `colors` [background, ink] hex, `seed`, `interactive`
  pointer seeding. Pauses off-screen; reduced motion grows the pattern once and holds it.
  Higher resolutions cost roughly resolution² per step; prefer 128 for full-bleed backgrounds.

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

### Landing-page scroll names

Map these common landing-page animation names to exports before writing scroll code.
All are React DOM >=18.2, SSR-safe and need no Three peers.

| Name | Use |
| --- | --- |
| fade-in, slide-in, blur-in, clip-path reveal, scale-in | `Reveal variant="fade" / "slide" (default) / "blur" / "clip" / "scale"`, `direction` up/down/left/right |
| stagger | `Reveal stagger={ms}` wraps each direct child (in `li` inside `as="ul"/"ol"`, so pass non-`li` children) |
| split-text reveal | `SplitReveal by="word" / "char"` (in flow); pinned word reveal: `StickyReveal` |
| typewriter | `Typewriter text="…"` or an array of phrases (types, holds, deletes, loops) |
| count-up | `CountUp to={…}` with `decimals`, `locale`, `format`, `prefix`, `suffix` |
| scroll-linked | `/core` `useScrollProgress`; CSS `animation-timeline: scroll()` where support suffices |
| parallax / scroll zoom | `/scroll-3d` `ScrollParallax` (`translateY`, `scale={[a,b]}`), `ScrollLayer`; pointer: `/mouse-parallax` |
| scroll-scrubbed image sequence | `/scroll-scrub` `ScrollScrubFrames`, `useFrameSequence`; video: `ScrollScrubVideo` |
| pin + scrub, scrollytelling | `ScrollScrubVideo`/`ScrollScrubFrames` (pinned), `useScrollProgress({ range: 'sticky' })`, `ChapterStage` + `createScrollTimeline` |
| SVG line draw | recipe, no export: `<path pathLength={1} strokeDasharray={1} strokeDashoffset={1 - progress}>` with `useScrollProgress` |
| text fill on scroll | `TextFill` (word-by-word background-clip fill; `from`/`to` viewport progress) |
| background colour transition | `ScrollColor colors={[…]} textColors={[…]} mode="blend" / "step"` around sections |
| marquee with scroll velocity | `VelocityMarquee` (window scroll; `scrollBoost`, `reverseOnScrollUp`); LED sign: `/dot-matrix` |
| stacking cards | `StackingCards items={[{ id, content }]}` |
| horizontal scroll | `HorizontalScroll` (pinned; native scroller under reduced motion) |
| hide-on-scroll header | `HideOnScroll` (position it sticky/fixed yourself) or `useScrollDirection` |
| scrollspy | `useScrollSpy(ids)` → active id for `aria-current` |
| position sticky, CSS scroll snap | plain CSS (`position: sticky`, `scroll-snap-type`); no export |

Behaviour shared by the entrance components: the server render and the first client
render are visible; before first paint the element is hidden and an
IntersectionObserver reveals it (`once` default true, `threshold` .15). Without an
observer or under reduced motion they stay visible with no motion. `Reveal`/`SplitReveal`
use CSS transitions only (no RAF loop). `SplitReveal`, `Typewriter`, `CountUp` and
`TextFill` render one visually hidden copy of the final text for screen readers and
mark the animated glyphs `aria-hidden`. `Typewriter` and `CountUp` drive `/core`
`useRafLoop` and stop when finished.

`/scroll-layout`: `StackingCards` uses `position: sticky` per card plus one rAF-throttled
scroll read for scale/dim (`top`, `offset`, `gap`, `scaleStep`, `minScale`, `dim`);
reduced motion keeps the stack without scaling. `HorizontalScroll` measures its track,
sets its own height and moves the track with vertical scroll; keyboard focus scrolls
the page to the focused item. Under reduced motion, or when nothing overflows, it is a
native horizontal scroller. `VelocityMarquee` repeats one run to fill the row (extra
runs `aria-hidden`; keep runs free of focusable controls; `marqueeCopies` gives the count), writes transforms directly,
pauses off-screen and in background tabs, and is still under reduced motion.
`ScrollColor` defaults to `range="sticky"` (element top at viewport top → bottom at
viewport bottom); colour changes also run under reduced motion, without `step` transitions.

`/scroll-nav`: `useScrollDirection({ threshold, topOffset })` and `HideOnScroll` read
window scroll; the header stays visible near the top and while it contains focus.
`useScrollSpy(ids, { rootMargin })` observes element ids in a band ~45% down the
viewport, follows sections that mount later or are replaced (duplicate ids count once),
and selects the last id at the page bottom.

### Refractive glass

Import `RefractiveGlass` and `GlassLens` from `@sigmastudioz/ui-foundation/refractive-glass`.
React DOM >=18.2, WebGL 1, no Three peers, no dependencies. Give `RefractiveGlass` a `src`
(image, or `media="video"`: muted, looped, inline, paused under reduced motion; give it a
`poster`, which is refracted until the first video frame is available), `alt`
and either a size or content that sizes it. Every `GlassLens` inside (up to 8, any
layout, `as` div/section/aside/button/a…) is measured from the DOM and its box and
computed `border-radius` (or `radius`) become a lens; its children stay crisp DOM.
Controls: `refraction` 0–1 (.6), `bevel` 2–160 px (28), `chromatic` 0–1 (.35),
`frost` 0–24 px (0), `magnify` 0–.5 (.06), `specular` 0–1 (.55), `tint` hex and
`tintStrength` 0–1 (.06), `merge` 0–160 px (0) fuses nearby lenses with a smooth union.
Static image backdrops redraw only on size, lens-geometry or control changes; pass
`live` for lenses moved by transforms or animation (re-measured every frame).
Browsers expose no page pixels to WebGL/WebGPU, so it refracts this backdrop, not
arbitrary DOM behind it: put the content you want refracted in the image/video, or use
CSS `/liquid-glass` over live DOM. Remote media needs CORS. The media element is the SSR,
loading and failure fallback; on WebGL loss or a tainted source lenses switch to CSS
frosted glass and `onError` reports it. `GlassLens` outside `RefractiveGlass` is CSS glass.
Pure helpers: `resolveRefractiveGlassConfig`, `lensRect`, `packLenses`, `lensKey`,
`parseTint`, `MAX_GLASS_LENSES`; renderer: `createRefractiveGlassRenderer`.

## Apply alongside each design skill

The maintainer playground's `?studio=1` route offers app-owned **Art direction**
recipes (Powerful, Bold, Rich) on its six material effects. Select a palette,
compare its accent on/off, and copy React/JSON, role CSS or a share link.
Color/finish inputs are mapped through the existing control schema; speed and
quality settings are retained. Single-ink effects use the accent over the ground;
scene assets are not recolored. Recipe colors, typography guidance, CSS roles and
the editor UI are playground content, not new runtime exports or capabilities
bundled with this offline skill. Copied effect code uses the existing public
subpaths; consumer layout, branding, type and artwork remain app-owned.

- **Taste:** use its direction, composition and review process; implement matching motion and material effects with library exports. Its handwritten effect recipes are alternatives after the reuse check establishes a gap. Keep typography, brand tokens, page structure and content in the consuming app.
- **Impeccable:** refine composition, styling, effect configuration and accessibility around library components. Do not replace a reusable shader or scene helper merely to satisfy a generic aesthetic detector. Honor explicit visual intent; investigate correctness or performance problems at their owning layer. Keep reviews read-only.
- **img2threejs:** its staged pipeline owns subject-specific geometry, materials and reconstruction evidence. Reuse the library for hosting and generic staging instead of generating another Canvas, asset loader, orbit controller or ambient float implementation. Keep custom subject geometry and unmet material requirements in the generated asset.
- **SigmaStudioz Visualizer (`visualizer`, which includes the former `visualization-videos` workflow):** reuse compatible effects and scene helpers for React video previews and supported exports. The video project owns its storyboard, captions, custom geometry, canonical timeline and encoder. Check actual clock/seeking contracts before promising deterministic capture; live RAF animation or scene pause alone is not a frame-driven export API. Verify effects in the encoded video. Keep Pillow/FFmpeg and non-React renderers when appropriate; add only a demonstrated, authorized adapter or report the compatibility/export gap.

These companion skills are independent installations. This guide does not install them or require all of them to be present.

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


### Shape patterns / generative SVG

Import `ShapePattern`, `SHAPE_PATTERNS`, `resolveShapePatternConfig`,
`buildShapePattern`, `createShapePatternSvg`, `SHAPE_PATTERN_CONTROLS`,
`defaultShapeParameters` and `shapePatternHasMotion` from
`@sigmastudioz/ui-foundation/shape-pattern`. React DOM >=18.2, SSR-safe SVG;
no WebGL, Canvas, textures or optional renderer peers. 23 kinds: `waves`,
`dots`, `letters`, `quarters`, `arcs`, `cubes`, `helix`, `rings`, `cube-frame`,
`flow-lines`, `flow-poles`, `flow-dots`, `chevron`, `triangles`, `nodes`,
`interference`, `spiral`, `broken-ring`, `truchet`, `butterfly`, `iso-cross`,
`scattered-cubes`, `iso-sphere`.
This is independent of `/geometric` image/field tracing. Preview and SVG export
use the same deterministic marks. Give the component dimensions/aspect ratio.

Use `parameters` for each shape's controls in the filmed/reference UI units.
The frozen `SHAPE_PATTERN_CONTROLS[pattern]` schema supplies labels, parameter
keys, limits, steps and defaults; `defaultShapeParameters(pattern)` returns a
fresh numeric parameter object. Top-level `seed`/`text` remain the Seed/Word
controls. Word is capped at 12 printable characters and uses editable Georgia/
serif text with variable-size seeded tiles; no glyph outlines or exact cross-
machine font guarantee. Text and SVG labels are escaped. Colors accept hex.

- `waves`: lineCount, waveWidth, waveAmplitude, noiseScaleX, noiseScaleY,
  ySpread, envelopeSharpness, verticalFade, softness; coherent, enveloped noise.
- `dots`: gridSize, dotSpacing, falloffRadius, circleRadius, falloffStrength;
  open circles repelled from the center of the square field. The workshop puts
  the current site’s extra falloffStrength under Additional controls so the four
  filmed sliders remain the primary panel.
- `letters`: gridDimension; plus top-level seed and text.
- `quarters`: tiles, density, gap; plus seed. Each tile has four inward-facing
  quadrants, with independently seeded visibility.
- `arcs`: spacing, rows, cols; independent rectangular dimensions.
- `cubes`: rows/cols (1–100 each); pale top faces and vertical outlines, aggregated
  into two SVG paths rather than up to 30,000 DOM elements.
- `helix`: cubeSize, helixAmplitude, helixCount (0–500), helixFrequency,
  cubeHeight; separate wireframe cubes, not a continuous line ribbon.
- `rings`: ringCount, minRadius, maxRadius, ringAmplitude. Radius units are half
  the 1000-unit artwork coordinates; min is clamped to max. Fractional counts
  round up when generating geometry; zero counts yield empty artwork.
- `cube-frame`: frameSize (3–20), gap; only the twelve boundary edges contain
  cubes (up to 224 cubes), with painter ordering.

- `flow-lines`: domain, separation, stopDistance; plus seed. Spatially indexed
  bidirectional streamlines through an arithmetic vector field.
- `flow-poles`: poles, poleRing, turn, poleCore, separation, scatter; plus seed.
  Vortex/sink field. Turn 0 and 360 are the same orientation.
- `flow-dots`: turbulence, wavelength, flowDotSpacing, dotSize, strands, format;
  an ordered grid unraveling into strands. Circles aggregate into one path.
- `chevron`: bands, taper, bandRatio, blocks; plus seed. Ruled rhombus faces.
- `triangles`: cols, rows, chaosStart; plus seed. Pinwheel tiles dissolve downward.
- `nodes`: nodeSize, connectionDensity, displacement, cols, rows; plus seed.
- `interference`: meshGrid, spacing, meshFrequency, meshAmplitude,
  sourceSeparation. Two radial waves displace horizontal lines.
- `spiral`: cols, rows, morph, turns, radius, noiseAmount, noiseScale;
  rectangular mesh morphing toward a spiral.
- `broken-ring`: sides, rings, holeRadius, warpAmount, noiseScale,
  fillNoiseScale, fillThreshold. Noise-masked annular polygon cells.
- `truchet`: arcCount, cols, rows, arcRatio; plus seed. Quarter-arc tiles.
- `butterfly`: arcCount, cols, rows, rowOffset, arcRatio; mirrored semicircles.
- `iso-cross`: resolution (1–5), gap; cube corners carved into crossing beams.
- `scattered-cubes`: gridDimension (3–16), gap, layers (2–16), noiseScale,
  displacement; plus seed. Outward-displaced layered cube surfaces.
- `iso-sphere`: dimension (3–40), gap; sphere carved from a voxel lattice.

These 14 added gallery families are static (no autoplay/RAF). Streamline work
is bounded to 450 paths / 60,000 integration steps, so the densest requests may
stop before filling the page. Voxels cull internal faces and group surfaces by
depth; no Three dependency. Filled motifs use size/ratio controls rather than
stroke width. Reuse the exact per-kind schema; do not offer every parameter to
every shape. The workshop includes searchable selection and SVG/React/JSON,
poster, download and shared-link support for all 23 kinds.

Existing generic count/amplitude/frequency/size/radius inputs remain accepted
aliases where applicable; explicit parameters win. Existing v1 share links load.
New editor exports use canonical parameters. `strokeWidth` .25–5 and `rotation`
-180–180 remain additional print controls. SVG uses a 1000-square viewBox;
nonsquare hosts letterbox. `label` names artwork; empty/omitted is decorative.

Static by default. `shapePatternHasMotion` enables optional autoplay for waves,
dots, arcs, helix and rings. Quarters, letters, cubes and cube frames stay static.
`animated`, `speed` 0–3, `paused` and explicit `time` 0–3600 retain their contracts.
An explicit time is a static frame and disables autoplay. The integrated clock
loops smoothly every 20π seconds; speed/pause retains phase. Core owns reduced
motion, provider pause, hidden-tab/offscreen suspension. Export takes config plus
`{time,width,height,label}` (dimensions 64–8192, default 1000); no external media
or scripts. Helpers need no DOM; the subpath component still requires React.

The `/shape-patterns.html` workshop provides reference control panels, editing,
SVG/React/JSON copying, downloads, links and a poster layout. Its composition,
recipe names, branding and typography are app-owned and are not offline-runtime
templates. Geometry is an independent reconstruction from the supplied footage
and visible reference controls, with no original source/SVG/font bundle.
