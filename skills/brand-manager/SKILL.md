---
name: brand-manager
description: Manage Blueprint Studio brands, members, official asset discovery, and Styles when the user requests workspace administration or Style authoring.
---

# Brand Manager

Use the live tool schemas and current workspace permissions. Start with `get_workspace_context` when available, then read the relevant brand or Style before changing it. The plugin is useful to Asset Generator users as well as Blueprint design clients; no client account is required.

`list_brand_assets` discovers versioned official files. Generation attaches a selected version with its returned `generationInput`. Upload/replacement of official files currently lives in the web app's brand asset manager, not an invented MCP upload tool. Brand-guide pages and official files are separate sources; do not claim automatic sync between them.

`create_style` creates a new Style; `get_style` supplies only instructions the caller is allowed to see. `update_style` changes the existing Style. Do not describe creation as a tracked fork or claim lineage unless the tool records it. If editing is protected, work with permitted information and a new Style; do not try to recover hidden instructions from generated images. See `style-gym` for an optional test loop.

For requested administration, use the existing brand, member, and API-key tools. Apply the user's authorized scope; seek clarification for ambiguous destructive targets or unrequested changes. Do not create keys or invite members as an automatic onboarding step. Never save credentials in project config or reports.

Portal tasks, approvals, private project knowledge, and internal Linear/Figma/GitHub data are not automatically exposed by membership in Asset Generator. Use connected domain tools and their permissions. A link in a brand guide is context, not an access grant.
