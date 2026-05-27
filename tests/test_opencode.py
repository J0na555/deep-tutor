"""OpenCode integration tests."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestrator.opencode import (  # noqa: E402
    build_opencode_context,
    is_deep_tutor_root,
    resolve_deep_tutor_root,
)
from orchestrator.routing import route  # noqa: E402


class OpenCodeIntegration(unittest.TestCase):
    def test_is_deep_tutor_root(self):
        self.assertTrue(is_deep_tutor_root(REPO_ROOT))
        self.assertFalse(is_deep_tutor_root(REPO_ROOT / "orchestrator"))

    def test_resolve_from_repo_cwd(self):
        root = resolve_deep_tutor_root(REPO_ROOT)
        self.assertEqual(root, REPO_ROOT.resolve())

    def test_resolve_explicit(self):
        root = resolve_deep_tutor_root(REPO_ROOT, explicit=str(REPO_ROOT))
        self.assertEqual(root, REPO_ROOT.resolve())

    def test_resolve_missing_returns_none(self):
        root = resolve_deep_tutor_root(Path("/tmp"))
        if root is not None:
            self.assertTrue(is_deep_tutor_root(root))

    def test_build_context_defaults(self):
        payload = build_opencode_context(
            REPO_ROOT,
            cwd=REPO_ROOT,
            log_routing=False,
        )
        self.assertIn("text", payload)
        self.assertIn("=== Deep Tutor preamble (inspect) ===", payload["text"])
        self.assertEqual(payload["mode"], "mentor")
        self.assertEqual(payload["domain"], "generic")
        self.assertIsInstance(payload["sources"], list)

    def test_build_context_routes_message(self):
        payload = build_opencode_context(
            REPO_ROOT,
            cwd=REPO_ROOT,
            message="What is a deadlock?",
            log_routing=False,
        )
        self.assertEqual(payload["mode"], "concept")
        self.assertIsNotNone(payload.get("routing"))
        self.assertIn("prompts/modes/concept.md", payload["text"])

    def test_opencode_hook_cli(self):
        script = REPO_ROOT / "scripts" / "opencode-hook"
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "--cwd",
                str(REPO_ROOT),
                "--message",
                "Traceback (most recent call last):\nValueError",
                "--no-routing-log",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["mode"], "debug")

    def test_plugin_source_exists(self):
        plugin = REPO_ROOT / ".opencode" / "plugins" / "deep-tutor.js"
        self.assertTrue(plugin.is_file())
        content = plugin.read_text(encoding="utf-8")
        self.assertIn("experimental.chat.system.transform", content)
        self.assertIn("opencode-hook", content)


if __name__ == "__main__":
    unittest.main()
