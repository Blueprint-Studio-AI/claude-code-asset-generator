# Blueprint Studio

Blueprint Studio is a design and development studio. This plugin connects Claude Code and Codex to Blueprint Studio Asset Generator, so anyone can create on-brand images and visual assets with their own brand's Styles and logos. Studio clients also get the brand workspace our team maintains for them (official logos, brand guides and Styles) right inside their coding agent.

Your brand's Styles, official logos and guides, and asset library live in one place, shared with your team. Your agent uses them to make on-brand icons, social graphics, hero images and slides that match, and saves them to your project and your Asset Generator library. The skills are optional; the tools work on their own.

Using Claude on the web, desktop or mobile, ChatGPT, Cursor or VS Code instead? See [Connect your AI](https://tools.blueprintstudio.ai/mcp-setup).

Install it from the [Blueprint marketplace](https://github.com/Blueprint-Studio-AI/claude-code-marketplace) below. This repository keeps the name `claude-code-asset-generator` so existing installs keep working.

## Install

Claude Code:

```text
/plugin marketplace add Blueprint-Studio-AI/claude-code-marketplace
/plugin install blueprint-studio@blueprint-studio-marketplace
```

Or from a terminal, in one line:

```text
claude plugin marketplace add Blueprint-Studio-AI/claude-code-marketplace && claude plugin install blueprint-studio@blueprint-studio-marketplace
```

To connect, run `/mcp`, select `plugin:blueprint-studio:asset-generator` (Blueprint Studio) and choose Authenticate; if Claude Code doesn't pick up the sign-in after you click Connect, copy the link from the Blueprint Studio tab and paste it into Claude Code, or run `/mcp` → `plugin:blueprint-studio:asset-generator` → Authenticate again.

Claude Code asks you to approve each Blueprint Studio step. To allow them all, run `/permissions` and add the allow rule `mcp__plugin_blueprint-studio_asset-generator` (it covers this plugin's tools only, deletions included); remove it there at any time.

For a local branch preview, start Claude Code with `--plugin-dir /absolute/path/to/this/repo`. Avoid adding a second standalone MCP connection if the plugin already supplies `asset-generator`.

Codex installs the same plugin from the same marketplace:

```text
codex plugin marketplace add https://github.com/Blueprint-Studio-AI/claude-code-marketplace.git
codex plugin add blueprint-studio@blueprint-studio-marketplace
```

Or in one line, which also signs you in:

```text
codex plugin marketplace add Blueprint-Studio-AI/claude-code-marketplace && codex plugin add blueprint-studio@blueprint-studio-marketplace && codex mcp login asset-generator
```

Your browser opens so you can click Connect in the Blueprint Studio window. Then start a new Codex session. Want the tools without the plugin? Run `codex mcp add blueprint-studio --url https://tools.blueprintstudio.ai/api/mcp` instead. Use one or the other, not both.

## Update

The tools come from the hosted service, so they're always current. The skills update with the plugin. When a newer plugin is out, `get_workspace_context` says so once per session (`pluginUpdate`), and your agent tells you how to update.

Claude Code: run `/plugin`, open **Installed**, select `blueprint-studio` and choose **Update now**, then run `/reload-plugins`. From a terminal:

```text
claude plugin update blueprint-studio@blueprint-studio-marketplace
```

To get new versions automatically, run `/plugin`, open **Marketplaces**, select `blueprint-studio-marketplace` and turn on auto-update. If you added Blueprint Studio from Claude's Directory, Claude Code updates it when it starts, once the Directory has the new version.

Codex:

```text
codex plugin marketplace upgrade blueprint-studio-marketplace
```

Then start a new Codex session.

## First image

In Claude Code, run `/blueprint-studio:start` (or ask what Blueprint Studio Asset Generator can do). It reads the account, says what Asset Generator does and the real free allowance, offers three starters, then makes the image from one pick, saves it into the project and links it in Asset Generator. No brand or setup is needed.

Or ask for one directly, in any host:

> Use Blueprint Studio Asset Generator to make a hero image for my website: a cozy neighborhood coffee shop at sunrise, warm light, 16:9

Then, so later images match your brand:

> Set up my brand from mywebsite.com so my images match it

The server also offers these starters as MCP prompts: `first_image`, `brand_from_website`, `app_icon` and `social_post`. Claude Code lists them as slash commands, e.g. `/mcp__plugin_blueprint-studio_asset-generator__first_image` with this plugin. Claude Code passes only the first word of a prompt argument, so the image starters ask for one line instead of taking one; `brand_from_website` takes a website. Codex doesn't show MCP prompts; its plugin card offers the same starters (`defaultPrompt`).

Using another AI app? Connect it to `https://tools.blueprintstudio.ai/api/mcp` with the steps in [Connect your AI](https://tools.blueprintstudio.ai/mcp-setup). Without this plugin, `get_guide` gives your agent the same skills as how-to guides. Apps that support skills can also use `skills/`.

Sign in when your app asks. One connection covers your personal library and every brand you belong to. Start with `get_workspace_context`: it returns your plan, credits left, what a default image costs, your brands with their guides and what your role allows and, for new accounts, a getting-started plan. No brand is needed; leave `brandId` out to work in your personal library. If you have exactly one brand, the agent works in it unless you ask for your personal library; with several, it passes the `brandId` of the one you name on every call. Installing the plugin doesn't add you to a brand, so accept your brand invitation first. If an older connection sees only one brand, disconnect it in Settings and connect again. API keys are only for scripts and automations and are on Pro and Max (sign-in works on every plan), you don't need an OpenAI or Google key, and keys never go in project files.

## Skills

Each skill is built on one rule, with numbers measured on our own service, the failures we've already seen, and its limits. `start` routes to the others.

| Skill | What it's for | The rule |
| --- | --- | --- |
| `start` | First run: what Asset Generator does, your real balance, three starters, a first image | One question at most, then make something |
| `asset-generator` | One image made, checked and saved into your project; edits of a saved image | An edit is the saved image plus one change, never a new prompt |
| `asset-sets` | Many matching images in one batch: icon sets, series, one campaign in several sizes | N images is one wait, not N waits |
| `brand-setup` | Your brand saved from your website or a few images, with a Style and your logo | Save only what you approved |
| `official-logos` | Find, add, label and place your official logos | A logo is used as supplied, never redrawn |
| `styles` | Build, test and keep reusable Styles | Keep a Style only after it works on three different briefs |

Each skill folder has a short `SKILL.md`, `references/` for depth, and `evals/evals.json` with try-it prompts and the behaviour to expect. Apps without the plugin get the same text from the server: `get_guide` with `topic` `start`, `assets` (`asset-generator`), `asset_set` (`asset-sets`), `brand` (`brand-setup`), `logos` (`official-logos`), `styles`, or `contract` (jobs and recovery). With the plugin installed you already have it.

Before 2.11.0 the plugin shipped `brand-manager` and `style-gym` skills and two Claude Code agents, `asset-creator` and `style-evaluator`. Their content now lives in `brand-setup`, `styles` and `asset-sets` and their references.

Suggested handoff to an existing project agent:

> Use Blueprint Studio Asset Generator for this project's brand context and assets. Select the intended brand from list_brands and pass its brandId on each call. Inspect available Styles and any discovered brand guides/official assets. Continue the existing brief. Use tools directly or adapt the optional workflows; save selected asset/receipt/Style IDs and any unresolved job/request IDs with the work so another session can resume.

A project `.blueprint.json` may set local preferences. It is not an authorization mechanism. Do not duplicate live brand files into this plugin to personalize an installation.

## What the plugin connects to

The plugin has no hooks or local programs. It adds one remote MCP server, Blueprint Studio's hosted service at `https://tools.blueprintstudio.ai/api/mcp`, which you sign in to with OAuth. So the service can tell you when a newer plugin is out, the plugin says which version it is. In Codex, each request carries an `X-Blueprint-Plugin` header with the plugin's name and version (for example `blueprint-studio/2.10.2`). In Claude Code the connection sends no extra header; instead, the `start` and `asset-generator` skills ask your agent to pass the version as `pluginVersion` when it calls `get_workspace_context`. Neither holds anything else. When your agent calls a tool, what that tool needs goes to the service: your prompts and settings, brand details, and any images, files or links you pass as inputs. Images are made with AI model providers and saved to your Blueprint Studio library. Brand setup reads the website you name, once, when you ask. With shell access, the skills also use `curl` for two things: saving a finished image from the `downloadUrl` the service returns, and sending a local file to the single-use upload link `create_upload_link` returns. Both links point at Blueprint Studio's own file storage (hosted on Supabase). See the [privacy policy](https://tools.blueprintstudio.ai/privacy).

## Maintainers

See [distribution and release instructions](docs/distribution.md).

## License

This public plugin package is [MIT licensed](LICENSE). This does not license Blueprint Studio's separately hosted backend, private Style instructions, or client materials. Published MCP Registry metadata is separately dedicated to CC0 under the [Registry terms](https://modelcontextprotocol.io/registry/terms-of-service).
