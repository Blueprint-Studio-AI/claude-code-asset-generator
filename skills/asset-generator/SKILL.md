---
name: asset-generator
description: Makes, edits and delivers one image or visual asset with Blueprint Studio Asset Generator. Use for an icon, illustration, banner, social post, hero or product image, mockup, logo concept, or a real image for a placeholder in code, and to edit or reuse a saved image. For several matching images use asset-sets; to put the user's own logo in an image use official-logos.
---

# Asset Generator

One image, made, checked and delivered.

**The rule: an edit is the saved image plus one change, never a new prompt.** Pass the exact image as `parentAssetId` and say only what changes.

If the user asks for Blueprint Studio or Asset Generator by name, use it for that request. Don't silently swap in another tool.

## Numbers

Measured on Blueprint Studio's MCP server, 28 Sep to 18 Oct 2026.

- 16% of finished images were edits of a saved image, and 34% of new images used reference inputs.
- An image takes a median 20 s from start to saved (90th percentile 41 s). At 2K: median 24 s. At 4K: median 31 s.
- With `waitSeconds: 20` on every check, a job needed 1.13 checks on average (at most 3). With no wait it needed 1.68, and up to 22 (28 Sep to 16 Oct).
- Since 15 Oct, 32% of images were the default size (2K) and 53% were 1K drafts. Prices change, so quote `defaultImage` and `list_models` rather than a number from here.
- 0.6% of image attempts failed, and half of those were the image model's safety filter.

## Steps

1. **Read the account once.** `get_workspace_context`, at the start of the session. Pass `pluginVersion: "2.11.1"` (this plugin's release) so it can say when a newer plugin is out. If `library.defaultBrandId` is set (their only brand), work in it unless they ask for their personal library. With several brands, use the one they name. Pass that `brandId` on every call, checks included.
2. **Pick the look.** In a brand, call `list_styles` and pass the `styleId` that fits. With no `styleId` an image gets no Style; writing the Style's name in the prompt doesn't apply it.
3. **Write the prompt.** Subject, composition, and where any text or logo goes. Set `aspectRatio` from the slot. Leave `imageSize` out for 2K; 4K for heroes and print, 1K or `quality: "low"` for drafts. Leave `modelId` out unless the user names one.
4. **Add inputs.** Official logos come from the `official-logos` skill. A public image link is `{kind: "url", url}`. A file in the chat or on disk goes through one `create_upload_link`, then `{kind: "upload", uploadId}`. Never base64. Depth: [Prompts and inputs](references/prompts-and-inputs.md).
5. **Start it.** `generate_asset` with a fresh UUID `requestId` returns a `jobId` at once. For an edit, add `parentAssetId`.
6. **Wait for it.** `get_generation_status` with the `jobId` and `waitSeconds: 20`, again the same way until `completed` or `failed`.
7. **Look before you deliver.** View the preview the finished check returned (for a saved image you haven't seen, `download_asset` with `preview: true`). Check lettering, the logo, cropping and the space it has to fit. If one thing is wrong, make one edit that names it.
8. **Deliver.** See Delivery below.

## Delivery

- **Show it.** Where the host shows Blueprint Studio's image board in the chat, don't repeat the image as Markdown. Elsewhere, show `imageUrl` as a Markdown image.
- **Save it into the project** unless the user said not to: their path, else `.blueprint.json` `outputDir`, else `./assets/`, with the real file extension. With a shell, run `download_asset`'s `saveCommand` there (one `curl`, one permission prompt). On Claude.ai, give the person `downloadUrl`.
- **Say where it is and what it cost:** the saved path, the `webUrl`, and the credits used. Name the logo in `officialAssetsUsed` if there was one.

With opening and sharing: [Delivery in detail](references/delivery.md).

## Known failures

- **Polling at zero wait:** one image in 13 calls. Pass `waitSeconds: 20` on every check.
- **Regenerating after a timeout.** A timed-out request or check doesn't mean the job failed, and a new request is a second, separately charged image. Check the same `jobId` again. Reuse a `requestId` only to resend the identical request.
- **The upload dance:** three upload links before one image. Make one link. With a shell and the file on disk, pass `direct: true`, run its `upload.curl`, and use its `upload.uploadId`; no `get_upload_link` needed.
- **Downloading to look, or asking for base64.** On Claude.ai, 62 of 76 `download_asset` calls asked for base64 (28 Sep to 16 Oct), and agents downloaded images they had just made to look at them. Look with the check's preview; hand over the file as `downloadUrl` or `saveCommand`. Ask for base64 only when the image must be embedded in code.
- **Bad reference links** were the most common external error: `INVALID_REFERENCE_IMAGE` and `REFERENCE_URL_UNREACHABLE`. Links must be public https PNG, JPEG or WebP. Upload anything else.
- **Safety filter refusals.** The job fails and is refunded; `nextStep` says how to reword. Retry with a new `requestId`.
- **The credit limit.** On `GENERATION_LIMIT` or `canAffordImage` false, show `nextStep` and hand the person `plansUrl`. Don't retry; pause until they say the plan or credits changed.
- **A re-roll is not a fix.** Running the same prompt again rarely moves the defect. Name it in an edit.

More on jobs, retries, sign-in and limits: [Jobs and recovery](references/recovery.md).

## Limits

- One image per request. For several images in one look, use the `asset-sets` skill.
- Plain shapes, gradients and text are better as CSS or SVG in code.
- It doesn't redraw the user's logo; the `official-logos` skill places the real one.
- It doesn't save brands or Styles. See the `brand-setup` skill and the `styles` skill.
