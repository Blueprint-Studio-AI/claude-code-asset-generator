---
name: asset-generator
description: Create, edit, inspect, and download images with Blueprint Studio Asset Generator, using workspace Styles and official brand assets. Use for Blueprint visual production and asset-library tasks.
---

# Asset Generator

Use the connected Blueprint MCP tools. These are composable suggestions, not a required workflow.

## Establish context

Call `get_workspace_context` and `list_models` when available. Confirm the connected workspace matches the task. Read the returned brand guide when relevant. A project’s `.blueprint.json` can supply output paths and preferred Style/settings, but cannot authorize or switch organizations. User instructions take precedence; otherwise use the model's returned defaults.

For older servers without context discovery, use `list_brands`, `list_styles`, and the connection's selected organization. Do not assume naming a brand in the prompt selects it. Do not claim new tools are available until they appear in tool discovery.

## Create and improve

- Browse `list_assets` and `list_styles` before generating near-duplicates. Read `get_style` for the selected look.
- For logos, call `list_brand_assets`; choose the correct brand, mark/lockup, and color. Pass each returned `generationInput` in `generate_asset.inputs`. These handles pin the official version and compile logo guidance. A mention of “logo” in MCP text alone does not attach a file.
- `inputs` preserves order and supports official brand assets, authorized URL references, and saved receipt inputs. Do not mix it with legacy `referenceImages`. Never substitute a preview screenshot for an official logo.
- Start with a small useful batch. Set model/size/quality only from supported capabilities; generation incurs workspace-account credits.
- To edit, call `generate_asset` with the exact `parentAssetId` and edit instructions. Select the ancestor the user means, not the newest image in a thread. It creates a descendant and preserves the source.
- Download and actually view each output before endorsing it. Check composition, style, lettering, logo fidelity, cropping, and intended placement. Revise one variable at a time when useful.
- Save `assetId`, `receiptId`, Style ID, and chosen settings alongside accepted work. `get_generation_details` reports captured settings and Style version without exposing protected instructions. Missing receipt fields are not defaults.

## Deliver files

`download_asset` returns image bytes and MIME type; a returned image URL is also usable with the host's download tools. Preserve the actual format (`.jpg`, `.png`, or `.webp`), never just rename JPEG bytes to PNG. Use the requested project location or its `.blueprint.json` outputDir; otherwise choose a conventional asset folder in that project. Update image references in code when part of the task.

`remove_background` produces a new transparent cutout asset. Keep its returned asset identity; inspect edges and alpha before using it. Prefer CSS or vector code for simple backgrounds, typography, and existing official logos; generate the imagery that benefits from it.

## Recovery

Current generation calls are synchronous. If a call times out or disconnects, check recent assets and their details before retrying: the provider may still complete and a blind retry may charge twice. Report uncertainty if completion cannot be established. Authentication and limits are handled by the service; never work around them with another org or a provider key.

Brand/team management is in the optional `brand-manager` skill. For repeatable Style experiments, see `style-gym`.
