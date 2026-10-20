# Team and keys

Inviting people to a brand, changing roles, and API keys for scripts. Do these only when the user asks; never as part of setup.

## Roles

- **Owner:** everything, including changing roles.
- **Admin:** invite and remove members, add and label official logos, change brand settings.
- **Member:** make images and Styles in the brand, and edit the Styles they made.
- **View-only member:** see the brand's images, Styles and logos, but not make images or Styles there. The owner can give create access with `update_member_role`.

`get_workspace_context` with the `brandId` returns the user's role (`brand.roleHelp`, `brand.canManage`). Offer only what that role allows. When a member asks for something an admin must do, the refusal names who can (`askOneOf`): suggest asking one of them.

## Members and invites

- `invite_member` sends an email invite to one address, or makes a shareable link (`type: "link"`) with optional `maxUses` and `expiresInDays`.
- A member link with neither limit works until revoked. An admin link works once within 7 days unless you pass `evergreen: true`; confirm that first, since anyone holding it can manage the brand.
- `list_members` shows members and pending invites. `list_invites` shows pending invites and active links with their `inviteUrl`; `revoke_invite` cancels one.
- `update_member_role` (owners only) changes a role. `remove_member` removes someone.
- Treat invite links as private: anyone with one can join.
- Each person uses their own credits. Plans are per person, not shared by the brand.

## API keys

- API keys are for scripts and automations. They need Pro or Max, or Pro access from extra credits or the brand. Signing in to the MCP works on every plan. On Free, `create_api_key` answers `PLAN_REQUIRED`: show its `nextStep` and `plansUrl`.
- `create_api_key` binds the key to that call's `brandId` (personal when left out). A key works only in its own workspace and can't create keys for another.
- A key made here stops working when the AI app that made it is disconnected. For a key that lasts, the user creates one under API Keys in Settings.
- `list_api_keys` and `revoke_api_key` manage them.
- Never save a key in project files, config or reports. No OpenAI or Google key is needed.
