"""Check permissions, fixture containment and nontrivial held-out coding checks without model calls."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVALUATION = ROOT / "plugins/what-if-tony-stark-built-this/evaluation"
spec = importlib.util.spec_from_file_location("stark_tools", EVALUATION / "run_tools.py")
tools_trial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools_trial)


class ToolTrialChecks(unittest.TestCase):
    def test_tool_command_enables_execution_without_permission_bypass(self):
        command = tools_trial.cursor_command({"model": "test-model", "workspace": "/tmp/owned-fixture"})
        self.assertIn("--auto-review", command)
        self.assertEqual(command[command.index("--sandbox") + 1], "enabled")
        self.assertNotIn("--mode", command)
        self.assertNotIn("--force", command)
        self.assertNotIn("--yolo", command)

    def test_snapshot_excludes_git_and_cache_but_keeps_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("package/module.py", ".git/config", "package/__pycache__/module.pyc", "README.md"):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture")
            self.assertEqual({str(p.relative_to(root)) for p in tools_trial.files_in(root)},
                             {"package/module.py", "README.md"})

    def test_original_public_tests_pass_and_hidden_checks_find_contract_failures(self):
        for task, count in (("relay", 15), ("importer", 18)):
            with self.subTest(task=task):
                fixture = EVALUATION / "tool-fixtures" / task
                public = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"],
                                        cwd=fixture, capture_output=True, text=True, timeout=30)
                self.assertEqual(public.returncode, 0, public.stderr)
                hidden = subprocess.run([sys.executable, "-I", str(EVALUATION / "tool_checks.py"),
                                         "--task", task, "--candidate", str(fixture)],
                                        capture_output=True, text=True, timeout=60)
                self.assertEqual(hidden.returncode, 0, hidden.stderr)
                report = json.loads(hidden.stdout)
                self.assertEqual(report["checks"], count)
                self.assertFalse(report["passed"])
                self.assertGreater(report["passed_checks"], 0)
                self.assertLess(report["passed_checks"], count)
                self.assertEqual(report["passed_checks"], count - len(report["failed_checks"]))

    def test_worker_fixture_has_no_hidden_evaluator(self):
        for task in ("relay", "importer"):
            files = {p.name for p in tools_trial.files_in(EVALUATION / "tool-fixtures" / task)}
            self.assertNotIn("tool_checks.py", files)
            self.assertNotIn("rubric.json", files)
            self.assertNotIn("RESULTS.md", files)


if __name__ == "__main__":
    unittest.main()
