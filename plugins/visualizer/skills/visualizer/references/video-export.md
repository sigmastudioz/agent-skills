# Export and public delivery

## Encode and deliver
Reuse the project's renderer. For new code, own storyboard/model, layout, assets, renderer and
encoder separately at the smallest useful scope. Stream frames and bound buffers; use argument
arrays for subprocesses. Detect render/encoder failures and incomplete frames. Preserve the prior
output until a staged export passes validation; avoid overwriting source or evidence files.
For R3F scenes, follow the [manual-frame export contract](react-three-fiber.md#one-clock-for-interaction-and-film);
React reconciliation, asset readiness and compositing must finish before capture.
Render at explicit frame times. A 60fps container with duplicated 30fps poses does not establish
smoother source motion; deliberate cel holds are valid when chosen and documented.
Use a compatible codec/container and color pipeline for the destination. Keep high-quality master
and delivery derivatives distinct. Copy encoded audio when appropriate to avoid unnecessary loss.

Decode the complete export, then verify dimensions, duration, FPS, frame count, audio, captions,
orientation, safe areas and representative transitions. Inspect rich textures after compression.
Retain reproduction commands, dependency versions, asset licenses and editable scene/timeline data.

## Inline playback and public delivery
Check the actual destination renderer: a Markdown image linking to an MP4 is a poster link.
On GitHub, upload an authorized MP4 through the Markdown attachment control, use its returned
stable attachment URL, and preview the resulting player before committing. Verify current file
limits and codecs; use a smaller delivery derivative when needed, preserving the full download.
Do not store expiring signed CDN URLs in source. Verify the public page without relying on the
publisher's session: player controls, media readiness, duration and actual time advancement.
Keep captions, source downloads and a fallback link. Record upload versus commit versus live
verification separately; stop/recover when another user controls the browser. Social launch drafts
remain unsent until authorized. A public repository is not a marketplace approval.
