---
description: Configure Blueprint Studio asset generator — API key and project defaults
argument-hint: (no arguments needed)
---

# Asset Generator Setup

Walk the user through configuring the Blueprint Studio asset generator. Follow these steps conversationally.

## Step 1: Global Config (API Key)

Check if `~/.config/blueprint-studio/config.json` exists and has an `apiKey` field.

**If no API key:**
1. Ask the user for their Blueprint Studio API key. Tell them they can create one at https://tools.blueprintstudio.ai under Settings → API Keys.
2. Validate the key by calling the `list_styles` MCP tool. If it fails with an auth error, tell the user the key is invalid and ask them to try again.
3. Create the directory `~/.config/blueprint-studio/` if it doesn't exist.
4. Write `~/.config/blueprint-studio/config.json`:
   ```json
   {
     "apiKey": "<their-key>",
     "baseUrl": "https://tools.blueprintstudio.ai/api/v1"
   }
   ```
5. Write `~/.config/blueprint-studio/mcp-auth.json`:
   ```json
   {
     "headers": {
       "Authorization": "Bearer <their-key>"
     }
   }
   ```

**If API key exists:** Tell the user their API key is already configured. Ask if they want to update it.

## Step 2: Project Config

Check if `.blueprint.json` exists in the project root.

**If no project config (or user wants to reconfigure):**

1. **Output directory:** Ask where generated assets should be saved. Default: `./public/assets`. Confirm the directory exists or offer to create it.

2. **Default style:** Call `list_styles` and show the available styles in a numbered list. Let the user pick a default or skip (freestyle). If they pick one, save its ID.

3. **Default aspect ratio:** Ask which aspect ratio to use by default. Options: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `4:5`, `5:4`, `21:9`. Default: `1:1`.

4. **Default image size:** Ask which resolution to use by default. Options: `1K`, `2K`, `4K`. Default: `2K`.

5. Write `.blueprint.json` to the project root with only the fields the user configured (omit fields left at default).

**If project config exists:** Show current config and ask what the user wants to change.

## Step 3: Confirmation

Summarize what was configured:
- API key: configured (masked)
- Output directory: `<path>`
- Default style: `<name>` or freestyle
- Default aspect ratio: `<ratio>`
- Default image size: `<size>`

Tell the user they're ready to go. They can generate assets by asking Claude or using the MCP tools directly.
