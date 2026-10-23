---
title: Run OpenCode headless with the Orca account's data folder and --standalone
kind: workflow
applies_when: when a headless `opencode run` fails with "Invalid credential", "Endpoint is unavailable" or a deprecated model
projects: all
evidence: 2026-10-23 APS-36 proof 10 (OpenCode signed in through Orca)
last_validated: 2026-10-23
status: active
---

The owner signs OpenCode in through `orca account add --agent opencode`; Orca keeps that login in a private data folder, `~/.config/orca/managed-data-accounts/opencode/<id>/data`. The config folder stays `~/.config/opencode`.
Run: `XDG_DATA_HOME=<that data folder> opencode run --standalone --auto --model opencode-go/<model> "<prompt>"`. Without `--standalone` the run goes through the background service, which has the default data folder and no credential.
The default free models (`exo-free`, `flint-40b-free`) were deprecated or unavailable on 2026-10-23; list the paid ones with `XDG_DATA_HOME=<…> opencode models`.
Confirm: the run exits 0 and answers.
