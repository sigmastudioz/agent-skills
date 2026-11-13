# Restartable CSV Import

Python standard library only. Public checks: `python3 -m unittest discover -s tests -v`.

## Ticket

Finish the importer so it can resume safely after an interrupted batch and report the durable
result accurately. Users have seen missing records after retrying and misleading completion output.
Preserve the current public APIs and CLI, tenant isolation and existing database rows. Add focused
regression tests without changing existing expectations. No services, new dependencies or deployment.

## Contracts

- CSV files are UTF-8 with columns `record_id,value`. A record's value can contain quoted commas,
  Unicode or embedded newlines. `next_row` is the next logical data-row index, not a byte or line offset.
- `Store(path)` persists runs and records. Identity is `(tenant, run_id)` for a run and
  `(tenant, record_id)` for a record. IDs may be reused by different tenants without interference.
  `start(tenant, run_id, source_key)` binds the run to one opaque source identity. A conflicting
  binding raises ValueError without changing either run or records. Existing data is never reset.
- `Runner(store).run(tenant, run_id, source, batch_size=2, after_row=None)` imports from a Path and
  returns the durable run dict. Source identity is content-based, so a moved identical source can
  resume but changed bytes must not reuse a partial run. Batch size must be positive.
- Record insertion and progress for a batch are atomic and durable together. An interrupted current
  batch leaves neither partial rows nor advanced progress; earlier completed batches remain.
  Reopening Store and rerunning resumes from the committed logical row without skipping or
  duplicating effects. The optional callback receives a row after its write inside processing; it
  may raise to simulate interruption. Its exception propagates; the run is not complete.
- A repeated record ID with the same value is an idempotent no-op. A different value raises
  ValueError and must not overwrite the original. Replaying a complete run on unchanged content
  returns the same result. The processed count is the number of committed logical input rows.
- Only a run whose input has been fully committed can be complete. `render(run)` and the CLI are
  supported consumers of durable state, including incomplete runs and tenant-reused run IDs.
  `get_run()` returns a dict or None; `records(tenant)` returns tenant-local record dictionaries.

```sh
python3 -m csv_import.cli --db /tmp/import.sqlite run acme first input.csv --batch-size 2
python3 -m csv_import.cli --db /tmp/import.sqlite show acme first
```
