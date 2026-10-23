---
title: Pick the right win11-dev snapshot layer and resync the clock after older ones
kind: reference
applies_when: when restoring or choosing a snapshot of the Windows test VM
projects: all
evidence: 2026-10-16 to 2026-10-22 VM snapshots; global CLAUDE.md machine section
last_validated: 2026-10-22
status: active
---

Default (owner 2026-10-22, also in `~/vms/DEFAULT_SNAPSHOT`): `ambysto-testbed-2026-10-22-apps` = the 2026-10-18 layer plus Chrome, CapCut and Ambysto.Kit.Safety 0.2.0 cached. Restore: `vm-stop.sh && vm-restore.sh <name> && vm-start.sh`.
`ambysto-testbed-wsl-2026-10-22` adds WSL 2 with Ubuntu on E:, for WSL probes only; restore the default before a destructive proof.
Older: `…-2026-10-18` (no Kit.Safety 0.2.0, Chrome, CapCut; has the clock fix), `…-2026-10-17b` (no clock fix), `…-2026-10-17` (no H:), `…-2026-10-16c` (E: Recycle Bin broken, old Kit fixtures), `…-2026-10-16b` (no Defender-excluded test-data folder), `…-2026-10-16` (no G:), `ambysto-baseline-cloud-2026-10-16` (no local NuGet feed), `ambysto-baseline-2026-10-16` (no AmbyCloud, no OneDrive).
After restoring a layer older than `…-2026-10-18` (one without the clock fix), resync first as Ramune: `Start-Service w32time; w32tm /resync /force`; the clock is 7 h fast until then and breaks incremental builds.
`clean-no-globalsign` is Steady's SIC-130 repro (GlobalSign Root CA removed), not an Ambysto baseline.
