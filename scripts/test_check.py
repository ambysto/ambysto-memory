"""Tests for scripts/check.py. Temp folders only. Run: python3 -m unittest scripts/test_check.py

Every refused value is joined from pieces at run time, so this file holds none and the real
repo still passes its own check.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check  # noqa: E402

TODAY = "2026-10-23"


def j(*parts):
    return "".join(parts)


def lesson(**over):
    fields = {
        "title": "Send a custom User-Agent to the tracker API",
        "kind": "gotcha",
        "applies_when": "when a REST call to the tracker returns HTTP 403",
        "projects": "all",
        "evidence": "2026-10-16 steady SIC-130; 2026-10-23 APS-36",
        "last_validated": "2026-10-23",
        "status": "active",
    }
    fields.update(over)
    body = over.pop("_body", None)
    head = "".join("%s: %s\n" % (k, v) for k, v in fields.items() if v is not None and k != "_body")
    if body is None:
        body = "Set any User-Agent header.\nThe default Python one is refused with 403.\nConfirm: the call returns 200.\n"
    return "---\n" + head + "---\n\n" + body


class Repo:
    """A throwaway git repo with the checker's layout."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="amem-test-")
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", j("test", "@", "invalid"))  # no TLD: never a refused address
        os.makedirs(os.path.join(self.root, "lessons"))

    def git(self, *args):
        return subprocess.run(["git", "-C", self.root] + list(args), capture_output=True, text=True)

    def write(self, path, text):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    def read(self, path):
        with open(os.path.join(self.root, path), encoding="utf-8") as fh:
            return fh.read()

    def run(self, *extra):
        out = subprocess.run(
            [sys.executable, os.path.join(HERE, "check.py"), "--root", self.root, "--today", TODAY] + list(extra),
            capture_output=True, text=True,
        )
        return out.returncode, out.stdout + out.stderr

    def index(self):
        return self.run("--write-index")

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


class Base(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.cleanup)

    def assertPass(self, *extra):
        code, out = self.repo.run(*extra)
        self.assertEqual(code, 0, out)
        return out

    def assertFail(self, needle, *extra):
        code, out = self.repo.run(*extra)
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)
        return out


