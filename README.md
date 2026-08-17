# Starline Obsidian Archive

`starline-obsidian-archive` connects user-approved local creative and project records to an Obsidian vault without relocating the originals. It creates a compact, repeatable index rather than a fragile pile of copied assets.

## What it does

- inventories images, video, audio, editable art files, and optionally prompts or project documents;
- keeps source paths relative to named source roots and adds clickable local file links;
- produces deterministic Obsidian Markdown group notes and a JSON manifest;
- optionally detects exact duplicate content with SHA-256;
- preserves hand-written project memory outside the generated folder.
- when explicitly requested, establishes a portable Vault-level `AGENTS.md` rule so compatible Agents retrieve context before work and write durable conclusions back after work.
- can run as a lightweight **Memory Coordination** Skill for every non-trivial Agent task, without scanning source folders unless archive work is explicitly requested.
- when enabled, creates one concise session-summary note per substantive completed session, linked to the authoritative project or system note rather than copying the chat.

## Install

Copy this directory into a compatible agent's skills directory, retaining its contents and UTF-8 encoding. The package has no network or third-party Python dependencies.

```bash
npx skills add FreeCodeCampXYG/starline-obsidian-archive
test -f ~/.agents/skills/starline-obsidian-archive/SKILL.md
```

## Prerequisites

- [ ] Python 3 available: `python --version`
- [ ] Node.js and npx available (only for `npx skills add` installs): `node --version && npx --version`
- [ ] A writable Obsidian vault path and explicitly approved source roots before any inventory write

## 你可以直接这样说

- “把我的绘画、分镜和视频素材链接进 Obsidian。”
- “盘点这几个作品目录，建立一个可持续同步的作品档案。”
- “将本机项目资料整理到现有 Obsidian 知识库，但不要搬动原文件。”
- “把这个 Obsidian 库设为所有项目的长期记忆，让 Agent 每次任务先检索后更新。”

## Quick start

First run an inventory without writes:

```bash
python scripts/index_artifacts.py \
  --vault "/path/to/Obsidian Vault" \
  --target "01-Projects/Creative Archive" \
  --source "Illustrations=/path/to/illustrations" \
  --source "Film project=/path/to/video-project" \
  --include-context
```

After checking the summary, add `--write`. Add `--hash-content` only when exact duplicate reporting is useful. The agent then links the archive from the vault's project index and writes the human-maintained project memory.

## Cross-client long-term memory

When explicitly requested, the skill first preserves any existing `<vault>/AGENTS.md`; otherwise it creates a portable root rule and a linked client protocol. The rule requires a task-start context Pull and a task-end durable-facts Push. It keeps the selected vault path local to the user's setup and never embeds the author's own path.

Saved Vault files are visible to other clients sharing that folder, but this does not bridge live chat histories or make every Agent automatically obey the rule. Clients that do not discover `AGENTS.md` must receive an equivalent global or workspace instruction. For VSCode/DeepSeek, configure that instruction in the specific extension's rules or system-prompt setting.

When a user asks for a global or workspace binding, verify the target client's actual rule file or settings path after applying the instruction; a shared Vault folder alone is not proof that the client loaded it. For projects with `DEV_STATE.md` (or an equivalent handoff note), update that note after confirmed code, configuration, or produced-artifact changes. Keep large binaries at their project path and store only links, verified status, and durable conclusions in the Vault.

## Global Agent use

Point a compatible Agent's global rule at `$starline-obsidian-archive` and require **Memory Coordination mode** before and after every non-trivial task. In this mode, the Skill retrieves task-relevant Vault notes first and synchronizes only durable, verified conclusions at the end. It does not run the media inventory script, hash files, or scan folders unless archive work and source roots were explicitly approved.

Enable **session-summary mode** when you want Backlinks from a project or system note back to a concise Agent-session handoff. The Skill creates one note per substantive completed session, links the authority note, and excludes raw dialogue, prompts, command output, and secrets. See [the session-summary contract](references/session-summary-mode.md).

## Verify

```bash
python -m py_compile scripts/index_artifacts.py
python scripts/index_artifacts.py --help
python /path/to/starline-meta-skill/scripts/validate_skill.py .
```

## Generated structure

```text
<vault>/<target>/
  项目记忆.md                 # human-maintained by the agent/user
  自动生成/
    资源总览.md               # deterministic source and group index
    资源清单.json             # source-relative inventory
    分组/
      <source-and-folder>.md  # one note per source folder group
```

The `自动生成` directory is owned by the synchronizer. Keep personal commentary in `项目记忆.md` or sibling notes so refreshes cannot overwrite it.

## Troubleshooting

### Obsidian does not open a source file

The generated link is a local `file:///` URI. Confirm the original file still exists and that the operating system permits local file links. The manifest also preserves its source label and relative path, so update the source configuration and rerun after moving a source root.

### The inventory includes non-creative files

Use narrower `--source` paths. The script already excludes common repository/cache folders; it deliberately does not infer authorship or artistic intent from a filename.

### A prior generated group is obsolete

Rerun after confirming the target. Add `--prune` only to remove obsolete notes that contain the script's `managed_by` marker; handwritten notes are never in that managed path.

### I need another Agent or VSCode extension to use the same memory

Add the portable instruction from [agent-memory-bridge.md](references/agent-memory-bridge.md) to that client's global or workspace rules. Ask for the exact extension name before attempting client-specific configuration; settings differ and this package does not claim automatic chat-context interception.

## Attribution

This package semantically adopts public ideas from [OpenClaw's Obsidian vault maintainer](https://github.com/openclaw/openclaw/tree/main/extensions/memory-wiki/skills/obsidian-vault-maintainer), [Kepano's Obsidian Markdown skill](https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-markdown), [Kepano's Obsidian CLI skill](https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-cli), and [Featured Image for Obsidian](https://github.com/johansan/obsidian-featured-image). Their source files were read for workflow ideas; no third-party code is executed or copied.

<!-- upstream_inspiration: https://github.com/openclaw/openclaw/tree/main/extensions/memory-wiki/skills/obsidian-vault-maintainer; https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-markdown; https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-cli; https://github.com/johansan/obsidian-featured-image -->

## License

MIT. See [LICENSE](LICENSE).
