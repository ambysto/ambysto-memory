---
status: accepted # draft → accepted (owner) ; the intent's status moves to planned on acceptance
---
# Plan: ambysto-memory v1 (APS-36)

Contract: `intent/2026-10-23-ambysto-memory.md` (approved 2026-10-23). This plan is the
hand-over: whoever builds reads this file and the intent, not the chat.

Rating: **HARD** as a whole (lost guidance and leaked secrets are both silent). The main
session builds every step itself; hard-reviewer (Fable 5.1) reviews each PR. Steps 1, 4a and 4b
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
    `superseded` needs `superseded_by` naming an existing lesson); the file name is the
    slug (`[a-z0-9-]+\.md`); body 3–10 non-empty lines.
  - `INDEX.md` byte-equal to what `--write-index` would write (active lessons only, sorted
    by kind then title, one line each: `- [title](lessons/slug.md) — kind — applies_when`).
  - secret and identifying text, in every tracked text file (lessons, INDEX, README,
    AGENTS.md, CLAUDE.md, intent, scripts): credential shapes (`ghp_`, `github_pat_`,
    `sk-`, `xox`, AWS key ids, PEM headers, `password=`/`token=`/`key=` with a value),
    the Plane key prefix, `Bearer` values, hex runs of 13+ characters (so full commit
    SHAs are refused, short ones up to 12 pass) and base64-like runs of 32+ with mixed case
    and at least 4.4 bits of entropy per character, all bounded by lookarounds rather than
    `\b` (a `_` prefix must not hide a key), UUIDs, e-mail addresses, `/home/<name>/` and
    `/Users/<name>/` paths (not after a drive letter), Claude Code's encoded
    `-home-<name>-…` folder names, non-loopback IPv4 addresses, and hosts (case-insensitive).
    Hosts are found three ways, and a host passes only when it equals an allowed domain or
    ends in `.` + one (so `nuget.pkg.github.com` passes through `github.com`):
    1. every URL with a scheme (any scheme), or starting `//`, by its host;
    2. every bare `label(.label)+.tld` token whose last label is in a short TLD list
       (`com net org io dev ai co me cloud xyz vn`), so file names (`check.py`, `INDEX.md`,
       `win11.qcow2`, `AmbystoLean.dll`, `vm-gates.sh`, `Lean.app`) never match;
    3. `vercel.app` hosts, refused whatever the rest (the owner deploys on Vercel; other
       `.dev`/`.com` deployment hosts are already caught by 2).
    Allowed domains (a list in the script, changed only by a reviewed PR): `github.com`,
    `githubusercontent.com`, `microsoft.com`, `nuget.org`, `python.org`, `anthropic.com`,
    `claude.com`, `ambysto.com`, `digicert.com` (signtool's timestamp server), and the
    reserved placeholders `example.com`, `example.org`, `example.net`. Allowed by rule: `~` paths, the SSH aliases and test-bed
    names listed in the intent, ticket ids, `localhost`. An allow comment per line is
    **not** offered.
  - stale: lessons whose `last_validated` is more than 90 days old are listed under
    `STALE:`; they do not fail the check.
- `scripts/test_check.py`: unittest, temp folders only. One case per check above, both
  directions (a planted bad value fails; the allowed values pass: the file names above,
  a 7- and a 12-char SHA, `nuget.pkg.github.com`, `tune.ambysto.com`, `ssh win11`,
  `C:\Users\ambytest\src`, `\\localhost\ambynet`; refused: a 40-char SHA, a made-up
  host under `.dev`, a Vercel deployment host, a UUID, an e-mail), plus the mutations named in
  intent criteria 1, 2 and 7. The planted values are built at run time (joined from
  pieces), so the test file itself holds none and `check.py` PASSes on the real repo.
- `hooks/pre-commit`: `exec python3 scripts/check.py`. `README.md`: layout, the lesson
  shape, and the one-time `git config core.hooksPath hooks`.
- `AGENTS.md`: the harness-neutral manual (intent, "Harness-neutral"): how to recall
  (pull on `main`, read `INDEX.md`, open matching lessons, name the one used), how to
  draft a lesson (shape, branch `aps-NN-slug` or `lesson-slug`, PR, never merge), the
  secret rule, and the harness table with each global instruction file. Its first line:
  "This repo's own rules are in `CLAUDE.md`; read it before changing anything here"
  (Codex, OpenCode and Hermes load `AGENTS.md` instead of `CLAUDE.md`).
- `INDEX.md` (empty list), `lessons/.gitkeep`.

### Step 2: the lessons (repo `ambysto-memory`, branch `aps-36-lessons`)
- `lessons/<slug>.md` for each row marked **lesson** in the migration table below, with
  the evidence the source gives. `INDEX.md` regenerated. The owner reads each lesson in
  the PR; the merge is the approval. A row the owner rejects in review is dropped from
  the PR and marked so in the table.
- The owner ticks the table when accepting this plan; step 2's PR records any row the
  owner then rejects or changes while reading the lessons (the table stays the record for
  criterion 3).

### Step 3: auto-memory off (this machine)
- `~/.claude/settings.json`: add `"autoMemoryEnabled": false` (backup first, as
  `settings.json.bak-<timestamp>`; nothing else in the file changes).
- Then take the listing again
  (`ls ~/.claude/projects/-home-*-work-ambysto*/memory/*.md | grep -v MEMORY.md`).
  Any file not in the table goes into it and through step 2's review (a follow-up commit
  on `aps-36-lessons` if that PR is still open, otherwise its own small PR).
