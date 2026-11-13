#!/usr/bin/env python3
"""Held-out behavioral checks for the tool-enabled coding trial; never copied to workers."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import csv
import io
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest

CANDIDATE = None


class RelayChecks(unittest.TestCase):
    def setUp(self):
        from relay.queue import Queue
        from relay.delivery import Sink
        from relay.worker import Worker
        self.Queue, self.Sink, self.Worker = Queue, Sink, Worker
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.qpath, self.spath = self.root / "queue.db", self.root / "sink.db"
        self.q, self.sink = Queue(self.qpath), Sink(self.spath)

    def add(self, tenant="a", key="r", payload="hello"):
        return self.q.enqueue(tenant, key, payload)

    def test_expired_ack_is_rejected(self):
        identity = self.add()
        job = self.q.claim(0, 10)
        self.assertFalse(self.q.ack(identity, job["lease_token"], 10))
        self.assertNotEqual(self.q.jobs()[0]["state"], "done")

    def test_reclaimed_owner_cannot_ack(self):
        identity = self.add()
        old = self.q.claim(0, 10)
        new = self.q.claim(10, 10)
        self.assertNotEqual(old["lease_token"], new["lease_token"])
        self.assertFalse(self.q.ack(identity, old["lease_token"], 11))
        self.assertEqual(self.q.jobs()[0]["state"], "leased")
        self.assertTrue(self.q.ack(identity, new["lease_token"], 11))

    def test_reclaimed_owner_cannot_release(self):
        identity = self.add()
        old = self.q.claim(0, 10)
        new = self.q.claim(10, 10)
        self.assertFalse(self.q.release(identity, old["lease_token"]))
        self.assertEqual(self.q.jobs()[0]["lease_token"], new["lease_token"])

    def test_current_release_is_boolean_and_retryable(self):
        identity = self.add()
        job = self.q.claim(0, 10)
        self.assertTrue(self.q.release(identity, job["lease_token"]))
        self.assertFalse(self.q.release(identity, job["lease_token"]))
        again = self.q.claim(1, 10)
        self.assertEqual(again["attempts"], 2)

    def test_duplicate_ack_does_not_mutate_done(self):
        identity = self.add()
        job = self.q.claim(0, 10)
        self.assertTrue(self.q.ack(identity, job["lease_token"], 1))
        self.assertFalse(self.q.ack(identity, job["lease_token"], 2))
        self.assertEqual(self.q.jobs()[0]["state"], "done")

    def test_unknown_ownership_is_rejected(self):
        self.assertFalse(self.q.ack(999, "wrong", 0))
        self.assertFalse(self.q.release(999, "wrong"))

    def test_nonpositive_ttl_preserves_pending(self):
        self.add()
        for ttl in (0, -2):
            with self.subTest(ttl=ttl):
                with self.assertRaises(ValueError):
                    self.q.claim(0, ttl)
                self.assertEqual(self.q.jobs()[0]["attempts"], 0)

    def test_concurrent_claim_has_one_owner(self):
        self.add()
        barrier = threading.Barrier(10)
        def claim(_):
            q = self.Queue(self.qpath)
            barrier.wait(timeout=10)
            return q.claim(0, 30)
        with ThreadPoolExecutor(max_workers=10) as pool:
            jobs = list(pool.map(claim, range(10)))
        self.assertEqual(sum(job is not None for job in jobs), 1)
        self.assertEqual(self.q.jobs()[0]["attempts"], 1)

    def test_failed_delivery_is_not_done_and_recovers(self):
        self.add()
        class Broken:
            def deliver(self, *args):
                raise OSError("synthetic provider unavailable")
        with self.assertRaises(OSError):
            self.Worker(self.q, Broken()).tick(0, ttl=10)
        self.assertNotEqual(self.q.jobs()[0]["state"], "done")
        self.Worker(self.Queue(self.qpath), self.Sink(self.spath)).tick(11, ttl=10)
        self.assertEqual(self.q.jobs()[0]["state"], "done")
        self.assertEqual(len(self.sink.messages()), 1)

    def test_interrupted_after_send_replays_without_duplicate(self):
        self.add()
        def interrupt(_):
            raise RuntimeError("synthetic process interruption")
        with self.assertRaises(RuntimeError):
            self.Worker(self.q, self.sink).tick(0, ttl=10, after_send=interrupt)
        self.Worker(self.Queue(self.qpath), self.Sink(self.spath)).tick(11, ttl=10)
        self.assertEqual(len(self.sink.messages()), 1)
        self.assertEqual(self.q.jobs()[0]["state"], "done")

    def test_old_worker_after_send_cannot_finish_replacement(self):
        identity = self.add()
        replacement = []
        def replace(_):
            replacement.append(self.Queue(self.qpath).claim(20, 30))
        self.Worker(self.q, self.sink).tick(0, ttl=10, after_send=replace)
        self.assertIsNotNone(replacement[0])
        self.assertEqual(self.q.jobs()[0]["state"], "leased")
        self.assertTrue(self.q.ack(identity, replacement[0]["lease_token"], 21))

    def test_provider_identity_is_collision_free(self):
        self.sink.deliver("a:b", "c", "first")
        self.sink.deliver("a", "b:c", "second")
        actual = {(row["tenant"], row["request_key"], row["payload"]) for row in self.sink.messages()}
        self.assertEqual(actual, {("a:b", "c", "first"), ("a", "b:c", "second")})

    def test_legacy_provider_rows_replay_without_loss(self):
        path = self.root / "legacy.db"
        db = sqlite3.connect(path)
        db.execute("CREATE TABLE messages(delivery_key TEXT PRIMARY KEY,tenant TEXT NOT NULL,request_key TEXT NOT NULL,payload TEXT NOT NULL)")
        db.execute("INSERT INTO messages VALUES('a:b:c','a:b','c','old')")
        db.commit()
        db.close()
        sink = self.Sink(path)
        sink.deliver("a:b", "c", "old")
        sink.deliver("a", "b:c", "new")
        self.assertEqual(len(sink.messages()), 2)
        self.assertEqual({r["payload"] for r in sink.messages()}, {"old", "new"})

    def test_queue_and_provider_tenant_replays(self):
        first = self.add("a", "same", "one")
        self.assertEqual(first, self.add("a", "same", "one"))
        with self.assertRaises(ValueError):
            self.add("a", "same", "changed")
        self.add("b", "same", "two")
        worker = self.Worker(self.q, self.sink)
        worker.tick(0)
        worker.tick(0)
        self.assertEqual(len(self.sink.messages()), 2)

    def test_cli_reopens_the_terminal_result(self):
        base = [sys.executable, "-m", "relay.cli", "--queue", str(self.qpath), "--sink", str(self.spath)]
        subprocess.run(base + ["enqueue", "a", "cli", "payload"], cwd=CANDIDATE, check=True, capture_output=True, timeout=15)
        subprocess.run(base + ["work", "--now", "0"], cwd=CANDIDATE, check=True, capture_output=True, timeout=15)
        result = subprocess.run(base + ["show"], cwd=CANDIDATE, check=True, capture_output=True, text=True, timeout=15)
        view = json.loads(result.stdout)
        self.assertEqual(view["jobs"][0]["state"], "done")
        self.assertEqual(view["messages"][0]["payload"], "payload")


class ImportChecks(unittest.TestCase):
    def setUp(self):
        from csv_import.store import Store
        from csv_import.runner import Runner
        from csv_import.presenter import render
        self.Store, self.Runner, self.render = Store, Runner, render
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / "store.db"
        self.source = self.root / "input.csv"
        self.write_source([(str(n), "value" + str(n)) for n in range(1, 6)])
        self.store = Store(self.path)

    def write_source(self, rows):
        with self.source.open("w", encoding="utf-8", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(["record_id", "value"])
            writer.writerows(rows)

    def fail_on(self, identity):
        def stop(row):
            if row["record_id"] == identity:
                raise RuntimeError("synthetic interruption")
        return stop

    def interrupted(self, identity="3"):
        with self.assertRaises(RuntimeError):
            self.Runner(self.store).run("a", "job", self.source, 2, self.fail_on(identity))

    def test_current_batch_is_atomic(self):
        self.interrupted("1")
        self.assertEqual(self.store.get_run("a", "job")["next_row"], 0)
        self.assertEqual(self.store.records("a"), [])

    def test_prior_batches_survive_current_failure(self):
        self.interrupted()
        self.assertEqual(self.store.get_run("a", "job")["next_row"], 2)
        self.assertEqual({r["record_id"] for r in self.store.records("a")}, {"1", "2"})

    def test_restart_resumes_without_skipping(self):
        self.interrupted()
        store = self.Store(self.path)
        result = self.Runner(store).run("a", "job", self.source, 2)
        self.assertEqual(result["state"], "complete")
        self.assertEqual(result["next_row"], 5)
        self.assertEqual({r["record_id"] for r in store.records("a")}, {"1", "2", "3", "4", "5"})

    def test_hard_process_exit_rolls_back_current_batch(self):
        code = """import os,sys
