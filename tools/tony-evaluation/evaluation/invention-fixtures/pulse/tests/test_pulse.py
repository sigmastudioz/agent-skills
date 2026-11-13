import unittest
from pulse.engine import analyze
from pulse.report import build


class PublicChecks(unittest.TestCase):
    def test_small_metrics(self):
        self.assertEqual(analyze({"values":[3,-2,5]}), dict(count=3,sum=6,first=3,last=5,minimum=-2,maximum=5,drawdown=5,rise=2))

    def test_repeat_report(self):
        self.assertEqual(build({"repeat":2,"body":{"values":[1,2]}})["preview"], [1,2,1,2])

    def test_empty(self):
        self.assertEqual(analyze({"values":[]})["rise"], 0)
