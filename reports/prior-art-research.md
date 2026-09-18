# Prior-Art Research

- Researched at: 2026-09-18
- Mode: library skill / local-first memory and archive
- Evidence rule: repository descriptions and documentation are design references, not proof that this Skill has their runtime behavior.

## Reference scan

| Source | Reusable pattern | Adopted | Rejected or bounded |
| --- | --- | --- | --- |
| [OpenClaw Obsidian vault maintainer](https://github.com/openclaw/openclaw/tree/main/extensions/memory-wiki/skills/obsidian-vault-maintainer) | deterministic vault maintenance and conservative generated sections | stable generated output and explicit ownership boundary | no plugin installation or implicit vault-wide mutation |
| [Kepano Obsidian skills](https://github.com/kepano/obsidian-skills) | Obsidian-native Markdown, link semantics, optional CLI | UTF-8 Markdown, Vault links for notes, external links for local files, CLI optional | no hard dependency on a running Obsidian app |
| [AI Context Linker](https://github.com/xhonye/AI-Context-Linker) | discover candidates, review/approve a snapshot, compile a small brief, question-directed slices | explicit note allowlists, `context-manifest.json`, `ai_context.md`, truncation and sensitivity states | no automatic project approval, no Google Drive upload, no raw repository scan |
| [obsidian-agent-memory](https://github.com/mithunyc/obsidian-agent-memory) | context capsules, tiered retrieval, contradiction handling, session closeout | context ladder, evidence states, one linked closeout summary, conflict visibility | no semantic index or embedding dependency in the baseline package |
| [agent-memory-wiki](https://github.com/cobibean/agent-memory-wiki) | daily/session/handoff notes and portable memory workflow | concise session summaries and durable handoff fields | no raw chat archive or automatic background interception |
| [coding-agent-toolkit](https://github.com/stefan-jansen/coding-agent-toolkit) | shared workspace with explicit align/plan/ship/handoff phases | separate Memory Pull, implementation verification, and Memory Push phases | no attempt to make one client's hidden state visible to another |
| [GitHub Copilot agent skills](https://docs.github.com/en/copilot/how-tos/customize-copilot/custom-instructions/add-agent-skills) | portable `SKILL.md` plus optional scripts/references and project skill locations | lean entrypoint with deferred references and deterministic scripts | no vendor-specific activation claim beyond declared adapters |

## First-principles synthesis

The stable problem is not “lack of more notes”; it is an unbounded retrieval surface with unclear authority and no evidence state. The package therefore treats the Vault as the source of durable facts, generated reports as rebuildable views, and context briefs as reviewed projections. Every new capability must reduce omission risk without expanding default scan scope.

## Missing evidence

- No independent benchmark compares this package with the listed projects.
- No provider or human study proves that the new brief improves every task.
- Google Drive or ChatGPT web synchronization is intentionally not implemented or tested.
- Cross-device installation and non-AGENTS client binding remain configuration-dependent.
