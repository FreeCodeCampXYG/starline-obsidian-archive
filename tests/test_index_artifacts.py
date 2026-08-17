"""验证本地创作档案索引器的核心非破坏行为。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE_ROOT / "scripts" / "index_artifacts.py"


class IndexArtifactsTests(unittest.TestCase):
    """覆盖受管输出、上下文收录和精确去重。"""

    def test_writes_only_vault_target_and_marks_exact_duplicates(self) -> None:
        """写入索引时不得改变来源文件，并应标记完全相同的副本。"""

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            vault = root / "vault"
            source = root / "source"
            nested = source / "video"
            vault.mkdir()
            nested.mkdir(parents=True)
            first = source / "cover.png"
            duplicate = nested / "cover-copy.png"
            context = nested / "scene.md"
            first.write_bytes(b"same-image-bytes")
            duplicate.write_bytes(b"same-image-bytes")
            context.write_text("# 分镜\n", encoding="utf-8")
            original_snapshot = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in (first, duplicate, context)}

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--vault",
                    str(vault),
                    "--target",
                    "01-Projects/Art Archive",
                    "--source",
                    f"作品={source}",
                    "--include-context",
                    "--hash-content",
                    "--write",
                ],
                cwd=PACKAGE_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            manifest_path = vault / "01-Projects" / "Art Archive" / "自动生成" / "资源清单.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["artifacts"]), 3)
            self.assertEqual(sum(item["duplicate_of"] is None for item in manifest["artifacts"]), 2)
            for path, snapshot in original_snapshot.items():
                self.assertEqual(path.read_bytes(), snapshot[0])
                self.assertEqual(path.stat().st_mtime_ns, snapshot[1])
            generated_groups = list((manifest_path.parent / "分组").glob("*.md"))
            self.assertEqual(len(generated_groups), 2)

    def test_rejects_target_outside_vault(self) -> None:
        """目标目录含父级跳转时必须拒绝，避免越界写入。"""

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            vault = root / "vault"
            source = root / "source"
            vault.mkdir()
            source.mkdir()
            (source / "cover.png").write_bytes(b"image")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--vault",
                    str(vault),
                    "--target",
                    "../outside",
                    "--source",
                    f"作品={source}",
                ],
                cwd=PACKAGE_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("--target", completed.stderr)
