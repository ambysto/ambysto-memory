---
title: Put every file meant for the Windows VM on its Desktop
kind: convention
applies_when: when copying a build, release zip or script into the Windows test VM
projects: all
evidence: 2026-10-16 owner, Steady SIC-130 ("every file from now on should be like this")
last_validated: 2026-10-16
status: active
---

Download on the Linux host first (for example `gh release download`), then `scp <file> "win11:C:/Users/Ramune/Desktop/"`, and compare the hash on both sides.
Why: the owner finds test builds in one place.
Do not download inside the VM with PowerShell or a browser while testing TLS: Windows then fetches roots and spoils the test.
