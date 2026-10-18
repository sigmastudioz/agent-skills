# Art direction, Three.js and shaders

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
