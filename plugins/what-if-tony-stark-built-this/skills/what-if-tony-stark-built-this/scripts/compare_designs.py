#!/usr/bin/env python3
"""Compare authorized local design variants under a Manifest v1 experiment.

Public entry:
  python3 compare_designs.py experiment.json --output report.json

Standard-library only. Subprocess isolation is measurement isolation, not a sandbox.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import signal
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
MANIFEST_VERSION = 1

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_VALIDATION = 2
EXIT_OUTPUT_EXISTS = 3
EXIT_CHANGED_INPUT = 4
EXIT_INTERNAL = 5

RUNNER_DIR = Path(__file__).resolve().parent
WORKER_PATH = RUNNER_DIR / "variant_worker.py"
RUNNER_PATH = Path(__file__).resolve()

MEASUREMENT_NOTES = (
    "Timing and allocation use separate fresh Python subprocesses, with no tracing in ranked timing. Measured times cover variant module "
    "import/setup plus one function call; call_seconds is reported separately. "
    "python_traced_peak_bytes is tracemalloc peak allocation during import and call "
    "(Python traced allocation, not RSS). Excluded from measured intervals: parent "
    "input parsing, interpreter startup outside the worker, JSON encode/decode of the "
    "worker protocol, and parent orchestration. subprocess_wall_seconds retains full "
    "worker wall time including worker-side protocol overhead after launch."
)


class ManifestError(ValueError):
    """Invalid experiment configuration."""


class ChangedInputError(RuntimeError):
    """Manifest or source inputs changed during execution."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reject_nonfinite(value: Any, path: str = "$") -> None:
    if isinstance(value, bool):
        return
    if isinstance(value, float) and not math.isfinite(value):
        raise ManifestError(f"nonfinite float at {path}")
    if isinstance(value, dict):
        for key, item in value.items():
            reject_nonfinite(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_nonfinite(item, f"{path}[{index}]")


def json_equal(expected: Any, actual: Any) -> bool:
    """Exact structural JSON equality; bool is not int; nonfinite rejected."""
    if isinstance(expected, float) and not math.isfinite(expected):
        return False
    if isinstance(actual, float) and not math.isfinite(actual):
        return False
    if type(expected) is not type(actual):
        # JSON has no distinct integer/float for whole numbers from some encoders,
        # but Python json keeps int vs float. Require exact Python types after load.
        return False
    if isinstance(expected, dict):
        if expected.keys() != actual.keys():
            return False
        return all(json_equal(expected[key], actual[key]) for key in expected)
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return False
        return all(json_equal(left, right) for left, right in zip(expected, actual))
    return expected == actual


def _is_relative_under(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def resolve_contained_file(root: Path, relative: str, label: str) -> Path:
    if not isinstance(relative, str) or not relative or relative.startswith("/"):
        raise ManifestError(f"{label} must be a relative path string")
    relative_path = Path(relative)
    if relative_path.is_absolute():
        raise ManifestError(f"{label} must be a relative path string")
    joined = root / relative_path
    if joined.is_symlink():
        raise ManifestError(f"{label} must be a contained regular file: {relative}")
    resolved = joined.resolve()
    if not _is_relative_under(root, resolved):
        raise ManifestError(f"{label} escapes manifest directory: {relative}")
    if not resolved.is_file() or resolved.is_symlink() or resolved.is_dir():
        raise ManifestError(f"{label} must be a contained regular file: {relative}")
    return resolved


def _finite_positive_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ManifestError(f"{label} must be a finite positive number")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ManifestError(f"{label} must be a finite positive number") from exc
    if not math.isfinite(number) or number <= 0:
        raise ManifestError(f"{label} must be a finite positive number")
    return number


def validate_manifest(raw: Any, manifest_dir: Path) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ManifestError("manifest must be a JSON object")
    if type(raw.get("version")) is not int or raw["version"] != MANIFEST_VERSION:
        raise ManifestError(f"unsupported manifest version: {raw.get('version')!r}")

    baseline = raw.get("baseline")
    if not isinstance(baseline, str) or not baseline:
        raise ManifestError("baseline must be a nonempty string variant id")

    variants_raw = raw.get("variants")
    if not isinstance(variants_raw, list) or not variants_raw:
        raise ManifestError("variants must be a nonempty array")

    variants: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(variants_raw):
        if not isinstance(item, dict):
            raise ManifestError(f"variants[{index}] must be an object")
        variant_id = item.get("id")
        path = item.get("path")
        function = item.get("function")
        if not isinstance(variant_id, str) or not variant_id:
            raise ManifestError(f"variants[{index}].id must be a nonempty string")
        if variant_id in seen_ids:
            raise ManifestError(f"duplicate variant id: {variant_id}")
        seen_ids.add(variant_id)
        if not isinstance(function, str) or not function:
            raise ManifestError(f"variants[{index}].function must be a nonempty string")
        resolved = resolve_contained_file(manifest_dir, path, f"variants[{index}].path")
        variants.append(
            {
                "id": variant_id,
                "path": path,
                "function": function,
                "resolved_path": resolved,
            }
        )

    if baseline not in seen_ids:
        raise ManifestError(f"baseline id not found in variants: {baseline}")

    cases_raw = raw.get("cases")
    if not isinstance(cases_raw, list) or not cases_raw:
        raise ManifestError("cases must be a nonempty array")

    cases: list[dict[str, Any]] = []
    case_ids: set[str] = set()
    measured = 0
    for index, item in enumerate(cases_raw):
        if not isinstance(item, dict):
            raise ManifestError(f"cases[{index}] must be an object")
        case_id = item.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise ManifestError(f"cases[{index}].id must be a nonempty string")
        if case_id in case_ids:
            raise ManifestError(f"duplicate case id: {case_id}")
        case_ids.add(case_id)
        if "input" not in item or "expected" not in item:
            raise ManifestError(f"cases[{index}] requires input and expected")
        if "measure" not in item or not isinstance(item["measure"], bool):
            raise ManifestError(f"cases[{index}].measure must be a boolean")
        reject_nonfinite(item["input"], f"cases[{index}].input")
        reject_nonfinite(item["expected"], f"cases[{index}].expected")
        if item["measure"]:
            measured += 1
        cases.append(
            {
                "id": case_id,
                "input": item["input"],
                "expected": item["expected"],
                "measure": item["measure"],
            }
        )
    if measured < 1:
        raise ManifestError("at least one case must have measure=true")

    dependencies_raw = raw.get("dependencies", [])
    if not isinstance(dependencies_raw, list):
        raise ManifestError("dependencies must be an array")
    dependencies: list[dict[str, Any]] = []
    for index, rel in enumerate(dependencies_raw):
        resolved = resolve_contained_file(manifest_dir, rel, f"dependencies[{index}]")
        dependencies.append({"path": rel, "resolved_path": resolved})

    repeats = raw.get("repeats")
    if isinstance(repeats, bool) or not isinstance(repeats, int) or repeats < 1:
        raise ManifestError("repeats must be a bounded positive integer")
    if repeats > 10_000:
        raise ManifestError("repeats exceeds supported bound (10000)")

    timeout_seconds = _finite_positive_number(raw.get("timeout_seconds"), "timeout_seconds")
    if timeout_seconds > 86_400:
        raise ManifestError("timeout_seconds exceeds supported bound")

    memory_limit_bytes = raw.get("memory_limit_bytes", None)
    if memory_limit_bytes is not None:
        if isinstance(memory_limit_bytes, bool) or not isinstance(memory_limit_bytes, int):
            raise ManifestError("memory_limit_bytes must be null or a positive integer")
        if memory_limit_bytes < 1:
            raise ManifestError("memory_limit_bytes must be a positive integer when set")

    tie_fraction = raw.get("tie_fraction")
    if isinstance(tie_fraction, bool) or not isinstance(tie_fraction, (int, float)):
        raise ManifestError("tie_fraction must be a finite number in [0, 1)")
    try:
        tie_fraction_f = float(tie_fraction)
    except OverflowError as exc:
        raise ManifestError("tie_fraction must be a finite number in [0, 1)") from exc
    if not math.isfinite(tie_fraction_f) or tie_fraction_f < 0 or tie_fraction_f >= 1:
        raise ManifestError("tie_fraction must be a finite number in [0, 1)")

    return {
        "version": MANIFEST_VERSION,
        "baseline": baseline,
        "variants": variants,
        "cases": cases,
        "dependencies": dependencies,
        "repeats": repeats,
        "timeout_seconds": timeout_seconds,
        "memory_limit_bytes": memory_limit_bytes,
        "tie_fraction": tie_fraction_f,
    }


def collect_identities(manifest_path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "manifest_sha256": sha256_file(manifest_path),
        "runner_sha256": sha256_file(RUNNER_PATH),
        "worker_sha256": sha256_file(WORKER_PATH),
        "variants": {
            item["id"]: sha256_file(item["resolved_path"]) for item in manifest["variants"]
        },
        "dependencies": {
            item["path"]: sha256_file(item["resolved_path"])
            for item in manifest["dependencies"]
        },
    }


def assert_identities_unchanged(
    manifest_path: Path,
    manifest: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    try:
        current = collect_identities(manifest_path, manifest)
    except OSError as exc:
        raise ChangedInputError("experiment input disappeared or became unreadable") from exc
    if current != expected:
        raise ChangedInputError("experiment inputs changed during execution")


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("median of empty sample")
    return float(statistics.median(values))


def within_tie_fraction(value: float, best: float, tie_fraction: float) -> bool:
    if best == 0:
        return value == 0
    return value <= best * (1.0 + tie_fraction)


def decide_winner(
    variant_records: list[dict[str, Any]],
    baseline_id: str,
    tie_fraction: float,
) -> dict[str, Any]:
    """Deterministic selector over already-qualified variant aggregates.

    Aggregate metric name: sum_median_setup_plus_call_seconds
    """
    metric_name = "sum_median_setup_plus_call_seconds"
    feasible = [item for item in variant_records if item.get("feasible")]
    aggregates = {
        item["id"]: item.get("aggregate_setup_plus_call_seconds") for item in variant_records
    }

    if not feasible:
        return {
            "winner_id": None,
            "outcome": "no_feasible_variant",
            "reason": "No variant passed correctness, timeout, crash, and memory limits.",
            "aggregate_metric_name": metric_name,
            "aggregates": aggregates,
            "speedup_vs_baseline": None,
            "baseline_valid": False,
        }

    best_time = min(item["aggregate_setup_plus_call_seconds"] for item in feasible)
    best_ids = [
        item["id"]
        for item in feasible
        if within_tie_fraction(item["aggregate_setup_plus_call_seconds"], best_time, tie_fraction)
    ]
    baseline = next((item for item in feasible if item["id"] == baseline_id), None)
    baseline_valid = baseline is not None
    baseline_time = (
        baseline["aggregate_setup_plus_call_seconds"] if baseline_valid else None
    )

    speedup = None
    if baseline_valid and within_tie_fraction(baseline_time, best_time, tie_fraction):
        if baseline_time and baseline_time > 0:
            speedup = baseline_time / baseline_time  # 1.0 when preserving baseline
        elif baseline_time == 0:
            speedup = 1.0
        return {
            "winner_id": baseline_id,
            "outcome": "baseline_preserved",
            "reason": (
                "Feasible baseline is within tie_fraction of the lowest aggregate "
                f"({metric_name}); preserving baseline."
            ),
            "aggregate_metric_name": metric_name,
            "aggregates": aggregates,
            "speedup_vs_baseline": speedup,
            "baseline_valid": True,
        }

    if len(best_ids) == 1:
        winner_id = best_ids[0]
        if baseline_valid and baseline_time and best_time > 0:
            speedup = baseline_time / best_time
        elif baseline_valid and baseline_time == 0 and best_time == 0:
            speedup = 1.0
        else:
            speedup = None
        return {
            "winner_id": winner_id,
            "outcome": "candidate_selected",
            "reason": (
                f"Unique candidate outside the tie band for {metric_name}; baseline not within band."
                if baseline_valid
                else f"Unique candidate outside the tie band for {metric_name}; baseline was not feasible."
            ),
            "aggregate_metric_name": metric_name,
            "aggregates": aggregates,
            "speedup_vs_baseline": speedup,
            "baseline_valid": baseline_valid,
        }

    return {
        "winner_id": None,
        "outcome": "inconclusive",
        "reason": (
            "Multiple feasible candidates fall within the best aggregate tie band and the baseline "
            "is not within tie_fraction of that best; no unique winner."
        ),
        "aggregate_metric_name": metric_name,
        "aggregates": aggregates,
        "speedup_vs_baseline": None,
        "baseline_valid": baseline_valid,
    }


def _kill_process_group(proc: subprocess.Popen[bytes]) -> None:
    try:
        if hasattr(os, "killpg"):
            os.killpg(proc.pid, signal.SIGKILL)
        elif proc.poll() is None:
            proc.kill()
    except ProcessLookupError:
        pass
    except PermissionError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass


def run_worker_once(
    *,
    module_path: Path,
    function: str,
    argument: Any,
    timeout_seconds: float,
    trace_memory: bool,
    work_dir: Path,
) -> dict[str, Any]:
    input_path = work_dir / "input.json"
    result_path = work_dir / "result.json"
    if result_path.exists():
        result_path.unlink()
    with open(input_path, "w", encoding="utf-8") as handle:
        json.dump(argument, handle, allow_nan=False)

    command = [
        sys.executable,
        "-B",
        str(WORKER_PATH),
        "--module-path",
        str(module_path),
        "--function",
        function,
        "--input-file",
        str(input_path),
        "--result-file",
        str(result_path),
    ]
    if trace_memory:
        command.append("--trace-memory")

    parent_started = time.perf_counter()
    try:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(module_path.parent),
            start_new_session=True,
        )
    except OSError as exc:
        return {
            "status": "crash",
            "ok": False,
            "result": None,
            "error": {"kind": "launch_failure", "message": str(exc)},
            "stdout": "",
            "stderr": "",
            "setup_seconds": None,
            "call_seconds": None,
            "setup_plus_call_seconds": None,
            "subprocess_wall_seconds": None,
            "python_traced_peak_bytes": None,
            "parent_wait_seconds": time.perf_counter() - parent_started,
            "timed_out": False,
        }

    timed_out = False
    try:
        stdout_b, stderr_b = proc.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_process_group(proc)
        try:
            stdout_b, stderr_b = proc.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            _kill_process_group(proc)
            stdout_b, stderr_b = b"", b""
    except BaseException:
        _kill_process_group(proc)
        try:
            proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        raise
    parent_wait = time.perf_counter() - parent_started

    stdout_text = stdout_b.decode("utf-8", errors="replace") if stdout_b else ""
    stderr_text = stderr_b.decode("utf-8", errors="replace") if stderr_b else ""

    if timed_out:
        return {
            "status": "timeout",
            "ok": False,
            "result": None,
            "error": {
                "kind": "timeout",
                "message": f"exceeded timeout_seconds={timeout_seconds}",
            },
            "stdout": stdout_text,
            "stderr": stderr_text,
            "setup_seconds": None,
            "call_seconds": None,
            "setup_plus_call_seconds": None,
            "subprocess_wall_seconds": parent_wait,
            "python_traced_peak_bytes": None,
            "parent_wait_seconds": parent_wait,
            "timed_out": True,
            "exit_code": proc.returncode,
        }

    worker_payload: dict[str, Any] | None = None
    if result_path.is_file():
        try:
            with open(result_path, encoding="utf-8") as handle:
                worker_payload = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            worker_payload = None
            stderr_text = f"{stderr_text}\nresult parse error: {exc}".strip()

    if worker_payload is None:
        return {
            "status": "crash",
            "ok": False,
            "result": None,
            "error": {
                "kind": "missing_result",
                "message": "worker did not produce a result file",
                "exit_code": proc.returncode,
            },
            "stdout": stdout_text,
            "stderr": stderr_text,
            "setup_seconds": None,
            "call_seconds": None,
            "setup_plus_call_seconds": None,
            "subprocess_wall_seconds": parent_wait,
            "python_traced_peak_bytes": None,
            "parent_wait_seconds": parent_wait,
            "timed_out": False,
            "exit_code": proc.returncode,
        }

    ok = bool(worker_payload.get("ok")) and proc.returncode == 0
    if proc.returncode != 0 and worker_payload.get("ok"):
        worker_payload["error"] = {"kind": "nonzero_exit", "message": f"worker exited {proc.returncode} after writing a result"}
    status = "ok" if ok else "crash"
    return {
        "status": status,
        "ok": ok,
        "result": worker_payload.get("result"),
        "error": worker_payload.get("error"),
        "stdout": stdout_text,
        "stderr": stderr_text,
        "setup_seconds": worker_payload.get("setup_seconds"),
        "call_seconds": worker_payload.get("call_seconds"),
        "setup_plus_call_seconds": worker_payload.get("setup_plus_call_seconds"),
        "subprocess_wall_seconds": worker_payload.get("subprocess_wall_seconds"),
        "python_traced_peak_bytes": worker_payload.get("python_traced_peak_bytes"),
        "parent_wait_seconds": parent_wait,
        "timed_out": False,
        "exit_code": proc.returncode,
    }


def _trial_failure_reason(
    trial: dict[str, Any],
    expected: Any,
    memory_limit_bytes: int | None,
) -> tuple[str | None, str | None]:
    if trial.get("timed_out") or trial.get("status") == "timeout":
        return "timeout", trial.get("error", {}).get("message", "timeout")
    if not trial.get("ok"):
        err = trial.get("error") or {}
        return "crash", err.get("message") or err.get("type") or "crash"
    if not json_equal(expected, trial.get("result")):
        return "incorrect", "result failed exact structural JSON equality"
    peak = trial.get("python_traced_peak_bytes")
    if memory_limit_bytes is not None and peak is not None and peak > memory_limit_bytes:
        return (
            "memory_limit",
            f"python_traced_peak_bytes {peak} exceeds memory_limit_bytes {memory_limit_bytes}",
        )
    return None, None


def _trial_record(trial, kind=None, repeat=None):
    record = {key: trial.get(key) for key in (
        "setup_seconds", "call_seconds", "setup_plus_call_seconds",
        "subprocess_wall_seconds", "parent_wait_seconds", "python_traced_peak_bytes", "error", "exit_code")}
    record.update(status=kind or "ok", ok=kind is None,
                  stdout_tail=(trial.get("stdout") or "")[-2000:],
                  stderr_tail=(trial.get("stderr") or "")[-2000:])
    if repeat is not None:
        record["repeat"] = repeat
    return record


def evaluate_variant(*, variant, manifest, manifest_path, identities, scratch_root):
    case_results = []
    exclusion_kind = exclusion_reason = None
    measured_medians, peak_samples = [], []
    variant_dir = scratch_root / hashlib.sha256(variant["id"].encode()).hexdigest()

    def execute(case, phase, trace):
        directory = variant_dir / hashlib.sha256(case["id"].encode()).hexdigest() / phase
        directory.mkdir(parents=True, exist_ok=True)
        assert_identities_unchanged(manifest_path, manifest, identities)
        trial = run_worker_once(module_path=variant["resolved_path"], function=variant["function"],
                                argument=case["input"], timeout_seconds=manifest["timeout_seconds"],
                                trace_memory=trace, work_dir=directory)
        assert_identities_unchanged(manifest_path, manifest, identities)
        return trial

    # Complete all correctness checks before doing any ranking measurements.
    for case in manifest["cases"]:
        trial = execute(case, "correctness", False)
        kind, reason = _trial_failure_reason(trial, case["expected"], None)
        record = dict(id=case["id"], measure=case["measure"], correctness=_trial_record(trial, kind),
                      measured_trials=[], allocation_trials=[], median_setup_plus_call_seconds=None,
                      median_call_seconds=None, qualification=kind or "ok", detail=reason)
        case_results.append(record)
        if kind is not None and exclusion_kind is None:
            exclusion_kind, exclusion_reason = kind, f"case {case['id']}: {reason}"

    if exclusion_kind is None:
        for case, record in zip(manifest["cases"], case_results):
            if not case["measure"]:
                continue
            kind = reason = None
            for repeat in range(manifest["repeats"]):
                # Ranking samples are not perturbed by tracemalloc.
                trial = execute(case, f"timing_{repeat}", False)
                kind, reason = _trial_failure_reason(trial, case["expected"], None)
                record["measured_trials"].append(_trial_record(trial, kind, repeat))
                if kind is not None:
                    break
            if kind is None:
                for repeat in range(manifest["repeats"]):
                    trial = execute(case, f"allocation_{repeat}", True)
                    kind, reason = _trial_failure_reason(trial, case["expected"], manifest["memory_limit_bytes"])
                    record["allocation_trials"].append(_trial_record(trial, kind, repeat))
                    if trial.get("python_traced_peak_bytes") is not None:
                        peak_samples.append(trial["python_traced_peak_bytes"])
                    if kind is not None:
                        break
            record["qualification"], record["detail"] = kind or "ok", reason
            if kind is not None:
                exclusion_kind, exclusion_reason = kind, f"case {case['id']}: {reason}"
                break
            samples = record["measured_trials"]
            record["median_setup_plus_call_seconds"] = median([t["setup_plus_call_seconds"] for t in samples])
            record["median_call_seconds"] = median([t["call_seconds"] for t in samples])
            measured_medians.append(record["median_setup_plus_call_seconds"])

    assert_identities_unchanged(manifest_path, manifest, identities)
    feasible = exclusion_kind is None
    return dict(id=variant["id"], path=variant["path"], function=variant["function"], feasible=feasible,
                qualification="feasible" if feasible else exclusion_kind, exclusion_reason=exclusion_reason,
                cases=case_results, aggregate_setup_plus_call_seconds=sum(measured_medians) if feasible else None,
                max_python_traced_peak_bytes=max(peak_samples) if peak_samples else None)


def build_report(
    *,
    manifest_path: Path,
    manifest: dict[str, Any],
    identities: dict[str, Any],
    variant_records: list[dict[str, Any]],
    decision: dict[str, Any],
    status: str,
    status_detail: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "status_detail": status_detail,
        "manifest": {
            "path": str(manifest_path),
            "version": manifest["version"],
            "baseline": manifest["baseline"],
            "repeats": manifest["repeats"],
            "timeout_seconds": manifest["timeout_seconds"],
            "memory_limit_bytes": manifest["memory_limit_bytes"],
            "tie_fraction": manifest["tie_fraction"],
            "case_ids": [case["id"] for case in manifest["cases"]],
            "variant_ids": [item["id"] for item in manifest["variants"]],
        },
        "environment": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "executable": sys.executable,
            "measurement_notes": MEASUREMENT_NOTES,
        },
        "limits": {
            "timeout_seconds": manifest["timeout_seconds"],
            "memory_limit_bytes": manifest["memory_limit_bytes"],
            "repeats": manifest["repeats"],
            "tie_fraction": manifest["tie_fraction"],
            "memory_metric": "python_traced_peak_bytes",
            "aggregate_metric_name": "sum_median_setup_plus_call_seconds",
        },
        "identities": identities,
        "variants": variant_records,
        "decision": decision,
    }


def run_experiment(manifest_path: Path, output_path: Path) -> tuple[int, dict[str, Any] | None]:
    if output_path.exists() or output_path.is_symlink():
        print(
            f"error: refusing to overwrite existing report: {output_path}",
            file=sys.stderr,
        )
        return EXIT_OUTPUT_EXISTS, None

    try:
        manifest_bytes = manifest_path.read_bytes()
        raw = json.loads(manifest_bytes)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"error: cannot read manifest: {exc}", file=sys.stderr)
        return EXIT_VALIDATION, None

    manifest_dir = manifest_path.parent
    try:
        manifest = validate_manifest(raw, manifest_dir)
    except ManifestError as exc:
        print(f"error: invalid manifest: {exc}", file=sys.stderr)
        return EXIT_VALIDATION, None

    if not WORKER_PATH.is_file():
        print(f"error: missing worker at {WORKER_PATH}", file=sys.stderr)
        return EXIT_INTERNAL, None

    identities = collect_identities(manifest_path, manifest)
    variant_records: list[dict[str, Any]] = []

    try:
        if identities["manifest_sha256"] != hashlib.sha256(manifest_bytes).hexdigest():
            raise ChangedInputError("manifest changed while loading the experiment")
        with tempfile.TemporaryDirectory(prefix="stark-compare-") as tmp:
            scratch = Path(tmp)
            for variant in manifest["variants"]:
                assert_identities_unchanged(manifest_path, manifest, identities)
                record = evaluate_variant(
                    variant=variant,
                    manifest=manifest,
                    manifest_path=manifest_path,
                    identities=identities,
                    scratch_root=scratch,
                )
                variant_records.append(record)
            assert_identities_unchanged(manifest_path, manifest, identities)
    except ChangedInputError as exc:
        decision = {
            "winner_id": None,
            "outcome": "rejected_changed_input",
            "reason": str(exc),
            "aggregate_metric_name": "sum_median_setup_plus_call_seconds",
            "aggregates": {
                item["id"]: item.get("aggregate_setup_plus_call_seconds")
                for item in variant_records
            },
            "speedup_vs_baseline": None,
            "baseline_valid": False,
        }
        report = build_report(
            manifest_path=manifest_path,
            manifest=manifest,
            identities=identities,
            variant_records=variant_records,
            decision=decision,
            status="rejected_changed_input",
            status_detail=str(exc),
        )
        try:
            _write_report(output_path, report)
        except FileExistsError:
            return EXIT_OUTPUT_EXISTS, report
        except OSError as write_exc:
            print(f"error: cannot write report: {write_exc}", file=sys.stderr)
            return EXIT_INTERNAL, report
        print(
            "rejected: experiment inputs changed during execution; "
            f"report={output_path}"
        )
        return EXIT_CHANGED_INPUT, report

    decision = decide_winner(
        variant_records,
        manifest["baseline"],
        manifest["tie_fraction"],
    )
    report = build_report(
        manifest_path=manifest_path,
        manifest=manifest,
        identities=identities,
        variant_records=variant_records,
        decision=decision,
        status="completed",
    )
    try:
        _write_report(output_path, report)
    except FileExistsError:
        return EXIT_OUTPUT_EXISTS, report
    except OSError as exc:
        print(f"error: cannot write report: {exc}", file=sys.stderr)
        return EXIT_INTERNAL, report

    winner = decision.get("winner_id")
    print(
        f"status=completed outcome={decision.get('outcome')} "
        f"winner={winner!r} report={output_path}"
    )
    return EXIT_OK, report


def _write_report(output_path: Path, report: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output_path.parent,
                                         prefix=".stark-report-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(report, handle, indent=2, allow_nan=False)
            handle.write("\n")
        # Exclusive publication: never replace another writer's report or side file.
        os.link(temporary, output_path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare Manifest v1 design variants with correctness and measured trials."
        )
    )
    parser.add_argument(
        "experiment",
        type=Path,
        help="Path to experiment.json (Manifest v1); paths inside are relative to it",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Destination report.json (must not already exist)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return 0 if code == 0 else EXIT_USAGE

    try:
        exit_code, _report = run_experiment(
            args.experiment.resolve(),
            args.output.absolute(),
        )
        return exit_code
    except Exception as exc:  # noqa: BLE001
        print(f"error: internal failure: {exc}", file=sys.stderr)
        traceback.print_exc()
        return EXIT_INTERNAL


if __name__ == "__main__":
    sys.exit(main())
