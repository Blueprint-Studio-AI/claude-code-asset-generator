# Blueprint Studio Asset Generator

Generate, browse, and manage Blueprint Studio assets directly from Claude Code.

## Setup

Run `/asset-generator-setup` in Claude Code to configure your API key and project defaults.

## Usage

Once configured, Claude can generate assets as part of natural conversation:

> "Generate a settings icon and save it to public/icons"

Or use the available MCP tools directly:

- `generate_asset` — Generate an image from a prompt
- `list_assets` — Browse your generated assets
- `get_asset` — Get details for a specific asset
- `delete_asset` — Delete an asset
- `download_asset` — Download an asset image
- `list_styles` — List available generation styles

## Configuration

### Global (`~/.config/blueprint-studio/config.json`)

Stores your API key. Created by `/asset-generator-setup`.

### Project (`.blueprint.json`)

Optional project-level config. Safe to commit to git.

```json
{
  "outputDir": "./public/assets",
  "defaultStyleId": "your-style-id",
  "defaultAspectRatio": "1:1",
  "defaultImageSize": "2K"
}
```
