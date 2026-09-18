# Memory Contract

## Context ladder

Read the smallest set that can answer the task:

1. `<vault>/AGENTS.md` and the system governance note.
2. `01-项目/项目总览.md` and the matching project's `项目记忆.md`.
3. Relevant notes in `02-复用知识/`, selected by task keywords.
4. One to three recent session summaries only when they answer an open loop.
5. Source records, code, or generated indexes only when the user explicitly asks for archive or evidence work.

The ladder prevents a large Vault from becoming an unbounded prompt. A smaller, targeted context with visible gaps is more reliable than a large context that hides the relevant project among historical notes.

## Evidence states

| State | Meaning | Agent behavior |
| --- | --- | --- |
| `confirmed` | Directly read or verified in the current task | May be used as a fact |
| `derived` | A bounded inference from confirmed sources | Label the inference and its basis |
| `needs_review` | Missing, stale, truncated, conflicting, or human-classification work | Do not silently promote to fact |
| `blocked` | Permission, privacy, sensitivity, or tool boundary stopped the operation | Preserve the reason and the safe next step |

## Push rules

- Re-read the target note immediately before updating it.
- Update the project memory first; update project indexes or reusable knowledge only when the result is durable and belongs there.
- Create exactly one concise session summary for a substantive session when the Vault policy enables summaries.
- Do not write raw dialogue, temporary logs, credentials, or duplicate source material.
- When sources conflict, keep the newer verified conclusion and record the unresolved conflict instead of merging guesses.

## Cross-client boundary

The Vault shares saved files and explicit context bundles. It does not share live reasoning, hidden chat history, authentication state, or semantic understanding between clients. A client that does not discover `AGENTS.md` must receive the portable instruction from `agent-memory-bridge.md` in its own rules.
