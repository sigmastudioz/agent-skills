"""Regressions for the read-only records budget checker, using temporary fixtures only."""
import contextlib
import io
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('check_records', Path(__file__).with_name('check_records.py'))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class RecordsBudgetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='ddd-records-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.records = self.root / '.principal-ddd'
        self.records.mkdir()
        (self.records / 'index.md').write_text('# Index\n\n- [Ledger](gap-trace.md) - open work\n')
        (self.records / 'gap-trace.md').write_text('| ID | Status |\n' * 10)

    def run_checker(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            status = checker.main([*args, str(self.root)])
        return status, out.getvalue()

    def test_within_budget_passes(self):
        self.assertEqual(self.run_checker()[0], 0)

    def test_long_active_ledger_fails(self):
        status, out = self.run_checker('--ledger-lines', '5')
        self.assertEqual(status, 1)
        self.assertIn('ledger_lines: gap-trace.md', out)

    def test_archived_ledger_is_not_an_active_ledger(self):
        archive = self.records / 'archive'
        archive.mkdir()
        (archive / 'gap-trace-2026-10.md').write_text('line\n' * 50)
        self.assertEqual(self.run_checker('--ledger-lines', '20')[0], 0)

    def test_large_file_and_tree_fail(self):
        evidence = self.records / 'evidence'
        evidence.mkdir()
        (evidence / 'dump.json').write_bytes(b'x' * 4096)
        status, out = self.run_checker('--file-bytes', '1024', '--tree-bytes', '2048')
        self.assertEqual(status, 1)
        self.assertIn('file_bytes: evidence/dump.json', out)
        self.assertIn('tree_bytes', out)

    def test_paragraph_index_entry_fails(self):
        with (self.records / 'index.md').open('a') as index:
            index.write('- ' + 'word ' * 80 + '\n')
        status, out = self.run_checker()
        self.assertEqual(status, 1)
        self.assertIn('index_chars: index.md:4', out)

    def test_missing_records_fails_instead_of_passing(self):
        empty = self.root / 'other'
        empty.mkdir()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(checker.main([str(empty)]), 2)

    def test_checker_does_not_modify_records(self):
        before = {p: p.read_bytes() for p in self.records.rglob('*') if p.is_file()}
        self.run_checker('--ledger-lines', '1')
        after = {p: p.read_bytes() for p in self.records.rglob('*') if p.is_file()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
