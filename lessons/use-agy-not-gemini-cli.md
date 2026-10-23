---
title: Use the Antigravity CLI (agy) for Google models, not the Gemini CLI (gemini)
kind: decision
applies_when: when running a Google model from the CLI, or when gemini fails with HTTP 401 "API key not valid"
projects: all
evidence: 2026-10-23 APS-36 (owner decision)
last_validated: 2026-10-23
status: active
---

Run Google models through the Antigravity CLI (`agy`, headless: `agy -p "<prompt>" --dangerously-skip-permissions`, global instructions in `~/.gemini/GEMINI.md`), never the Gemini CLI (`gemini`).
Why: the owner decided on 2026-10-23 not to use `gemini` (turned down because its API key on this machine is invalid and fails with HTTP 401 `"API key not valid"`), and to use `agy` for Google models instead.
Confirm: `agy -p "<prompt>" --dangerously-skip-permissions` exits 0 and answers without an HTTP 401 error.
