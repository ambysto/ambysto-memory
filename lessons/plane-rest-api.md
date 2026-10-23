---
title: Reach Plane over REST with a custom User-Agent and the key read at run time
kind: reference
applies_when: when a session must read or write Plane tickets and no Plane tool is loaded
projects: all
evidence: 2026-10-16 steady SIC-130; 2026-10-17 ambysto-gate; 2026-10-23 APS-36; 2026-10-23 APS-31
last_validated: 2026-10-23
status: active
---

Base URL, workspace slug and API key are in `~/.claude.json`, the `plane` MCP server's `env`, which sits under `projects["<home dir>"].mcpServers.plane`, not top-level `mcpServers` (`PLANE_BASE_URL`, `PLANE_WORKSPACE_SLUG`, `PLANE_API_KEY`). Read them at run time inside the script; never print the key.
Calls go to `<base>/api/v1/workspaces/<slug>/…` with header `X-API-Key`. Send any custom `User-Agent`: Python's default one gets HTTP 403.
Find a project's id by its identifier with `GET projects/`, and its states with `GET projects/<id>/states/`; do not copy ids into notes or GitHub.
Create: `POST projects/<id>/issues/` with `name`, `state`, `labels`, `description_html`. Link a PR: `POST projects/<id>/issues/<issue id>/links/` with `url` and `title`.
Language per project: APS and AGD in English; SIC ticket names in Vietnamese, descriptions with sections Bối cảnh / Đã làm / Tiêu chí xong.
Never put the Plane host, workspace or ids on GitHub: PRs name the ticket only ("Plane: APS-36").
Auto mode's classifier blocks reading the key ("Credential Exploration"); the owner switches to accept-edits for it.
Confirm: `GET projects/` returns the project list with HTTP 200.
