---
title: Keep bot-repo names out of gh arguments; use --body-file for PR text
kind: gotcha
applies_when: when a `gh pr create`, `gh pr comment` or `gh api` call for a private Ambysto repo fails with "Could not resolve to a Repository" or HTTP 404, or its body or title mentions `ambysto/1prompt` or `ambysto-memory`
projects: all
evidence: 2026-11-16 APS-78 (coding-playbook PR #76)
last_validated: 2026-11-16
status: active
---

The `gh` wrapper (`~/.local/bin/gh`) switches to the bot token when ANY argument names `ambysto/1prompt` or `ambysto/ambysto-memory`. That includes a `--body` or `--title` that only mentions such a PR, such as `ambysto/1prompt#9`.
The bot cannot see the private repos, so the call fails as if the repo did not exist ("Could not resolve to a Repository", REST 404), even though `gh api user` prints `ambysto`.
Fix: write the PR text to a file and pass `--body-file <path>`. Keep the bot-repo name out of `--title` (write "1prompt PR 9" instead).
Confirm: `gh pr create … --body-file <file>` prints the PR URL.
