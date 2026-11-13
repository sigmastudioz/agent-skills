import unittest
from windows.model import Series
from windows.engine import first_overlap
from windows.planner import plan


class PublicChecks(unittest.TestCase):
    def test_small_overlap(self):
        self.assertEqual(first_overlap(Series(0,10,2,10), Series(1,15,1,5), 0,100), 1)

    def test_touch_and_empty(self):
        self.assertIsNone(first_overlap(Series(0,10,2,1), Series(2,10,1,1), 0,10))
        self.assertIsNone(first_overlap(Series(0,10,2,0), Series(1,15,1,5), 0,100))

    def test_plan(self):
        self.assertEqual(plan({"lower":0,"upper":10,"schedules":[]}), {"conflicts":[]})
