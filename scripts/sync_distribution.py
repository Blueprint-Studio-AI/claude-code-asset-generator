#!/usr/bin/env python3
"""Generate host compatibility files from the portable plugin. No network/dependencies."""

import argparse
import copy
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
IDENTITY_FIELDS = (
    "name", "version", "description", "author", "homepage", "repository", "license", "keywords"
)
# The MCP Registry caps descriptions at 100 characters; plugin manifests can say more.
REGISTRY_NAMESPACE = "io.modelcontextprotocol.registry"
# The one header a connection may carry: this package's name and release (for example
# blueprint-studio/2.10.0), so the hosted service can tell a user when a newer plugin is out.
# It is generated from plugin.json, never authored, and is not a credential. Only mcp.json
# (current Codex and other Agent Plugins hosts) sends it: Codex keys each sign-in on the
# server's name and URL alone (codex-rs/rmcp-client compute_store_key), so a header that
# changes per release keeps users signed in there. Claude Code's .mcp.json never carries it;
# see claude_code_connection.
VERSION_HEADER = "X-Blueprint-Plugin"
# The skills agents load first ask them to pass this release to get_workspace_context, which is
# how a Claude Code connection, with no header, says which release it runs. The version in
# that one sentence is generated from plugin.json too.
VERSIONED_SKILLS = ("skills/start/SKILL.md", "skills/asset-generator/SKILL.md")
SKILL_VERSION = re.compile(r'`pluginVersion: "[^"`]*"`')
# Header names that carry credentials. They are refused by name, before the allowlist, so a
# token can never reach a public package even under a new header name.
CREDENTIAL_HEADER = re.compile(
    r"(?i)auth|cookie|token|secret|passw|credential|session|bearer|signature|api[-_]?key|(^|[-_])key($|[-_])"
)


def version_headers(server, name, version):
    """The generated version header, after refusing anything credential-like or unknown."""
    headers = server.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("MCP headers must be an object")
    for header in headers:
        if not isinstance(header, str) or CREDENTIAL_HEADER.search(header):
            raise ValueError(f"MCP headers must not carry credentials: {header!r}")
        if header.lower() != VERSION_HEADER.lower():
            raise ValueError(f"The only MCP header is the generated {VERSION_HEADER} version header")
    return {VERSION_HEADER: f"{name}/{version}"}


def claude_code_connection(server):
    """Claude Code's connection: type and URL only, the same in every release.

    Claude Code stores each MCP sign-in under "<server name>|" plus the first 16 hex characters
    of sha256(JSON of the server's type, url and headers). Anything here that changes per
    release is a new key, so every Claude Code user is signed out by the update: 2.10.0 and
    2.10.1 sent the version header and did exactly that. This stays byte-for-byte the pre-2.10
    shape, so 2.10.2 and later find the sign-in made before 2.10.0 again and never lose it.
    """
    return {"type": "http", "url": server["url"]}


def versioned_skill(text, version, relative="skill"):
    """A skill's text with its one pluginVersion sentence set to this release."""
    found = SKILL_VERSION.findall(text)
    if len(found) != 1:
        raise ValueError(f'{relative} must say `pluginVersion: "<version>"` exactly once')
    return SKILL_VERSION.sub(f'`pluginVersion: "{version}"`', text)


