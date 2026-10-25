# Shader and Three.js motion direction

Use shaders when material, light, depth, or continuous motion serves the explanation.
Choose Three.js for a requested scene/shader pipeline; reuse the project's renderer.
Keep canonical scene timing and cue data independent of the rendering adapter.

## Reuse compatible effects and scene infrastructure

Apply the installed `ui-foundation-reuse` skill for compatible React work before
authoring shaders, animation loops or scene infrastructure. Its resolved runtime
exports/types are the API authority. Search `/gradient`, `/liquid-metal`,
`/liquid-glass`, `/image-filter`, `/image-transition` and `/paper-motion` for
materials and reveals; inspect `/visualizer` or `/cymatics` for audio-driven work,
`/three` for scene/staging helpers and `/core` for shared lifecycle behavior.
These are search candidates, not a guarantee that every installed version has them.
Use that skill's bundled local runtime workflow when no package is installed.

Reuse a compatible existing Canvas or the library's `Scene`; do not nest or add
another Canvas around scene content. Inspect supported helpers such as `World`,
`Float`, `Model`, lighting/material helpers and `useSceneMotion` before rebuilding
them. Procedural subject geometry belongs to the video project; `Model` expects
an actual supported model URL, not a procedural group factory. Custom motion must
obey the host's pause/reduced-motion policy. Preserve cleanup and offscreen behavior.

React components do not drop directly into Pillow or a plain Three.js renderer.
Keep those routes when appropriate; identify a compatibility gap before proposing
an adapter or alternative. Author a new shader or generic helper only after the
reuse check demonstrates missing behavior and implementation is in scope.

## Keep preview and export on the same timeline

Inspect the selected effect's actual clock, seeking and pause contracts before
choosing an export adapter. A live RAF animation, `paused` prop or scene motion
signal does not imply support for arbitrary video timestamps. Reuse a supported
frame-driven API when available; otherwise identify and implement only the required
authorized timing bridge, or disclose the export limitation. Verify representative
fixed-time frames, seeks and the encoded output before claiming that preview effects
are included in the film. Keep captions and audio on the same canonical timeline.

## Additional shader and rendering constraints

- When custom effect code is required, use an owned module with explicit uniforms: media time, resolution,
  strength, pointer, and bounded cue data. Reuse its math across preview/export where feasible.
- For a demonstrated custom video post-processing gap, a Three.js scene, orthographic camera, plane, VideoTexture,
  and ShaderMaterial are sufficient. Do not claim this turns existing flat artwork into
  reconstructed 3D geometry. Use actual meshes when independent depth is required.
- Distinguish event-synchronized visual pulses from measured audio reactivity. Only claim
  FFT/envelope reactivity when an actual audio analysis path supplies those uniforms.
  For measured mix energy, persist a bounded smoothed envelope on the canonical frame clock;
  validate its source hash, duration, and levels in preview and export.
- Keep text, evidence, captions, and brand marks outside distortion/glow masks. Use restrained
  relief lighting, refraction, grain, sheen, and spatially meaningful ripples; avoid flashing.
- Declare color-space handling. Custom shaders need explicit conversion or a documented
  display-RGB pass. Verify orientation and before/after frames; do not double gamma-correct.
- Pin dependencies, preserve licenses, and bundle locally when offline review is required.
  Verify registry integrity; do not rely on an unversioned CDN or hide a failed import.
- Cap render resolution and expensive loops. Avoid redundant uploads/renders of the same
  video frame. Suspend work while paused or hidden, except deliberate interaction redraws.
- Recreate textures when source dimensions change; dispose textures, geometry, materials,
  renderers, animation callbacks, and listeners at the correct lifecycle boundary.
- Respect reduced-motion preferences. Provide an effects toggle and a playable plain-video
  fallback for import/compile/render/context failures. Do not leave a black canvas over it.
- Fix motion at its source: interpolate sampled paths and avoid quantized size/rotation
  steps. Use an explicit supported frame rate; a 60fps encode cannot repair 30fps motion
  by duplicating frames. Cache reusable texture sizes separately from animated transforms.
- Test loading, paused seeks, replay, format switches, mute/volume, effects on/off, context
  loss, and recovery. Check temporal stability and representative full-size exports.
- A GPU preview is not an exported film. Bake effects into a playable output through a
  documented supported adapter, or state exactly which export remains unavailable.
  Match frame timing and audio, bound memory, detect partial frames and encoder/GPU failures,
  and retain the original source until the completed export passes decoding checks.
