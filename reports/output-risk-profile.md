# Output Risk Profile

## Scope

This package produces Markdown/JSON indexes, structure reports, context briefs, and session-navigation notes.

## Main risks and controls

| Risk | Control | Evidence required |
| --- | --- | --- |
| Agent reads the wrong project | context ladder and explicit project/note allowlist | manifest source list and project path |
| Unverified gaps appear as facts | `confirmed / derived / needs_review / blocked` states | rendered status and unresolved section |
| Sensitive content leaks into a brief | standard-library pattern check and blocked source record | secret fixture test; no secret body in output |
| Large notes hide relevant content | byte cap and visible truncation marker | `needs_review` status in manifest |
| Generated notes overwrite human work | dedicated `自动生成/` ownership boundary | managed marker and target-containment test |
| “Unnamed” cleanup changes meaning | read-only audit; no automatic rename | audit report only |
| External links stop working after a move | source-relative manifest and rerun instruction | source path and verification result |

## Review standard

Every delivered run states selected scope, excluded scope, verification, and next action. A report must not claim provider, runtime, human, or database evidence that the local run did not produce.
