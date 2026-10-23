---
title: Give each concurrent VM user its own worktree
kind: gotcha
applies_when: when two agents sync code into the Windows VM at the same time
projects: all
evidence: 2026-10-17 ambysto-space ASP-7 (two agents collided in one VM clone)
last_validated: 2026-10-17
status: active
---

Run each agent that uses `vm-sync.sh` or `vm-gates.sh` from its own host worktree.
Why: the VM clone under `C:\Users\ambytest\src\` is named after the worktree folder, so two agents syncing one worktree overwrite each other's clone.
`vm-gates.sh` also refuses when HEAD moved after launch; treat that refusal as this collision.
