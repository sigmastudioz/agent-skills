"""Candidate design: same answer with far lower call cost."""

from __future__ import annotations

from typing import Any

_SETUP_MARKER = sum(range(2000))


def run(payload: dict[str, Any]) -> dict[str, Any]:
    n = int(payload.get("n", 0))
    return {"sum": n * (n + 1) // 2, "setup_marker": _SETUP_MARKER}
