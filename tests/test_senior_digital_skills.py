"""Static regressions for the Senior Digital Skills Class plugin (no network).

They guard the skill's safety and honest-claim rules against silent edits; they do not measure
whether an agent follows them. The pressure scenarios in the skill's tests/README.md do that.
"""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / 'plugins' / 'senior-digital-skills'
SKILL_DIR = PLUGIN / 'skills' / 'senior-digital-skills'
SKILL = SKILL_DIR / 'SKILL.md'
REFERENCES = sorted((SKILL_DIR / 'references').glob('*.md'))
LINK = re.compile(r'\]\(([^)#\s]+)(?:#[^)]*)?\)')


def read(path):
    return path.read_text(encoding='utf-8')


class Package(unittest.TestCase):
    def test_frontmatter_byline_and_license(self):
        text = read(SKILL)
        head = text.split('---')[1]
        self.assertIn('name: senior-digital-skills', head)
        self.assertIn('license: MIT', head)
        self.assertIn('By [Lex from SigmaStudioz](https://github.com/sigmastudioz).', text)
        for license_file in (PLUGIN / 'LICENSE', SKILL_DIR / 'LICENSE'):
            self.assertIn('Copyright (c) 2026 Lex from SigmaStudioz', read(license_file))

    def test_every_reference_is_routed_from_skill_md(self):
        linked = {(SKILL.parent / target).resolve() for target in LINK.findall(read(SKILL))}
        unrouted = [p.name for p in REFERENCES if p.resolve() not in linked]
        self.assertEqual(unrouted, [])
        self.assertGreaterEqual(len(REFERENCES), 7)

    def test_skill_md_stays_short(self):
        self.assertLess(len(read(SKILL).splitlines()), 120)

    def test_three_host_manifests_share_identity(self):
        portable = json.loads(read(PLUGIN / 'plugin.json'))
        for host in ('claude', 'codex', 'cursor'):
            native = json.loads(read(PLUGIN / f'.{host}-plugin' / 'plugin.json'))
            self.assertEqual((native['name'], native['version']), (portable['name'], portable['version']))
            self.assertEqual(native['description'], portable['description'], host)
        self.assertEqual(portable['name'], 'senior-digital-skills')

    def test_no_local_paths(self):
        hits = [str(p.relative_to(PLUGIN)) for p in PLUGIN.rglob('*') if p.is_file()
                and '/Users/' in p.read_text(encoding='utf-8', errors='ignore')]
        self.assertEqual(hits, [])


class SafetyRules(unittest.TestCase):
    def test_instructors_never_handle_credentials_or_payments(self):
        skill, safety = read(SKILL), read(SKILL_DIR / 'references' / 'learner-safety.md')
        for phrase in ('passwords', 'PINs', 'verification codes', 'never log in'):
            self.assertIn(phrase, skill)
        for phrase in ('Point, don\'t take.', 'Forgotten passwords.', 'Demo accounts.'):
            self.assertIn(phrase, safety)

    def test_loaners_and_scam_examples_cannot_leak_accounts_or_reach_scammers(self):
        curriculum = read(SKILL_DIR / 'references' / 'curriculum.md')
        self.assertIn('signed out and reset before the next learner', curriculum)
        self.assertIn('fictional names, numbers and links', curriculum)

    def test_no_selling_to_learners(self):
        self.assertIn('Teach, do not sell.', read(SKILL))

    def test_viral_funding_figure_is_never_stated_as_fact(self):
        """The reel's dollar figure may appear only in the pressure scenario that tests refusing it."""
        dollar = re.compile(r'\$\s?[\dX]|\bUSD\b|\d(?:\.\d+)?\s*(?:million|thousand|M\b)', re.I)
        hits = [str(p.relative_to(PLUGIN)) for p in [SKILL, *REFERENCES, PLUGIN / 'README.md']
                if dollar.search(read(p))]
        self.assertEqual(hits, [])
        self.assertIn('unverified claim', read(SKILL_DIR / 'references' / 'funding-and-partners.md'))

    def test_funding_leads_require_verification(self):
        funding = read(SKILL_DIR / 'references' / 'funding-and-partners.md')
        self.assertIn('**lead to verify**', funding)
        self.assertIn('Digital Equity Act', funding)
        self.assertRegex(funding, r'Status is uncertain')
        self.assertIn('July 2026', funding)  # dated, so a stale note is visible to reviewers
        self.assertIn('not eligible applicants', funding)

    def test_neighbouring_skills_are_linked_not_duplicated(self):
        skill = read(SKILL)
        for name in ('small-business **grant-rfp-writer**', 'small-business **proposal-builder**',
                     'marketing **events**', 'implementing-anti-phishing-training-program'):
            self.assertIn(name, skill)


if __name__ == '__main__':
    unittest.main()
