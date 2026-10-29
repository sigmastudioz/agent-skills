# Optional sound tools: verified identities and limits

Checked 2026-10-29 against the primary sources below. The bundled
[sound bridge](sound-runtime.md) now connects Openverse audio discovery/download,
Earshot bank rendering and Real SFX mixing. A local 12-second integration test used
a licensed public asset, an original generated whoosh and narration. Runtime setup
is per host; these scoped technical checks do not establish listening quality or
that optional models/filters are installed everywhere.

Keep the project's renderer, cue sheet and mixer authoritative. Discover available
tools and inspect their installed version/help before use; resolve paths on that
host. No automatic global installs, MCP registration, model downloads, uploads or
paid calls follow from selecting this skill. Use a project environment for an
authorized installation. The workflow still works with existing assets and FFmpeg
when these optional tools are absent. Apply [the sound-design pass](sound-design.md).

On the tested host, Openverse keyword requests timed out while license/source
filtering worked. Use the explicit `search --browse` route when useful, inspect its
results and report that limitation; do not silently call browsing a keyword match.
The bridge disables optional model downloads and automatic tonal fitting. Its doctor
reports missing `drawtext`/`rubberband`; those upstream review/pitch paths need an
appropriate FFmpeg build even when the tested core mix path works.

## Openverse: find existing audio

- Official [API reference](https://api.openverse.org/v1/) documents audio search,
  item detail, source stats and fields including the original page, file URL,
  creator, license, license version/URL and attribution. Search results include
  audio tracks generally; an index total is not a count of usable sound effects.
- Anonymous access is supported with rate/pagination limits; registered access
  uses OAuth. Recheck current limits rather than copying “no key needed” as an
  unlimited-access promise. Use narrow queries, limited pages, timeouts and bounded
  retries; respect 429/retry guidance. Do not bulk scrape the index or create an
  account/token as a side effect of a video task.
- A documented request shape is `GET https://api.openverse.org/v1/audio/` with
  `q=whoosh`, `page_size=5` and an appropriate `license` or `license_type` filter.
  Check the HTTP response and JSON fields; search metadata is not an audio file.
  Inspect the original item page and download a selected file from its actual URL,
  then probe it and retain provenance. Do not send private media in search queries.
- [Openverse terms](https://docs.openverse.org/terms_of_service) require independently
  checking rights; Openverse does not verify every item's licensing. Filters are
  discovery aids, not clearance. There is no blanket “royalty-free/no attribution”
  claim for all results. When building an API-backed product, also follow the
  terms' Openverse attribution/non-endorsement requirement.

## Real SFX: place recordings against picture

Identity: Clipwing's **`real-sfx` skill**, not a general executable named RealSFX.
Verified [upstream README](https://github.com/Clipwing/skills/blob/edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e/skills/real-sfx/README.md),
[skill](https://github.com/Clipwing/skills/blob/edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e/skills/real-sfx/SKILL.md)
and [mixer source](https://github.com/Clipwing/skills/blob/edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e/skills/real-sfx/scripts/mix.py)
at `edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e`.

- Uses a supplied recording library, project cues/HyperFrames timing or inspected
  picture events; produces a new MP4, separate SFX WAV and cue/review reports. It is
  not a sound generator or a guaranteed detector of every meaningful event. Its
  optional uisfx UI pack is synthesized, a stated exception to the recordings route.
- Requires Python 3.9+, FFmpeg/ffprobe and relevant filters (`drawtext`, `rubberband`
  for the paths using them). Check the actual FFmpeg build; do not replace a system
  installation based solely on a package name. Optional UI-package/model setup has
  additional dependencies/downloads; a skill's presence does not provision them.
- Upstream README declares scripts MIT and uisfx sounds CC0; third-party recordings
  retain their own terms. Link to this tool rather than silently vendoring it or
  bundling the user's library. Recheck the notices for an installation/distribution.
- If available, run its read-only preflight `python scripts/setup.py check` from
  the actual tool root. Review its cue schema before adapting project events. Use
  `python scripts/mix.py PROJECT_CUES.json --out NEW_OUTPUT.mp4 --plan` to inspect
  resolved choices before rendering; retain manual cue edits across imports.
- In its mixer, `--voice-safe` ducks effects beneath speech; `--duck` dips the
  original audio beneath effects for a music-led edit. They are not interchangeable.
  Verify the actual mix rather than assuming a flag protects narration. Replacing
  baked effects needs suitable stems/project sources; do not promise clean recovery
  from an arbitrary combined track. Its measurements still require listening review.
  The bridge supplies explicit audio files, including separately generated Earshot
  WAVs, to this mixer. Upstream labels direct files as “library”; our provenance
  records distinguish downloaded, local and generated assets. Do not relabel
  generated effects as recorded foley.

## Earshot: synthesize effects and inspect audio evidence

Identity: **Leonxlnx/earshot**, not similarly named spatial-audio or speech projects.
Verified [README](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/README.md),
[package metadata](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/pyproject.toml),
[CLI](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/earshot/cli.py)
and [limits](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/docs/LIMITS.md)
at `591fa3e028032e6dce56620a20e932e35667e8d8`, version 0.4.0; the supplied video shows 0.3.

- Provides CLI/Python/MCP interfaces. Bank rendering (`sfx`) and coordinated kits
  (`kit`) use local DSP without model inference; measurement is also model-free.
  Model-assisted matching/tagging is a different route: first use can download
  substantial weights. The package itself includes substantial dependencies.
- Code is [MIT](https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/LICENSE);
  model licenses and any input-recording rights are separate. No generated output
  or “realness” score proves provenance or clears third-party material.
- Check the installed help and bank IDs first. Documented examples, to adapt in
  the video project's output folder after setup:

```sh
earshot sfx list --kind whoosh
earshot sfx render whoosh_fast/crisp -o audio/whoosh.wav --dur 0.8 --apex 0.32
earshot sfx check audio/whoosh.wav
earshot kit init --preset calm -o audio/kit.json
earshot kit render audio/kit.json --out audio/kit
```

  Keep recipes, seed/version and generated WAVs/kit lock with the project. Inspect
  measured onset/peak/end and adapt them to its cue sheet; these commands do not
  insert audio into our renderer or establish correct final muxing. Bank generation
  is synthesis, not proof of realistic recorded foley or arbitrary text-to-audio.
- `EARSHOT_OFFLINE=1` prevents model fetches; missing models must be reported, not
  silently downloaded. Do not invoke upload/LLM-critique routes without authorization.
  Metering, tags and launch-film profiles are evidence with domain limits, not a
  judgment of taste, emotion, speech content or license validity. Review the encoded
  film and do not add unwanted sounds merely to satisfy its critique scores.
