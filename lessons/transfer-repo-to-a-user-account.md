---
title: Transferring a repo to a user account waits for that account to accept
kind: workflow
applies_when: when the owner asks to move a repo to another GitHub account and gh api repos/OWNER/NAME/transfer is the tool
projects: all
evidence: 2026-11-23 agentsocial moved from the owner's own account to the ambysto account
last_validated: 2026-11-23
status: active
---

Check the target first: `gh api users/NAME --jq .type`. An organisation takes the transfer at once; a user account must accept it from its e-mail or notification, and no agent can (the token guard refuses it), so tell the owner to accept.
Before sending, list what moves: open PRs go along, repo-level self-hosted runners and secrets must be checked after, the clone's remote and folder change, and the hosting project keeps its own team.
After acceptance: `git remote set-url origin`, move the clone under `~/work/ambysto/`, remove a repo-local `user.name` and `user.email` (they override the includeIf identity), run `git worktree repair <worktree paths>`, fetch.
The runner stayed registered and online in this case; the first merge still has to prove the deploy.
Confirm: `gh api repos/NEW/NAME --jq .full_name` works, `git config user.name` prints the Ambysto author, and the first CI run after a merge is green.
