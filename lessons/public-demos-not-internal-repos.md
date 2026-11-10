---
title: Illustrate public landings with famous open-source repos and live HTML demos
kind: correction
applies_when: when illustrating an app or tool landing page with code graphs, diagrams or examples
projects: all
evidence: 2026-10-25 ambysto-graph APS-40
last_validated: 2026-10-25
status: active
---

Never use Ambysto's own repositories or internal system architecture to illustrate a public landing page or demo.
Render diagrams and examples from well-known open-source repositories (such as Express, FastAPI or Next) so visitors recognise the structure immediately and internal systems stay private.
On dark landing pages, render diagram previews with `--theme light` for contrast, and pair static preview images with links to live standalone `.html` demos so visitors can hover nodes and test keyboard shortcuts in the browser.
Why: the owner does not want outsiders to see Ambysto's internal structure, and static screenshots alone undersell interactive HTML output.
Confirm: every landing diagram and `.html` demo cites only public open-source paths and opens with working hover and keyboard controls.
