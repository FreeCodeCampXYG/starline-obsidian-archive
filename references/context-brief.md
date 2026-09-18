# Context Brief Contract

The context compiler is a file-backed adapter for planning and handoff. It is not a repository mirror, a model, an MCP server, or a replacement for implementation verification.

## Required flow

1. Name the Vault and explicitly select one or more project memories or Markdown notes.
2. Preview the source list and the per-source byte limit.
3. Review the generated `context-manifest.json` for `confirmed`, `needs_review`, and `blocked` sources.
4. Share `ai_context.md` only after that review. Bring decisions back to the coding Agent, which must re-check the real repository and tests.

`--project` means exactly `01-项目/<name>/项目记忆.md`; it does not recursively include the project's sessions or source files. Add a session or reusable note with a separate explicit `--note`.

## Output semantics

- `ai_context.md` is the small human/Agent-facing brief.
- `context-manifest.json` is the machine-readable source and status ledger.
- Truncated notes remain `needs_review` and include a visible boundary marker.
- Suspected credentials or private keys are `blocked`; their body is never written to the brief.
- Missing project facts remain unknown. The compiler never infers goals, priority, completion, ownership, or relationships from filenames or Git activity.

This follows the useful part of reviewed context-compilation systems: discover candidates, review/approve the snapshot, then build a portable brief. The approval decision remains with the user or calling Agent.
