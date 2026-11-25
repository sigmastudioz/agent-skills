# ui-foundation effect API

Detailed props, defaults, compatibility and constraints for the effects named in the capability
map of [SKILL.md](../SKILL.md). Check the installed declarations when a version differs.

The image-effect facades in the capability map (for example `/dither`, `/glitch`, `/halftone`, `/pixelate`, `/zoom-blur`) share `/image-filter`'s WebGL 1 texture pass;
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
- Glitch flash rate: the tear/slice pattern changes at most 3 times a second in real time
  at any `speed`, and `interval` bursts are lengthened when needed so they start and end at
  most 3 times a second (WCAG 2.3.1; `glitchPatternRate`, `glitchSafeInterval`,
  `MAX_GLITCH_CHANGES_PER_SECOND` from `/image-filter`). Continuous drift is not capped; keep large, high-contrast glitches brief.
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
  `aria-pressed`. Links, buttons and fields inside a face keep their own click, Enter and
  Space and do not flip the card (`FLIP_IGNORE`, `fromInnerControl`; add `data-flip-ignore`
  to opt out any other element). Screen readers still meet them inside a button, so prefer
  few controls per face, or controlled `flipped` with an app-owned button. `trigger` `click` (default) or `hover` (fine pointers preview),
  `axis` `y`/`x`, `duration` 150–2000 ms. The hidden face is inert; reduced motion
  crossfades. `LanyardBadge` hangs a `FlipCard` from a strap (`strapLength` 40–400,
  `strapColor`, `size`, `damping` .9–.999): drag swings a damped pendulum, a click or
  Enter flips, Arrow keys nudge. On touch only the badge captures the finger (strap and
  margins still scroll the page, `touch-action: pan-y`). Physics is CSS-transform only (no physics engine).
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
  pointer seeding (on touch, horizontal drags and taps seed while vertical swipes scroll the
  page: `touch-action: pan-y`). Pauses off-screen; reduced motion grows the pattern once and holds it.
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
| SVG line draw | `ScrollPath d viewBox from to` (one or several paths, optional `trackColor` and riding `marker`; `progress` for controlled drawing) |
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

### Page flip, card ring, type refraction and shard burst

All four are React DOM >=18.2 with no Three peers, SSR-safe (the server renders the
readable resting state), and honour reduced motion.

- `/page-flip` `PageFlip`: `pages` (ReactNodes in reading order; page 1 sits alone on the
  right). The book fills its container, two pages wide; `aspectRatio` is page height ÷ width
  (1.35). Turn by dragging or clicking a page, ←/→/PageUp/PageDown/Home/End on the focused
  book, or the built-in buttons (`controls`); `spread`/`defaultSpread`/`onSpreadChange`
  (0 = closed, 1 = pages 2–3). Scroll-linked: `progress` 0–1, or `scrollTrack` (e.g.
  '400vh') to pin it and turn with page scroll; both disable drag, keys and buttons.
  `curl` 0–1 (.6) and `segments` 2–16 (8) shape the curl, drawn as hinged strips
  (aria-hidden copies) only while a leaf turns; at rest each page is one real DOM face, and
  covered faces are `visibility: hidden` so they cannot take focus. A polite live region
  announces "Pages 2 and 3 of 8". Style pages with `pageClassName` and the
  `--page-flip-paper` colour. Interactive elements inside pages do not start drags (or
  mark any element `data-page-flip-ignore`). Only leaves within two of the open spread are
  mounted, so long books stay light; pages that move out of that window unmount and lose
  local state. Reduced motion turns instantly. Touch swipes work (`touch-action: pan-y`
  keeps vertical page scroll); a touch the browser takes for a scroll never turns a page.
  A turn writes strip angles straight to the DOM: React renders only when a different leaf
  starts or stops turning. CSS 3D only.
