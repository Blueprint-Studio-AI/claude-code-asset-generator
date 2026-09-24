import copy
import json
from pathlib import Path
import tempfile
import unittest

from sync_distribution import ROOT, render, sync


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.plugin = json.loads((ROOT / "plugin.json").read_text())
        self.mcp = json.loads((ROOT / "mcp.json").read_text())

    def test_single_edit_reaches_every_host(self):
        self.plugin.update(version="9.1.2", description="Updated shared description")
        self.mcp["mcpServers"]["asset-generator"]["url"] = "https://example.com/mcp"
        result = render(self.plugin, self.mcp)
        for file in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "server.json"]:
            self.assertEqual(result[file]["version"], "9.1.2")
            self.assertEqual(result[file]["description"], "Updated shared description")
        self.assertEqual(result[".mcp.json"]["mcpServers"]["asset-generator"], {
            "type": "http", "url": "https://example.com/mcp",
        })
        self.assertEqual(result["server.json"]["remotes"], [{
            "type": "streamable-http", "url": "https://example.com/mcp",
        }])

    def test_keeps_canonical_data_and_openai_presentation(self):
        original = copy.deepcopy(self.plugin)
        result = render(self.plugin, self.mcp)
        self.assertEqual(self.plugin, original)
        self.assertEqual(result[".codex-plugin/plugin.json"]["interface"],
                         self.plugin["extensions"]["com.openai"]["interface"])
        self.assertNotIn("extensions", result[".claude-plugin/plugin.json"])

    def test_drift_check_does_not_write_and_sync_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, data in [("plugin.json", self.plugin), ("mcp.json", self.mcp)]:
                (root / name).write_text(json.dumps(data))
            (root / "LICENSE").write_text((ROOT / "LICENSE").read_text())
            self.assertEqual(len(sync(root, check=True)), 4)
            self.assertFalse((root / "server.json").exists())
            sync(root)
            self.assertEqual(sync(root), [])
            path = root / ".claude-plugin/plugin.json"
            path.write_text("{}\n")
            self.assertEqual(sync(root, check=True), [".claude-plugin/plugin.json"])
            self.assertEqual(path.read_text(), "{}\n")

    def test_refuses_secret_bearing_or_unsupported_connections(self):
        for change in [{"headers": {"Authorization": "Bearer test"}},
                       {"type": "stdio"}, {"url": "http://example.com/mcp"},
                       {"url": "https://user:pass@example.com/mcp"},
                       {"url": "https://example.com/mcp?token=test"}]:
            with self.subTest(change=change):
                mcp = copy.deepcopy(self.mcp)
                mcp["mcpServers"]["asset-generator"].update(change)
                with self.assertRaises(ValueError):
                    render(self.plugin, mcp)

    def test_prevents_license_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "plugin.json").write_text(json.dumps(self.plugin))
            (root / "mcp.json").write_text(json.dumps(self.mcp))
            (root / "LICENSE").write_text("All rights reserved.\n")
            with self.assertRaises(ValueError):
                sync(root, check=True)

    def test_rejects_invalid_registry_metadata(self):
        for change in [{"version": "release"}, {"description": "x" * 101},
                       {"repository": "https://example.com/org/repo"}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                render({**self.plugin, **change}, self.mcp)


if __name__ == "__main__":
    unittest.main()
