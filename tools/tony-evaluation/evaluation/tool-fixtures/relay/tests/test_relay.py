import tempfile
import unittest
from pathlib import Path
from relay.queue import Queue
from relay.delivery import Sink
from relay.worker import Worker


class HappyPath(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.queue = Queue(self.root / "queue.db")
        self.sink = Sink(self.root / "sink.db")

    def test_delivery(self):
        self.queue.enqueue("a", "r", "hello")
        self.assertTrue(Worker(self.queue, self.sink).tick(0))
        self.assertEqual(self.queue.jobs()[0]["state"], "done")
        self.assertEqual(self.sink.messages()[0]["payload"], "hello")

    def test_empty(self):
        self.assertFalse(Worker(self.queue, self.sink).tick(0))

    def test_enqueue_replay(self):
        first = self.queue.enqueue("a", "r", "hello")
        self.assertEqual(first, self.queue.enqueue("a", "r", "hello"))


if __name__ == "__main__":
    unittest.main()
