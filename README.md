# Blueprint Studio

Blueprint Studio is a design and development studio. This plugin connects Claude Code and Codex to Blueprint Studio Asset Generator, so anyone can create on-brand images and visual assets with their own brand's Styles and logos. Studio clients also get the brand workspace our team maintains for them (official logos, brand guides and Styles) right inside their coding agent.

Your brand's Styles, official logos and guides, and asset library live in one place, shared with your team. Your agent uses them to make on-brand icons, social graphics, hero images and slides that match, and saves them to your project and your Asset Generator library. Workflow skills and agents are optional; tools can be used directly.

Using Claude on the web, desktop or mobile, ChatGPT, Cursor or VS Code instead? See [Connect your AI](https://tools.blueprintstudio.ai/mcp-setup).

Install it from the [Blueprint marketplace](https://github.com/Blueprint-Studio-AI/claude-code-marketplace) below. This repository keeps the name `claude-code-asset-generator` so existing installs keep working.

## Install

Claude Code:

```text
/plugin marketplace add Blueprint-Studio-AI/claude-code-marketplace
/plugin install blueprint-studio@blueprint-studio-marketplace
```

To connect, run `/mcp`, select `plugin:blueprint-studio:asset-generator` (Blueprint Studio) and choose Authenticate; if your browser can't connect after you approve, copy the link from the Blueprint Studio tab and paste it into Claude Code, or run `/mcp` → `plugin:blueprint-studio:asset-generator` → Authenticate again.

For a local branch preview, start Claude Code with `--plugin-dir /absolute/path/to/this/repo`. Avoid adding a second standalone MCP connection if the plugin already supplies `asset-generator`.

Codex installs the same plugin from the same marketplace:

```text
codex plugin marketplace add https://github.com/Blueprint-Studio-AI/claude-code-marketplace.git
codex plugin add blueprint-studio@blueprint-studio-marketplace
```

Your browser opens so you can approve in the Blueprint Studio window. Then start a new Codex session. Want the tools without the plugin? Run `codex mcp add blueprint-studio --url https://tools.blueprintstudio.ai/api/mcp` instead. Use one or the other, not both.

## First image

In Claude Code, run `/blueprint-studio:start` (or ask what Blueprint Studio Asset Generator can do). It reads the account, says what Asset Generator does and the real free allowance, offers three starters, then makes the image from one pick, saves it into the project and links it in Asset Generator. No brand or setup is needed.

Or ask for one directly, in any host:

> Use Blueprint Studio Asset Generator to make a hero image for my website: a cozy neighborhood coffee shop at sunrise, warm light, 16:9

Then, so later images match your brand:

> Set up my brand from mywebsite.com so my images match it

The server also offers these starters as MCP prompts: `first_image`, `brand_from_website`, `app_icon` and `social_post`. Claude Code lists them as slash commands, e.g. `/mcp__plugin_blueprint-studio_asset-generator__first_image` with this plugin. Claude Code passes only the first word of a prompt argument, so the image starters ask for one line instead of taking one; `brand_from_website` takes a website. Codex doesn't show MCP prompts; its plugin card offers the same starters (`defaultPrompt`).

Using another AI app? Connect it to `https://tools.blueprintstudio.ai/api/mcp` with the steps in [Connect your AI](https://tools.blueprintstudio.ai/mcp-setup). Apps that support skills can also use `skills/`.

Sign in when your app asks. One connection covers your personal library and every brand you belong to. Start with `get_workspace_context`: it returns your plan, credits left, what a default image costs, your brands and, for new accounts, a getting-started plan. No brand is needed; leave `brandId` out to work in your personal library. If you have exactly one brand, the agent works in it unless you ask for your personal library; with several, it passes the `brandId` of the one you name on every call. Installing the plugin doesn't add you to a brand, so accept your brand invitation first. If an older connection sees only one brand, disconnect it in Settings and connect again. API keys are only for scripts and automations, you don't need an OpenAI or Google key, and keys never go in project files.

## Tool contract

`generate_asset` already returns a durable `jobId` immediately. Use a fresh UUID `requestId` for each intended generation; reuse the same ID with identical arguments only for transport retries. Poll `get_generation_status` in the same `brandId` until `completed` or `failed`. Unknown outcomes and polling timeouts never establish failed generation or refunded credits. Preserve returned asset, receipt, and Style IDs. See [the MCP contract](skills/asset-generator/references/mcp-contract.md) for recovery and handoff details.

| Core tools | Context and references |
| --- | --- |
| Account OAuth and per-call workspace selection | `get_workspace_context` and published guide discovery |
| Styles, categories, generated examples, Style thumbnails | `list_models` capability and cost catalog |
| Generation and status, asset reads, downloads and share links | `list_brand_assets` with version-pinned `generationInput` for ordered `inputs` |
| Brand/member administration within permissions | Exact `parentAssetId` edits and `get_generation_details` |

The plugin doesn't include Style editing from reference images, client project tasks or approvals, or access to private repositories. Brand setup reads your website once when you ask; it doesn't keep your brand in sync with the site.

## Optional skills and agents

- `start`: guided first run; three starters, then a first image saved into the project.
- `asset-generator`: browse, generate, inspect, refine, and deliver assets.
- `brand-manager`: requested workspace and Style administration.
- `style-gym`: optional repeatable Style experiments on diverse briefs.

Claude Code also discovers two agents from `agents/`: `blueprint-studio:asset-creator` for a bounded production brief and `blueprint-studio:style-evaluator` for requested Style comparisons. They inherit host tools and permissions, use the same `asset-generator` MCP connection, and add no mandatory routing. Other hosts can use the skills directly; agent auto-discovery is host-specific. See the [Claude Code plugin agent format](https://code.claude.com/docs/en/plugins-reference#agents).

Suggested handoff to an existing project agent:

> Use Blueprint Studio Asset Generator for this project's brand context and assets. Select the intended brand from list_brands and pass its brandId on each call. Inspect available Styles and any discovered brand guides/official assets. Continue the existing brief. Use tools directly or adapt the optional workflows; save selected asset/receipt/Style IDs and any unresolved job/request IDs with the work so another session can resume.

A project `.blueprint.json` may set local preferences. It is not an authorization mechanism. Do not duplicate live brand files into this plugin to personalize an installation.

## Maintainers

See [distribution and release instructions](docs/distribution.md).

## License

This public plugin package is [MIT licensed](LICENSE). This does not license Blueprint Studio's separately hosted backend, private Style instructions, or client materials. Published MCP Registry metadata is separately dedicated to CC0 under the [Registry terms](https://modelcontextprotocol.io/registry/terms-of-service).