- `/card-ring` `CardRing`: `items` (`{ id, content, label? }`) around a cylinder sized from
  `cardWidth` (260), `gap` (28) and the item count; `aspectRatio` (1.35), `tilt` −30–30°
  (−8). Rotate by dragging, ←/→/Home/End, the buttons, or scroll (`progress` 0–1 from the
  first card to the last, or `scrollTrack`). `index`/`defaultIndex`/`onIndexChange`; it
  always rests with one card in front and turns the short way round. Only the front card is
  reachable: the others are `inert` and `aria-hidden`, with backfaces hidden; the front card
  is announced politely ("Project 2, 2 of 8"). Controlled (`index` set), the ring moves only
  when `index` changes: answer `onIndexChange` or it settles back. Spinning writes transforms
  straight to the DOM; React renders only when the front card changes. Reduced motion snaps.
  CSS 3D only.
- `/type-refraction` `TypeRefraction`: `text` (plain string) or inline `children` (`<em>`,
  `<span>`, links; each text node is drawn with its own computed font and colour), `as`
  heading tag. The heading
  stays real DOM text (screen readers, selection, SEO); while the effect draws, only its glyph
  fill (`-webkit-text-fill-color`) is transparent and a WebGL 1 copy, measured word by word from the browser's own layout
  (wrapping, font, `letter-spacing`, `text-transform`), is bent by a lens. `lens` `orb`
  (wobbling jelly bulge) or `crystal` (faceted hexagonal prism); `size` .1–2 (.6, in units
  of twice the font size), `strength`, `chromatic`, `wobble` 0–1, `speed` 0–3 (drift across
  the inked words; 0 parks it), `followPointer` (mouse/pen), `tint`, `color` (default the
  computed colour). Without WebGL, under forced colours or until the copy is ready, the plain
  heading shows; `onError` reports failures. Reduced motion parks the lens in the middle.
  The orb draws as clear glass (Fresnel rim, glints). The lens is a 2D refraction look, not a
  3D model (pair with `/three` for real geometry). Keep children inline; block children,
  images and form controls are not drawn into the refraction layer.
- `/shard-burst` `ShardBurst`: `src`, `alt`, `aspectRatio` (16/10; the image covers the box).
  A seeded jittered triangulation (`columns` × `rows` × 2 shards, default 70) flies apart in
  3D (`spread`, `depth`, `spin`, `fade`, `seed`) and back. Driven by scroll (`mode`: `both`
  assembles on the way in and breaks on the way out, `burst`, `assemble`) or a controlled
  `progress`. While whole it is one real `<img>`; shards exist only while broken, each a
  bounding-box-sized layer (keeps GPU memory near two images). Images only: arbitrary panels
  would need their DOM duplicated per shard. Reduced motion stays whole. No CORS needed.

### Swing rail

Import `SwingRail` from `@sigmastudioz/ui-foundation/swing-rail`. React DOM >=18.2, no
WebGL or Three peers, SSR renders the still rail. Pass `items` (`{ id, content }`); each
hangs on a string (`length` 0–400 px, default 64) below a rail, `gap` px apart, as a
labelled list (`label`). Moving the pointer across an item swings it (`push` 0–3, 1);
page scroll swings the row in alternating directions (`scrollSwing` 0–3, .4; 0 ignores
scroll); neighbours knock each other (`bounce` 0–1, .6; 0 passes through); `damping`
.9–.999 (.985). Swings are capped at `MAX_SWING_ANGLE` (~55°). `rail`/`strings` toggle the
lines, `color` styles both, `itemClassName` the item wrapper. Each item is the `/flip-card`
`stepPendulum`; transforms are written directly, the loop sleeps at rest and pauses
off-screen, and reduced motion hangs everything still and ignores input. Pointer brushing
needs a hovering pointer; touch users get the scroll swing. Keep each item one focus stop
or none. It is not `/force-2d`: that springs circles toward a home point with no pivot or
string, so it cannot swing hanging items. Pure helpers: `stepSwingRail`, `resolveNeighbours`,
`brushImpulse`, `scrollImpulse`, `itemAt`, `bottomSpan`, `swingOffset`, `railAtRest`.

