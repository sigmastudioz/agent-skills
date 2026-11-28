## Capability search map

Subpaths below are relative to `@sigmastudioz/ui-foundation`. Confirm availability in the installed manifest before using them.

| Requested behavior | Inspect these public subpaths first |
| --- | --- |
| Shader backgrounds, liquid metal/glass, glass distortion | `/gradient` (`pointer` warp, `audio` swell), `/liquid-metal`, `/liquid-glass` (CSS/SVG, any content), `/fluted-glass`, `/iridescence`, `/iridescent-ribbon`, `/spectral-ribbon` (`SpectralRibbon`, dark flowing ribbon) |
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
| Two-sided flip cards and a lanyard badge that swings when dragged | `/flip-card`: `FlipCard`, `LanyardBadge`, `stepPendulum`, `dragAngle`, `fromInnerControl`, `FLIP_IGNORE` |
| Book whose pages turn in 3D with a curl (drag, keys, buttons or scroll) | `/page-flip`: `PageFlip`, `curlAngles`, `spreadLabel` |
| Cards around a rotating 3D cylinder with one focusable front card | `/card-ring`: `CardRing`, `ringRadius`, `frontIndex`, `angleForIndex` |
| A lens (jelly orb or crystal) bending a live DOM headline | `/type-refraction`: `TypeRefraction` (WebGL 1; text stays real DOM) |
| An image shattering into 3D shards and reassembling on scroll | `/shard-burst`: `ShardBurst`, `buildShards`, `scrollBurst` (CSS 3D, no WebGL) |
| Swing rail: tags, cards or photos hanging from a rail that swing when brushed or scrolled | `/swing-rail`: `SwingRail`, `stepSwingRail`, `resolveNeighbours`, `brushImpulse`, `scrollImpulse`, `MAX_SWING_ANGLE` |
| 3D product configurator / product page: spin a model, recolour parts per option, price updating per option | `/three` `Model materials` (recolour) with `orbit`/`autoRotate` (spin); `/product-config`: `useProductConfig`, `priceConfiguration`, `resolveSelection`, `selectionMaterials`, `formatPrice` |
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
| 3D hosting, staging and models | `/three`: `Scene`, `World`, `Model`, `Float`, `GlassMaterial`, `Portal`, `ReflectiveFloor`, `SoftShadows`, `Bloom`, `Caustics`, `ExplodedAssembly`, `Environment`, `Finish`, `PostEffects`, `useSceneMotion`, `applyLightmap`. `Model` takes a baked `lightmap`, or `materials` to recolour named parts (`createMaterialVariants` for a scene you load yourself). `Model` and `Float` accept `onError` when their runtime cannot load. `World` then shows its install fallback. |
| Camera lens in mm, first-person walk/look, lighting moods (morning, sunset, storm, night), device tilt | `/three`: `lensToFov`, `fovToLens`, `LENS_PRESETS`, `WalkControls`, `LightingMood`; `/weather` `SceneEnvironment mood`; `/core`: `useDeviceTilt`, `resolveLightingMood`, `LIGHTING_MOODS` |
| Rigid-body scene content | `/physics`: `BallPit` loads `@react-three/rapier` on mount and accepts `onError`. `/physics/rapier`: `Physics`, `RigidBody`, `CuboidCollider`, `BallCollider`, `CapsuleCollider` (this subpath evaluates the peer at import). |
| Shared lifecycle, visibility, interaction and quality policy | `/core`: `EffectsProvider`, `useEffectsSettings`, `useRafLoop`, `useReducedMotion`, `useInView`, `usePageVisible`, `useWebGLEffect`, `useScrollProgress`, `useInteraction`, `useAdaptiveQuality`, `useDragGesture` |

Every `/native` subpath (`/visualizer/native`, `/foil-surface/native`, `/frosted-blur/native`, `/remote-image/native`) requires the optional `react-native` peer (>=0.77) and the host app's native build; `/visualizer/native` and `/foil-surface/native` also lazy-load the optional `@shopify/react-native-skia` peer and keep a static fallback without it. The remaining subpaths are web React DOM entries that need no native or Three peers unless their row says so.

Search the full installed exports if the selective map has no match. Inspect `/presets` when available for existing configurations and composition patterns. `npm run check:skill` fails when a public export subpath is missing from this guide.

Per-effect props, defaults and constraints are in [effect API](effect-api.md): image
filters and glitch, blob tracking to reaction-diffusion, iridescent ribbon, rain on glass,
landing-page scroll names, refractive glass, page flip to shard burst, swing rail, drag
gestures, scene input (lens, walk, moods, tilt), the product configurator, portfolio
set-pieces, native foil laminate and shape patterns. Read the section for an effect before
configuring it; the map above is enough to choose one.
