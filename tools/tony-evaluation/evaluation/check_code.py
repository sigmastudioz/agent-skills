#!/usr/bin/env python3
"""Hidden local behavioral checks for returned pilot code; not supplied to evaluated models."""
from pathlib import Path
import argparse
import ast
import copy
import importlib.util
import io
import json
import unittest

CANDIDATE = None


def inspect_source(source):
    """Reject obvious off-task effects before coordinator inspection; not a security sandbox."""
    tree = ast.parse(source)
    allowed = {"copy", "collections", "dataclasses", "typing", "__future__"}
    denied = {"open", "exec", "eval", "compile", "__import__", "input", "breakpoint", "exit", "quit"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(n.name.split(".")[0] not in allowed for n in node.names):
            raise ValueError("Off-task import; inspect manually before execution")
        if isinstance(node, ast.ImportFrom) and (node.level or (node.module or "").split(".")[0] not in allowed):
            raise ValueError("Off-task import; inspect manually before execution")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in denied:
            raise ValueError("Off-task executable call")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            raise ValueError("Off-task reflective attribute")
    return tree


class InventoryChecks(unittest.TestCase):
    def setUp(self):
        self.original = {("a", "x"): 10, ("a", "y"): 5, ("b", "x"): 8}
        self.store = CANDIDATE.Inventory(self.original)

    def test_reserve_and_constructor_copy(self):
        receipt = self.store.reserve("a", "r", [("x", 3)])
        self.assertEqual(receipt["items"], {"x": 3})
        self.assertEqual(receipt["status"], "reserved")
        self.assertEqual(self.store.stocks[("a", "x")], 7)
        self.assertEqual(self.original[("a", "x")], 10)

    def test_normalized_reordered_replay(self):
        first = self.store.reserve("a", "r", [("x", 1), ("y", 2), ("x", 2)])
        second = self.store.reserve("a", "r", [("y", 2), ("x", 3)])
        self.assertEqual(first, second)
        self.assertEqual(first["items"], {"x": 3, "y": 2})
        self.assertEqual(self.store.stocks[("a", "x")], 7)

    def test_conflicting_replay_preserves_state(self):
        self.store.reserve("a", "r", [("x", 2)])
        before = copy.deepcopy(vars(self.store))
        with self.assertRaises(CANDIDATE.ConflictError):
            self.store.reserve("a", "r", [("x", 3)])
        self.assertEqual(vars(self.store), before)

    def test_unknown_sku_is_atomic(self):
        before = copy.deepcopy(vars(self.store))
        with self.assertRaises(ValueError):
            self.store.reserve("a", "r", [("x", 2), ("missing", 1)])
        self.assertEqual(vars(self.store), before)

    def test_insufficient_stock_is_atomic(self):
        before = copy.deepcopy(vars(self.store))
        with self.assertRaises(ValueError):
            self.store.reserve("a", "r", [("x", 2), ("y", 9)])
        self.assertEqual(vars(self.store), before)

    def test_aggregate_cannot_oversell(self):
        before = copy.deepcopy(vars(self.store))
        with self.assertRaises(ValueError):
            self.store.reserve("a", "r", [("x", 6), ("x", 5)])
        self.assertEqual(vars(self.store), before)

    def test_tenant_request_isolation(self):
        self.store.reserve("a", "r", [("x", 2)])
        self.store.reserve("b", "r", [("x", 3)])
        self.assertEqual(self.store.stocks[("a", "x")], 8)
        self.assertEqual(self.store.stocks[("b", "x")], 5)
        self.store.release("a", "r")
        self.assertEqual(self.store.stocks[("b", "x")], 5)

    def test_separator_keys_do_not_collide(self):
        store = CANDIDATE.Inventory({("a:b", "x"): 9, ("a", "x"): 9})
        store.reserve("a:b", "c", [("x", 2)])
        store.reserve("a", "b:c", [("x", 3)])
        self.assertEqual(store.stocks, {("a:b", "x"): 7, ("a", "x"): 6})

    def test_release_restores_once(self):
        self.store.reserve("a", "r", [("x", 2), ("y", 1)])
        first = self.store.release("a", "r")
        second = self.store.release("a", "r")
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "released")
        self.assertEqual(self.store.stocks, self.original)

    def test_replay_after_release_does_not_reacquire(self):
        self.store.reserve("a", "r", [("x", 2)])
        self.store.release("a", "r")
        replay = self.store.reserve("a", "r", [("x", 2)])
        self.assertEqual(replay["status"], "released")
        self.assertEqual(self.store.stocks, self.original)

    def test_released_request_still_rejects_conflict(self):
        self.store.reserve("a", "r", [("x", 2)])
        self.store.release("a", "r")
        with self.assertRaises(CANDIDATE.ConflictError):
            self.store.reserve("a", "r", [("x", 3)])
        self.assertEqual(self.store.stocks, self.original)

    def test_reservation_receipt_is_detached(self):
        receipt = self.store.reserve("a", "r", [("x", 2)])
        receipt["items"]["x"] = 100
        receipt["status"] = "released"
        replay = self.store.reserve("a", "r", [("x", 2)])
        self.assertEqual(replay["items"], {"x": 2})
        self.assertEqual(replay["status"], "reserved")
        self.store.release("a", "r")
        self.assertEqual(self.store.stocks, self.original)

    def test_release_receipt_is_detached(self):
        self.store.reserve("a", "r", [("x", 2)])
        receipt = self.store.release("a", "r")
        receipt["items"]["x"] = 100
        receipt["status"] = "reserved"
        self.assertEqual(self.store.release("a", "r")["status"], "released")
        self.assertEqual(self.store.stocks, self.original)

    def test_unknown_release_is_isolated(self):
        self.store.reserve("a", "r", [("x", 2)])
        before = copy.deepcopy(vars(self.store))
        with self.assertRaises(KeyError):
            self.store.release("b", "r")
        self.assertEqual(vars(self.store), before)

    def test_invalid_quantities_are_atomic(self):
        for quantity in (True, False, 0, -1, 1.5, "2", None):
            with self.subTest(quantity=quantity):
                before = copy.deepcopy(vars(self.store))
                with self.assertRaises(ValueError):
                    self.store.reserve("a", "bad", [("x", 1), ("y", quantity)])
                self.assertEqual(vars(self.store), before)

    def test_empty_items_rejected(self):
        with self.assertRaises(ValueError):
            self.store.reserve("a", "r", [])
        self.assertEqual(self.store.stocks, self.original)
        self.assertEqual(self.store.requests, {})

    def test_invalid_identifiers_rejected(self):
        for tenant, request, sku in (("", "r", "x"), ("a", "", "x"), ("a", "r", ""),
                                     (None, "r", "x"), ("a", 3, "x"), ("a", "r", 7)):
            with self.subTest(tenant=tenant, request=request, sku=sku):
                with self.assertRaises(ValueError):
                    self.store.reserve(tenant, request, [(sku, 1)])
                self.assertEqual(self.store.stocks, self.original)

    def test_rejected_request_can_succeed(self):
        with self.assertRaises(ValueError):
            self.store.reserve("a", "r", [("x", 99)])
        receipt = self.store.reserve("a", "r", [("x", 2)])
        self.assertEqual(receipt["status"], "reserved")
        self.assertEqual(self.store.stocks[("a", "x")], 8)


