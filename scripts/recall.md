## Shared memory
Ambysto repos share one owner-reviewed memory in `~/work/ambysto/ambysto-memory` (its `AGENTS.md` says how to use it). Claude Code's per-folder auto-memory is off.
- Before non-trivial work, and when a command fails in a way that may have a known fix: if the clone is on `main`, run `git -C ~/work/ambysto/ambysto-memory pull --ff-only` (on another branch, offline, or when a sandbox refuses the pull, read it as it is and say so); read its `INDEX.md`; open the lessons whose line matches the task.
- When a lesson changes what you do, name it in one line. If a lesson conflicts with the owner or the project's own docs, follow those and say so.
- To add or change a lesson (something learned that a later session needs), draft it on a branch there and open a PR, as its `AGENTS.md` says; the owner's merge is the approval. Never merge it yourself.

