---
name: asset-generator
description: Create, edit, inspect, and download images with Blueprint Studio Asset Generator, using workspace Styles and official brand assets. Use for Blueprint visual production and asset-library tasks.
---

# Asset Generator

Use the connected Blueprint MCP tools directly or adapt these optional workflows. Before workspace calls or generation, read [the MCP contract](references/mcp-contract.md) for account OAuth, explicit per-call `brandId`, durable jobs, and discovery-gated additions. `generate_asset` returns a job immediately: use a fresh UUID `requestId` per intended generation, reuse it only with identical arguments for transport retries, and poll the returned job in the same workspace until terminal. A timeout never proves failure or a refund.

## Context and creation

- Select the intended workspace from `list_brands`. When available, use `get_workspace_context` and read the relevant published guide. A project's `.blueprint.json` can supply preferred output paths and settings, but grants no access. User instructions take precedence.
- Browse `list_assets` when reuse would help and `list_styles` to choose a look. Read `get_style` as needed. Pass the actual `styleId` when using a saved Style; describing its name in a prompt does not associate the image with it.
- When exposed, use `list_models` for capabilities/defaults and `list_brand_assets` for official version-pinned `generationInput` handles. Preserve their order in `inputs`. Select the exact `parentAssetId` for edits when the schema supports it. See the contract for rollout limits and retries.
- Keep the batch proportional to the brief and any stated budget. Each intended generation can consume credits. Use only supported model/settings, then download and actually view saved outputs before endorsing them. Check composition, lettering, logo fidelity, cropping, and intended placement; revise meaningful variables when useful.
- Keep returned asset, receipt, and Style IDs with accepted work. Use `get_generation_details` when available to inspect captured settings; report missing information as unknown.

## Shared Styles

Get existing categories from `list_styles` before creating a Style. Reuse a fitting category unless the user requests another. Create the Style before generating its saved examples, and pass its returned `styleId` with the intended `brandId` on those generations. Freestyle exploration remains Freestyle; never retroactively label it as a saved Style's output.

Finish the library entry with a representative saved example: read the Style's `updatedAt` using `get_style`, then call `set_style_thumbnail` with the example's `assetId` and `expectedUpdatedAt` in that workspace. Refresh on a conflict rather than blindly retrying. Verify category/thumbnail with `get_style` and examples with Style-filtered `list_assets`. The thumbnail changes display metadata, not generation references. If a required tool is absent, report the unfinished portion.

## Delivery

A completed `get_generation_status`, and `download_asset`, return a small preview image you can see plus `webUrl` (the image in the user's Blueprint Studio library), `libraryUrl`, a full-resolution `downloadUrl`, and `suggestedFilename`. Older servers return only `imageUrl`; use it as the download URL. After each image the user keeps:

1. **Save it into the project** unless the user said not to: the requested location, else `.blueprint.json` `outputDir`, else `./assets/`. Name it from `suggestedFilename` or a short slug of the brief, and keep its real extension (never rename JPEG bytes to PNG). With shell access: `mkdir -p assets && curl -fsSL -o "assets/<file>" "<downloadUrl>"`; otherwise use the host's download tool. `download_asset` inlines base64 only with `includeBase64`, for hosts without network access; never paste base64 into files by hand.
2. **Show where it is.** Give the saved path and always the `webUrl`, so the user can open it in Blueprint Studio; give `libraryUrl` the first time, for everything they have made.
3. **Offer to open it** on their machine: `open <path>` on macOS, `xdg-open <path>` on Linux, `start "" <path>` on Windows. Open it when the user agrees or asked to see it, not in headless or CI sessions.

Update code references when part of the task.

`remove_background` saves a new cutout. If its schema exposes `operationId`, retain the same ID and source asset for recovery and honor processing responses. Keep its returned asset identity and inspect edges/alpha. Prefer CSS or vector code for simple backgrounds, typography, and existing official logos.

Hand off files and returned IDs, plus unresolved job handles if any. A saved asset is not automatically a published webpage. For requested administration see `brand-manager`; for reusable Style experiments see `style-gym`.
