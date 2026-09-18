#!/usr/bin/env python3
"""只读审计 Obsidian Vault 的命名、主档案、索引和内部链接。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


EXCLUDED_DIRS = {".obsidian", ".git", "自动生成", "node_modules", "__pycache__"}
UNNAMED_STEMS = {"未命名", "Untitled", "New note", "新建笔记", "无标题"}
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


@dataclass
class Finding:
    """保存一项需要人审的结构发现，不擅自替用户改名或补档案。"""

    status: str
    kind: str
    path: str
    detail: str


def is_within(path: Path, parent: Path) -> bool:
    """判断输出是否仍在用户指定的 Vault 内，避免报告路径越界。"""

    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def is_unnamed(path: Path) -> bool:
    """识别常见占位名称；仅产生建议，不代表可以自动重命名。"""

    return path.stem in UNNAMED_STEMS or path.name.lower().startswith("untitled ")


def relative(vault: Path, path: Path) -> str:
    """以 Vault 相对路径保存审计证据，避免把本机绝对路径写入共享报告。"""

    return path.resolve().relative_to(vault.resolve()).as_posix()


def iter_notes(vault: Path) -> list[Path]:
    """遍历 Markdown/Base 文件，但跳过应用配置和受管自动生成区。"""

    notes: list[Path] = []
    for path in vault.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".base"}:
            continue
        parts = set(path.relative_to(vault).parts)
        if parts & EXCLUDED_DIRS:
            continue
        notes.append(path)
    return sorted(notes, key=lambda item: relative(vault, item).casefold())


def has_frontmatter_type(text: str) -> bool:
    """判断笔记是否声明 type，保持审计器不依赖第三方 YAML 解析器。"""

    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end < 0:
        return False
    return bool(re.search(r"(?m)^type\s*:", text[3:end]))


def resolve_wikilink(vault: Path, source: Path, target: str) -> bool:
    """解析常见 Obsidian 内链，未识别的特殊链接保留为待人工确认。"""

    target_path = Path(target.strip())
    candidates = [vault / target_path, vault / f"{target_path}.md"]
    for ancestor in (source.parent, *source.parents):
        if not is_within(ancestor, vault):
            continue
        candidates.extend([ancestor / target_path, ancestor / f"{target_path}.md"])
    if any(candidate.resolve().exists() for candidate in candidates):
        return True
    # Obsidian 对不带目录的链接按笔记名解析；只要全库恰好存在一个同名笔记，
    # 就不能把它标为断链，否则大量合法的 [[项目记忆]] 会污染人工审计队列。
    if len(target_path.parts) == 1:
        stem = target_path.stem
        matches = [path for path in vault.rglob(f"{stem}.md") if EXCLUDED_DIRS.isdisjoint(path.relative_to(vault).parts)]
        return len(matches) == 1
    return False


def audit(vault: Path) -> tuple[dict[str, object], list[Finding]]:
    """执行只读结构审计，并把推断性问题标为 needs_review。"""

    notes = iter_notes(vault)
    findings: list[Finding] = []
    for path in notes:
        rel = relative(vault, path)
        if is_unnamed(path):
            findings.append(Finding("needs_review", "unnamed", rel, "占位名称需要人工确认语义后再改名"))

    project_root = vault / "01-项目"
    registered = ""
    index_path = project_root / "项目总览.md"
    if index_path.exists():
        registered = index_path.read_text(encoding="utf-8")
    project_dirs = sorted((item for item in project_root.iterdir() if item.is_dir()), key=lambda item: item.name.casefold()) if project_root.is_dir() else []
    for project in project_dirs:
        memory = project / "项目记忆.md"
        rel = relative(vault, project)
        if not memory.exists():
            findings.append(Finding("needs_review", "missing_project_memory", rel, "项目目录缺少唯一主档案 项目记忆.md"))
        if project.name not in registered:
            findings.append(Finding("needs_review", "unregistered_project", rel, "项目目录未在 01-项目/项目总览.md 登记"))

    for path in notes:
        if path.suffix.lower() != ".md":
            continue
        if "模板" in path.stem:
            # 模板中的 [[项目记忆]] 是待实例化占位符，不应污染断链报告。
            continue
        text = path.read_text(encoding="utf-8")
        for target in WIKILINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://")):
                continue
            if not resolve_wikilink(vault, path, target):
                findings.append(Finding("needs_review", "broken_wikilink", relative(vault, path), f"内链目标不存在：{target}"))

    counts = Counter(path.suffix.lower() for path in notes)
    report = {
        "schema_version": 1,
        "managed_by": "starline-obsidian-archive",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "vault_relative_scope": ".",
        "notes": len(notes),
        "extensions": dict(sorted(counts.items())),
        "findings": len(findings),
        "status_counts": dict(sorted(Counter(item.status for item in findings).items())),
        "findings_detail": [asdict(item) for item in findings],
    }
    return report, findings


def render_markdown(report: dict[str, object]) -> str:
    """把机器审计结果渲染成可扫描的人工复核报告。"""

    lines = [
        "---",
        "type: vault-structure-audit",
        "managed_by: starline-obsidian-archive",
        f"generated_at: {report['generated_at']}",
        "---",
        "",
        "# Vault 结构审计",
        "",
        "> [!warning] 只读报告\n> 发现项只提供证据和建议，不自动重命名、移动、删除或补写笔记。",
        "",
        f"- Markdown/Base 文件：{report['notes']}",
        f"- 发现项：{report['findings']}",
        f"- 状态统计：`{json.dumps(report['status_counts'], ensure_ascii=False)}`",
        "",
        "## 发现项",
        "",
        "| 状态 | 类型 | 路径 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for item in report["findings_detail"]:
        lines.append(f"| {item['status']} | {item['kind']} | `{item['path']}` | {item['detail']} |")
    if report["findings"] == 0:
        lines.append("| confirmed | none | - | 未发现结构问题 |")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    """定义默认只读的审计命令。"""

    parser = argparse.ArgumentParser(description="只读审计 Obsidian Vault 结构。")
    parser.add_argument("--vault", required=True, help="Obsidian Vault 根目录。")
    parser.add_argument("--output", help="Vault 内报告目录，例如 00-系统/自动生成/结构审计。")
    parser.add_argument("--json", action="store_true", help="将 JSON 审计结果输出到标准输出。")
    return parser.parse_args()


def main() -> int:
    """执行审计并在显式指定输出目录时写入受限报告。"""

    args = parse_args()
    vault = Path(args.vault).expanduser().resolve()
    if not vault.is_dir():
        print(f"错误：Vault 不存在：{vault}", file=sys.stderr)
        return 2
    try:
        report, _ = audit(vault)
    except (OSError, UnicodeError) as exc:
        print(f"错误：读取 Vault 失败：{exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"审计完成：{report['notes']} 个 Markdown/Base 文件，{report['findings']} 项需要人工确认。")
    if args.output:
        output_dir = (vault / Path(args.output)).resolve()
        if not is_within(output_dir, vault):
            print("错误：--output 必须位于 Vault 内。", file=sys.stderr)
            return 2
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "vault-structure-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        (output_dir / "vault-structure-audit.md").write_text(render_markdown(report), encoding="utf-8", newline="\n")
        print(f"已写入只读报告：{output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
