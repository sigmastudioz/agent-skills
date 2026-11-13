"""Exercise credential-free process and native-manifest boundaries."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/'plugins/visualizer/skills/visualizer/scripts'


def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS/file)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SCRIPTS))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


runtime = load_module('credential_runtime', 'tool_runtime.py')
sound = load_module('credential_sound', 'sound_design.py')
try:
    media = load_module('credential_media', 'media_in_3d.py')
except ModuleNotFoundError as error:
    if error.name not in ('numpy', 'PIL'):
        raise
    media = None
CHILD = [sys.executable, '-c', 'import os,json; print(json.dumps(dict(os.environ)))']
SENTINELS = {'OPENAI_API_KEY':'sentinel-key', 'AWS_SESSION_TOKEN':'sentinel-session',
             'HF_TOKEN':'sentinel-token', 'UNRELATED_SECRET':'sentinel-secret',
             'HTTPS_PROXY':'https://sentinel:secret@invalid', 'HOME':'/nonexistent/credentials',
             'PYTHONPATH':'/nonexistent/python', 'PYTHONSTARTUP':'/nonexistent/startup',
             'NODE_OPTIONS':'--require=/nonexistent/injection', 'FFREPORT':'sentinel-report',
             'TMPDIR':'/nonexistent/tmp', 'LANG':'sentinel-locale', 'LC_ALL':'sentinel-locale'}


class CredentialBoundaries(unittest.TestCase):
    def assert_clean(self, env):
        self.assertTrue((set(SENTINELS)-{'LANG','LC_ALL'}).isdisjoint(env))
        self.assertEqual(env['LANG'], 'C')
        self.assertEqual(env['LC_ALL'], 'C')
        self.assertEqual(env['PYTHONNOUSERSITE'], '1')
        self.assertTrue(all(value not in env.values() for value in SENTINELS.values()))

    def test_environment_does_not_consult_the_callers_values(self):
        with patch('os.environ', {}):
            clean = runtime.tool_environment(sys.executable)
        with patch.dict(os.environ, SENTINELS):
            self.assertEqual(runtime.tool_environment(sys.executable), clean)
        self.assert_clean(clean)

    def test_explicit_tool_directory_survives_in_real_child(self):
        env = runtime.tool_environment(sys.executable)
        with patch.dict(os.environ, SENTINELS):
            child = json.loads(subprocess.check_output(CHILD, env=env))
        self.assert_clean(child)
        self.assertIn(str(Path(sys.executable).absolute().parent), child['PATH'].split(os.pathsep))

    def test_sound_default_run_does_not_inherit_credentials(self):
        with patch.dict(os.environ, SENTINELS):
            child = json.loads(sound.run(CHILD))
        self.assert_clean(child)

    @unittest.skipUnless(media, 'NumPy/Pillow required for media adapter')
    def test_media_probe_and_decode_runner_does_not_inherit_credentials(self):
        with patch.dict(os.environ, SENTINELS):
            child = json.loads(media.run(CHILD))
        self.assert_clean(child)

    def test_native_manifests_have_no_credential_or_execution_configuration(self):
        for slug in ('ui-foundation-reuse', 'visualizer'):
            plugin = ROOT/'plugins'/slug
            with self.subTest(plugin=slug):
                manifest = json.loads((plugin/'.claude-plugin/plugin.json').read_text())
                self.assertEqual(manifest['mcpServers'], {})
                self.assertFalse(set(manifest) & {'hooks','userConfig','channels','lspServers'})
                self.assertNotIn('${', json.dumps(manifest))
                for file in ('.mcp.json','hooks/hooks.json','.lsp.json'):
                    self.assertFalse((plugin/file).exists())


if __name__ == '__main__':
    unittest.main()
