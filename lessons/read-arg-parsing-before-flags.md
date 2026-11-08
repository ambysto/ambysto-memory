---
title: Read how a script parses arguments before passing it --help
kind: correction
applies_when: when about to run a repo script with --help or an unfamiliar flag, above all one that installs or writes outside the repo
projects: all
evidence: 2026-11-08 claudecode-guide (`install.py --help` ran the real installer into ~/.claude)
last_validated: 2026-11-08
status: active
---

Open the script and read its argument handling (argparse, `sys.argv` checks) first; run it only with flags it handles.
Why: `install.py` ignored unknown arguments, so `--help` ran the real install and rewrote files in `~/.claude` (the backup it keeps was the only way back).
Confirm: the command you run appears in the script's parser, or the script prints usage and exits non-zero on an unknown flag.
