# Principal Driven Domain Design records

- [Owning gap ledger and handoff](gap-trace.md).
- [Legacy forwarding path](../docs/architecture/gap-trace.md).

## Migration and recovery

Moved the DDD-owned record on 2026-10-24; findings and evidence identities are preserved.
Only relative Markdown targets were rebased. Existing evidence bundles remain with their owner.
See [the migration receipt](migration.json) for hashes and the reversible link edits.
To restore, first require the canonical SHA-256 to equal `after_sha256` and the legacy file to
equal `forward_sha256`. Reverse `link_edits` in reverse order at `after_start`, replacing each
exact `new` substring with `old`; require the result hash to equal `before_sha256`. Restore
the original path and mode only after those checks, then remove the unchanged migrated copy.
If either file has newer work, reconcile it rather than overwriting it. Keep the forwarding
path until its known readers have transitioned and cleanup is authorized.
