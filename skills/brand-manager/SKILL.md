---
name: brand-manager
description: Manage Blueprint Studio brands, members, official asset discovery, and Styles when the user requests workspace administration or Style authoring.
---

# Brand Manager

Use the live tool schemas and current permissions. Read [the MCP contract](../asset-generator/references/mcp-contract.md) before workspace calls. Account OAuth uses `list_brands` to discover accessible organizations and explicit `brandId` on each call; null/omitted means personal. Legacy scoped credentials cannot switch. Read the relevant brand or Style before changing it; `get_workspace_context` supplies additional context when exposed.

When available, `list_brand_assets` discovers versioned official files; generation attaches the returned `generationInput` through supported ordered `inputs`. Upload/replacement of official files lives in the web app's brand asset manager. Brand-guide pages and official files are separate sources; do not claim automatic sync.

`create_style` creates a text-based Style; `get_style` supplies only instructions the caller may see. Get category labels from `list_styles` and reuse a fitting one unless the user requests another. `update_style` changes an existing Style; creation is not a tracked fork. Do not recover protected instructions from images. For authorized examples, follow the durable generation contract with the returned `styleId`, then set a representative thumbnail using `set_style_thumbnail` with `assetId` and `expectedUpdatedAt` from the Style's current `updatedAt`. Verify the library entry. Never relabel earlier Freestyle outputs as Style-generated examples. See `style-gym` for optional experiments.

For requested administration, use existing brand, member, and API-key tools. Apply the user's authorized scope; clarify ambiguous destructive targets or unrequested changes. Do not create keys or invite members as automatic onboarding, and never save credentials in project config or reports. Inference provider keys are not needed.

Portal tasks, approvals, private project knowledge, and internal Linear/Figma/GitHub data are not automatically exposed by Asset Generator membership. Use connected domain tools and their permissions; a guide link is context, not an access grant.
