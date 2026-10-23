---
title: Port Windows apps in order: Lean, Kit Process, DevBox, Optimer, Power, Tune
kind: decision
applies_when: when choosing which Ambysto app to port to Windows next
projects: all
evidence: 2026-10-19 owner decision; 2026-10-22 key decision
last_validated: 2026-10-22
status: active
---

Order (owner 2026-10-19): Lean v1 (pilot, first release) → Kit Process → DevBox → Optimer → Power → Tune. Gate and Steady are not assessed; their step [0] places them. Why: first the apps that reuse most of the Kit, the riskiest last.
Kit Process (.NET, from the Kit's `docs/spec/process.md`): a new APS ticket, HARD, the same loop as APS-24 (close APS-24 first). Probes: pid + start time as identity; other users and admin unreadable; listeners via `GetExtendedTcpTable`; energy and wakeups *absent*, never 0. Lean's own process reading (app-gone, `NtQuerySystemInformation`) is a candidate to move into it.
DevBox (Process, Safety): the first consumer, so it proves Kit Process. Optimer (Process, Safety): cache cleanup reuses Lean's and the Kit's recycle path.
Power (Process usage fields): energy, battery and keep-awake work differently on Windows; expect many step [0] questions.
Tune (License, Safety, maybe a new Kit capture/restore piece): highest risk, it writes system settings and the registry; after Lean ASP-8, so the registry, UAC and restore lessons come first.
The next app's step [0] may run while the current one builds; builds run one app at a time (one VM, one lock). The Windows suite bar comes once two or more Windows apps exist (after DevBox).
After each app, run `hil-report.py --project <app>`: owner interventions should fall from app to app.
Superseded detail: "the signing key is due before Lean's Pro release" was replaced on 2026-10-22 by lesson `license-key-plan` (Free ships first).
