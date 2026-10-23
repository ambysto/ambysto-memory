---
title: Give a reviewer a diff range instead of letting it check out
kind: workflow
applies_when: when sending a reviewer or hard-reviewer to review a branch
projects: all
evidence: 2026-10-16 ambysto-kit APS-23 (a reviewer checked out main mid-review)
last_validated: 2026-10-23
status: active
---

Pass the range in the prompt (`git diff main..<branch>`) and tell it to read files with `git show <branch>:<path>`, never to check out.
Why: reviewers share the working tree; one that switched branches made the next `git commit --amend` rewrite the wrong branch.
Confirm: `git branch --show-current` after the review still prints the branch you were on.
