# Media in 3D: relief, marks and time stacks

Use when an original or authorized photo/video should become depth relief, source-colored
marks, frames distributed through space, or an audio-driven spatial composition. Extend the
[timed specification](reference-to-spec.md); keep its source IDs, shot clock, sound and export
owners. A reference application's controls are evidence, not a requirement to install it.

## Select the actual spatial mechanism

| Mechanism | Needed data | Honest interpretation |
| --- | --- | --- |
| Screen/surface effect | Image/video texture and a mapping | A visual filter; it does not recover depth |
| Depth relief | Aligned depth or an explicitly authored/photometric proxy | One visible surface with limited camera travel; label a proxy as illustrative |
| Point/glyph field | Source colors/alpha, sample grid, positions and mark size | Marks occupy actual projected positions; more points alone do not supply geometry |
| Time stack | Selected decoded frames and source timestamps | Space represents time, not simultaneous people or a recovered world |
| Image collection field | One record per image: stable ID, file, source metadata and the field each layout encodes | Each card is one catalogued item at a layout position; arrangement shows the chosen field, not similarity unless measured. Untested here: pack thumbnails into a texture atlas or array, draw instanced quads with per-instance UV offsets, and load full resolution only for a revealed hero card |
| Scanned point cloud | PLY/LAS positions and colours, units and up-axis from a lidar or photogrammetry capture | Measured geometry at capture density; holes are unscanned areas, never filled in. Untested here: decimate with a seeded voxel grid to a fixed budget and render as size-attenuated points on a camera spline |
| Independent 3D geometry | Meshes/rigs with appropriate views | Use the existing scene/DCC owner when new viewpoints or articulation require it |

Record whether depth is measured, model-estimated, manually authored or derived from luminance.
Brightness is not distance. A hidden background, rear surface or hand outside the source cannot
be recovered by rotating a relief. Narrow the camera or use authorized additional views rather
than filling missing geometry without disclosure. Keep logos, exact type and evidence labels in
a controlled layer; do not convert them into illegible points unless that transformation is wanted.