- Not a PR: a machine change, recorded in the plan's proof section.

### Step 4a: the Claude Code recall (repo `claudecode-guide`, branch `aps-36-memory-recall`, worktree of its own)
`git -C ~/work/ambysto/claudecode-guide fetch`, then a worktree from `origin/main` (the
local `main` lags) at `~/work/ambysto/claudecode-guide-aps36`, never in the
`aps-34-boundary-hook` checkout another session is using.
- `global/CLAUDE.md`, a new short section "Shared memory":
  "Ambysto repos share one reviewed memory in `~/work/ambysto/ambysto-memory`. Before
  non-trivial work, and when a command fails in a way that may have a known fix: if the
  clone is on `main`, `git -C ~/work/ambysto/ambysto-memory pull --ff-only` (on another
  branch, offline, or when a sandbox refuses the pull, read it as it is and say so); read `INDEX.md`; open the lessons whose
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

### Step 4b: the other harnesses (repo `ambysto-memory`, branch `aps-36-wire`)
- `scripts/wire.py`, standard library only. A table of harness → global instruction file
  (the intent's table, each path confirmed first from the harness's own docs or binary;
  Antigravity: `~/.gemini/GEMINI.md` only, since both it and `~/.gemini/AGENTS.md` would
  load; Hermes: `~/.hermes/SOUL.md`, its only global file, markers appended at the end
  when absent). For each
  harness whose file or config folder exists: back the file up as `<file>.bak-<timestamp>`,
  then write the recall paragraph between `<!-- ambysto-memory:begin -->` and
  `<!-- ambysto-memory:end -->`, creating the file if the harness reads it but it is
  missing. Text outside the markers is never changed; broken markers (not exactly one
  begin before one end) are refused with exit 2 and nothing written. `--check`: exit 0
  when every installed harness has the current paragraph, 1 otherwise, naming each.
  Claude Code is skipped (step 4a owns it); Muse is covered through Codex and Claude Code.
- The paragraph is the same text as step 4a's, in `scripts/recall.md`, so all harnesses
  read the same words; `wire.py --check` also fails when the recall section of the
  installed `~/.claude/CLAUDE.md` differs from `scripts/recall.md` (kept out of
  `check.py`, so a guide update never blocks a lesson commit).
- `scripts/test_wire.py`: temp HOME only; a fresh write, a second run that changes
  nothing, the owner's text around the markers kept byte for byte (CRLF too), broken
  markers refused, `--check` both ways.
- Then run `wire.py` on this machine and `wire.py --check`.

### Step 5: the machine section of `~/.claude/CLAUDE.md`
- Backup `~/.claude/CLAUDE.md` to `CLAUDE.md.bak-<timestamp>` first.
- Edit only the part after `<!-- claudecode-guide:end -->`, following the rows marked
  **stays**, **lesson** and **dropped** in the table (CLAUDE.md part). It runs only after
  step 2 is merged (every moved text has its lesson on `main`) and step 4a is installed
  (sessions are told to read the memory).
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

### Auto-memory (listing 2026-10-23: 13 files at plan acceptance, 14 at 10:13)

