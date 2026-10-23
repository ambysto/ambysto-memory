---
title: Pass --integration when adding an OpenCode account non-interactively
kind: gotcha
applies_when: when running orca account add --agent opencode without an interactive terminal
projects: all
evidence: 2026-10-23 APS-36 (OpenCode account add in non-interactive shell)
last_validated: 2026-10-23
status: active
---

Run non-interactive account addition with `--integration <id>`: `orca account add --agent opencode --integration <id>`. In a real interactive terminal, the flag is not required.
Without an interactive terminal, `opencode auth login --standalone` cannot show its picker and fails with "Pass an integration ID or name when running without an interactive terminal".
Confirm: `orca account list` shows the OpenCode account.
