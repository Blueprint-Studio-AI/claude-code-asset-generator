# Prompts and inputs

How to brief one image well. The tool schemas list every field; this page says which ones matter and when.

## The prompt

- **Say what goes where.** Subject first, then composition, then what the image must leave room for: "a ceramic mug on a wooden table, mug on the right third, plain warm wall on the left for a headline".
- **Name the slot, not the screen.** A hero behind a headline needs a quiet area; an app icon needs one bold shape that reads at 32 px.
- **With a Style, describe the subject only.** The Style carries the treatment (palette, light, materials, line). Repeating it in the prompt fights it.
- **Exact text is fragile.** Short words render well. For a headline, a price or legal text, make the image without it and set the text in code.
- **An edit names one change.** "Make the background deep navy" with `parentAssetId`, not the whole brief again.

## Size, shape and quality

| Want | Pass |
|---|---|
| The default, good for most uses | leave `imageSize` out (2K) |
| A hero, print, a large banner | `imageSize: "4K"` |
| Quick drafts or many variations | `imageSize: "1K"` or `quality: "low"` |
| A square post or icon | `aspectRatio: "1:1"` |
| A website hero or slide | `aspectRatio: "16:9"` |
| A story or phone screen | `aspectRatio: "9:16"` |

An edit keeps its parent's size unless you pass one. `get_workspace_context` returns `defaultImage` (what a default image costs where you'll work) and `list_models` returns every model's price by size and quality. Quote those numbers; never assume one credit per image. Logos, references and the image being edited add no credits.

Measured, 28 Sep to 18 Oct 2026: 1:1 was 32% of images and 16:9 16%. Since 15 Oct, 32% were 2K and 53% were 1K drafts.

## Models

Leave `modelId` out: the default suits most images. Agents sent `modelId` on 96% of calls, and 87% of those named the default anyway (28 Sep to 16 Oct 2026). Pick another model only when the user asks, or when `list_models` says one does something the default can't.

## Transparent backgrounds

For sprites, icons, stickers and product cut-outs, pass `background: "transparent"`. The result's `background` field says how it was made. To cut out an image already in the library, call `remove_background` with its `assetId` and a fresh UUID `operationId`; reuse that `operationId` only to retry or check the same removal. `ALREADY_TRANSPARENT` and `NOTHING_TO_REMOVE` mean use the image as it is. `NO_SUBJECT_FOUND` means try an image with one clear subject, or generate one with `background: "transparent"`; the credit comes back.

## Inputs

`inputs` is an ordered list. Keep the order you mean, and the same order on a retry.

| You have | Pass |
|---|---|
| An official logo or product image | its `generationInput` from `list_brand_assets`, unchanged |
| A public https PNG, JPEG or WebP | `{kind: "url", url}` |
| A saved image | its `imageUrl` as a url input, or `parentAssetId` to edit it |
| A file attached in the chat or on disk | `{kind: "upload", uploadId}` from `create_upload_link` |

Uploads:

- **With a shell and the file on this machine:** `create_upload_link` with `direct: true`, run the returned `upload.curl` with the file's path, then use `upload.uploadId`.
- **Otherwise:** give the user the link's `pageUrl` to drop the file on, then call `get_upload_link` for the ready file's `uploadId`.
- Uploads work for 24 hours, in the workspace the link was made for.

A reference makes a new image that borrows from it. An edit (`parentAssetId`) continues that exact image. Pick the one the user means.

## Project preferences

A `.blueprint.json` in the project can set an output folder and preferred settings. It grants no access, and the user's words win over it.
