---
title: Mutate each guard to prove a self-test fails, and check refusals by reason
kind: workflow
applies_when: when a script's self-test or unit tests are the proof for a guard (refuse, restore, validate)
projects: all
evidence: 2026-11-08 claudecode-guide APS-45 PR #29 and APS-47 PR #31 (switch-test.py and switch-model.py)
last_validated: 2026-11-08
status: active
---

On a scratch copy, break one guard at a time (`if cond:` → `if False:`, drop a restore, skip an edit), run the self-test, and expect FAIL; keep the runner in the scratchpad so it can be rerun.
A missed mutation means a weak test: most often it checks that a call was refused, not why, so another guard refusing later hides the broken one. Assert the refusal's message.
Why: in switch-model.py, dropping the check before a switch was missed because the check after it also refused; only the reason check caught it.
Confirm: every mutation reports CAUGHT, and the unmodified self-test still passes.
