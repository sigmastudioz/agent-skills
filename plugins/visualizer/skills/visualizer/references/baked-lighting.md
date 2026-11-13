# Baked lighting for static scenes

By [Lex from SigmaStudioz](https://github.com/sigmastudioz).

Read this when a React Three Fiber or Three.js scene should look softly lit (bounce light, glowing
surfaces, shafts of light) inside a browser or artifact budget. Baking moves that lighting into
textures offline, so the page draws it for almost nothing. The idea is common in browser 3D demos;
it reached this skill from a creator's video on browser 3D game demos, whose stated per-demo costs
are his own claims and whose prompts were not used.

Checked 2026-11-13 on a small room (five walls, three boxes, an emissive ceiling panel and wall
strip): Blender 5.2.3 Cycles, a 1024 px lightmap, glTF export, Three.js 0.186, React Three Fiber
9, Drei 10, headless Chromium on an Apple M1 Max. Treat other versions and GPUs as unverified.

## When to bake
- The lit geometry does not move, and neither do the lights.
- The camera is fixed or limited to a small range (see the trade-off below).
- The target is a browser page, an embedded artifact or a phone, where shadow maps and several
  lights cost real frame time.

Do not bake a scene whose lights, layout or time of day change, and do not bake moving objects.
Keep those live, and light them cheaply (see reflections below).

## Bake a lightmap in Blender
1. Give the static meshes a **second UV set** for the lightmap, with every face in its own space
   and a margin between islands (Smart UV Project with an island margin works). Keep the first UV
   set for ordinary textures. Faces the camera never sees still take lightmap space: delete them or
   leave them out.
2. Create the bake image as **32-bit float and non-colour data** (`bpy.data.images.new(...,
   float_buffer=True, is_data=True)`). A new image is tagged sRGB by default, and Blender applies
   that when saving: the file then holds display-encoded values. In the check this made the scene
   30–130 % too bright and flat in the viewer while Blender's own preview still looked right.
3. Add an unconnected Image Texture node holding that image to every material and make it the
   active node. Bake with Cycles, type Diffuse, with Direct and Indirect on and **Color off**, so
   the map holds lighting only and the surface colour stays in the material. Use a margin of about
   8 px. Emissive meshes light their neighbours in this bake.
4. Save as OpenEXR (or Radiance HDR). Remove the bake node, then export the meshes as GLB; both UV
   sets go out as `TEXCOORD_0` and `TEXCOORD_1`.
5. Render one frame in Cycles from the camera the page will use. It is the reference the page is
   judged against.

Here the bake took 54 s at 1,024 samples on the GPU and some grain remained; denoise the map or
raise samples before shipping.

## Apply it in Three.js or React Three Fiber
```ts
// lightmap: the EXR loaded with EXRLoader; meshes: the GLB's meshes
lightmap.channel = 1                       // read the second UV set (uv1)
lightmap.colorSpace = THREE.LinearSRGBColorSpace
lightmap.repeat.set(1, -1); lightmap.offset.set(0, 1)   // see the row-order note below
for (const mesh of meshes) {
  const m = mesh.material as THREE.MeshStandardMaterial
  m.lightMap = lightmap
  m.lightMapIntensity = Math.PI            // lighting-only bake: restores the 1/pi of the diffuse term
  m.envMapIntensity = 0
}
// No lights in the scene. Emissive materials keep their own emissive colour and strength.
```
- **Intensity.** With a lighting-only bake, `lightMapIntensity = Math.PI` matched the Cycles
  reference within 3–9 % in five regions; an intensity of 1 came out at 0.3 of the reference.
- **Row order.** glTF puts v = 0 at the top of an image. The EXR here loaded with its rows the other
  way up, so V had to be flipped with the texture transform; a Radiance HDR loaded with
  `flipY = false` did not need it. Check the mapping against something recognisable, such as the
  shadow under an object, before judging brightness.
- **No scene-wide environment map.** `scene.environment` (or Drei's `<Environment>`) lights every
  standard material as well as the lightmap. In the check it more than tripled the room's brightness.
  Put an `envMap` on the reflective materials only.
- **Tone mapping.** Compare with tone mapping off and sRGB output, against a reference rendered
  with Blender's Standard view transform. Add a tone curve afterwards if the look calls for it.

## Reflections and moving objects
Render an equirectangular panorama from the middle of the scene in Cycles (panoramic camera,
equirectangular, saved as HDR) and load it as the `envMap` of reflective or moving objects (Drei's
`useEnvironment({ files })` prefilters it). They then reflect the baked room without a live
reflection pass. A moving object still has no shadow on the baked floor: give it a small blob or
contact shadow of its own. The reflection is correct only near the point it was rendered from.

## Light shafts
Fake them. Place a few planes where the shaft should be, with a soft gradient texture, additive
blending, `depthWrite` off and `toneMapped` off, slightly fanned so they do not look like one card.
Keep them faint (the check used a peak alpha of 0.2); at 0.55 they read as a solid white column.
They are view-dependent, which is another reason to limit the camera.

## The fixed-vantage trade-off
A fixed or narrowly limited camera buys fidelity: lightmap texels are spent only where the camera
looks, hidden faces can be dropped, light-shaft cards and the baked reflection stay convincing, and
one offline frame is enough to judge the page. It costs freedom: outside that range the viewer sees
low-resolution lightmap, flat cards and reflections from the wrong place. Decide the range before
baking, and clamp the camera controls to it.

## A lighter path
For objects on an open ground plane that only need a soft shadow, Drei's `AccumulativeShadows`
with `RandomizedLight`, or `BakeShadows` to freeze ordinary shadow maps, avoid the Blender step.
They add no bounce light or glow. Not verified here: two configurations in the enclosed test room
rendered the whole floor dark, because that helper expects open ground. Check it in a scene of the
right kind before relying on it.

## Verify
1. Screenshot the page at the bake's camera and compare it with the Cycles reference: the same
   regions (a wall, the floor, a face in shadow) should be within about 10 % in linear light.
   Here the baked page differed from the reference by a mean of 3.6 of 255 per channel, against
   21.0 for the same scene lit with two shadow-casting point lights.
2. Screenshot the same camera with real-time lights instead of the bake, and show both to the user.
3. Measure the frame: time a few hundred renders with a one-pixel read-back after each (so the GPU
   finishes), and read `renderer.info.render.calls`. Here: 7 draw calls and about 0.7 ms a frame
   baked, against 57 draw calls and 2–3 ms with two point lights and 2048 px shadow maps.
   These are one machine's numbers; measure on the device that matters.
4. Check the things a still hides: the camera limits, a moving object's reflection and shadow, and
   the lightmap at the closest allowed distance.
