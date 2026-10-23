# ambysto-memory

Shared, owner-reviewed memory for every Ambysto repo and session, in any coding agent.
Tracked in Plane as APS-36.

- `INDEX.md`: one line per active lesson, generated. Read it first.
- `lessons/<slug>.md`: one lesson per file: frontmatter `title`, `kind`, `applies_when`,
  `projects`, `evidence`, `last_validated`, `status`, then 3 to 10 lines (shape and
  example in `AGENTS.md`).
- `AGENTS.md`: how any agent reads the memory and drafts a lesson.
- `scripts/check.py`: lesson shape, `INDEX.md` in step, refused secret and identifying
  text, stale lessons (over 90 days) listed. `python3 scripts/check.py --write-index`
  after changing a lesson.
- `hooks/pre-commit`: runs the check on what is staged.
- `scripts/wire.py`: writes the recall paragraph (`scripts/recall.md`, the same text as the
  claudecode-guide "Shared memory" section) between markers into each installed harness's
  global instruction file, with a backup; `--check` reports any that miss it. Run it after
  installing a new harness or changing `recall.md`.

## Set up a clone

```sh
git clone https://github.com/ambysto/ambysto-memory ~/work/ambysto/ambysto-memory
git -C ~/work/ambysto/ambysto-memory config core.hooksPath hooks
```

The hook stops a commit whose staged files fail the check. `--no-verify` and edits on the
GitHub web page get past it; the owner's PR review is the last check.

## Test

```sh
python3 -m unittest scripts/test_check.py scripts/test_wire.py
python3 scripts/check.py
```
