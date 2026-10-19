# React Three Fiber: reusable interactive scenes and films

## Choose and verify the runtime
Use R3F for new React-based 3D explanations, shader scenes and reusable spatial components.
Keep SVG/HTML/plotting for legible 2D information. Preserve working vanilla Three.js unless an
actual React integration or reuse requirement warrants migration. R3F expresses Three.js through
React; it does not automatically provide art direction, an encoder or better GPU performance.

Inspect the existing package manager, lockfile, framework, React/React DOM, Three.js and R3F
versions before editing. Pair compatible majors: R3F8 with React18; R3F9 with React19, per the
[official introduction](https://r3f.docs.pmnd.rs/getting-started/introduction). Recheck current peer
requirements before installation; do not switch a working app to an alpha for a showcase effect.
Pin the resolved compatible versions and retain licenses. Add only needed helpers, not the whole
ecosystem. In SSR frameworks, put browser/GPU code behind the framework's client boundary;
keep the accessible explanatory content server-renderable and size the canvas container explicitly.

## Study examples, then make an original scene
Use the [pmndrs gallery](https://pmndrs.github.io/examples/) as a technique library. Select two or
three examples matching the explanation, inspect their running behavior and linked source, and
record what was observed versus inferred. A thumbnail alone cannot establish behavior or stack.
Check code, model, texture, HDRI, font and audio licenses separately before reusing anything.
Keep the author credit and required notices; gallery availability is not permission for every asset.

| Direction to investigate | Useful purpose | Cost or correctness constraint |
| --- | --- | --- |
| Aquarium / transmission | Reveal containment, layers or a material boundary | Refraction passes, thickness, background readability; keep labels outside glass |
| Room With Soft Shadows | Ground objects and separate visual planes | Shadow map/PCSS samples and light scale; contact must remain stable |
| Shader Materials / Halftone | Give surfaces a coherent graphic identity | UVs, aliasing, resolution and temporal stability; preserve evidence contrast |
| Bezier Curves And Nodes | Explain dependency, flow and handoffs | Stable endpoint IDs, direction, occlusion and selectable paths |
| HTML Annotations / multiple views | Connect spatial objects with readable information | Occlusion, DOM focus/order, clipping and shared camera/event coordinates |
| Instanced particles / geometry reuse | Show many entities without per-object draw overhead | Stable picking IDs, bounded counts and meaningful aggregation |
| Audio Analyser / spring motion | Tie response to a real event or signal | User-started audio, measured envelope, damping, mute and deterministic film cues |

These are starting directions, not mandatory effects or claims all examples were executed.
Choose one dominant material/lighting world and one explanatory motion system. Compare hero,
mechanism and payoff frames at phone size. Use rim/key/fill separation, restrained roughness,
clear silhouettes and intentional camera paths; extra bloom cannot repair poor composition.
Provide a cheaper equivalent for costly transmission, volumetrics, shadows and postprocessing.

## Own the model and scene components
Keep domain calculations and a seeded timeline independent of React and Three.js. Give reusable
behavior a cohesive owner; split scene objects, material definitions, interaction and export only
when they have distinct responsibilities. Avoid a second model in a video-specific scene.
Pass validated scenario, stable IDs and time into scene components. Use React state for semantic
choices such as selection or play/pause, refs for transient transforms/uniforms, and selectors for
external stores. Do not add a state library solely for one small scene.

Call `useThree`, `useFrame` and loader hooks only inside the Canvas tree. Keep hooks unconditional.
Use declarative meshes/materials; memoize expensive construction and stable uniforms. Mutate only
objects owned by the component in `useFrame`; do not call React setState, allocate vectors/materials
or run domain solvers per display frame. Use delta-aware damping for live response and a bounded
simulation step; use absolute-time sampling or reproducible simulation replay for export.

This complete TSX scene component demonstrates one explicit time source and stable uniforms.
The host supplies `time.current.seconds`, canvas, controls and capture; it is not a video encoder.

```tsx
import { useMemo, useRef, type RefObject } from 'react'
import { useFrame } from '@react-three/fiber'
import type { Mesh, ShaderMaterial } from 'three'

type SceneTime = RefObject<{ seconds: number }>
export function Signal({ time, onSelect }: { time: SceneTime; onSelect: () => void }) {
  const mesh = useRef<Mesh>(null)
  const material = useRef<ShaderMaterial>(null)
  const uniforms = useMemo(() => ({ uTime: { value: 0 } }), [])
  useFrame(() => {
    const t = time.current.seconds
    if (!Number.isFinite(t) || t < 0) throw new Error('Invalid scene time')
    if (mesh.current) mesh.current.rotation.y = t * 0.3
    if (material.current) material.current.uniforms.uTime.value = t
  })
  return (
    <mesh ref={mesh} onClick={(e) => { e.stopPropagation(); onSelect() }}>
      <sphereGeometry args={[1, 32, 24]} />
      <shaderMaterial ref={material} uniforms={uniforms}
        vertexShader={`varying vec2 vUv;
          void main(){vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`}
        fragmentShader={`uniform float uTime; varying vec2 vUv;
          void main(){float p=.5+.5*sin(vUv.y*12.+uTime);
            gl_FragColor=vec4(mix(vec3(.04,.12,.2),vec3(.1,.7,.65),p),1.);
            #include <tonemapping_fragment>
            #include <colorspace_fragment>
          }`} />
    </mesh>
  )
}
```

For a real shader, define uniform units/ranges, update resolution after DPR/size changes and keep
material instances stable. Choose a documented color/tone/alpha pipeline; apply output conversion
once. Keep captions and Lex from SigmaStudioz marks clear of distortion. GLSL ShaderMaterial
requires a compatible WebGL path; do not paste it into a WebGPU/TSL pipeline and claim equivalence.
Use Drei only where it reduces real work: controls, environments, text, bounds, instances or GLTF.
Use postprocessing selectively and give the composer one render owner; positive `useFrame`
priority takes over automatic rendering. Recheck APIs and supported backends for pinned versions.

## Schedule, interact and release resources
Use `frameloop="demand"` for settled scenes. Imperative camera/uniform/store changes must invalidate;
`invalidate()` requests a frame, not an immediate capture. Continue invalidating while a transition
is active and stop on rest. Continuous motion needs an intentional live loop; pause hidden work.
Cap DPR, geometry, texture memory, lights, render targets and passes against measured targets.
Profile draw calls, frame pacing and memory with realistic assets; instance repeated geometry.
Avoid remounting expensive resources during every scene change, but do not retain unbounded scenes.

Use a Suspense loading state and an error boundary with a useful retry/static alternative.
DOM elements belong outside Canvas or in an explicit HTML integration; Suspense inside Canvas
must use valid scene elements. Canvas fallback handles unavailable GL, not every later loader or
shader failure. Handle asset failures, unsupported contexts, context loss/restoration and resize.
Cached GLTFs/textures are shared: clone scene instances when required and do not dispose a cache
while another consumer uses it. R3F disposes owned declarative resources; external primitives,
custom render targets, loaders, listeners and caches need explicit ownership and cleanup.
Exercise Strict Mode setup/cleanup/remount; never make a one-time flag hide broken effects.

Supply labeled DOM controls and a text/table companion, keyboard equivalents for scene actions,
visible focus and a reset. Account for raycast propagation, pointer capture, touch, overlays and
missed clicks. Do not swallow page scrolling indiscriminately. Respect reduced motion, mute and
user-started audio; connect actual cue/envelope data to uniforms instead of claiming fake reactivity.

## One clock for interaction and film
Own a scene-time contract in seconds, independent of the browser clock. Interactive playback
maps play/pause/seek/visibility to that contract. Springs, physics, particles, GLTF mixers and
procedural effects must be sampleable at absolute time or reset/replayed with a fixed seeded step.
Freeze the export scenario and camera; clear damping/history/temporal buffers before random seeks.

For exact export, use a dedicated root with `frameloop="never"` and its `advance` adapter, or an
existing compatible capture integration. Give exactly one system frame ownership. Resolve assets,
fonts, React commits and shader warm-up before frame zero. At frame i, set scene seconds=i/fps,
advance/render using the pinned API's timestamp contract, then await frame capture before i+1.
Do not confuse RAF milliseconds with model seconds, or use `invalidate()` as a completion signal.
Capture DOM annotations/captions through an explicit compositor or put export text in the scene;
canvas pixels alone omit HTML overlays. Preserve the same model, framing, color and attribution.
Render original/licensed sound and captions from the same event IDs/time origin, then encode and
verify using [video guidance](video.md). A browser MediaRecorder preview is not exact-frame proof.

## Trace and prove the integration
Trace request → model/time → Canvas/component → shader/controls → fallback → capture/encode and
all cleanup owners. Compile/typecheck and run the actual preview. Test selection/reset, paused
seek, rapid changes, resize/DPR, missing assets, GL failure, reduced motion, mute and remount.
Compare matching interactive/export states, including out-of-order times and first/last frames.
A React test renderer can verify scene props/events but does not compile GLSL or prove GPU output.
Record dependency versions, reference links/licenses, chosen techniques, performance budget,
commands, results, unresolved paths and next action in the task handoff, outside the installed skill.

Consult current official [Canvas](https://r3f.docs.pmnd.rs/api/canvas),
[hooks](https://r3f.docs.pmnd.rs/api/hooks), [performance](https://r3f.docs.pmnd.rs/advanced/scaling-performance)
and [pitfalls](https://r3f.docs.pmnd.rs/advanced/pitfalls) before relying on version-sensitive behavior.
