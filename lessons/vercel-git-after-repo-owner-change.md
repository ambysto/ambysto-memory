---
title: Reinstall the Vercel GitHub app after a repo moves to another GitHub owner
kind: gotcha
applies_when: when `vercel git connect` fails with "Failed to connect <owner>/<repo> to project … you have access to the repository if it's private", or a repo was transferred and merges stopped deploying
projects: all
evidence: 2026-11-24 aipub (ambysto/aipub moved to dunfoju/aipub-landing), AIPUB-56
last_validated: 2026-11-24
status: active
match: \bvercel\s+git\s+connect\b
---

A transfer drops the Vercel git link, and the Vercel login is not the problem: the Vercel GitHub app must be installed on the new owner.
1. An admin of the new owner (accept a pending invite first: `gh api user/memberships/orgs/<org>` shows `pending`) opens https://github.com/apps/vercel/installations/new, picks the org, "Only select repositories", ticks the repo, Install.
2. In each linked folder (one per Vercel project, e.g. the root for `dist`, `labs/app` for a mockup): `vercel git connect https://github.com/<org>/<repo> --yes`.
3. Confirm: `vercel api /v9/projects/<name>` shows a `link` object whose `org`, `repo` and `productionBranch` are the new owner, the repo and `main`.
Why: until then nothing deploys on merge, so deploys silently fall back to the CLI; the aipub session spent three owner exchanges suspecting the Vercel account.
Remember: once reconnected, a merge to `main` publishes again; ask before merging where the repo's CLAUDE.md says so.
