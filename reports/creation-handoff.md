# Creation Handoff

## Result

Created `starline-obsidian-archive` 1.0.0 and updated it to 1.3.1 in a compatible local Agent Skills directory; the 1.4.0 redesign is prepared in the public repository worktree before install-directory synchronization.

It inventories explicitly approved local creative/project sources, links them into an Obsidian vault without moving originals, produces repeatable group notes and a JSON manifest, and directs the agent to maintain durable project memory around the generated index. Publication was not requested.

Version 1.1.0 adds an optional, portable Vault-level `AGENTS.md` Pull / Push memory contract. It reads and preserves an existing root policy, establishes one only on explicit request, requires durable task-end updates, and documents that shared files are not a real-time raw-chat bridge.

Version 1.2.0 adds Global Memory Coordination mode. A compatible Agent can invoke this Skill around every non-trivial task to perform the required context Pull and durable-facts Push. Archive scanning remains explicitly scoped, so ordinary project work does not inventory local folders.

Version 1.3.0 adds opt-in session-summary mode. A substantive completed session creates one concise note linked to its authoritative project or system note, enabling Obsidian Backlinks without turning the Vault into a raw chat archive.

Version 1.3.1 promotes three reusable handoff rules from project practice: update an existing `DEV_STATE.md` (or equivalent) after confirmed code/configuration/production changes; verify that a requested global or workspace Agent binding is actually discoverable by the target client; and keep large binaries at approved project paths while the Vault stores links and durable status rather than copies.

Version 1.4.0 separates four routes: Memory Coordination, approved Archive, read-only Vault Audit, and explicit-list context compilation. It adds `audit_vault.py`, `build_context_brief.py`, evidence states, a context ladder, reviewed context manifests, truncation/sensitivity boundaries, and library output/trust profiles.

## Reference Skills Studied

- OpenClaw `obsidian-vault-maintainer`: learned deterministic generated sections, stable filenames and conservative rename behavior; incorporated in `references/vault-contract.md` and the generated-file marker.
- Kepano `obsidian-markdown`: learned the distinction between wikilinks for vault notes and Markdown links for external resources; incorporated in `scripts/index_artifacts.py` output.
- Kepano `obsidian-cli`: learned to probe an optional app/CLI rather than assuming it; the new package has no CLI dependency.
- Featured Image for Obsidian: learned bulk-preview, dedicated generated storage and exclusion mechanisms; incorporated as dry-run, `自动生成/` and explicit source exclusions.

## Absorbed and Rejected

- Keep: standards-compliant frontmatter, stable links and deterministic generated content.
- Adapt: work filesystem-first when Obsidian CLI is absent, and treat local originals as external links rather than importing them.
- Reject: plugin installation, remote asset downloading, implicit whole-disk scans and automatic edits to handwritten notes.
- Invent: source-relative manifests, an exact-duplicate boundary, safe `--prune` behavior, and privacy-aware source confirmation.

## Advantages and Evidence

- **[design advantage]** The generated directory is deliberately separate from project memory, so refreshes cannot overwrite the durable narrative notes.
- **[validated advantage]** `scripts/index_artifacts.py` completed a real three-source write: 505 records, 377 byte-level representatives, 19 groups and no source-file mutation.
- **[hypothesis]** Copying the package to another compatible agent's skills directory should allow the same workflow on a different computer; second-device installation evidence is missing.
- **[design advantage]** The cross-client memory policy uses the selected Vault path at runtime and asks non-AGENTS clients to receive an explicit equivalent instruction, avoiding false claims of automatic context bridging.

## Verification and Limits

- Package validation, trigger evaluation, Skill IR export and a local install-path check are recorded separately.
- The script uses only Python standard library modules and writes only after `--write` is supplied.
- It does not classify image semantics, infer ownership, back up to cloud, inspect unapproved chat/browser paths, or repair broken source links after a source root moves.
- `file:///` links refer to this machine's paths; rerun with new source roots after a migration.
