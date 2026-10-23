---
status: approved  # draft → approved → planned → building → verified → shipped (PR #n)
---
# ambysto-memory: one reviewed memory for every Ambysto session

Ticket: Plane APS-36. Source: owner request, 2026-10-23, after reading the prior art below.

## Problem

What sessions learn does not reach the next session that needs it.

- **Claude Code's auto-memory is keyed by folder path.** On 2026-10-23 it holds 13 items for
  the Ambysto repos: ambysto-space 6, steady 3, ambysto-kit 2, ambysto-gate 1, ambysto-tune 1
  (written that morning), every other repo 0. The count moves while sessions run. The dozens of worktrees (`ambysto-space-asp*`, `ambysto-kit-*`) see none of it,
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
  the lessons, refuses secret or identifying text (defined below), and lists lessons not
  validated for 90 days so they come back to the owner for review. A plain git pre-commit
  hook runs it, installed in each clone with one command named in the README
  (`git config core.hooksPath hooks`). Where it is installed, a refused value is not
  committed; `--no-verify` and edits on the GitHub web page get past it, and the owner's
  PR review is the last check.
- **What counts as secret or identifying** (refused): keys, tokens, passwords and
  credential-shaped strings; UUIDs and other account, workspace or project ids; e-mail
  addresses; hostnames and URLs of real services other than public, well-known ones
  (github.com, learn.microsoft.com and the like). **Allowed:** local paths written from `~`
  (not `/home/<account>`), SSH aliases from
  `~/.ssh/config` (`win11`, `win11-test`), the test bed's own names (`win11-dev`, `Ramune`,
  `ambytest`, `\\localhost\ambynet`), ticket ids (APS-36) and repo names.
- **Recall:** one line in the claudecode-guide global block tells every session, before
  non-trivial work and when a command fails in a way that may have a known fix, to update
  the clone (`git pull --ff-only`, only when it is on `main`; on another branch or offline,
  read it as it is and say so) and read `INDEX.md`, and to name the lesson it used when
  one changes what it does. No hook, no tool.
- **Review:** an agent drafts a lesson in a PR; the owner merging the PR is the approval.
- **Migration:** every auto-memory item for the Ambysto repos (the listing
  `~/.claude/projects/-home-dc-group-work-ambysto*/memory/*.md` minus `MEMORY.md`, taken
  after auto-memory is off, so it cannot grow afterwards), and the lessons and machine facts
  in `~/.claude/CLAUDE.md`, each moved into a lesson, kept where they are, or dropped, with
  the owner approving the list item by item. Rules that every session must follow stay in
  `CLAUDE.md`; facts and gotchas a task looks up move out. The old memory folders are left
  in place, not deleted. The Mac's own auto-memory folders for Ambysto repos are listed by
  the owner before it is turned off there, and migrated the same way (owner step).
- **Auto-memory off** with `autoMemoryEnabled: false` in `~/.claude/settings.json`, on this
  machine and on the Mac (owner step there).

## Decisions (owner, 2026-10-23)

1. **No external tool.** Beacon, cass-memory, claude-mem, memorix, beads and the rest were
   read, not installed. We take ideas, not software.
2. **A private GitHub repo of its own**, so the Mac gets the same memory and every change
   has a PR.
3. **v1 scope:** the store, recall, and the migration out of `CLAUDE.md` and auto-memory.
4. **Loaded by one line in `CLAUDE.md`**, not by a hook and not only on demand.
5. **Replace the per-folder auto-memory entirely.**
6. **Windows VM facts move out of `CLAUDE.md`** (the Recycle Bin table, the snapshot layers,
   the VM state) into `reference` and `gotcha` lessons. `CLAUDE.md` keeps the rules, for
   example: run in the VM as ambytest, never on the host; the lock rule; never read the
   guest password. The migration table decides each line.
7. **The recall line lives in the claudecode-guide global block** (a claudecode-guide PR
   under APS-36), so a reinstall keeps it and the Mac gets it.
8. **Auto-memory is turned off** (`autoMemoryEnabled: false`), not redirected with
   `autoMemoryDirectory`, so every lesson goes through a PR.