### Drag gestures

`/core` `useDragGesture(options)` returns `{ handlers, pressed }`; spread `handlers` on the
draggable element. It owns the rules every press-drag-release surface needs: one pointer at a
time, a movement threshold (`slop`, 5 px on `axis` 'x' | 'y' | 'both') that separates a tap from
a drag, pointer capture (`capture`: `'drag'` by default, so a tap's click still reaches a child
control; `'press'` when children are replaced mid-gesture and the surface handles taps itself),
a swallowed click after a drag, and descendants that keep their own
clicks (`ignore`, default `DRAG_IGNORE`: links, buttons, form fields, `[data-drag-ignore]`).
Callbacks: `onStart(sample, event)` (return `false` to refuse), `onMove`, `onEnd` (a tap when
`sample.dragged` is false) and `onCancel`. A cancelled pointer (a touch the browser takes for
a page scroll) or a lost capture calls `onCancel` and never `onEnd`, so it cannot be mistaken
for a tap. `sample` carries `x`, `y`, `dx`, `dy`, `elapsedMs`, mean `velocityX`/`velocityY` in
px/s, `dragged` and `pointerType`. `PageFlip`, `CardRing`, `DiscCarousel` and `LanyardBadge` use it; reach for it before writing
pointer handlers for a new draggable surface. Keyboard control stays with the component.

### Scene input: lens, walk and look, lighting moods, device tilt

- **Lens in mm.** `/three` `lensToFov(mm, { aspect, filmGauge })` returns the vertical field of
  view three.js uses, with the same film convention as `PerspectiveCamera.setFocalLength`
  (35 mm gauge across the longer side; three.js's default, not full frame, which is 36 mm:
  pass `filmGauge: 36` to model a full-frame camera), so `Scene canvasProps={{ camera: { fov: lensToFov(50,
  { aspect: 16 / 9 }) } }}` matches `camera.setFocalLength(50)`. `fovToLens` is the inverse;
  `LENS_PRESETS` lists 14–200 mm primes. Pure maths, no Three peer; pass a lens-derived `fov`
  to `/camera-journey` waypoints the same way.
- **Walk and look.** `/three` `WalkControls` inside `<Scene>`: while the canvas has focus, W/S or
  ↑/↓ walk, A/D strafe and ←/→ turn (`turnSpeed` rad/s, 1.8). Keys are read by physical
  position (`KeyboardEvent.code`), so AZERTY and other layouts use the same positions. The
  canvas becomes focusable, `role="application"` and labelled with the keys (`label` names
  it). Mouse or pen drag looks, and on touch the left half of the canvas is a move stick and the right half looks.
  Props: `speed` (units/s, 2), `lookSpeed` (rad/px, .004), `eyeHeight` (1.6), `start` [x, z],
  `heading`, `bounds` [[minX, minZ], [maxX, maxZ]], `maxPitch` (1.2), `enabled`, `onError`.
  The camera stays on the ground plane; there is no collision with geometry, no pointer lock
  and no inertia, so under reduced motion it moves only while input is held. It sets the
  camera directly: do not combine with `Model orbit` or `/camera-journey`. Pure helpers:
  `stepWalk` (input `turn` −1…1), `keyAxes` (a set of key codes such as `KeyW`, `ArrowLeft`
  → `{ forward, strafe, turn }`), `stickAxes`, `createWalkState`, `resolveWalkConfig`.
