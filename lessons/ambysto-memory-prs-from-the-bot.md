---
title: Open ambysto-memory PRs as ambystobot so the owner can approve them
kind: gotcha
applies_when: when opening or merging a PR in `ambysto-memory`, or when `gh pr review --approve` fails with "Can not approve your own pull request"
projects: all
evidence: 2026-11-24 ambysto-memory PR #51 (opened as ambysto, merged with --admin) and PR #52 (opened as ambystobot, approved by the owner)
last_validated: 2026-11-25
status: active
---

`main` there needs a code-owner review from `@ambysto`. GitHub refuses that review on a PR the `ambysto` account opened, so the owner's "merge" then only works with `--admin`, which skips the protection.
Open these PRs from the clone or a worktree named `ambysto-memory-*` without `AMBYSTO_OWNER=1`, so the `gh` wrapper uses the bot; check with `gh pr view <n> --json author -q .author.login` (must be `ambystobot`).
When the owner says "merge <n>": `AMBYSTO_OWNER=1 gh pr review <n> --approve -b "Approved by the owner (merge <n>)."`, then `AMBYSTO_OWNER=1 gh pr merge <n> --merge --delete-branch`.
A PR the `ambysto` account already opened: tell the owner it needs `--admin` (or a new PR from the bot) before merging.
