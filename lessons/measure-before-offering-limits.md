---
title: Measure the worst cases end to end before offering a performance limit
kind: correction
applies_when: before asking the owner to choose a time budget, work counter or size cap
projects: all
evidence: 2026-10-21 ambysto-search group 3 (6 review rounds)
last_validated: 2026-10-21
status: active
---

Probe the known worst inputs through the real entry point, at small and full size, timing parse, query and post-processing separately.
Offer only the options the numbers support, with the numbers in the question.
Why: twice an option ("deterministic counts") was offered and picked, then measurements showed callback counts do not track time; each wrong option cost the owner a decision and a round.
Confirm: every option in the question cites a measured case.
