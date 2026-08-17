#!/usr/bin/env python3
"""将用户批准的本地创作记录安全索引为 Obsidian 档案。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


MANAGED_BY = "starline-obsidian-archive"
MANAGED_DIR = "自动生成"
GROUP_DIR = "分组"
EXCLUDED_DIRS = {
    ".git",
    ".idea",
    ".obsidian",
    ".venv",
    ".vscode",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "venv",
}
CATEGORY_BY_EXTENSION = {
    ".ai": "可编辑作品",
    ".afdesign": "可编辑作品",
    ".aif": "音频",
    ".aiff": "音频",
    ".avif": "图片",
    ".blend": "三维作品",
    ".bmp": "图片",
    ".clip": "可编辑作品",
    ".clipstudio": "可编辑作品",
    ".flac": "音频",
    ".gif": "图片",
    ".heic": "图片",
    ".jpeg": "图片",
    ".jpg": "图片",
    ".kra": "可编辑作品",
    ".m4a": "音频",
    ".mkv": "视频",
    ".mov": "视频",
    ".mp3": "音频",
    ".mp4": "视频",
    ".oga": "音频",
    ".ogg": "音频",
    ".ora": "可编辑作品",
    ".png": "图片",
    ".psb": "可编辑作品",
    ".psd": "可编辑作品",
    ".sai": "可编辑作品",
    ".sai2": "可编辑作品",
    ".svg": "矢量图",
    ".tif": "图片",
    ".tiff": "图片",
    ".wav": "音频",
    ".webm": "视频",
    ".webp": "图片",
    ".xcf": "可编辑作品",
}
CONTEXT_EXTENSIONS = {
    ".csv",
    ".docx",
    ".json",
    ".md",
    ".pdf",
    ".pptx",
    ".txt",
    ".yaml",
    ".yml",
}


@dataclass
class Source:
    """保存一个经过用户批准的扫描来源。"""

    label: str
    path: Path


@dataclass
class Artifact:
    """保存一项可复跑的来源文件记录。"""

    identifier: str
    source: str
    relative_path: str
    category: str
    size_bytes: int
    modified_at: str
    file_uri: str
    group: str
    sha256: str | None = None
    duplicate_of: str | None = None


def parse_source(value: str) -> Source:
    """解析“显示名=目录”的命令行来源参数。"""

    if "=" not in value:
        raise argparse.ArgumentTypeError("--source 必须使用“显示名=目录”格式。")
    label, raw_path = value.split("=", 1)
    label = label.strip()
    raw_path = raw_path.strip()
    if not label or not raw_path:
        raise argparse.ArgumentTypeError("--source 的显示名和目录都不能为空。")
    path = Path(raw_path).expanduser().resolve()
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"来源目录不存在或不是目录：{path}")
    return Source(label=label, path=path)


def is_within(path: Path, parent: Path) -> bool:
    """判断路径是否位于父目录之内，防止越界写入或扫描。"""

    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def format_size(size_bytes: int) -> str:
    """将字节数转成适合索引表阅读的单位。"""

    units = ("B", "KiB", "MiB", "GiB", "TiB")
    amount = float(size_bytes)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.2f} {unit}"
        amount /= 1024
    return f"{size_bytes} B"


def escape_table_cell(value: str) -> str:
    """转义 Markdown 表格单元格，避免路径破坏生成表格。"""

    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def safe_filename(value: str) -> str:
    """生成跨平台可用且稳定的分组笔记文件名。"""

    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "-", value).strip(" .-")
    cleaned = re.sub(r"\s+", " ", cleaned) or "未命名分组"
    if len(cleaned) <= 96:
        return cleaned
    suffix = hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]
    return f"{cleaned[:84].rstrip()}-{suffix}"


def category_for(path: Path, include_context: bool) -> str | None:
    """按扩展名识别媒体或可选上下文文件类别。"""

    extension = path.suffix.lower()
    if extension in CATEGORY_BY_EXTENSION:
        return CATEGORY_BY_EXTENSION[extension]
    if include_context and extension in CONTEXT_EXTENSIONS:
        return "创作上下文"
    return None


def group_for(relative_path: Path, depth: int) -> str:
    """按来源内目录深度生成稳定的作品分组。"""

    parent_parts = relative_path.parent.parts[:depth]
    return "/".join(parent_parts) if parent_parts else "根目录"


def sha256_for(path: Path) -> str:
    """分块计算文件哈希，避免一次读入大型视频或原始素材。"""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def walk_source(source: Source, target: Path, include_context: bool, group_depth: int) -> tuple[list[Artifact], list[str]]:
    """只读遍历一个来源，跳过依赖目录和当前生成目标。"""

    artifacts: list[Artifact] = []
    warnings: list[str] = []
    for current, directory_names, filenames in os.walk(source.path, topdown=True, followlinks=False):
        current_path = Path(current).resolve()
        if is_within(current_path, target):
            directory_names[:] = []
            continue
        directory_names[:] = sorted(
            name
            for name in directory_names
            if name not in EXCLUDED_DIRS and not name.startswith(".") and not is_within(current_path / name, target)
        )
        for filename in sorted(filenames):
            path = current_path / filename
            category = category_for(path, include_context)
            if category is None:
                continue
            try:
                stat = path.stat()
                relative = path.relative_to(source.path)
                relative_text = relative.as_posix()
                artifacts.append(
                    Artifact(
                        identifier=f"{source.label}:{relative_text}",
                        source=source.label,
                        relative_path=relative_text,
                        category=category,
                        size_bytes=stat.st_size,
                        modified_at=datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(timespec="seconds"),
                        file_uri=path.as_uri(),
                        group=group_for(relative, group_depth),
                    )
                )
            except (OSError, ValueError) as exc:
                warnings.append(f"无法读取：{path}（{exc}）")
    return artifacts, warnings


def artifact_source_path(artifact: Artifact, sources: dict[str, Source]) -> Path:
    """从来源标签和相对路径重建本地路径，不依赖私有 URI 反解。"""

    return sources[artifact.source].path / Path(artifact.relative_path)


def mark_duplicates_from_sources(artifacts: list[Artifact], sources: dict[str, Source]) -> list[str]:
    """为兼容所有目标 Python，使用来源路径计算精确哈希。"""

    warnings: list[str] = []
    by_hash: dict[str, list[Artifact]] = defaultdict(list)
    for artifact in artifacts:
        try:
            artifact.sha256 = sha256_for(artifact_source_path(artifact, sources))
            by_hash[artifact.sha256].append(artifact)
        except OSError as exc:
            warnings.append(f"无法计算哈希：{artifact.source}/{artifact.relative_path}（{exc}）")
    for entries in by_hash.values():
        if len(entries) < 2:
            continue
        canonical = sorted(entries, key=lambda item: (item.source, item.relative_path))[0]
        for entry in entries:
            if entry is not canonical:
                entry.duplicate_of = canonical.identifier
    return warnings


def render_group_note(title: str, artifact_group: Iterable[Artifact], generated_at: str) -> str:
    """生成一个来源分组的 Obsidian 表格笔记。"""

    items = sorted(artifact_group, key=lambda item: (item.relative_path.casefold(), item.identifier))
    unique_items = [item for item in items if item.duplicate_of is None]
    duplicate_items = [item for item in items if item.duplicate_of is not None]
    total_size = sum(item.size_bytes for item in items)
    lines = [
        "---",
        "type: artifact-group",
        f"managed_by: {MANAGED_BY}",
        f"generated_at: {generated_at}",
        f"source: {json.dumps(items[0].source, ensure_ascii=False)}",
        f"group: {json.dumps(items[0].group, ensure_ascii=False)}",
        f"raw_file_count: {len(items)}",
        f"unique_file_count: {len(unique_items)}",
        "---",
        "",
        f"# {title}",
        "",
        f"> [!info] 来源保留在原处\n> 本组共发现 {len(items)} 项、{format_size(total_size)}；索引只记录链接和元数据。",
        "",
        "| 文件 | 类别 | 修改时间 | 大小 | 本地打开 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in unique_items:
        lines.append(
            "| {name} | {category} | {modified} | {size} | [打开]({uri}) |".format(
                name=escape_table_cell(item.relative_path),
                category=item.category,
                modified=item.modified_at,
                size=format_size(item.size_bytes),
                uri=item.file_uri,
            )
        )
    if duplicate_items:
        lines.extend(
            [
                "",
                "## 精确重复项",
                "",
                "以下文件与本组或其他分组的代表文件字节完全相同，完整路径仍保留在 `资源清单.json`：",
                "",
            ]
        )
        for item in duplicate_items:
            lines.append(f"- `{item.relative_path}` → `{item.duplicate_of}`")
    return "\n".join(lines) + "\n"


def render_overview(
    title: str,
    target_relative: Path,
    sources: list[Source],
    artifacts: list[Artifact],
    group_notes: dict[tuple[str, str], str],
    generated_at: str,
    include_context: bool,
    hashed: bool,
    warnings: list[str],
) -> str:
    """生成所有来源与分组的总览笔记。"""

    unique_count = sum(1 for item in artifacts if item.duplicate_of is None)
    duplicate_count = len(artifacts) - unique_count
    total_size = sum(item.size_bytes for item in artifacts)
    lines = [
        "---",
        "type: artifact-index",
        f"managed_by: {MANAGED_BY}",
        f"generated_at: {generated_at}",
        f"raw_file_count: {len(artifacts)}",
        f"unique_file_count: {unique_count}",
        "---",
        "",
        f"# {title}：资源总览",
        "",
        "> [!warning] 自动生成区\n> 刷新会覆盖本目录内由同步器管理的文件。请把评论、决策和创作过程写入上级的 `项目记忆.md` 或其他手写笔记。",
        "",
        f"- 生成时间：{generated_at}",
        f"- 发现文件：{len(artifacts)} 项，合计 {format_size(total_size)}",
        f"- 代表文件：{unique_count} 项；精确重复：{duplicate_count} 项" if hashed else "- 未启用内容哈希；未声明精确重复项。",
        f"- 创作上下文：{'已包含' if include_context else '未包含'}",
        "- 原始文件：未复制、未移动、未改名。",
        "",
        "## 来源",
        "",
        "| 来源 | 本地根目录 | 文件数 |",
        "| --- | --- | ---: |",
    ]
    for source in sources:
        source_count = sum(1 for item in artifacts if item.source == source.label)
        lines.append(f"| {escape_table_cell(source.label)} | `{escape_table_cell(str(source.path))}` | {source_count} |")
    lines.extend(["", "## 分组", ""])
    for (source, group), note_name in sorted(group_notes.items(), key=lambda item: (item[0][0].casefold(), item[0][1].casefold())):
        group_count = sum(1 for item in artifacts if item.source == source and item.group == group)
        note_path = target_relative / MANAGED_DIR / GROUP_DIR / f"{note_name}.md"
        lines.append(f"- [[{note_path.with_suffix('').as_posix()}|{source} / {group}]]（{group_count} 项）")
    if warnings:
        lines.extend(["", "## 需人工确认", ""])
        lines.extend(f"- {escape_table_cell(warning)}" for warning in warnings)
    return "\n".join(lines) + "\n"


def build_manifest(
    target_relative: Path,
    sources: list[Source],
    artifacts: list[Artifact],
    generated_at: str,
    include_context: bool,
    hashed: bool,
    warnings: list[str],
) -> dict[str, object]:
    """构建可供后续同步或审计的完整 JSON 清单。"""

    return {
        "schema_version": 1,
        "managed_by": MANAGED_BY,
        "generated_at": generated_at,
        "target": target_relative.as_posix(),
        "scan_options": {
            "include_context": include_context,
            "hash_content": hashed,
            "excluded_directories": sorted(EXCLUDED_DIRS),
        },
        "sources": [{"label": source.label, "path": str(source.path)} for source in sources],
        "artifacts": [asdict(item) for item in sorted(artifacts, key=lambda item: (item.source, item.relative_path.casefold()))],
        "warnings": warnings,
    }


def write_text(path: Path, content: str) -> None:
    """以 UTF-8 写入受管文件，并确保父目录存在。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def prune_stale_groups(group_dir: Path, expected: set[Path]) -> list[Path]:
    """仅删除带受管标记且不再生成的旧分组笔记。"""

    removed: list[Path] = []
    if not group_dir.is_dir():
        return removed
    for path in group_dir.glob("*.md"):
        if path in expected:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if f"managed_by: {MANAGED_BY}" not in content:
            continue
        path.unlink()
        removed.append(path)
    return removed


