---
title: Send fixes made after a reviewer PASS back to the reviewer before merging
kind: workflow
applies_when: when changing code after a reviewer or hard-reviewer PASS, before the merge
projects: all
evidence: 2026-11-11 coding-playbook APS-66 (cb28f23 fixed MINORs after the round 2 PASS and broke heredocs inside quoted $( ))
last_validated: 2026-11-11
status: active
---

Send the delta (`git diff <passed commit>..<new commit>`) to the same reviewer and ask whether the PASS holds; merge only on its answer.
Why: a MINOR fix after a PASS changed the quote handling and made the hook refuse ordinary commit messages; the self-test passed and only the delta review caught it.
Ask the reviewer to list what is left as follow-ups for the ticket, so the confirmation does not turn into another full round.
Confirm: the reviewer's last verdict names the commit that is merged.
