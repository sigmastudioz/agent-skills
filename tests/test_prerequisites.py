"""Collection rule: ship your own tools, never a runtime; check prerequisites with the user first.

Every plugin in catalog.json that ships executable code or calls an outside tool must tell the
agent to check what is installed, explain what is missing, and install only with the user's yes.
No plugin may bundle a runtime, dependency tree or native binary.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = {".py", ".js", ".mjs", ".cjs", ".ts", ".sh"}
EXTERNAL = re.compile(r"\b(ffmpeg|ffprobe|node(?:\.js)?\b|npm|python3?|blender|cursor-agent|codex cli)\b", re.I)
RUNTIME_PARTS = {"node_modules", "site-packages", "__pypackages__", ".venv", "venv"}
RUNTIME_SUFFIX = {".whl", ".exe", ".dll", ".so", ".dylib", ".msi", ".pkg", ".dmg"}


def plugins():
    for entry in json.loads((ROOT / "catalog.json").read_text())["plugins"]:
        yield entry["name"], (ROOT / entry["path"]).resolve()


def ships_code(root):
    return any(p.suffix in CODE and "tests" not in p.parts for p in root.rglob("*") if p.is_file())


class PrerequisitePatternTests(unittest.TestCase):
    def test_plugins_needing_tools_check_first_and_ask(self):
        for name, root in plugins():
            for skill in root.glob("skills/*/SKILL.md"):
                text = skill.read_text()
                if not (ships_code(root) or EXTERNAL.search(text)):
                    continue  # instructions only: nothing to install
                with self.subTest(plugin=name, skill=skill.parent.name):
                    self.assertTrue("Before first use" in text, "no 'Before first use' section")
                    self.assertTrue("--version" in text or "command -v" in text, "no installed-version check")
                    self.assertTrue("never install silently" in text, "no consent-only install rule")

    def test_no_bundled_runtime_or_binary(self):
        for name, root in plugins():
            for p in root.rglob("*"):
                if not p.is_file():
                    continue
                with self.subTest(plugin=name, file=str(p.relative_to(root))):
                    self.assertFalse(RUNTIME_PARTS & set(p.parts), "bundled dependency tree")
                    self.assertNotIn(p.suffix.lower(), RUNTIME_SUFFIX, "bundled binary or installer")


if __name__ == "__main__":
    unittest.main()
