---
name: official-logos
description: Finds, adds, labels and places the user's official logos in Blueprint Studio. Use when an image should carry their logo, when they share a logo file or link to save, or when logos need labels such as primary, wordmark, or for dark backgrounds. For setting up a brand from a website use brand-setup; for a new logo concept use asset-generator.
---

# Official logos

The brand's real logo files: find the right one, put it in the image, keep the set labelled.

**The rule: a logo is used as supplied, never redrawn.** It goes into the image as its official file, never as words in a prompt or a stand-in drawing.

## Numbers

Measured in Blueprint Studio, October 2026.

- 80% of saved logos carry `form` and `background` labels, but about two brands in three have no logo marked `primary`. So choose by form and background, and offer to mark one primary.
- Before 6 Oct, a brand with no logos answered with an empty list and agents drew stand-in logos. Now the answer carries `officialLogos: 0` and a `nextStep`.

## Find and choose

1. `list_brand_assets` with the `brandId`, `kind: "logo"` and `previews: true`. It returns the logos and one numbered logo sheet; each number is that logo's `sheetNumber`. A light logo sits on a dark swatch that isn't part of the file.
2. Choose one: the `primary` logo first, then the `form` that fits the space (a `mark` for small or square spots, a `wordmark` or `lockup` for wide ones), then the version whose `background` matches the image (a white logo on dark, a dark logo on light). One logo per image unless asked.

## Place it

1. Pass its `generationInput` unchanged in `generate_asset` `inputs`, with any other inputs in the order you mean.
2. Say in the prompt where it goes and how big: "small, top left, with clear space around it".
3. Look at the result. A completed job lists `officialAssetsUsed`: name it to the user ("used the white wordmark").
4. For exact lettering on a flat layout (a banner with a headline, a slide), make the image without the logo and place the original file in code.

## Add, label and replace (owners and admins)

- **Add:** `add_brand_asset` with one source: `url` (a public https link, or a saved image's `imageUrl`), `assetId` (a saved image in that brand), `uploadId` (from `create_upload_link`), or `dataUrl` for a small file. Give it a `name`, a short `variant` ("White wordmark, for dark backgrounds"), `form`, `background`, `primary` if it's the main one, and a fresh UUID `requestId`. Use the returned `asset.generationInput`.
- **Label:** `update_brand_asset` with the `assetId` and `form`, `background` or `primary`. When the variants already say it ("White · brandmark"), offer to label them all.
- **Replace:** `add_brand_asset` with `replaceAssetId` and its `revision` as `expectedRevision`. Every later image uses the new version, so confirm first. Earlier versions are kept.

## Known failures

- **No logos yet** (`officialLogos: 0`). Don't draw one. Ask for the file or a link and add it, or make the image without a logo.
- **A member tries to add one.** Only owners and admins can. The refusal names who can (`askOneOf`); suggest the user ask one of them.
- **The wrong version for the background.** A dark logo on a dark photo disappears. Check `background` before choosing.
- **The logo comes out distorted.** Make one edit that names the defect, or place the original file in code.
- **A preview or screenshot used as the logo.** Use the `generationInput`, never a sheet crop or a preview link.
- **SVG files** are saved as PNG. That is expected.

## Limits

- It doesn't design logos. A new logo concept is the `asset-generator` skill.
- Brand guide pages and official files are separate. Adding a logo doesn't update a guide.
- One logo per image unless the user asks for more.
