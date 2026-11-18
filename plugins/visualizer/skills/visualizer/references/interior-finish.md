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
- **Windows** `{ x, z, width, sill, head }`, centred on a wall line like a door, under the door's
  rules: on exactly one wall line, with no crossing or touching wall inside the opening, and not
  overlapping a door or another window. Reject a window
  that is not on an *exterior* wall (a room on one side only), that is not inside a stretch left
  solid after door cuts, or whose sill is below 0 or head not above the sill. Keep the head below
  the wall height (2.6 m here). A window is visual only: collision keeps the full wall, so no one walks out through the glass.
- **A floor finish per room** (`floor: 'oak' | 'walnut' | 'tile'`), optional, with a default.
- **Furniture `kind` and `facing`** (`'n' | 'e' | 's' | 'w'`, the way the front of the piece
  looks). The kind picks the generator; the footprint `{ x, z, w, d, h }` stays the source of size.
- **`solid: false`** for walk-over decor such as rugs. Collision and "standable" checks skip it;
  the plan and the 3D view still draw it. Without it, a rug blocks the room it lies in.

- **A default `facing` of `'s'`** (front toward +z) when a piece omits it.
- **A ceiling height** (`ceiling`, default 2.6 m) when the plan states one; lofts often run 3.3–3.6 m.

Keep the plan's furniture rule (inside one room) for rugs too, and tighten it: furniture must clear
the wall faces, so inside the room minus half the wall thickness on each side. A wardrobe drawn to
the room edge otherwise sits 7 cm into the wall.

## Architecture from the plan
Generate every architectural mesh from the plan output, never by hand, so the 3D view, the SVG and
collision cannot drift:
- **Walls with windows.** For each wall segment, subtract its window spans to get solid stretches,
  which run full height. Each window adds a piece below the sill and one above the head. At a corner or
  T, fill the junction square once: extend the free ends of runs along x by half the wall thickness
  and leave runs along z flush. Extending both makes the two volumes overlap with coplanar faces. Never
  extend an end that is a door or window jamb. Add a slim dark frame (four sides and a mullion), a thin glass pane, an inside and outside
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

## Luxury finish
The checked finish reads as a tidy show home. For a luxury apartment, these additions made the
largest difference, in order (checked on four traced apartment plans, same versions as above):
- **Height and windows.** Use the stated ceiling (lofts are often 3.3–3.6 m) and run windows nearly
  floor to ceiling (sill about 0.4 m, head 0.35 m below the ceiling) with steel divided lights: bars
  about every 0.42 m across and 0.5 m up, 22 mm wide, in the black frame material.
- **Drapes.** Two floor-to-ceiling linen panels per window on the room side, each about 0.42 m wide,
  pulled past the window edges, with a slim black rod. Find the room side by probing 0.3 m either
  side of the wall line. Fold them with a sine displacement on a subdivided plane so they catch
  the window light, and use a sheen material, not flat colour.
- **Mouldings.** Crown moulding in two stepped strips at the ceiling, and skirting 16 cm tall.
- **Materials.** Wide-plank light ash (24 cm boards, longer lengths) for living rooms and bedrooms;
  polished marble (soft blurred veins plus a few crisp ones, roughness about 0.15, clearcoat) for
  bathroom floors in 60 cm tiles, and for worktops, the island, vanity tops, the coffee table and
  the dining table. Give upholstery `MeshPhysicalMaterial` sheen so velvet reads at grazing angles.
  Use deep colours (bottle green, cognac) against the pale shell, and brass for legs and fittings.
- **Light fittings.** A brass ring chandelier over each dining table, hung above eye height (about
  1.8 m): at 1.6 m it reads as a flat line. Pendants over the island hang from the actual ceiling.
- **Art.** One large framed canvas per room, on the longest wall stretch with no window, door or
  furniture taller than 1.2 m within 0.9 m of it, about 60% of that stretch wide (at most 1.6 m),
  centred at 1.55 m. Generated soft colour fields in a muted palette avoid any image licence.
