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
    if not isinstance(description, str) or not 1 <= len(description) <= 100:
        raise ValueError("Shared description must fit the MCP Registry's 100-character limit")
    common = {key: copy.deepcopy(plugin[key]) for key in IDENTITY_FIELDS if key in plugin}
    interface = copy.deepcopy(plugin["extensions"]["com.openai"]["interface"])
    servers = mcp["mcpServers"]
    if not servers:
        raise ValueError("At least one remote MCP connection is required")
    legacy_servers = {}
    remotes = []
    for key, server in servers.items():
        # Refuse to publish secrets or silently drop fields when the contract changes.
        if set(server) != {"type", "url"} or server["type"] != "streamable-http":
            raise ValueError("Only remote Streamable HTTP connections with type/url are supported")
        endpoint = urlsplit(server["url"])
        if endpoint.scheme != "https" or not endpoint.hostname or endpoint.username or endpoint.password or endpoint.query or endpoint.fragment:
            raise ValueError("MCP endpoint must be HTTPS without credentials, query, or fragment")
        legacy_servers[key] = {"type": "http", "url": server["url"]}
        remotes.append(copy.deepcopy(server))
    return {
        ".claude-plugin/plugin.json": {**common, "mcpServers": "./.mcp.json"},
        ".codex-plugin/plugin.json": {
            **common, "skills": "./skills/", "interface": interface,
            "mcpServers": "./.mcp.json",
        },
        ".mcp.json": {"mcpServers": legacy_servers},
        "server.json": {
            "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
            "name": f"io.github.{repo_parts[0]}/{name}",
            "title": interface["displayName"],
            "description": description,
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
    stale = []
    for relative, data in render(plugin, mcp).items():
        expected = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
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
