---
title: When a green check hides a defect, name what the check never measured
kind: correction
applies_when: when the owner reports a visual or product defect on something whose checks were green
projects: all
evidence: 2026-11-23 agentsocial, owner found wrong badge art, a stale second Facebook icon and a split hero background that every check passed
last_validated: 2026-11-23
status: active
---

Say which check was green and what it does not measure, in one line, before fixing the defect ("brand check measures text colours; nobody compared the character").
Then fix it with one of: a new check if the defect can be measured (a 390 px scan found the one hero whose background image covered only part of the box), a named human step if it cannot, or a list for the owner.
Never write "all checks pass" as the summary of quality; write what was checked and what was only looked at, and "not run" for the rest.
Re-baseline a count check only with the reason beside the number, in the same change.
Confirm: the report lists what is not measured, and the defect now fails something or has an owner.