- **Stairs.** Open walnut treads with steel stringers and a brass rail, not a block.
- **Walls.** Picture-frame panelling in every room but the bathrooms: a chair rail at 0.9 m, a box
  below it and a tall box above it in bays of about 1.1 m, cut 12–14 cm clear of doors and windows.
  Build every strip as a box, merge them all into one geometry (`mergeGeometries`) and draw the
  house's panelling as one mesh in the wall material; frame time did not move.
- **Kitchens.** Two-tone joinery: deep sage shaker doors (a plate plus a raised frame) with brass
  knobs, a 3 cm marble top and a marble splashback up to the wall cabinets, wall cabinets to about
  2.9 m with an emissive under-cabinet strip and a warm point light, a plaster hood over the hob in
  place of the cabinets there, an undermount sink with a brass gooseneck tap, and a panel-front
  fridge with long brass pulls. Where a window is behind the run, drop the wall cabinets and keep a
  low marble upstand. The island gets a fluted base (a striped colour and bump texture, not one
  mesh per flute) and marble waterfall ends. Make the hob and sink matte (roughness 0.3 or more): a
  glossy black glass top mirrors the sky and reads pale blue.
- **Beds.** A channel-tufted headboard about 1.3 m tall spanning the bedsides, an upholstered base,
  a duvet folded back, a bouclé throw at the foot, euro shams, pillows and a lumbar cushion, and a
  rug that reaches past the foot and sides. Panel-door wardrobes with long brass pulls and a cornice.
- **Bathrooms.** Generated, since no CC0 library checked has modern fittings:
  - polished marble cladding to 1.2 m on every wall with a brass cap rail, cut around doors and kept
    below window sills, and no wall art there;
  - a freestanding stadium-shaped bath (an extruded outline with a hole, bevelled) with a floor-standing
    brass filler;
  - a floating walnut vanity with a marble top, a lathe-turned vessel basin and a tall brass tap per
    basin (two from 1.3 m wide);
  - a round mirror per basin in a brass frame with a thin warm halo ring behind it, and a brass sconce
    either side.

  Make the mirror a mid-grey metal (about `#9aa2a9`, roughness 0.04): a pale one reflects the bright
  fill light and reads as a glowing disc, and so does a full halo disc behind it. Put towels on the
  vanity top, not on a rail placed relative to another fitting: such a rail ran across the vanity in
  two of four bathrooms.

**Doors.** A painted leaf with three raised panels a side and brass levers, standing open about 85°
in every opening up to 1 m wide; wider openings stay open-plan with no leaf. Hang it by one rule
that the 3D leaf and the plan's swing arc both read: open into a room rather than a hall or
corridor, into the larger room between two rooms, hinged at the end nearer that room's corner so
the open leaf rests near a wall. Merge each leaf's mouldings into one mesh. Draw swing arcs only for
openings that get a leaf.

**Two storeys.** A loft plan with a mezzanine needs a level per floor, not a taller ceiling. Keep
each floor an ordinary validated plan and add, around them:
- `upper: { elevation, rooms, doors, windows, furniture, open, doubleHeight }` and
  `stairs: [{ x, z, w, d, up }]`, where `up` is the direction you walk to climb, `open` lists the
  upper wall lines drawn as glass balustrade, and `doubleHeight` names the lower rooms that rise to
  the roof.
- Validation per stair: it is wide enough to walk, its foot is reachable on the lower floor, and
  its top lands in an upper room. A tracing mistake should name the stair, not fail later as "the
  start is not in a room".
- Walking: the walker carries a level. On a stair the floor height follows the flight, so the
  camera rises with it; the level flips at the halfway point. A stair can be entered only at its
  foot from below or its top from above; its sides are solid. Upstairs, collide with the upper
  plan's walls (balustrades stay solid) and with the stair hole, open only at its top edge, and
  refuse any step that leaves the upper rooms.
- Drawing: lower walls take the height of what is above them (the roof beside a double-height
  room, the upper floor elsewhere), so split wall runs at every room edge on both floors. Cut the
  stair hole out of the upper floor, put a deep fascia under each open edge, roof the single-storey
  wing at the upper-floor level, and give each double-height room its tall windows (head about
  5.2 m) while the upper floor gets its own.
