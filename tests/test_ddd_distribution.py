"""Guard the guidance-only marketplace boundary against executable payloads."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT/'plugins/domain-driven-design'


class GuidanceDistribution(unittest.TestCase):
    def test_plugin_contains_only_allowed_guidance_and_listing_files(self):
        for file in PLUGIN.rglob('*'):
            with self.subTest(file=file.relative_to(PLUGIN)):
                self.assertFalse(file.is_symlink())
                if not file.is_file():
                    continue
                self.assertTrue(file.suffix in {'.md','.txt','.json','.yaml','.yml'}
                                or file.relative_to(PLUGIN).as_posix() in {'LICENSE','assets/icon.svg'})
                data = file.read_bytes()
                self.assertFalse(data.startswith(b'#!'))
                self.assertNotIn(b'\x00', data)
                data.decode('utf-8')

    def test_discovery_cannot_activate_a_program_or_remote_server(self):
        manifest = json.loads((PLUGIN/'.claude-plugin/plugin.json').read_text())
        self.assertFalse(set(manifest) & {'hooks','mcpServers','lspServers','userConfig','channels'})
        for path in ('.mcp.json','.lsp.json','hooks/hooks.json','skills/domain-driven-design/scripts'):
            self.assertFalse((PLUGIN/path).exists())
        self.assertTrue((PLUGIN/'skills/domain-driven-design/SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
