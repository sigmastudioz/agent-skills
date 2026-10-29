"""Guard the sound bridge's rights, revision and non-destructive boundaries."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sound_bridge', ROOT / 'plugins/visualizer/skills/visualizer/scripts/sound_design.py')
sound = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sound)


class SoundDesignTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        (self.root / 'picture.mp4').write_bytes(b'picture-revision-one')
        (self.root / 'effect.wav').write_bytes(b'cleared-source-one')
        self.proof = {'kind': 'local', 'sha256': sound.sha(self.root / 'effect.wav'), 'rights_status': 'reviewed',
                      'rights_note': 'Original source reviewed for this use'}
        sound.save(self.root / 'proof.json', self.proof)
        self.plan = {'video': 'picture.mp4', 'picture_sha256': sound.sha(self.root / 'picture.mp4'),
                     'mode': 'effects', 'preserve_original': False,
                     'cues': [{'id': 'contact', 'purpose': 'Explain contact', 'time': 1.0,
                               'file': 'effect.wav', 'provenance': 'proof.json', 'anchor': 'peak', 'role': 'hit'},
                              {'id': 'quiet', 'purpose': 'Allow reading', 'time': 2.0, 'silence': True}]}
        self.meta = {'format': {'duration': '3.0'}, 'streams': [{'codec_type': 'video'}]}

    def prepare(self):
        path = self.root / 'plan.json'
        path.write_text(json.dumps(self.plan))
        with patch.object(sound, 'probe', return_value=self.meta):
            return sound.prepare(path, {}, {})

    def test_resolves_project_relative_assets_and_preserves_silence(self):
        _, sheet, proofs, quiet, _ = self.prepare()
        self.assertEqual(sheet['cues'][0]['file'], str(self.root / 'effect.wav'))
        self.assertEqual(len(sheet['cues']), 1)
        self.assertEqual(quiet[0]['id'], 'quiet')
        self.assertEqual(proofs[0]['provenance'], self.proof)
        self.assertEqual(sheet['keep_audio'], 'no')

    def test_changed_picture_requires_retiming_review(self):
        (self.root / 'picture.mp4').write_bytes(b'new-edit')
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.prepare()

    def test_changed_asset_invalidates_its_rights_snapshot(self):
        (self.root / 'effect.wav').write_bytes(b'different-file')
        with self.assertRaisesRegex(ValueError, 'hash differs'):
            self.prepare()

    def test_uncleared_asset_does_not_enter_mix(self):
        self.proof['rights_status'] = 'unknown'
        sound.save(self.root / 'proof.json', self.proof)
        with self.assertRaisesRegex(ValueError, 'rights'):
            self.prepare()

    def test_invalid_cues_are_rejected(self):
        for value in (float('nan'), float('inf'), True, -1, 3.1):
            with self.subTest(time=value):
                self.plan['cues'][0]['time'] = value
                with self.assertRaises(ValueError):
                    self.prepare()

    def test_duplicate_ids_do_not_silently_merge(self):
        self.plan['cues'][1]['id'] = 'contact'
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.prepare()

    def test_voice_mode_requires_an_actual_base(self):
        self.plan['mode'] = 'voice'
        with self.assertRaisesRegex(ValueError, 'Voice mode'):
            self.prepare()

    def test_source_audio_and_stems_cannot_double(self):
        self.plan.update(preserve_original=True, base_audio=['effect.wav'])
        with self.assertRaisesRegex(ValueError, 'not both'):
            self.prepare()

    def test_audio_preservation_requires_a_boolean_decision(self):
        self.plan['preserve_original'] = 1
        with self.assertRaisesRegex(ValueError, 'explicitly'):
            self.prepare()

    def test_local_audio_needs_an_explicit_origin(self):
        del self.proof['kind']
        sound.save(self.root / 'proof.json', self.proof)
        with self.assertRaisesRegex(ValueError, 'kind'):
            self.prepare()

    def test_existing_outputs_are_preserved(self):
        p = self.root / 'delivery.mp4'
        p.write_bytes(b'approved')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            sound.fresh(p)
        self.assertEqual(p.read_bytes(), b'approved')

    def test_existing_stems_and_reports_prevent_the_mixer_from_starting(self):
        prepared = self.prepare()
        for suffix in ('_sfx_track.wav', '_stem_motion.wav', '_resolved_cues.json',
                       '_cue_report.md', '.sound-report.json', '_work', '.sound-work'):
            with self.subTest(suffix=suffix):
                sidecar = self.root / ('delivery' + suffix)
                sidecar.write_bytes(b'approved-artifact')
                with patch.object(sound, 'prepare', return_value=prepared), patch.object(sound, 'run') as run:
                    with self.assertRaisesRegex(ValueError, 'Existing mix sidecar'):
                        sound.mix(self.root / 'plan.json', self.root / 'delivery.mp4', {}, {})
                    run.assert_not_called()
                self.assertEqual(sidecar.read_bytes(), b'approved-artifact')
                self.assertFalse((self.root / 'delivery.mp4').exists())
                sidecar.unlink()

    def test_non_mp4_output_fails_before_any_mix_write(self):
        with self.assertRaisesRegex(ValueError, '.mp4 extension'):
            sound.mix_output(self.root / 'delivery.wav')

    def test_browse_cannot_masquerade_as_keyword_search(self):
        with self.assertRaises(ValueError):
            sound.search('click', self.root / 'search.json', browse=True)
        with patch.object(sound, 'get', return_value=b'{"results": []}') as request:
            sound.search(None, self.root / 'browse.json', browse=True)
        self.assertNotIn('q=', request.call_args.args[0])
        self.assertEqual(sound.load(self.root / 'browse.json')['strategy'], 'filtered-browse')

    def test_download_size_is_bounded(self):
        response = io.BytesIO(b'123456')
        response.headers = {}
        with patch.object(sound.urllib.request, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'too large'):
                sound.get('https://example.org/audio.wav', limit=5)

    def test_rate_limit_does_not_trigger_unbounded_retries(self):
        error = urllib.error.HTTPError('https://example.org', 429, 'limited', {'Retry-After': '60'}, None)
        with patch.object(sound.urllib.request, 'urlopen', side_effect=error) as request:
            with self.assertRaisesRegex(ValueError, 'longer wait'):
                sound.get('https://example.org/audio.wav')
        self.assertEqual(request.call_count, 1)


if __name__ == '__main__':
    unittest.main()
