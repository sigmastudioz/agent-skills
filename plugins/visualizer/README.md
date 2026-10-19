# SigmaStudioz Visualizer

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · MIT · version 1.1.0.

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

## React Three Fiber in 1.1.0

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
