# ambysto-memory: how any coding agent uses this memory

This repo's own rules are in `CLAUDE.md`; read it before changing anything here.

This is the shared, owner-reviewed memory of every Ambysto repo. It works the same in
every harness (Claude Code, Codex, Grok Build, OpenCode, …): Markdown files, standard
library Python, git.

## Recall: read before you work

Before non-trivial work in any Ambysto repo, and when a command fails in a way that may
have a known fix:

1. If this clone is on `main`, update it: `git -C ~/work/ambysto/ambysto-memory pull --ff-only`.
   On another branch, offline, or when your sandbox refuses the pull, read it as it is and
   say so.
2. Read `INDEX.md`: one line per active lesson (title, kind, when it applies).
3. Open only the lessons whose line matches your task, under `lessons/`.
4. When a lesson changes what you do, name it in one line ("Using lesson
   `plane-rest-api`: …").

A lesson is guidance from earlier sessions, reviewed by the owner. If it conflicts with
the owner's words or the project's own `CLAUDE.md` / `AGENTS.md`, follow those and say so.
A lesson that turns out wrong or outdated: say so, and draft its replacement (below).

## Write: draft a lesson, never approve one

1. Branch in this repo: `lesson-<slug>` (or `aps-NN-<slug>` for ticket work), from an
   up-to-date `main`.
2. Add `lessons/<slug>.md`. The file name is the slug (lowercase letters, digits,
   hyphens). Shape:

   ```markdown
   ---
   title: Imperative, under 80 characters, names the tool, file or error
   kind: gotcha
   applies_when: when <a trigger a session would recognise: a command, a path, an error>
   projects: all
   evidence: 2026-10-23 APS-36 (date plus repo, ticket or PR)
   last_validated: 2026-10-23
   status: active
   ---

   What to do, with exact commands and paths.
   Why, in one sentence.
   How to confirm it worked.
   ```

   - `kind`: `workflow`, `correction`, `debugging_pattern`, `gotcha`, `convention`,
     `decision` (what was decided, why, the options turned down), `reference` (where
     something lives).
   - `projects`: `all`, or a list such as `[ambysto-space, steady]`.
   - Body: 3 to 10 non-empty lines.
   - Outdated lesson: never delete it. Set `status: superseded` and
     `superseded_by: <new-slug>`.
3. `python3 scripts/check.py --write-index` (regenerates `INDEX.md`, then checks), commit,
   push, open a PR. The owner's merge is the approval. Never merge it yourself.

Not a lesson: a summary of what happened, a one-off fact, anything true only on one day
or branch, a rule for one project only (that goes in the project's own `CLAUDE.md`), or
anything the project's docs already say.

## Never write here

Keys, tokens, passwords, UUIDs or other account, workspace or project ids, e-mail
addresses, hostnames of private services, `*.vercel.app` hosts, full commit SHAs, or
paths under `/home/<account>`. Say where the value lives instead ("the base URL in
`~/.claude.json`, `plane` server env"). Allowed: `~` paths, SSH aliases (`win11`,
`win11-test`), the test bed's names (`win11-dev`, `Ramune`, `ambytest`,
`\\localhost\ambynet`), ticket ids, repo names, short SHAs, `ambysto.com`, `github.com`
and the other domains listed in `scripts/check.py`. The pre-commit hook refuses the rest.

## Harnesses

Each harness gets the same short recall paragraph, between `ambysto-memory` markers, in
its global instruction file. Fallback order (owner, 2026-10-23):

| Tier | Harness | Global instruction file |
|---|---|---|
| 1 | Claude Code | `~/.claude/CLAUDE.md`, through the claudecode-guide global block |
| 2 | Codex | `~/.codex/AGENTS.md` |
| 2 | Grok Build | `~/.grok/AGENTS.md` |
| 2 | Muse Code | reads `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` |
| 2 | Oh My Pi | to confirm when installed |
| 2 | Cursor CLI | to confirm when installed |
| 3 | OpenCode | `~/.config/opencode/AGENTS.md` |
| 3 | Antigravity CLI | `~/.gemini/GEMINI.md` (not also `AGENTS.md` there: both would load) |
| 3 | Hermes | `~/.hermes/SOUL.md`, between markers |
| 3 | Codewhale | a file named in `instructions = [...]` of its config, when installed |
| 3 | DeepSeek Harness | to confirm when installed |
