"""Validate the runner-only treatment and read-only recommendation checks without model calls."""
from pathlib import Path
import importlib.util
import json
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
EVAL=ROOT/'plugins/what-if-tony-stark-built-this/evaluation'
def load(name,file):
    spec=importlib.util.spec_from_file_location(name,EVAL/file);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
trial=load('runner_trial','run_runner_trial.py')
checker=load('runner_checks','runner_trial_checks.py')


class RunnerTrialChecks(unittest.TestCase):
    def test_assets_only_in_treatment_and_pairs_share_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'campaign';m=trial.engine.prepare(root,['test-model'],trial.profile())
            self.assertEqual(len(m['jobs']),4);self.assertEqual(m['maximum_calls'],4);self.assertEqual(m['maximum_active'],2)
            for task in ['lookup','codec']:
                pair=[j for j in m['jobs'] if j['task']==task];self.assertEqual(len({j['base_revision'] for j in pair}),1)
                self.assertEqual(len({j['ticket_sha256'] for j in pair}),1)
                for j in pair:
                    w=Path(j['workspace']);self.assertEqual((w/'.stark-tools/compare_designs.py').exists(),j['condition']=='relevant')
                    self.assertNotIn('runner_trial_checks.py',{p.name for p in trial.engine.files_in(w)})
                    for name,h in j['supplied_assets'].items():self.assertEqual(trial.engine.digest((w/name).read_bytes()),h)

    def test_legacy_model_budget_rejects_one_model_without_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'trial'
            with self.assertRaises(ValueError):trial.engine.prepare(target,['one'])
            self.assertFalse(target.exists())

    def test_snapshot_does_not_follow_worker_created_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);workspace=root/'workspace';workspace.mkdir()
            outside=root/'outside.txt';outside.write_text('not worker input')
            try:(workspace/'linked.txt').symlink_to(outside)
            except OSError:self.skipTest('symlinks unavailable')
            with self.assertRaises(ValueError):trial.engine.files_in(workspace)

    def test_correct_winner_still_requires_manual_measurement_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'task';shutil.copytree(EVAL/'runner-fixtures/lookup',target)
            (target/'evidence.json').write_text(json.dumps({'placeholder_evidence':True}))
            (target/'decision.json').write_text(json.dumps(dict(winner='granite',reason='correct result alone',evidence_path='evidence.json')))
            r=checker.check('lookup',target);self.assertTrue(r['automated_checks_passed']);self.assertTrue(r['manual_measurement_audit_required'])
            (target/'granite.py').write_text('changed source')
            self.assertFalse(checker.check('lookup',target)['automated_checks_passed'])


if __name__=='__main__':unittest.main()
