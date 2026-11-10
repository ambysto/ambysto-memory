---
title: Prove a changed ~/.claude/agents file in a new session, not the installing one
kind: gotcha
applies_when: when a live proof runs a subagent right after its file in ~/.claude/agents/ (model, effort, hooks, body) was installed or edited in the same session
projects: all
evidence: 2026-11-08 APS-46 (claudecode-guide #35, #36)
last_validated: 2026-11-08
status: active
---

Claude Code reads agent files when a session starts; a session that installs or edits `~/.claude/agents/<name>.md` keeps dispatching the old definition until it ends.
Run the live proof in a new session: ask the owner to start one, or run it headless from the session, e.g. `claude -p --model claude-haiku-5-5 --permission-mode acceptEdits --allowedTools "Agent Bash Read Write Grep Glob" < prompt.txt`, with a prompt that makes one Agent call to the subagent and prints its report (a headless run writes no owner time log line).
Why: in APS-46 the installing session's builder still ran its old frontmatter (one Bash hook), so a planted write outside the task contract went through unblocked; the same test in a fresh session locked at once.
How to confirm: the proof shows the new behaviour (a new hook's refusal or state file, the new model in the run), not just the absence of the old one.
Until that new session, say in the summary that the change is installed but not yet live in the current session.
