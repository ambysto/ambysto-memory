---
title: Prove an app never hydrates cloud files with AmbyCloud and the test OneDrive
kind: reference
applies_when: when a test must prove an app does not download or recycle cloud placeholders
projects: all
evidence: 2026-10-16 VM probes (console session)
last_validated: 2026-10-16
status: active
---

`C:\Ambysto\tools\AmbyCloud\AmbyCloud.exe` (source and self-test in `~/vms/tools/AmbyCloud`; `~/vms` is a local git repo) creates real Cloud Files API placeholders and logs every fetch with the reader's pid.
OneDrive in the VM is signed in for ambytest with the owner's test Microsoft account only.
Probe: an online-only file sent to the Recycle Bin (AmbyCloud or real OneDrive) is not in the local bin; a hydrated one is. Table in `~/vms/README.md`.
