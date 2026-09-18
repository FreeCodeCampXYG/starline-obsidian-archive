# Starline Obsidian Archive

`starline-obsidian-archive` is a local-first, reviewable memory and archive workflow for Obsidian. It keeps the Vault human-readable, preserves original files, and gives Agents a small context ladder instead of asking them to read an ever-growing folder blindly.

## Four modes

- **Memory Coordination** reads Vault policy and relevant project context before a meaningful task, then writes only durable verified conclusions after completion.
- **Archive** indexes explicitly approved local media or project records into a target `自动生成/` directory without moving originals.
- **Context Brief** compiles explicitly approved project memories or notes into `ai_context.md` and `context-manifest.json` for planning, handoff, or manual ChatGPT upload.
- **Vault Audit** reports unnamed paths, missing project authorities, index gaps, and broken internal links without changing notes.

The modes are deliberately separate: a normal coding task does not become a Vault scan, and a context brief does not become a codebase upload.

## Install

Copy this directory into a compatible Agent Skills directory, retaining UTF-8 encoding:

```bash
npx skills add FreeCodeCampXYG/starline-obsidian-archive
test -f ~/.agents/skills/starline-obsidian-archive/SKILL.md
```

The package uses Python's standard library only. Python 3 is required for the scripts; Node.js/npx is only required by the installer.

## Context brief quick start

Preview a small, explicit context set:

```bash
python scripts/build_context_brief.py \
  --vault "/path/to/Obsidian Vault" \
  --project "my-project" \
  --note "02-复用知识/技术方案索引.md" \
  --question "What should I verify before the next implementation?" \
  --output-dir "./context-output"
```

Review the source list and then add `--write`. The compiler does not recursively include session logs, source code, chat exports, cloud files, or dependencies. Oversized notes are marked `needs_review`; suspected credentials are `blocked` and their content is not written.

## Vault audit quick start

```bash
python scripts/audit_vault.py \
  --vault "/path/to/Obsidian Vault" \
  --output "00-系统/自动生成/结构审计"
```

The report is read-only evidence. It does not decide what an unnamed note should be called and does not auto-repair links.

## Archive quick start

Always preview first:

```bash
python scripts/index_artifacts.py \
  --vault "/path/to/Obsidian Vault" \
  --target "01-项目/作品档案" \
  --source "Illustrations=/path/to/illustrations" \
  --include-context
```

After reviewing counts, exclusions, privacy boundaries, and optional hashing, add `--write`. Generated files stay under the target's `自动生成/` directory; handwritten project memory stays outside it.

## Memory contract

Use `<vault>/AGENTS.md` as the runtime policy. The default retrieval order is governance -> project index -> one project memory -> relevant reusable knowledge -> explicit detail. Use `confirmed`, `derived`, `needs_review`, and `blocked` to prevent gaps from becoming invented facts. See [references/memory-contract.md](references/memory-contract.md), [references/context-brief.md](references/context-brief.md), and [references/vault-structure.md](references/vault-structure.md).

Saved Vault files are visible to other clients sharing the folder, but this does not bridge live reasoning or hidden chat history. Clients that do not discover `AGENTS.md` need the portable instruction in [references/agent-memory-bridge.md](references/agent-memory-bridge.md).

## Privacy and safety

- no cloud upload or third-party runtime dependency;
- no raw chat, browser cache, email store, credential, or private-key capture;
- no implicit whole-disk or whole-Vault brief generation;
- no source move, rename, delete, or copy by default;
- SHA-256 means exact byte equality only, not semantic similarity or deletion approval.

## Prior art

The design adapts deterministic generated views and conservative boundaries from OpenClaw/Kepano Obsidian skills, reviewed snapshot and question-directed brief ideas from [AI Context Linker](https://github.com/xhonye/AI-Context-Linker), tiered retrieval and closeout ideas from [obsidian-agent-memory](https://github.com/mithunyc/obsidian-agent-memory) and [agent-memory-wiki](https://github.com/cobibean/agent-memory-wiki), and explicit align/plan/ship/handoff separation from [coding-agent-toolkit](https://github.com/stefan-jansen/coding-agent-toolkit). No third-party code is copied or executed.

## License

MIT. See [LICENSE](LICENSE).
