---
status: draft   # draft → accepted (owner) ; the intent's status moves to planned on acceptance
---
# Plan: ambysto-memory v1 (APS-36)

Contract: `intent/2026-10-23-ambysto-memory.md` (approved 2026-10-23). This plan is the
hand-over: whoever builds reads this file and the intent, not the chat.

Rating: **HARD** as a whole (lost guidance and leaked secrets are both silent). The main
session builds every step itself; hard-reviewer (Fable 5.1) reviews each PR. Steps 1 and 4
are the HARD core; the lesson text of step 2 is reviewed by the owner in its PR.

## Steps and files, in order

Each step is one PR on its own branch, merged by the owner before the next one starts,
except where noted.

### Step 1: the checker (repo `ambysto-memory`, branch `aps-36-checker`)
- `scripts/check.py`: standard library only. Reads `lessons/*.md`. Exit 0 PASS, 1 FAIL,
  2 usage error. `--write-index` regenerates `INDEX.md`. Checks:
  - frontmatter present and closed; fields `title` (< 80 chars), `kind` (one of the seven),
    `applies_when` (starts with when/before/after), `projects` (list or `all`), `evidence`,
    `last_validated` (ISO date, not in the future), `status` (`active` | `superseded`;
    `superseded` needs `superseded_by` naming an existing lesson); file name = slug of
    the `name` field; body 3–10 non-empty lines.
  - `INDEX.md` byte-equal to what `--write-index` would write (active lessons only, sorted
    by kind then title, one line each: `- [title](lessons/slug.md) — kind — applies_when`).
  - secret and identifying text, in every tracked text file (lessons, INDEX, README,
    CLAUDE.md, intent): credential shapes (`ghp_`, `github_pat_`, `sk-`, `xox`, AWS key
    ids, PEM headers, `password=`/`token=` with a value, 32+ char hex/base64 runs), UUIDs,
    e-mail addresses, `/home/<name>/` paths, and hostnames/URLs whose domain is not on the
    allow list in the script (github.com, githubusercontent.com, microsoft.com and
    subdomains, learn.microsoft.com, nuget.org, python.org, anthropic.com, claude.com,
    docs.claude.com). Allowed by rule: `~` paths, the SSH aliases and test-bed names listed
    in the intent, ticket ids, `localhost`. An allow comment per line is **not** offered.
  - stale: lessons whose `last_validated` is more than 90 days old are listed under
    `STALE:`; they do not fail the check.
- `scripts/test_check.py`: unittest, temp folders only. One case per check above, both
  directions (a planted bad value fails; the allowed values pass), plus the mutations
  named in intent criteria 1, 2 and 7.
- `hooks/pre-commit`: `exec python3 scripts/check.py`. `README.md`: layout, the lesson
  shape, and the one-time `git config core.hooksPath hooks`.
- `INDEX.md` (empty list), `lessons/.gitkeep`.

### Step 2: the lessons (repo `ambysto-memory`, branch `aps-36-lessons`)
- `lessons/<slug>.md` for each row marked **lesson** in the migration table below, with
  the evidence the source gives. `INDEX.md` regenerated. The owner reads each lesson in
  the PR; the merge is the approval. A row the owner rejects in review is dropped from
  the PR and marked so in the table.
- The table itself is updated in this PR with the owner's ticks (it is the record for
  criterion 3).

### Step 3: auto-memory off (this machine)
- `~/.claude/settings.json`: add `"autoMemoryEnabled": false` (backup first, as
  `settings.json.bak-<timestamp>`; nothing else in the file changes).
- Then take the listing again
  (`ls ~/.claude/projects/-home-dc-group-work-ambysto*/memory/*.md | grep -v MEMORY.md`).
  Any file not in the table goes into it and through step 2's review (a follow-up commit
  on `aps-36-lessons` if that PR is still open, otherwise its own small PR).
- Not a PR: a machine change, recorded in the plan's proof section.

