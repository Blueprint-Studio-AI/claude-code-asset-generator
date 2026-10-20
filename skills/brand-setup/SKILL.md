---
name: brand-setup
description: Sets up the user's brand in Blueprint Studio from their website or a few images they like, saved as a brand and a Style with their logo. Use when the user wants to set up their brand, make images match their site, or capture their brand colors, fonts and look. For adding or labelling logos use official-logos; for another Style in a saved brand use styles.
---

# Brand setup

From a website or a few images to a saved brand that every later image can use.

**The rule: save only what the person approved.** Show the draft and previews, ask what to change, then save.

## Numbers

Measured on Blueprint Studio's MCP server.

- Setups took a median 92 s from start to save when made from images, and 158 s from a website (1 Sep to 18 Oct 2026; a small sample, mostly our own tests).
- After setup, images land in the brand only when the call says so: 1.3% of generations passed a `brandId` and 0.7% a saved Style (28 Sep to 16 Oct 2026).
- The previews come from the account's free setup previews and use no credits.

## Steps

1. **Start it.** `setup_brand` with `website` (or 1 to 5 `imageUrls` of work in the look they want), plus `brandName` and `description` if they gave them, and a fresh UUID `requestId`. It answers at once with a `setupId`.
2. **Wait for the draft.** `get_brand_setup` with the `setupId` and `waitSeconds: 20`, again until `ready` or `failed`.
3. **Show it and ask.** The name, the logo found on the site, the palette with where each color came from, the fonts, the descriptors and the previews. Ask one question: what should change?
4. **Save what they approved.** `save_brand_setup` with the `setupId` and only the edits they asked for: `brandName`, `styleName`, `palette`, `fonts`, `descriptors`, `referenceIndexes`. Pass `logo: false` if the logo it found is wrong. Saving again returns the first save.
5. **Use it.** Every later image passes the returned `brandId` and `styleId`. Offer one image in the new Style straight away.
6. **Offer the rest of the logos.** Setup saves the logo it found on the site (a brand that already has logos keeps them). White versions, wordmarks and marks go in with the `official-logos` skill, or on the web.

## Known failures

- **Social pages can't be read.** Instagram, Facebook, TikTok and Linktree pages fail. Ask for 2 or 3 images of their posts, products or logo and pass them as `imageUrls`.
- **Saving before the person looked.** When it's their only brand, a saved brand is where their images go by default. Show the previews first.
- **The wrong logo from the site** (a favicon, a share image, a partner's logo). Save with `logo: false` and add the right file with the `official-logos` skill.
- **Forgetting the brand afterwards.** Without `brandId` and `styleId`, the next image goes to the personal library with no Style.
- **Another setup while two are running** returns `SETUP_IN_PROGRESS`. Check the running one with `get_brand_setup` instead of starting over.
- **A failed setup.** Show its `nextStep`. A website that blocks readers often works as 2 or 3 images instead.
- **Free previews used up.** Setup still drafts the brand and Style; it skips the previews.

## Limits

- It reads the website once, when asked. It doesn't keep the brand in sync with the site.
- Up to 2 setups running at once and 10 started per day. A draft expires after 7 days.
- One Style per setup. More Styles for the same brand: the `styles` skill.
- Teammates, roles and API keys: [Team and keys](references/team-and-keys.md).
