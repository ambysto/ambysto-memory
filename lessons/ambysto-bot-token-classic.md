---
title: Renew the ambystobot token as a classic token with the repo scope
kind: gotcha
applies_when: when a push or `gh` call in `ambysto-memory` fails with `Authentication failed` or `Bad credentials (HTTP 401)`
projects: all
evidence: 2026-11-24 ambysto-memory PR #52 (token file dated 2026-10-23 had expired)
last_validated: 2026-11-25
status: active
---

A 401 there means the bot token in `~/.config/ambysto-bot/token` expired or was revoked; it is an owner-only step, and the session must not fall back to the `ambysto` account.
Tell the owner: sign in as `ambystobot`, open https://github.com/settings/tokens/new (Tokens (classic)), tick only `repo`, generate, then run in a terminal on this machine:
`read -rs T && printf '%s' "$T" > ~/.config/ambysto-bot/token && chmod 600 ~/.config/ambysto-bot/token && unset T && echo saved`
Do not send the owner to fine-grained tokens: the bot is a collaborator, not a member of the `ambysto` org, so that page only offers `ambystobot` as resource owner (the owner hit this on 2026-11-24).
Confirm: `gh api user --jq .login` run inside the `ambysto-memory` clone prints `ambystobot`, and `stat -c %y` on the token file shows today.
