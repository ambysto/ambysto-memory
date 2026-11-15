---
title: Verify repository ownership, GitHub identity and network separately
kind: workflow
applies_when: before writing to GitHub or diagnosing a failed GitHub operation
projects: all
evidence: 2026-10-26 sitting-time SIT-21 / PR 9
last_validated: 2026-10-26
status: active
---

Read the repository's `AGENTS.md` and `CLAUDE.md`, then inspect `git remote -v` to identify its owner; never infer ownership from the workspace or another repository.
Before a GitHub write, check the active CLI identity and that the selected tool has write access to this exact repository; do not use a connected account that belongs to another owner.
When DNS or socket operations fail, check whether the execution environment restricts networking before diagnosing credentials, repository visibility or permissions; do not ask the owner to repeat the same failing command.
Use an authorized networked terminal only for the operation the current environment cannot perform, then verify the resulting remote state before reporting completion.
Why: repository ownership, tool identity and environment network access are separate facts; a failure in one does not establish a failure in another.
