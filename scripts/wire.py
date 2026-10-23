#!/usr/bin/env python3
"""Write the shared-memory recall paragraph into each installed harness's global instruction file.

Usage:
  python3 scripts/wire.py           # write it (backup first, only between the markers)
  python3 scripts/wire.py --check   # report; exit 0 when every installed harness has the current text
  python3 scripts/wire.py --home DIR  # act on another home folder (tests)

The paragraph is `scripts/recall.md`, the same text as the "## Shared memory" section of the
claudecode-guide global block, which Claude Code reads (that block is installed by the guide,
so this script never writes `~/.claude/CLAUDE.md`; `--check` only compares it).
Text outside the markers is never changed. Exit 0 done or current, 1 something missing or
different (`--check`), 2 refused (broken markers, unreadable file) or usage error.
Standard library only.
"""

import argparse
import datetime
import os
import sys

BEGIN = "<!-- ambysto-memory:begin -->"
END = "<!-- ambysto-memory:end -->"
RECALL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recall.md")

# (harness, folder that shows it is installed, global instruction file), all relative to home.
# Paths confirmed 2026-10-23 from each harness's binary, docs or source.
HARNESSES = (
    ("Codex", ".codex", ".codex/AGENTS.md"),
    ("Grok Build", ".grok", ".grok/AGENTS.md"),
    ("OpenCode", ".config/opencode", ".config/opencode/AGENTS.md"),
    ("Antigravity CLI", ".gemini", ".gemini/GEMINI.md"),
    ("Hermes", ".hermes", ".hermes/SOUL.md"),
)
# Not wired: Muse Code reads the Codex and Claude Code files; the rest are not installed on this
# machine and their global file is to confirm when they are (AGENTS.md, "Harnesses").
DOCUMENTED_ONLY = ("Muse Code (through Codex and Claude Code)", "Oh My Pi", "Cursor CLI", "Codewhale", "DeepSeek Harness")
CLAUDE_FILE = ".claude/CLAUDE.md"
CLAUDE_SECTION = "## Shared memory"


class Refused(Exception):
    pass


def read_recall():
    with open(RECALL, encoding="utf-8") as fh:
        return fh.read().strip() + "\n"


def newline_of(text):
    return "\r\n" if "\r\n" in text else "\n"


def block(recall, nl):
    body = recall.replace("\n", nl)
    return BEGIN + nl + body + END + nl


def split(text, path):
    """Return (before, inside, after) around the markers, or None when there are none."""
    begins, ends = text.count(BEGIN), text.count(END)
    if begins == 0 and ends == 0:
        return None
    if begins != 1 or ends != 1 or text.index(BEGIN) > text.index(END):
        raise Refused("%s: broken ambysto-memory markers (need exactly one begin before one end); fix by hand" % path)
    start = text.index(BEGIN)
    stop = text.index(END) + len(END)
    nl = newline_of(text)
    if text.startswith(nl, stop):
        stop += len(nl)
    return text[:start], text[start:stop], text[stop:]


def wired_text(text, recall, path):
    """The file's text with the current block, everything else byte for byte."""
    nl = newline_of(text) if text else "\n"
    parts = split(text, path)
    if parts is None:
        sep = "" if not text or text.endswith(nl + nl) else (nl if text.endswith(nl) else nl + nl)
        return text + sep + block(recall, nl)
    before, _, after = parts
    return before + block(recall, nl) + after


def read_bytes(path):
    with open(path, "rb") as fh:
        data = fh.read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused("%s: not UTF-8; not touched" % path)


def claude_section(home):
    """The installed global block's Shared memory section, or None."""
    path = os.path.join(home, CLAUDE_FILE)
    if not os.path.isfile(path):
        return None
    text = read_bytes(path).replace("\r\n", "\n")
    if CLAUDE_SECTION not in text:
        return ""
    rest = text[text.index(CLAUDE_SECTION):]
    lines = rest.split("\n")
    out = [lines[0]]
    for line in lines[1:]:
        if line.startswith("## ") or line.startswith("<!-- claudecode-guide:end"):
            break
        out.append(line)
    return "\n".join(out).strip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Wire the shared-memory recall into each harness.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--home", default=os.path.expanduser("~"))
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    home = os.path.abspath(args.home)
    try:
        recall = read_recall()
    except OSError as exc:
        print("cannot read %s: %s" % (RECALL, exc), file=sys.stderr)
        return 2

    problems, refused = [], []
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    section = claude_section(home)
    if section is None:
        print("Claude Code: %s not found; not checked" % CLAUDE_FILE)
    elif section != recall:
        problems.append("Claude Code: the \"%s\" section in ~/%s differs from scripts/recall.md "
                        "(install the claudecode-guide block, or update recall.md to match)" % (CLAUDE_SECTION, CLAUDE_FILE))
    else:
        print("Claude Code: current (claudecode-guide block)")

    for name, marker_dir, rel in HARNESSES:
        if not os.path.isdir(os.path.join(home, marker_dir)):
            print("%s: not installed (no ~/%s)" % (name, marker_dir))
            continue
        path = os.path.join(home, rel)
        try:
            text = read_bytes(path) if os.path.exists(path) else ""
            new = wired_text(text, recall, "~/" + rel)
        except Refused as exc:
            refused.append(str(exc))
            continue
        if new == text:
            print("%s: current (~/%s)" % (name, rel))
            continue
        if args.check:
            problems.append("%s: ~/%s %s" % (name, rel, "lacks the recall block" if split(text, rel) is None else "has an old recall block"))
            continue
        if os.path.exists(path):
            backup = "%s.bak-%s" % (path, stamp)
            with open(backup, "wb") as fh:
                fh.write(text.encode("utf-8"))
            note = "backup ~/%s" % os.path.relpath(backup, home)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            note = "created"
        with open(path, "wb") as fh:
            fh.write(new.encode("utf-8"))
        print("%s: wrote ~/%s (%s)" % (name, rel, note))

    for name in DOCUMENTED_ONLY:
        print("%s: documented only (AGENTS.md, \"Harnesses\")" % name)
    for line in refused:
        print("REFUSED: " + line)
    for line in problems:
        print("MISSING: " + line)
    if refused:
        return 2
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
