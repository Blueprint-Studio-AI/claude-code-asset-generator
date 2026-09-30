import copy
import json
import re
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

    def test_codex_starters_fit_the_composer(self):
        # Codex shows at most 3 starters and truncates each after 128 characters.
        starters = self.plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        self.assertTrue(1 <= len(starters) <= 3)
        for starter in starters:
            with self.subTest(starter=starter):
                self.assertIsInstance(starter, str)
                self.assertTrue(0 < len(starter.strip()) <= 128)


SKILL_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def frontmatter(text):
    lines = text.split("\n")
    if lines[0] != "---" or "---" not in lines[1:]:
        return None
    end = lines.index("---", 1)
    return dict(line.split(": ", 1) for line in lines[1:end] if line.strip())


class SkillTests(unittest.TestCase):
    def test_every_skill_has_valid_frontmatter(self):
        skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertIn("start", [path.parent.name for path in skills])
        for path in skills:
            with self.subTest(skill=path.parent.name):
                meta = frontmatter(path.read_text())
                self.assertIsNotNone(meta)
                self.assertLessEqual(set(meta), SKILL_KEYS)
                self.assertEqual(meta["name"], path.parent.name)
                self.assertRegex(meta["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
                description = meta["description"].strip()
                self.assertTrue(0 < len(description) <= 1024)
                self.assertNotRegex(description, "[<>]")
                # One plain YAML scalar: ": " or " #" would break or truncate it.
                self.assertNotIn(": ", description)
                self.assertNotIn(" #", description)

    def test_skills_trigger_on_intent_not_the_brand_name(self):
        # Hosts load a skill from its description, and people ask for "an icon",
        # not "Blueprint". Each workflow names the requests it serves.
        expected = {
            "asset-generator": ["any image or visual asset", "icons", "logos", "illustrations",
                                "social graphics", "banners", "hero images", "product shots",
                                "mockups", "placeholders", "brand assets",
                                "default way to create images"],
            "start": ["what images or visual assets you can make", "first image"],
            "brand-manager": ["set up their brand", "colors", "fonts", "official logos",
                              "brand guidelines", "team access"],
            "style-gym": ["consistent look across many assets", "Style library"],
        }
        for name, phrases in expected.items():
            meta = frontmatter((ROOT / "skills" / name / "SKILL.md").read_text())
            for phrase in phrases:
                with self.subTest(skill=name, phrase=phrase):
                    self.assertIn(phrase, meta["description"])


class AgentTests(unittest.TestCase):
    def test_agents_describe_when_to_delegate(self):
        agents = sorted((ROOT / "agents").glob("*.md"))
        self.assertTrue(agents)
        for path in agents:
            lines = path.read_text().split("\n")
            self.assertEqual(lines[0], "---", path.name)
            header = lines[1:lines.index("---", 1)]
            fields = dict(line.split(": ", 1) for line in header if ": " in line)
            with self.subTest(agent=path.stem):
                self.assertEqual(fields["name"], path.stem)
                description = fields["description"].strip()
                self.assertTrue(0 < len(description) <= 1024)
                self.assertNotIn(": ", description)
                self.assertNotRegex(description, "[<>]")
        creator = (ROOT / "agents" / "asset-creator.md").read_text()
        self.assertIn("Use proactively when a task needs several assets", creator)

    def test_relative_links_resolve(self):
        docs = [ROOT / "README.md", *sorted((ROOT / "skills").rglob("*.md")),
                *sorted((ROOT / "agents").glob("*.md"))]
        for doc in docs:
            for target in LINK.findall(doc.read_text()):
                if "://" in target or target.startswith("mailto:"):
                    continue
                with self.subTest(doc=doc.relative_to(ROOT).as_posix(), target=target):
                    self.assertTrue((doc.parent / target).exists())


if __name__ == "__main__":
    unittest.main()
