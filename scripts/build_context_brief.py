#!/usr/bin/env python3
"""从用户明确批准的 Vault 笔记生成小型、可审阅的 AI 上下文简报。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


MANAGED_BY = "starline-obsidian-archive"
SECRET_PATTERN = re.compile(
    r"(?:sk-[A-Za-z0-9]{12,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"AIza[0-9A-Za-z_-]{20,}|xox[baprs]-[0-9A-Za-z-]{12,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|"
    r"(?:password|passwd|token|api[_ -]?key)\s*[:=]\s*[^\s`]{8,})",
    re.IGNORECASE,
)


def is_within(path: Path, parent: Path) -> bool:
    """限制输入笔记在 Vault 内，防止项目参数变成任意文件读取器。"""

    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def safe_vault_path(vault: Path, value: str) -> Path:
    """解析 Vault 相对路径，拒绝绝对路径和父级跳转。"""

    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"路径必须是 Vault 内相对路径：{value}")
    resolved = (vault / candidate).resolve()
    if not is_within(resolved, vault) or not resolved.is_file():
        raise ValueError(f"Vault 文件不存在：{value}")
    return resolved


def read_source(path: Path, vault: Path, max_bytes: int) -> dict[str, object]:
    """读取已批准 Markdown，并在超长或疑似敏感时保留明确状态。"""

    relative = path.relative_to(vault).as_posix()
    raw = path.read_text(encoding="utf-8")
    if SECRET_PATTERN.search(raw):
        # 敏感内容不应被“截断后顺便上传”；默认阻断并只保留路径和原因。
        return {"path": relative, "status": "blocked", "reason": "疑似包含凭据或私钥，未写入简报"}
    encoded = raw.encode("utf-8")
    truncated = len(encoded) > max_bytes
    if truncated:
        content = encoded[:max_bytes].decode("utf-8", errors="ignore")
        content += "\n\n> [!warning] 内容已按字节上限截断；未知部分不得视为已阅读。\n"
    else:
        content = raw
    return {
        "path": relative,
        "status": "confirmed" if not truncated else "needs_review",
        "bytes": len(encoded),
        "content": content,
    }


def project_memory_path(vault: Path, project: str) -> Path:
    """只把项目名映射到唯一项目主档案，不递归猜测项目边界。"""

    return safe_vault_path(vault, f"01-项目/{project}/项目记忆.md")


def render_brief(question: str | None, sources: list[dict[str, object]], generated_at: str) -> str:
    """生成适合单文件上传或跨 Agent 交接的上下文简报。"""

    included = [source for source in sources if source["status"] != "blocked"]
    lines = [
        "---",
        "type: ai-context-brief",
        f"managed_by: {MANAGED_BY}",
        f"generated_at: {generated_at}",
        f"source_count: {len(sources)}",
        "---",
        "",
        "# AI Context Brief",
        "",
        "> [!info] 这是经用户选择的上下文快照，不是完整仓库镜像，也不替代代码验证。",
        "",
    ]
    if question:
        lines.extend(["## 当前问题", "", question.strip(), ""])
    lines.extend(["## 已纳入来源", ""])
    for source in sources:
        suffix = f"（{source['status']}）"
        if source["status"] == "blocked":
            suffix += f"：{source['reason']}"
        lines.append(f"- `{source['path']}` {suffix}")
    lines.extend(["", "## 项目上下文", ""])
    for source in included:
        lines.extend([f"### {source['path']}", "", source["content"].rstrip(), ""])
    lines.extend(
        [
            "## 阅读边界",
            "",
            "- 本简报只包含显式批准的笔记；未列出的项目、代码、数据库和原始会话仍是未知。",
            "- `needs_review` 表示内容受大小上限影响，不代表 Agent 已经读完。",
            "- `blocked` 来源仅记录阻断原因，不包含敏感正文。",
            "- 进入实现阶段后，必须回到真实仓库和测试结果重新核验。",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    """定义上下文编译器的显式输入和默认预览行为。"""

    parser = argparse.ArgumentParser(description="从批准的 Obsidian 笔记生成 AI 上下文简报。")
    parser.add_argument("--vault", required=True, help="Obsidian Vault 根目录。")
    parser.add_argument("--project", action="append", default=[], help="项目目录名；只读取其项目记忆.md。可重复。")
    parser.add_argument("--note", action="append", default=[], help="Vault 内 Markdown 相对路径。可重复。")
    parser.add_argument("--question", help="本次讨论问题，写入简报入口。")
    parser.add_argument("--output-dir", required=True, help="简报输出目录。")
    parser.add_argument("--max-bytes", type=int, default=12000, help="每份来源正文的 UTF-8 字节上限，默认 12000。")
    parser.add_argument("--write", action="store_true", help="确认写入 ai_context.md 和 context-manifest.json。")
    return parser.parse_args()


def main() -> int:
    """编译批准来源，阻止隐式全库扫描和敏感正文泄漏。"""

    args = parse_args()
    if args.max_bytes <= 0:
        print("错误：--max-bytes 必须为正数。", file=sys.stderr)
        return 2
    if not args.project and not args.note:
        print("错误：至少指定一个 --project 或 --note；编译器不会自动扫描全库。", file=sys.stderr)
        return 2
    vault = Path(args.vault).expanduser().resolve()
    if not vault.is_dir():
        print(f"错误：Vault 不存在：{vault}", file=sys.stderr)
        return 2
    paths: list[Path] = []
    try:
        for project in args.project:
            paths.append(project_memory_path(vault, project))
        for note in args.note:
            paths.append(safe_vault_path(vault, note))
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    unique_paths = list(dict.fromkeys(paths))
    sources = [read_source(path, vault, args.max_bytes) for path in unique_paths]
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not args.write:
        print(f"预览：{len(sources)} 份批准来源，阻断 {sum(item['status'] == 'blocked' for item in sources)} 份；未写入。")
        return 0
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "managed_by": MANAGED_BY,
        "generated_at": generated_at,
        "question": args.question,
        "max_bytes_per_source": args.max_bytes,
        "sources": [{key: value for key, value in source.items() if key != "content"} for source in sources],
    }
    (output_dir / "ai_context.md").write_text(render_brief(args.question, sources, generated_at), encoding="utf-8", newline="\n")
    (output_dir / "context-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"已写入上下文简报：{output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
