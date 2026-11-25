---
title: Document review MINORs that only fail on input the shell rejects
kind: decision
applies_when: when a review of a command parser (`session-gates.py`, agent-guard) lists a MINOR that needs malformed or pathological input
projects: all
evidence: 2026-11-11 coding-playbook APS-72 (4 review rounds; the last MINORs needed unclosed substitutions or thousands of nested `$((`); 2026-11-25 APS-98 review (the bash-and-dash test mislabelled a valid line above an unclosed `$(`); 2026-11-25 CPB-7 review (the marker test truncated a file through a kept redirection)
last_validated: 2026-11-25
status: active
---

Fix every MINOR that gives a wrong result on a command people really type.
A MINOR that needs input the shell rejects as a whole, before any of it runs (a lone unclosed `$(`) or a pathological size (thousands of nested levels): do not fix it. Add it to the limits in `docs/internals.md` and tell the owner in one line.
Options turned down: fixing all of them. In a quote-aware scanner each fix opened a new odd case, and APS-72 took four review rounds and long reports.
When unsure whether an input is malformed, check its syntax without running it: pass it as one argument to `bash -n -c` and to `dash -n -c`. It is malformed only if it is one line and both reject it. A multi-line input is realistic: both shells run a valid first line before they reach an error on a later one, so a guard must still judge that line. Do not test by running it with the actions swapped out: a kept redirection (`> file`) truncates a real file, and a redirection-only line leaves no mark.
Confirm: the PR body lists each MINOR as fixed or documented, and the owner has no MINOR left to ask about.
