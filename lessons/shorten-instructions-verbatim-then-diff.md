---
title: Shorten an instruction file by moving text verbatim, then check it line by line
kind: workflow
applies_when: when slimming a CLAUDE.md, AGENTS.md or global instruction block to save context
projects: all
evidence: 2026-11-11 coding-playbook APS-62 PR #60 (hard review round 1 MAJOR)
last_validated: 2026-11-11
status: active
---

Move detail out verbatim (to `docs/internals.md` or a skill) and leave one line per item that keeps every rule a session acts on: each "never", each owner decision, each fail-open or fail-closed property.
Check with a script that every old line is either still in the file or byte-identical in the new place, and send a different model to compare the old and new text sentence by sentence.
Never merge two items into one sentence when their invariants differ.
Why: in APS-62 the save-it, graph and owner-token-guard hooks were folded into one bullet that said "must never block a session (exit 0, `|| true`)". That is true of the first two and wrong for the guard, which must block; a later session could have "fixed" the guard to fail open.
Confirm: the script prints no missing line, and the reviewer lists no lost or weakened rule.
