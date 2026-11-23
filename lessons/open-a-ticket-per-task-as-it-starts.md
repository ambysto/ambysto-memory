---
title: Open and move one ticket per task as it starts, not one umbrella ticket
kind: correction
applies_when: when a session finishes several tasks in a repo that has a tracker project and only one ticket is open
projects: all
evidence: 2026-11-23 agentsocial, 16 tasks shipped under a single ticket, owner objected, tickets made afterwards
last_validated: 2026-11-23
status: active
---

Create the ticket when a task is rated and starts, set it In Progress, link each PR as it opens, set Done after the live check. One task, one ticket; a plan with tasks gets one ticket for the plan and the tasks as its steps.
Waiting until the end makes a batch of calls that the tracker rate-limits (HTTP 429), and the history says nothing about when things happened.
For a backlog already shipped: create the tickets with the PR links and a one-line comment each, plus Backlog tickets for what waits for the owner or the design agent.
Confirm: every PR in the summary appears in some ticket, and no ticket is Done without a link.
