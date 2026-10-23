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
Why: the owner does not use the Gemini CLI (decision 2026-10-23); on this machine it also fails with HTTP 401 `"API key not valid"`, while `agy` works.
Confirm: `agy -p "<prompt>" --dangerously-skip-permissions` exits 0 and answers without an HTTP 401 error.
