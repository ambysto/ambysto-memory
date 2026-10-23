---
title: Judge the agent loop by owner interventions, not credits or first incidents
kind: decision
applies_when: when assessing how well the agent loop works or listing its weaknesses
projects: all
evidence: 2026-10-18 owner, on judging the loop
last_validated: 2026-10-18
status: active
---

Owner decision 2026-10-18: model credits running out are not a loop defect (the owner tops them up); incidents a model could not know on first contact are part of the process.
Measure human involvement: how many times, how often, how long each time (`hil-report.py` in claudecode-guide).
A recurring lesson becomes a gate only if it fits that project; a lesson that holds across contexts goes into the shared guide, not into every repo as a gate.
Why: the goal is a loop with little, measurable human involvement that carries to other projects, not one with no human at all.