class SortingChecks(unittest.TestCase):
    def setUp(self):
        self.rows = [{"id": "missing"}, {"id": "zero", "score": 0}, {"id": "low", "score": -2},
                     {"id": "none", "score": None}, {"id": "high", "score": 4},
                     {"id": "high2", "score": 4}]

    def ids(self, rows):
        return [row["id"] for row in rows]

    def test_default_ascending(self):
        self.assertEqual(self.ids(CANDIDATE.sort_rows(self.rows)),
                         ["low", "zero", "high", "high2", "missing", "none"])

    def test_descending_missing_last_and_stable(self):
        self.assertEqual(self.ids(CANDIDATE.sort_rows(self.rows, True)),
                         ["high", "high2", "zero", "low", "missing", "none"])

    def test_input_not_mutated(self):
        before = copy.deepcopy(self.rows)
        CANDIDATE.sort_rows(self.rows)
        CANDIDATE.sort_rows(self.rows, True)
        self.assertEqual(self.rows, before)

    def test_all_missing_stable(self):
        rows = [{"id": 1}, {"id": 2, "score": None}, {"id": 3}]
        self.assertEqual(CANDIDATE.sort_rows(rows, True), rows)

    def test_empty(self):
        self.assertEqual(CANDIDATE.sort_rows([]), [])

    def test_fractional_and_negative_values(self):
        rows = [{"id": n, "score": n} for n in (0, -0.25, 0.5, -3)]
        self.assertEqual(self.ids(CANDIDATE.sort_rows(rows)), [-3, -0.25, 0, 0.5])
        self.assertEqual(self.ids(CANDIDATE.sort_rows(rows, True)), [0.5, 0, -0.25, -3])


def evaluate(task, candidate):
    global CANDIDATE
    inspect_source(candidate.read_text())
    spec = importlib.util.spec_from_file_location("pilot_candidate", candidate)
    CANDIDATE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(CANDIDATE)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(InventoryChecks if task == "inventory" else SortingChecks)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream).run(suite)
    return {"task": task, "checks": result.testsRun, "failure_count": len(result.failures),
            "error_count": len(result.errors), "passed": result.wasSuccessful(),
            "failures": [{"test": str(test), "trace": trace} for test, trace in result.failures + result.errors],
            "summary": stream.getvalue()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("inventory", "sorting"), required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = evaluate(args.task, args.candidate.resolve())
    except Exception as error:
        result = {"task": args.task, "passed": False, "load_error": str(error)}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
