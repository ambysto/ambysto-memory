---
title: Reach ambytest's desktop through VNC, never RDP
kind: gotcha
applies_when: when the owner or an agent needs to see or use the VM's console desktop
projects: all
evidence: 2026-10-16 VM provisioning (autologon lost)
last_validated: 2026-10-22
status: active
---

Use VNC :5900 for ambytest's console session.
Why: an RDP logon takes the console session away from ambytest, and an RDP logon plus logoff wipes the autologon secret.
If it happened, re-arm autologon with `vm-autologon.sh` (it reboots the VM), then confirm `vm-status.sh` shows ambytest on the console.
