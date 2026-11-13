"""Behavioral checks for pilot isolation, output parsing and the hidden code verifier."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVALUATION = ROOT / "plugins/what-if-tony-stark-built-this/evaluation"


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, EVALUATION / file)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


pilot = module("stark_pilot", "run_pilot.py")
checks = module("stark_checks", "check_code.py")


class PilotChecks(unittest.TestCase):
    def test_matched_tasks_and_no_criteria_leak(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "pilot"
            manifest = pilot.prepare(output, ["grok-test", "fable-test"])
            payload, _ = pilot.runtime_payload(EVALUATION.parent / "skills/what-if-tony-stark-built-this")
            self.assertEqual(len(manifest["jobs"]), 16)
            for model in ("grok-test", "fable-test"):
                for task in ("inventory", "sorting", "offline-design", "replan"):
                    pair = [j for j in manifest["jobs"] if j["model"] == model and j["task"] == task]
                    self.assertEqual({j["condition"] for j in pair}, {"with", "without"})
                    self.assertEqual(len({j["task_sha256"] for j in pair}), 1)
                    texts = {j["condition"]: (output / "control" / (j["id"] + ".prompt.txt")).read_text() for j in pair}
                    self.assertIn(payload, texts["with"])
                    self.assertNotIn(payload, texts["without"])
                    for text in texts.values():
                        self.assertNotIn("evaluation requests and scoring criteria", text)
                        self.assertNotIn("critical_failures", text)
                        self.assertNotIn("Hidden local behavioral checks", text)
            with self.assertRaises(ValueError):
                pilot.prepare(output, ["grok-test", "fable-test"])

    def test_stream_prefers_final_and_detects_tools(self):
        raw = "\n".join(json.dumps(e) for e in [
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "partial"}]}},
            {"type": "tool_call", "subtype": "started", "tool_call": {"readToolCall": {}}},
            {"type": "result", "result": '{"analysis":"final"}', "usage": {"output_tokens": 4}}])
        result = pilot.parse_stream(raw)
        self.assertEqual(result["response"], '{"analysis":"final"}')
        self.assertEqual(len(result["tool_events"]), 1)
        self.assertEqual(result["provider_usage"], {"output_tokens": 4})

    def test_json_artifact_survives_markers_and_fences(self):
        text = 'MILESTONE inputs-read\n```json\n{"code":"def f(): return {1: 2}","rationale":"ok"}\n```\nDONE'
        self.assertEqual(pilot.response_object(text)["code"], "def f(): return {1: 2}")
        self.assertIsNone(pilot.response_object("No artifact supplied"))

    def test_verifier_catches_original_sort_and_accepts_correct_function(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.py"
            candidate.write_text('def sort_rows(rows, descending=False):\n return sorted(rows, key=lambda r: (r.get("score") is None, r.get("score") or 0), reverse=not descending)\n')
            bad = checks.evaluate("sorting", candidate)
            self.assertFalse(bad["passed"])
            self.assertGreater(bad["failure_count"], 0)
            candidate.write_text('def sort_rows(rows, descending=False):\n present = [r for r in rows if r.get("score") is not None]\n missing = [r for r in rows if r.get("score") is None]\n return sorted(present, key=lambda r: r["score"], reverse=descending) + missing\n')
            good = checks.evaluate("sorting", candidate)
            self.assertTrue(good["passed"], good["summary"])
            self.assertEqual(good["checks"], 6)

    def test_off_task_execution_is_rejected_before_loading(self):
        for source in ('import os\n', 'open("secret")', 'eval("1")', 'x.__class__.__subclasses__()'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                checks.inspect_source(source)


if __name__ == "__main__":
    unittest.main()
