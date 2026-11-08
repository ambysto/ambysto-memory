---
title: Set the threat model and a stop rule before hardening a leak detector
kind: debugging_pattern
applies_when: when writing or extending a heuristic check that scans agent transcripts or commands for forbidden reads (void checks, secret scanners)
projects: all
evidence: 2026-11-08 claudecode-guide APS-45 PR #26 and PR #29 (switch-test.py void-check, three review rounds)
last_validated: 2026-11-08
status: active
---

Before adding rules, write down what the check must catch (an honest agent stumbling on answers) and what it will not (a path built at run time, deliberate evasion), and list the limits in the README.
After every rule change, rerun it on every recorded stream, not only the new fixture: each fix for a missed read added false positives (`ls -la ~ | grep`, `find / -name x`, a heredoc line `/*.yml`, `"$(date)"`).
Stop when a new finding is outside the written threat model; record it as a limit instead of another rule.
Why: three review rounds each found new evasions; without a stop rule the parser kept growing and broke real, clean runs.
Confirm: every recorded clean run still reports clean, and each limit has a line in the README.