- The map shows one floor at a time with a Ground floor / Mezzanine switch. It follows the walker
  once they step off the stairs, keeps the ground floor's bounds so it does not jump, draws the
  ground floor faintly under the upper one, and lands plan clicks on the floor it shows. List every
  room on both floors in "Go to".
- Test it with the model (walk up, halfway height, walk down, no side entry, the mezzanine edge
  holds, clicks land on the shown floor, a stair landing nowhere is rejected) and in the browser
  by holding W from the foot of the stair. Checked 2026-11-17 on both traced lofts: the model
  tests pass 13/13 and the browser climb reaches the mezzanine and comes back down, in both.

Fit the outdoor context to the layout: shadow camera, sun distance, ground size and tree positions
from the bounds. A demo that hardcodes them for one house puts trees inside the next.

**Real models.** Primitives limit the furniture. Poly Haven (CC0) offers furniture, lights, plants
and vases as glTF, about 0.4–3 MB each with 1k textures; it has no toilets, baths, basins or
kitchen units, so those stay generated. Download only with the user's approval. Checked 2026-11-17
with 15 models: choose by look, not availability. The mid-century lounge chair, a concrete-and-wood
coffee table, tufted leather dining chairs, a potted plant, a shaded brass chandelier, a globe
pendant, display shelves and brass or ceramic vases suited a modern loft. Its sofas (carved and
chesterfield), console, nightstand, bar stool and tall side table are traditional or rustic and
looked like a period house, so the generated pieces stayed. Render each candidate alone and look at
it before placing it.

Load each through ui-foundation `Model` (it takes one uniform `scale` and no rotation) inside a
group that carries the piece's position and `facing`, then fit it:
- Wait for the meshes: the bounds stay empty until the glTF arrives, which took several seconds
  with all models loading at once. Give up only after about 30 s, and keep it hidden until fitted.
- Measure in the group's own frame: combine each mesh's geometry bounds with the inverse of the
  group's world matrix. `Box3.setFromObject` measures in world axes, which include the room position
  and the rotation, so turned pieces are scaled and placed wrongly.
- Scale uniformly to fit the footprint (and height, except plants), centre it, stand it on the
  floor. Hang ceiling fittings from the ceiling, with a cord down to about 2.5 m.
- Fall back to the generated piece if the model fails to load (an error boundary plus `onError`).

**Draw shadows once.** With models, drapes and the larger luxury plan, re-rendering every object into
the sun's shadow map each frame dominated: 92 ms per frame at 1440×810 2x on Residence 205 (a
traced plan, 10 rooms, about 340k triangles). Nothing moves, so set `gl.shadowMap.autoUpdate =
false`, set `needsUpdate = true` once, and again whenever a model finishes fitting. That gave
13–16 ms at the same size (10–20 ms at 1x, 10–13 ms on a phone-sized canvas), measured on a busy
machine with occasional long stalls. Remaining cost is mostly detailed models (each dining chair is
22k triangles) and point lights; instance repeated chairs and cap lights per room before phones.

## Light
Ceilings and walls facing away from the windows get no direct light, and realtime Three.js has no
bounce. Fake the parts that matter:

