# Demo and editable sources

By **Lex from SigmaStudioz**. [Watch the 50-second demo](ddd-demo.mp4?raw=true) ·
[Scene captions](ddd-demo.srt) · [Download the runnable source ZIP](ddd-demo-source.zip?raw=true).

Extract the ZIP and open a terminal in `sigmastudioz-demo/`. With Node.js 20 or later:

```sh
node demos/refunds/reproduce-gap.mjs
node --test demos/refunds/*.test.mjs
```

The first command reproduces a deliberately unsafe boundary against an isolated,
synthetic in-memory store; the second checks the repaired implementation (18 cases).
No network services, external dependencies or payment provider are used by this fixture.
The fixture README explains its limits, including absent production concurrency and durability.

To edit the video, change `demos/video/film/film.json`. The archive includes the
film renderer, interactive preview, and reproduction instructions in `demos/video/README.md`. Requires Python
with Pillow/NumPy, FFmpeg/libx264/AAC and local fonts; fonts are not redistributed.
The 60fps film has GPU-baked paper lighting, pearlescent sheen, cue-synchronized ripples,
an original stereo score and 33 synchronized, synthesized effects. Its editable
preview uses Three.js with a locally bundled dependency and plain-video fallback. There is no voiceover.
The SRT contains scene summaries, not a transcription of speech.

The animation is a visual replay of recorded Claude Code 1.0.5 evidence, not a new
live session. Versions 1.0.6 and 1.0.7 update branding and packaging; the recorded coding-test baseline remains 1.0.5. The archive includes the public
validation receipt and MIT license. It contains no private agent transcripts or
third-party reference footage, illustrations, presenter, voice or soundtrack.


## Visualizer and Video Analysis films

Two original 32-second films by **Lex from SigmaStudioz**, rendered with Three.js shaders
at 1920×1080 and 60 frames per second, with original stereo music and synthesized effects.
There is no voiceover; SRT and VTT files contain timed scene summaries.

| Film | Watch/download | Captions | Poster |
| --- | --- | --- | --- |
| SigmaStudioz Visualizer | [Full HD MP4](visualizer-demo.mp4?raw=true) | [SRT](visualizer-demo.srt) · [VTT](visualizer-demo.vtt) | [PNG](visualizer-demo-poster.png) |
| SigmaStudioz Video Analysis | [Full HD MP4](video-analysis-demo.mp4?raw=true) | [SRT](video-analysis-demo.srt) · [VTT](video-analysis-demo.vtt) | [PNG](video-analysis-demo-poster.png) |

[Download the editable source bundle for both films](visual-skills-demo-source.zip?raw=true).
Extract it, read its README, and run `python3 source/server.py` from the extracted folder.
The loopback preview is `http://127.0.0.1:8773/preview.html`; `watch.html` plays the finished films.
Reproduction needs Python 3.10+, NumPy, FFmpeg/ffprobe and a WebGL2-capable browser.
The archive includes pinned Three.js 0.186.1 with its MIT license, original mastered audio,
storyboards, shaders, captions, evidence and export checks. It installs nothing automatically.

Visualizer illustrates a deterministic fluid queue and the model-to-scene-to-export workflow.
Video Analysis displays six actual timestamped samples from our original six-second synthetic
clip; the released sampler returned eleven frames within a twelve-frame budget. Sparse frames
do not establish exhaustive viewing or audio understanding. Both films are authored
demonstrations, not recordings of fresh agent sessions or production performance benchmarks.

Both exports passed full decoding, frame-count and browser-playback checks. Measured encoded
loudness is −16.2 LUFS for each; true peaks are −1.53 dBTP and −1.40 dBTP respectively.
These structural measurements do not substitute for a listening review.
The original visuals, music, synthesized effects and source are MIT by Lex from SigmaStudioz;
Three.js retains its included MIT notice. No private media, reference footage or session logs
are redistributed. Files live outside plugin folders to keep skill distributions small.


## React Three Fiber Visualizer film

The current Visualizer demo is a new 36-second 1920×1080/60fps material study by
**Lex from SigmaStudioz**. [Watch/download MP4](visualizer-r3f-demo.mp4?raw=true) ·
[Captions: SRT](visualizer-r3f-demo.srt) / [VTT](visualizer-r3f-demo.vtt) ·
[Poster](visualizer-r3f-demo-poster.png) ·
[Editable source ZIP](visualizer-r3f-demo-source.zip?raw=true) ·
[Validation](visualizer-r3f-validation.json). The earlier films above remain available.

Original refractive geometry, procedural GLSL, studio lighting, smooth transitions and a stereo
score share one deterministic model and clock. The live preview includes keyboard ranges,
selection, reduced motion, mute/volume and bounded user-gesture feedback. Inspiration from the
pmndrs examples informed lighting, materials and flow; no example code, artwork or media was copied.

Extract the source ZIP and read `visualizer-r3f-demo/README.md`. It includes source, lockfile,
original mastered audio, finished film, scene captions, encoder dependencies, license notices and
verification evidence. Generated `dist/` is omitted to avoid duplicating media; `npm run build`
recreates it. Reproduction needs compatible Node, Python with NumPy/Pillow, FFmpeg/ffprobe and WebGL2.
Nothing is installed automatically. All browser dependencies and Manrope font assets build locally.

The final MP4 passed full decode: 2160 frames, 36 seconds, H.264/yuv420p and stereo AAC.
Encoded sound measured −15.35 LUFS and −1.67 dBTP. TypeScript, analytic-model regressions,
keyboard controls, compiled preview, native playback and actual GPU-loss recovery were checked.
Offline 60fps is not a realtime performance promise. This is an authored demonstration, not a
fresh-agent efficacy test; captions are scene summaries without voiceover. Subjective listening
was not performed by the agent. Original work is MIT by Lex from SigmaStudioz; dependencies
retain their included licenses. No reference footage, private transcripts or account data is included.
