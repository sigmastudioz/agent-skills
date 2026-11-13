"""Public contracts for the maintained album sequence implementation."""
import copy
import unittest
from music.sequence import propose_sequence, validate_album_order


class SequenceTests(unittest.TestCase):
    def setUp(self):
        self.tracks = [dict(id='intro', head_rms_dbfs=-30, tail_rms_dbfs=-20),
                       dict(id='a', head_rms_dbfs=-20, tail_rms_dbfs=-12),
                       dict(id='b', head_rms_dbfs=-12, tail_rms_dbfs=-25),
                       dict(id='end', head_rms_dbfs=-25, tail_rms_dbfs=-30)]

    def test_kept_block_and_pins(self):
        result = propose_sequence(self.tracks, 'intro', 'end', [['intro', 'a']])
        self.assertEqual(result['technical_flow_proposal'], ['intro', 'a', 'b', 'end'])
        self.assertEqual(result['original_order'], ['intro', 'a', 'b', 'end'])

    def test_constraints_reject_conflicts(self):
        for args in [('intro', 'intro', None), ('a', None, [['intro', 'a']]),
                     ('intro', 'end', [['intro', 'end']]), (None, None, [['a', 'a']])]:
            with self.assertRaises(ValueError):
                propose_sequence(self.tracks, *args)

    def test_single_track_and_unknown_levels(self):
        self.assertEqual(propose_sequence([{'id': 'x'}], 'x', 'x')['technical_flow_proposal'], ['x'])
        self.assertEqual(propose_sequence([{'id': 'a'}, {'id': 'b'}])['technical_flow_proposal'], ['a', 'b'])

    def test_does_not_mutate_inputs(self):
        original = copy.deepcopy(self.tracks)
        groups = [['a', 'b']]
        propose_sequence(self.tracks, keep_together=groups)
        self.assertEqual(self.tracks, original)
        self.assertEqual(groups, [['a', 'b']])

    def test_editorial_validation_and_rejection(self):
        constraints = dict(opener='intro', closer='end', keep_together=[['a', 'b']])
        self.assertIsNone(validate_album_order(['intro', 'a', 'b', 'end'], self.tracks, constraints))
        for order in [['a', 'b', 'intro', 'end'], ['intro', 'b', 'a', 'end'], ['intro', 'a', 'end']]:
            with self.assertRaises(ValueError):
                validate_album_order(order, self.tracks, constraints)


if __name__ == '__main__':
    unittest.main()
