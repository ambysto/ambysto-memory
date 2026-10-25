---
title: Set Vercel rootDirectory to site and verify live HTTP bodies after deploy
kind: gotcha
applies_when: when deploying a repo whose landing page lives in site/ to Vercel
projects: all
evidence: 2026-10-25 ambysto-graph APS-40
last_validated: 2026-10-25
status: active
---

Check the Vercel project's `rootDirectory` setting over the Vercel REST API before deploying a repo whose static site lives under `site/`, and set `"rootDirectory": "site"` if it is `null`.
When replacing static images in place, append a cache-busting query string (such as `?v=2`) to their `<img>` URLs so browsers and edge caches fetch the new bytes immediately.
Why: a Vercel project linked to a repo with `rootDirectory: null` builds from the repository root instead of `site/`, returning HTTP 404 or stale assets even when the CLI prints a production URL.
Confirm: fetch the production URL and every demo route over HTTP and check that the response status is 200 and the body contains the new markup.