| Light | Settings that worked | Why |
| --- | --- | --- |
| Sun: one `directionalLight` with shadows | Intensity 3.4, warm white. Direction about 31° above the horizon, turned to face the main living windows. One sun cannot reach windows on opposite walls, so check sun only where windows face it. Shadow map 4096, bias −0.0003, normal bias 0.025. Fit the shadow camera to the house bounds plus a margin, and aim the target at the house centre (add the target to the scene). | A low sun reaches through the windows and draws patches on the floor. A loose shadow camera wastes resolution and makes edges soft and blotchy. |
| Image-based fill | Drei `Environment` with `frames={1}` and `resolution={256}`, holding `Lightformer` panels: a warm one overhead at least twice the house's size, a dim cool one on the main window side and dim warm ones on the other three sides. Three panels on one axis (overhead, window side, opposite) leave walls at right angles to it dark brown and turn walls facing the cool panel blue-grey; that was fine for the checked layout only because all its windows faced one way. | Gives every surface soft light and gives metal and glass something to reflect, without downloading an HDRI. Rendered once, so it costs nothing per frame. |
| Sky and ground tint | `hemisphereLight`, sky blue-white over warm ground, intensity about 0.35. | Lifts the shadow side without flattening it. |
| Ceiling "bounce" | Emissive on the ceiling material, about 0.32 of a warm white. | Without it the ceiling renders dark brown and the rooms feel like caves. |
| Room fill | One point light per room at about 1.5 m, not near the ceiling, intensity 0.7, distance 8, decay 1.6. | A fill near the ceiling leaves a hot spot on it. |
| Practical lights | Lamp shades and downlight discs with emissive above 1, and a small point light inside each lamp. | Gives bloom something real to catch, and warm pools by the furniture. |

Turn shadows on the canvas (`shadows: true`; `'soft'` asks for `PCFSoftShadowMap`, which Three.js 0.186 has removed, so it logs a warning and falls back to the same PCF shadows) and mark walls, floors, furniture and the roof as
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
| Subway splashback | 7.5 × 15 cm bricks, offset rows; stop it below any window sill above the counter (a low upstand there) | 0.25 | 0.5 |
| Upholstery | Fine weave tinted by the material colour | 0.95 | 0.8 |
| Stone worktop or ceramic | Plain colour, `MeshPhysicalMaterial` with clearcoat 0.4–0.6 | 0.22–0.25 | none |
| Glass | `MeshPhysicalMaterial` with opacity about 0.25, `depthWrite: false` and no transmission | 0.02 | none |

Transmission on glass makes Three.js render every opaque object a second time for the refraction pass; a fresh build that used it measured more than twice the draw calls. Plain transparency looks the same through a window.

Keep variation small. Plaster specks above about 1% opacity look like leopard spots on a large wall,
and plank-to-plank lightness swings above about ±3% make a dark wood floor look patchy.

## Furniture fitted to the footprint
Write one small generator per `kind`, in a local frame: width along x, depth along z, front facing
+z, origin at the footprint centre on the floor. Rotate by `facing` (s = 0, n = π, e = π/2,
w = −π/2), swapping width and depth for east and west, so the piece fills exactly the rectangle the
plan and collision use. Build from rounded boxes, cylinders and a few shapes: a sofa is a base,
back, arms, seat and back cushions and two angled throw cushions; a plant is a pot, soil, a stem and
about 30 leaf shapes from a seeded random. Write generators for every kind you know when building, including kinds the layout uses but this
recipe does not name (bookshelf, bathtub, vanity). Keep the plain rounded box, and a plain outlined
rectangle on the plan, for a kind nobody wrote a generator for, so a new layout never fails to render.

Real models look better, but need a source whose licence allows the use, approved before download.
Load them with ui-foundation `Model` and scale each to its footprint.

## Post-processing
Use one composer, and let it own tone mapping:

```tsx
<Scene canvasProps={{ flat: true, shadows: true, gl: { antialias: false } }}>  {/* flat: no renderer tone mapping */}
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
On the checked layout, with headless Chromium and vsync off: 1440×810 at 2x took a median of 6.5 ms
per frame (95th percentile 9.1 ms), 2.7 ms at 1x, and 2.6 ms at 390×844, with plain transparent
glass. That is about 410–460 draw calls and 75–90k triangles per frame, with 54 textures. With
transmission glass the same scene took 9.9 ms at 2x. Most of the draw calls are separate
rounded boxes in furniture. Before targeting phones, merge each static piece's geometry by material
or instance repeated parts, and drop the shadow map to 2048. These numbers do not transfer between
builds: a fresh build of a different layout from this recipe measured 1,060–1,330 draw calls and
310–380k triangles at about the same frame time, mostly from transmission glass and rounded-box
subdivision. Measure your own.

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
