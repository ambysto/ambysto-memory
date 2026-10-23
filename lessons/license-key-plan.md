---
title: Ship Free first; the owner makes every production key on the Mac at the end
kind: decision
applies_when: when a Windows app's intent or plan touches licensing, Pro or keys
projects: all
evidence: 2026-10-16 owner decision; 2026-10-22 owner decision (Free first)
last_validated: 2026-10-22
status: active
---

Every Windows app builds on the Kit's .NET library `Ambysto.Kit.License` (0.1.2 or later, GitHub Packages); it trusts no key until the production signing key exists.
The key is created by the owner on the Mac, never by an agent and never on the Linux machine, then added to the Swift and .NET copies in one PR (`scripts/check-key-sets.py`) and released as a minor Kit version.
Owner decision 2026-10-22 (replaces "due before the first release with Pro"): apps ship Free first, usable without a key; the owner makes the keys for every product in one go once all products are done.
The key blocks only Pro (selling or gifting keys, gift keys included), not a Free release; every Windows app intent lists it as a Pro blocker.
Apps test entitlement through their own verifier seam, never with a real key.
