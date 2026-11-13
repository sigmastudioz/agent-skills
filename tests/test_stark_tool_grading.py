"""Check explicit tool audit and the inspect-before-execute grading boundary."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/tony-evaluation/evaluation/grade_tools.py"
spec = importlib.util.spec_from_file_location("stark_tool_grading", PATH)
grading = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grading)


class GradingChecks(unittest.TestCase):
    def test_audit_distinguishes_local_reads_and_global_guidance_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            events = [
                {"type": "tool_call", "subtype": "started", "tool_call": {"readToolCall": {"args": {"path": str(root / "module.py")}}}},
                {"type": "tool_call", "subtype": "started", "tool_call": {"readToolCall": {"args": {"path": str(root / ".stark-coding-guidance.md")}}}},
                {"type": "tool_call", "subtype": "started", "tool_call": {"readToolCall": {"args": {"path": "/outside/global-skill.md"}}}},
                {"type": "tool_call", "subtype": "started", "tool_call": {"shellToolCall": {"args": {"command": "python3 -m unittest discover -s tests"}}}},
            ]
            stream = root / "stream.jsonl"
            stream.write_text("\n".join(json.dumps(e) for e in events))
            result = grading.audit_stream(stream, root)
            self.assertEqual(result["guide_reads"], 1)
            self.assertEqual(result["outside_read_candidates"], ["/outside/global-skill.md"])
            self.assertEqual(result["tool_starts"]["shellToolCall"], 1)

    def test_grading_requires_coordinator_inspection_before_accessing_candidate(self):
        with self.assertRaises(ValueError):
            grading.grade(Path("/nonexistent-trial"), "unknown", reviewed=False)

    def test_failing_reproducer_preserves_nonzero_exit_and_stderr(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stream = root / "stream.jsonl"
            stream.write_text(json.dumps({"type": "tool_call", "subtype": "completed", "tool_call": {
                "shellToolCall": {"args": {"command": "python3 -m unittest"}, "result": {
                    "failure": {"exitCode": 1, "stdout": "", "stderr": "FAILED (failures=1)"},
                    "isBackground": False}}}}))
            result = grading.audit_stream(stream, root)["shell_results"][0]
            self.assertEqual(result["exit_code"], 1)
            self.assertEqual(result["stderr"], "FAILED (failures=1)")
            self.assertFalse(result["is_background"])


if __name__ == "__main__":
    unittest.main()
