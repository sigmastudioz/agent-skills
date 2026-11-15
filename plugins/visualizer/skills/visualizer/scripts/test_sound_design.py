#!/usr/bin/env python3
"""Tests for the pure functions in sound_design.py. By Lex from SigmaStudioz.

No network, Earshot or Real SFX runtime is needed. Run from this folder: python3 -m unittest
"""
import json
import math
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sound_design  # noqa: E402


class NumberTests(unittest.TestCase):
    def test_accepts_bounds_inclusive_and_returns_float(self):
        self.assertEqual(sound_design.number(0, 'x', 0, 1), 0.0)
        self.assertIsInstance(sound_design.number(1, 'x', 0, 1), float)
        self.assertEqual(sound_design.number(-2, 'offset', -2, 2), -2.0)
        self.assertEqual(sound_design.number(0.5, 'x', 0, 1), 0.5)

    def test_rejects_out_of_range_non_finite_and_wrong_types(self):
        for value in (-0.001, 1.001, math.nan, math.inf, -math.inf, True, False, '0.5', None, [0.5]):
            with self.subTest(value=value), self.assertRaises(ValueError) as caught:
                sound_design.number(value, 'gain_db', 0, 1)
            self.assertEqual(str(caught.exception), 'Invalid gain_db')


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='sound-test-'))
        self.addCleanup(shutil.rmtree, self.tmp, True)


class FreshTests(TempDirCase):
    def test_returns_resolved_path_and_creates_parent(self):
        out = sound_design.fresh(self.tmp / 'nested' / 'new.wav')
        self.assertEqual(out, (self.tmp / 'nested' / 'new.wav').resolve())
        self.assertTrue(out.parent.is_dir())
        self.assertFalse(out.exists())

    def test_refuses_existing_file(self):
        existing = self.tmp / 'taken.wav'
        existing.write_bytes(b'')
        with self.assertRaises(ValueError) as caught:
            sound_design.fresh(existing)
        self.assertIn('Output already exists', str(caught.exception))

    def test_refuses_existing_directory(self):
        with self.assertRaises(ValueError):
            sound_design.fresh(self.tmp)


class MixOutputTests(TempDirCase):
    def test_accepts_new_mp4_path(self):
        self.assertEqual(sound_design.mix_output(self.tmp / 'review.mp4'), (self.tmp / 'review.mp4').resolve())

    def test_refuses_non_mp4_suffix(self):
        for name in ('review.mov', 'review.wav', 'review', 'review.mp4.bak'):
            with self.subTest(name=name), self.assertRaises(ValueError) as caught:
                sound_design.mix_output(self.tmp / name)
            self.assertIn('.mp4 extension', str(caught.exception))

    def test_refuses_existing_sidecar_or_work_collisions(self):
        collisions = ('review_resolved_cues.json', 'review_sfx.wav', 'review.sound-work', 'review.sound-report.json')
        for name in collisions:
            with self.subTest(name=name):
                path = self.tmp / name
                path.mkdir() if name.endswith('.sound-work') else path.write_text('{}')
                with self.assertRaises(ValueError) as caught:
                    sound_design.mix_output(self.tmp / 'review.mp4')
                self.assertIn(name, str(caught.exception))
                shutil.rmtree(path) if path.is_dir() else path.unlink()

    def test_ignores_unrelated_neighbours(self):
        (self.tmp / 'reviewer_notes.json').write_text('{}')  # different stem, not stem + '_'
        (self.tmp / 'other_resolved_cues.json').write_text('{}')
        sound_design.mix_output(self.tmp / 'review.mp4')


