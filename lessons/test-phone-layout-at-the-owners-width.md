---
title: Test a phone layout at the owner's width and after adding to a bar
kind: gotcha
applies_when: when a change adds a button or text to a fixed header or nav bar, or the owner sends a phone screenshot
projects: all
evidence: 2026-11-23 agentsocial, a new language button made the logo word collide with Try free at 390 px; the owner's phone is about 440 px wide
last_validated: 2026-11-23
status: active
---

Divide the screenshot's pixel width by its device scale to get the owner's CSS width (a 1320 px shot at 3x is 440 px) and test that width plus 360 and 390.
After adding to a bar, measure with the browser: right edge of the brand text must be left of the controls, and `scrollWidth` must equal the viewport width.
When there is no room, move the least needed control into the menu at the narrow widths (a Try free that the menu already has) instead of shrinking everything.
Fixed side margins can leave empty bands: set the bar to the full width on phones.
Confirm: three widths measured with no overlap, and a screenshot of the bar at the owner's width.