class ShapeTests(Base):
    def test_good_lesson_passes(self):
        self.repo.write("lessons/tracker-user-agent.md", lesson())
        code, out = self.repo.index()
        self.assertEqual(code, 0, out)
        index = self.repo.read("INDEX.md")
        self.assertIn("- [Send a custom User-Agent to the tracker API](lessons/tracker-user-agent.md)"
                      " — gotcha — when a REST call to the tracker returns HTTP 403\n", index)

    def test_missing_evidence_fails(self):  # intent criterion 1, mutation
        self.repo.write("lessons/a.md", lesson(evidence=None))
        self.repo.index()
        self.assertFail("missing field: evidence")

    def test_applies_when_must_start_with_trigger_word(self):  # intent criterion 1, mutation
        self.repo.write("lessons/a.md", lesson(applies_when="if the call fails"))
        self.repo.index()
        self.assertFail("applies_when must start with when, before or after")

    def test_stale_index_fails(self):  # intent criterion 1, mutation
        self.repo.write("lessons/a.md", lesson())
        self.repo.index()
        self.repo.write("lessons/b.md", lesson(title="Another lesson"))
        self.assertFail("INDEX.md:0: not equal to the lessons")

    def test_hand_edited_index_fails(self):
        self.repo.write("lessons/a.md", lesson())
        self.repo.index()
        with open(os.path.join(self.repo.root, "INDEX.md"), "a", encoding="utf-8") as fh:
            fh.write("- a line added by hand\n")
        self.assertFail("not equal to the lessons")

    def test_unknown_kind_fails(self):
        self.repo.write("lessons/a.md", lesson(kind="tip"))
        self.repo.index()
        self.assertFail("kind 'tip' is not one of")

    def test_long_title_fails(self):
        self.repo.write("lessons/a.md", lesson(title="x" * 80))
        self.repo.index()
        self.assertFail("title is 80 characters")

    def test_file_name_must_be_slug(self):
        self.repo.write("lessons/Bad_Name.md", lesson())
        self.repo.index()
        self.assertFail("lesson file name must be a slug")

    def test_frontmatter_must_close(self):
        self.repo.write("lessons/a.md", "---\ntitle: x\n")
        self.repo.index()
        self.assertFail("frontmatter not closed")

    def test_unknown_field_fails(self):
        self.repo.write("lessons/a.md", lesson(owner="me"))
        self.repo.index()
        self.assertFail("unknown field: owner")

    def test_projects_list_form(self):
        self.repo.write("lessons/a.md", lesson(projects="[ambysto-space, steady]"))
        self.repo.index()
        self.assertPass()
        self.repo.write("lessons/a.md", lesson(projects="ambysto-space"))
        self.repo.index()
        self.assertFail("projects must be")

    def test_body_line_count(self):
        self.repo.write("lessons/a.md", lesson(_body="one\ntwo\n"))
        self.repo.index()
        self.assertFail("body has 2 non-empty lines")
        self.repo.write("lessons/a.md", lesson(_body="x\n" * 11))
        self.repo.index()
        self.assertFail("body has 11 non-empty lines")

    def test_future_date_fails(self):
        self.repo.write("lessons/a.md", lesson(last_validated="2026-10-24"))
        self.repo.index()
        self.assertFail("last_validated is in the future")

    def test_bad_date_fails(self):
        self.repo.write("lessons/a.md", lesson(last_validated="23/10/2026"))
        self.repo.index()
        self.assertFail("last_validated must be a date")

    def test_superseded_needs_existing_target(self):
        self.repo.write("lessons/a.md", lesson(status="superseded", superseded_by="b"))
        self.repo.index()
        self.assertFail("superseded_by names no lesson: b")
        self.repo.write("lessons/b.md", lesson(title="The replacement"))
        self.repo.index()
        out = self.assertPass()
        self.assertIn("1 active lesson", out)
        index = self.repo.read("INDEX.md")
        self.assertIn("lessons/b.md", index)
        self.assertNotIn("lessons/a.md", index)

    def test_superseded_without_target_fails(self):
        self.repo.write("lessons/a.md", lesson(status="superseded"))
        self.repo.index()
        self.assertFail("a superseded lesson needs superseded_by")


class StaleTests(Base):
    def test_lesson_older_than_90_days_is_listed_not_failed(self):  # intent criterion 7, mutation
        self.repo.write("lessons/old.md", lesson(last_validated="2026-07-24"))  # 91 days before TODAY
        self.repo.index()
        out = self.assertPass()
        self.assertIn("STALE: lessons/old.md (last_validated 2026-07-24", out)

    def test_lesson_at_90_days_is_not_stale(self):
        self.repo.write("lessons/old.md", lesson(last_validated="2026-07-25"))
        self.repo.index()
        self.assertNotIn("STALE", self.assertPass())


