---
title: Keep the old parser as one reading when rewriting a gate's command parser
kind: workflow
applies_when: when rewriting how a guard hook (`session-gates.py`, agent-guard) splits or scans shell commands
projects: all
evidence: 2026-11-11 coding-playbook APS-71 (two review FAILs; each fix of the new case scanner let a push to main through that main refused)
last_validated: 2026-11-11
status: active
---

Keep the shipped scanner verbatim beside the new one, read each command with both, and check every command any reading finds (APS-71 `READINGS`, `scan_end_main`). The old reading runs first, and a fault in a new reading skips only that reading.
Where shells disagree (bash, dash, zsh), add one reading per shell rule instead of picking one.
Why: a refusal can then only be added, never lost. Rewrites of a quote-aware scanner kept dropping refusals in shapes nobody tested; the review found new ones each round.
No regex with overlapping alternatives under `*` (`(?:\s|#[^\n]*)*`). It backtracks exponentially, and a fail-open hook times out and allows the command.
Confirm: a differential fuzz of old against new, in real bash and dash with a stub `git`, shows no old-deny/new-allow case, and the self-test pins the reading order.
