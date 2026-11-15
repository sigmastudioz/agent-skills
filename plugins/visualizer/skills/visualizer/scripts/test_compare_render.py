#!/usr/bin/env python3
"""Tests for compare_render.py. By Lex from SigmaStudioz. Run from this folder: python3 -m unittest"""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compare_render  # noqa: E402


def to_srgb(linear):
    linear = np.clip(linear, 0, 1)
    return np.where(linear <= .0031308, linear * 12.92, 1.055 * linear ** (1 / 2.4) - .055)


def picture(scale=1.0, size=(120, 80)):
    """A left-to-right ramp in linear light with a dark strip along the bottom."""
    width, height = size
    linear = np.tile(np.linspace(.08, .6, width), (height, 1))
    linear[int(height * .9):] = .0005
    return np.repeat(to_srgb(linear * scale)[..., None], 3, axis=2)


def save(array, path):
    Image.fromarray((np.clip(array, 0, 1) * 255).round().astype(np.uint8)).save(path)
    return path


class CompareTests(unittest.TestCase):
    def test_identical_pictures_pass_with_unit_ratios(self):
        report = compare_render.compare(picture(), picture(), compare_render.grid_regions(4, 3))
        self.assertTrue(report['passed'])
        self.assertEqual(report['mean_abs_difference_of_255'], 0)
        self.assertTrue(all(row['ratio'] in (1.0, None) for row in report['regions']))

    def test_ratio_is_measured_in_linear_light(self):
        # 0.3 of the light is far more than 0.3 of the screen value; the report must say 0.3.
        report = compare_render.compare(picture(.3), picture(), compare_render.grid_regions(2, 1))
        self.assertFalse(report['passed'])
        self.assertAlmostEqual(report['regions'][0]['ratio'], .3, delta=.02)
        self.assertAlmostEqual(report['overall_luminance_ratio'], .3, delta=.02)

    def test_one_wrong_region_fails_and_is_named(self):
        candidate = picture()
        candidate[:40, 60:] = to_srgb(compare_render.to_linear(candidate[:40, 60:]) * 1.5)
        regions = [{'name': 'left', 'x': 0, 'y': 0, 'w': .5, 'h': .5}, {'name': 'right', 'x': .5, 'y': 0, 'w': .5, 'h': .5}]
        report = compare_render.compare(candidate, picture(), regions)
        self.assertEqual(report['failed_regions'], ['right'])
        self.assertEqual(report['worst_region'], 'right')
        self.assertAlmostEqual(report['regions'][1]['ratio'], 1.5, delta=.03)

    def test_tolerance_is_the_boundary(self):
        regions = compare_render.grid_regions(1, 1)
        self.assertTrue(compare_render.compare(picture(1.08), picture(), regions, .10)['passed'])
        self.assertFalse(compare_render.compare(picture(1.14), picture(), regions, .10)['passed'])

    def test_dark_regions_are_judged_by_difference_not_ratio(self):
        region = [{'name': 'strip', 'x': 0, 'y': .92, 'w': 1, 'h': .08}]
        report = compare_render.compare(picture(), picture(), region)
        self.assertIsNone(report['regions'][0]['ratio'])
        self.assertEqual(report['regions'][0]['judged_by'], 'difference')
        self.assertTrue(report['passed'])
        bright = picture()
        bright[74:] = .5
        self.assertFalse(compare_render.compare(bright, picture(), region)['passed'])

    def test_rejects_bad_regions_and_grids(self):
        for regions in ([], [{'name': 'a', 'x': .5, 'y': 0, 'w': .6, 'h': .2}], [{'name': '', 'x': 0, 'y': 0, 'w': 1, 'h': 1}],
                        [{'name': 'a', 'x': 0, 'y': 0, 'w': 1, 'h': 1}] * 2, [{'name': 'a', 'x': 'left', 'y': 0, 'w': 1, 'h': 1}]):
            with self.subTest(regions=regions), self.assertRaises(ValueError):
                compare_render.named_regions(regions)
        for grid in ('4', '0x3', '4x40', 'axb'):
            with self.subTest(grid=grid), self.assertRaises(ValueError):
                compare_render.parse_grid(grid)


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.reference = save(picture(), self.tmp / 'reference.png')

    def test_writes_report_and_sheet_and_exits_by_result(self):
        good = save(picture(1.03), self.tmp / 'good.png')
        bad = save(picture(.5), self.tmp / 'bad.png')
        report, sheet = self.tmp / 'out' / 'report.json', self.tmp / 'out' / 'sheet.png'
        self.assertEqual(compare_render.main([str(good), str(self.reference), '--report', str(report), '--sheet', str(sheet)]), 0)
        data = json.loads(report.read_text())
        self.assertTrue(data['passed'])
        self.assertEqual(len(data['candidate_sha256']), 64)
        self.assertEqual(data['regions_source'], 'grid 4x3')
        with Image.open(sheet) as image:
            self.assertGreater(image.width, image.height * 3)
        self.assertEqual(compare_render.main([str(bad), str(self.reference)]), 1)

    def test_refuses_different_sizes_transparency_and_existing_outputs(self):
        small = save(picture(size=(60, 40)), self.tmp / 'small.png')
        with self.assertRaises(ValueError) as caught:
            compare_render.main([str(small), str(self.reference)])
        self.assertIn('Sizes differ', str(caught.exception))
        clear = self.tmp / 'clear.png'
        Image.new('RGBA', (120, 80), (10, 10, 10, 0)).save(clear)
        with self.assertRaises(ValueError) as caught:
            compare_render.main([str(clear), str(self.reference)])
        self.assertIn('transparent', str(caught.exception))
        existing = self.tmp / 'report.json'
        existing.write_text('{}')
        with self.assertRaises(ValueError):
            compare_render.main([str(save(picture(), self.tmp / 'again.png')), str(self.reference), '--report', str(existing)])
        with self.assertRaises(ValueError) as caught:
            compare_render.main([str(self.reference), str(self.reference)])
        self.assertIn('Paths must differ', str(caught.exception))

    def test_named_regions_file(self):
        regions = self.tmp / 'regions.json'
        regions.write_text(json.dumps([{'name': 'floor', 'x': 0, 'y': .5, 'w': 1, 'h': .3}]))
        report = self.tmp / 'r.json'
        same = save(picture(), self.tmp / 'same.png')
        self.assertEqual(compare_render.main([str(same), str(self.reference), '--regions', str(regions), '--report', str(report)]), 0)
        self.assertEqual([row['name'] for row in json.loads(report.read_text())['regions']], ['floor'])


if __name__ == '__main__':
    unittest.main()
