"""Slipstream: behaviour checks on synthetic data only (no real logs, homes or network)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/slipstream/skills/slipstream"
PY = sys.executable


def run(args, stdin="", env=None, timeout=120):
    e = dict(os.environ, **(env or {}))
    return subprocess.run(args, input=stdin, capture_output=True, text=True, env=e, timeout=timeout)


def skill_md(root, name, body="body"):
    d = Path(root) / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: test {name} skill\n---\n{body}\n")


class GuardTests(unittest.TestCase):
    def decide(self, cmd):
        out = run([PY, SKILL / "hooks/slip_guard.py"], json.dumps({"tool_input": {"command": cmd}})).stdout
        return "deny" if '"deny"' in out else "allow"

    def test_bare_sleep_denied_shell_wait_allowed(self):
        self.assertEqual(self.decide("sleep 30"), "deny")
        self.assertEqual(self.decide("sleep 30 && gh run view 1"), "deny")
        self.assertEqual(self.decide("sleep 2"), "allow")
        self.assertEqual(self.decide("until curl -s localhost; do sleep 5; done"), "allow")
        self.assertEqual(self.decide("npm test"), "allow")

    def test_wait_for_ready_and_timeout(self):
        with tempfile.TemporaryDirectory() as d:
            flag = Path(d) / "ready"
            flag.touch()
            ok = run(["bash", SKILL / "scripts/wait_for.sh", "--timeout", "5", "--every", "1", "--", "test", "-f", str(flag)])
            self.assertEqual(ok.returncode, 0)
            late = run(["bash", SKILL / "scripts/wait_for.sh", "--timeout", "2", "--every", "1", "--", "test", "-f", str(Path(d) / "never")])
            self.assertEqual(late.returncode, 124)


class HintTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        cat = Path(self.tmp.name) / "catalog.tsv"
        rows = [("detecting-kerberoasting-attacks", "Detect Kerberoasting in Kerberos TGS logs"),
                ("localization", "Localize game UI text"), ("airflow-dag-patterns", "Airflow DAG patterns"),
                ("evaluation", "Evaluate models"), ("dark-mode", "Dark mode toggles")]
        cat.write_text("".join(f"{n}\tskills\t{d}\t/x/{n}/SKILL.md\n" for n, d in rows))
        self.env = {"SKILL_CATALOG": str(cat), "SKILL_ALIASES": str(Path(self.tmp.name) / "none.json"),
                    "SKILL_LISTED_DIRS": str(Path(self.tmp.name) / "listed")}

    def tearDown(self):
        self.tmp.cleanup()

    def hint(self, prompt):
        out = run([PY, SKILL / "hooks/slip_hint.py"], json.dumps({"prompt": prompt, "cwd": "."}), self.env).stdout
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else ""

    def test_specialist_requests_get_the_right_skill(self):
        self.assertIn("detecting-kerberoasting-attacks", self.hint("Help me detect Kerberoasting attacks in our logs"))
        self.assertIn("localization", self.hint("Set up localization for my game"))
        self.assertIn("airflow-dag-patterns", self.hint("Which Airflow DAG patterns fit the daily job?"))
        # 2 of 3 name words is deliberately not enough: it raised noise on a real catalog with no recall gain
        self.assertEqual(self.hint("Write an Airflow DAG for the daily job"), "")

    def test_everyday_and_machine_messages_stay_silent(self):
        for p in ("fix the typo in the README", "ok do it", "rename this variable everywhere",
                  "bxyz toolu_01abc /private/tmp/task.output completed"):
            self.assertEqual(self.hint(p), "", p)


class MeterTests(unittest.TestCase):
    def test_silent_small_then_one_nudge(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d) / "s.jsonl"

            def write(ctxs):
                t.write_text("".join(json.dumps({"type": "assistant", "message": {"usage": {
                    "input_tokens": 0, "cache_read_input_tokens": c, "cache_creation_input_tokens": 0}}}) + "\n" for c in ctxs))
            ev = json.dumps({"transcript_path": str(t), "session_id": f"test-{os.getpid()}"})
            env = {"TMPDIR": d}
            write([40000, 60000])
            self.assertEqual(run([PY, SKILL / "hooks/slip_meter.py"], ev, env).stdout.strip(), "")
            write([40000, 200000])
            self.assertIn("handoff", run([PY, SKILL / "hooks/slip_meter.py"], ev, env).stdout)
            self.assertEqual(run([PY, SKILL / "hooks/slip_meter.py"], ev, env).stdout.strip(), "")


class LifecycleTests(unittest.TestCase):
    def test_apply_promote_undo_restores_exactly(self):
        with tempfile.TemporaryDirectory() as home:
            h = Path(home)
            for n in ("alpha", "beta", "graphify", "gamma-helper"):
                skill_md(h / ".claude/skills", n)
            with open(h / ".claude/skills/graphify/SKILL.md", "a") as f:
                f.write("Then use gamma-helper.\n")
            (h / ".claude/CLAUDE.md").write_text("Use graphify.\n")
            (h / ".codex/skills").mkdir(parents=True)
            (h / ".codex/AGENTS.md").write_text("# agents\n")
            (h / ".claude/projects/p").mkdir(parents=True)
            (h / ".codex/sessions").mkdir(parents=True)
            settings = {"enabledPlugins": {}, "hooks": {"PreToolUse": [{"matcher": "Edit", "hooks": [{"type": "command", "command": "echo keep"}]}]}}
            (h / ".claude/settings.json").write_text(json.dumps(settings))
            env = {"HOME": home}
            r = run([PY, SKILL / "scripts/lean_setup.py", "--apply"], env=env, timeout=300)
            self.assertEqual(r.returncode, 0, r.stderr)
            listed = set(os.listdir(h / ".claude/skills"))
            self.assertEqual(listed, {"graphify", "gamma-helper", "skill-library", "slipstream"})
            (h / ".claude/projects/p/s.jsonl").write_text(json.dumps({"type": "assistant", "timestamp": "2099-01-01T00:00:00Z",
                "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "beta"}}], "usage": {"input_tokens": 1}}}, separators=(",", ":")) + "\n")
            os.utime(h / ".claude/projects/p/s.jsonl")
            r = run([PY, h / ".claude/skill-library/slipstream/scripts/lean_setup.py", "--refresh"], env=env, timeout=300)
            self.assertIn("beta", os.listdir(h / ".claude/skills"), r.stdout + r.stderr)
            r = run([PY, SKILL / "scripts/lean_setup.py", "--undo"], env=env, timeout=300)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(set(os.listdir(h / ".claude/skills")), {"alpha", "beta", "graphify", "gamma-helper"})
            self.assertEqual(json.loads((h / ".claude/settings.json").read_text()), settings)
            self.assertEqual((h / ".codex/AGENTS.md").read_text(), "# agents\n")


class PackageTests(unittest.TestCase):
    def test_no_publisher_machine_paths_or_personal_data(self):
        for p in (ROOT / "plugins/slipstream").rglob("*"):
            if p.is_file() and p.suffix in {".py", ".md", ".sh", ".json", ".svg", ".mdc"}:
                t = p.read_text(errors="ignore")
                for bad in ("/Users/", "/private/tmp", "@gmail"):
                    self.assertNotIn(bad, t, f"{p}: {bad}")

    def test_production_modules_under_600_lines(self):
        for p in (SKILL).rglob("*.py"):
            self.assertLessEqual(len(p.read_text().splitlines()), 600, p)


if __name__ == "__main__":
    unittest.main()
