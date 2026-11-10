---
title: Do not edit any tree a running builder or reviewer reads, not only its own
kind: gotcha
applies_when: when a builder or reviewer runs in the background and the main session is about to edit, commit or merge in the same repo
projects: all
evidence: 2026-11-10 claudecode-guide APS-51 PR #43 (one builder OUTSIDE CONTRACT stop, two reviewers TREE CHANGED)
last_validated: 2026-11-10
status: active
---

agent-guard snapshots every git work tree an agent touches, reads included, and compares it after each tool call. An edit, commit or merge by the main session in that tree shows up as the agent's change.
So while a builder or reviewer runs, leave alone every tree it reads, the main checkout included when its plan, intent or diff lives there. Do the other work in a separate worktree (`dispatch.py new`, or `git worktree add`), or wait for the notification.
Point a reviewer at a commit (`git show <sha>:<path>`, a diff range) so it has no reason to read the moving working tree.
Why: in APS-51 a README edit in the main checkout locked a builder that only read its plan there (OUTSIDE CONTRACT), and a T4 commit plus a merge gave both reviewers TREE CHANGED; no harm, but each stop cost a judgment and a round of explaining.
Confirm: the agent's report has no OUTSIDE CONTRACT or TREE CHANGED line that names a path you changed.