### Step 4: the global block (repo `claudecode-guide`, branch `aps-36-memory-recall`, worktree of its own)
Work from `main` in a separate worktree (`~/work/ambysto/claudecode-guide-aps36`), never
in the `aps-34-boundary-hook` checkout another session is using.
- `global/CLAUDE.md`, a new short section "Shared memory":
  "Ambysto repos share one reviewed memory in `~/work/ambysto/ambysto-memory`. Before
  non-trivial work, and when a command fails in a way that may have a known fix: if the
  clone is on `main`, `git -C ~/work/ambysto/ambysto-memory pull --ff-only` (on another
  branch or offline, read it as it is and say so); read `INDEX.md`; open the lessons whose
  line matches. When a lesson changes what you do, name it. To add or change a lesson,
  draft it on a branch there and open a PR; the owner's merge is the approval. Claude
  Code's per-folder auto-memory is off."
  It is the guide's first ecosystem path in `global/`; the guide's rule "Universal only: no
  project's paths" is about single projects, and this path is shared by all of them. The
  PR says so, so the owner decides it there.
- `templates/project-CLAUDE.md`, "Session state": "Durable facts go in this file or in
  memory" → "… in this file or in ambysto-memory".
- `skills/handoff/SKILL.md`: the same wording, where it names memory.
- `scripts/check.py` of the guide: unchanged unless it checks the global block's
  sections; then the new section is added to its list.
- After the owner merges: `python scripts/install.py` (the global block), then
  `install.py --check` exit 0.

### Step 5: the machine section of `~/.claude/CLAUDE.md`
- Backup `~/.claude/CLAUDE.md` to `CLAUDE.md.bak-<timestamp>` first.
- Edit only the part after `<!-- claudecode-guide:end -->`, following the rows marked
  **stays**, **lesson** and **dropped** in the table (CLAUDE.md part). Moved text is
  removed only once its lesson is merged on `main` (step 2).
- Not a PR (the file is not in a repo). The before/after diff is saved in the proof as
  `proof/claude-md-machine-section.diff` in this repo, run through `check.py`'s secret
  check first; anything refused there is replaced by a description.

### Step 6: proofs (branch `aps-36-proof`)
- Run every item of the Proof section below, write the results into this file, set the
  intent to `verified`. Final PR "Closes #1".

## Migration table

Fate: **lesson** (moved into `lessons/<slug>`), **stays** (left where it is), **dropped**
(already recorded elsewhere, named). Owner tick: ☐ until the owner agrees in the plan
review; a changed row is rewritten, not ticked.

### Auto-memory (listing 2026-10-23, 13 files)

