# Run the integrated sound workflow

Read after [sound design](sound-design.md) when executing Openverse, Earshot and Real
SFX together. The [bridge](../scripts/sound_design.py) owns only discovery/download,
generation, cue adaptation and verification; keep the existing picture renderer.
It uses argument arrays, new outputs, bounded public downloads and offline Earshot
commands. It does not install software, create accounts or configure MCP on its own.

## Runtime discovery and setup

The default host config is
`~/.local/share/sigmastudioz/visualization-sound-tools/config.json`; override it with
`--config /path/to/config.json` before the subcommand. A host's config is local state,
not part of a distributed skill or project handoff. Check it with:

```sh
python scripts/sound_design.py doctor
```

An authorized setup needs Git, Python 3.10+, FFmpeg/ffprobe with libx264/AAC and the
audio filters used by the selected path. In a new isolated runtime folder, clone
[Earshot](https://github.com/Leonxlnx/earshot) at
`591fa3e028032e6dce56620a20e932e35667e8d8` and
[Clipwing skills](https://github.com/Clipwing/skills) at
`edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e`. Create a venv and install Earshot editable
into it with `python -m pip install -e /path/to/earshot 'transformers<5'`. Do not run
model-fetch or upload commands for the bank-render/mix workflow. Preserve notices;
do not redistribute a user's library. Record `pip freeze` and `pip check` locally.

Configure these absolute paths, adapting them to that host:

```json
{
  "python": "/path/to/runtime/venv/bin/python",
  "ffmpeg": "/path/to/bin/ffmpeg",
  "ffprobe": "/path/to/bin/ffprobe",
  "earshot_root": "/path/to/runtime/earshot",
  "real_sfx_root": "/path/to/runtime/clipwing/skills/real-sfx",
  "revisions": {
    "earshot": "591fa3e028032e6dce56620a20e932e35667e8d8",
    "real_sfx": "edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e",
    "openverse": "https://api.openverse.org/v1/"
  }
}
```

The bridge checks tool revisions and tracked modifications before running. It
prepends the chosen FFmpeg directory only in subprocesses; place ffprobe alongside
it for upstream scripts. Doctor checks the model-free bank and mixer imports/help,
and reports optional filters separately. A green core preflight is not proof of
network access, a listening review or every optional upstream feature.

## Discover, clear, download, generate

Run from the skill folder or use the actual script path. Outputs belong to the
video project; paths with spaces should be quoted. Select meaningful assets rather
than downloading the whole index:

```sh
python scripts/sound_design.py search whoosh --output /project/search.json
# Explicit alternative if keyword search is unavailable; no keyword matching claimed:
python scripts/sound_design.py search --browse --source freesound --license cc0 --output /project/browse.json
```

Inspect a candidate's original item page and license for the intended use, then
fetch its ID from those saved results:

```sh
python scripts/sound_design.py fetch /project/browse.json --id ITEM_UUID --output /project/audio/effect.mp3 --rights-note 'Original item and license reviewed for this use; retain creator, terms and any modifications.'
python scripts/sound_design.py generate whoosh_fast/crisp --output /project/audio/whoosh.wav --duration 0.8 --apex 0.32 --seed 42
```

Each asset gets a `.provenance.json` with hash and source/recipe details. Inspect
Earshot's checks and actual sync points. Generated sounds are not recorded foley.
For an existing approved local file, provide the same provenance fields: `kind`
`local`, `sha256`, `rights_status` `reviewed`, and a meaningful `rights_note` with
its source/approval. The bridge records that decision; it cannot adjudicate rights.

## Adapt one cue sheet and mix

Create a project plan from the actual picture revision (SHA-256 of the video).
All media/provenance paths resolve relative to this JSON file. Example:

```json
{
  "video": "picture.mp4",
  "picture_sha256": "ACTUAL_SHA256",
  "mode": "voice",
  "preserve_original": false,
  "base_audio": ["audio/narration.wav"],
  "target_lufs": -16,
  "cues": [
    {"id": "contact", "scene_id": "find", "time": 1.85,
     "purpose": "Accent contact", "file": "audio/effect.mp3",
     "provenance": "audio/effect.mp3.provenance.json",
     "anchor": "peak", "role": "pop", "gain_db": -8},
    {"id": "move", "scene_id": "shape", "time": 5.85,
     "purpose": "Resolve the movement", "file": "audio/whoosh.wav",
     "provenance": "audio/whoosh.wav.provenance.json",
     "anchor": "peak", "role": "whoosh", "gain_db": -10},
    {"id": "rest", "scene_id": "end", "time": 10,
     "silence": true, "purpose": "Leave time to understand the payoff"}
  ]
}
```

`mode` is `voice` (speech-safe effects ducking), `music` (original audio dips under
effects), or `effects`. Choose clean base stems OR `preserve_original: true` to keep
the render's audio; never both. The bridge cannot recover stems from a combined
track. `target_lufs` is optional and destination-specific; -16 is an example, not a
universal target. For `anchor`, use `start` for audible onset, `peak` or `end`;
`intentional_offset` adds a deliberate lead/lag in seconds. Optional `fade_in`,
`fade_out` and `pan` carry into the mixer. More complex processing stays with the
project and needs a newly reviewed processed asset/provenance snapshot.

```sh
python scripts/sound_design.py mix /project/sound-plan.json --output /project/review.mp4
```

The bridge validates picture/assets/rights and cues, runs Real SFX's plan step,
then mixes explicit files without automatic tonal fitting or cue snapping. It
checks decode, duration, audio presence, resolved identities/times, pre-roll and
tail boundaries. Real SFX writes the SFX WAV, grouped stems and cue report; the
bridge writes `.sound-report.json` carrying provenance, tool/adapter identities,
mix measurements and listening-review status. Its `.sound-work` folder retains the
adapted sheet, isolated upstream config and commands' results for reproduction.
No edits are made to the source picture or upstream skill configuration.

Existing output, stem, report and work paths sharing the output basename are
refused before starting the mixer. Choose a fresh `.mp4` basename for each edit.
A failed external command or post-export
check can leave partial artifacts for diagnosis; do not deliver them as a pass.
Correct the issue and use a new output path. If all cues are intentionally silent,
keep the approved base/silent edit instead of forcing a sound through this adapter.
Review the actual exported audio and [finish the sound-design checks](sound-design.md).
