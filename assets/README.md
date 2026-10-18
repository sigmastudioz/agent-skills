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
