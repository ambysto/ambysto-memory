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
import tempfile

BEGIN = "<!-- ambysto-memory:begin -->"
END = "<!-- ambysto-memory:end -->"
RECALL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recall.md")

# (harness, folder that shows it is installed, global instruction file), all relative to home.
# Paths confirmed 2026-10-23 from each harness's binary, docs or source.
HARNESSES = (
    ("Grok Build", ".grok", ".grok/AGENTS.md"),
    ("OpenCode", ".config/opencode", ".config/opencode/AGENTS.md"),
    ("Antigravity CLI", ".gemini", ".gemini/GEMINI.md"),
    ("Hermes", ".hermes", ".hermes/SOUL.md"),
)
# Not wired: Muse Code reads the Codex and Claude Code files; the rest are not installed on this
# machine and their global file is to confirm when they are (AGENTS.md, "Harnesses").
DOCUMENTED_ONLY = ("Muse Code (through Codex and Claude Code)", "Oh My Pi", "Cursor CLI", "Codewhale", "DeepSeek Harness")
CLAUDE_FILE = ".claude/CLAUDE.md"
# Codex reads `$CODEX_HOME/AGENTS.md` (default `~/.codex`). Orca runs Codex with a home per account
# under `~/.config/orca/codex-accounts/<id>/home`, so each of those gets the block too.
ORCA_CODEX_HOMES = ".config/orca/codex-accounts"


def codex_homes(home, env):
    """Codex homes under `home`, as (name, folder) relative to it, without duplicates."""
    found = [".codex"]
    codex_home = env.get("CODEX_HOME")
    if codex_home:
        full = os.path.abspath(os.path.expanduser(codex_home))
        if full == home or full.startswith(home + os.sep):
            found.append(os.path.relpath(full, home))
    orca = os.path.join(home, ORCA_CODEX_HOMES)
    if os.path.isdir(orca):
        for account in sorted(os.listdir(orca)):
            if os.path.isdir(os.path.join(orca, account, "home")):
                found.append(os.path.join(ORCA_CODEX_HOMES, account, "home"))
    out, seen = [], set()
    for rel in found:
        key = os.path.realpath(os.path.join(home, rel))
        if key in seen:
            continue
        seen.add(key)
        label = "Codex" if rel == ".codex" else "Codex (%s)" % ("Orca account" if rel.startswith(ORCA_CODEX_HOMES) else "CODEX_HOME")
        out.append((label, rel, os.path.join(rel, "AGENTS.md")))
    return out
CLAUDE_SECTION = "## Shared memory"


class Refused(Exception):
    pass


def read_recall():
    with open(RECALL, encoding="utf-8") as fh:
        return fh.read().strip() + "\n"


def newline_of(text):
    """The file's main line ending: CRLF only when most line ends are CRLF."""
    crlf = text.count("\r\n")
    return "\r\n" if crlf and crlf > text.count("\n") - crlf else "\n"


def block(recall, nl):
    body = recall.replace("\n", nl)
    return BEGIN + nl + body + END + nl


def is_fence(line):
    return line.lstrip().startswith(("```", "~~~"))


def fence_open(lines):
    """True when a fence is still open after these lines; a fence closes only on its own kind."""
    opener = None
    for line in lines:
        if is_fence(line):
            kind = line.lstrip()[0]
            if opener is None:
                opener = kind
            elif kind == opener:
                opener = None
    return opener is not None


def split(text, path):
    """Return (before, inside, after) around the block, or None when the file has no marker text.

    wire.py always appends its block at the end of the file, so a block is recognised only when:
    each marker is a line of its own, exactly; there is one begin line before one end line and no
    other marker text anywhere; only blank lines follow the end line; no code fence line is inside
    the block; and no fence is open before it. A marker in
    any other form or place could be an example the owner wrote: refused, the file is not touched.
    """
    total = text.count(BEGIN) + text.count(END)
    if total == 0:
        return None
    lines = text.splitlines(True)
    exact = [(i, line.rstrip("\r\n")) for i, line in enumerate(lines) if line.rstrip("\r\n") in (BEGIN, END)]
    ok = total == len(exact) == 2 and [kind for _, kind in exact] == [BEGIN, END]
    if ok:
        first, last = exact[0][0], exact[1][0]
        ok = (all(not line.strip() for line in lines[last + 1:])
              and not any(is_fence(line) for line in lines[first:last + 1])
              and not fence_open(lines[:first]))
    if not ok:
        raise Refused("%s: ambysto-memory marker text in an unexpected form or place (the block must be "
                      "one begin line and one end line, each alone on its line, at the end of the file, "
                      "outside any code fence); fix by hand" % path)
    return "".join(lines[:first]), "".join(lines[first:last + 1]), "".join(lines[last + 1:])


