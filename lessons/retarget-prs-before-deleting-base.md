---
title: Retarget stacked PRs before deleting their base branch
kind: gotcha
applies_when: before deleting a branch that other open PRs use as their base
projects: all
evidence: 2026-10-16 ambysto-kit APS-23; 2026-10-23 APS-36 PRs 2-4
last_validated: 2026-10-23
status: active
---

Point each dependent PR at `main` first: `gh api -X PATCH repos/<owner>/<repo>/pulls/<n> -f base=main`.
Why: deleting a PR's base branch closes the PR on GitHub; it does not retarget it.
Confirm: `gh pr list --state open --json number,baseRefName` shows no PR on the branch about to go.
