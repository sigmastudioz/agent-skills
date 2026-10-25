# SigmaStudioz Visualizer

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · MIT · version 1.2.0.

Build interactive diagrams, simulations and editable visualization videos with React Three Fiber, reusable scenes, shaders and sound. By Lex from SigmaStudioz.

## Watch the demo

https://github.com/user-attachments/assets/7bb28e63-35e4-40de-b639-f50430f04ab4

A 36-second React Three Fiber film by **Lex from SigmaStudioz**: refractive glass, brushed
alloy and a procedural pigment surface reveal one shared illustrative model. Smooth 1080p60
animation is paired with an original stereo score and synchronized synthesized effects.
The editable preview adds keyboard controls, object selection, motion settings and sound feedback.

[Download MP4](../../assets/visualizer-r3f-demo.mp4?raw=true) ·
[Captions: SRT](../../assets/visualizer-r3f-demo.srt) / [VTT](../../assets/visualizer-r3f-demo.vtt) ·
[Poster](../../assets/visualizer-r3f-demo-poster.png) ·
[Editable React Three Fiber sources](../../assets/visualizer-r3f-demo-source.zip?raw=true)

The film is an authored demonstration, not a recorded agent session or a production
performance benchmark. Captions are timed scene summaries; there is no voiceover.
[Reproduce the preview and inspect export checks](../../assets/README.md#react-three-fiber-visualizer-film).

## UI Foundation Reuse upgrade: Light takes form

https://github.com/user-attachments/assets/18032b0e-c269-4d64-bb6f-b0b6106474b5

This additional 12-second film by **Lex from SigmaStudioz** demonstrates the 1.2.0
workflow with the **UI Foundation Reuse** companion: a bundled shader backdrop, shared
scene host, controlled assembly, glass material, reflective floor and seeded paper reveals
compose an original sculpture. The app owns the geometry, composition and capture clock.

[Download MP4](../../assets/visualizer-ui-foundation-demo.mp4?raw=true) ·
[Captions: VTT](../../assets/visualizer-ui-foundation-demo.vtt) ·
[Poster](../../assets/visualizer-ui-foundation-demo-poster.png) ·
[Editable source ZIP](../../assets/visualizer-ui-foundation-demo-source.zip?raw=true) ·
[Export checks](../../assets/visualizer-ui-foundation-validation.json)

The film is 1280×720 at 24 fps with an original synthesized stereo score; captions
are scene summaries, with no narration. The source includes runtime 0.5.0, licenses
and an app-specific frame adapter. Its selected effects demonstrate actual reuse;
this does not imply every effect supports seeking or establish fresh agent efficacy.
[Reproduction and timing limits](../../assets/README.md#ui-foundation-reuse-upgrade-film).

## Install

```sh
npx skills add sigmastudioz/agent-skills --skill visualizer
```

Or register this repository as a Claude marketplace and select `visualizer@sigmastudioz`.
The package includes Claude, Cursor and Codex manifests. Native directories require separate
review; repository availability does not mean this plugin is approved by any marketplace.
Normal skill discovery is enabled for relevant requests; installation does not rewrite global
settings or guarantee selection on every model, desktop or remote host.

## Capability and limits

One unified skill supports interactive explanations and video generation, with shared model,
scene/time, data and evidence contracts. Read only the references needed for the requested mode.
It covers charts, diagrams, simulations, React Three Fiber/Three.js shaders, art direction, sound, captions,
accessible interaction, exports, performance evidence, gap tracing and agent handoffs.

No renderer, commercial generation account or media library is automatically installed. Agents
use existing project/host tools and must deliver and verify actual artifacts. Reference art is
not redistributed. Video Analysis can supply an evidence brief but is an optional separate skill.

## Local video workflow and runtime reuse in 1.2.0

The existing `visualizer` identity now includes the latest Visualization Videos guidance:
reference-led storyboards, art direction, layered motion and sound, shader/export timing,
and the optional deterministic Pillow/FFmpeg renderer. Read its
[storyboard contract](skills/visualizer/references/storyboards.md) before running it.
Pillow, FFmpeg and fonts are external prerequisites; no global install occurs.
The helper is suitable for simple diagrams, code and metrics, not every creative reference.

For compatible React effects, add the companion alongside Visualizer:

```sh
npx skills add sigmastudioz/agent-skills --skill ui-foundation-reuse
```

Use the separate
[UI Foundation Reuse companion](../ui-foundation-reuse/README.md). It includes its runtime;
Visualizer does not duplicate that archive. Inspect installed exports and motion clocks
before promising frame-driven capture. Keep interactive and film outputs tied to one
model/timeline; preserve a suitable non-React renderer.

The original demo above remains a historical authored example. This instruction/helper
update does not establish fresh native-agent efficacy or directory approval.

## React Three Fiber introduced in 1.1.0

For new React 3D work, the skill now prefers composable R3F scenes over imperative scene setup.
It covers compatible dependencies, stable shader uniforms, Drei helpers, demand rendering,
resource ownership, accessible controls and one deterministic timeline for interaction and film.
The [R3F reference](skills/visualizer/references/react-three-fiber.md) includes a TSX component and
a method for adapting [pmndrs examples](https://pmndrs.github.io/examples/) into original visuals.

Existing vanilla Three.js projects and lightweight 2D charts keep their appropriate renderer.
The demo above uses React Three Fiber and Drei with a shared deterministic timeline. No R3F
dependencies install automatically, and this demo does not imply new native marketplace approval.

## Example requests

No test account or paid API is required. Use a host that can write and preview local HTML;
video exports additionally need an available renderer and encoder. These are review scenarios,
not claims of fresh-agent test results.

1. “Using React Three Fiber, build an interactive queue simulation with adjustable arrival and service rates. Label it
   illustrative, explain its assumptions, show overload clearly, and add keyboard controls.”
2. “Visualize this synthetic series: Jan 12, Feb 18, Mar 15. Keep the unit ‘orders’, include a
   zero baseline and a readable data table, and let me toggle the series without losing context.”
3. “Create a 15-second code-rendered film explaining a three-stage pipeline. Use original geometry,
   smooth motion, optional original sound, captions and editable sources. Verify the actual export.”

## Evidence and support

See [the skill](skills/visualizer/SKILL.md), [collection validation](../../docs/visual-skills-validation.md)
and [Privacy](../../PRIVACY.md). Packaging checks are distinct from fresh-agent efficacy.
Report issues without private media, credentials or transcripts. No universal performance or
automatic activation claim is made.