from pathlib import Path
from csv_import.store import Store
from csv_import.runner import Runner
def stop(row):
    if row['record_id']=='3': os._exit(27)
Runner(Store(sys.argv[1])).run('a','job',Path(sys.argv[2]),2,stop)
"""
        result = subprocess.run([sys.executable, "-c", code, str(self.path), str(self.source)],
                                cwd=CANDIDATE, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 27)
        reopened = self.Store(self.path)
        self.assertEqual(reopened.get_run("a", "job")["next_row"], 2)
        self.assertEqual(len(reopened.records("a")), 2)

    def test_changed_source_is_rejected_without_mutation(self):
        self.interrupted()
        before_run = self.store.get_run("a", "job")
        before_rows = self.store.records("a")
        self.write_source([("1", "changed"), ("2", "other")])
        with self.assertRaises(ValueError):
            self.Runner(self.Store(self.path)).run("a", "job", self.source)
        self.assertEqual(self.store.get_run("a", "job"), before_run)
        self.assertEqual(self.store.records("a"), before_rows)

    def test_identical_moved_source_can_resume(self):
        self.interrupted()
        moved = self.root / "moved.csv"
        self.source.rename(moved)
        store = self.Store(self.path)
        self.Runner(store).run("a", "job", moved)
        self.assertEqual(len(store.records("a")), 5)

    def test_csv_preserves_unicode_and_embedded_newline(self):
        self.write_source([("a", "café, snow ☃"), ("b", "first\nsecond"), ("c", "end")])
        self.Runner(self.store).run("a", "job", self.source, 1)
        actual = {r["record_id"]: r["value"] for r in self.store.records("a")}
        self.assertEqual(actual, {"a": "café, snow ☃", "b": "first\nsecond", "c": "end"})

    def test_logical_row_resume_with_multiline_value(self):
        self.write_source([("1", "first\nsecond"), ("2", "middle"), ("3", "last")])
        self.interrupted("2")
        store = self.Store(self.path)
        self.Runner(store).run("a", "job", self.source, 2)
        self.assertEqual({r["record_id"]: r["value"] for r in store.records("a")},
                         {"1": "first\nsecond", "2": "middle", "3": "last"})

    def test_duplicate_identical_record_counts_logical_rows(self):
        self.write_source([("1", "same"), ("1", "same"), ("2", "new")])
        result = self.Runner(self.store).run("a", "job", self.source, 2)
        self.assertEqual(result["next_row"], 3)
        self.assertEqual(len(self.store.records("a")), 2)

    def test_conflicting_record_preserves_original_and_batch(self):
        self.store.write_record("a", "x", "original")
        self.write_source([("fresh", "new"), ("x", "different")])
        with self.assertRaises(ValueError):
            self.Runner(self.store).run("a", "job", self.source, 2)
        self.assertEqual(self.store.records("a"), [{"tenant": "a", "record_id": "x", "value": "original"}])
        self.assertEqual(self.store.get_run("a", "job")["next_row"], 0)

    def test_store_binding_is_immutable(self):
        first = self.store.start("a", "job", "identity-one")
        with self.assertRaises(ValueError):
            self.store.start("a", "job", "identity-two")
        self.assertEqual(self.store.get_run("a", "job"), first)

    def test_same_run_id_is_tenant_scoped(self):
        self.Runner(self.store).run("a", "job", self.source)
        other = self.root / "other.csv"
        other.write_text("record_id,value\nx,other\n", encoding="utf-8")
        result = self.Runner(self.store).run("b", "job", other)
        self.assertEqual(result["tenant"], "b")
        self.assertEqual(len(self.store.records("b")), 1)
        self.assertEqual(self.store.get_run("a", "job")["next_row"], 5)

    def test_unknown_tenant_cannot_read_other_run(self):
        self.store.start("a", "job", "identity")
        self.assertIsNone(self.store.get_run("other", "job"))

    def test_incomplete_presenter_is_not_terminal(self):
        self.interrupted()
        self.assertNotEqual(self.render(self.store.get_run("a", "job"))["status"], "complete")

    def test_empty_input_is_complete_with_zero_progress(self):
        self.write_source([])
        result = self.Runner(self.store).run("a", "job", self.source)
        self.assertEqual(self.render(result)["status"], "complete")
        self.assertEqual(self.render(result)["processed"], 0)

    def test_invalid_batch_size_is_rejected(self):
        self.write_source([])
        with self.assertRaises(ValueError):
            self.Runner(self.store).run("a", "job", self.source, 0)

    def test_complete_replay_is_unchanged(self):
        first = self.Runner(self.store).run("a", "job", self.source)
        rows = self.store.records("a")
        second = self.Runner(self.Store(self.path)).run("a", "job", self.source)
        self.assertEqual(first, second)
        self.assertEqual(self.store.records("a"), rows)

    def test_cli_reopens_durable_result(self):
        base = [sys.executable, "-m", "csv_import.cli", "--db", str(self.path)]
        subprocess.run(base + ["run", "a", "job", str(self.source), "--batch-size", "2"],
                       cwd=CANDIDATE, capture_output=True, check=True, timeout=15)
        result = subprocess.run(base + ["show", "a", "job"], cwd=CANDIDATE,
                                capture_output=True, text=True, check=True, timeout=15)
        self.assertEqual(json.loads(result.stdout), {"tenant": "a", "run_id": "job", "status": "complete", "processed": 5})


def evaluate(task, candidate):
    global CANDIDATE
    CANDIDATE = candidate.resolve()
    sys.path.insert(0, str(CANDIDATE))
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RelayChecks if task == "relay" else ImportChecks)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    failed_methods = sorted({str(test).split()[0] for test, _ in result.failures + result.errors})
    return {"task": task, "checks": result.testsRun, "failures": len(result.failures),
            "errors": len(result.errors), "passed": result.wasSuccessful(),
            "failed_checks": failed_methods, "passed_checks": result.testsRun - len(failed_methods),
            "failed_cases": [{"test": str(t), "trace": trace} for t, trace in result.failures + result.errors],
            "summary": stream.getvalue()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("relay", "importer"), required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.task, args.candidate), indent=2))


if __name__ == "__main__":
    main()
