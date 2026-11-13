"""Static checks for the published Visualizer and Video Analysis packages (no network)."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "plugins"
CHECKED = ["visualizer", "delegating-to-agents"]
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def text_files(plugin):
    for p in (ROOT / plugin).rglob("*"):
        if p.is_file() and p.suffix in {".md", ".py", ".yaml", ".json", ".txt"}:
            yield p


class Packages(unittest.TestCase):
    def test_archive_exclusions_cover_only_download_links(self):
        """Media that .gitattributes leaves out of source archives is linked only as a ?raw=true download."""
        patterns = [line.split()[0].lstrip("/") for line in (REPO / ".gitattributes").read_text().splitlines()
                    if line.strip().endswith("export-ignore") and not line.startswith("#")]
        self.assertTrue(patterns)
        plain = []
        for p in ROOT.rglob("*.md"):
            for target in LINK.findall(p.read_text(encoding="utf-8")):
                if "://" in target or "?raw=true" in target:
                    continue
                resolved = (p.parent / target).resolve()
                if any(resolved.match(str(REPO / pattern)) for pattern in patterns):
                    plain.append(f"{p.relative_to(ROOT)} -> {target}")
        self.assertEqual(plain, [])

    def test_text_keeps_numbers_apart_from_words(self):
        """A lost space once fused words and numbers ("the432×768", "own0") in docs and error messages."""
        fused = re.compile(r"(?<![\w/.-])(a|an|the|own|version|about|first|and|or|for|at|to|with|most|opacity|normalized|grayscale)\d")
        hits = [f"{p.relative_to(ROOT)}:{n}" for plugin in ("visualizer", "video-analysis")
                for p in (ROOT / plugin).rglob("*") if p.suffix in {".md", ".py"}
                for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if fused.search(line)]
        self.assertEqual(hits, [])

    def test_no_local_paths(self):
        hits = [str(p.relative_to(ROOT)) for plugin in CHECKED for p in text_files(plugin)
                if "/Users/" in p.read_text(encoding="utf-8", errors="ignore")]
        self.assertEqual(hits, [])

    def test_selected_skills_have_frontmatter_and_license(self):
        for plugin in CHECKED:
            skill = ROOT / plugin / "skills" / plugin / "SKILL.md"
            head = skill.read_text(encoding="utf-8").split("---")[1]
            self.assertIn(f"name: {plugin}", head)
            self.assertIn("license: MIT", head)


if __name__ == "__main__":
    unittest.main()
