# Blueprint Studio

One plugin for Blueprint Studio Styles, assets, and durable image generation. Additional brand-context tools expose published guides and official assets when enabled on the connected server. Workflow skills and agents are optional; tools can be used directly.

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

Sign in through the host's MCP OAuth flow for account-wide access. Call `list_brands` to discover accessible organizations, then pass explicit `brandId` on every workspace call. Null/omitted selects personal scope, not the last-used brand. Legacy scoped credentials cannot switch workspaces. A plugin install grants no membership. Service API keys remain available for scoped automation; inference provider keys are not needed and credentials never belong in checked-in files.

## Tool contract and rollout

`generate_asset` already returns a durable `jobId` immediately. Use a fresh UUID `requestId` for each intended generation; reuse the same ID with identical arguments only for transport retries. Poll `get_generation_status` in the same `brandId` until `completed` or `failed`. Unknown outcomes and polling timeouts never establish failed generation or refunded credits. Preserve returned asset, receipt, and Style IDs. See [the MCP contract](skills/asset-generator/references/mcp-contract.md) for recovery and handoff details.

| Available now | Pending backend rollout; use only when discovered |
| --- | --- |
| Account OAuth and per-call workspace selection | `get_workspace_context` and published guide discovery |
| Styles, categories, generated examples, Style thumbnails | `list_models` capability and cost catalog |
| Durable generation/status, asset reads/downloads, background removal | `list_brand_assets` with version-pinned `generationInput` for ordered `inputs` |
| Brand/member administration within permissions | Exact `parentAssetId` edits and `get_generation_details` |

The plugin does not enable pending backend tools. Check live discovery for both tools and fields before using them. Reference-set Style authoring, tracked forks, and Portal-backed tasks/approvals are not bundled features. There is no internal client list, private repository access, or automatic brand-site/database sync.

## Optional skills and agents

- `asset-generator`: browse, generate, inspect, refine, and deliver assets.
- `brand-manager`: requested workspace and Style administration.
- `style-gym`: optional repeatable Style experiments on diverse briefs.

Claude Code also discovers two agents from `agents/`: `blueprint-studio:asset-creator` for a bounded production brief and `blueprint-studio:style-evaluator` for requested Style comparisons. They inherit host tools and permissions, use the same `asset-generator` MCP connection, and add no mandatory routing. Other hosts can use the skills directly; agent auto-discovery is host-specific. See the [Claude Code plugin agent format](https://code.claude.com/docs/en/plugins-reference#agents).

Suggested handoff to an existing project agent:

> Use Blueprint Studio for this project's brand context and assets. Select the intended brand from list_brands and pass its brandId on each call. Inspect available Styles and any discovered brand guides/official assets. Continue the existing brief. Use tools directly or adapt the optional workflows; save selected asset/receipt/Style IDs and any unresolved job/request IDs with the work so another session can resume.

A project `.blueprint.json` may set local preferences. It is not an authorization mechanism. Do not duplicate live brand files into this plugin to personalize an installation.

## Development

Backend and permission services live in the private monorepo; this public repository contains packaging and optional guidance only. Do not add tokens, production fixtures, client-private notes, or internal source links. Validate compatibility manifests and each skill before release. Public directory submission needs its own OAuth, metadata, and tool-annotation review.

Installation, cachebusting, and marketplace rollout are separate release steps. For local validation, run `claude plugin validate .`, the plugin-creator `validate_plugin.py` on this directory, and skill-creator `quick_validate.py` on each `skills/*` directory. Validation requires no generation calls or credentials.
