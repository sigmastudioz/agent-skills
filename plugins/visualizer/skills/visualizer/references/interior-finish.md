# Finishing a walkable interior in the browser

By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Read this after the [live floor-plan map](interactive.md#recipe-live-floor-plan-map-beside-a-walkable-3d-space)
works and the rooms are still grey boxes. It turns the same validated layout into a lit,
furnished interior, live in the browser: windows that let the sun in, floors and walls with real
surfaces, furniture fitted to each footprint, image-based fill light and a short post-processing
stack. The plan gets an architectural finish to match. Nothing is downloaded: every texture and
piece of furniture is generated in code, so the page has no asset licence to check.

Checked 2026-11-17 on a three-room, 10 × 5 m layout (2 doors, 6 windows, 21 furniture pieces) with
React 19.3, Three.js 0.186, React Three Fiber 9.8, Drei 10.7.9, @react-three/postprocessing 3.2.2
(postprocessing 6.39.6, n8ao 2.1.0) and ui-foundation 0.13.2, in headless Chromium on an Apple
M1 Max. Treat other versions, Safari, Firefox and real phones as unverified. The walkthrough
checks from the floor-plan recipe all still passed with the finish applied.

## When to use this, and when to bake
Use it when the viewer walks freely and the sun, layout or furniture may change: everything here is
lit live. When the camera path is fixed or small and nothing moves, [bake the lighting](baked-lighting.md)
instead; that is cheaper on phones and gives true bounce light.

## Layout additions
The finish needs four more fields in the layout. Validate them in the same pure model as the rest:
- **Windows** `{ x, z, width, sill, head }`, centred on a wall line like a door. Reject a window
  that is not on an *exterior* wall (a room on one side only), that is not inside a stretch left
  solid after door cuts, or whose sill is below 0 or head not above the sill. Keep the head below
  the wall height (2.6 m here). A window is visual only: collision keeps the full wall, so no one walks out through the glass.
- **A floor finish per room** (`floor: 'oak' | 'walnut' | 'tile'`), optional, with a default.
- **Furniture `kind` and `facing`** (`'n' | 'e' | 's' | 'w'`, the way the front of the piece
  looks). The kind picks the generator; the footprint `{ x, z, w, d, h }` stays the source of size.
- **`solid: false`** for walk-over decor such as rugs. Collision and "standable" checks skip it;
  the plan and the 3D view still draw it. Without it, a rug blocks the room it lies in.

Keep the plan's furniture rule (inside one room) for rugs too.

## Architecture from the plan
Generate every architectural mesh from the plan output, never by hand, so the 3D view, the SVG and
collision cannot drift:
- **Walls with windows.** For each wall segment, subtract its window spans to get solid stretches,
  which run full height. Each window adds a piece below the sill and one above the head. Extend only
  the segment's two outer ends by half the wall thickness, so corners close without overlapping
  faces. Add a slim dark frame (four sides and a mullion), a thin glass pane, an inside and outside
  sill, and skirting (about 9 cm) on both faces of every floor-level piece.
- **Doors.** A lintel fills the wall above the opening (doors about 2.1 m, walls 2.6 m), with a
  painted casing on both faces. The door itself can stay open and undrawn; the plan shows its swing.
- **Ceiling and roof.** A ceiling plane at wall height, and a roof slab just above it that casts
  shadows. Without the slab the sun lights the whole floor through the ceiling, and the windows do
  nothing.
- **Outside.** A large ground plane, paving the size of the house plus a margin, a few simple trees
  and a sky. Windows that show only the clear colour read as a void.

Round-cornered boxes (Drei `RoundedBox`) for furniture and trim catch highlights on their edges and
stop the scene reading as CG; keep the radius below half the smallest side.

## Light
Ceilings and walls facing away from the windows get no direct light, and realtime Three.js has no
bounce. Fake the parts that matter:

| Light | Settings that worked | Why |
| --- | --- | --- |
| Sun: one `directionalLight` with shadows | Intensity 3.4, warm white. Direction about 31° above the horizon. Shadow map 4096, bias −0.0003, normal bias 0.025. Fit the shadow camera to the house bounds plus a margin, and aim the target at the house centre (add the target to the scene). | A low sun reaches through the windows and draws patches on the floor. A loose shadow camera wastes resolution and makes edges soft and blotchy. |
| Image-based fill | Drei `Environment` with `frames={1}` and `resolution={256}`, holding three `Lightformer` panels: a large warm one overhead, a cool one on the window side, a dim warm one opposite. | Gives every surface soft light and gives metal and glass something to reflect, without downloading an HDRI. Rendered once, so it costs nothing per frame. |
| Sky and ground tint | `hemisphereLight`, sky blue-white over warm ground, intensity about 0.35. | Lifts the shadow side without flattening it. |
| Ceiling "bounce" | Emissive on the ceiling material, about 0.32 of a warm white. | Without it the ceiling renders dark brown and the rooms feel like caves. |
| Room fill | One point light per room at about 1.5 m, not near the ceiling, intensity 0.7, distance 8, decay 1.6. | A fill near the ceiling leaves a hot spot on it. |
| Practical lights | Lamp shades and downlight discs with emissive above 1, and a small point light inside each lamp. | Gives bloom something real to catch, and warm pools by the furniture. |

Turn shadows on the canvas (`shadows: 'soft'`) and mark walls, floors, furniture and the roof as
both casting and receiving. Glass casts nothing.

## Surfaces
Draw each texture once on a canvas, seeded so it looks the same on every load, and cache it. Draw a
matching greyscale bump map at the same size. Give each use its own `repeat` by cloning the cached
texture: clones share one image upload. Set colour maps to sRGB, wrapping to repeat and anisotropy
to about 8.

Size one texture tile in metres and set the repeat from the surface size: a 1.2 m tile on a
4.8 m floor repeats 4 times. Run planks along the room's long side. Values that read well:

| Surface | Texture | Roughness | Bump scale |
| --- | --- | --- | --- |
| Oak or walnut floor | 8 staggered planks per tile, faint wavy grain, few knots, dark seams | 0.5 | 0.4 |
| Porcelain tile floor | 60 cm squares, faint veining, 6 px grout | 0.28 | 0.4 |
| Plaster wall | Hundreds of faint specks below 1% opacity | 0.92 | 0.08 |
| Subway splashback | 7.5 × 15 cm bricks, offset rows | 0.25 | 0.5 |
| Upholstery | Fine weave tinted by the material colour | 0.95 | 0.8 |
| Stone worktop or ceramic | Plain colour, `MeshPhysicalMaterial` with clearcoat 0.4–0.6 | 0.22–0.25 | none |
| Glass | `MeshPhysicalMaterial`, transmission 0.92, low opacity, `depthWrite: false` | 0.02 | none |

Keep variation small. Plaster specks above about 1% opacity look like leopard spots on a large wall,
and plank-to-plank lightness swings above about ±3% make a dark wood floor look patchy.

## Furniture fitted to the footprint
Write one small generator per `kind`, in a local frame: width along x, depth along z, front facing
+z, origin at the footprint centre on the floor. Rotate by `facing` (s = 0, n = π, e = π/2,
w = −π/2), swapping width and depth for east and west, so the piece fills exactly the rectangle the
plan and collision use. Build from rounded boxes, cylinders and a few shapes: a sofa is a base,
back, arms, seat and back cushions and two angled throw cushions; a plant is a pot, soil, a stem and
about 30 leaf shapes from a seeded random. Draw an unknown kind as a plain rounded box of its
footprint, so a new layout never fails to render.

Real models look better, but need a source whose licence allows the use, approved before download.
Load them with ui-foundation `Model` and scale each to its footprint.

## Post-processing
Use one composer, and let it own tone mapping:

```tsx
<Scene canvasProps={{ flat: true, shadows: 'soft', gl: { antialias: false } }}>  {/* flat: no renderer tone mapping */}
  …
  <EffectComposer multisampling={0} enableNormalPass={false}>
    <N8AO aoRadius={0.55} distanceFalloff={0.6} intensity={2.4} halfRes quality="high" />
    <Bloom luminanceThreshold={1.1} intensity={0.55} mipmapBlur radius={0.7} />
    <ToneMapping mode={ToneMappingMode.NEUTRAL} />
    <Vignette offset={0.32} darkness={0.42} />
    <SMAA />
  </EffectComposer>
</Scene>
```
- **AO** (N8AO) darkens corners, skirting lines and the floor under furniture: the biggest step
  from "boxes" to "room". Half resolution is enough.
- **Bloom** with a threshold above 1 blooms only emissive parts (lamps, downlights), not white walls.
- **Neutral tone mapping** keeps the finishes close to their chosen colours.
- **SMAA** smooths edges, since the composer runs with `multisampling={0}`. Leave canvas
  antialiasing off too: the composer renders to its own targets, so it would only cost time.
- Do not also mount ui-foundation's `Bloom`: it brings its own composer, and the two stack.
- Mark overlays that must keep an exact colour, such as the hover glow on a floor, `toneMapped={false}`.

## The plan, finished to match
Draw the SVG like an architect's plan, still in metres:
- Walls as thick dark lines, windows as a thin double line with glazing across the gap, and each
  door as a quarter-circle swing.
- A simple outline symbol per furniture kind (sofa back and arms, bed and pillows, sink, hob).
- Each room's name and area (`w × d`, in m²), with a white text halo (`paint-order: stroke`) so
  labels stay readable over symbols.
- A 1 m scale bar and a north arrow outside the bounds.

A room jump (click or "Go to") reads as a cut rather than a glitch with a short dip to dark, about
320 ms, on an overlay above the view. Skip it under reduced motion.

## Budget and how to measure it
On the checked layout, with headless Chromium and vsync off: 1440×810 at 2x took a median of 9.9 ms
per frame (95th percentile 14.3 ms), 3.9 ms at 1x, and 3.7 ms at 390×844. That is about 480–540
draw calls and 90k triangles per frame, with 55 textures. Most of the draw calls are separate
rounded boxes in furniture. Before targeting phones, merge each static piece's geometry by material
or instance repeated parts, and drop the shadow map to 2048.

Two traps give false numbers:
- Headless Chromium caps `requestAnimationFrame` at 30 fps, so every size reads 33.3 ms. Launch it
  with `--disable-gpu-vsync --disable-frame-rate-limit` (and `--use-angle=metal --enable-gpu
  --ignore-gpu-blocklist` on a Mac) to measure frame time.
- With a composer, `renderer.info` resets on each pass and reports one draw call. Set
  `info.autoReset = false`, reset it once, wait for one frame, read it, then restore it.

Measure while walking (hold a key), not on a still view: a host running on demand renders nothing
when nothing changes.

A hidden tab or hidden preview pane shows an empty canvas, because ui-foundation `Scene` pauses
offscreen before the first frame is drawn. Show the pane before judging the look.

## Verify
In addition to the floor-plan checks:
- Sunlight falls through each window onto the floor, and nowhere else (check the roof slab).
- Ceilings are pale, not brown; no hot spot on the ceiling above a fill light.
- Plaster and wood read as surfaces at walking distance, with no blotches or repeating stripes.
- Rugs are walkable; every other piece blocks, and each piece fills its plan footprint and faces its
  `facing`.
- Only lamps and downlights bloom; white walls do not.
- Labels on the plan stay readable over furniture symbols; the dip to dark is absent under reduced
  motion.
- Frame time measured as above at desktop and phone sizes, with the numbers and GPU recorded.

## Limits
- No true bounce light or colour bleed; the emissive ceiling and fills approximate it. Bake for that.
- Glass shows no reflection of the room; transmission here only tints the view outside.
- The sun is fixed. Moving it needs the shadow camera refitted and the environment re-rendered.
- Not checked on real phones, in Safari or Firefox, or over long sessions (texture memory).