Ideas taken from the prior art (read 2026-10-23): reviewed lessons kept apart from raw
history and approved by a person, the lesson shape and its kinds, supersede instead of
delete (agent-beacon); a last-validated date so lessons age (cass-memory); a short index
first and details on demand (claude-mem); decisions recorded with their reasons, and
cross-project scope only when a lesson says so (memorix).

## Success criteria

| # | Criterion | How it is checked |
|---|---|---|
| 1 | Every lesson has the shape above; `INDEX.md` lists exactly the active lessons | `check.py` PASS; mutation: a lesson without `evidence`, an `applies_when` not starting with when/before/after, and a stale `INDEX.md` each make it FAIL |
| 2 | No secret or identifying value in the repo, by the definition above | `check.py` refuses a test token, a real-service hostname, a UUID and an e-mail address planted in a lesson, and accepts `ssh win11` and `ambytest` (mutation); passes on the real repo; a commit with a planted token is refused by the pre-commit hook |
| 3 | Every item in the migration listing and each lesson or fact block in `~/.claude/CLAUDE.md` has an owner-approved fate | a migration table in the plan: item, fate (lesson / stays / dropped), reason, owner tick; its row count equals the listing's file count |
| 4 | `~/.claude/CLAUDE.md` is smaller and lost nothing | its size before and after; every moved line traced to a lesson in the migration table |
| 5 | Auto-memory no longer writes per folder | a fresh session on this machine, asked to remember a fact, writes nothing under `~/.claude/projects/*/memory` |
| 6 | A session in a repo that never had a lesson finds and uses it | a fresh session in a worktree (e.g. `ambysto-space-asp24`) asked to list the latest APS tickets reaches Plane with no 403 retry and names the lesson it used (a read, no tracker write) |
| 7 | Stale lessons come back | `check.py` lists a lesson whose `last_validated` is set back 91 days (mutation) |
| 8 | The Mac reads the same memory and its auto-memory is off | not run here: Mac, owner step (list and migrate its auto-memory, clone, install the hook, `autoMemoryEnabled: false`, one session recalls a lesson) |

Accepted, not measured in v1: whether sessions keep recalling after the first proof. A
known lesson relearned is logged as an owner `incident` in the time log, which is where it
will show up.

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

None. The three earlier ones were answered by the owner on 2026-10-23 (decisions 6–8).
`autoMemoryEnabled` was seen in the Claude Code binary, not yet tested; criterion 5 tests it.

## Review log

**Round 1 (hard-reviewer: Fable 5.1, FAIL, 2026-10-23).** All six issues fixed in this
revision.
1. MAJOR: the auto-memory count was 13, not 12, and a fixed number lets an item go missing.
   Fixed: the migration set is a listing taken after auto-memory is off; criterion 3 checks
   the row count against it.
2. MAJOR: "no hostnames" contradicted moving the VM facts. Fixed: refused and allowed
   values are defined, and criterion 2 tests both sides.
3. MINOR: the Mac's auto-memory, a stale clone, ongoing recall and a push-time secret check
   were uncovered. Fixed: criterion 8 includes the Mac setting, the recall line pulls first,
   a pre-commit hook runs `check.py`, and ongoing recall is an accepted gap.
4. MINOR: criterion 6 wrote to the tracker. Fixed: it reads.
5. NIT: "five kinds" against seven. Fixed.
6. NIT: CLAUDE.md said "repo-local author"; it comes from `includeIf`. Fixed.

**Round 2 (hard-reviewer: Fable 5.1, PASS, 2026-10-23).** Round-1 fixes verified (the
listing gives 13 files; `win11` and `win11-test` are real SSH aliases). Five issues found
after the PASS, all fixed:
1. MINOR: git hooks are not cloned, and `--no-verify` or a web edit gets past them. Fixed:
   the install command is named and the claim narrowed.
2. MINOR: the recall pull would follow a lesson draft branch, and fails offline. Fixed:
   pull only on `main`.
3. MINOR: the Mac's own auto-memory would be lost when turned off. Fixed: listed and
   migrated first (owner step).
4. NIT: absolute paths carry the account name. Fixed: paths from `~`.
5. NIT: decision 6 named only some of the rules that stay. Fixed: "for example".
