# Blueprint Studio — Claude Code Plugin

Generate assets, manage brands, invite team members, and more — directly from Claude Code.
This Claude plugin is for use with the [Blueprint Studio Asset Generator](https://tools.blueprintstudio.ai/?utm_source=github&utm_medium=readme&utm_campaign=asset_generator_claude_plugin).

## Installation

### Option A: Via Marketplace (recommended)

```bash
/plugin marketplace add Blueprint-Studio-AI/claude-code-marketplace
/plugin install blueprint-studio@blueprint-studio-marketplace
```

### Option B: Direct from GitHub

```bash
/plugin install Blueprint-Studio-AI/claude-code-asset-generator
```

### Option C: Manual MCP config

Add the MCP server URL to your Claude Code config:

```json
{
    "mcpServers": {
        "blueprint-studio": {
            "url": "https://tools.blueprintstudio.ai/api/mcp"
        }
    }
}
```

Claude Code will open your browser to sign in with your Blueprint Studio account. No API keys needed.

## Usage

Once authenticated, Claude can work with Blueprint Studio as part of natural conversation:

> "Generate a settings icon in my brand style"
> "Invite brandon@example.com to my brand"
> "Create a new brand called Acme Design"
> "List my API keys"

## Available Tools

### Asset Generation

- `generate_asset` — Generate an image from a prompt
- `list_assets` — Browse generated assets
- `get_asset` — Get details for a specific asset
- `delete_asset` — Delete an asset
- `download_asset` — Download an asset image
- `favorite_asset` — Toggle favorite on an asset
- `remove_background` — Remove image background
- `share_asset` — Generate a shareable link

### Brand Management

- `create_brand` — Create a new brand/organization
- `list_brands` — List your brands
- `get_brand` — Get brand details and settings
- `update_brand_settings` — Update default style or prompt template
- `delete_brand` — Delete a brand (owner only)

### Team Management

- `invite_member` — Invite someone by email
- `list_members` — List members and pending invites
- `update_member_role` — Change a member's role
- `remove_member` — Remove a member

### Styles

- `list_styles` — List available styles
- `create_style` — Create a custom brand style
- `get_style` — Get style details
- `update_style` — Update a custom style
- `delete_style` — Delete a custom style

### Generation Helpers

- `suggest_prompts` — Get AI-powered prompt suggestions
- `generate_ideas` — Brainstorm asset concepts

### API Keys

- `create_api_key` — Create a key for automation/CI
- `list_api_keys` — List your active keys
- `revoke_api_key` — Revoke a key

## Project Config (`.blueprint.json`)

Optional project-level defaults. Safe to commit to git.

```json
{
    "outputDir": "./public/assets",
    "defaultStyleId": "your-style-id",
    "defaultAspectRatio": "1:1",
    "defaultImageSize": "2K"
}
```
