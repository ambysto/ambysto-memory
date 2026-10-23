---
title: Drive the Windows VM through the ~/vms/bin scripts
kind: reference
applies_when: when building, testing or running a job in the Windows test VM
projects: all
evidence: 2026-10-16 to 2026-10-22 ~/vms tooling
last_validated: 2026-10-22
status: active
---

`vm-status.sh` first in every agent run. `vm-gates.sh <repo-dir>` runs the suites in the repo's `windows/gates.json` (exit 0 only when every gate passed).
`vm-sync.sh <repo-dir> [branch]` mirrors a host branch into `C:\Users\ambytest\src\<repo>` (the VM copy is reset); a plain `git push win11:…` fails because the Windows SSH shell is `cmd.exe`.
`vm-ps.sh [-u test] [-7] -` runs PowerShell from stdin with no `cmd.exe` quoting trouble; `vm-ui.sh <job.ps1>` runs a job in the interactive console session; `vm-screenshot.sh` grabs the console.
`vm-nuget-pull.sh <PackageId> <version>` downloads on the host (read-only token in `~/vms/secrets/`) into the VM feed `ambysto-local`.
`vm-stop.sh` holds every job runner's lock and refuses while a job runs; never stop the VM another way.
