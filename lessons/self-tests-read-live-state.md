---
title: Make a config-editing tool's self-test read today's state, not hard-code it
kind: correction
applies_when: when writing a self-test for a script that edits model pins, settings, versions or other values that will change
projects: all
evidence: 2026-11-08 claudecode-guide APS-47 PR #30 and PR #31 (switch-model.py's first real run was refused)
last_validated: 2026-11-08
status: active
---

Read the current values (model IDs, labels, effort, existing record lines) from the scratch copy at the start of the self-test, and derive every expected result from them.
Use placeholders that can never occur in real data (`claude-test-9-9`, `claude-guess-1-1`), never a likely future value such as the next real model ID.
Why: `switch-model.py --self-test` hard-coded the day's state, so the first real switch (effort `medium` → `high`) broke it and the tool refused itself; an earlier draft used the expected `claude-fable-5-5` as its "guessed ID" and would have refused the real release-day switch.
Confirm: apply each switch the tool exists for to scratch copies (here: effort change, release-day (a), (b), (a) then (b)) and run the self-test in every resulting state.
