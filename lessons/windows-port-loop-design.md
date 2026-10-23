---
title: Build each Windows app through steps [0] to [5] of the port loop
kind: decision
applies_when: when starting or running the Windows port of an Ambysto app
projects: all
evidence: 2026-10-16 owner and agent design (Kit APS-24, Lean ASP-7)
last_validated: 2026-10-17
status: active
---

[0] spec audit per repo, one batched list of owner questions in a draft intent; [1] acceptance tests from the spec, by an agent other than the builder.
[2] plan with tasks rated EASY/MEDIUM/HARD; [3] per task: builder, then machine gates (0-warning build, tests in the VM as ambytest, banned-API grep, copy-lint, Stryker on safety code), then reviewer, at most 2 fix rounds; blocked questions queue instead of interrupting.
[4] real-disk proofs in the VM after restoring the default snapshot (`vm-gates.sh --fresh`); [5] the owner merges per phase.
Why: quality comes from executable gates, and ambiguity is front-loaded into one owner batch, so the loop runs with few interruptions.
