---
name: brand-manager
description: Manage Blueprint Studio brands, team members, styles, and API keys
triggers:
  - create a brand
  - invite someone
  - manage my team
  - list members
  - add a member
  - remove a member
  - manage styles
  - create a style
  - manage api keys
  - create an api key
---

# Brand Manager

Manage Blueprint Studio brands, team members, styles, and API keys through natural conversation.

## Available Tools

### Brand Management
- `create_brand` — Create a new brand/organization
- `list_brands` — List brands you belong to
- `get_brand` — Get brand details, settings, and member count
- `update_brand_settings` — Update default style or prompt template
- `delete_brand` — Delete a brand (owner only)

### Team Management
- `invite_member` — Invite a user by email with a role
- `list_members` — List members and pending invites
- `update_member_role` — Change a member's role (admin/member)
- `remove_member` — Remove a member from a brand

### Style Management
- `list_styles` — List available styles (system + custom)
- `create_style` — Create a custom brand style
- `get_style` — Get style details and references
- `update_style` — Update a custom style
- `delete_style` — Delete a custom style

### API Key Management
- `create_api_key` — Create a new API key for automation
- `list_api_keys` — List active keys with usage stats
- `revoke_api_key` — Permanently revoke an API key

## Behavior

When the user asks to manage brands, members, styles, or API keys:

1. Use the appropriate tool from the list above
2. For destructive actions (delete brand, remove member, revoke key), confirm with the user before proceeding
3. When creating a brand, offer to set up default style and invite members
4. When inviting members, share the invite URL with the user
