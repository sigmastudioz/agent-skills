"""Baseline design: correct but pays a fixed setup-plus-call cost."""

from __future__ import annotations

import time
from typing import Any

# Module import setup cost (counted in setup_plus_call).
_SETUP_MARKER = sum(range(2000))


def run(payload: dict[str, Any]) -> dict[str, Any]:
    n = int(payload.get("n", 0))
    time.sleep(0.05)
    return {"sum": n * (n + 1) // 2, "setup_marker": _SETUP_MARKER}
