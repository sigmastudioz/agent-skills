# SigmaStudioz Visualizer

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · MIT · version 1.4.5.

Build interactive diagrams, simulations and editable visualization videos with React Three Fiber, reusable scenes, shaders and sound. By Lex from SigmaStudioz.

## Changes in 1.4.5

Two recipes, each built and checked as a small working demo first. The data reference gains a
data city: grouped 3D bars with an orthographic camera, a no-data state, selection by stable id,
and the table and plan view that keep it honest. The interactive reference gains explainer controls
for a 3D subject: a cutaway toggle, camera-shot hotkeys, rewind to a beat, and notes pinned to
parts, with a text list and reduced-motion behaviour.

## Changes in 1.4.4

Uses one credential-free environment policy for the sound bridge, storyboard encoder and
media-in-3D decoder/encoder. Child tools receive selected executable directories, fixed locale
and offline flags where appropriate, with no copied host environment, credential/proxy variables,
home-directory setting, Python injection variables or FFmpeg report setting. The sound bridge
no longer reads even the previous OS/temp/locale environment allowlist. Windows' system directory
is queried from the OS. Existing local tool configuration and anonymous downloads remain.

The Claude manifest explicitly declares no MCP servers. Regression checks exercise real child
processes and an actual storyboard encode with sentinel credentials in the caller. Anthropic's
scanner must independently verify warning clearance; this does not resolve organization eligibility.

## Changes in 1.4.3

Isolates local sound-tool environments from host credentials and proxy settings, restricts
audio-download output types and decoders, and preserves valid audio provenance.

## Changes in 1.4.2

Sound design: derive a mechanism's pulse rate from the mechanism (a V8 fires RPM / 60 × 4 times a second, with uneven spacing per exhaust bank) and keep the formula in the cue sheet.

## Changes in 1.4.1

Adds a brief pattern for looping and interactive assets to the motion vocabulary: loop length first, one verb per element, what stays fixed, and named states such as Ambient and Focused.

## Changes in 1.4.0

Folds the remaining local video workflow into this package: reference-to-timed-spec,
character and world consistency, montage and compositing, and media in 3D (with its optional
offline study adapter and tests). Adds a [motion vocabulary](skills/visualizer/references/motion-vocabulary.md)
that turns named effects into constructions, reuse candidates and review targets;
[beat maps and word timing](skills/visualizer/references/timing-maps.md); look presets in the
art-direction reference; motion tokens in the timed spec; an engine-discovery note; and a
contact-sheet check before full export. Also adds optional renderer notes for raea and
HyperFrames (telemetry off, never `skills update`), 31 more motion-vocabulary entries with the
name + duration/strength/subject rule, and an independent critique loop (fresh critic per round when
delegation is authorized, three rounds by default). These additions came from reviewing saved motion-design
posts; they are guidance, not efficacy claims.

## Changes in 1.3.1

Adds explicit even-dimension validation (640–3840 pixels), a supported Pillow dependency range,
portable CLI regressions and updated sound-runtime commands. The video-only local workflow is
merged into this existing package; interactive diagrams, data, React Three Fiber, shaders,
manual export guidance and demos remain available. Existing sound-output collision safeguards
are retained. [Pressure scenarios](skills/visualizer/tests/README.md) contain synthetic inputs
and historical results with explicit limits, not a new efficacy claim.

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

## Sound-design workflow in 1.3.0

The [sound-design pass](skills/visualizer/references/sound-design.md) adds editable cues,
asset rights and provenance, audible onset/peak/end anchors, speech-safe mixing and
review of the actual encoded export. Intentional silence remains a valid choice.
The [sound runtime and bridge](skills/visualizer/references/sound-runtime.md) connect
Openverse audio discovery/download, Earshot generation and Real SFX mixing. Tools
use a separately provisioned isolated host runtime; no automatic installation, model
fetch, account setup or upload follows from installing Visualizer.

A local 12-second integration test exercised a CC0 asset from Openverse's source/license
filter route, an Earshot whoosh and narration mixed through Real SFX. Effect peaks
landed within 9 ms of their targets at 30fps; the encoded mix measured −16.0 LUFS and
−3.6 dBTP, and local ASR recovered all narration words. These are scoped technical
checks, not subjective listening approval or fresh native-agent efficacy.

Openverse keyword queries timed out during the test; explicit filtered browsing and
download worked. Optional analysis models and FFmpeg drawtext/rubberband paths were
not exercised. The bridge refuses existing MP4s and same-basename stems/reports/work
folders before invoking the mixer. Existing interactive/R3F routes and both earlier
demos remain available; marketplace reviewer activation is separate.

## Feedback and learning in 1.2.1

The [learning reference](skills/visualizer/references/learning.md) connects reviewed feedback
to bounded storyboard and production decisions. Keep project-specific identities, assets,
voice choices and configuration in project notes. Promote only supported reusable lessons;
a successful encode and creative approval are distinct observations. This instruction update
preserves the existing interactive/R3F routes, renderer, demos and stable `visualizer` identity.
It does not imply model training, background learning or fresh native-agent efficacy.

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

### Credential and execution boundaries

The sound bridge requires no API credentials. Version 1.4.3 replaces inherited
subprocess environments with explicit tool paths, offline flags and OS/temp/locale
settings. Anonymous downloads do not use host proxy credentials. Fetch writes audio
data only; downloaded-audio decoding rejects playlist demuxers and network protocols.
Downloaded audio is never run as code. Earshot and Real SFX remain separately
provisioned, revision-checked local tools; installation examples are not automatic
plugin execution. See the [runtime contract](skills/visualizer/references/sound-runtime.md).

The Claude manifest is `.claude-plugin/plugin.json`; it registers no MCP server,
credential environment, hook or secret input. The root `plugin.json` supports other
hosts. Claude directory notes about that file, `icon` and `documentationUrl` do not
require removing cross-host metadata. The directory's Verified-organization gate
for bundled scripts remains separate from these runtime fixes; no directory
acceptance or live activation is implied.