- **Lighting moods.** One table, `resolveLightingMood('morning' | 'sunset' | 'storm' |
  'night')` (from `/core`, re-exported by `/three` and `/weather`): sky, fog, sun, sky/ground
  fill, environment strength, exposure, weather and a 2D grade. `/three` `<LightingMood mood>`
  inside `<Scene>` paints the sky (`background`), fog, a sun (`castShadow`) and fill, and adds
  `Environment` (`environment`) and `Finish` exposure (`finish`; turn off if you place your own
  `Finish`). It replaces your own sky and lights. `/weather` `SceneEnvironment mood` grades a
  photo with the same mood and adds its weather; explicit `grade` fields and `weather` win, and
  `weather={null}` removes it. The 3D component draws no rain: layer `<Weather
  {...resolveLightingMood(mood).weather}>` over the canvas (absolutely positioned, no pointer
  events). Mood changes are instant in 3D and use `durationMs` on the photo. `World` presets
  are separate and unchanged.
- **Device tilt.** `/core` `useDeviceTilt({ fallback: 'pointer' | 'none', range: 30,
  enabled })` returns `{ tilt, source, permission, requestPermission, recenter }`. `tilt.current`
  is `{ x, y }` in −1…1, written without re-rendering, so read it in your animation loop. The
  first device reading is the neutral pose (`recenter()` resets it); `range` degrees from it
  reach ±1, and the axes follow the screen rotation (a rotation resets the neutral pose). Until a reading arrives it follows the
  pointer over the window (or reports 0 with `fallback: 'none'`). It never prompts on its own:
  where `permission === 'prompt'` (iOS Safari, and Chromium builds that expose
  `requestPermission`), show a button that calls `requestPermission()` from the tap. Reduced
  motion or `enabled: false` gives `source: 'none'` and 0. Pure helpers: `screenTilt`,
  `normalizeTilt`, `pointerTilt`, `tiltPermissionState`.
- **Scroll-drawn path.** `/scroll-reveal` `ScrollPath` (see the scroll table): paths use
  `pathLength="1"`, so the server renders the finished drawing, the stroke hides only after
  hydration, and reduced motion or paused effects show it fully drawn. Without `label` it is decorative.
- **Gradient input.** `/gradient` `pointer` (true = .5, or 0–1) bends the field toward a mouse or
  pen over the gradient (touch ignored) and relaxes when it leaves; `audio` takes any
  `/visualizer` source (`sample()` → `{ amplitude, bass }`) and swells the waves,
  `audioReactivity` 0–2. Both are read per frame without rebuilding the renderer and are
  ignored under reduced motion. Only a structural type is shared with `/visualizer`, so a
  gradient-only bundle does not include it.

The playground's `scene-input.html` shows all of these together.

### Product configurator

A product page that spins a 3D model, recolours it per option and keeps the price current is
three existing or small pieces; the page, options, prices and copy stay in the app.

- **Spin.** `/three` `Model src="/product.glb" fit orbit autoRotate={.35}` inside `Scene`:
  OrbitControls turns the camera, auto-rotation stops while the shopper drags, and reduced
  motion, off-screen and hidden-tab states hold a still frame. `SoftShadows` grounds it.
- **Light.** `<Environment />` lights the scene from a built-in neutral studio room (no asset),
  or from your own equirectangular image with `src="/studio.hdr"` (`.hdr` or `.exr`):
  `intensity` 0–10 (1), `background` to show it behind the scene with `blur` 0–1, `rotation`
  in radians, `onError`. It is what gives metal and gloss something to reflect: a fully
  metallic finish (`metalness: 1`) renders near black without it. It adds to the lights
  already in the scene, so keep one or two directional lights for shape and lower them (the
  playground uses 1.5 and .6 with `intensity={.9}`). `<Finish toneMapping="neutral" />` sets
  the renderer's tone curve (`neutral` keeps brand colours closest to their swatches; `aces`
  and `agx` are filmic; `none` clips) and `exposure` 0–8; one per scene. Both restore the
  previous scene and renderer settings when removed. `<PostEffects ambientOcclusion
  depthOfField={{ focus, aperture, maxBlur }} bloom />` adds lens finishing on one chain, in
  that order, ending with the tone curve: ambient occlusion (`radius` in scene units, .4;
  `intensity` 0–2) darkens creases and contact, depth of field keeps `focus` (distance from
  the camera in scene units) sharp and blurs `aperture` of the frame per unit away from it up
  to `maxBlur`, bloom glows around light above `threshold` (keep ordinary surfaces below 1
  in linear light or raise it, or the whole frame washes out). `true` uses defaults;
  `resolution` caps the buffers (2048). One per Canvas, at the root, and not together with
  `<Bloom>` (use its `bloom` instead): a second chain reports through `onError`. With any
  effect on, the tone curve also applies to the scene background, so a plain background
  colour shifts slightly. Expensive: use `frameloop: 'demand'` for a still scene. Do not add `Environment` inside
  `World`, which already has one, or over a `Model lightmap` scene you expect to match its
  offline render (unlit baked surfaces ignore it; lit ones would be lit twice).
