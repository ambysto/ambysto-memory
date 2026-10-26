---
title: Do not add local code-search CLI or MCP tools to save coding-agent tokens
kind: decision
applies_when: when proposing or adding a BM25, AST or symbol code-search CLI/MCP tool (such as ambysto-search or xerj) to cut agent token usage
projects: all
evidence: 2026-10-26 ambysto-search PR #9, issue #10 (1,170-run Round 2 benchmark)
last_validated: 2026-10-26
status: active
---

Do not build, adopt, or wire external local code-search CLI/MCP tools (`ambysto-search`, `xerj`, or similar BM25/tree-sitter indexers) to reduce coding-agent token costs on single-session or multi-session (`--resume`) tasks; let agents use their built-in `Grep` and `Read` tools.
Why: across 1,170 paired Claude Code task-runs on Django and Gitea (`ambysto/ambysto-search` PR #9, archived), raw file reads were under 2% of total input (~6k of ~480k tokens) while over 93% was per-turn prompt-cache replay across the edit-and-test loop; neutral tool adoption was 2.1% (0.6% in resumed session 2) and directive adoption added a turn and increased input tokens (+3.8%).
Confirm: see `REPORT.md` under `bench/agents/results/` (Round 2, 2026-10-25) in `ambysto/ambysto-search` before evaluating any code-search token-saving claim.
