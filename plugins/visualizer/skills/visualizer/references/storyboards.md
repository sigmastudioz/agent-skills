# Deterministic storyboard renderer

Requires Python 3.10+, Pillow, FFmpeg with libx264 and AAC, and two local TrueType/OpenType
fonts. Resolve font paths on the execution host; fonts are not redistributed by this skill.
Use another renderer when these simple graph/code/metric scenes cannot explain the topic.

```sh
python scripts/render.py project/storyboard.json --output project/demo.mp4 \
  --font /path/to/body.ttf --mono-font /path/to/mono.ttf \
  --size 1080x1920 --fps 30 --score --poster project/poster.png
```

Use `--validate-only` with the same font/size options for schema and text-layout checks.
Use `--still 12 --poster project/frame.png` for an individual frame without encoding.
Output files are not overwritten unless `--overwrite` is explicit. Rendering writes
temporary media next to the output and replaces it only after successful encoding.
`--score` synthesizes original tones; external speech/music mixing is a separate step.
Captions are emitted as an adjacent `.srt`, one cue per scene. These are on-screen
scene summaries, not a transcription of speech that this renderer does not generate.

Top-level fields:

| Field | Meaning |
| --- | --- |
| `brand` | Short publisher label, e.g. `SIGMASTUDIOZ` |
| `author` | Byline, e.g. `Lex from SigmaStudioz` |
| `scenes` | Nonempty list, maximum 60; total runtime at most 300 seconds |

Every scene has `id`, `duration` (2–30 seconds), `eyebrow`, `title`, `body`, `caption`,
and `kind` (`graph`, `code`, `metrics`, or `end`). Keep titles short. The renderer
rejects overflow instead of silently clipping. Newlines in titles are not fixed layout.

- `graph`: `nodes` list with unique `id`, short `label`, normalized `x`/`y` (0.1–0.9),
  and optional `tone` (`accent`, `good`, `gap`). `edges` contain `from`, `to`, and
  optional `tone`. Nodes appear in sequence; edges reveal with traveling flow marks.
  Avoid intersecting labels; schema checks cannot establish good diagram composition.
- `code`: `lines` list (at most 10), optional `label` and `highlight` zero-based indices.
  Show only the relevant excerpt; manually split long commands with real shell continuations.
- `metrics`: `items`, at most three objects with `value` and `label`; values must have
  evidence outside the renderer. `label` can identify the exact historical baseline.
- `end`: `lines`, at most 10; useful for an install command or a link and next action.

Use `caption` for one concise sentence; it is drawn inside the lower safe area.
The renderer uses a charcoal/violet/mint palette and portable layout templates for
portrait/landscape. A custom visual direction requires editing or selecting a suitable
renderer; this helper is not an illustration or cinematic-generation model.

Example scene:

```json
{
  "id": "flow", "duration": 5, "kind": "graph", "eyebrow": "01 / EXPLAIN",
  "title": "Follow the signal", "body": "Input becomes an observable result.",
  "caption": "Trace both the successful route and its failure path.",
  "nodes": [
    {"id": "in", "label": "Input", "x": 0.2, "y": 0.25},
    {"id": "out", "label": "Result", "x": 0.8, "y": 0.7, "tone": "good"}
  ],
  "edges": [{"from": "in", "to": "out"}]
}
```

Do not put the supplied reference video or an unknown third-party soundtrack in the
skill folder. Store project-specific evidence and private media outside public exports.
