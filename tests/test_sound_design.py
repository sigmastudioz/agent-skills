"""Guard the sound bridge's rights, revision and non-destructive boundaries."""
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import wave
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
        with patch.object(sound.urllib.request.OpenerDirector, 'open', return_value=response):
            with self.assertRaisesRegex(ValueError, 'too large'):
                sound.get('https://example.org/audio.wav', limit=5)

    def test_rate_limit_does_not_trigger_unbounded_retries(self):
        error = urllib.error.HTTPError('https://example.org', 429, 'limited', {'Retry-After': '60'}, None)
        with patch.object(sound.urllib.request.OpenerDirector, 'open', side_effect=error) as request:
            with self.assertRaisesRegex(ValueError, 'longer wait'):
                sound.get('https://example.org/audio.wav')
        self.assertEqual(request.call_count, 1)

    def test_credentials_do_not_reach_runtime_children(self):
        for directory in ('earshot', 'clipwing/skills/real-sfx'):
            (self.root / directory).mkdir(parents=True)
        config = {'python': sys.executable, 'ffmpeg': sys.executable, 'ffprobe': sys.executable,
                  'earshot_root': str(self.root / 'earshot'),
                  'real_sfx_root': str(self.root / 'clipwing/skills/real-sfx'),
                  'revisions': {'earshot': 'earshot-pin', 'real_sfx': 'sfx-pin'}}
        sound.save(self.root / 'runtime.json', config)
        secrets = {'OPENAI_API_KEY': 'sentinel-openai', 'HF_TOKEN': 'sentinel-hf',
                   'AWS_SESSION_TOKEN': 'sentinel-aws', 'HTTPS_PROXY': 'https://secret:secret@invalid',
                   'PYTHONPATH': '/untrusted/python', 'UNRELATED_SECRET': 'sentinel-other'}
        with patch.dict(os.environ, secrets), patch.object(shutil, 'which', return_value='/tools/git'), \
                patch.object(sound, 'run', side_effect=['earshot-pin\n', '', 'sfx-pin\n', '']) as run:
            _, env = sound.runtime(self.root / 'runtime.json')
            for call in run.call_args_list:
                self.assertTrue(set(secrets).isdisjoint(call.args[1]))
            self.assertEqual(run.call_args_list[0].args[0][0], '/tools/git')
        # Exercise a real child, rather than only checking the constructed dictionary.
        output = sound.run([sys.executable, '-c', 'import os,json; print(json.dumps(dict(os.environ)))'], env)
        child = json.loads(output)
        self.assertTrue(set(secrets).isdisjoint(child))
        for key in ('EARSHOT_OFFLINE', 'HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE', 'PYTHONNOUSERSITE'):
            self.assertEqual(child[key], '1')
        self.assertIn(str(Path(sys.executable).parent), child['PATH'].split(os.pathsep))

    def test_anonymous_download_does_not_discover_host_proxy_credentials(self):
        response = io.BytesIO(b'public-audio')
        response.headers = {}
        opener = sound.urllib.request.build_opener(sound.urllib.request.ProxyHandler({}))
        with patch.dict(os.environ, {'HTTPS_PROXY': 'https://secret:secret@invalid'}), \
                patch.object(sound.urllib.request, 'build_opener', return_value=opener) as build, \
                patch.object(opener, 'open', return_value=response) as request:
            self.assertEqual(sound.get('https://example.org/audio.wav'), b'public-audio')
        self.assertEqual(build.call_args.args[0].proxies, {})
        self.assertNotIn('Authorization', request.call_args.args[0].headers)

    def test_credential_url_is_rejected_before_opening_network(self):
        with patch.object(sound.urllib.request, 'build_opener') as build:
            with self.assertRaisesRegex(ValueError, 'Credential-bearing'):
                sound.get('https://user:secret@example.org/audio.wav')
            build.assert_not_called()

    def test_download_cannot_write_a_script_or_package_configuration(self):
        item = {'id': 'sound', 'foreign_landing_url': 'https://example.org/item',
                'url': 'https://example.org/audio.wav', 'license': 'cc0',
                'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/'}
        sound.save(self.root / 'results.json', {'response': {'results': [item]},
                                              'request_url': 'https://api.openverse.org/v1/audio/'})
        with patch.object(sound, 'get', return_value=b'audio-data') as request, \
                patch.object(sound, 'probe', return_value={'streams': [{'codec_type': 'audio'}]}):
            for name in ('setup.py', 'setup.sh', 'package.json', 'payload', 'asset.svg'):
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'audio extension'):
                    sound.fetch(self.root / 'results.json', 'sound', self.root / name, 'Cleared', {}, {})
                self.assertFalse((self.root / name).exists())
            request.assert_not_called()

    @unittest.skipUnless(shutil.which('ffprobe'), 'ffprobe is required for the local decoder boundary')
    def test_probe_accepts_audio_but_refuses_playlist_disguised_as_audio(self):
        audio = self.root / 'tone.wav'
        with wave.open(str(audio), 'wb') as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(8000)
            wav.writeframes(b'\0\0' * 800)
        config = {'ffprobe': shutil.which('ffprobe')}
        self.assertEqual(sound.probe(audio, config, {}, downloaded=True)['streams'][0]['codec_type'], 'audio')
        playlist = self.root / 'playlist.mp3'
        playlist.write_text(f'ffconcat version 1.0\nfile {audio}\n')
        with self.assertRaisesRegex(ValueError, 'not on whitelist'):
            sound.probe(playlist, config, {}, downloaded=True)

    @unittest.skipUnless(shutil.which('ffprobe'), 'ffprobe is required for the download consumer')
    def test_public_audio_download_still_probes_and_records_provenance(self):
        data = io.BytesIO()
        with wave.open(data, 'wb') as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(8000)
            wav.writeframes(b'\0\0' * 800)
        item = {'id': 'sound', 'foreign_landing_url': 'https://example.org/item',
                'url': 'https://example.org/audio.wav', 'license': 'cc0',
                'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/'}
        sound.save(self.root / 'results.json', {'response': {'results': [item]},
                                              'request_url': 'https://api.openverse.org/v1/audio/'})
        output = self.root / 'download.wav'
        with patch.object(sound, 'get', return_value=data.getvalue()):
            result = sound.fetch(self.root / 'results.json', 'sound', output, 'Reviewed CC0 source',
                                 {'ffprobe': shutil.which('ffprobe')}, {})
        self.assertEqual(output.read_bytes(), data.getvalue())
        proof = sound.load(result['provenance'])
        self.assertEqual(proof['sha256'], sound.sha(output))
        self.assertEqual(proof['source'], item)
        self.assertEqual(proof['rights_status'], 'reviewed')

    @unittest.skipUnless(shutil.which('ffprobe'), 'ffprobe is required for the download consumer')
    def test_code_disguised_as_audio_is_deleted_without_execution(self):
        item = {'id': 'sound', 'foreign_landing_url': 'https://example.org/item',
                'url': 'https://example.org/audio.mp3', 'license': 'cc0',
                'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/'}
        sound.save(self.root / 'results.json', {'response': {'results': [item]}})
        marker = self.root / 'executed'
        payload = f'from pathlib import Path; Path({str(marker)!r}).touch()'.encode()
        output = self.root / 'download.mp3'
        with patch.object(sound, 'get', return_value=payload):
            with self.assertRaisesRegex(ValueError, 'Command failed'):
                sound.fetch(self.root / 'results.json', 'sound', output, 'Reviewed item',
                            {'ffprobe': shutil.which('ffprobe')}, {})
        self.assertFalse(marker.exists())
        self.assertFalse(output.exists())
        self.assertFalse(Path(str(output) + '.provenance.json').exists())


if __name__ == '__main__':
    unittest.main()
