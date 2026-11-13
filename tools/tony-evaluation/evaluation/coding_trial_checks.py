#!/usr/bin/env python3
"""Frozen independent coding checks. A pass still requires a manual measurement/tool audit."""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import io
import json
import math
import random
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, *args, **kwargs):
    try:
        return ('return', function(*args, **kwargs))
    except Exception as error:
        return ('error', type(error).__name__, str(error))


def tracks(count, seed):
    rng = random.Random(seed)
    return [dict(id='track:' + str(i), head_rms_dbfs=rng.uniform(-45, -2),
                 tail_rms_dbfs=rng.uniform(-45, -2)) for i in range(count)]


class SequenceChecks(unittest.TestCase):
    def setUp(self):
        self.before = load('sequence_before', self.root / 'reference/original.py')
        self.after = load('sequence_after', self.root / 'music/sequence.py')

    def equivalent(self, rows, **constraints):
        original = copy.deepcopy(rows)
        expected = outcome(self.before.propose_sequence, copy.deepcopy(rows), **copy.deepcopy(constraints))
        actual = outcome(self.after.propose_sequence, rows, **constraints)
        self.assertEqual(actual, expected)
        self.assertEqual(rows, original)
        return actual

    def test_random_proposals_blocks_and_pins(self):
        for seed in range(32):
            rows = tracks(14 + seed, seed)
            if seed % 3 == 0:
                for row in rows[::4]:
                    row.pop('head_rms_dbfs')
            groups = [[rows[3]['id'], rows[4]['id']], [rows[8]['id'], rows[9]['id']]]
            self.equivalent(rows, opener=rows[0]['id'], closer=rows[-1]['id'], keep_together=groups)
            self.equivalent(rows)

    def test_rounded_ties_nonfinite_and_immutability(self):
        for value in (None, math.inf, -math.inf, math.nan):
            rows = [dict(id='zero', tail_rms_dbfs=-10),
                    dict(id='earlier', head_rms_dbfs=-10.0049, tail_rms_dbfs=value),
                    dict(id='closer', head_rms_dbfs=-10.0001, tail_rms_dbfs=-5),
                    dict(id='unknown', head_rms_dbfs=value)]
            self.equivalent(rows)
        self.equivalent([{'id': 'solo'}], opener='solo', closer='solo')

    def test_invalid_constraint_precedence(self):
        rows = tracks(8, 771)
        cases = [dict(opener='absent'), dict(opener='track:0', closer='track:0'),
                 dict(keep_together='bad'), dict(keep_together=[[]]),
                 dict(keep_together=[['track:1', 'track:1']]),
                 dict(keep_together=[['track:1', 'absent']]),
                 dict(opener='track:2', keep_together=[['track:1', 'track:2']]),
                 dict(opener='track:0', closer='track:7', keep_together=[['track:0', 'track:7']])]
        for constraints in cases:
            self.equivalent(rows, **constraints)
        for malformed in ([], [{'id': ''}], [{'id': 'same'}, {'id': 'same'}]):
            self.equivalent(malformed)
        orders = [None, [], ['track:0'] * 8, [r['id'] for r in reversed(rows)]]
        constraints = [{}, {'unsupported': True}, {'opener': 'absent'},
                       {'keep_together': [['track:1', 'track:2']]},
                       {'opener': 'track:0', 'closer': 'track:7'}]
        for order in orders + [[r['id'] for r in rows]]:
            for constraint in constraints:
                self.assertEqual(outcome(self.after.validate_album_order, order, rows, constraint),
                                 outcome(self.before.validate_album_order, order, rows, constraint))

    def test_proposal_scale_and_editorial_validation(self):
        rows = tracks(1000, 28917)
        expected = self.before.propose_sequence(rows)
        self.assertEqual(self.after.propose_sequence(rows), expected)
        timings = {'before': [], 'after': []}
        for index in range(3):
            for name in (('before', 'after') if index % 2 == 0 else ('after', 'before')):
                started = time.perf_counter()
                result = getattr(self, name).propose_sequence(rows)
                timings[name].append(time.perf_counter() - started)
                self.assertEqual(result, expected)
        ratio = statistics.median(timings['before']) / statistics.median(timings['after'])
        self.metrics.update(proposal_seconds=timings, proposal_speedup=ratio)
        self.assertGreaterEqual(ratio, 3.0)
        with patch.object(self.after, 'propose_sequence', side_effect=AssertionError('unused proposal generated')):
            self.assertIsNone(self.after.validate_album_order(expected['technical_flow_proposal'], rows, {}))


def tree(root):
    registry = dict(name='skills', displayName='Skills', description='Local test',
                    publisher={'name': 'Owner', 'email': 'owner@example.test'}, plugins=[])
    directory = root / 'plugins/first'
    directory.mkdir(parents=True)
    manifest = dict(name='first', version='1.0.0', description='First', author={'name': 'Owner'})
    for relative in ('plugin.json', '.claude-plugin/plugin.json', '.cursor-plugin/plugin.json', '.codex-plugin/plugin.json'):
        target = directory / relative
        target.parent.mkdir(exist_ok=True)
        target.write_text(json.dumps(manifest))
    registry['plugins'].append(dict(name='first', path='./plugins/first'))
    (root / 'catalog.json').write_text(json.dumps(registry))
    return directory