def parse_args() -> argparse.Namespace:
    """定义命令行接口，并明确默认只预览不写入。"""

    parser = argparse.ArgumentParser(description="将用户批准的本地作品和项目记录索引到 Obsidian。")
    parser.add_argument("--vault", required=True, help="Obsidian vault 的根目录。")
    parser.add_argument("--target", required=True, help="Vault 内的相对输出目录，例如 01-项目/作品档案。")
    parser.add_argument("--source", action="append", type=parse_source, required=True, help="显示名=来源目录；可重复指定。")
    parser.add_argument("--title", help="总览显示标题；默认使用目标目录名称。")
    parser.add_argument("--group-depth", type=int, default=1, choices=range(0, 5), metavar="0-4", help="按来源内目录分组的深度，默认 1。")
    parser.add_argument("--include-context", action="store_true", help="同时收录 Markdown、PDF、文本、JSON 等创作上下文。")
    parser.add_argument("--hash-content", action="store_true", help="计算 SHA-256，识别字节完全相同的文件。")
    parser.add_argument("--write", action="store_true", help="确认写入 vault；缺省仅输出预览。")
    parser.add_argument("--prune", action="store_true", help="写入时删除不再生成且带受管标记的旧分组笔记。")
    return parser.parse_args()


def main() -> int:
    """执行预览或受限写入，并输出可审查的同步摘要。"""

    args = parse_args()
    vault = Path(args.vault).expanduser().resolve()
    if not vault.is_dir():
        print(f"错误：Vault 目录不存在：{vault}", file=sys.stderr)
        return 2
    target_relative = Path(args.target)
    if target_relative.is_absolute() or ".." in target_relative.parts:
        print("错误：--target 必须是 vault 内不含 .. 的相对目录。", file=sys.stderr)
        return 2
    target = (vault / target_relative).resolve()
    if not is_within(target, vault):
        print("错误：目标目录越出 Vault 边界。", file=sys.stderr)
        return 2
    if args.prune and not args.write:
        print("错误：--prune 必须与 --write 一起使用。", file=sys.stderr)
        return 2

    source_map = {source.label: source for source in args.source}
    if len(source_map) != len(args.source):
        print("错误：来源显示名必须唯一。", file=sys.stderr)
        return 2

    artifacts: list[Artifact] = []
    warnings: list[str] = []
    for source in args.source:
        found, source_warnings = walk_source(source, target, args.include_context, args.group_depth)
        artifacts.extend(found)
        warnings.extend(source_warnings)
    artifacts.sort(key=lambda item: (item.source.casefold(), item.relative_path.casefold()))
    if args.hash_content:
        warnings.extend(mark_duplicates_from_sources(artifacts, source_map))

    title = args.title or target_relative.name
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    grouped: dict[tuple[str, str], list[Artifact]] = defaultdict(list)
    for artifact in artifacts:
        grouped[(artifact.source, artifact.group)].append(artifact)
    group_names: dict[tuple[str, str], str] = {}
    used_names: set[str] = set()
    for key in sorted(grouped, key=lambda item: (item[0].casefold(), item[1].casefold())):
        base_name = safe_filename(f"{key[0]} - {key[1]}")
        note_name = base_name
        if note_name.casefold() in used_names:
            suffix = hashlib.sha256(f"{key[0]}\0{key[1]}".encode("utf-8")).hexdigest()[:10]
            note_name = f"{base_name[:84].rstrip()}-{suffix}"
        used_names.add(note_name.casefold())
        group_names[key] = note_name
    manifest = build_manifest(target_relative, args.source, artifacts, generated_at, args.include_context, args.hash_content, warnings)

    unique_count = sum(1 for item in artifacts if item.duplicate_of is None)
    print(f"预览：来源 {len(args.source)} 个，发现文件 {len(artifacts)} 项，代表文件 {unique_count} 项。")
    print(f"总大小：{format_size(sum(item.size_bytes for item in artifacts))}；分组：{len(grouped)} 个。")
    for source in args.source:
        print(f"- {source.label}: {sum(1 for item in artifacts if item.source == source.label)} 项，{source.path}")
    if warnings:
        print(f"警告：{len(warnings)} 项；请查看生成的资源总览中的“需人工确认”。")
    if not args.write:
        print("未写入：这是预览。确认范围后加 --write。")
        return 0

    managed_root = target / MANAGED_DIR
    group_dir = managed_root / GROUP_DIR
    expected_group_paths: set[Path] = set()
    for key, items in grouped.items():
        note_path = group_dir / f"{group_names[key]}.md"
        expected_group_paths.add(note_path)
        write_text(note_path, render_group_note(f"{key[0]} / {key[1]}", items, generated_at))
    overview = render_overview(title, target_relative, args.source, artifacts, group_names, generated_at, args.include_context, args.hash_content, warnings)
    write_text(managed_root / "资源总览.md", overview)
    write_text(managed_root / "资源清单.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    removed = prune_stale_groups(group_dir, expected_group_paths) if args.prune else []
    print(f"已写入：{managed_root}")
    if removed:
        print(f"已清理 {len(removed)} 份带受管标记的旧分组笔记。")
    print("原始来源文件未被修改。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
