"""Runtime evidence for the shipped sampler; synthetic media only."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('media_sampler', ROOT / 'plugins/video-analysis/skills/video-analysis/scripts/sample.py')
SAMPLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SAMPLER)


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg/ffprobe required')
class MediaSamplingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def encode(self, name='source.mp4', filters=None):
        path = self.root / name
        command = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=size=320x240:rate=8:duration=2']
        if filters:
            command += ['-vf', filters, '-fps_mode', 'vfr']
        subprocess.run(command + ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(path)], check=True, capture_output=True)
        return path

    def inspect(self, source, **kwargs):
        return SAMPLER.sample(source, self.root / 'evidence', **kwargs)

    def test_budget_actual_pts_and_source_preservation(self):
        source = self.encode()
        original = source.read_bytes()
        result = self.inspect(source, frames=5)
        self.assertEqual(result['sha256'], SAMPLER.digest(source))
        self.assertEqual(source.read_bytes(), original)
        self.assertGreaterEqual(len(result['samples']), 3)
        self.assertLessEqual(len(result['samples']), 5)
        self.assertEqual(result['samples'][0]['source_seconds'], 0)
        for frame in result['samples']:
            self.assertTrue((self.root / 'evidence' / frame['file']).is_file())
            self.assertAlmostEqual(frame['source_seconds'] * 8, round(frame['source_seconds'] * 8))
        self.assertNotIn(str(self.root), json.dumps(result))

    def test_window_uses_source_times_not_local_filename_index(self):
        result = self.inspect(self.encode(), frames=5, start=.75, end=1.75)
        self.assertGreaterEqual(result['samples'][0]['source_seconds'], .75)
        self.assertLessEqual(result['samples'][-1]['source_seconds'], 1.75)
        self.assertAlmostEqual(result['samples'][0]['source_seconds'], .75)

    def test_nonzero_media_start_is_preserved_and_normalized(self):
        result = self.inspect(self.encode(filters='setpts=PTS+5/TB'), frames=4, start=.5, end=1.5)
        self.assertAlmostEqual(result['time_origin_seconds'], 5)
        self.assertAlmostEqual(result['samples'][0]['pts_seconds'], 5.5)
        self.assertAlmostEqual(result['samples'][0]['source_seconds'], .5)

    def test_variable_rate_frames_report_real_presentation_times(self):
        source = self.encode(filters="select='eq(n,0)+eq(n,2)+eq(n,3)+eq(n,7)+eq(n,12)'")
        result = self.inspect(source, frames=24)
        times = [s['source_seconds'] for s in result['samples']]
        self.assertEqual(times, [0, .25, .375, .875, 1.5])
        self.assertGreater(result['packet_duration_seconds'], result['reported_duration_seconds'])

    def test_rotation_and_maximum_display_size(self):
        source = self.encode()
        rotated = self.root / 'rotated.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-display_rotation', '90', '-i', str(source), '-c', 'copy', str(rotated)], check=True, capture_output=True)
        result = self.inspect(rotated, frames=2, side=320)
        image = self.root / 'evidence' / result['samples'][0]['file']
        info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'json', str(image)], text=True))
        self.assertEqual((info['streams'][0]['width'], info['streams'][0]['height']), (240, 320))

    def test_audio_only_inventory_without_fabricated_frames(self):
        source = self.root / 'tone.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1', str(source)], check=True, capture_output=True)
        result = self.inspect(source)
        self.assertIsNone(result['selected_video_stream'])
        self.assertEqual(result['samples'], [])
        self.assertEqual(result['audio_review'], 'Not performed; metadata only')

    def test_existing_destination_is_not_modified(self):
        source = self.encode()
        destination = self.root / 'evidence'
        destination.mkdir()
        marker = destination / 'keep.txt'
        marker.write_text('preserve')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.inspect(source)
        self.assertEqual(marker.read_text(), 'preserve')

    def test_invalid_windows_and_streams_leave_no_success_directory(self):
        source = self.encode()
        for options in [{'start': float('nan')}, {'start': 1, 'end': .5}, {'end': 9}, {'frames': 0}, {'stream': 999}]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.inspect(source, **options)
            self.assertFalse((self.root / 'evidence').exists())

    def test_corrupt_media_fails_without_publishing_partial_output(self):
        source = self.root / 'broken.mp4'
        source.write_bytes(b'not a video')
        with self.assertRaises(subprocess.CalledProcessError):
            self.inspect(source)
        self.assertFalse((self.root / 'evidence').exists())

    def test_missing_decoder_fails_atomically_without_installing(self):
        source = self.encode()
        find = shutil.which
        with patch.object(SAMPLER.shutil, 'which', side_effect=lambda name: None if name == 'ffmpeg' else find(name)):
            with self.assertRaisesRegex(ValueError, 'FFmpeg is required'):
                self.inspect(source)
        self.assertFalse((self.root / 'evidence').exists())

    def test_default_and_explicit_video_stream_selection(self):
        first, second = self.encode(), self.encode('second.mp4')
        combined = self.root / 'two-tracks.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(first), '-i', str(second), '-map', '0:v', '-map', '1:v', '-c', 'copy', '-disposition:v:0', '0', '-disposition:v:1', 'default', str(combined)], check=True, capture_output=True)
        default = self.inspect(combined, frames=2)
        explicit = SAMPLER.sample(combined, self.root / 'explicit', frames=2, stream=0)
        self.assertEqual(default['selected_video_stream'], 1)
        self.assertEqual(explicit['selected_video_stream'], 0)


if __name__ == '__main__':
    unittest.main()
