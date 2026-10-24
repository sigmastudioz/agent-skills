# Project records and migration

Use `.principal-ddd/` at the actual owning repository root for records maintained by this skill.
The name identifies Principal Driven Domain Design; it is independent of a particular agent host.
Read `index.md` first when present. Hidden placement is organization, not access control: Git,
search, publishing and build tools may include dotfolders. Keep secrets and raw private payloads out.

## One source of task truth

- An established issue, task tracker, `.planning/` system or operational ledger keeps its authority
  and current location. Link it from `.principal-ddd/index.md`; do not copy its status or replace it.
- If no owning tracker exists and substantial work needs a durable record, use
  `.principal-ddd/gap-trace.md` for findings, decisions, trace evidence and the resumable handoff.
  Small work without a continuity need can remain in the final response.
- `index.md` is a short map: owning tracker/ledger, active evidence and any legacy pinned paths.
  Keep outcomes and open work in their owning records, not duplicated in the map.
- Create only files required by current data. No empty evidence/archive/decisions directories,
  per-session journal, second status database, forced project config or new background process.
- Keep public architecture/product documentation in the project's normal documentation system.
  Keep source, tests, scripts, deployment tools and release artifacts in their established locations.
  Other skills and task systems retain their own records.

For necessary new DDD evidence, prefer existing CI/native receipts first. If a local bundle is
required by the evidence-retention policy, use the owner's existing convention or
`.principal-ddd/evidence/<purpose>/`. Identify its consumer and retention trigger in the tracker.
Reuse an existing archive convention; otherwise `.principal-ddd/archive/` can hold a required,
verified lossless archive. Folder names never waive the evidence or safe-archival rules.
Inspect effective compiler, test, import, packaging and release inputs before adding evidence.
Use narrow exclusions where needed; do not blanket-ignore all `.principal-ddd/` records and lose
shared findings or handoffs. Track durable non-sensitive records according to repository policy;
exclude only identified local/private/generated material. Do not change access or retention rules.

## Migrate existing projects only within authorized scope

A skill update defines future behavior; it does not authorize a sweep of every local repository.
When the human requests migration, inventory only the named roots and repositories with actual
DDD data. Skip empty projects, vendored copies, historical snapshots and unrelated worktrees.
Resolve each owning repository independently; a shared parent does not merge ownership.

1. Read applicable instructions and the current tracker. Record the source path, exact hash,
   Git/index state and destination. Check for another writer before changing either record.
2. Trace literal and dynamically constructed path consumers: scripts, links/anchors, native
   instructions, active tasks/monitors, packaging, archive/restore tools and external callers.
   An untracked or modified file is user work to preserve, not permission to replace its content.
3. Choose an explicit mode per record. Move a DDD-owned, unpinned record when all consumers can
   transition safely. For an active appender, mixed-version writer or uncertain consumer, keep the
   original authoritative and link it from the new index. Mark this as linked/pinned, not relocated.
4. Recheck the source identity immediately before the move; stop on a changed source or an occupied
   destination. Preserve all findings and original evidence identities. Rebase relative Markdown
   links to the same targets and retain heading anchors. Preserve evidence in place when pinned.
5. Update owned readers/writers and instructions together. If older document links must keep
   working, leave a forwarding document at the old path pointing to the canonical ledger, preserving
   incoming heading anchors too.
   A forwarding document cannot satisfy a parser/appender that expects the old body; migrate that
   consumer or keep the original pinned. Do not silently install symlinks across host boundaries.
6. Verify canonical content preservation, old/new links, actual readers, hidden-file discovery and
   effective runtime/build/release exclusions using inert local checks. Do not trigger a deployment,
   scheduled job, full application audit or marketplace publication just to test a record move.
7. Save one concise migration outcome in the owning record: old/new paths, before/after hashes,
   link transformations, retained forwarding/pinned paths, checks and rollback instructions.
   Rollback must verify the migrated record has not gained newer work before restoring the old path.
   Keep enough original content or a lossless restore recipe to recover exact pre-move bytes.

Keep the compatibility period explicit in the owning record. Retire an old forwarding path only
when its known consumers have migrated and the task authorizes that cleanup. Do not delete audit
originals or rewrite historical evidence merely to remove the old folder spelling. A migration does
not renew old test results, close existing findings or establish production success.
