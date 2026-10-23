---
title: Expect IFileOperation to delete for good while it reports success
kind: gotcha
applies_when: when code or a test sends files to the Windows Recycle Bin
projects: all
evidence: 2026-10-16 VM probes; ~/vms/README.md probe table
last_validated: 2026-10-16
status: active
---

`PerformOperations` returns S_OK yet deletes for good: removable (F:) and network (`\\localhost\ambynet`) items, online-only cloud files, an item over the bin quota, `NukeOnDelete`/`NoRecycleFiles`, a long path on a volume without 8.3 names.
Recycling a folder downloads its online-only children; a large recycle silently purges older bin items.
A folder with a descendant path of 260+ characters is deleted for good as a whole unless every `PreDeleteItem` without the recycle flag (children included) is aborted.
`PostDeleteItem` with no new item means it did not reach the bin; a reported item matched in every re-check, but still open it and compare identity.
VB `FileSystem.DeleteFile(SendToRecycleBin)` deletes for good from an SSH (session 0) process even on C:; `IFileOperation` recycles there. Run Recycle Bin tests through `vm-ui.sh` anyway.
