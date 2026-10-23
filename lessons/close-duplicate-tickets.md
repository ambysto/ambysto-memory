---
title: Close a duplicate ticket as Cancelled with a link, without asking
kind: convention
applies_when: when a Plane or GitHub ticket exactly duplicates another
projects: all
evidence: 2026-10-23 owner, ambysto-space ASP-23 = ASP-24 ("trùng thì đóng thôi, giữ làm gì")
last_validated: 2026-10-23
status: active
---

Set the duplicate to the project's Cancelled state in Plane (look the state up by name in `GET projects/<id>/states/`) with a comment naming the ticket kept; close a GitHub duplicate with a link the same way. Do not ask first.
Why: asking about it cost the owner time.
Before telling anyone a ticket is open, check its state's name, not just that it exists: ASP-21 was Cancelled and was wrongly offered as free.
