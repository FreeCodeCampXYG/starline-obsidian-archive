# Agent Memory Bridge Contract

Use this contract only when the user explicitly asks to make an Obsidian vault a cross-project long-term memory system, or asks to connect multiple Agents or clients to the same durable project context.

## Preserve first, create only when needed

1. Resolve the target vault and read `<vault>/AGENTS.md` if it already exists.
2. Preserve an existing, equivalent vault policy. Improve it only within the user's requested scope; do not replace unrelated user rules.
3. If no equivalent policy exists, create a concise root `AGENTS.md` in the vault's prevailing language and link it from the vault's system or home note when such a structure exists.
4. Do not modify an Agent application's global settings, extensions, or system prompts unless the user explicitly asks for that client-specific configuration.

## Required portable policy content

The vault rule must state that the selected vault is the canonical long-term memory source and require every meaningful task to:

1. read the vault governance/index and search relevant project and reusable-knowledge notes before work;
2. create and register a project memory only when the task is genuinely a new project;
3. re-read a note before writing, preserve concurrent human or Agent changes, and record unresolved conflicts instead of silently merging them;
4. after a meaningful result, update only durable, confirmed background, preferences, decisions, verified deliverables, progress, pitfalls, failures, reusable solutions, and next steps;
5. when session-summary mode is enabled, create one concise session note linked to the authoritative project or system note before the final durable-facts update;
6. exclude secrets, credentials, private data, raw chat transcripts, temporary logs, and duplicate content; and
7. verify UTF-8, internal links, and any maintained state note after a structural or configuration change; when a project has `DEV_STATE.md` (or an equivalent handoff note), re-read and update it after confirmed code, configuration, or produced-artifact changes.

Use `<vault>` as a runtime placeholder in the package and examples. Never hard-code the skill author's own computer path into a portable skill.

## Cross-client boundary and handoff

A shared local or synced vault makes saved files visible to other clients. It does not automatically capture another application's reasoning, invoke its model, or bridge raw conversation context in real time. State this boundary plainly.

Provide a short, copyable instruction for clients that do not automatically discover `AGENTS.md`:

> Use `<vault>` as the canonical long-term memory source. Before every meaningful task, read and follow `<vault>/AGENTS.md` and retrieve relevant notes. After every meaningful task, update only durable, confirmed conclusions according to that rule. Never save secrets or raw chat transcripts.

Tell the user to add that instruction to the client's global or workspace rules. For a VSCode/DeepSeek integration, ask for the exact extension name before giving vendor-specific navigation, because rule-setting locations differ.

After the user requests a global or workspace binding, verify that the target client's rule file or settings path contains the instruction and report unsupported clients explicitly. A shared Vault folder is evidence of shared files only; it is not evidence that the client has loaded the rule.

## Global Agent integration

When a compatible Agent supports Skills, its global rules may designate `$starline-obsidian-archive` as the mandatory memory coordinator for every non-trivial task. The global rule must specify that the Skill runs in **Memory Coordination mode** by default: it reads the Vault policy and relevant context before work, then writes only durable, verified conclusions after completion.

The global rule must also state that artifact inventory, source scanning, hashing, and generated indexes remain opt-in: run them only when the user explicitly asks for archive work and has approved the source roots. This prevents an ordinary coding task from becoming an unapproved disk scan.

When the user enables session-summary mode, the global rule must require one concise note per substantive completed session. Put project summaries under the project's session-summary directory and system summaries under a system directory; link the authority note, capture only verified outcomes and next steps, and never save raw dialogue. See [the session-summary contract](session-summary-mode.md).

## Do not claim

- Do not claim real-time chat synchronization or semantic merging across arbitrary clients.
- Do not imply that a client will read `AGENTS.md` unless that client is known to support it or has been explicitly configured with the copyable instruction.
- Do not scan chat caches, browser data, or entire disks to reconstruct conversations without explicit scope and privacy approval.
