"""Tests for scripts/wire.py. Temp HOME folders only. Run: python3 -m unittest scripts/test_wire.py"""

import glob
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wire  # noqa: E402

RECALL = wire.read_recall()


class Home:
    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="amem-wire-")

    def path(self, rel):
        return os.path.join(self.root, rel)

    def mkdir(self, rel):
        os.makedirs(self.path(rel), exist_ok=True)

    def write(self, rel, data):
        os.makedirs(os.path.dirname(self.path(rel)), exist_ok=True)
        with open(self.path(rel), "wb") as fh:
            fh.write(data.encode("utf-8") if isinstance(data, str) else data)

    def read(self, rel):
        with open(self.path(rel), "rb") as fh:
            return fh.read().decode("utf-8")

    def run(self, *extra):
        out = subprocess.run([sys.executable, os.path.join(HERE, "wire.py"), "--home", self.root] + list(extra),
                             capture_output=True, text=True)
        return out.returncode, out.stdout + out.stderr

    def backups(self, rel):
        return glob.glob(self.path(rel) + ".bak-*")


def claude_md(section):
    return ("<!-- claudecode-guide:begin -->\n# Global\n\n## Owner time log\n- a rule\n\n" + section +
            "\n## Working practice\n- another\n<!-- claudecode-guide:end -->\n\n## This machine\n- local\n")


class WireTests(unittest.TestCase):
    def setUp(self):
        self.home = Home()
        self.addCleanup(shutil.rmtree, self.home.root, True)

    def test_creates_missing_file_for_an_installed_harness(self):
        self.home.mkdir(".codex")
        code, out = self.home.run()
        self.assertEqual(code, 0, out)
        self.assertIn("Codex: wrote ~/.codex/AGENTS.md (created)", out)
        self.assertEqual(self.home.read(".codex/AGENTS.md"), wire.BEGIN + "\n" + RECALL + wire.END + "\n")

    def test_skips_harnesses_not_installed(self):
        code, out = self.home.run()
        self.assertEqual(code, 0, out)
        self.assertIn("Grok Build: not installed", out)
        self.assertFalse(os.path.exists(self.home.path(".grok")))

    def test_owner_text_kept_byte_for_byte_and_backed_up(self):
        owner = "# My Hermes soul\n\nBe kind.\nKeep this line exactly.  \n"
        self.home.write(".hermes/SOUL.md", owner)
        code, out = self.home.run()
        self.assertEqual(code, 0, out)
        text = self.home.read(".hermes/SOUL.md")
        self.assertTrue(text.startswith(owner + "\n" + wire.BEGIN + "\n"), text[:200])
        self.assertTrue(text.endswith(wire.END + "\n"))
        backups = self.home.backups(".hermes/SOUL.md")
        self.assertEqual(len(backups), 1)
        with open(backups[0], encoding="utf-8") as fh:
            self.assertEqual(fh.read(), owner)

    def test_second_run_changes_nothing(self):
        self.home.write(".grok/AGENTS.md", "rules\n")
        self.home.run()
        first = self.home.read(".grok/AGENTS.md")
        code, out = self.home.run()
        self.assertEqual(code, 0, out)
        self.assertIn("Grok Build: current", out)
        self.assertEqual(self.home.read(".grok/AGENTS.md"), first)
        self.assertEqual(len(self.home.backups(".grok/AGENTS.md")), 1)

    def test_old_block_replaced_text_around_kept(self):
        before, after = "top\n", "\nbottom line\n"
        self.home.write(".config/opencode/AGENTS.md", before + wire.BEGIN + "\nold text\n" + wire.END + "\n" + after)
        code, out = self.home.run()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.home.read(".config/opencode/AGENTS.md"),
                         before + wire.BEGIN + "\n" + RECALL + wire.END + "\n" + after)

    def test_crlf_file_stays_crlf(self):
        owner = "line one\r\nline two\r\n"
        self.home.write(".gemini/GEMINI.md", owner)
        self.home.run()
        text = self.home.read(".gemini/GEMINI.md")
        self.assertTrue(text.startswith(owner))
        self.assertNotIn("\n", text.replace("\r\n", ""))
        self.assertIn(RECALL.replace("\n", "\r\n"), text)

    def test_broken_markers_refused_and_untouched(self):
        cases = [wire.BEGIN + "\nno end\n", "no begin\n" + wire.END + "\n",
                 wire.END + "\n" + wire.BEGIN + "\n",
                 wire.BEGIN + "\n" + wire.END + "\n" + wire.BEGIN + "\n" + wire.END + "\n"]
        for text in cases:
            with self.subTest(text=text):
                self.home.write(".codex/AGENTS.md", text)
                code, out = self.home.run()
                self.assertEqual(code, 2, out)
                self.assertIn("REFUSED: ~/.codex/AGENTS.md: broken ambysto-memory markers", out)
                self.assertEqual(self.home.read(".codex/AGENTS.md"), text)

    def test_non_utf8_refused_and_untouched(self):
        self.home.write(".codex/AGENTS.md", b"\xff\xfe junk")
        code, out = self.home.run()
        self.assertEqual(code, 2, out)
        self.assertIn("not UTF-8", out)
        with open(self.home.path(".codex/AGENTS.md"), "rb") as fh:
            self.assertEqual(fh.read(), b"\xff\xfe junk")

    def test_check_reports_missing_then_passes(self):
        self.home.write(".codex/AGENTS.md", "rules\n")
        code, out = self.home.run("--check")
        self.assertEqual(code, 1, out)
        self.assertIn("MISSING: Codex: ~/.codex/AGENTS.md lacks the recall block", out)
        self.assertEqual(self.home.read(".codex/AGENTS.md"), "rules\n")  # --check never writes
        self.home.run()
        code, out = self.home.run("--check")
        self.assertEqual(code, 0, out)

    def test_check_reports_an_old_block(self):
        self.home.write(".codex/AGENTS.md", wire.BEGIN + "\nold\n" + wire.END + "\n")
        code, out = self.home.run("--check")
        self.assertEqual(code, 1, out)
        self.assertIn("has an old recall block", out)

    def test_check_compares_the_claude_code_section(self):
        self.home.write(".claude/CLAUDE.md", claude_md(RECALL))
        code, out = self.home.run("--check")
        self.assertEqual(code, 0, out)
        self.assertIn("Claude Code: current", out)
        self.home.write(".claude/CLAUDE.md", claude_md(RECALL.replace("INDEX.md", "INDEX.txt")))
        code, out = self.home.run("--check")
        self.assertEqual(code, 1, out)
        self.assertIn("MISSING: Claude Code", out)
        self.home.write(".claude/CLAUDE.md", claude_md(""))
        code, out = self.home.run("--check")
        self.assertEqual(code, 1, out)

    def test_never_writes_claude_md(self):
        original = claude_md("")
        self.home.write(".claude/CLAUDE.md", original)
        self.home.run()
        self.assertEqual(self.home.read(".claude/CLAUDE.md"), original)

    def test_recall_matches_the_guide_section_text(self):
        # scripts/recall.md is the guide's "## Shared memory" section: a heading and at most a few lines.
        self.assertTrue(RECALL.startswith(wire.CLAUDE_SECTION + "\n"))
        self.assertIn("INDEX.md", RECALL)
        self.assertIn("pull --ff-only", RECALL)


if __name__ == "__main__":
    unittest.main()
