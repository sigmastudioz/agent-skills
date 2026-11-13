"""Prove matched invention inputs, preserved public behavior and nontrivial scale acceptance."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
EVAL=ROOT/'plugins/what-if-tony-stark-built-this/evaluation'
spec=importlib.util.spec_from_file_location('invention_trial',EVAL/'run_invention.py')
trial=importlib.util.module_from_spec(spec);spec.loader.exec_module(trial)


class InventionChecks(unittest.TestCase):
    def test_inputs_are_matched_and_only_selected_guidance_is_supplied(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'trial'
            manifest=trial.engine.prepare(output,['model-a','model-b'],trial.profile())
            self.assertEqual(len(manifest['jobs']),8)
            self.assertEqual(manifest['checker_source'],'invention_checks.py')
            self.assertEqual(len(manifest['guidance_sources']),2)
            for model in ['model-a','model-b']:
                for task in ['windows','pulse']:
                    pair=[j for j in manifest['jobs'] if j['model']==model and j['task']==task]
                    self.assertEqual(len({j['base_revision'] for j in pair}),1)
                    self.assertEqual(len({j['ticket_sha256'] for j in pair}),1)
                    for j in pair:
                        root=Path(j['workspace']);guide=root/j['guidance_file']
                        self.assertEqual(guide.exists(),j['condition']=='relevant')
                        if guide.exists():self.assertEqual(trial.engine.digest(guide.read_bytes()),manifest['guide_sha256'])
                        names={p.name for p in trial.engine.files_in(root)}
                        self.assertNotIn('invention_checks.py',names)
                        self.assertNotIn('INVENTION_PROTOCOL.md',names)
                        self.assertNotIn('invention-methods.md',names)

    def test_small_public_behavior_is_correct_before_scale_invention(self):
        for task in ['windows','pulse']:
            fixture=EVAL/'invention-fixtures'/task
            result=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests'],cwd=fixture,capture_output=True,text=True,timeout=20)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_acceptance_rejects_expansion_baselines_and_counts_distinct_methods(self):
        for task in ['windows','pulse']:
            result=subprocess.run([sys.executable,'-I',str(EVAL/'invention_checks.py'),'--task',task,'--candidate',str(EVAL/'invention-fixtures'/task)],capture_output=True,text=True,timeout=40)
            self.assertEqual(result.returncode,1,result.stderr)
            report=json.loads(result.stdout)
            self.assertEqual(report['checks'],13)
            self.assertFalse(report['passed'])
            self.assertEqual(report['passed_checks'],13-len(report['failed_checks']))
            self.assertGreater(report['passed_checks'],0)
            self.assertNotIn('test_random_small_exact_oracle',report['failed_checks'])
            self.assertNotIn('test_small_random_exact_oracle',report['failed_checks'])


if __name__=='__main__':unittest.main()
