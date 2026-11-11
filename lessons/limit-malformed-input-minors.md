---
title: Document review MINORs that only fail on input the shell rejects
kind: decision
applies_when: when a review of a command parser (`session-gates.py`, agent-guard) lists a MINOR that needs malformed or pathological input
projects: all
evidence: 2026-11-11 coding-playbook APS-72 (4 review rounds; the last MINORs needed unclosed substitutions or thousands of nested `$((`)
last_validated: 2026-11-11
status: active
---

Fix every MINOR that gives a wrong result on a command people really type.
A MINOR that needs input the shell itself rejects (unclosed `$(`, a body bash and dash both error on) or a pathological size (thousands of nested levels): do not fix it. Add it to the limits in `docs/internals.md` and tell the owner in one line.
Options turned down: fixing all of them. In a quote-aware scanner each fix opened a new odd case, and APS-72 took four review rounds and long reports.
When unsure whether an input is realistic, run it in bash and dash: if both fail on it, it is malformed.
Confirm: the PR body lists each MINOR as fixed or documented, and the owner has no MINOR left to ask about.