| # | Source (`~/.claude/projects/…/memory/`) | Fate | Lesson / where it already is | Owner |
|---|---|---|---|---|
| A1 | gate `plane-agd-rest-api.md` | lesson, merged with A12 | `plane-rest-api` (reference): key, base URL and workspace slug in `~/.claude.json` `plane` env, read at run time and never printed; custom User-Agent or HTTP 403; links POST; auto mode blocks reading the key. Project ids, states, the host and the workspace slug are not copied: read them at run time. Ticket/issue/PR naming already in Gate's `CLAUDE.md` | ☑ 2026-10-23 |
| A2 | kit `measure-before-offering-limits.md` | lesson | `measure-before-offering-limits` (correction, all) | ☑ 2026-10-23 |
| A3 | kit `suite-positioning-jetpack.md` | lesson | `suite-positioning-jetpack` (decision): positioning + deferred landing items. Vercel domains written as project names, not hostnames | ☑ 2026-10-23 |
| A4 | space `autonomous-run-aps31.md` | lesson (short) | `long-run-coding-is-aps-31` (reference): the owner's phrase "phiên nghiên cứu long-run coding" means APS-31 in claudecode-guide. The state snapshot is dropped: it is in Plane APS-31/32/34 and the guide's intent files | ☑ 2026-10-23 |
| A5 | space `check-branch-before-amend.md` | dropped + lesson | the branch check is in the guide's working practice ("After any subagent has run, check the branch…"). New lessons `retarget-prs-before-deleting-base` (gotcha) and `give-reviewers-a-diff-range` (workflow: pass `main..branch`, do not let a reviewer check out) | ☑ 2026-10-23 |
| A6 | space `loop-assessment-framing.md` | lesson | `loop-assessment-framing` (decision) | ☑ 2026-10-23 |
| A7 | space `sure-over-fast.md` | lesson | `sure-over-fast` (correction, all) | ☑ 2026-10-23 |
| A8 | space `windows-app-order.md` | lesson, merged with C5 | `windows-port-order` (decision). Its "signing key due before the first Pro release (Lean)" is superseded by the 2026-10-22 decision in C6 and is written that way | ☑ 2026-10-23 |
| A9 | space `windows-port-loop.md` | lesson + dropped | `windows-port-loop-design` (decision): steps [0]–[5] and why. `gitignore-hides-fixture-folders` (gotcha: `fixtures/` in `.gitignore` hid every `scripts/fixtures/`; check `git check-ignore`). `one-vm-clone-per-worktree` (gotcha). Dropped: the progress log (in git history, Plane, PRs); the probe facts (in `~/vms/README.md`); "refuse online-only cloud files" (in Lean's `intent/2026-10-16-lean-windows-v1.md`); stray processes after a stop (guide working practice) | ☑ 2026-10-23 |
| A10 | tune `ambysto-dmg-builds.md` | lesson | `ambysto-dmg-builds` (reference): release `dmgs-2026-10-15` in `ambysto/ambysto-assets`; the Tune site needs `site/dl/AmbystoTune.dmg` put back before each deploy | ☑ 2026-10-23 |
| A11 | steady `vm-files-to-desktop.md` | lesson | `vm-files-to-desktop` (convention) | ☑ 2026-10-23 |
| A12 | steady `plane-sic-rest-api.md` | lesson, merged into A1 | `plane-rest-api`. "SIC ticket names in Vietnamese" is in Steady's `CLAUDE.md`; the description sections (Bối cảnh / Đã làm / Tiêu chí xong, as `description_html`) cannot go there (its docs-language test), so they go into the lesson | ☑ 2026-10-23 |
| A13 | steady `windows-test-vm.md` | lesson, merged with C2/C8 | `win11-vm-layout` and `win11-snapshots` (reference); `clean-no-globalsign` = Steady's SIC-130 repro | ☑ 2026-10-23 |
| A14 | ambysto (root) `address-owner-as-sir.md` (written 2026-10-23 10:13 by another session, after plan acceptance) | lesson | `address-owner-as-sir` (convention, all): the owner is addressed as "Sir" ("Dạ Sir, …" in Vietnamese), naturally, not in every sentence | ☐ |

### `~/.claude/CLAUDE.md`, machine section (after the guide block, 12 KB)

| # | Bullet | Fate | Detail | Owner |
|---|---|---|---|---|
| C1 | "Applies to every repo… Windows only" + "Develop the Windows app only…", macOS Verify "not run" line, "work from `docs/spec/`" | stays | rules | ☑ 2026-10-23 |
| C2 | Test environment (QEMU, cores, disks, ports, `ssh win11`) | split | stays: run in the VM never on the host, never read the guest password, the ports on `0.0.0.0` are deliberate, check it is up with `ss -ltnp \| grep 33890`. Lesson `win11-vm-layout`: process, disks, monitor socket, forwards, console | ☑ 2026-10-23 |
| C3 | Driving the VM (`~/vms/bin` scripts, nuget pull, tokens) | split | stays: start every agent run with `vm-status.sh`; `vm-gates.sh`/`vm-sync.sh` exist (one line + pointer to `~/vms/README.md`); never a GitHub token in the VM except the one `read:packages` token; the VM never pushes. Lesson `win11-vm-scripts`: what each script does, `cmd.exe` shell, `vm-ps.sh` for quoting | ☑ 2026-10-23 |
| C4 | Two users; Recycle Bin by API; VNC not RDP | split | stays: every build/test/proof as ambytest; Ramune only provisions; Recycle Bin tests through `vm-ui.sh`. Lessons `recycle-bin-deletes-for-good` (gotcha: the full IFileOperation list) and `use-vnc-not-rdp` (gotcha: RDP takes the console; logon + logoff wipes autologon; `vm-autologon.sh`) | ☑ 2026-10-23 |
| C5 | Order of the Windows ports | lesson | `windows-port-order` (with A8); CLAUDE.md keeps one line: "Windows ports follow the order in lesson `windows-port-order`" | ☑ 2026-10-23 |
| C6 | License key for Windows apps | split | stays: build on `Ambysto.Kit.License`; agents never create or use a real key; Free ships first, the key blocks only Pro; apps test entitlement through their own verifier seam. Lesson `license-key-plan` (decision: who makes the key, where, when, the 2026-10-22 change) | ☑ 2026-10-23 |
| C7 | Private NuGet feed and DPAPI | lesson | `nuget-feed-dpapi-over-ssh` (gotcha: NU1301 over SSH, restore through `vm-ui.sh`, cache then SSH works; token expiry about 90 days from 2026-10-16) | ☑ 2026-10-23 |
| C8 | Snapshots | split | stays: before a destructive proof, restore the default snapshot named in `~/vms/DEFAULT_SNAPSHOT`; after restoring an older layer, resync the clock first. Lesson `win11-snapshots` (reference: every layer and what it lacks) | ☑ 2026-10-23 |
| C9 | Cloud files (AmbyCloud, OneDrive) | split | stays: OneDrive in the VM uses only the owner's test Microsoft account, never the personal one. Lesson `cloud-files-in-vm` (reference + gotcha: AmbyCloud logs fetches by pid; online-only items do not reach the bin) | ☑ 2026-10-23 |
| C10 | Contribute only as Ambysto (no trailer) | stays | rule | ☑ 2026-10-23 |
| C11 | GitHub accounts, `gh` and `vercel` wrappers | stays | rule | ☑ 2026-10-23 |
| C12 | Two identities, never mixed | stays | rule | ☑ 2026-10-23 |
| C13 | VM state 2026-10-16 (Windows build, SDKs, volumes, long paths, Defender, SCM right, Steady installed) | lesson | `win11-vm-state` (reference; `last_validated` 2026-10-16, so it ages first). The evaluation expiry 2027-01-13 stays in CLAUDE.md as one line: it blocks everything when it passes | ☑ 2026-10-23 |

| G1 | The guide block (lines 1–65: model economy, rating, loop, owner time log, working practice, switching, honesty) | stays | changed only through claudecode-guide PRs; step 4a adds the recall section there; step 5 never touches it | ☑ 2026-10-23 |

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
| Editing the guide while the APS-34 session works in its checkout | step 4a in its own worktree from `origin/main`; only the owner merges |
| The installer overwrites the machine section | `install.py` only rewrites between its markers (guide rule, checked by its `--check`); a backup is taken in step 5 anyway |
| `wire.py` damages a harness file the owner wrote (Hermes `SOUL.md`, Codex `AGENTS.md`) | markers only, broken markers refused, backup before every write, byte-for-byte tests including CRLF; hard-review of step 4b |
| A harness path in the table is wrong, so a harness never sees the paragraph | each path confirmed from the harness's docs or binary before wiring; proof 10 runs each installed harness without telling it the path |
| The recall text drifts between Claude Code and the others | one source, `scripts/recall.md`; `wire.py --check` compares it with the installed global block |

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
   lesson `plane-rest-api`. Run as `claude -p --permission-mode bypassPermissions`, as
   the owner's sessions run, so a permission prompt or the auto-mode credential block
   cannot fail it for a reason unrelated to recall. (Headless: no owner line in the time
   log.)
7. `check.py` lists a lesson whose `last_validated` is set back 91 days (from test 1).
8. Not run: Mac, owner step (list and migrate its auto-memory, clone, hook, setting, one
   recall).
9. Guide: `python scripts/check.py` and `python scripts/install.py --check` exit 0 after
   the step 4a merge and install.
10. Intent criterion 9: `wire.py --check` exit 0; `python3 -m unittest scripts/test_wire.py`
    all pass; then the task of proof 6, headless, once per installed harness, with the
    flags named per harness in the proof record (the non-interactive auto-approve flag and
    read access to `~/.claude.json` and to the clone outside the cwd), tier 2 first (Codex, Grok Build, Muse),
    then tier 3 (OpenCode, Antigravity, Hermes), from the same worktree, with no path in
    the prompt; each answer names `plane-rest-api`. A harness whose own login or quota
    fails, or that has no headless mode (Antigravity and Hermes may not), is reported as
    such ("not run: <reason>"), not as a recall failure. Oh My Pi,
    Cursor, Codewhale, DeepSeek Harness: "not run: not installed".

## Review log

**Round 1 (hard-reviewer: Fable 5.1, FAIL, 2026-10-23).** Every "dropped" claim was found
where the table says; no stays/split row moves a rule. Issues, all fixed in this revision:
1. MAJOR: the host check was under-specified (a bare-host match hits every file name).
   Fixed: URLs plus bare hosts with a short TLD list, deployment suffixes, suffix matching
   for allowed domains, `ambysto.com` allowed, tests both ways.
2. MINOR: "slug of the `name` field" was not in the intent's shape. Fixed: the file name
   is the slug, in both.
3. MINOR: the guide's local `main` lags. Fixed: fetch, worktree from `origin/main`.
4. MINOR: Steady's description headings are not in its `CLAUDE.md`. Fixed: into the lesson.
5. MINOR: the Plane workspace slug is identifying and uncatchable. Fixed: not copied,
   left out by rule.
6. MINOR: no row for the guide block. Fixed: row G1.
7. MINOR: headless proof could fail on permissions. Fixed: bypass mode named.
8. NIT: full SHAs vs the hex rule. Fixed: short SHAs allowed, full refused, tested.
9. NIT: A5 dropped the diff-range advice. Fixed: lesson `give-reviewers-a-diff-range`.
10. NIT: A8's signing-key line is superseded. Fixed: written as superseded.
11. NIT: when the ticks happen, and step 5's order. Fixed: ticks at plan acceptance;
    step 5 after step 2 merged and step 4a installed.

Also in this revision, at the owner's request: intent decisions 9–10 (the memory keeps
working if Claude Code stops; the harness fallback order), `AGENTS.md`, step 4b
(`wire.py`), proof 10.

**Round 2 (hard-reviewer: Fable 5.1, PASS, 2026-10-23).** Harness paths checked against
each binary or source (Codex, Grok, Muse, Antigravity, Hermes; OpenCode plausible). Six
issues after the PASS, all fixed:
1. MINOR: planted values in `test_check.py` would fail the real-repo check. Fixed: built
   at run time.
2. MINOR: sandboxed harnesses refuse the pull, and some have no headless mode. Fixed: the
   recall reads as is when refused; proof 10 names flags per harness and allows "not run".
3. MINOR: comparing with the installed guide tied the pre-commit to another repo. Fixed:
   moved to `wire.py --check`.
4. MINOR: Antigravity and Hermes paths left open. Fixed: `~/.gemini/GEMINI.md`;
   `~/.hermes/SOUL.md`, markers appended at the end.
5. NIT: `vn` added; three ways; extra deployment suffixes removed.
6. NIT: `AGENTS.md` displaces `CLAUDE.md` for some harnesses. Fixed: its first line points
   to `CLAUDE.md`.
