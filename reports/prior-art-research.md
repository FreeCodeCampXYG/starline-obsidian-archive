# Prior-Art Research

- Researched at: 2026-08-16
- Queries: `Obsidian knowledge base organization`; `Obsidian vault project memory`; `Obsidian image asset catalog`; `local file inventory Obsidian`
- Catalogs: SkillsMP completed for all four queries; skills.sh was not run because this computer has no `npx` executable.
- Rating evidence: unavailable. SkillsMP exposes repository stars, not skill ratings; skills.sh installation telemetry is missing evidence in this run.

## Shortlist

| Candidate | Role and relevance | skills.sh installs | SkillsMP repo stars observed | GitHub source review | Adopt | License |
| --- | --- | ---: | ---: | --- | --- | --- |
| [OpenClaw `obsidian-vault-maintainer`](https://github.com/openclaw/openclaw/tree/main/extensions/memory-wiki/skills/obsidian-vault-maintainer) | Vault-maintenance pattern | missing evidence | 386,158 | Read `SKILL.md`; stable names, frontmatter, deterministic generated sections, CLI availability probe | Adapt deterministic output and no-destructive-rename rule | `NOASSERTION` in GitHub API at review time |
| [Kepano `obsidian-markdown`](https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-markdown) | Obsidian syntax/trust anchor | missing evidence | 45,427 | Read `SKILL.md`; distinguishes rename-aware wikilinks from external Markdown links and uses frontmatter | Keep that link split and UTF-8 Markdown contract | MIT |
| [Kepano `obsidian-cli`](https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-cli) | Optional local-app integration | missing evidence | 45,427 | Read `SKILL.md`; probes a running CLI before relying on it | Adapt “probe optional tool; never require it” | MIT |
| [Featured Image](https://github.com/johansan/obsidian-featured-image) | Media-archive specialist | not a skill catalog candidate | 121 | Read `README`; bulk processing, dry-run, dedicated generated storage and explicit exclusions | Adapt preview-first workflow and managed output boundary | MIT |

GitHub repository metadata was read directly on 2026-08-16. Current repository stars were 386,371 for `openclaw/openclaw`, 46,303 for `kepano/obsidian-skills`, and 121 for `johansan/obsidian-featured-image`. These repository-level signals measure attention, not skill quality.

## Contribution Ledger

### Keep

- Use valid Obsidian frontmatter and stable wikilinks for vault-native notes.
- Use standard Markdown links for external local files rather than pretending they are vault files.
- Generate deterministic sections and keep a clear ownership boundary around generated content.

### Adapt

- Make Obsidian CLI support optional: the package writes valid Markdown without requiring an open application or installed CLI.
- Replace automatic thumbnail/download behavior with source-relative inventory plus `file:///` links; this avoids copying, network access and media mutation.
- Use a dry-run before writes and an explicit `--prune` gate for stale generated notes.

### Reject

- Do not install a community plugin or execute third-party scripts; the archive works with Python's standard library.
- Do not automatically change note thumbnail/frontmatter properties or crawl an entire vault/disk.
- Do not assume a default vault path or environment variable, since silently targeting the wrong vault would be harmful.

### Invent

- Pair a user-approved source boundary with a portable `<target>/自动生成/` ownership boundary.
- Preserve both human-readable grouped notes and a machine-readable source-relative JSON manifest.
- Offer SHA-256 duplicate detection as an explicit option and state its exact-equality limitation.
- Teach the agent to separate visual work sources from privacy-sensitive chat/browser/cloud locations before creating links.

## Created Skill Advantages

- **Design advantage:** The package separates original sources, generated index data and handwritten project memory; this is visible in `references/vault-contract.md` and the script's target-containment checks.
- **Validated advantage:** The bundled script completed a real three-source archive without altering originals, producing 505 records, 377 unique byte-level representatives and 19 groups in the user's vault.
- **Hypothesis:** The explicit source boundary and dry-run review should reduce accidental privacy or code-asset ingestion on other computers; independent human review across unrelated vaults is missing evidence.

## Missing Evidence

- skills.sh installation telemetry is unavailable because `npx` is not installed on this computer.
- No public skill rating/review metric was available in the queried catalog.
- No provider-backed or blind human evaluation compares this package with the shortlisted candidates.
- Cross-device installation is designed and documented but has not been exercised on a second computer.
