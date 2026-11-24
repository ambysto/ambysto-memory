---
title: Bulk tracker calls hit HTTP 429: retry with a pause, check the new id
kind: gotcha
applies_when: when a script creates or updates many Plane tickets in a row with tools/plane.py
projects: all
evidence: 2026-11-23 agentsocial, 13 creates in a loop, the 429 text was stored as the new ticket id
last_validated: 2026-11-23
status: active
---

Run the loop as a script in the background with a log, and wait on it with a monitor; a foreground `sleep` is refused.
Wrap every call: on "HTTP 429" sleep 20 seconds and retry (up to 8 times), and pause 2 to 3 seconds between calls.
After `create`, accept the result only if it looks like `PROJ-<number>`; otherwise stop for that ticket. A script that keeps the error text as the id sets states and links on nothing.
Confirm: `plane.py show` on the first and last new ticket prints the state you set.
