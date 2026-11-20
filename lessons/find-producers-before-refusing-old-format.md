---
title: Find every producer of a format before a change refuses its old shape
kind: correction
applies_when: when a change makes a tool, schema, IR or config parser refuse a shape it used to accept (an old `mode`, a removed field, a stricter validator)
projects: all
evidence: 2026-11-20 ambysto-graph PR #19 refused `mode: workflow`; coding-playbook `progress-diagram.py` still wrote it, fixed by APS-83 (PR #80)
last_validated: 2026-11-20
status: active
---

Before merging, search every repo under `~/work/ambysto/` and the installed tools for code that writes the old shape, not only for code that reads it: `grep -rlE '<old key or value>' ~/work/ambysto --include=*.py --include=*.json --include=*.sh --include=*.rs`, skipping `target/`, `.git/` and the changed repo's own fixtures.
Fix or move each producer in the same change or a linked one, before the refusing change merges.
Why: ambysto-graph began refusing `mode: workflow` while `progress-diagram.py` still wrote it, so every session's progress diagram and coding-playbook's `check.py` failed until the next unrelated task ran `check.py`.
Confirm: the search lists only the change's own refusal fixtures and docs, and each other repo's checks that call the tool (for coding-playbook, `check.py`) pass against the new build.
