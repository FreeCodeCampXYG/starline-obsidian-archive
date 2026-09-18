---
name: starline-obsidian-archive
description: "Maintain an Obsidian vault as a safe, cross-agent project memory and local archive. Use for explicit Vault memory Pull/Push, linked session summaries, approved local media/project indexing, Vault structure audits, or reviewable AI context briefs built from approved notes. Separate durable facts from raw conversations, preserve originals, keep unknowns visible, and generate deterministic Markdown/JSON outputs. Do not use for image generation, cloud backup, whole-disk scanning, raw-chat capture, live chat bridging, automatic note renaming, or destructive cleanup."
author: "墨点星痕 (starline)"
version: "1.4.0"
---

# Starline Obsidian Archive

Use this skill as a controlled memory and local-archive workflow. The Vault is the durable human-readable source; generated indexes and briefs are rebuildable views.

## Routes

- **Memory Coordination**: read the runtime Vault policy, governance, project index, matching project memory, and relevant reusable notes before meaningful work; after verified work, create one linked summary when required and push only durable facts.
- **Archive**: require explicit source roots and a dry-run; write only under the selected target's `自动生成/`, never move or mutate originals.
- **Context Brief**: require explicit `--project` or `--note` allowlists; generate `ai_context.md` and `context-manifest.json` with visible source, truncation, and sensitivity states.
- **Vault Audit**: run the read-only structure audit for unnamed paths, missing project authorities, index gaps, and broken links; report findings as `needs_review` and do not auto-repair.

## Common workflow

1. Resolve the Vault path at runtime and read `<vault>/AGENTS.md`.
2. Use the context ladder: governance -> project index -> one project memory -> relevant reusable knowledge -> explicit detail. Do not read the whole Vault by default.
3. Re-read each target note immediately before writing. Use `confirmed`, `derived`, `needs_review`, and `blocked`; never turn absence into a fact.
4. After code/configuration/artifact changes, update an existing `DEV_STATE.md` or equivalent with verified results and known gaps.
5. Return scope, evidence state, changed paths, verification, unresolved risks, and next step.

## Boundaries

- Preview before archive or brief writes; show roots, counts, exclusions, and hash status.
- Keep UTF-8 Markdown/JSON and standard-library scripts. Obsidian CLI is optional.
- Do not scan chat, browser, email, cloud, system, dependency, or unapproved project paths.
- SHA-256 proves byte equality only; it does not prove ownership, semantic similarity, or deletion safety.
- A shared Vault does not bridge hidden reasoning, live chat, credentials, or login state between clients.

## Contracts

Archive output remains `资源总览.md`, grouped notes, and `资源清单.json`. Context output is `ai_context.md` plus `context-manifest.json`. Handwritten project memory stays outside managed output. Read details only when needed: `references/memory-contract.md`, `references/context-brief.md`, `references/vault-structure.md`, `references/agent-memory-bridge.md`, `references/session-summary-mode.md`, `references/source-safety.md`, `references/vault-contract.md`, and `evals/trigger_cases.json`.

This skill does not install Obsidian plugins, sync cloud storage, recover deleted files, classify artistic quality, save raw chat, or silently rename/move Vault content.
