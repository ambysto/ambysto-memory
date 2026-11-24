---
title: Write ambysto-graph flow IR as kind workflow or sequence, without step numbers
kind: gotcha
applies_when: when writing a `*.flow.json` or any IR for `ambysto-graph validate` / `render` (user flow, sequence with `alt` or `loop`)
projects: all
evidence: 2026-11-24 aipub intent 2026-11-24-app-publisher-studio (four flows), PR #45
last_validated: 2026-11-24
status: active
---

Use `"kind": "workflow"` with `nodes` and `links`, or `"kind": "sequence"` with participants and `steps`; branches go in a step with `"fragment": "alt"` and `branches`, repeats in `"fragment": "loop"`.
Do not write the old `"mode": "workflow"` shape: `validate` refuses it.
Do not number steps in their labels ("1. Gửi mã"): the renderer numbers sequence steps itself, so hand numbers show twice.
Run `ambysto-graph validate <ir>.json` before `render <ir>.json -o <file>.html`, then open the HTML once.
Why: the aipub session lost two render rounds to the old shape and doubled numbers.
