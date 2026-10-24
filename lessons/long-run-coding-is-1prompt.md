---
title: Read "long-run coding" as APS-31, now in ambysto-1prompt
kind: reference
applies_when: when the owner mentions the "long-run coding research session" or asks to continue the long-run session
projects: all
evidence: 2026-10-23 APS-31, APS-38, ambysto/1prompt 3be8f1c
last_validated: 2026-10-23
status: active
---

The owner's "long-run coding" research is APS-31, "Autonomous run mode: one prompt takes a project to done", not Lean's Windows work.
Since 2026-10-23 it lives in `~/work/ambysto/ambysto-1prompt` (public GitHub `ambysto/1prompt`, Apache-2.0, Plane APS-38): read its `HANDOFF.md`, `CLAUDE.md` and `CLAUDE.local.md` first.
That repo is the only source of `hooks/agent-guard.py`; claudecode-guide installs a pinned copy. The original intent and history stay in claudecode-guide's `intent/` (APS-32, APS-34, APS-37 there).
Everything in 1prompt is public: no ticket ids, names or private paths in files, commits or PR bodies; `python3 scripts/check.py` runs the scrub gate.
Confirm: `git -C ~/work/ambysto/ambysto-1prompt remote get-url origin` prints the 1prompt repo.