def render(plugin, mcp):
    """Project portable data without mutating it or duplicating authored content."""
    name = plugin["name"]
    version = plugin["version"]
    if not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", name):
        raise ValueError("Invalid plugin name")
    if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", version):
        raise ValueError("Invalid release version")
    repo = urlsplit(plugin["repository"])
    repo_parts = repo.path.strip("/").split("/")
    if repo.scheme != "https" or repo.netloc != "github.com" or len(repo_parts) != 2 or repo.query or repo.fragment:
        raise ValueError("Registry publication requires a canonical GitHub repository URL")
    description = plugin["description"]
    if not isinstance(description, str) or not 1 <= len(description) <= 250:
        raise ValueError("Plugin description must be 1-250 characters")
    registry_description = plugin.get("extensions", {}).get(REGISTRY_NAMESPACE, {}).get(
        "description", description
    )
    if not isinstance(registry_description, str) or not 1 <= len(registry_description) <= 100:
        raise ValueError("Registry description must fit the MCP Registry's 100-character limit")
    common = {key: copy.deepcopy(plugin[key]) for key in IDENTITY_FIELDS if key in plugin}
    interface = copy.deepcopy(plugin["extensions"]["com.openai"]["interface"])
    servers = mcp["mcpServers"]
    if not servers:
        raise ValueError("At least one remote MCP connection is required")
    portable_servers = {}
    legacy_servers = {}
    remotes = []
    for key, server in servers.items():
        # Refuse to publish secrets or silently drop fields when the contract changes.
        if not {"type", "url"} <= set(server) <= {"type", "url", "headers"} or server["type"] != "streamable-http":
            raise ValueError("Only remote Streamable HTTP connections with type/url (and the version header) are supported")
        endpoint = urlsplit(server["url"])
        if endpoint.scheme != "https" or not endpoint.hostname or endpoint.username or endpoint.password or endpoint.query or endpoint.fragment:
            raise ValueError("MCP endpoint must be HTTPS without credentials, query, or fragment")
        headers = version_headers(server, name, version)
        portable_servers[key] = {"type": "streamable-http", "url": server["url"], "headers": headers}
        legacy_servers[key] = claude_code_connection(server)
        # The Registry lists the server for every client, not this plugin: no plugin header.
        remotes.append({"type": "streamable-http", "url": server["url"]})
    return {
        # Claude's directory reads its listing links from the Claude manifest. Legal URLs are
        # authored once (with OpenAI's presentation); support and docs links under com.anthropic.claude.
        ".claude-plugin/plugin.json": {
            **common,
            "privacyPolicyUrl": interface["privacyPolicyURL"],
            "termsOfServiceUrl": interface["termsOfServiceURL"],
            **copy.deepcopy(plugin["extensions"].get("com.anthropic.claude", {})),
            "mcpServers": "./.mcp.json",
        },
        ".codex-plugin/plugin.json": {
            **common, "skills": "./skills/", "interface": interface,
            "mcpServers": "./.mcp.json",
        },
        # Agent Plugins hosts (current Codex, Cursor) read mcp.json and send the generated version
        # header. Claude Code (and older Codex) read .mcp.json, which never changes between
        # releases: Claude Code keys sign-ins on it (claude_code_connection).
        "mcp.json": {**{k: copy.deepcopy(v) for k, v in mcp.items() if k != "mcpServers"},
                     "mcpServers": portable_servers},
        ".mcp.json": {"mcpServers": legacy_servers},
        "server.json": {
            "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
            "name": f"io.github.{repo_parts[0]}/{name}",
            "title": interface["displayName"],
            "description": registry_description,
            "version": version,
            "repository": {"url": plugin["repository"], "source": "github"},
            "websiteUrl": plugin["homepage"],
            "remotes": remotes,
        },
    }


def sync(root, check=False):
    plugin = json.loads((root / "plugin.json").read_text())
    mcp = json.loads((root / "mcp.json").read_text())
    if plugin.get("license") != "MIT" or not (root / "LICENSE").read_text().startswith("MIT License\n"):
        raise ValueError("Manifest and public package LICENSE must both declare MIT")
    outputs = {relative: json.dumps(data, indent=2, ensure_ascii=False) + "\n"
               for relative, data in render(plugin, mcp).items()}
    for relative in VERSIONED_SKILLS:
        outputs[relative] = versioned_skill((root / relative).read_text(), plugin["version"], relative)
    stale = []
    for relative, expected in outputs.items():
        path = root / relative
        if not path.exists() or path.read_text() != expected:
            stale.append(relative)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected)
    return stale


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on drift without writing files")
    args = parser.parse_args()
    try:
        stale = sync(ROOT, check=args.check)
    except (KeyError, TypeError, ValueError, OSError) as error:
        print(f"Distribution check failed: {error}", file=sys.stderr)
        return 1
    if stale and args.check:
        print("Generated files are stale: " + ", ".join(stale), file=sys.stderr)
        print("Run python3 scripts/sync_distribution.py", file=sys.stderr)
        return 1
    print("Distribution files match canonical sources." if not stale else "Updated: " + ", ".join(stale))
    return 0


if __name__ == "__main__":
    sys.exit(main())
