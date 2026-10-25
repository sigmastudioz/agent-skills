"""Behavior checks for the real renderer; all outputs stay in temporary directories."""
import copy
import os
import shutil
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'plugins/visualizer/skills/visualizer/scripts/render.py'
spec = importlib.util.spec_from_file_location('renderer', SCRIPT)
render = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(render)
except ModuleNotFoundError as error:
    if error.name == 'PIL': raise unittest.SkipTest('Pillow is required for renderer behavior tests')
    raise
BOARD = {"brand":"SIGMASTUDIOZ","author":"Lex from SigmaStudioz","scenes":[{"id":"flow","duration":2,"kind":"graph","eyebrow":"01 / EXPLAIN","title":"Signal","body":"A connected path.","caption":"Trace the path.","nodes":[{"id":"in","label":"Input","x":0.2,"y":0.25},{"id":"out","label":"Result","x":0.8,"y":0.7}],"edges":[{"from":"in","to":"out"}]}]}
FONT = os.environ.get('VISUALIZER_TEST_FONT') or next((p for p in ['/Library/Fonts/SourceSansPro-Semibold.otf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'] if Path(p).is_file()), '')
MONO = os.environ.get('VISUALIZER_TEST_MONO_FONT') or next((p for p in ['/System/Library/Fonts/Menlo.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'] if Path(p).is_file()), '')


class RendererBehavior(unittest.TestCase):
    def run_cli(self, board, directory, *extra):
        source = directory/'source.json'; source.write_text(json.dumps(board))
        return subprocess.run([sys.executable, str(SCRIPT), str(source), '--font', FONT,
            '--mono-font', MONO, '--size', '720x1280', *extra], capture_output=True, text=True)

    def test_missing_edge_is_rejected(self):
        board = copy.deepcopy(BOARD); board['scenes'][0]['edges'][0]['to'] = 'missing'
        with self.assertRaisesRegex(ValueError, 'Undefined edge'): render.validate(board)

    def test_nonfinite_timing_is_rejected(self):
        board = copy.deepcopy(BOARD); board['scenes'][0]['duration'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'Duration'): render.validate(board)

    def test_duplicate_nodes_are_rejected(self):
        board = copy.deepcopy(BOARD); board['scenes'][0]['nodes'][1]['id'] = 'in'
        with self.assertRaisesRegex(ValueError, 'Duplicate'): render.validate(board)

    def test_invalid_graph_coordinates_are_rejected(self):
        board = copy.deepcopy(BOARD); board['scenes'][0]['nodes'][0]['x'] = float('inf')
        with self.assertRaisesRegex(ValueError, 'coordinates'): render.validate(board)

    @unittest.skipUnless(FONT and MONO and shutil.which("ffmpeg") and shutil.which("ffprobe"), "Fonts and FFmpeg/ffprobe are required")
    def test_text_overflow_fails_before_export(self):
        board = copy.deepcopy(BOARD); board['scenes'][0]['title'] = 'longword'*30
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); output = p/'never.mp4'
            result = self.run_cli(board, p, '--output', str(output))
            self.assertNotEqual(result.returncode, 0); self.assertFalse(output.exists())
            self.assertIn('overflows', result.stderr)

    @unittest.skipUnless(FONT and MONO and shutil.which("ffmpeg") and shutil.which("ffprobe"), "Fonts and FFmpeg/ffprobe are required")
    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); output = p/'existing.mp4'; output.write_bytes(b'keep')
            result = self.run_cli(BOARD, p, '--output', str(output))
            self.assertNotEqual(result.returncode, 0); self.assertEqual(output.read_bytes(), b'keep')

    @unittest.skipUnless(FONT and MONO and shutil.which("ffmpeg") and shutil.which("ffprobe"), "Fonts and FFmpeg/ffprobe are required")
    def test_source_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            result = self.run_cli(BOARD, p, '--output', str(p/'source.json'), '--overwrite')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads((p/'source.json').read_text()), BOARD)

    @unittest.skipUnless(FONT and MONO and shutil.which("ffmpeg") and shutil.which("ffprobe"), "Fonts and FFmpeg/ffprobe are required")
    def test_non_frame_aligned_duration_is_rejected(self):
        board = copy.deepcopy(BOARD); board['scenes'][0]['duration'] = 2.01
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(board, Path(tmp), '--validate-only')
            self.assertNotEqual(result.returncode, 0); self.assertIn('align to frames', result.stderr)

    @unittest.skipUnless(FONT and MONO and shutil.which("ffmpeg") and shutil.which("ffprobe"), "Fonts and FFmpeg/ffprobe are required")
    def test_real_encode_has_frames_audio_captions_and_poster(self):
        board = copy.deepcopy(BOARD); board['scenes'] = board['scenes'][:1]
        board['scenes'][0]['duration'] = 2
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); output = p/'smoke.mp4'
            result = self.run_cli(board, p, '--output', str(output), '--poster', str(p/'poster.png'), '--score')
            self.assertEqual(result.returncode, 0, result.stderr)
            streams = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(output)]))['streams']
            video = next(s for s in streams if s['codec_type']=='video')
            self.assertEqual((video['width'], video['height'], int(video['nb_frames'])), (720,1280,60))
            self.assertTrue(any(s['codec_type']=='audio' for s in streams))
            self.assertIn('00:00:00,000 --> 00:00:02,000', output.with_suffix('.srt').read_text())
            self.assertTrue((p/'poster.png').exists())
            self.assertFalse(list(p.glob('viz-*')))
            subprocess.run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'], check=True)


if __name__ == '__main__': unittest.main()
