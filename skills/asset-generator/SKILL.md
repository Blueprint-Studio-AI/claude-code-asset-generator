---
name: asset-generator
description: Use when the user wants to generate, browse, download, or manage visual assets (icons, illustrations, images, graphics, placeholders) using Blueprint Studio's AI asset generator.
---

# Asset Generator

Generate, browse, and manage Blueprint Studio assets using MCP tools.

## When to Use

- User asks to generate an image, icon, illustration, or visual asset
- User asks to create a placeholder image for a component or page
- User mentions Blueprint Studio assets
- User wants to browse, download, or delete generated assets
- User asks about available styles

## Before You Start

1. **Check for project config:** Read `.blueprint.json` in the project root. If it exists, use its defaults (`outputDir`, `defaultStyleId`, `defaultAspectRatio`, `defaultImageSize`).
2. **Check for global config:** Read `~/.config/blueprint-studio/config.json`. If it has no `apiKey`, tell the user to run `/asset-generator-setup` first and stop.
3. **If no `.blueprint.json`:** Use built-in defaults (outputDir: `./assets`, aspectRatio: `1:1`, imageSize: `2K`, no style). Suggest running `/asset-generator-setup` for project-specific config.

## Generating Assets

1. Call the `generate_asset` MCP tool with:
   - `prompt`: The user's description
   - `styleId`: From `.blueprint.json` defaultStyleId unless user specifies otherwise
   - `aspectRatio`: From `.blueprint.json` defaultAspectRatio unless user specifies otherwise
   - `imageSize`: From `.blueprint.json` defaultImageSize unless user specifies otherwise
   - `temperature`, `referenceImages`: Only if user provides them

2. After generation succeeds, call `download_asset` with the returned `assetId`.

3. Decode the base64 response and write the file to the `outputDir` from `.blueprint.json`.

4. **File naming:** Derive a descriptive filename from the prompt:
   - "a blue gradient settings icon" → `blue-gradient-settings-icon.png`
   - Use kebab-case, lowercase, `.png` extension
   - If the file already exists, append a numeric suffix: `settings-icon-2.png`
   - If the user specifies a filename, use that instead

5. Tell the user what was created and where. If they're working on code that references images (e.g., `<img>`, CSS `background-image`, imports), offer to update the reference.

## Browsing Assets

- Use `list_assets` to show recent assets. Default limit is 20.
- Use `get_asset` for details on a specific asset.
- Present results in a concise table or list format.

## Downloading Assets

- Use `download_asset` to get base64 image data.
- Write to the `outputDir` from `.blueprint.json` (or the path the user specifies).
- Use the asset's prompt to generate a descriptive filename.

## Deleting Assets

- Use `delete_asset` with the asset ID.
- Confirm with the user before deleting.

## Listing Styles

- Use `list_styles` to show available styles.
- Present as a simple list with ID and name.

## Common Mistakes

- Don't generate assets without checking for config first.
- Don't use a hardcoded output directory — always read from `.blueprint.json`.
- Don't skip the download step — `generate_asset` returns a URL, not file data. You need `download_asset` to get the actual image bytes to save locally.
