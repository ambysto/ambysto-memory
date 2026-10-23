---
status: draft   # draft → approved → planned → building → verified → shipped (PR #n)
---
# ambysto-memory: one reviewed memory for every Ambysto session

Ticket: Plane APS-36. Source: owner request, 2026-10-23, after reading the prior art below.

## Problem

What sessions learn does not reach the next session that needs it.

- **Claude Code's auto-memory is keyed by folder path.** On 2026-10-23 it holds 12 items for
  the Ambysto repos: ambysto-space 6, steady 3, ambysto-kit 2, ambysto-gate 1, every other
  repo 0. The dozens of worktrees (`ambysto-space-asp*`, `ambysto-kit-*`) see none of it,
  and neither does the Mac.
- **The same lesson gets learned again.** Reaching Plane over REST (where the key lives, the
  HTTP 403 without a custom User-Agent) is written down twice, in Gate's and in Steady's
  memory. This session found it out a third time while it opened this ticket.
- **Everything else piles up in `~/.claude/CLAUDE.md`.** It is 20 KB and loads in full into
  every session: 8 KB of guide rules and 12 KB of machine facts (the VM's Recycle Bin
  behaviour, ten snapshot layers, the VM state, dated owner decisions). Most of it matters
  only to a few tasks.
- **Nothing tells a stale lesson from a live one.** Snapshot names, tool versions and the
  VM state change; old lines stay until someone notices.

## Outcome

A private repo `ambysto/ambysto-memory`, cloned at `~/work/ambysto/ambysto-memory` beside
the project repos, that every Ambysto session reads:

- `lessons/<slug>.md`, one lesson per file, in a fixed shape:
  - `title`: imperative, under 80 characters, names the tool, file or error;
  - `kind`: `workflow`, `correction`, `debugging_pattern`, `gotcha`, `convention`,
    `decision` (what was decided, why, and the options turned down) or `reference`
    (where something lives);
  - `applies_when`: starts with "when", "before" or "after", and names a trigger a session
    would recognise (a command, a path, an error text);
  - `projects`: the repos it holds for, or `all`;
  - `evidence`: date plus repo, ticket or PR;
  - `last_validated`: the date it was last seen to hold;
  - `status`: `active` or `superseded` (with `superseded_by`);
  - a body of 3–10 lines: what to do, why in one sentence, how to confirm it worked.
- `INDEX.md`: one line per active lesson (title, kind, applies-when), generated, read first.
  Lesson files are opened only when their line matches the task.
- `scripts/check.py` (standard library only) keeps the shape, keeps `INDEX.md` in step with
  the lessons, refuses secret-like text, and lists lessons not validated for 90 days so they
  come back to the owner for review.
- **Recall:** one line in `~/.claude/CLAUDE.md` tells every session to read `INDEX.md`
  before non-trivial work and when a command fails in a way that may have a known fix, and
  to name the lesson it used when one changes what it does. No hook, no tool.
- **Review:** an agent drafts a lesson in a PR; the owner merging the PR is the approval.
- **Migration:** the 12 auto-memory items, and the lessons and machine facts in
  `~/.claude/CLAUDE.md`, each moved into a lesson, kept where they are, or dropped, with
  the owner approving the list item by item. Rules that every session must follow stay in
  `CLAUDE.md`; facts and gotchas a task looks up move out.
- **Auto-memory off.** Per-folder auto-memory is replaced, not kept beside it (owner
  decision 2026-10-23).

## Decisions (owner, 2026-10-23)

1. **No external tool.** Beacon, cass-memory, claude-mem, memorix, beads and the rest were
   read, not installed. We take ideas, not software.
2. **A private GitHub repo of its own**, so the Mac gets the same memory and every change
   has a PR.
3. **v1 scope:** the store, recall, and the migration out of `CLAUDE.md` and auto-memory.
4. **Loaded by one line in `CLAUDE.md`**, not by a hook and not only on demand.
5. **Replace the per-folder auto-memory entirely.**

Ideas taken from the prior art (read 2026-10-23): reviewed lessons kept apart from raw
history and approved by a person, the lesson shape and its five kinds, supersede instead of
delete (agent-beacon); a last-validated date so lessons age (cass-memory); a short index
first and details on demand (claude-mem); decisions recorded with their reasons, and
cross-project scope only when a lesson says so (memorix).

## Success criteria

| # | Criterion | How it is checked |
|---|---|---|
| 1 | Every lesson has the shape above; `INDEX.md` lists exactly the active lessons | `check.py` PASS; mutation: a lesson without `evidence`, an `applies_when` not starting with when/before/after, and a stale `INDEX.md` each make it FAIL |
| 2 | No secret or identifying value in the repo | `check.py` refuses a test token, a hostname and a UUID planted in a lesson (mutation), and passes on the real repo |
| 3 | Each of the 12 auto-memory items and each lesson or fact block in `~/.claude/CLAUDE.md` has an owner-approved fate | a migration table in the plan: item, fate (lesson / stays / dropped), reason, owner tick |
| 4 | `~/.claude/CLAUDE.md` is smaller and lost nothing | its size before and after; every moved line traced to a lesson in the migration table |
| 5 | Auto-memory no longer writes per folder | a fresh session on this machine, asked to remember a fact, writes nothing under `~/.claude/projects/*/memory` |
| 6 | A session in a repo that never had a lesson finds and uses it | a fresh session in a worktree (e.g. `ambysto-space-asp24`) asked to open a Plane ticket reaches Plane with no 403 retry and names the lesson it used |
| 7 | Stale lessons come back | `check.py` lists a lesson whose `last_validated` is set back 91 days (mutation) |
| 8 | The Mac reads the same memory | not run here: Mac, owner step (clone, one session recalls a lesson) |

## Constraints

- Standard library Python only; Markdown files; no daemon, no database, no MCP server, no
  network call beyond git.
- Nothing secret or identifying in the repo (see `CLAUDE.md`, Rules).
- The claudecode-guide block of `~/.claude/CLAUDE.md` is installed from that repo: a change
  there goes through a claudecode-guide PR, not a hand edit. The machine section outside
  the block is edited in place, with a backup.
- Linux machine: Windows work only (global rule). The Mac clone is an owner step.

## Out of scope

- Capturing or storing session transcripts; a distill skill that drafts lessons from the
  owner time log and transcripts (a later ticket, once v1 holds).
- Vector or semantic search; a hook that injects the index; a dashboard.
- Tasks and plans: they stay in Plane and in each repo's `intent/`.
- Rules that hold for one project only: they stay in that project's `CLAUDE.md`.

## Open questions

1. **Machine facts of the Windows VM** (the Recycle Bin table, snapshot layers, VM state):
   proposed to move into `reference` and `gotcha` lessons, keeping in `CLAUDE.md` only the
   rules (run in the VM as ambytest, never on the host; the lock rule; never read the guest
   password). Confirm, or keep the whole VM section in `CLAUDE.md`.
2. **Where the recall line lives:** proposed in the claudecode-guide global block (one
   APS-36 PR there), so a reinstall keeps it. The alternative is the machine section, which
   the Mac does not have.
3. **How auto-memory is replaced.** This Claude Code build has an `autoMemoryEnabled`
   setting and an `autoMemoryDirectory` setting (seen in the binary, 2026-10-23; behaviour
   not tested yet). Proposed: `autoMemoryEnabled: false`, so every lesson goes through a PR.
   The alternative is `autoMemoryDirectory` pointed at one shared folder: the harness would
   load its index on its own, but sessions would write lessons there with no review, in the
   harness's format.