class CatalogChecks(unittest.TestCase):
    def setUp(self):
        self.before = load('catalog_before', self.root / 'reference/original.py')
        self.after = load('catalog_after', self.root / 'tools/build_catalogs.py')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.plugin = tree(self.data)

    def test_tree_equivalence_ignored_and_unicode(self):
        for index in range(90):
            target = self.plugin / ('level' + str(index % 7)) / ('asset-' + str(index) + '-é.bin')
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(bytes([index]) * (index + 5))
        ignored = self.plugin / 'scripts/.venv/deep/deeper'
        ignored.mkdir(parents=True)
        (ignored / 'python').symlink_to('/definitely/not/a/distribution/file')
        (self.plugin / '.DS_Store').write_bytes(b'ignored')
        self.assertEqual(self.after.render(self.data), self.before.render(self.data))

    def test_content_changes_not_metadata_cache(self):
        target = self.plugin / 'payload.bin'
        target.write_bytes(b'a' * 1000)
        first = self.after.render(self.data)
        target.write_bytes(b'b' * 1000)
        second = self.after.render(self.data)
        self.assertNotEqual(first, second)
        self.assertEqual(second, self.before.render(self.data))

    def test_symlinks_rejected_files_directories_and_dangling(self):
        for name, target in [('file', self.plugin / 'plugin.json'), ('directory', self.plugin),
                             ('dangling', self.data / 'absent')]:
            link = self.plugin / name
            link.symlink_to(target)
            try:
                self.assertEqual(outcome(self.after.render, self.data), outcome(self.before.render, self.data))
                self.assertEqual(outcome(self.after.render, self.data)[0], 'error')
            finally:
                link.unlink()

    def test_stale_check_and_failure_before_write(self):
        self.after.build(self.data)
        paths = list(self.before.render(self.data))
        original = {p: (self.data / p).read_bytes() for p in paths}
        target = self.plugin / 'plugin.json'
        data = json.loads(target.read_text())
        data['description'] = 'Changed'
        target.write_text(json.dumps(data))
        self.assertEqual(outcome(self.after.build, self.data, True), outcome(self.before.build, self.data, True))
        self.assertEqual(original, {p: (self.data / p).read_bytes() for p in paths})
        data['name'] = 'wrong'
        target.write_text(json.dumps(data))
        self.assertEqual(outcome(self.after.build, self.data), outcome(self.before.build, self.data))
        self.assertEqual(original, {p: (self.data / p).read_bytes() for p in paths})

    def test_large_asset_bounded_allocation(self):
        target = self.plugin / 'large.bin'
        with target.open('wb') as handle:
            for _ in range(48):
                handle.write(b'x' * 1048576)
        expected = self.before.render(self.data)
        tracemalloc.start()
        try:
            imported = load('catalog_measured_import', self.root / 'tools/build_catalogs.py')
            actual = imported.render(self.data)
            peak = tracemalloc.get_traced_memory()[1]
        finally:
            tracemalloc.stop()
        self.metrics['large_asset_python_peak_bytes'] = peak
        self.assertEqual(actual, expected)
        self.assertLess(peak, 8 * 1048576)


def check(task, candidate):
    candidate = Path(candidate).resolve()
    fixture = HERE / 'coding-fixtures' / task
    readonly = ['README.md', 'SOURCE.json', 'reference/original.py']
    readonly.extend(str(p.relative_to(fixture)) for p in (fixture / 'tests').rglob('*.py'))
    changed = [name for name in readonly if not (candidate / name).is_file()
               or (candidate / name).is_symlink()
               or (candidate / name).read_bytes() != (fixture / name).read_bytes()]
    errors = []
    try:
        decision = json.loads((candidate / 'decision.json').read_text())
        if decision.get('implemented') is not True or not decision.get('reason'):
            errors.append('No completed implementation decision')
        if not isinstance(decision.get('limitations'), list):
            errors.append('Missing limitations list')
        report = (candidate / decision['evidence_path']).resolve()
        if candidate not in report.parents or not isinstance(json.loads(report.read_text()), (dict, list)):
            errors.append('No contained JSON evidence')
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(str(error))
    cls = CatalogChecks if task == 'catalog' else SequenceChecks
    cls.root, cls.metrics = candidate, {}
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    public = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                            cwd=candidate, capture_output=True, text=True, timeout=120)
    return dict(task=task, input_errors=changed, decision_errors=errors,
                coding_checks_passed=result.wasSuccessful(), coding_checks_run=result.testsRun,
                coding_check_output=stream.getvalue(), metrics=cls.metrics,
                public_checks_passed=public.returncode == 0, public_output=public.stdout + public.stderr,
                automated_checks_passed=not changed and not errors and result.wasSuccessful() and public.returncode == 0,
                manual_measurement_audit_required=True,
                note='Coding acceptance alone cannot establish valid comparison setup or executed measurements.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task', choices=('catalog', 'sequencing'), required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = check(args.task, args.candidate)
    text = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text)
    return int(not report['automated_checks_passed'])


if __name__ == '__main__':
    raise SystemExit(main())