| # | Source (`~/.claude/projects/…/memory/`) | Fate | Lesson / where it already is | Owner |
|---|---|---|---|---|
| A1 | gate `plane-agd-rest-api.md` | lesson, merged with A12 | `plane-rest-api` (reference): key in `~/.claude.json` `plane` env, read at run time and never printed; custom User-Agent or HTTP 403; links POST; auto mode blocks reading the key. Project ids, states and the host are not copied: read them from the API at run time. Ticket/issue/PR naming already in Gate's `CLAUDE.md` | ☐ |
| A2 | kit `measure-before-offering-limits.md` | lesson | `measure-before-offering-limits` (correction, all) | ☐ |
| A3 | kit `suite-positioning-jetpack.md` | lesson | `suite-positioning-jetpack` (decision): positioning + deferred landing items. Vercel domains written as project names, not hostnames | ☐ |
| A4 | space `autonomous-run-aps31.md` | lesson (short) | `long-run-coding-is-aps-31` (reference): the owner's phrase "phiên nghiên cứu long-run coding" means APS-31 in claudecode-guide. The state snapshot is dropped: it is in Plane APS-31/32/34 and the guide's intent files | ☐ |
| A5 | space `check-branch-before-amend.md` | dropped + lesson | the branch check is in the guide's working practice ("After any subagent has run, check the branch…"). New lesson `retarget-prs-before-deleting-base` (gotcha) | ☐ |
| A6 | space `loop-assessment-framing.md` | lesson | `loop-assessment-framing` (decision) | ☐ |
| A7 | space `sure-over-fast.md` | lesson | `sure-over-fast` (correction, all) | ☐ |
| A8 | space `windows-app-order.md` | lesson, merged with C5 | `windows-port-order` (decision) | ☐ |
| A9 | space `windows-port-loop.md` | lesson + dropped | `windows-port-loop-design` (decision): steps [0]–[5] and why. `gitignore-hides-fixture-folders` (gotcha: `fixtures/` in `.gitignore` hid every `scripts/fixtures/`; check `git check-ignore`). `one-vm-clone-per-worktree` (gotcha). Dropped: the progress log (in git history, Plane, PRs); the probe facts (in `~/vms/README.md`); "refuse online-only cloud files" (in Lean's `intent/2026-10-16-lean-windows-v1.md`); stray processes after a stop (guide working practice) | ☐ |
| A10 | tune `ambysto-dmg-builds.md` | lesson | `ambysto-dmg-builds` (reference): release `dmgs-2026-10-15` in `ambysto/ambysto-assets`; the Tune site needs `site/dl/AmbystoTune.dmg` put back before each deploy | ☐ |
| A11 | steady `vm-files-to-desktop.md` | lesson | `vm-files-to-desktop` (convention) | ☐ |
| A12 | steady `plane-sic-rest-api.md` | lesson, merged into A1 | `plane-rest-api`. "SIC tickets in Vietnamese" is already in Steady's `CLAUDE.md` | ☐ |
| A13 | steady `windows-test-vm.md` | lesson, merged with C2/C8 | `win11-vm-layout` and `win11-snapshots` (reference); `clean-no-globalsign` = Steady's SIC-130 repro | ☐ |

### `~/.claude/CLAUDE.md`, machine section (after the guide block, 12 KB)

| # | Bullet | Fate | Detail | Owner |
|---|---|---|---|---|
| C1 | "Applies to every repo… Windows only" + "Develop the Windows app only…", macOS Verify "not run" line, "work from `docs/spec/`" | stays | rules | ☐ |
| C2 | Test environment (QEMU, cores, disks, ports, `ssh win11`) | split | stays: run in the VM never on the host, never read the guest password, the ports on `0.0.0.0` are deliberate, check it is up with `ss -ltnp \| grep 33890`. Lesson `win11-vm-layout`: process, disks, monitor socket, forwards, console | ☐ |
| C3 | Driving the VM (`~/vms/bin` scripts, nuget pull, tokens) | split | stays: start every agent run with `vm-status.sh`; `vm-gates.sh`/`vm-sync.sh` exist (one line + pointer to `~/vms/README.md`); never a GitHub token in the VM except the one `read:packages` token; the VM never pushes. Lesson `win11-vm-scripts`: what each script does, `cmd.exe` shell, `vm-ps.sh` for quoting | ☐ |
| C4 | Two users; Recycle Bin by API; VNC not RDP | split | stays: every build/test/proof as ambytest; Ramune only provisions; Recycle Bin tests through `vm-ui.sh`. Lessons `recycle-bin-deletes-for-good` (gotcha: the full IFileOperation list) and `use-vnc-not-rdp` (gotcha: RDP takes the console; logon + logoff wipes autologon; `vm-autologon.sh`) | ☐ |
| C5 | Order of the Windows ports | lesson | `windows-port-order` (with A8); CLAUDE.md keeps one line: "Windows ports follow the order in lesson `windows-port-order`" | ☐ |
| C6 | License key for Windows apps | split | stays: build on `Ambysto.Kit.License`; agents never create or use a real key; Free ships first, the key blocks only Pro; apps test entitlement through their own verifier seam. Lesson `license-key-plan` (decision: who makes the key, where, when, the 2026-10-22 change) | ☐ |
| C7 | Private NuGet feed and DPAPI | lesson | `nuget-feed-dpapi-over-ssh` (gotcha: NU1301 over SSH, restore through `vm-ui.sh`, cache then SSH works; token expiry about 90 days from 2026-10-16) | ☐ |
| C8 | Snapshots | split | stays: before a destructive proof, restore the default snapshot named in `~/vms/DEFAULT_SNAPSHOT`; after restoring an older layer, resync the clock first. Lesson `win11-snapshots` (reference: every layer and what it lacks) | ☐ |
| C9 | Cloud files (AmbyCloud, OneDrive) | split | stays: OneDrive in the VM uses only the owner's test Microsoft account, never the personal one. Lesson `cloud-files-in-vm` (reference + gotcha: AmbyCloud logs fetches by pid; online-only items do not reach the bin) | ☐ |
| C10 | Contribute only as Ambysto (no trailer) | stays | rule | ☐ |
| C11 | GitHub accounts, `gh` and `vercel` wrappers | stays | rule | ☐ |
| C12 | Two identities, never mixed | stays | rule | ☐ |
| C13 | VM state 2026-10-16 (Windows build, SDKs, volumes, long paths, Defender, SCM right, Steady installed) | lesson | `win11-vm-state` (reference; `last_validated` 2026-10-16, so it ages first). The evaluation expiry 2027-01-13 stays in CLAUDE.md as one line: it blocks everything when it passes | ☐ |

The guide block (lines 1–65) is not touched by step 5; only step 4 changes it, through its
repo.

## Risks and how they are caught

| Risk | Caught by |
|---|---|
| A rule moved out by mistake, so no session follows it any more | the table's stays/split rows are the owner's call; step 5 removes text only after its lesson is merged; hard-review compares the before/after diff with the table row by row |
| A lesson loses a detail its source had | hard-review of step 2 reads each source next to its lesson |
| A secret or the Plane host reaches GitHub | `check.py` on every commit (hook) and in hard-review; A1/A12 are rewritten without host or ids; the CLAUDE.md diff is checked before it is committed |
| The secret check refuses legitimate text, so people turn the hook off | test cases for the allowed values; no per-line override, the allow list is changed in a reviewed PR |
| `autoMemoryEnabled` does not do what its name says | criterion 5 is tested right after step 3, before step 5 relies on it; if it fails, stop and ask |
| A session writes a new auto-memory between the listing and step 3 | the listing is taken again after step 3 |
| Sessions skip recall | accepted in the intent; criterion 6 proves it works once |
| Editing the guide while the APS-34 session works in its checkout | step 4 in its own worktree from `main`; only the owner merges |
| The installer overwrites the machine section | `install.py` only rewrites between its markers (guide rule, checked by its `--check`); a backup is taken in step 5 anyway |

## Proof (what "done" means; run in step 6)

1. `python3 scripts/check.py` PASS on `main`; `python3 -m unittest scripts/test_check.py`
   all pass, including the mutations of intent criteria 1, 2 and 7 (each named in the
   output).
2. A commit with a planted `ghp_` token in a lesson is refused by the hook (show the
   output), then the file is restored.
3. The migration table: every row ticked; row count A = the listing's file count after
   step 3.
4. `wc -c ~/.claude/CLAUDE.md` before and after; the machine section diff, every removed
   line mapped to a table row.
5. A fresh headless session (`claude -p`) in `~/work/ambysto/ambysto-power` asked to
   "remember that the test word is pelican" exits, and
   `find ~/.claude/projects -path '*memory*' -newer <stamp>` lists nothing.
6. A fresh headless session in `~/work/ambysto/ambysto-space-asp24` asked "list the five
   most recent APS tickets in Plane" answers with no HTTP 403 in its transcript and names
   lesson `plane-rest-api`. (Headless: no owner line in the time log.)
7. `check.py` lists a lesson whose `last_validated` is set back 91 days (from test 1).
8. Not run: Mac, owner step (list and migrate its auto-memory, clone, hook, setting, one
   recall).
9. Guide: `python scripts/check.py` and `python scripts/install.py --check` exit 0 after
   the step 4 merge and install.
