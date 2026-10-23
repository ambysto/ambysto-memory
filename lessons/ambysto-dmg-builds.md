---
title: Find built macOS .dmg files in the ambysto-assets release
kind: reference
applies_when: when a task needs an Ambysto app's macOS build or a session says an app has no build
projects: all
evidence: 2026-10-23 ambysto-tune (Tune landing download)
last_validated: 2026-10-23
status: active
---

The unsigned .dmg builds of Tune, Lean, Optimer, DevBox, Power and Steady are attached to release `dmgs-2026-10-15` in the private repo `ambysto/ambysto-assets`; the release body lists build time and SHA-256 prefix per file.
The Linux host cannot build macOS apps, so look there before saying an app has no build.
The Tune landing (tune.ambysto.com) serves `site/dl/AmbystoTune.dmg`, copied from `AmbystoTune-0.1.0-7e09aa7.dmg`; the file is gitignored, so put it back into `site/dl/` before every deploy of `site/`.
