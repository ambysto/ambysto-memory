---
title: Clear env vars that point at real homes in tests of tools that write there
kind: correction
applies_when: when testing a script that writes into a home folder and reads env vars such as CODEX_HOME, HOME or XDG_*
projects: all
evidence: 2026-10-23 APS-36 (a reviewer's mutant of wire.py wrote into the real Orca Codex home through an inherited CODEX_HOME)
last_validated: 2026-10-23
status: active
---

In `setUp`, patch `os.environ` (`unittest.mock.patch.dict`) and remove every variable the tool reads to find a real home, so in-process calls and subprocesses see only the temp home.
Why: a test that called the tool in-process inherited the developer's `CODEX_HOME`; once a mutant removed the under-home guard, the test wrote into the real home.
Confirm: run the suite against a mutant without the guard and check the real home's file times do not change.
