---
title: Port Windows apps in order: Lean, Kit Process, DevBox, Optimer, Power, Tune
kind: decision
applies_when: when choosing which Ambysto app to port to Windows next
projects: all
evidence: 2026-10-19 owner decision; 2026-10-22 key decision
last_validated: 2026-10-22
status: active
---

Order: Lean v1 (pilot, first release) → Kit Process (.NET, from the Kit's `docs/spec/process.md`; close APS-24 first) → DevBox → Optimer → Power → Tune (after Lean ASP-8, for the registry, UAC and restore lessons). Gate and Steady are not assessed; their step [0] places them.
Why: first the apps that reuse most of the Kit; the riskiest (Tune writes system settings) last.
The next app's step [0] may run while the current one builds; builds run one app at a time (one VM, one lock).
The Windows suite bar comes once two or more Windows apps exist (after DevBox).
After each app, run `hil-report.py --project <app>`: owner interventions should fall from app to app.
Superseded detail: "the signing key is due before Lean's Pro release" was replaced on 2026-10-22 by lesson `license-key-plan` (Free ships first).
