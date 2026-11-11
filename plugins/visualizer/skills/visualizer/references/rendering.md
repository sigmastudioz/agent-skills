# Art direction, Three.js and shaders

For compatible React effects and scene infrastructure, apply the separately installed
`ui-foundation-reuse` companion first. Its actual exports/types own reusable capabilities;
keep custom subject geometry and the canonical timeline in this project. For video,
read [shader timing and reuse](shaders.md) before claiming deterministic capture.

## Select a coherent visual world
Study references at distributed timestamps and dense transition windows. Distinguish a finished
shot, montage, tutorial claim and interaction demo. Do not infer a production stack from style.
Record silhouette, palette, hierarchy, texture, light, lens/camera, cadence and visible mechanism.
Choose a primary world and borrow techniques selectively; do not combine every reference look.

Establish strong silhouettes, purposeful negative space, dominant/accent colors and typography
roles before detail. Use macro/system/detail views to reveal meaning. Stage foreground, subject
and background with occlusion and value separation. Different materials need different light
responses; global noise, blur or glow is not material richness.
For papercraft, separate moving layers, cut edges, overlap and shadows. A slowly zooming flat
illustration is not independent part animation. Use real alpha for cutouts and inspect halos.
For spatial reveals, use a real scene graph, geometry and camera tracks. A full-screen filter
cannot provide unseen surfaces, independent parallax or new camera angles.

Motivate camera motion and lights. Preserve identity, scale, anchors and geography across shots.
For procedural smoke/ribbons/particles, preserve flow direction and coherent silhouettes rather
than displacing everything with noise. Generated assets need a style/identity sheet and anchors;
reject drift rather than hiding it with transitions. Retain provenance and authorized prompts.

## GPU and Three.js implementation
For React scenes, use [React Three Fiber](react-three-fiber.md) for component ownership, lifecycle,
frame scheduling and ecosystem selection; the material, evidence and export rules below still apply.
Use the requested renderer when viable. A plane, orthographic camera, VideoTexture and
ShaderMaterial can post-process video; state that it is material processing of flat artwork.
Use meshes/layers when independent spatial depth is required. Keep model/timing outside adapters.
Give effect modules explicit uniforms for media time, resolution, strength, pointer and bounded
cue data. Derive pulses from timeline events; call an effect audio-reactive only when a real
FFT/envelope analysis path supplies it. Persist analysis provenance, source hash and time origin.

Keep evidence text, captions and brand marks outside distortion/glow masks. Declare color-space,
tone-mapping and alpha handling; compare before/after frames, avoid double gamma correction,
verify texture orientation and distinguish premultiplied from straight alpha.
Pin versions and retain licenses. Bundle dependencies for offline use when appropriate. A failed
import/compile/context must reveal a usable fallback, not a black canvas or invented success.

Cap pixel ratio, render size, geometry/particle counts and shader loops. Budget texture formats,
draw calls and passes for real target devices; measure before claiming frame rate. Avoid repeated
uploads/draws of an unchanged video frame. Suspend paused/hidden work except necessary redraws.
Dispose GPU objects, listeners, callbacks and media handles. Rebuild textures on source-size
changes; handle resize and context restoration. Reduced-motion/effects toggles must preserve meaning.

Fix stepped motion at its source: interpolate sampled paths, cache textures separately from
animated transforms, preserve intentional holds and test temporal stability. A GPU preview is
not an exported film. Bake effects through a documented supported adapter or disclose which
export is unavailable. Compare representative preview/export states at the same timeline times.

Verify loading, paused seeks, replay, rapid control changes, resize, format switch, mute/volume,
effects on/off, WebGL failure, context loss, recovery and cleanup. Browser-safe fallbacks and
static companions are part of the affected consumer path, not optional proof substitutes.

## Optional native renderer: raea
[raea](https://github.com/shinyobjectz/raea) renders Remotion-style React/TypeScript
compositions (`Composition`, `useCurrentFrame`, `interpolate`) on the local GPU through Rust and
Bevy, and plays the same file live. Consider it for 2D motion-graphics explainers and short-form
films when the user already has it or asks for it. It is not a browser engine (its `render PAGE.html` path is untested here): DOM and WebGL code, React
Three Fiber scenes and `ui-foundation` effects are not established to run in it, so keep those on
their existing renderer. Its 3D is Bevy (glTF, splats), not Three.js.
Use it only when it is already installed or the user authorizes the install. It is a canary release
under FSL-1.1-ALv2; its shell installer also writes agent skills into the user's skill folder, so
prefer an isolated binary or its plugin and do not let it silently replace this skill's routing.
Run it with `RAEA_OFFLINE=1` unless network assets are part of the brief. Pin the version used.
When an agent installs it with the user's approval, it writes `~/.raea/INSTALLED_BY.json` recording
`"installed_by": "agent"`, date, version, method, every component (binary folder, PATH link, plugin,
marketplace) and the matching uninstall commands. An agent may uninstall raea only when raea is
present and that marker says an agent installed it; it then removes exactly the listed components
and reports what it removed. With no marker, or one that names the user, leave raea in place and
tell the user how to remove it instead.
Observed on raea 0.1.0 (Apple Silicon, 2026-11-09): the README hello composition encoded 90 frames of
1080p H.264 in about 1.9 s warm (10 s on first run with GPU warm-up stalls); `--frame N -o x.png`
renders a single frame for inspection. `raea check` caught nothing on text flush against the frame
corner, so it does not replace the safe-area review in [verification](verification.md).

## Optional browser renderer: hyperframes
[hyperframes](https://github.com/heygen-com/hyperframes) (Apache-2.0, Node 22+) renders HTML
compositions to MP4 in headless Chrome: each frame is captured at `floor(frame)/fps`, never the
wall clock, through seek adapters for GSAP, CSS, WAAPI, Lottie, Three.js, anime.js, D3, maps and
TypeGPU, and `<audio>`/`<video>` tracks are mixed on the same timeline. Consider it as the timing
bridge in [shader timing](shaders.md) when a browser or WebGL scene must become deterministic
video. Its Three.js adapter drives plain `THREE` timing; React Three Fiber scenes (on-demand frame
loop) and `ui-foundation` effects are not established under it, so test-render one before relying
on it. Use `render --docker` when renders must match across machines.
Use it only when it is already present or the user authorizes the install. Pin the exact version
(`npx hyperframes@<version>`, project-local), since releases are frequent. Telemetry stays off:
set `HYPERFRAMES_NO_TELEMETRY=1` and `DO_NOT_TRACK=1` in the environment of every hyperframes
command and run `hyperframes telemetry disable` once after install; never run it with telemetry on.
Never run `hyperframes skills update` or enable its plugin auto-update: both write skills into the
user's skill folders and can replace this skill's routing. Before running any other hyperframes
command, check that it does not write there; if one does, stop and tell the user. Vendor CDN scripts (its examples load
GSAP from a CDN) when renders must work offline. Stay on the open-source CLI; HeyGen Studio Pro
and cloud render paths send work to HeyGen and need the user's explicit go-ahead.
