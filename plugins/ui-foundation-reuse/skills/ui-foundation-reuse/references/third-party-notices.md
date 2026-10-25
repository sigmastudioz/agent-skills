# Bundled runtime licenses and attribution

The ui-foundation implementation is Copyright (c) 2026 Sigma Studioz and is
distributed under the MIT license in `LICENSE`. Retain that license when sharing
the skill or its bundled runtime. The following mesh datasets retain their own
attribution licenses; the MIT license does not replace them. Notices also remain
in their source and compiled geometry modules and the runtime README.

## Head particle geometry

**Infinite, 3D Head Scan**, Lee Perry-Smith / Infinite-Realities. Based on work at
triplegangers.com. Licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/).

- [Source geometry](https://threejs.org/examples/models/gltf/LeePerrySmith/LeePerrySmith.glb)
- [Distributed original notice](https://threejs.org/examples/models/gltf/LeePerrySmith/LeePerrySmith_License.txt)
- Changes: shoulders cropped, centered, scaled, ray-sampled, quantized and rendered
  as particles; textures omitted.
- Included in `src/particle-form/headMeshData.ts` and its compiled equivalents.

## Brain particle geometry

**BodyParts3D, © The Database Center for Life Science licensed under CC Attribution
4.0 International**. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
[official license](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html),
[dataset](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html).

Uses the 59 FMA50801 brain elements in the 4.0 PART-OF release plus the six
additional FMA55676 cortical elements from IS-A (orbital and superior temporal
gyri). Changes: brain structures combined, axes converted to Y-up, centered,
scaled, ray-sampled and quantized; textures omitted. The atlas geometry remains
CC BY 4.0.

Included in `src/particle-form/brainMeshData.ts` and its compiled equivalents.

## External dependencies and user assets

React and optional rendering peers are not bundled. Install them separately under
their own licenses. Photos, videos, audio, fonts, downloaded models and playground
assets are not included; supply app-owned or appropriately licensed assets when
an effect requires them. Attribution links are notices, not runtime downloads.
