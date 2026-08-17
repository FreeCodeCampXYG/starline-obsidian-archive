---
name: starline-obsidian-archive
description: |
  Organize explicitly scoped local project, art, image, video, and creation-record files into a safe, portable Obsidian knowledge-base archive. It can also act as a global Agent's Memory Coordination mode: retrieve relevant Vault context before every non-trivial task, create one concise linked session summary for a substantive completed session, and sync only durable conclusions after verified completion. Inventory sources in place, create linked index notes, detect optional exact duplicates, sync durable project context, and, when explicitly requested, establish a vault-wide AGENTS.md Pull / Push protocol for cross-project and cross-client long-term memory without moving originals. Use when users ask to organize, catalog, link, archive, continuously maintain local creative/project records, make an Obsidian vault a shared long-term memory system, request session summaries linked to project notes, or explicitly invoke this Skill as a task-memory coordinator. Do not use for image generation, cloud backup, raw-chat backup, real-time chat interception, or destructive file cleanup.
author: "墨点星痕 (starline)"
version: "1.3.1"
---

# Starline Obsidian Archive

Use this skill to turn a user-approved set of local creative or project-record folders into an Obsidian-native, repeatable archive. The source files remain where they are; the vault contains durable notes, grouped file links, and a machine-readable manifest.

## Global Memory Coordination Mode

When a global Agent invokes `$starline-obsidian-archive` for an ordinary non-trivial task, use this lightweight mode instead of the artifact workflow:

1. Resolve the Vault, read `<vault>/AGENTS.md`, and perform the required Memory Pull over relevant governance, project, and reusable-knowledge notes.
2. Execute the actual task using that retrieved context.
3. If the session produced a durable result, create exactly one concise session-summary note before the final Memory Push. Follow [the session-summary contract](references/session-summary-mode.md): link the authoritative project or system note, retain only verified outcomes and next steps, and never copy raw dialogue.
4. Re-read the relevant project memory and perform the required Memory Push with only durable, confirmed conclusions. If there is no durable result, record nothing and create no summary.
5. Do not inventory, hash, scan, move, or generate any artifact index unless the user explicitly requested archive work and approved the source roots.

This mode coordinates memory; it does not intercept live chats or make another application's reasoning available in real time.

### Project State Handoff

When the task changes code, configuration, or a produced project artifact, check whether the project has a `DEV_STATE.md` or equivalent handoff note. Re-read it before updating, then record only confirmed goals, completed work, key decisions, core files, verification, known issues, failed approaches, and next steps. Do not paste raw logs, temporary diagnostics, or secrets. Do not create a new state file unless the project convention or the user's requested scope calls for one.

### Client Binding Verification

When the user asks to bind this coordinator to a global or workspace Agent, read the target client's existing rules first, apply the smallest explicit instruction, and verify that the rule is discoverable at the requested path. If the client does not support `AGENTS.md`, provide the copyable Vault instruction and report that live interception is unsupported. Do not treat a shared folder or a written rule as proof that a client is actually using it.

## Guardrails

- Read the existing vault index, project notes, and reusable-knowledge notes before changing anything. Follow the vault's established layout when it has one.
- Before every run, look for `<vault>/AGENTS.md`. If it exists, read it first and obey its retrieval, update, privacy, conflict, and verification rules in addition to this skill. If it does not exist, retrieve the vault index and relevant project notes before acting.
- Discover candidate locations read-only first. Treat chat-app caches, browser data, cloud-sync folders, system folders, and source-code dependencies as out of scope unless the user explicitly names them.
- Show the proposed source roots, approximate file count, total size, exclusions, and whether content hashing will run before the first write.
- Never move, rename, delete, upload, or copy original source files by default. Do not store secrets, credentials, or private conversation exports in the vault.
- Generate only into `<target>/自动生成/`; preserve handwritten project notes. Use `--prune` only after confirming that the managed-folder boundary is correct.
- Only when the user explicitly asks to make a vault a cross-project long-term memory system, establish or update a portable root `AGENTS.md` and a linked protocol note. Never hard-code the author's own vault path into a reusable package; use the selected vault path at runtime.
- A shared vault synchronizes saved files, not live application reasoning or raw chat context. Tell the user that non-AGENTS clients need an equivalent global or workspace instruction; do not claim automatic real-time chat bridging.
- Session summaries are session-level navigation notes, not chat backups. Keep one summary per substantive session and make its project or system note the authority for durable facts.
- Keep large generated binaries and source assets at their approved project paths; store links, verified status, and concise conclusions in the Vault instead of copying bulky artifacts into it.

