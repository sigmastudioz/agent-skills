"""Report .principal-ddd records that exceed their readability budgets. Read-only.

Usage: python3 -B check_records.py [--json] [--ledger-lines N] [--file-bytes N]
                                   [--tree-bytes N] [--index-chars N] ROOT [ROOT ...]

Each ROOT is a repository root containing .principal-ddd/. Exit status: 0 within budget,
1 over budget, 2 when a root has no .principal-ddd/ (a missing input fails rather than passes).
"""
import argparse
import json
import sys
from pathlib import Path

DEFAULTS = {
    'ledger_lines': 3000,         # active ledger: top-level *.md except index.md
    'file_bytes': 1024 * 1024,    # any single record file
    'tree_bytes': 25 * 1024 * 1024,  # whole .principal-ddd/ tree
    'index_chars': 200,           # one line per index.md entry
}
ARCHIVE_DIRS = {'archive'}


def check(root, budgets):
    records = Path(root) / '.principal-ddd'
    if not records.is_dir():
        return None
    findings, total = [], 0
    for path in sorted(p for p in records.rglob('*') if p.is_file() and not p.is_symlink()):
        size = path.stat().st_size
        total += size
        rel = path.relative_to(records).as_posix()
        if size > budgets['file_bytes']:
            findings.append({'path': rel, 'rule': 'file_bytes', 'value': size, 'budget': budgets['file_bytes']})
        if path.parent == records and path.suffix == '.md' and path.name != 'index.md':
            lines = len(path.read_text(encoding='utf-8', errors='replace').splitlines())
            if lines > budgets['ledger_lines']:
                findings.append({'path': rel, 'rule': 'ledger_lines', 'value': lines, 'budget': budgets['ledger_lines']})
    index = records / 'index.md'
    if index.is_file():
        for number, line in enumerate(index.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
            if len(line) > budgets['index_chars']:
                findings.append({'path': f'index.md:{number}', 'rule': 'index_chars', 'value': len(line), 'budget': budgets['index_chars']})
    if total > budgets['tree_bytes']:
        findings.append({'path': '.', 'rule': 'tree_bytes', 'value': total, 'budget': budgets['tree_bytes']})
    return {'root': str(root), 'tree_bytes': total, 'findings': findings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('roots', nargs='+')
    parser.add_argument('--json', action='store_true')
    for key, value in DEFAULTS.items():
        parser.add_argument('--' + key.replace('_', '-'), type=int, default=value, dest=key)
    args = parser.parse_args(argv)
    budgets = {key: getattr(args, key) for key in DEFAULTS}
    reports, status = [], 0
    for root in args.roots:
        report = check(root, budgets)
        if report is None:
            reports.append({'root': root, 'error': 'no .principal-ddd/ directory'})
            status = 2
            continue
        reports.append(report)
        if report['findings'] and status == 0:
            status = 1
    if args.json:
        print(json.dumps({'budgets': budgets, 'reports': reports}, indent=2))
    else:
        for report in reports:
            if 'error' in report:
                print(f"ERROR {report['root']}: {report['error']}")
                continue
            state = 'OVER' if report['findings'] else 'OK'
            print(f"{state} {report['root']} ({report['tree_bytes']:,} bytes)")
            for item in report['findings']:
                print(f"  {item['rule']}: {item['path']} {item['value']:,} > {item['budget']:,}")
    return status


if __name__ == '__main__':
    sys.exit(main())
