---
title: In a systemd unit, run side effects in the foreground; detached ones die
kind: gotcha
applies_when: when code that runs in a systemd service or a `systemd-run` unit starts a detached child (Popen with start_new_session, `&`, nohup) to post a comment, notify or write a log
projects: all
evidence: 2026-11-11 coding-playbook APS-59 PR #58 (hard review rounds 1 and 2)
last_validated: 2026-11-11
status: active
---

When a oneshot service or a `systemd-run` unit ends, systemd kills every process in its cgroup, detached or not. A ticket comment started with `Popen(..., start_new_session=True)` from a loop hook was killed before it reached Plane.
Do the side effect in the foreground with a timeout (`subprocess.run(..., timeout=30)`), or start it as its own unit (`systemd-run --user --collect --no-block ...`).
Why: the same hook ran fine from an interactive session, so the bug showed only in a woken session that ran inside a unit.
Confirm: run the path inside a real unit (`systemd-run --user --wait ...`) and check that the side effect landed after the unit ended.
