---
name: asset-generator
description: Create, edit, inspect, and download images with Blueprint Studio Asset Generator, using workspace Styles and official brand assets. Use for Blueprint visual production and asset-library tasks.
---

# Asset Generator

Use the connected Blueprint MCP tools directly or adapt these optional workflows. Before workspace calls or generation, read [the MCP contract](references/mcp-contract.md) for account OAuth, explicit per-call `brandId`, durable jobs, and discovery-gated additions. `generate_asset` returns a job immediately: use a fresh UUID `requestId` per intended generation, reuse it only with identical arguments for transport retries, and poll the returned job in the same workspace until terminal. A timeout never proves failure or a refund.

## First run

Start with `get_workspace_context`. It returns the plan, credits left, what a default image costs, the account's brands and, for a new account, a `gettingStarted` block. A new account needs no brand or Style: omit `brandId` to create in the personal library with the defaults. When `gettingStarted` is present and the user wants an image, make one promptly (at most one short question), leaving `modelId`, `imageSize` and `quality` unset. Show the finished image, then offer variations and, after the first image, brand setup.

## Context and creation

- Select the intended workspace: personal (`brandId` null or omitted) or a brand from `get_workspace_context` or `list_brands`. Read the relevant published guide for a brand. A project's `.blueprint.json` can supply preferred output paths and settings, but grants no access. User instructions take precedence.
- Browse `list_assets` when reuse would help and `list_styles` to choose a look. Read `get_style` as needed. Pass the actual `styleId` when using a saved Style; describing its name in a prompt does not associate the image with it.
- When exposed, use `list_models` for capabilities/defaults and `list_brand_assets` for official version-pinned `generationInput` handles. Preserve their order in `inputs`. Select the exact `parentAssetId` for edits when the schema supports it. See the contract for rollout limits and retries.
- Keep the batch proportional to the brief and any stated budget. Each generation spends credits weighted by model, size and quality, so one image is not one credit. Quote costs from `get_workspace_context` (`defaultImage.credits`), `get_asset_generator_usage` (`creditsPerDefaultImage`) or `list_models`; never assume one credit per image. Higher quality, larger sizes and premium models cost more, and Free plans make 1K only: don't take 2K or 4K from `.blueprint.json` unless `defaultImage.sizesOnThisPlan` includes it. Use only supported model/settings, then download and actually view saved outputs before endorsing them. Check composition, lettering, logo fidelity, cropping, and intended placement; revise meaningful variables when useful.
- Keep returned asset, receipt, and Style IDs with accepted work. Use `get_generation_details` when available to inspect captured settings; report missing information as unknown.

## Shared Styles

Get existing categories from `list_styles` before creating a Style. Reuse a fitting category unless the user requests another. Create the Style before generating its saved examples, and pass its returned `styleId` with the intended `brandId` on those generations. Freestyle exploration remains Freestyle; never retroactively label it as a saved Style's output.

Finish the library entry with a representative saved example: read the Style's `updatedAt` using `get_style`, then call `set_style_thumbnail` with the example's `assetId` and `expectedUpdatedAt` in that workspace. Refresh on a conflict rather than blindly retrying. Verify category/thumbnail with `get_style` and examples with Style-filtered `list_assets`. The thumbnail changes display metadata, not generation references. If a required tool is absent, report the unfinished portion.

## Delivery

`download_asset` returns image bytes and MIME type; a returned image URL also works with host download tools. Preserve the actual format rather than renaming JPEG bytes to PNG. Use the requested project location or its `.blueprint.json` outputDir; otherwise choose a conventional project asset folder. Update code references when part of the task.

`remove_background` saves a new cutout. If its schema exposes `operationId`, retain the same ID and source asset for recovery and honor processing responses. Keep its returned asset identity and inspect edges/alpha. Prefer CSS or vector code for simple backgrounds, typography, and existing official logos.

Hand off files and returned IDs, plus unresolved job handles if any. A saved asset is not automatically a published webpage. For requested administration see `brand-manager`; for reusable Style experiments see `style-gym`.