class SearchTests(TempDirCase):
    """search() must validate arguments before touching the network; get() is replaced throughout."""

    def setUp(self):
        super().setUp()
        self.calls = []

        def fake_get(url, limit=4 * 1024 * 1024, attempts=2):
            self.calls.append(url)
            return json.dumps({'results': [
                {'id': 'abc', 'title': 'Whoosh', 'creator': 'someone', 'license': 'cc0',
                 'foreign_landing_url': 'https://example.org/item', 'url': 'https://example.org/a.mp3',
                 'extra': 'dropped'}]}).encode()

        patcher = mock.patch.object(sound_design, 'get', side_effect=fake_get)
        self.get = patcher.start()
        self.addCleanup(patcher.stop)

    def assert_rejected(self, query, browse):
        with self.assertRaises(ValueError) as caught:
            sound_design.search(query, self.tmp / 'out.json', browse=browse)
        self.assertIn('query OR --browse', str(caught.exception))
        self.get.assert_not_called()
        self.assertFalse((self.tmp / 'out.json').exists())

    def test_rejects_neither_query_nor_browse(self):
        self.assert_rejected(None, False)
        self.assert_rejected('', False)

    def test_rejects_query_together_with_browse(self):
        self.assert_rejected('whoosh', True)

    def test_rejects_overlong_or_non_string_query(self):
        self.assert_rejected('w' * 201, False)
        self.assert_rejected(123, False)

    def test_keyword_search_builds_request_and_writes_results(self):
        result = sound_design.search('whoosh', self.tmp / 'search.json')
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(self.calls[0].startswith('https://api.openverse.org/v1/audio/?'))
        self.assertIn('q=whoosh', self.calls[0])
        self.assertIn('license=cc0', self.calls[0])
        self.assertEqual(result['results'], [{'id': 'abc', 'title': 'Whoosh', 'creator': 'someone', 'license': 'cc0',
                                              'foreign_landing_url': 'https://example.org/item',
                                              'url': 'https://example.org/a.mp3'}])
        saved = json.loads((self.tmp / 'search.json').read_text())
        self.assertEqual(saved['strategy'], 'keyword')
        self.assertEqual(saved['request_url'], self.calls[0])

    def test_browse_omits_query_parameter(self):
        sound_design.search(None, self.tmp / 'browse.json', browse=True, source='freesound')
        self.assertNotIn('q=', self.calls[0])
        self.assertIn('source=freesound', self.calls[0])
        self.assertEqual(json.loads((self.tmp / 'browse.json').read_text())['strategy'], 'filtered-browse')

    def test_refuses_existing_output_before_network(self):
        (self.tmp / 'exists.json').write_text('{}')
        with self.assertRaises(ValueError):
            sound_design.search('whoosh', self.tmp / 'exists.json')
        self.get.assert_not_called()

    def test_rejects_non_results_payload(self):
        self.get.side_effect = lambda url, **kw: b'{"detail": "nope"}'
        with self.assertRaises(ValueError) as caught:
            sound_design.search('whoosh', self.tmp / 'bad.json')
        self.assertIn('Not an Openverse results response', str(caught.exception))


class RedirectTests(unittest.TestCase):
    """The HTTPS-only rule must hold for every hop, not only the first URL."""

    def redirect(self, target):
        request = sound_design.urllib.request.Request('https://example.org/a.wav')
        return sound_design.HttpsOnlyRedirects().redirect_request(request, None, 302, 'Found', {}, target)

    def test_follows_https_redirect(self):
        self.assertEqual(self.redirect('https://cdn.example.org/a.wav').full_url, 'https://cdn.example.org/a.wav')

    def test_refuses_downgrade_and_credentials(self):
        for target in ('http://example.org/a.wav', 'ftp://example.org/a.wav', 'https://user:pw@example.org/a.wav'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                self.redirect(target)

    def test_opener_uses_the_checked_handler(self):
        with mock.patch.object(sound_design.urllib.request, 'build_opener') as build:
            build.return_value.open.side_effect = ValueError('stop')
            with self.assertRaises(ValueError):
                sound_design.get('https://example.org/a.wav')
        self.assertTrue(any(isinstance(h, sound_design.HttpsOnlyRedirects) for h in build.call_args.args))


@unittest.skipUnless(shutil.which('git'), 'git is not installed')
class PinnedRuntimeTests(TempDirCase):
    """runtime() accepts only the recorded revisions with nothing added or changed."""

    def repo(self, name):
        root = self.tmp / name
        (root / 'pkg' / 'scripts').mkdir(parents=True)
        (root / 'pkg' / 'scripts' / 'mix.py').write_text('print(1)\n')
        git = ['git', '-C', str(root), '-c', 'user.name=t', '-c', 'user.email=t@example.invalid']
        for args in (['init', '-q'], ['add', '-A'], ['commit', '-q', '-m', 'init']):
            sound_design.run(git + args)
        return root, sound_design.run(git + ['rev-parse', 'HEAD']).strip()

    def config(self):
        earshot, earshot_head = self.repo('earshot')
        real, real_head = self.repo('real')
        path = self.tmp / 'config.json'
        path.write_text(json.dumps({
            'python': sys.executable, 'ffmpeg': sys.executable, 'ffprobe': sys.executable,
            'earshot_root': str(earshot), 'real_sfx_root': str(real / 'pkg' / 'scripts'),
            'revisions': {'earshot': earshot_head, 'real_sfx': real_head}}))
        return path, earshot, real

    def test_accepts_clean_pinned_checkouts(self):
        path, _, _ = self.config()
        config, env = sound_design.runtime(path)
        self.assertEqual(env['EARSHOT_OFFLINE'], '1')
        self.assertIn('revisions', config)

    def test_refuses_untracked_and_modified_files_by_name(self):
        path, earshot, real = self.config()
        (earshot / 'sitecustomize.py').write_text('x = 1\n')
        with self.assertRaises(ValueError) as caught:
            sound_design.runtime(path)
        self.assertIn('earshot checkout', str(caught.exception))
        self.assertIn('sitecustomize.py', str(caught.exception))
        (earshot / 'sitecustomize.py').unlink()
        (real / 'pkg' / 'scripts' / 'mix.py').write_text('print(2)\n')
        with self.assertRaises(ValueError) as caught:
            sound_design.runtime(path)
        self.assertIn('real_sfx checkout', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
