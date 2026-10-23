# Ambysto Memory

What one coding-agent session learns does not reach the next session that needs it, so the same lesson gets
learned again. This repo (`ambysto-memory`) is one shared memory that the owner reviews, for every Ambysto repo and
session, in any coding agent. Tracked in Plane as APS-36.

- **One line per lesson.** `INDEX.md` lists every active lesson; a session reads it first and opens only the
  lessons that match its task.
- **One file per lesson.** Each file in `lessons/` has a title, a kind, when it applies, its evidence and a date it
  was last checked, then 3 to 10 lines.
- **Checked by script.** A checker refuses a bad lesson shape, an `INDEX.md` out of step, and secret or identifying
  text, and lists lessons older than 90 days.

Standard library Python only.

## Is it for you?

Yes, if you run coding agents across the Ambysto repos and want what one session learns to be there for the next.
No, if your work is outside Ambysto: the lessons are about Ambysto's repos, machines and owner decisions.

## Status

- Built: the lesson format, the checker, the pre-commit hook, and the script that wires the recall paragraph into
  each harness.
- A lesson reaches `main` only through a pull request the owner merges. Agents draft; they never approve.

## What is in the repo

| Path | What |
|---|---|
| `INDEX.md` | One line per active lesson, generated. Read it first. |
| `lessons/<slug>.md` | One lesson per file: frontmatter `title`, `kind`, `applies_when`, `projects`, `evidence`, `last_validated`, `status`, then 3 to 10 lines (shape and example in `AGENTS.md`). |
| `AGENTS.md` | How any agent reads the memory and drafts a lesson. |
| `scripts/check.py` | Lesson shape, `INDEX.md` in step, refused secret and identifying text, stale lessons (over 90 days) listed. Run `python3 scripts/check.py --write-index` after changing a lesson. |
| `hooks/pre-commit` | Runs the check on what is staged. |
| `scripts/wire.py` | Writes the recall paragraph (`scripts/recall.md`, the same text as the claudecode-guide "Shared memory" section) between markers into each installed harness's global instruction file, with a backup; `--check` reports any that miss it. Run it after installing a new harness or changing `recall.md`. |

## Set up a clone

```sh
git clone https://github.com/ambysto/ambysto-memory ~/work/ambysto/ambysto-memory
git -C ~/work/ambysto/ambysto-memory config core.hooksPath hooks
```

The hook stops a commit whose staged files fail the check.

## Limits

- `--no-verify` and edits on the GitHub web page get past the hook. The owner's PR review is the last check.

## Check

```sh
python3 -m unittest scripts/test_check.py scripts/test_wire.py
python3 scripts/check.py
```

## Licence

Apache-2.0, see [LICENSE](LICENSE) and [NOTICE](NOTICE).
