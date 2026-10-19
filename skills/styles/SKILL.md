---
name: styles
description: Builds, tests and keeps reusable Styles in Blueprint Studio so many images share one look. Use when the user wants a consistent look across assets, a Style from references or a description, to grow a brand's Style library, or to compare Style candidates. For making the matching set itself use asset-sets; for a whole brand from a website use brand-setup.
---

# Styles

A Style is a saved look: palette, light, materials, line and texture. Every image made with its `styleId` shares it.

**The rule: keep a Style only after it works on three different briefs.** One good image is not a Style.

## Numbers

Measured on Blueprint Studio's MCP server, 28 Sep to 16 Oct 2026.

- A saved Style was passed on 0.7% of generations. Agents sent `styleId: "freestyle"` (no Style) 19 times as often. A Style named only in the prompt isn't applied.
- The same Style, model and settings can still give different results run to run. That is why one image proves nothing.

## Steps

1. **Read what's there.** `list_styles` in the workspace: names, categories, thumbnails and the brand's default. `get_style` on the nearest ones. Look at the user's references.
2. **Split the look from the layout.** The treatment (palette, light, materials, line, texture) goes in the Style. Subject and placement (what's shown, where the empty space is) go in each image's prompt.
3. **Draft a candidate.** `create_style` with a clear `name`, a short `stylePrompt`, `description`, an existing `category` from `list_styles` (unless the user names a new one), and `colorPalette` and `mood` when they help. Keep the returned `styleId`.
4. **Test on three briefs.** One close to the references and two with new subjects or compositions. Keep model, size and quality the same. Start all three in one `generate_asset` call with `images`, the `styleId` and one `requestId` (see the `asset-sets` skill), then check them in one `get_generation_status` call and look at all three.
5. **Change one thing and rerun.** `update_style` with the `styleId` and the new `stylePrompt`, then the same three briefs. Keep the stronger version.
6. **Finish the entry.** `get_style` for its `updatedAt`, then `set_style_thumbnail` with the best example's `assetId` and `expectedUpdatedAt`. Check `list_assets` filtered by the `styleId` shows the examples.
7. **Report.** The examples you'd keep, what failed, and the `styleId`. If the user doesn't want the candidate, `delete_style` removes it.

For hero images, cards and anything that must sit inside a page: [Placement composition](references/placement-composition.md). To judge candidates someone else made: [Reviewing Style candidates](references/reviewing-candidates.md).

## Known failures

- **The Style named in the prompt only.** Pass the `styleId`. Writing its name or pasting its text doesn't link the image to it.
- **Layout baked into the Style.** "Subject on the right, empty left side" in the Style makes every image empty on the left. Keep placement in each prompt.
- **Overwriting a shared Style to experiment.** Others' images change with it. Make a candidate instead.
- **A thumbnail conflict.** Someone changed the Style. Read `updatedAt` again and retry once.
- **Relabelling old images.** Images made with no Style stay that way after you save a Style. Generate new examples with the `styleId`.
- **Several things changed at once.** Then you can't tell what helped. Change one variable per round.

## Limits

- `create_style` saves text: the prompt, palette and mood. It doesn't save reference images. A Style with reference images comes from the `brand-setup` skill.
- Members with create access can make Styles in a brand; view-only members can't. Changing a brand's default Style is for owners and admins.
- Making the full matching set is the `asset-sets` skill.
