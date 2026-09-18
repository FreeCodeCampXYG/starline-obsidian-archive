# Trust Report

- Package: `starline-obsidian-archive` 1.4.0
- Runtime dependencies: Python standard library only
- Network requirement: none for local memory, audit, brief, or archive generation
- Default external mutation: none
- Default source mutation: none
- Default write targets: selected Vault managed target, explicit brief output directory, or package-local files during development
- Sensitive data policy: no credentials, private keys, raw chat, browser caches, or cloud roots by default
- Permission boundary: archive roots and brief notes must be explicitly approved
- Rollback boundary: generated notes are marked and isolated; handwritten notes and original sources are outside the managed directory

## Verification status

- `scripts/index_artifacts.py`: existing unit coverage retained
- `scripts/audit_vault.py`: unit coverage added for unnamed and missing-authority findings
- `scripts/build_context_brief.py`: unit coverage added for explicit sources and sensitive-content blocking
- Provider telemetry, human output review, and second-device installation: `missing evidence`
