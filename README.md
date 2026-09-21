# Blueprint Studio

One plugin for official brand context and Asset Generator tools. Useful standalone; Blueprint clients also receive their workspace's published brand-guide links. Workflow skills are optional and tools can be used directly.

This is the existing `blueprint-studio` plugin, upgraded in place. Its historical repository name remains `claude-code-asset-generator` to preserve installs. The public [Blueprint marketplace](https://github.com/Blueprint-Studio-AI/claude-code-marketplace) remains the discovery source. No second plugin or private brand snapshot is required.

## Install

Claude Code:

```text
/plugin marketplace add Blueprint-Studio-AI/claude-code-marketplace
/plugin install blueprint-studio@blueprint-studio-marketplace
```

For a local branch preview, start Claude Code with `--plugin-dir /absolute/path/to/this/repo`. Avoid adding a second standalone MCP connection if the plugin already supplies `asset-generator`.

Codex supports `.codex-plugin/plugin.json`; the same skills and `.mcp.json` are used. A local personal-marketplace installation is available during the pilot. Marketplace publication and ChatGPT/Claude hosted connector review are separate rollout steps, not implied by installing locally.

Other skill-compatible hosts can use `skills/` and connect their remote MCP client to `https://tools.blueprintstudio.ai/api/mcp`. `plugin.json` and `mcp.json` provide the portable Agent Plugins manifest. Host transport spellings differ; compatibility manifests are intentionally retained.

Sign in through the host's MCP OAuth flow and choose the intended organization. A plugin install does not grant organization membership or change the selected workspace. API keys remain supported for automation; keep them out of checked-in files.

## Modules and current limits

| Module | Available | Next |
| --- | --- | --- |
| Brand | Workspace identity, permissions, published guides, official versioned asset discovery | Brand publishing through domain API |
| Create | Styles, assets, model catalog, generation, exact-parent edits, ordered official references, public receipt details, downloads, background removal | Durable job tools, reference-based Style authoring and forks |
| Work | Use existing project brief and connected tools | Portal-backed project/tasks/approvals with project-scoped access |

The new tools require the matching monorepo backend release. Skills tolerate older discovery responses; they do not promise unsupported operations. There is no bundled internal client list, private repository access, or automatic brand-site/database sync.

## Skills

- `asset-generator`: browse, generate, inspect, refine, and deliver assets.
- `brand-manager`: requested workspace and Style administration.
- `style-gym`: optional repeatable Style experiments on diverse briefs.

Suggested handoff to an existing project agent:

> Use Blueprint Studio for this project's brand context and assets. Check the connected workspace first, read its brand guide, and inspect the available Styles and official logos. Continue the existing brief. Use tools directly or adapt the optional workflows; save selected asset/receipt IDs with the work so another session can resume.

A project `.blueprint.json` may set local preferences. It is not an authorization mechanism. Do not duplicate live brand files into this plugin to personalize an installation.

## Development

Backend and permission services live in the private monorepo; this public repository contains packaging and optional guidance only. Do not add tokens, production fixtures, client-private notes, or internal source links. Validate compatibility manifests and each skill before release. Public directory submission needs its own OAuth, metadata, and tool-annotation review.