## Compact Workflow

1. Resolve the vault path. Read `<vault>/AGENTS.md` when present, then retrieve its relevant index, project-memory, and reusable-knowledge notes. If the user explicitly requests a shared long-term memory system and no equivalent policy exists, add a portable root rule and linked client protocol following [the agent-memory bridge contract](references/agent-memory-bridge.md).
2. If the user explicitly requested archive work and approved source roots, inventory them with the bundled script in dry-run mode. Use media files by default; add `--include-context` only when scripts, prompts, or design documents are part of the record. Otherwise use Global Memory Coordination Mode and skip directly to the applicable durable project-memory update.
3. For archive work, review counts, candidate groups, excluded directories, unreadable files, and the likely privacy boundary. Narrow false-positive sources before writing.
4. For approved archive work, run with `--write`; add `--hash-content` when exact duplicate detection is worth the I/O cost. The script writes an index, group notes, and a JSON manifest with source-relative paths plus clickable local `file:///` links.
5. Create or update the human-maintained project memory: background, durable preferences, key decisions, completed content, current state, failed approaches, pitfalls, reusable techniques, and next steps. If the project has a `DEV_STATE.md` or equivalent, update it for confirmed code/configuration/production changes and include verification results. Register the project memory in the vault's central project index using the existing table or convention. For a substantive completed session, create one concise linked session summary before this Memory Push, following [the session-summary contract](references/session-summary-mode.md). Write only durable, confirmed facts; do not save raw conversation text or sensitive data.
6. Verify strict UTF-8 decoding, generated wikilinks, target containment, source-file counts, and that originals have not been modified. Record any uncertain classifications as needing review.
7. On later tasks, perform the vault's required Memory Pull before work and its Memory Push after a meaningful result. Retrieve the archive's project memory and generated index first when archive work is requested; rerun the same source configuration only when source changes need synchronization.

## Bundled Inventory Command

```bash
python scripts/index_artifacts.py \
  --vault "/path/to/vault" \
  --target "01-Projects/Creative Archive" \
  --source "Personal art=/path/to/images" \
  --source "Video project=/path/to/project" \
  --include-context \
  --hash-content \
  --write
```

The script defaults to dry-run. It accepts Windows, macOS, and Linux paths, writes only inside the chosen vault target, and does not depend on Obsidian being open. See [the vault contract](references/vault-contract.md) and [source-safety rules](references/source-safety.md).

## Output Contract

Deliver:

1. a source inventory and the final approved source boundaries;
2. a project-memory note and a central-index link that fit the current vault;
3. `<target>/自动生成/资源总览.md`, source-group notes, and `资源清单.json` produced by the bundled script;
4. a concise report of file counts, duplicate handling, exclusions, verification, and anything requiring manual classification; keep large source or generated binaries at their approved project paths and record links/status rather than copying them into the Vault;
5. no altered original assets, no copied credentials, and no claims that unreviewed files are artistic works.
6. when explicitly requested, a portable vault-level `AGENTS.md` and client protocol that require task-start retrieval and durable task-end updates, while clearly excluding real-time raw-chat bridging.
7. when session-summary mode is enabled, one concise session note per substantive completed session, linked to its authoritative project or system note without a raw transcript.

## Exclusions

Do not use this skill to generate images, synchronize a vault to cloud storage, recover deleted files, install an Obsidian plugin, or silently scan an entire disk. For code-repository documentation without local creative/media records, use the appropriate project-documentation workflow together with this Skill's Global Memory Coordination Mode when the global Agent rule requires it.
