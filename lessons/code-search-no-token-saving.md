---
title: Do not add local code-search CLI or MCP tools to save coding-agent tokens
kind: decision
applies_when: when proposing or adding a BM25, AST or symbol code-search CLI/MCP tool (such as ambysto-search or xerj) to cut agent token usage
projects: all
evidence: 2026-10-26 APS-41, ambysto-saveit PR #9, issue #10 (1,170-run Round 2 benchmark)
last_validated: 2026-10-26
status: active
---

Do not wire external ranked BM25 code-search CLI/MCP tools (`ambysto-search`, `xerj`) or global CLI output-rewriting proxies (`rtk`, `caveman`) to cut coding-agent token spend; use zero-token cross-agent handoff (`ambysto-saveit resume` / `tail --write`), anti-relitigation ledgers (`dead-end`), quiet verification gates (`gate`), and direct AST symbol definitions (`def` / `map`) instead.
Why: across 1,170 paired Claude Code task-runs on Django and Gitea plus upstream `xerj` `#2327` (`4df3931`), raw file reads were under 2% of total input while over 93% was per-turn prompt-cache replay (~470k tokens/turn), so extra search turns increased cost (+1.9% on H1, +8.9% on H2, +54.0% on H3).
Confirm: see `HANDOFF.md` and the 24-task evaluation harness in `~/work/ambysto/ambysto-saveit` (renamed from `ambysto-search`) and `scripts/handoff-tail.py` / `scripts/quiet-gate.py` in `~/work/ambysto/ambysto-1prompt`.
