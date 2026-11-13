"""Exercise the installable runner without the separate maintainer evaluation suite."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/what-if-tony-stark-built-this'


class InstalledRunner(unittest.TestCase):
    def test_complete_plugin_runs_example_without_collection_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / 'plugin'
            shutil.copytree(PLUGIN, installed)
            self.assertFalse((installed / 'evaluation').exists())
            skill = installed / 'skills/what-if-tony-stark-built-this'
            report = Path(directory) / 'report.json'
            result = subprocess.run(
                [sys.executable, '-I', str(skill / 'scripts/compare_designs.py'),
                 str(skill / 'assets/comparison-example/experiment.json'),
                 '--output', str(report)],
                cwd=directory, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(report.read_text())
            self.assertEqual(data['status'], 'completed')
            self.assertEqual(data['decision']['outcome'], 'candidate_selected')
            self.assertEqual(data['decision']['winner_id'], 'candidate')


if __name__ == '__main__':
    unittest.main()