For an image collection, compute each layout (tunnel, cluster spheres, wall) as a pure function
from record to position, and transition by interpolating the same record ID between layouts so
items never trade identity. State what a cluster means (date range, box, catalogue subject or a
model's tags) and label model-assigned tags as machine output. Hero-card captions come from the
record's own metadata. Budget texture memory from item count × thumbnail size before choosing an
atlas, and check rights per item: a library hosting a scan does not make every item free to reuse.

Define source range/PTS, display orientation, alpha/depth alignment, sample dimensions and depth
units, origin, axis direction, camera path, near/far limits and protected subject margins. Preserve
colors consistently. For video, review moving edges and depth stability; independent per-frame
depth guesses can flicker. Sparse marks or newly exposed silhouettes are visible creative limits.

## Bind motion to the soundtrack

Choose the actual signal before writing the animation: low/mid/high energy, RMS, onset or an
owner-provided cue. Measure it from the selected audio range, using its sample rate and the same
output clock. Record window, normalization/noise floor, smoothing, sensitivity, range and latency.
Keep silence at rest; do not amplify numerical leakage into activity. Clamp controls and use
attack/release or another explicit smoothing rule rather than flashing at arbitrary thresholds.

Map a few purposeful controls, for example low-band energy to relief amplitude or slice spacing,
and high-band energy to point radius. Label keyframed accents as synchronized animation; they are
not measured audio reactivity. Separate source-video playback speed from camera and effect speed.
For live playback, user input starts audio; mute/pause/seek must reach every dependent consumer.
For film, precompute features and evaluate at frame/sample time; do not record wall-clock RAF.

Compare a quiet and accented interval. Verify the encoded audio at the same times, including
codec offset and tails. Retain the unmodulated state for diagnosis. More bass activity is not
proof of a better film. Follow the existing [sound pass](sound-design.md) for rights and mix review.

## Choose an execution path

Reuse the project renderer first. For compatible React scenes, inspect actual UI Foundation
exports/types before planning new effects; a still-image facade or live audio visualizer is not
automatically a video-texture, depth or arbitrary-time export adapter. Reuse its compatible
scene/lifecycle pieces and add only demonstrated gaps. Do not add React to an offline composition.
Keep an existing Three.js/Blender path when it fits. Vendor model/API names and old tutorial
claims do not establish current operation, pricing, rights or a working local integration.

The optional [offline study adapter](../scripts/media_in_3d.py) supplies one bounded portrait
source → continuous point-relief reveal → eight transparent historical poses with measured three-band
PCM bindings. It uses NumPy/Pillow and existing FFmpeg, no browser or generation service.
Its [optional requirements](../scripts/requirements-media-3d.txt) are separate from the simpler
storyboard renderer. Reuse an existing compatible environment; install only when authorized.

Agent-operated example, resolving paths for the actual host:

```sh
python scripts/media_in_3d.py --source /private/source.mp4 --source-in 0 --source-duration 5 \
  --audio /private/cleared-track.wav --font /private/licensed-font.ttf \
  --duration 15 --width 1080 --height 1920 --output /private/new-revision
```

For an isolated subject, optionally add `--matte /private/matte.mkv` and
`--depth /private/depth.png --depth-kind authored`. The matte is a 432×768 video aligned to the
**selected, padded source derivative**, starting at its own 0 and covering the complete source
interval. Depth is a static 432×768 8-bit grayscale PNG, normalized 0–1 with white nearer the
camera. Declare `authored`, `estimated` or `measured`; recording a kind does not validate it.
No matte/depth estimator is bundled. Without fields, the helper still uses explicitly
illustrative luminance relief over the whole image; this fallback cannot isolate a person.

Review the matte on contact, release and maximum-displacement frames before rendering. Retain
fingers, hair, boots and prop handles; remove background wedges between limbs and inside handles.
Do not interpolate an arm mask across a release as though its motion were linear: inspect the
actual source at release/after release and add timing keys or a tracked correction there.
A hand-guided silhouette with local color refinement is asset-specific preparation, not a general
segmentation capability. A static authored convex field is shallow relief, not a recovered body.
Keep curvature/camera travel modest enough to retain the face and hands. Lighting changes must
not move geometry when an aligned authored depth field is supplied.

This adapter accepts 6–30 seconds on a 30 fps grid, portrait 720×1280 or 1080×1920, a 0.5–15 s
source range and a mono/stereo 16-bit PCM WAV covering the complete output. It decodes one bounded
24 fps 432×768 source derivative, with aspect-preserving letterboxing (up to about 359 MB RGB for 15 s,
plus fields/caches). The first 69% advances the selected source once. From 55–75%, fixed
historical source anchors peel out with staggered, continuous position/opacity ramps; the
final quarter holds eight source moments. A not-yet-available anchor is clamped to the
current source time rather than showing a future frame. Source sampling is approximate, not a native-PTS conform. It is a study
template, not a configurable general film engine, automatic depth estimator, glyph generator or
live interactive tool. Change the project's scene adapter for a different art direction.

Use a fresh output folder; existing media is never overwritten. `render.json` binds source/audio/
font/helper/field hashes, actual ranges, feature/onset values, mappings and full-decode result. A partial
render has no completed receipt and must not be selected as final. Missing/short media or an
invalid range stops before the output folder is created. An encode failure preserves diagnostic
output; use a fresh revision after fixing it.

## Preserve the transformation and the beat

Use one source index and initial projection while blending image into points. Keep sampled
historical poses at stable source-time anchors while their positions and opacity peel out.
Continuously recomputing an older pose from a widening lookback window can make it rewind or
morph during the transition. Stagger emergence to avoid piling several nearly opaque copies
onto the current face, and keep opacity continuous at zero. Distinguish time trails from
simultaneous people; record anchors and show a modest past/now cue when direction is unclear.

Fit the **maximum** allowed audio displacement, trail extent and camera path once. Fixed focal
length or a time-authored pullback preserves beat-driven changes; per-frame bounds auto-fit can
cancel spacing/depth modulation. Keep all subjects/props within protected artwork margins.
Clip decorative floor guides to that region and composite their alpha; never let a bright grid
compete with faces or explanatory copy. Place the floor at the actual supported subject contact
edge, not the padded image bottom. The study adapter uses the lowest visible matte row as
a fixed contact plane, gently aligns each standing pose's support edge during lift, and rejects
an entirely empty matte. Review this against the footage: it
is a geometric support heuristic, not a foot/ground detector, and airborne poses need an
appropriate scene adapter.

This helper measures 40 ms FFT windows ending at `frame/fps` (no lookahead), uses an offline
per-band 95th-percentile ceiling and a shared leakage floor, then 40 ms attack/180 ms release.
Positive change of the **unsmoothed normalized** low band adds an 80 ms-release onset envelope;
do not derive the transient from an already attack-smoothed display meter. Low energy changes depth and trail
extent; high energy changes point radius; mid energy and onsets add local emissive bloom.
Premultiply the accumulated subject field by alpha before blurring, then add one bounded
local-emission pass behind the points. Otherwise faint ghosts can glow too strongly or acquire
dark blur fringes. Keep source-color intensity restrained and check face/jewel highlight clipping.
The camera is not driven by these signals. Expose these mappings in the receipt.

Compare audio-on with all-zero features at identical source/camera time, cropping to the
**artwork** so meters and labels cannot make a false pass. Check that spacing remains visible
after projection, silence rests, isolated bands stay separated, and a known onset has no
pre-onset response. Compare final decoded AAC features and onset lag against driving PCM;
correlation alone does not prove strong visible response.

## Verify what the film demonstrates

Inspect source, relief, maximum camera angle, sparse edges, stack occlusion and first/last frames.
Check that labels describe the visible mechanism, source time remains intelligible, and important
hands/props/text stay reviewable. A rotating flat card is not a depth-relief test; a plane stack is
not point-cloud reconstruction. Inspect motion, not only attractive stills.

Test silence, frequency separation and short-input rejection when changing feature extraction.
Check the signal→parameter relation in actual output, then full picture/audio decode, exact frame
count/duration, phone-sized playback and the current preview. Report instruction validation,
adapter/runtime checks, visible result, listening and user creative acceptance separately. One
sample proves that execution path on those assets, not universal fidelity or audience performance.
