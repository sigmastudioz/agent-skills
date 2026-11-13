#!/usr/bin/env python3
"""Subprocess worker for compare_designs: import module, call once, report timings.

Not a security sandbox. Candidate stdout/stderr stay on the process pipes; structured
results are written only to --result-file so they cannot be corrupted by prints.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
import traceback
import tracemalloc
from pathlib import Path
from typing import Any


def _reject_nonfinite(value: Any, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"nonfinite float at {path}")
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_nonfinite(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nonfinite(item, f"{path}[{index}]")


def _load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(
        "_stark_compare_variant",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(module_path.resolve().parent))
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Variant measurement worker")
    parser.add_argument("--module-path", required=True)
    parser.add_argument("--function", required=True)
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--result-file", required=True)
    parser.add_argument("--trace-memory", action="store_true")
    args = parser.parse_args(argv)

    wall_started = time.perf_counter()
    payload: dict[str, Any] = {
        "ok": False,
        "result": None,
        "setup_seconds": None,
        "call_seconds": None,
        "setup_plus_call_seconds": None,
        "subprocess_wall_seconds": None,
        "python_traced_peak_bytes": None,
        "error": None,
    }

    tracing = False
    try:
        with open(args.input_file, encoding="utf-8") as handle:
            argument = json.load(handle)
        _reject_nonfinite(argument)

        if args.trace_memory:
            tracemalloc.start()
            tracing = True

        setup_started = time.perf_counter()
        module = _load_module(Path(args.module_path))
        function = getattr(module, args.function)
        setup_seconds = time.perf_counter() - setup_started

        call_started = time.perf_counter()
        result = function(argument)
        call_seconds = time.perf_counter() - call_started

        peak = None
        if tracing:
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            tracing = False
        _reject_nonfinite(result)

        payload.update(
            {
                "ok": True,
                "result": result,
                "setup_seconds": setup_seconds,
                "call_seconds": call_seconds,
                "setup_plus_call_seconds": setup_seconds + call_seconds,
                "python_traced_peak_bytes": peak,
            }
        )
    except BaseException as exc:  # noqa: BLE001 — report crash details to parent
        if tracing:
            try:
                _, peak = tracemalloc.get_traced_memory()
                payload["python_traced_peak_bytes"] = peak
                tracemalloc.stop()
            except Exception:  # noqa: BLE001
                pass
            tracing = False
        payload["error"] = {
            "kind": "crash" if not isinstance(exc, Exception) else "exception",
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
    finally:
        payload["subprocess_wall_seconds"] = time.perf_counter() - wall_started
        result_path = Path(args.result_file)
        result_path.parent.mkdir(parents=True, exist_ok=True)
        with open(result_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, allow_nan=False)
            handle.write("\n")

    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
