---
title: Put Proof outcome tags (O1, O2) on the first line for sdlc-check converge
kind: gotcha
applies_when: when `sdlc-check.py converge <plan>` reports an outcome with no Proof item although the plan's `## Proof` names it
projects: all
evidence: 2026-11-24 aipub plan 2026-11-24-app-publisher-studio.plan.md, AIPUB-56
last_validated: 2026-11-25
status: active
---

`converge` reads the outcome tags only from the first line of each numbered Proof item.
Write `1. node labs/app/check.mjs exit 0 … (O1, O2, O3)` with the tags on that first line, or keep the item to one line; tags on a wrapped second line are not seen.
Confirm: `python3 ~/work/0xdonniechu/coding-playbook/tools/sdlc-check.py converge <plan>` prints PASS with 0 gaps.
Why: the aipub plan listed every outcome but `converge` reported them missing until the tags moved up.
