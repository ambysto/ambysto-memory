# ambysto-memory: shared, owner-reviewed memory for every Ambysto repo (Plane APS, GitHub ambysto/ambysto-memory)

## What it does
Holds the lessons, decisions and references that every Ambysto session needs, whatever repo or worktree it runs in, on the Ubuntu machine and the Mac. One file per lesson in `lessons/`, one line per lesson in `INDEX.md`. Sessions read `INDEX.md` before non-trivial work and open the lessons that match. Private. Standard library Python only. The design is in `intent/2026-10-23-ambysto-memory.md`.
Cost of a bug: a wrong or stale lesson is followed by every later session, silently; a lesson moved out of `CLAUDE.md` and lost is guidance no session gets any more; a secret written here reaches GitHub.

## Verify
- `python3 scripts/check.py`: every lesson's frontmatter and shape, `INDEX.md` equal to the lessons, no secret-like text, stale lessons listed (from the plan; not written yet).
- Owner-only or other-machine checks: cloning on the Mac and a Mac session reading the memory ("not run: Mac, owner step").

## HARD: the main session does it directly, then hard-reviewer
- Moving or deleting guidance out of `~/.claude/CLAUDE.md`, the claudecode-guide global block, or a project's `CLAUDE.md`.
- Turning Claude Code's per-folder auto-memory off, or anything else that changes what loads into every session.
- The lesson format and what `check.py` refuses (the secret check above all).

## MEDIUM: builder builds, reviewer reviews
- `check.py` changes outside the secret check; README and the recall instructions' wording when it changes what a session does.

## EASY: transcriber or builder, no review
- Typos, `INDEX.md` regenerated from unchanged lessons, README wording.
- A new or superseded lesson needs no agent review: the owner reviews its PR, and the merge is the approval.

## Rules
- A lesson reaches `main` only through a PR the owner merges. Agents draft; they never approve.
- Supersede, never delete: an outdated lesson gets `status: superseded` and `superseded_by`, and stays.
- Nothing secret or identifying: no keys, tokens, passwords, hostnames, workspace slugs, project or account ids. Say where the value lives instead ("the Plane base URL in `~/.claude.json`, `plane` server env").
- Every lesson names its evidence (date, repo, ticket or PR). No evidence, no lesson.
- Git: English only; the `ambysto` account (`gh api user --jq .login` before the first PR of a session; if it is not `ambysto`, stop and ask; never `gh auth switch`); repo-local author `Ambysto`; branches `aps-NN-slug`, never a push to `main` (the skeleton commit was the only one); commits "Summary (APS-NN)" with no Co-Authored-By trailer, PR bodies with no "Generated with" line; do not merge without being asked.
- Issue tracker: Plane, project APS, written in English. Each ticket gets a GitHub issue titled `[APS-NN] …`; a phase PR body starts with "Part of #<issue>. Plane: APS-NN.", and only the last PR of a ticket says "Closes #<issue>". Never put the Plane host or ids on GitHub.

## Session state
- Work in progress lives in `HANDOFF.md` (gitignored). If it exists at session start, read it before anything else. Update it with `/handoff` before `/clear`; delete it once the goal is finished and recorded.
- Durable facts go in this file or in `lessons/`, tasks in the tracker. `HANDOFF.md` holds only where the current goal stands.
