# Optional DDD records budget checker

By Lex from SigmaStudioz. MIT, under the repository [LICENSE](../../LICENSE).

A read-only Python tool, distributed separately from the guidance-only
[DDD marketplace plugin](../../plugins/domain-driven-design/README.md). It reports
`.principal-ddd/` records that exceed the budgets in the skill's
[project records reference](../../plugins/domain-driven-design/skills/domain-driven-design/references/project-records.md#keep-records-readable).
It never edits, moves or archives a record.

```sh
python3 -B tools/records-budget/check_records.py /path/to/repo [/path/to/other-repo ...]
python3 -B tools/records-budget/check_records.py --json --ledger-lines 5000 /path/to/repo
```

| Budget | Default | Flag |
| --- | --- | --- |
| Active ledger (top-level `*.md` except `index.md`) | 3,000 lines | `--ledger-lines` |
| Any single record file | 1 MiB | `--file-bytes` |
| Whole `.principal-ddd/` tree | 25 MiB | `--tree-bytes` |
| Each `index.md` line | 200 characters | `--index-chars` |

Exit status is 0 within budget, 1 over budget and 2 when a root has no `.principal-ddd/`.
A repository that already has its own commit or CI size gate keeps it; this tool is for
repositories without one, or for a quick read-only survey. Wiring it into a hook or CI is a
separate, explicitly requested change.

## Tests

```sh
python3 -B tools/records-budget/test_check_records.py
```

The tests use temporary fixtures and confirm the checker leaves records unchanged.
