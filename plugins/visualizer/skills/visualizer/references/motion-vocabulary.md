# Motion vocabulary

By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Read this when a brief or reference names an effect ("text mask", "fisheye grid", "karaoke
captions") or when a reference shows one. Turn the name into a build plan: what reads on screen,
how to construct it in code, what to reuse first, and how to review it in the encoded film.
Names here are working vocabulary, not a style to apply everywhere. One dominant action per
scene still applies ([video workflow](video.md)).

## Asking by name

A name alone is ambiguous. Pair it with a duration, a strength and a subject ("overshoot,
0.6 s, soft, on the logo"); when a brief gives only the name, choose those three and state
them in the shot plan so a reviewer can check them.

## Reuse first

Before building an entry, discover the installed `ui-foundation-reuse` companion and check the
resolved package's actual exports. Entries below name exports that existed when this table was
written; newer versions may add more (for example animated pixelate, dither or glitch effects).
Use what the installed version exports, verify its seek/pause contract, and record the version.
Do not invent an import because a name appears here.

## Timing contract

Every entry is a pure function of frame time `f` (or normalized progress) on the shot timeline:
no `Date.now()`, no free-running `requestAnimationFrame` during export, and seeded randomness.
Await image/video decode at each explicit seek ([montage and compositing](montage-and-compositing.md))
and follow the shader timing rules in [shader direction](shaders.md). An effect that only looks
right in a live preview is not done until it appears correctly in the decoded export.

## Entries

| Effect (aliases) | Code construction | Reuse first | Review target |
| --- | --- | --- | --- |
| Kinetic type: per-word or per-letter reveal (blur-in, rise, scale-pop, stagger) | Split into word/glyph spans or SVG text runs; per-unit transform, opacity and blur keyed to frame; stagger offsets from a motion token | `/kinetic-text` | A readable hold per phrase; no clipped glyphs; real font metrics |
| Word-highlight captions (karaoke chips) | Word timestamps from an aligned, approved transcript → highlight box or colour swap per word; separate from display type | none | Each word lands within one frame of its speech onset ([timing maps](timing-maps.md)) |
| Beat-synced cuts and words | Measured onsets/downbeats → `beatmap.json` on the master clock → snap cut and reveal frames; minor accents on off-beats | the sound-design cue sheet | Listen at normal speed; drift under one frame |
| Text mask (type as a window) | Text as clip path or mask (SVG `<clipPath>`, canvas `globalCompositeOperation`, shader alpha) revealing image or video | the type-behind-subject row in [montage and compositing](montage-and-compositing.md) | Edge anti-aliasing; legible at phone size |
| Motion path (follow-path, route line) | SVG path; `getPointAtLength(t·L)`; orient to the tangent; optional dashed trail or map route draw-on | none | Constant versus eased speed is deliberate; no tangent flips |
| Write-on, live pen, handwriting | `stroke-dasharray`/`stroke-dashoffset` per stroke in order; pen sprite locked to the stroke head; variable width through a brush library | `/paper-motion` | Natural stroke order; pen tip on the stroke head |
| Pixelate or mosaic transition | Animated cell size peaking at the cut (shader or canvas downsample), or a tile grid flip | `/pixelate` (static in older versions), `/square-tile-reveal` | Peak lands on the cut; sharp recovery; no flashing |
| Slice or strip shift | N strips with per-strip offset and stagger, horizontal or vertical | `/slice-shift` | Seams hidden; source realigned at rest |
| Concentric ring rotation | Annular masks of one image rotating at different rates, then locking | none | Rings re-register exactly at rest |
| Fisheye or grid world | Barrel distortion over a perspective grid, or a Three.js grid with a wide FOV and continuous dolly | `/lens-distortion`, `/three` | Type kept outside the distortion unless intended |
| 3D type cylinder or ring | Text on a cylinder (canvas texture on `CylinderGeometry`, or CSS 3D `rotateY` per glyph) with a camera orbit | `/three` | Back-facing text readable or hidden; reading direction correct |
| Ransom-note or cut-letter type | Per-letter cards with varied font, case and fill, slight rotation, paper shadow, staggered placement | `/xerox-collage` (texture) | The word still reads as one unit |
| Explode to shapes (shatter, burst, bouncing primitives) | Word → primitives with physics or authored ballistic arcs and bounce easing; seeded | `/physics`, `/particles` | Deterministic seed; a clear settle state |
| Stop-motion from stills (on 2s or 3s, boil) | Hold each pose 2–3 frames; small positional jitter; replacement cutouts; no tweening between holds | none | Cadence reads as intended, not as dropped frames |
| Paper and print props (polaroid, tape, stamp, sticker) | Layered PNG/SVG with drop shadow and slight rotation; slide in with overshoot | `/paper-motion` | Consistent shadow scale |
| Cut-out rig from a still | Separate a still into pieces (head, limbs, props) on their own layers, then pivot and offset them | [motion and sound direction](motion-and-sound.md) layered illustration | Joints hidden; no gaps at the extremes of motion |
| Halftone, dither or dot-matrix type | Shader or glyph grid sampled from a text raster | `/halftone`, `/glyph-grid`, `/geometric` | Text still legible |
| Rolling number counter (odometer) | Tween the value per frame with formatting, or per-digit vertical reels; tabular figures | none | The final value is exact and sourced |
| UI-mock choreography (cursor path, click ripple, card stack, device frame) | UI rebuilt in HTML/SVG; scripted cursor Bézier; press scale plus ripple; parallax card stacks | none | No fabricated product claims or results |
| Mascot or blob character (squash and stretch) | SVG or 2D rig; scale and squash on contact; a blink loop | [character and world consistency](character-and-world-consistency.md) | Identity stable across shots |
| Melt or drip | Metaball/SDF or a downward path morph | `/moving-blobs` | The silhouette still reads |
| Particle orbs and flow lines | Seeded particle field; curl-noise flow lines; brush-rendered fills | `/particles`, `/luminous-trails`, `/particle-form` | Temporally stable at the export frame rate |
| Procedural water or caustics | Fragment shader `caustic(uv, t)` plus ripple normals | [shader direction](shaders.md), `/liquid-*` | A seekable time uniform |
| Glitch, chromatic split, motion-blur slide | RGB channel offset envelope; directional blur during fast transforms | the `/image-filter` family | Short envelope; no flashing |
| Anticipation (wind-up) | Before each move, a short counter-move (about a third of the move's time, 10–15 % of its distance), then release with ease-out; optional squash on the wind-up | none | The wind-up reads at normal speed but never looks like a hesitation |
| Follow-through (overlapping action) | Body eases to a stop; an attached part (antenna, hair, tail) lags as a damped spring computed from time since the stop: `A·e^(−d·t)·cos(ω·t)` | none | The secondary part settles after the body; no endless jiggle |
| Wiggle (shake) | Rotation or position from a seeded sum of integer-frequency sines, multiplied by an envelope so it comes in bursts | none | Irregular, not a metronome; small amplitude; loops cleanly |
| Pulse (heartbeat) | Scale envelope with two Gaussian peaks per beat (lub-dub) on the beat grid; optional expanding ring on the first peak | the sound-design cue sheet for beat times | Peaks land on beats; returns to exactly 1.0 between them |
| Ping-pong loop (yo-yo) | Drive progress with a triangle wave of time (forward, then reverse) and ease it | none | No pop at either turn-around; the reversal is intended, not a rewind glitch |
| Line boil (wobble) | Redraw outlines with fresh seeded per-vertex jitter every 2–3 frames; the jitter seed comes from `floor(frame / hold)` | the stop-motion row above | Cadence reads as hand-drawn; jitter small enough to keep the silhouette |
| Text scramble (decode, shuffle) | Per glyph, seeded random characters (new every 1–2 frames) until a staggered lock time, then the real glyph; monospace to stop reflow | none | Final text exact and readable; lock order deliberate |
| Wave text | Per-glyph vertical offset `A·sin(2πk·p − i·φ)` with integer `k` per loop | `/kinetic-text` (`mode="wave"`) | Baseline legible at the lowest point; no glyph collisions |
| Text on a path (path text, marquee curve) | Sample the path by arc length; place each glyph at its centre distance, rotated to the tangent; scroll by exactly one repeat unit per loop | none | Spacing even on curves; no upside-down glyphs; seamless scroll |
| Variable-font animation (weight morph) | Animate `font-variation-settings: 'wght'` (or other axes) on a variable font loaded from a known file; never rely on a system font name | none | Width change does not reflow nearby layout; the export shows the axis moving |
| Repeater (radial clone) | One shape drawn N times with per-copy rotation, offset, scale or colour step; N and the group rotation keyed to time | none | Copies register exactly; count steps are intentional |
| Kaleidoscope | Draw one wedge of moving content clipped to `2π/(2n)`, then rotate it n times and mirror each copy | none | Seams line up at the wedge edges; motion is symmetric |
| Push transition | Outgoing and incoming scenes translate together by the frame width, eased; direction carries meaning | none | No gap or overlap between scenes; both are sharp at rest |
| Cube transition | Two or four faces on a 3D rig (CSS `preserve-3d` with `rotateY` and `translateZ`, or Three.js) turned 90° per cut with perspective | `/three` | Face edges meet; text is never mirrored; the turn is not too fast to read |
| Page curl | Fold line sweeps the page; beyond it shows the next page; the flap is the removed corner reflected across the fold line, with a crease shadow | none | The flap stays attached to the fold; the reveal reads as paper |
| Exploded view | Stacked layers separate along one axis with stagger, leader lines and labels draw on, then reassemble; draw back-to-front | none | Layer order and labels stay correct; parts reassemble exactly |
| Split screen | The frame divides into panels with sliding dividers; each panel keeps its own content and timing | none | Dividers stay crisp; each panel's subject stays inside its panel |
| Pop-in | Scale from 0 with a back-ease overshoot (about 110 % before settling at 100 %); secondary parts (badge, label) pop a beat later; exit with ease-in | none | Overshoot visible but brief; nothing shifts layout while scaling |
| Burst (accent rays) | On the landing frame, 8–12 short rays and an expanding ring fire outward and fade within about 0.5 s; radii and alpha keyed to time since landing | the particle row for heavier bursts | Rays finish before the hold and stay inside the frame |
| Typewriter | Reveal one character per step from frame time; caret solid while typing and blinking on frame count while holding; measure the typed substring for caret position | none | Steady cadence; caret sits on the last glyph; final text exact |
| Easing (named curve) | Map normalized time through a named curve (linear, ease-out, ease-in-out, back) before it drives position; apply the curve to time in both directions, never by reversing the forward clip | the motion tokens | Ease-out decelerates into rest on the return leg too |
| Overshoot (spring settle) | Damped spring from the move's start: `to − (to − from)·e^(−ζt)·cos(ωt)`; show the target so the overshoot reads | none | Passes the target once or twice and settles within about 1 s; no endless wobble |
| Shape morph | Sample both shapes as the same N points (radius by angle, or arc length on paths) and interpolate point by point; star radii come from the ray–edge intersection, not a ramp | `/layout-morph` for layout morphs | Recognizable star and square at rest; no self-intersection mid-morph |
| Motion trail | Draw the path sampled at earlier times (`pos(t − k·dt)`) with falling size and alpha; never accumulate previous frames | `/luminous-trails` | Any frame renders correctly on its own after a seek |
| Parallax | Layers move at speeds proportional to their nearness; for loops, each layer moves a whole number of tile widths per loop and adjacent tiles overlap by a pixel | `/mouse-parallax`, `/scroll-scrub` for interactive parallax | Nearer layers move faster; no tile seam |
| Mask transition (iris) | The next scene is drawn inside a growing clip shape (circle, wordmark, object silhouette) over the current scene | `/aperture-reveal`, the `/image-transition` family | Mask origin is motivated (sun, subject, cut point); edges anti-aliased |
| Shape transition (wipe) | Staggered bars or shapes cover the whole frame, the scene swaps only while fully covered, then the shapes exit; scenes differ clearly from any mask-transition scenes | `/square-tile-reveal`, `/slice-shift` | Full coverage at the swap frame; no slivers at rest or at the loop seam |
| Zoom through | Scale exponentially about a point inside a letter or object until its interior fills the frame; the next scene sits behind the hole in screen space and fades in only once the dive starts | `/zoom-blur` for the blur pass | At rest the word reads normally; the hole is plain until the dive |
| Flip | Rotate about one axis; width = `cos θ`, swap faces at 90°, add keystone (near edge taller) and edge-on shading so it reads as 3D | `/flip-card`, `/three` | Never mirrored; perspective reads; face swaps exactly at edge-on |
| Light sweep (shine) | A soft angled gradient band crosses an element, clipped to its shape, with pauses between passes | none | Highlight stays inside the element and never washes out its text |
| Impact shake | On landing, offset the whole frame by `A·e^(−kt)·sin(ωt)` on two axes, squash the object once and puff dust; exit by fading, not by reversing the drop | the wiggle row above | Shake decays within about 0.5 s; the impact frame lines up with the sound cue |

## Adding an entry

Add an entry only when a reviewed film or reference needed it and the construction was verified in
an encoded export. Record the alias the user or reference used, so the next request can find it.
Keep project-specific looks, brand names and assets in the project, not in this table.
