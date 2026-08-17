# Vault Contract

## Ownership boundary

The synchronizer may write only beneath the chosen relative target inside the vault. Its managed area is `<target>/自动生成/`; every generated Markdown file carries `managed_by: starline-obsidian-archive` frontmatter. Handwritten notes must live outside that directory.

## Stable outputs

- `资源总览.md` is the human-readable source and group index.
- `资源清单.json` is the complete, source-relative machine-readable manifest.
- `分组/*.md` provides one concise table per source-and-folder group.

All Markdown is UTF-8. Notes link to other vault notes with wikilinks. Source files outside the vault use standard Markdown `file:///` links because they are external resources, not rename-tracked vault notes.

## Refresh behavior

The script is dry-run unless `--write` is passed. A refresh overwrites only current managed files. `--prune` can remove stale generated group files after confirming their marker; it never removes non-managed files or any source file.

## Project-memory integration

The script deliberately does not overwrite `项目记忆.md` or a vault-wide project index. The agent updates those human-maintained notes after reviewing the generated inventory, matching the current vault's format and retaining only durable facts.

## Vault-level agent rules

Before every archive run, the agent checks for `<vault>/AGENTS.md`. When present, it is the vault's controlling contract for task-start retrieval, task-end durable updates, privacy, conflict resolution, and state maintenance. This skill supplements that contract; it does not overwrite it.

Only when the user explicitly requests a cross-project long-term memory system and no equivalent policy exists may the agent create a concise root `AGENTS.md` and a linked protocol note. The policy must use the selected vault path at runtime, require a project-context Pull before work and a durable-facts Push after meaningful work, and prohibit secrets and raw chat transcripts. See [the agent-memory bridge contract](agent-memory-bridge.md).

## Session-summary integration

When enabled by the user's Vault policy, a substantive completed Agent session receives one concise Markdown summary before the final project-memory update. Store it outside the managed `自动生成/` area, place it under the project's session-summary directory or the Vault's system-session directory, and link its authoritative project or system note. It is a navigation and handoff note, not a transcript. See [the session-summary contract](session-summary-mode.md).
