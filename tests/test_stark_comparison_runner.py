#!/usr/bin/env python3
"""Tests for the skill-owned Manifest v1 comparison runner."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (
    ROOT
    / "plugins"
    / "what-if-tony-stark-built-this"
    / "skills"
    / "what-if-tony-stark-built-this"
)
SCRIPTS = SKILL / "scripts"
COMPARE = SCRIPTS / "compare_designs.py"
EXAMPLE = SKILL / "assets" / "comparison-example"


def load_compare_module():
    spec = importlib.util.spec_from_file_location(
        "stark_compare_designs",
        COMPARE,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


COMPARE_MOD = load_compare_module()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle)
        handle.write("\n")


def run_cli(manifest: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(COMPARE), str(manifest), "--output", str(output)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )


class DecideWinnerTests(unittest.TestCase):
    def test_preserve_baseline_within_tie_fraction(self):
        records = [
            {
                "id": "base",
                "feasible": True,
                "aggregate_setup_plus_call_seconds": 1.02,
            },
            {
                "id": "candidate",
                "feasible": True,
                "aggregate_setup_plus_call_seconds": 1.0,
            },
        ]
        decision = COMPARE_MOD.decide_winner(records, "base", 0.05)
        self.assertEqual(decision["outcome"], "baseline_preserved")
        self.assertEqual(decision["winner_id"], "base")

    def test_select_unique_candidate_outside_band(self):
        records = [
            {
                "id": "base",
                "feasible": True,
                "aggregate_setup_plus_call_seconds": 2.0,
            },
            {
                "id": "candidate",
                "feasible": True,
                "aggregate_setup_plus_call_seconds": 1.0,
            },
        ]
        decision = COMPARE_MOD.decide_winner(records, "base", 0.05)
        self.assertEqual(decision["outcome"], "candidate_selected")
        self.assertEqual(decision["winner_id"], "candidate")
        self.assertEqual(decision["speedup_vs_baseline"], 2.0)

    def test_inconclusive_when_best_candidates_tie(self):
        records = [
            {
                "id": "base",
                "feasible": True,
                "aggregate_setup_plus_call_seconds": 3.0,
            },
            {
                "id": "c1",
                "feasible": True,
                "aggregate_setup_plus_call_seconds": 1.0,
            },
            {
                "id": "c2",
                "feasible": True,
                "aggregate_setup_plus_call_seconds": 1.0,
            },
        ]
        decision = COMPARE_MOD.decide_winner(records, "base", 0.05)
        self.assertEqual(decision["outcome"], "inconclusive")
        self.assertIsNone(decision["winner_id"])

    def test_no_feasible_variant(self):
        records = [
            {
                "id": "base",
                "feasible": False,
                "aggregate_setup_plus_call_seconds": None,
            },
            {
                "id": "candidate",
                "feasible": False,
                "aggregate_setup_plus_call_seconds": None,
            },
        ]
        decision = COMPARE_MOD.decide_winner(records, "base", 0.05)
        self.assertEqual(decision["outcome"], "no_feasible_variant")
        self.assertIsNone(decision["speedup_vs_baseline"])

    def test_near_tied_candidates_are_inconclusive(self):
        records=[dict(id='base',feasible=True,aggregate_setup_plus_call_seconds=3.0),
                 dict(id='a',feasible=True,aggregate_setup_plus_call_seconds=1.0),
                 dict(id='b',feasible=True,aggregate_setup_plus_call_seconds=1.02)]
        result=COMPARE_MOD.decide_winner(records,'base',0.05)
        self.assertEqual(result['outcome'],'inconclusive')
        self.assertIsNone(result['winner_id'])


class JsonEqualityTests(unittest.TestCase):
    def test_bool_is_not_int(self):
        self.assertFalse(COMPARE_MOD.json_equal(True, 1))
        self.assertTrue(COMPARE_MOD.json_equal({"ok": True}, {"ok": True}))

    def test_rejects_nonfinite(self):
        self.assertFalse(COMPARE_MOD.json_equal(1.0, float("nan")))


class ComparisonRunnerIntegrationTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory(prefix="stark-test-")
        self.dir = Path(self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def _manifest(
        self,
        *,
        variants: list[dict],
        cases: list[dict] | None = None,
        repeats: int = 2,
        timeout_seconds: float = 2,
        memory_limit_bytes=None,
        tie_fraction: float = 0.05,
        dependencies: list[str] | None = None,
        baseline: str = "base",
    ) -> Path:
        payload = {
            "version": 1,
            "baseline": baseline,
            "variants": variants,
            "cases": cases
            or [
                {
                    "id": "small",
                    "input": {"n": 1},
                    "expected": {"value": 1},
                    "measure": False,
                },
                {
                    "id": "workload",
                    "input": {"n": 2},
                    "expected": {"value": 2},
                    "measure": True,
                },
            ],
            "dependencies": dependencies or [],
            "repeats": repeats,
            "timeout_seconds": timeout_seconds,
            "memory_limit_bytes": memory_limit_bytes,
            "tie_fraction": tie_fraction,
        }
        path = self.dir / "experiment.json"
        write_json(path, payload)
        return path

    def test_real_example_cli(self):
        out = self.dir / "example-report.json"
        proc = run_cli(EXAMPLE / "experiment.json", out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "completed")
        self.assertEqual(report["decision"]["winner_id"], "candidate")
        self.assertIn("manifest_sha256", report["identities"])
        self.assertIn("runner_sha256", report["identities"])
        self.assertEqual(
            set(report["identities"]["variants"]),
            {"base", "candidate"},
        )

    def test_fast_incorrect_candidate(self):
        (self.dir / "base.py").write_text(
            "def run(payload):\n    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        (self.dir / "candidate.py").write_text(
            "def run(payload):\n    return {'value': payload['n'] + 1}\n",
            encoding="utf-8",
        )
        manifest = self._manifest(
            variants=[
                {"id": "base", "path": "base.py", "function": "run"},
                {"id": "candidate", "path": "candidate.py", "function": "run"},
            ]
        )
        out = self.dir / "report.json"
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in report["variants"]}
        self.assertTrue(by_id["base"]["feasible"])
        self.assertFalse(by_id["candidate"]["feasible"])
        self.assertEqual(by_id["candidate"]["qualification"], "incorrect")
        self.assertEqual(report["decision"]["winner_id"], "base")

    def test_timeout_and_crash(self):
        (self.dir / "base.py").write_text(
            "def run(payload):\n    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        (self.dir / "slow.py").write_text(
            "import time\n"
            "def run(payload):\n"
            "    time.sleep(5)\n"
            "    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        (self.dir / "crash.py").write_text(
            "def run(payload):\n    raise RuntimeError('boom')\n",
            encoding="utf-8",
        )
        manifest = self._manifest(
            variants=[
                {"id": "base", "path": "base.py", "function": "run"},
                {"id": "slow", "path": "slow.py", "function": "run"},
                {"id": "crash", "path": "crash.py", "function": "run"},
            ],
            timeout_seconds=2.0,
            repeats=1,
        )
        out = self.dir / "report.json"
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in report["variants"]}
        self.assertTrue(by_id["base"]["feasible"])
        self.assertEqual(by_id["slow"]["qualification"], "timeout")
        self.assertEqual(by_id["crash"]["qualification"], "crash")
        self.assertEqual(report["decision"]["winner_id"], "base")

    def test_memory_cap(self):
        (self.dir / "base.py").write_text(
            "def run(payload):\n    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        (self.dir / "heavy.py").write_text(
            "def run(payload):\n"
            "    blob = bytearray(2_000_000)\n"
            "    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        cases = [
            {
                "id": "small",
                "input": {"n": 1},
                "expected": {"value": 1},
                "measure": False,
            },
            {
                "id": "workload",
                "input": {"n": 2},
                "expected": {"value": 2},
                "measure": True,
            },
        ]
        manifest = self._manifest(
            variants=[
                {"id": "base", "path": "base.py", "function": "run"},
                {"id": "heavy", "path": "heavy.py", "function": "run"},
            ],
            cases=cases,
            memory_limit_bytes=500_000,
            repeats=1,
            timeout_seconds=5,
        )
        out = self.dir / "report.json"
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in report["variants"]}
        self.assertTrue(by_id["base"]["feasible"])
        self.assertFalse(by_id["heavy"]["feasible"])
        self.assertEqual(by_id["heavy"]["qualification"], "memory_limit")

    def test_no_winner_when_all_fail(self):
        (self.dir / "base.py").write_text(
            "def run(payload):\n    return {'value': 0}\n",
            encoding="utf-8",
        )
        (self.dir / "candidate.py").write_text(
            "def run(payload):\n    return {'value': -1}\n",
            encoding="utf-8",
        )
        manifest = self._manifest(
            variants=[
                {"id": "base", "path": "base.py", "function": "run"},
                {"id": "candidate", "path": "candidate.py", "function": "run"},
            ]
        )
        out = self.dir / "report.json"
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["decision"]["outcome"], "no_feasible_variant")
        self.assertIsNone(report["decision"]["winner_id"])

    def test_input_mutation_detected(self):
        (self.dir / "base.py").write_text(
            "def run(payload):\n    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        (self.dir / "mutator.py").write_text(
            "from pathlib import Path\n"
            "def run(payload):\n"
            "    target = Path(__file__).with_name('base.py')\n"
            "    target.write_text('def run(payload):\\n    return {\"value\": 999}\\n', encoding='utf-8')\n"
            "    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        manifest = self._manifest(
            variants=[
                {"id": "mutator", "path": "mutator.py", "function": "run"},
                {"id": "base", "path": "base.py", "function": "run"},
            ],
            baseline="base",
            repeats=1,
        )
        out = self.dir / "report.json"
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, COMPARE_MOD.EXIT_CHANGED_INPUT, proc.stderr)
        self.assertTrue(out.is_file())
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "rejected_changed_input")

    def test_source_identities_and_setup_cost(self):
        (self.dir / "base.py").write_text(
            "import time\n"
            "time.sleep(0.03)\n"
            "def run(payload):\n"
            "    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        (self.dir / "candidate.py").write_text(
            "def run(payload):\n"
            "    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        dep = self.dir / "dep.txt"
        dep.write_text("dependency-bytes\n", encoding="utf-8")
        manifest = self._manifest(
            variants=[
                {"id": "base", "path": "base.py", "function": "run"},
                {"id": "candidate", "path": "candidate.py", "function": "run"},
            ],
            dependencies=["dep.txt"],
            repeats=2,
            timeout_seconds=5,
            tie_fraction=0.0,
        )
        out = self.dir / "report.json"
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertIn("dep.txt", report["identities"]["dependencies"])
        self.assertEqual(len(report["identities"]["manifest_sha256"]), 64)
        by_id = {item["id"]: item for item in report["variants"]}
        # Setup sleep should inflate setup_plus_call relative to call-only for base.
        base_case = next(
            case for case in by_id["base"]["cases"] if case["id"] == "workload"
        )
        trial = base_case["measured_trials"][0]
        self.assertIsNotNone(trial["setup_plus_call_seconds"])
        self.assertIsNotNone(trial["call_seconds"])
        self.assertGreater(
            trial["setup_plus_call_seconds"],
            trial["call_seconds"] + 0.01,
        )
        self.assertEqual(report["decision"]["winner_id"], "candidate")

    def test_validation_and_overwrite_prevention(self):
        (self.dir / "base.py").write_text(
            "def run(payload):\n    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        bad = {
            "version": 1,
            "baseline": "missing",
            "variants": [{"id": "base", "path": "base.py", "function": "run"}],
            "cases": [
                {
                    "id": "small",
                    "input": {},
                    "expected": {},
                    "measure": False,
                }
            ],
            "dependencies": [],
            "repeats": 1,
            "timeout_seconds": 1,
            "memory_limit_bytes": None,
            "tie_fraction": 0.05,
        }
        manifest = self.dir / "bad.json"
        write_json(manifest, bad)
        out = self.dir / "report.json"
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, COMPARE_MOD.EXIT_VALIDATION)
        self.assertFalse(out.exists())

        # Missing measured case also invalid.
        bad["baseline"] = "base"
        write_json(manifest, bad)
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, COMPARE_MOD.EXIT_VALIDATION)

        # Overwrite prevention after a good run.
        good_manifest = self._manifest(
            variants=[{"id": "base", "path": "base.py", "function": "run"}],
            baseline="base",
            repeats=1,
        )
        proc = run_cli(good_manifest, out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc2 = run_cli(good_manifest, out)
        self.assertEqual(proc2.returncode, COMPARE_MOD.EXIT_OUTPUT_EXISTS)

    def test_path_escape_rejected(self):
        (self.dir / "base.py").write_text(
            "def run(payload):\n    return {'value': payload['n']}\n",
            encoding="utf-8",
        )
        nested = self.dir / "nested"
        nested.mkdir()
        shutil.copy(self.dir / "base.py", nested / "base.py")
        payload = {
            "version": 1,
            "baseline": "base",
            "variants": [
                {"id": "base", "path": "../base.py", "function": "run"},
            ],
            "cases": [
                {
                    "id": "small",
                    "input": {"n": 1},
                    "expected": {"value": 1},
                    "measure": False,
                },
                {
                    "id": "workload",
                    "input": {"n": 2},
                    "expected": {"value": 2},
                    "measure": True,
                },
            ],
            "dependencies": [],
            "repeats": 1,
            "timeout_seconds": 1,
            "memory_limit_bytes": None,
            "tie_fraction": 0.05,
        }
        manifest = nested / "experiment.json"
        write_json(manifest, payload)
        out = self.dir / "escape-report.json"
        proc = run_cli(manifest, out)
        self.assertEqual(proc.returncode, COMPARE_MOD.EXIT_VALIDATION)

    def test_module_helpers_and_dataclasses_load_normally(self):
        (self.dir/'helper.py').write_text('VALUE=7\n')
        (self.dir/'base.py').write_text('from dataclasses import dataclass\nfrom helper import VALUE\n@dataclass\nclass Row:\n    value: int\ndef run(payload):\n    return {"value":Row(VALUE).value}\n')
        m=self._manifest(variants=[dict(id='base',path='base.py',function='run')],
                         cases=[dict(id='work',input={},expected={'value':7},measure=True)],
                         dependencies=['helper.py'],repeats=1)
        out=self.dir/'helpers-report.json';proc=run_cli(m,out)
        self.assertEqual(proc.returncode,0,proc.stderr)
        r=json.loads(out.read_text());self.assertTrue(r['variants'][0]['feasible'])

    def test_nonzero_exit_after_result_is_a_crash(self):
        (self.dir/'base.py').write_text('import atexit,os\natexit.register(lambda:os._exit(7))\ndef run(payload):\n    return {"value":payload["n"]}\n')
        m=self._manifest(variants=[dict(id='base',path='base.py',function='run')],repeats=1)
        out=self.dir/'crash-report.json';proc=run_cli(m,out)
        self.assertEqual(proc.returncode,0,proc.stderr)
        r=json.loads(out.read_text());self.assertFalse(r['variants'][0]['feasible'])
        self.assertIsNone(r['decision']['winner_id'])

    def test_existing_neighbor_tmp_file_is_preserved(self):
        (self.dir/'base.py').write_text('def run(payload):\n    return {"value":payload["n"]}\n')
        m=self._manifest(variants=[dict(id='base',path='base.py',function='run')],repeats=1)
        out=self.dir/'report.json';neighbor=self.dir/'report.json.tmp';neighbor.write_text('keep this other work')
        proc=run_cli(m,out);self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertTrue(neighbor.exists());self.assertEqual(neighbor.read_text(),'keep this other work')

    def test_deleted_input_is_a_rejected_experiment(self):
        (self.dir/'base.py').write_text('from pathlib import Path\ndef run(payload):\n    Path(__file__).unlink(missing_ok=True)\n    return {"value":payload["n"]}\n')
        m=self._manifest(variants=[dict(id='base',path='base.py',function='run')],repeats=1)
        out=self.dir/'deleted-report.json';proc=run_cli(m,out)
        self.assertEqual(proc.returncode,COMPARE_MOD.EXIT_CHANGED_INPUT,proc.stderr)
        self.assertEqual(json.loads(out.read_text())['status'],'rejected_changed_input')

    def test_timing_and_allocation_run_in_separate_processes(self):
        (self.dir/'base.py').write_text('import tracemalloc\nfrom pathlib import Path\ndef run(payload):\n    with Path(__file__).with_name("observed.txt").open("a") as f:f.write(str(tracemalloc.is_tracing())+"\\n")\n    return {"value":payload["n"]}\n')
        m=self._manifest(variants=[dict(id='base',path='base.py',function='run')],repeats=2)
        out=self.dir/'separate-report.json';proc=run_cli(m,out)
        self.assertEqual(proc.returncode,0,proc.stderr)
        r=json.loads(out.read_text());case=next(c for c in r['variants'][0]['cases'] if c['measure'])
        self.assertEqual(len(case['measured_trials']),2)
        self.assertTrue(all(t['python_traced_peak_bytes'] is None for t in case['measured_trials']))
        self.assertEqual(len(case['allocation_trials']),2)
        self.assertTrue(all(t['python_traced_peak_bytes'] is not None for t in case['allocation_trials']))
        states=(self.dir/'observed.txt').read_text().splitlines()
        self.assertEqual(states.count('True'),2)
        self.assertEqual(states.count('False'),4)

    def test_ids_do_not_escape_scratch(self):
        (self.dir/'base.py').write_text('def run(payload):return {"value":payload["n"]}\n')
        m=self._manifest(variants=[dict(id='../escape',path='base.py',function='run')],baseline='../escape',repeats=1)
        raw=json.loads(m.read_text());config=COMPARE_MOD.validate_manifest(raw,self.dir)
        scratch=self.dir/'scratch';scratch.mkdir();observed=[]
        def fake(**kwargs):
            observed.append(kwargs['work_dir'].resolve())
            return dict(ok=True,status='ok',result={'value':kwargs['argument']['n']},error=None,
                        setup_seconds=0.1,call_seconds=0.1,setup_plus_call_seconds=0.2,
                        subprocess_wall_seconds=0.3,python_traced_peak_bytes=1 if kwargs['trace_memory'] else None)
        with patch.object(COMPARE_MOD,'run_worker_once',side_effect=fake),patch.object(COMPARE_MOD,'assert_identities_unchanged'):
            COMPARE_MOD.evaluate_variant(variant=config['variants'][0],manifest=config,manifest_path=m,identities={},scratch_root=scratch)
        self.assertTrue(observed)
        self.assertTrue(all(scratch.resolve() in path.parents for path in observed))

    def test_report_publication_never_replaces_a_concurrent_writer(self):
        out=self.dir/'concurrent.json';out.write_text('other writer')
        with self.assertRaises(FileExistsError):COMPARE_MOD._write_report(out,{'ours':True})
        self.assertEqual(out.read_text(),'other writer')
        self.assertEqual(list(self.dir.glob('.stark-report-*.tmp')),[])

    def test_invalid_numeric_configuration_fails_validation(self):
        (self.dir/'base.py').write_text('def run(payload):return payload\n')
        m=self._manifest(variants=[dict(id='base',path='base.py',function='run')],repeats=1)
        original=json.loads(m.read_text())
        for field,value in [('version',True),('timeout_seconds',10**1000),('tie_fraction',10**1000)]:
            data=dict(original);data[field]=value
            with self.subTest(field=field),self.assertRaises(COMPARE_MOD.ManifestError):
                COMPARE_MOD.validate_manifest(data,self.dir)

    @unittest.skipUnless(hasattr(__import__('os'),'killpg'),'POSIX owned process groups')
    def test_cleanup_can_reach_children_after_group_leader_exits(self):
        from unittest.mock import Mock
        process=Mock();process.pid=12345;process.poll.return_value=0
        with patch.object(COMPARE_MOD.os,'killpg') as kill_group:
            COMPARE_MOD._kill_process_group(process)
        kill_group.assert_called_once_with(12345,COMPARE_MOD.signal.SIGKILL)


if __name__ == "__main__":
    unittest.main()
