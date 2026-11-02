---
title: Default UI, CLI, docs and code to English; keep Vietnamese optional
kind: convention
applies_when: when building or editing UI copy, CLI output, documentation, or code in any repo
projects: all
evidence: 2026-11-02 owner ("mọi thứ chúng ta làm default language là Eng, Vi chỉ là optional")
last_validated: 2026-11-02
status: active
---

Default every product UI, CLI, documentation file, and code identifier/comment to English (`en`), even when the owner chats in Vietnamese.
Offer Vietnamese (`vi`) only as an optional toggle or locale (`lang = 'en'` by default).
Why: the owner requires English as the primary product and engineering language across all repositories, with Vietnamese kept strictly optional.
Confirm by checking that initial HTML/UI state (`lang="en"`), CLI help/output, and README files render in English out of the box.
