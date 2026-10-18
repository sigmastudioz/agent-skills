# Audio, text and synchronized evidence

Determine which audio track matters. Preserve language, channel arrangement, offset and source ID.
No-audio, audible silence, music-only, unintelligible speech and unavailable listening are different
states. Never fill a silent passage with plausible narration from surrounding images.

Prefer an available authorized local/native transcript path. Choose model/runtime from actual
language, duration, hardware, quality needs and resource budget; don't hard-code one model for
all hosts. Check installed CLI help/version before using model-specific options.

With an already installed official Whisper CLI, an example that preserves text and time evidence is:

```sh
whisper /path/to/audio-or-video.mp4 --model base --task transcribe \
  --output_format all --output_dir /path/to/transcript
```

Use one output_format value; repeating --output_format txt and --output_format srt does not request
both. Use --language only when known, and label English translation separately from transcription.
The example may download weights if absent: check caches/requirements and authorization first.
Long clips can be processed in bounded chunks with recorded offsets, overlap and deduplication.
Retain absolute and chunk-local times; check boundary words instead of blindly concatenating text.

Whisper output is a hypothesis, especially for silence, music, accents, names and multiple speakers.
Review suspicious repetition, implausible text, uncertain numbers and passages near long silences.
Use available VAD/no-speech diagnostics and listening rather than treating scores as calibrated
confidence. Word timestamps are estimates, not forensic synchronization. Record the model/version,
language/task, chunking and any manual corrections. Do not infer speaker identity from a voice.

If audio can be heard, assess requested delivery, music, impacts, ambience and picture synchronization.
If only transcript data is available, discuss wording with that limitation and leave sound-design
claims unverified. Loudness/true-peak measurements are not substitutes for listening.
Keep authorized originals when deriving mono/low-rate analysis audio; don't call a downmix identical
to the original multichannel mix. Retain conversion parameters and offsets.

Correlate separate evidence lanes:
| Lane | Record |
| --- | --- |
| Visual event | Actual frame/range, shot/action, inspected artifact |
| Visible text | Location, transcription/OCR, uncertainty, timestamp |
| Speech | Transcript segment, language, source track, corrections |
| Sound | Heard event/range or measurement, method and listening limits |
| Claim | Observation versus inference versus quoted presenter assertion |

Preserve contradictions: a title card may promise a feature the demonstration never shows.
Quote only what was actually observed/transcribed; don't turn paraphrases into verbatim speech.
Time citations should identify the source when several clips are compared. Keep an evidence table
small enough to review and link to detailed artifacts when necessary.

Original workflow provenance: local frame extraction plus local Whisper, now generalized across
hosts. This package does not redistribute the older auto-install wrapper or vendor model weights.
Official reference: [Whisper CLI implementation](https://github.com/openai/whisper/blob/main/whisper/transcribe.py).
