"""验证 Vault 审计和上下文简报的边界行为。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
AUDIT = PACKAGE_ROOT / "scripts" / "audit_vault.py"
BRIEF = PACKAGE_ROOT / "scripts" / "build_context_brief.py"


class MemoryToolTests(unittest.TestCase):
    """覆盖只读审计、显式来源和敏感内容阻断。"""

    def test_audit_reports_unnamed_and_missing_project_memory(self) -> None:
        """审计只能报告结构缺口，不能偷偷替用户命名或补档案。"""

        with tempfile.TemporaryDirectory() as temporary:
            vault = Path(temporary) / "vault"
            (vault / "01-项目" / "Demo").mkdir(parents=True)
            (vault / "未命名.base").write_text("views:\n", encoding="utf-8")
            (vault / "01-项目" / "项目总览.md").write_text("# 项目总览\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(AUDIT), "--vault", str(vault), "--json"],
                cwd=PACKAGE_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(completed.stdout)
            kinds = {item["kind"] for item in report["findings_detail"]}
            self.assertIn("unnamed", kinds)
            self.assertIn("missing_project_memory", kinds)
            self.assertFalse((vault / "01-项目" / "Demo" / "项目记忆.md").exists())

    def test_context_brief_requires_explicit_sources_and_blocks_secret(self) -> None:
        """简报只能读取批准笔记，并且不把疑似凭据写入输出。"""

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            vault = root / "vault"
            output = root / "brief"
            project = vault / "01-项目" / "Demo"
            project.mkdir(parents=True)
            (project / "项目记忆.md").write_text("---\ntype: project-memory\n---\n\n# Demo\n\n状态：进行中\n", encoding="utf-8")
            secret = vault / "secret.md"
            blocked_token = "ghp_" + ("1" * 32)
            secret.write_text(f"token={blocked_token}\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(BRIEF),
                    "--vault",
                    str(vault),
                    "--project",
                    "Demo",
                    "--note",
                    "secret.md",
                    "--output-dir",
                    str(output),
                    "--write",
                ],
                cwd=PACKAGE_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            brief = (output / "ai_context.md").read_text(encoding="utf-8")
            manifest = json.loads((output / "context-manifest.json").read_text(encoding="utf-8"))
            self.assertIn("Demo", brief)
            self.assertNotIn(blocked_token, brief)
            self.assertEqual(manifest["sources"][1]["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
