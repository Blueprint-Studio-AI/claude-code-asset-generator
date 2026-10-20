---
name: asset-sets
description: Makes many matching images in one batch with Blueprint Studio Asset Generator, such as an icon set, a series of illustrations, one campaign in several sizes, or one image per item in a list. Use when the user asks for a set of, one for each, all our, or several images in one look. For a single image use asset-generator; to build the shared look first use styles.
---

# Asset sets

Many images, one look, one wait.

**The rule: N images is one wait, not N waits.** Start every image before you check any, then check them together.

## Numbers

Measured on Blueprint Studio's MCP server, 28 Sep to 18 Oct 2026.

- Sets are the main job: 87% of images were made on days when the person made 5 or more.
- Ten or more images started within a minute of each other finished in a median 62 s, start to last image. Waiting on each in turn would have taken a median 273 s. For 4 to 9 images: 45 s against 117 s.
- Those agents still started images one call at a time, 32 s apart from first to last for a set of 10 or more. One call removes that gap.
- The best hand-made set was 17 images in 35 calls, about 2 calls per image. One image at a time costs a median 3 to 4 calls per image, depending on the app (28 Sep to 16 Oct).

## Steps

1. **Plan, for free.** Write the list: one line per image with its subject, `aspectRatio` and size. Choose the one look they share: a `styleId` from `list_styles`, or build one with the `styles` skill. Two different looks are two sets.
2. **Price it and ask.** Multiply the per-image cost (`defaultImage` from `get_workspace_context`, or `list_models` for other sizes) by the count, and compare it with the balance: "12 images will use about 36 credits; you have 140." For more than four images, wait for a yes.
3. **Start them all in one call.** `generate_asset` with `images`: 1 to 20 entries, each with its own `prompt` and any setting it doesn't share. Settings at the top level (`styleId`, `aspectRatio`, `imageSize`, `inputs`) apply to every image unless an entry sets its own. Always pass one fresh UUID `requestId` for the set: a batch without one is refused. `maxCredits` caps what the call may spend. The answer has `jobIds` for the check, `jobs` in the order of `images` (each with `index`, `jobId`, `status` and `credits`), `creditsCharged` and `creditsRemaining`. For more than 20, send the rest in another call with its own `requestId` straight away, before any check.
4. **Check them together.** Call `get_generation_status` once with all the answer's `jobIds` (up to 20) and `waitSeconds: 20`. It answers when all are done, or lists `unfinishedJobIds` to check again the same way. Never start these images again because a check timed out. Match images by `jobId`: a check's `index` and contact-sheet numbers count positions in the `jobIds` you sent.
5. **Look at the whole set.** Line the previews up, or read the numbered contact sheet. Fix an outlier with an edit (`parentAssetId` and the one change). Don't remake the set.
6. **Deliver.** Save them with names that sort together (`icon-home.png`, `icon-search.png`), then list each path with its `webUrl`, and the total credits used. Delivery details are in the `asset-generator` skill's Delivery section.

For a brief with an output folder and a budget, or a set someone else will pick up: [Production brief](references/production-brief.md).

## Known failures

- **One image per call.** Agents ran `generate_asset` up to 52 times in a row (28 Sep to 16 Oct). Put the images in one call.
- **One check per job.** Pass every `jobId` in one check.
- **One bad entry.** A set starts all or nothing: if one image can't start (a bad link, a setting the model can't take, a missing Style), none start, nothing is charged, and the error names `images[n]`. Fix that entry and send the set again with a fresh `requestId`.
- **`IDEMPOTENCY_CONFLICT`.** That `requestId` already started images. Send the original call again, unchanged, to get their `jobIds`, then start only what's missing under a new `requestId`. Resending everything under a new key charges twice.
- **Short of credits.** Nothing starts. Show `nextStep` and hand the person `plansUrl`, or offer a smaller set. Don't resend the same set.
- **Over `maxCredits`** (`MAX_CREDITS_EXCEEDED`). Nothing starts. Tell the person the total, then send fewer or cheaper images, or the same set with a higher `maxCredits` if they agree.
- **An image that didn't start, or failed later.** The others are running and paid for. If its entry carries a `jobId`, check that first. Otherwise remake only that image, with a new `requestId`; a failed job's credits come back on their own.
- **A timed-out or lost start.** Send the identical call again with the same `requestId`. It returns the jobs the first call started, even if that call is still running, and charges nothing again. A new `requestId` starts and charges every image a second time.
- **A timed-out check.** It doesn't mean the set failed. Check the same `jobIds` (or `unfinishedJobIds`) again. Never start these images again.
- **`BATCH_PREPARATION_TIMEOUT`.** The set wasn't ready to start within 40 s, so nothing started or was charged. Send the same call again with the same `requestId`, or split it into smaller sets.
- **`BATCH_REFERENCES_TOO_LARGE`.** A set's reference images share a 120 MiB cap. Send fewer images per call, or smaller references.
- **A blended set.** Images that need different treatments in one set come out matching neither. Split them.
- **The logo written into every prompt.** Pass the official logo's `generationInput` in the shared `inputs` (see the `official-logos` skill).

## Limits

- Up to 20 images per call and 20 jobs per check.
- One shared look per set. Building that look is the `styles` skill.
- For one image, use the `asset-generator` skill.