class SecretTests(Base):
    """Intent criterion 2: refused values fail, allowed values pass."""

    def plant(self, value):
        self.repo.write("lessons/a.md", lesson(_body="Do the thing.\nIt uses %s here.\nConfirm it worked.\n" % value))
        self.repo.index()

    def test_refused(self):
        cases = [
            (j("gh", "p_", "A1b2C3d4E5f6G7h8I9j0K1l2"), "GitHub token"),
            (j("github", "_pat_", "11ABCDEFG0123456789_abcdefghij"), "GitHub token"),
            (j("s", "k-", "ant-api03-abcdefghijklmnopqrstu"), "API key"),
            (j("AK", "IA", "ABCDEFGHIJKLMNOP"), "AWS key id"),
            (j("-----BEGIN ", "OPENSSH PRIVATE KEY-----"), "private key"),
            (j("pass", "word=", "hunter2hunter2"), "credential assignment"),
            (j("12345678-", "abcd-ef01-2345-", "67890abcdef0"), "UUID"),
            (j("someone", "@", "example", ".com"), "e-mail address"),
            (j("/ho", "me/", "someone/work"), "absolute home path"),
            (j("4ba51bfb5e90", "42cd85e36d1e", "d2af3b416f22", "f4b5"), "hex run of 40 characters"),
            (j("https://", "plane.", "example", ".dev/api"), "URL host not on the allow list"),
            (j("plane.", "example", ".dev"), "host not on the allow list"),
            (j("tracker.", "example", ".vn"), "host not on the allow list"),
            (j("ambysto-eta", ".vercel", ".app"), "Vercel deployment host"),
            (j("QWxhZGRpbjpvcGVu", "c2VzYW1lMTIzNDU2Nzg5"), "base64-like run"),
        ]
        for value, reason in cases:
            with self.subTest(value=value):
                self.plant(value)
                self.assertFail(reason)

    def test_allowed(self):
        allowed = [
            "`ssh win11` and `ssh win11-test`",
            "user ambytest on win11-dev, admin Ramune",
            r"`C:\Users\ambytest\src` and `\\localhost\ambynet`",
            "`~/vms/bin/vm-gates.sh` and `~/.claude.json`",
            "files check.py, INDEX.md, win11.qcow2, AmbystoLean.dll, Lean.app",
            "short SHAs 4ba51bf and 4ba51bfb5e90",
            "https://nuget.pkg.github.com/ambysto/index.json",
            "https://github.com/ambysto/ambysto-memory/pull/2",
            "tune.ambysto.com and https://learn.microsoft.com/windows",
            "http://localhost:18080 and APS-36",
            "the Vercel project ambysto-optimer",
            "timestamp 20261023095905123",
        ]
        for value in allowed:
            with self.subTest(value=value):
                self.plant(value)
                self.assertPass()

    def test_every_tracked_file_is_scanned(self):
        self.repo.index()
        self.repo.write("README.md", "Contact %s\n" % j("someone", "@", "example", ".com"))
        self.assertFail("README.md:1: refused: e-mail address")


class StagedTests(Base):
    def test_staged_reads_the_index_not_the_tree(self):
        self.repo.write("lessons/a.md", lesson())
        self.repo.index()
        self.repo.git("add", "-A")
        self.assertPass("--staged")
        token = j("gh", "p_", "A1b2C3d4E5f6G7h8I9j0K1l2")
        self.repo.write("lessons/a.md", lesson(_body="Do it.\nWith %s.\nConfirm.\n" % token))
        self.assertPass("--staged")  # not staged yet
        self.repo.git("add", "lessons/a.md")
        self.assertFail("GitHub token", "--staged")

    def test_pre_commit_hook_refuses_a_token(self):  # proof 2
        hooks = os.path.join(self.repo.root, "hooks")
        os.makedirs(hooks)
        shutil.copy(os.path.join(os.path.dirname(HERE), "hooks", "pre-commit"), hooks)
        os.makedirs(os.path.join(self.repo.root, "scripts"))
        shutil.copy(os.path.join(HERE, "check.py"), os.path.join(self.repo.root, "scripts"))
        self.repo.git("config", "core.hooksPath", "hooks")
        self.repo.write("lessons/a.md", lesson())
        self.repo.index()
        self.repo.git("add", "-A")
        ok = self.repo.git("commit", "-qm", "clean")
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        token = j("gh", "p_", "A1b2C3d4E5f6G7h8I9j0K1l2")
        self.repo.write("lessons/a.md", lesson(_body="Do it.\nWith %s.\nConfirm.\n" % token))
        self.repo.git("add", "-A")
        bad = self.repo.git("commit", "-qm", "leak")
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("GitHub token", bad.stdout + bad.stderr)


class UsageTests(Base):
    def test_staged_with_write_index_is_a_usage_error(self):
        code, _ = self.repo.run("--staged", "--write-index")
        self.assertEqual(code, 2)

    def test_not_a_repo_is_a_usage_error(self):
        plain = tempfile.mkdtemp(prefix="amem-plain-")
        self.addCleanup(shutil.rmtree, plain, True)
        out = subprocess.run([sys.executable, os.path.join(HERE, "check.py"), "--root", plain],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)

    def test_non_utf8_file_fails(self):
        self.repo.index()
        with open(os.path.join(self.repo.root, "notes.txt"), "wb") as fh:
            fh.write(b"\xff\xfe bad")
        self.assertFail("not UTF-8 text")


if __name__ == "__main__":
    unittest.main()