- **Recolour.** `Model materials={{ Shell: { color, metalness, roughness, emissive,
  emissiveIntensity, opacity } }}`, keyed by glTF material name, else mesh name, so author the
  asset with one named material per recolourable part. Matched parts get their own material
  copies (other instances of the same asset keep theirs, cached materials are never edited);
  each change resets the copy from the authored finish, so dropping a key restores it. Keys
  that match nothing are reported through `onError`. It composes with `lightmap`: colours apply to the
  source materials and the bake on top, so a colour change keeps the baked lighting (an unlit
  bake shows colour only; metalness and roughness need `lightmap={{ unlit: false }}`). `createMaterialVariants(root)` returns `{ apply(overrides) → unmatched keys,
  restore() }` for a scene loaded outside `Model`; `resolveMaterialOverride` clamps values.
- **Price and selection.** `/product-config` (React only, no Three peer, SSR-safe):
  `useProductConfig(product, { selection?, defaultSelection?, onSelectionChange? })` returns
  `{ selection, select(groupId, optionId), quote, materials }`. `product` is `{ basePrice,
  currency, groups: [{ id, label, defaultOption?, options: [{ id, label, priceDelta?,
  materials?, available? }] }] }`; every group is single-choice and always has an available
  option chosen (the default is `defaultOption` if available, else the first available one).
  Prices are whole numbers of the currency's minor unit (cents); a fractional price throws
  rather than drift. `quote` is `{ total, currency, lines }` with one line per group;
  `materials` merges the chosen options' recolouring in group order (later groups win) and is
  passed straight to `Model materials`. Unknown or unavailable options are ignored by `select`
  and replaced by the default when they arrive through `selection`. `formatPrice(minor,
  currency, locale?, signed?)` formats in the currency's own precision (+$20.00, ¥1,500). The
  pure `priceConfiguration`, `resolveSelection`, `selectionMaterials` and `defaultOptionFor`
  do the same without React. Prices shown here are display values: charge from the server's
  own price list, never from a total the browser sends.
- **Page.** Render each group as a `fieldset` of radio inputs (a disabled radio for sold-out),
  put the total in an `aria-live="polite"` element, and keep line items as text. The
  playground's `product-configurator.html` is a worked example; its headphones asset is
  generated by `playground/asset-sources/product/build-headphones.mjs`.

### Portfolio set-pieces (app-level recipe, no export)

A periodic-table skills grid, bento wall or similar portfolio set-piece is app layout and
content, so it stays in the app (AGENTS.md: no app-specific layout, tokens or content in
the library). Compose it: a CSS grid places each tile (`grid-template-columns:
repeat(18, 1fr)`, then `grid-column: <group>; grid-row: <period>` per tile; collapse to
`repeat(auto-fill, minmax(5rem, 1fr))` on narrow screens), `Reveal as="ol" stagger={30}`
(`/scroll-reveal`) brings tiles in, `FlipCard` (`/flip-card`) shows detail on the back,
and `SwingRail` suits a shorter row of hanging skill tags. Keep tiles as list items with
real text (symbol, name, level) and give the category colour a text label too.


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
