import tempfile
import unittest
from pathlib import Path
from csv_import.store import Store
from csv_import.runner import Runner
from csv_import.presenter import render


class HappyPath(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "data.csv"
        self.source.write_text("record_id,value\none,first\ntwo,second\n", encoding="utf-8")
        self.store = Store(self.root / "store.db")

    def test_import(self):
        result = Runner(self.store).run("a", "job", self.source)
        self.assertEqual(result["next_row"], 2)
        self.assertEqual(len(self.store.records("a")), 2)
        self.assertEqual(render(result)["status"], "complete")

    def test_replay(self):
        runner = Runner(self.store)
        runner.run("a", "job", self.source)
        self.assertEqual(runner.run("a", "job", self.source)["state"], "complete")
        self.assertEqual(len(self.store.records("a")), 2)


if __name__ == "__main__":
    unittest.main()
