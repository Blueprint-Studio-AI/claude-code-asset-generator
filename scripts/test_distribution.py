import copy
import hashlib
import json
import re
from pathlib import Path
import tempfile
import unittest

from sync_distribution import ROOT, VERSION_HEADER, VERSIONED_SKILLS, render, sync

# Claude Code 2.10.1 and earlier: the exact .mcp.json from before 2.10.0, whose sign-ins
# Claude Code users still have.
PRE_2_10_CLAUDE_CODE_MCP = """{
  "mcpServers": {
    "asset-generator": {
      "type": "http",
      "url": "https://tools.blueprintstudio.ai/api/mcp"
    }
  }
}
"""


def claude_code_sign_in_key(server):
    """The hash in Claude Code's sign-in key for a server config: "<name>|<this>"."""
    config = {"type": server.get("type"), "url": server.get("url"), "headers": server.get("headers") or {}}
    return hashlib.sha256(json.dumps(config, separators=(",", ":")).encode()).hexdigest()[:16]


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.plugin = json.loads((ROOT / "plugin.json").read_text())
        self.mcp = json.loads((ROOT / "mcp.json").read_text())

    def test_single_edit_reaches_every_host(self):
        self.plugin.update(version="9.1.2", description="Updated shared description")
        self.plugin["extensions"]["io.modelcontextprotocol.registry"]["description"] = "Registry line"
        self.mcp["mcpServers"]["asset-generator"]["url"] = "https://example.com/mcp"
        result = render(self.plugin, self.mcp)
        for file in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "server.json"]:
            self.assertEqual(result[file]["version"], "9.1.2")
        for file in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]:
            self.assertEqual(result[file]["description"], "Updated shared description")
        self.assertEqual(result["server.json"]["description"], "Registry line")
        self.assertEqual(result[".mcp.json"]["mcpServers"]["asset-generator"], {
            "type": "http", "url": "https://example.com/mcp",
        })
        self.assertEqual(result["mcp.json"]["mcpServers"]["asset-generator"], {
            "type": "streamable-http", "url": "https://example.com/mcp",
            "headers": {"X-Blueprint-Plugin": "blueprint-studio/9.1.2"},
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

    def test_claude_manifest_carries_the_one_privacy_policy(self):
        self.plugin["extensions"]["com.openai"]["interface"]["privacyPolicyURL"] = "https://example.com/privacy"
        result = render(self.plugin, self.mcp)
        self.assertEqual(result[".claude-plugin/plugin.json"]["privacyPolicyUrl"], "https://example.com/privacy")
        self.assertEqual(result[".claude-plugin/plugin.json"]["termsOfServiceUrl"],
                         self.plugin["extensions"]["com.openai"]["interface"]["termsOfServiceURL"])
        self.assertEqual(result[".claude-plugin/plugin.json"]["supportUrl"],
                         self.plugin["extensions"]["com.anthropic.claude"]["supportUrl"])
        self.assertNotIn("com.anthropic.claude", json.dumps(result[".codex-plugin/plugin.json"]))

    def test_drift_check_does_not_write_and_sync_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, data in [("plugin.json", self.plugin), ("mcp.json", self.mcp)]:
                (root / name).write_text(json.dumps(data))
            (root / "LICENSE").write_text((ROOT / "LICENSE").read_text())
            for skill in VERSIONED_SKILLS:
                (root / skill).parent.mkdir(parents=True)
                (root / skill).write_text((ROOT / skill).read_text())
            # mcp.json too: its version header is generated from plugin.json.
            self.assertEqual(len(sync(root, check=True)), 5)
            self.assertFalse((root / "server.json").exists())
            sync(root)
            self.assertEqual(sync(root), [])
            path = root / ".claude-plugin/plugin.json"
            path.write_text("{}\n")
            self.assertEqual(sync(root, check=True), [".claude-plugin/plugin.json"])
            self.assertEqual(path.read_text(), "{}\n")

    def test_refuses_secret_bearing_or_unsupported_connections(self):
        for change in [{"headers": {"Authorization": "Bearer test"}},
                       {"headers": {"authorization": "Bearer test"}},
                       {"headers": {"Proxy-Authorization": "Basic dGVzdA=="}},
                       {"headers": {"X-API-Key": "test"}},
                       {"headers": {"X-Api_Key": "test"}},
                       {"headers": {"Cookie": "session=test"}},
                       {"headers": {"X-Auth-Token": "test"}},
                       {"headers": {"X-Client-Secret": "test"}},
                       {"headers": {"Key": "test"}},
                       # An unknown name, even a harmless-looking one, is refused too.
                       {"headers": {"X-Blueprint-Plugin": "blueprint-studio/1.0.0", "X-Extra": "1"}},
                       {"headers": "X-Blueprint-Plugin: blueprint-studio/1.0.0"},
                       {"headersHelper": "./print-headers.sh"},
                       {"type": "stdio"}, {"url": "http://example.com/mcp"},
                       {"url": "https://user:pass@example.com/mcp"},
                       {"url": "https://example.com/mcp?token=test"}]:
            with self.subTest(change=change):
                mcp = copy.deepcopy(self.mcp)
                mcp["mcpServers"]["asset-generator"].update(change)
                with self.assertRaises(ValueError):
                    render(self.plugin, mcp)

    def test_version_header_is_generated_from_plugin_json(self):
        # Codex and other Agent Plugins hosts send it on every request, so the service can say
        # when a newer plugin is out. Codex keys sign-ins on server name and URL, not headers.
        self.assertEqual(VERSION_HEADER, "X-Blueprint-Plugin")
        for authored in [None, {}, {"X-Blueprint-Plugin": "blueprint-studio/0.0.1"},
                         {"x-blueprint-plugin": "anything else"}]:
            with self.subTest(authored=authored):
                mcp = copy.deepcopy(self.mcp)
                server = mcp["mcpServers"]["asset-generator"]
                server.pop("headers", None)
                if authored is not None:
                    server["headers"] = authored
                result = render({**self.plugin, "version": "3.4.5"}, mcp)
                expected = {"X-Blueprint-Plugin": "blueprint-studio/3.4.5"}
                self.assertEqual(result["mcp.json"]["mcpServers"]["asset-generator"]["headers"], expected)
                # Never in Claude Code's connection, whatever mcp.json authors.
                self.assertNotIn("headers", result[".mcp.json"]["mcpServers"]["asset-generator"])
                # The Registry lists the server for every client, not just this plugin.
                self.assertNotIn("headers", json.dumps(result["server.json"]))

    def test_committed_connection_files_carry_the_current_version(self):
        version = self.plugin["version"]
        server = json.loads((ROOT / "mcp.json").read_text())["mcpServers"]["asset-generator"]
        self.assertEqual(server["headers"], {"X-Blueprint-Plugin": f"blueprint-studio/{version}"})
        self.assertEqual(set(server), {"type", "url", "headers"})
        self.assertEqual(json.loads((ROOT / "mcp.json").read_text())["$schema"],
                         "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json")

    def test_claude_code_connection_never_changes_between_releases(self):
        # Claude Code keeps each MCP sign-in under "<server name>|" plus the first 16 hex
        # characters of sha256(JSON of the server config's type, url and headers). Anything in
        # .mcp.json that changes per release (a version, a header carrying one) is a new key,
        # so every Claude Code user has to sign in again after updating: 2.10.0 and 2.10.1
        # sent X-Blueprint-Plugin: blueprint-studio/<version> here and did exactly that.
        releases = [render({**self.plugin, "version": version}, self.mcp)[".mcp.json"]
                    for version in ["2.10.2", "2.10.3", "3.0.0-beta.1", "10.0.0"]]
        self.assertTrue(all(release == releases[0] for release in releases))
        committed = (ROOT / ".mcp.json").read_text()
        self.assertNotIn(self.plugin["version"], committed)
        self.assertNotRegex(committed, r"\d+\.\d+\.\d+")
        self.assertNotIn(VERSION_HEADER.lower(), committed.lower())
        for server in json.loads(committed)["mcpServers"].values():
            self.assertEqual(set(server), {"type", "url"})
        # Byte for byte the pre-2.10 file, so updating finds the sign-in made before 2.10.0
        # (Claude Code's key plugin:blueprint-studio:asset-generator|de48b78f50b233db) again.
        self.assertEqual(committed, PRE_2_10_CLAUDE_CODE_MCP)
        server = json.loads(committed)["mcpServers"]["asset-generator"]
        self.assertEqual(claude_code_sign_in_key(server), "de48b78f50b233db")
        # The 2.10.0 config's key, as Claude Code stored it, for the record.
        self.assertEqual(claude_code_sign_in_key(
            {**server, "headers": {"X-Blueprint-Plugin": "blueprint-studio/2.10.0"}}), "2a5622c5373a95c2")

    def test_skills_ask_agents_to_pass_the_current_version(self):
        # Without a header, a Claude Code connection says its release to get_workspace_context
        # as pluginVersion, from this sentence in the skills agents load first.
        version = self.plugin["version"]
        for skill in VERSIONED_SKILLS:
            with self.subTest(skill=skill):
                text = (ROOT / skill).read_text()
                self.assertEqual(text.count("`pluginVersion: "), 1)
                self.assertIn(f'Pass `pluginVersion: "{version}"` (this plugin\'s release)', text)
                self.assertIn("get_workspace_context", text)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plugin = {**self.plugin, "version": "9.8.7"}
            for name, data in [("plugin.json", plugin), ("mcp.json", self.mcp)]:
                (root / name).write_text(json.dumps(data))
            (root / "LICENSE").write_text((ROOT / "LICENSE").read_text())
            for skill in VERSIONED_SKILLS:
                (root / skill).parent.mkdir(parents=True)
                (root / skill).write_text((ROOT / skill).read_text())
            self.assertLessEqual(set(VERSIONED_SKILLS), set(sync(root, check=True)))
            sync(root)
            for skill in VERSIONED_SKILLS:
                self.assertIn('`pluginVersion: "9.8.7"`', (root / skill).read_text())
            self.assertEqual(sync(root, check=True), [])
            # The sentence must be there, once.
            (root / VERSIONED_SKILLS[0]).write_text("No version here.\n")
            with self.assertRaises(ValueError):
                sync(root, check=True)

    def test_prevents_license_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "plugin.json").write_text(json.dumps(self.plugin))
            (root / "mcp.json").write_text(json.dumps(self.mcp))
            (root / "LICENSE").write_text("All rights reserved.\n")
            with self.assertRaises(ValueError):
                sync(root, check=True)

    def test_rejects_invalid_registry_metadata(self):
        for change in [{"version": "release"}, {"description": "x" * 251},
                       {"repository": "https://example.com/org/repo"}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                render({**self.plugin, **change}, self.mcp)
        long_line = copy.deepcopy(self.plugin)
        long_line["extensions"]["io.modelcontextprotocol.registry"]["description"] = "x" * 101
        with self.assertRaises(ValueError):
            render(long_line, self.mcp)

    def test_registry_keeps_its_own_one_liner(self):
        # The plugin description says who we are; the Registry's 100 characters don't fit it.
        result = render(self.plugin, self.mcp)
        registry = self.plugin["extensions"]["io.modelcontextprotocol.registry"]["description"]
        self.assertEqual(result["server.json"]["description"], registry)
        self.assertLessEqual(len(registry), 100)
        self.assertNotIn("io.modelcontextprotocol.registry", json.dumps(result[".claude-plugin/plugin.json"]))
        self.assertIn("design and development studio", self.plugin["description"])
        # Without the extension, the Registry falls back to the shared description.
        bare = copy.deepcopy(self.plugin)
        del bare["extensions"]["io.modelcontextprotocol.registry"]
        bare["description"] = "Short shared description"
        self.assertEqual(render(bare, self.mcp)["server.json"]["description"], "Short shared description")

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
            "start": ["first run", "what Blueprint Studio can do", "first image"],
            "asset-generator": ["icon", "illustration", "banner", "social post", "hero",
                                "mockup", "placeholder", "edit or reuse a saved image"],
            "asset-sets": ["icon set", "several sizes", "one for each", "several images in one look"],
            "brand-setup": ["set up their brand", "website", "colors, fonts"],
            "official-logos": ["their logo", "logo file", "primary", "dark backgrounds"],
            "styles": ["consistent look", "Style library", "compare Style candidates"],
        }
        self.assertEqual(set(expected), {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")})
        for name, phrases in expected.items():
            meta = frontmatter((ROOT / "skills" / name / "SKILL.md").read_text())
            for phrase in phrases:
                with self.subTest(skill=name, phrase=phrase):
                    self.assertIn(phrase, meta["description"])

    def test_descriptions_fit_the_always_on_budget(self):
        # Every description sits in every session's system prompt (Codex budgets
        # about 8,000 characters for all of a user's skills): under 400 each, 5,000 in all.
        descriptions = [frontmatter(path.read_text())["description"]
                        for path in (ROOT / "skills").glob("*/SKILL.md")]
        for description in descriptions:
            with self.subTest(description=description[:40]):
                self.assertLessEqual(len(description), 400)
        self.assertLessEqual(sum(map(len, descriptions)), 5000)

    def test_skills_never_steer_tool_choice(self):
        # Anthropic's and OpenAI's directories forbid steering the model toward our
        # tools. Canva's fair line is allowed: don't silently swap tools when the
        # user names us.
        for path in sorted((ROOT / "skills").rglob("*.md")):
            text = path.read_text()
            with self.subTest(file=path.relative_to(ROOT).as_posix()):
                self.assertNotRegex(text, r"(?i)prefer (it|us|blueprint)[^.]*over|default way to create|other image tools|instead of (any|other) (image )?tools?")

    def test_skills_are_built_on_one_rule(self):
        # Flora's shape: one rule, measured numbers, steps, known failures, limits.
        for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            text = path.read_text()
            with self.subTest(skill=path.parent.name):
                self.assertEqual(text.count("**The rule: "), 1)
                for heading in ["## Numbers", "## Known failures", "## Limits"]:
                    self.assertIn(f"\n{heading}\n", text)
                self.assertLess(len(text.split("\n")), 150)

    def test_skills_stand_alone_and_name_tools_bare(self):
        # A host can install one skill alone, so no links into another skill's folder.
        # Tool names are bare: the host prefix (mcp__...) differs per host.
        for path in sorted((ROOT / "skills").rglob("*.md")):
            text = path.read_text()
            skill = path.relative_to(ROOT / "skills").parts[0]
            with self.subTest(file=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("mcp__", text)
                self.assertNotIn(chr(0x2014), text)
                for target in LINK.findall(text):
                    if "://" in target:
                        continue
                    resolved = (path.parent / target).resolve()
                    self.assertTrue(resolved.is_relative_to((ROOT / "skills" / skill).resolve()), target)

    def test_each_skill_has_try_it_prompts(self):
        # Positive, indirect and negative prompts, with the behaviour to expect.
        for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                evals = json.loads((path.parent / "evals" / "evals.json").read_text())
                self.assertEqual(evals["skill_name"], path.parent.name)
                self.assertEqual({item["kind"] for item in evals["evals"]}, {"positive", "indirect", "negative"})
                for item in evals["evals"]:
                    self.assertTrue(item["prompt"].strip() and item["expected_output"].strip())


class PackageTests(unittest.TestCase):
    def test_no_agents(self):
        # Agents load only in Claude Code; their content lives in skill references.
        self.assertFalse((ROOT / "agents").exists())

    def test_relative_links_resolve(self):
        docs = [ROOT / "README.md", *sorted((ROOT / "skills").rglob("*.md"))]
        for doc in docs:
            for target in LINK.findall(doc.read_text()):
                if "://" in target or target.startswith("mailto:"):
                    continue
                with self.subTest(doc=doc.relative_to(ROOT).as_posix(), target=target):
                    self.assertTrue((doc.parent / target).exists())


if __name__ == "__main__":
    unittest.main()
