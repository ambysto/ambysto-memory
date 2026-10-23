---
title: Wire Codex instructions into CODEX_HOME, not only ~/.codex
kind: gotcha
applies_when: when Codex ignores ~/.codex/AGENTS.md or a global Codex setting seems to have no effect
projects: all
evidence: 2026-10-23 APS-36 proof 10 (Codex answered "No" to the Shared memory question)
last_validated: 2026-10-23
status: active
---

Check `echo $CODEX_HOME` first. Orca launches Codex with `CODEX_HOME` set to a home per account (`~/.config/orca/codex-accounts/<id>/home`) and has a runtime home (`~/.config/orca/codex-runtime-home/home`); Codex then reads `AGENTS.md` and `config.toml` there, not in `~/.codex`.
`python3 scripts/wire.py` in ambysto-memory writes the recall block into every one of these.
Confirm: ask `codex exec` with no tools whether it sees the "Shared memory" section; it should quote its first sentence.
