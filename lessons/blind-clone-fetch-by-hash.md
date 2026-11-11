---
title: Fetch one commit by hash when a clone must not see later history
kind: gotcha
applies_when: when cloning a local repo at an old commit for a blind test, an eval or a replay that must not see the fix or the answers
match: git\s+clone\b[^\n]*\s(/|~/|\.\.?/|file://)
projects: all
evidence: 2026-11-08 claudecode-guide APS-45 PR #26 (switch-test clones carried the kit's branch)
last_validated: 2026-11-08
status: active
---

Do not use `git clone` (even `--no-local` or detached): it copies every branch and tag, so `git log --all` reaches later commits.
Use `git init <dir>`, then `git -C <dir> fetch --no-tags file://<source> <full commit hash>` and `git -C <dir> checkout --detach FETCH_HEAD`, then delete `.git/FETCH_HEAD`.
Why: the switch test's reviewer clones carried the branch holding the known findings, one `git log --all` away from the answers.
Confirm: `git -C <dir> branch -a` and `git -C <dir> tag` print nothing and `git -C <dir> log --all --oneline | head -1` is the case's commit.
