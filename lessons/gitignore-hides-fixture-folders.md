---
title: Check git check-ignore when adding fixture folders
kind: gotcha
applies_when: when adding a folder named fixtures, build, out or similar to a repo
projects: all
evidence: 2026-10-17 ambysto-space ASP-7 (a `fixtures/` line hid every `scripts/fixtures/`)
last_validated: 2026-10-17
status: active
---

Run `git check-ignore -v <new path>` before relying on the files being committed.
Why: a bare `fixtures/` line in `.gitignore` matches that name at every depth, so new fixture files were silently left out of commits.
Confirm: `git status` lists the new files as untracked or staged.
