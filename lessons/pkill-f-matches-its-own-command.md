---
title: pkill -f kills its own shell when the pattern is in the same command
kind: gotcha
applies_when: when a Bash call stops a background node, python or server process by name with pkill -f or pgrep -f
match: \bpkill\s+-f\b
projects: all
evidence: 2026-11-23 agentsocial, the tool shell died three times (exit 144) and each time took the rest of the command with it
last_validated: 2026-11-23
status: active
---

The pattern is part of the command line of the shell that runs it, so `-f` matches that shell too.
Use `kill $(pgrep -f "node tools/[c]heck_parity.cjs")` in a call of its own: the bracket keeps the pattern from matching its own text, and the later steps are not in the same command string.
Or start the job with `nohup ... &`, keep its PID, and `kill <pid>`.
After stopping, run `pgrep -f` again to see that nothing is left.
Confirm: the call returns normally and the job no longer appears.
