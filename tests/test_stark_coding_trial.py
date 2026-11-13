"""Verify isolated, timed coding trials without dispatching any model."""
from pathlib import Path
import hashlib
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / 'tools/tony-evaluation/evaluation'
spec = importlib.util.spec_from_file_location('coding_trial', EVAL / 'run_coding_trial.py')
trial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trial)


class CodingTrialTests(unittest.TestCase):
    def test_fresh_code_no_prepared_experiment_and_timed_setup(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = trial.engine.prepare(Path(directory) / 'campaign', ['test-model'], trial.profile())
            self.assertEqual(manifest['maximum_calls'], 4)
            self.assertEqual(manifest['maximum_active'], 1)
            self.assertEqual(manifest['timeout_seconds'], 1800)
            for task in ('catalog', 'sequencing'):
                pair = [j for j in manifest['jobs'] if j['task'] == task]
                self.assertEqual(len({j['base_revision'] for j in pair}), 1)
                self.assertEqual(len({j['ticket_sha256'] for j in pair}), 1)
                for job in pair:
                    workspace = Path(job['workspace'])
                    self.assertFalse((workspace / 'experiment.json').exists())
                    self.assertFalse((workspace / 'decision.json').exists())
                    self.assertFalse((workspace / 'coding_trial_checks.py').exists())
                    self.assertEqual((workspace / '.stark-skill/scripts/compare_designs.py').is_file(), job['condition'] == 'relevant')
                    self.assertEqual((workspace / '.stark-skill/SKILL.md').is_file(), job['condition'] == 'relevant')
                    for relative, digest in job['supplied_assets'].items():
                        self.assertEqual(hashlib.sha256((workspace / relative).read_bytes()).hexdigest(), digest)

    def test_reference_and_active_source_match_frozen_origin(self):
        published = {entry['name'] for entry in json.loads((ROOT / 'catalog.json').read_text())['plugins']}
        for task, active in [('catalog', 'tools/build_catalogs.py'), ('sequencing', 'music/sequence.py')]:
            root = EVAL / 'coding-fixtures' / task
            origin = json.loads((root / 'SOURCE.json').read_text())
            raw = (root / active).read_bytes()
            self.assertEqual(raw, (root / 'reference/original.py').read_bytes())
            self.assertEqual(hashlib.sha256(raw).hexdigest(), origin['sha256'])
            source_path = Path(origin['source_path'])
            if source_path.parts[0] == 'plugins' and source_path.parts[1] not in published:
                # The frozen fixture ships independently; its source plugin can remain private.
                self.assertFalse((ROOT / 'plugins' / source_path.parts[1]).exists())
            else:
                self.assertEqual(raw, (ROOT / source_path).read_bytes())


if __name__ == '__main__':
    unittest.main()
