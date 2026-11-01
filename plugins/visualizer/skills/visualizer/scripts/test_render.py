#!/usr/bin/env python3
"""Tests for render.py (standard-library unittest only). By Lex from SigmaStudioz.

Run from this folder: python3 -m unittest
"""
import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
STORYBOARDS_DOC = HERE.parent / 'references' / 'storyboards.md'
FONT = Path(os.environ.get('VISUALIZER_TEST_FONT') or next((p for p in [
    '/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/SourceSansPro-Semibold.otf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'] if Path(p).is_file()), '/missing-font'))
MONO = Path(os.environ.get('VISUALIZER_TEST_MONO_FONT') or next((p for p in [
    '/System/Library/Fonts/Supplemental/Courier New.ttf', '/System/Library/Fonts/Menlo.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'] if Path(p).is_file()), '/missing-mono-font'))
SIZE_MESSAGE = 'Output dimensions must be even and between 640 and 3840 pixels'

try:
    import PIL  # noqa: F401
    HAVE_PILLOW = True
except ImportError:
    HAVE_PILLOW = False

if HAVE_PILLOW:
    sys.path.insert(0, str(HERE))
    try:
        import render
    finally:
        sys.path.pop(0)
else:  # render.py imports Pillow at module level, so nothing here can run without it.
    raise unittest.SkipTest('Pillow is not installed; see scripts/requirements.txt')


def example_scene():
    """The documented example scene, parsed from references/storyboards.md so docs and tests agree."""
    text = STORYBOARDS_DOC.read_text(encoding='utf-8')
    blocks = re.findall(r'```json\n(.*?)\n```', text, flags=re.S)
    scenes = [json.loads(b) for b in blocks if '"kind"' in b]
    assert scenes, 'storyboards.md no longer contains a JSON example scene'
    return scenes[0]


def storyboard(*scenes):
    return {'brand': 'SIGMASTUDIOZ', 'author': 'Lex from SigmaStudioz', 'scenes': list(scenes)}


class ValidateTests(unittest.TestCase):
    def test_accepts_documented_example_scene(self):
        render.validate(storyboard(example_scene()))  # must not raise

    def assert_rejects(self, data, message):
        with self.assertRaises(ValueError) as caught:
            render.validate(data)
        self.assertIn(message, str(caught.exception))

    def test_rejects_duplicate_scene_id(self):
        scene = example_scene()
        self.assert_rejects(storyboard(scene, copy.deepcopy(scene)), 'Duplicate scene ID')

    def test_rejects_undefined_edge_endpoint(self):
        scene = example_scene()
        scene['edges'] = [{'from': 'in', 'to': 'missing'}]
        self.assert_rejects(storyboard(scene), 'Undefined edge endpoint')

    def test_rejects_duration_outside_bounds(self):
        for duration in (1.9, 0, -5, 30.5, True):
            scene = example_scene(); scene['duration'] = duration
            with self.subTest(duration=duration):
                self.assert_rejects(storyboard(scene), 'Duration must be 2–30s')

    def test_accepts_duration_bounds_inclusive(self):
        for duration in (2, 30):
            scene = example_scene(); scene['duration'] = duration
            render.validate(storyboard(scene))

    def test_rejects_total_runtime_over_300_seconds(self):
        scenes = []
        for i in range(11):  # 11 × 30 s = 330 s, within the 60-scene cap
            scene = example_scene(); scene['id'] = f'flow-{i}'; scene['duration'] = 30
            scenes.append(scene)
        self.assert_rejects(storyboard(*scenes), 'Maximum runtime is 300 seconds')
        render.validate(storyboard(*scenes[:10]))  # exactly 300 s is allowed


class SizeRuleTests(unittest.TestCase):
    def assert_rejects(self, text):
        with self.assertRaises(ValueError) as caught:
            render.parse_size(text)
        self.assertEqual(str(caught.exception), SIZE_MESSAGE)

    def test_rejects_540x960_with_range_message(self):
        self.assert_rejects('540x960')

    def test_rejects_odd_width(self):
        self.assert_rejects('721x1280')

    def test_rejects_odd_height_and_oversize(self):
        self.assert_rejects('1080x1921')
        self.assert_rejects('3842x2160')

    def test_accepts_even_sizes_in_range(self):
        self.assertEqual(render.parse_size('720x1280'), (720, 1280))
        self.assertEqual(render.parse_size('640x640'), (640, 640))
        self.assertEqual(render.parse_size('3840x2160'), (3840, 2160))

    def test_rejects_malformed_size_text(self):
        for text in ('1080', '1080x', 'ax1920', '1080x1920x3', '-720x1280'):
            with self.subTest(text=text), self.assertRaises(ValueError) as caught:
                render.parse_size(text)
            self.assertIn('WIDTHxHEIGHT', str(caught.exception))


@unittest.skipUnless(FONT.is_file() and MONO.is_file(), 'supply VISUALIZER_TEST_FONT and VISUALIZER_TEST_MONO_FONT')
class CommandLineTests(unittest.TestCase):
    """--validate-only never starts FFmpeg, so these cases need only Pillow and the fonts."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='viz-test-'))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.board = self.tmp / 'storyboard.json'
        self.board.write_text(json.dumps(storyboard(example_scene())), encoding='utf-8')

    def run_render(self, *extra):
        return subprocess.run([sys.executable, str(HERE / 'render.py'), str(self.board),
                               '--font', str(FONT), '--mono-font', str(MONO), '--validate-only', *extra],
                              capture_output=True, text=True, timeout=120)

    def test_validate_only_succeeds_at_720x1280(self):
        proc = self.run_render('--size', '720x1280')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), {'scenes': 1, 'seconds': 5, 'layout': '720x1280'})

    def test_validate_only_reports_size_rule_for_540x960(self):
        proc = self.run_render('--size', '540x960')
        self.assertEqual(proc.returncode, 1)
        self.assertIn(SIZE_MESSAGE, proc.stderr)
        self.assertNotIn('Invalid even output dimensions', proc.stderr)


if __name__ == '__main__':
    unittest.main()
