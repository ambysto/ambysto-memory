---
title: Restore from the private NuGet feed through vm-ui.sh, not SSH
kind: gotcha
applies_when: when a VM restore fails with NU1301 or "Key not valid for use in specified state"
projects: all
evidence: 2026-10-16 VM provisioning; confirmed 2026-10-18
last_validated: 2026-10-18
status: active
---

The `ambysto` source (GitHub Packages) is read with a `read:packages` token encrypted with DPAPI in ambytest's user NuGet.Config. DPAPI cannot decrypt over SSH (key auth gives the session no password).
Restore anything new from that feed through `vm-ui.sh` (the console session); once a version is in ambytest's global packages folder, SSH builds of it restore from the cache.
Or pull the package on the host with `vm-nuget-pull.sh` into the VM's local feed `ambysto-local`.
The token was added 2026-10-16 and expires about 90 days later, so expect NU1301 everywhere around mid-January 2027.
