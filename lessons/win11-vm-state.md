---
title: Check the win11-dev VM's installed tools and volumes
kind: reference
applies_when: when a VM task depends on an installed SDK, tool, volume or policy
projects: all
evidence: 2026-10-16 VM provisioning
last_validated: 2026-10-16
status: active
---

Windows 11 Enterprise LTSC Evaluation (build 26100, expires 2027-01-13). .NET SDK 10.0.402 machine-wide and first on PATH (8.0.426 beside it, ends 2026-11-10), PowerShell 7.6.7, VS Build Tools 2026 18.11 (MSBuild, C++, Windows SDK 10.0.26100 with signtool and makeappx), Sysinternals on PATH, Stryker.NET 5.0.0 for ambytest, Python 3.12, git 2.56. No winget.
Volumes: C: NTFS (about 49 GB free), E: NTFS second disk (64 GB), F: FAT32 removable (8 GB), G: exFAT fixed (4 GB), H: NTFS removable (4 GB, `AMBYSTO_REMOVABLE_NTFS=H:\` for ambytest), `\\localhost\ambynet` loopback share, Z: virtio CD.
Long paths off (`C:\Ambysto\bin\set-longpaths.ps1 0|1` as Ramune). Defender on; only build trees and NuGet caches excluded.
ambytest may enumerate services on the SCM, so `dotnet --info` and Stryker work over SSH (old SDDL in `C:\Ambysto\scmanager-sddl.orig.txt`).
Steady 1.0.2 is installed and the GlobalSign Root CA is absent (left from Steady's repro).
