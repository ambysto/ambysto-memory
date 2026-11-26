---
title: Start gh for an Ambysto repo with cd into it; never ask the owner to switch
kind: gotcha
applies_when: when a `gh` call for a private Ambysto repo fails with HTTP 404 or "Could not resolve to a Repository" and the command did not start with a `cd`, or before you ask the owner to change the GitHub account
projects: all
evidence: 2026-11-26 aipub-landing PR 103 session (the owner switched the account by hand twice for nothing)
last_validated: 2026-11-26
status: active
---

The `gh` wrapper (`~/.local/bin/gh`) uses the `ambysto` account only when the command runs in a folder under `~/work/ambysto/` (`pwd -P`); anywhere else it uses the active keyring account, the owner's personal one. Claude Code returns the shell to the project folder after every command, so a `gh` call that does not begin with `cd ~/work/ambysto/<repo> &&` in the same command can run as the personal account and get a 404 on a private Ambysto repo.
Fix: begin every `gh` command for an Ambysto repo with `cd ~/work/ambysto/<repo> &&`, in that same command. Never ask the owner to switch accounts and never run `gh auth token`: the keyring is fine, and a wrong switch breaks every folder outside `~/work/ambysto/`.
If the personal account is no longer the active one, the only switch an agent may run is back to it, as the whole command with nothing before or after it (`owner-token-guard` allows exactly that since 2026-11-26).
Confirm: `cd ~/work/ambysto/<repo> && gh api user --jq .login` prints `ambysto`; from another folder it prints the personal account.