def wired_text(text, recall, path):
    """The file's text with the current block, everything else byte for byte."""
    nl = newline_of(text) if text else "\n"
    parts = split(text, path)
    if parts is None and fence_open(text.splitlines()):
        raise Refused("%s: a code fence looks open at the end of the file (fences are matched by kind, ``` or "
                      "~~~, not by length); a block appended there could be read as code; close the fence, or "
                      "add a blank line and the recall block by hand" % path)
    if parts is None:
        sep = "" if not text or text.endswith(nl + nl) else (nl if text.endswith(nl) else nl + nl)
        return text + sep + block(recall, nl)
    before, _, after = parts
    return before + block(recall, nl) + after


def read_bytes(path, shown=None):
    shown = shown or path
    if os.path.isdir(path):
        raise Refused("%s: is a folder, not a file" % shown)
    with open(path, "rb") as fh:
        data = fh.read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused("%s: not UTF-8; not touched" % shown)


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


def backup_path(path, stamp):
    """A backup name that does not exist yet (two runs in one second must not share one)."""
    base = "%s.bak-%s" % (path, stamp)
    candidate, n = base, 1
    while os.path.lexists(candidate):
        candidate, n = "%s-%d" % (base, n), n + 1
    return candidate


def write_atomically(path, data):
    """Write through a temp file in the same folder, then rename over the target."""
    folder = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(prefix=".wire-", dir=folder)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        if os.path.exists(path):
            mode = os.stat(path).st_mode & 0o7777
        else:
            umask = os.umask(0)
            os.umask(umask)
            mode = 0o666 & ~umask
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def wire_one(name, rel, home, recall, check, stamp, problems):
    """Wire or check one harness. Raises Refused or OSError on doubt; never writes outside its markers."""
    link = os.path.join(home, rel)
    # Write through a symlink to its target, so the link itself stays a link.
    path = os.path.realpath(link) if os.path.islink(link) else link
    if os.path.islink(link) and not os.path.exists(path):
        raise Refused("~/%s: a symlink to a missing file" % rel)
    text = read_bytes(path, "~/" + rel) if os.path.exists(path) else ""
    new = wired_text(text, recall, "~/" + rel)
    if new == text:
        print("%s: current (~/%s)" % (name, rel))
        return
    if check:
        problems.append("%s: ~/%s %s" % (name, rel, "lacks the recall block" if split(text, rel) is None else "has an old recall block"))
        return
    if os.path.exists(path):
        if not os.access(path, os.W_OK) or not os.access(os.path.dirname(path), os.W_OK):
            raise Refused("~/%s: not writable; not touched" % rel)
        backup = backup_path(path, stamp)
        with open(backup, "xb") as fh:
            fh.write(text.encode("utf-8"))
        shown = os.path.relpath(backup, home)
        note = "backup " + ("~/" + shown if not shown.startswith("..") else backup)
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        note = "created"
    write_atomically(path, new.encode("utf-8"))
    print("%s: wrote ~/%s (%s)" % (name, rel, note))


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

    try:
        section = claude_section(home)
    except (Refused, OSError) as exc:
        print("cannot read ~/%s: %s" % (CLAUDE_FILE, exc), file=sys.stderr)
        return 2
    if section is None:
        print("Claude Code: %s not found; not checked" % CLAUDE_FILE)
    elif section != recall:
        problems.append("Claude Code: the \"%s\" section in ~/%s differs from scripts/recall.md "
                        "(install the claudecode-guide block, or update recall.md to match)" % (CLAUDE_SECTION, CLAUDE_FILE))
    else:
        print("Claude Code: current (claudecode-guide block)")

    for name, marker_dir, rel in codex_homes(home, os.environ) + list(HARNESSES):
        if not os.path.isdir(os.path.join(home, marker_dir)):
            print("%s: not installed (no ~/%s)" % (name, marker_dir))
            continue
        try:
            wire_one(name, rel, home, recall, args.check, stamp, problems)
        except Refused as exc:
            refused.append(str(exc))
        except OSError as exc:
            refused.append("%s: ~/%s: %s; not touched" % (name, rel, exc.strerror or exc))

    print("Documented only (AGENTS.md, \"Harnesses\"): " + ", ".join(DOCUMENTED_ONLY))
    for line in refused:
        print("REFUSED: " + line)
    for line in problems:
        print("MISSING: " + line)
    if refused:
        return 2
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
