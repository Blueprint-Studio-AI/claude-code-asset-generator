---
name: styles
description: Builds reusable Styles in Blueprint Studio by testing drafts side by side on the same prompts. Use when the user wants a consistent look across assets, a Style from references or a description, to grow a brand's Style library, to compare Style candidates or to try variations of a Style. For making the matching set itself use asset-sets; for a whole brand from a website use brand-setup.
---

# Styles

A Style is a saved look: palette, light, materials, line and texture. Every image made with its `styleId` shares it. A Style made from reference images is images only unless you add text; a Style with no references needs text.

**The rule: keep the draft the person picks most, side by side on three different prompts.** One good image is not a Style.

## Numbers

Measured on Blueprint Studio's MCP server, 28 Sep to 16 Oct 2026.

- A saved Style was passed on 0.7% of generations. Agents sent `styleId: "freestyle"` (no Style) 19 times as often. A Style named only in the prompt isn't applied.
- The same Style, model and settings can still give different results run to run. That is why one image proves nothing.

On 25 Styles run through the production generation path, 12 to 13 Nov 2026:

- With images only, the reference's subject leaked into 42% of images and text was printed in 32%. With each analysis model's text added: 54 to 64%, and up to 46%.
- One score, the match to the look, favoured the text. So test it: one draft images only, one with text.

## Steps

No `start_style_trial` among your tools (search for it first if tools load on demand)? Skip to Without the trial tools, below.

1. **Read what's there.** `list_styles` in the workspace, with the same `brandId` on every call; `list_styles` with `drafts: true` lists drafts already made. `get_style` on the nearest ones shows their references and text in full. Look at the user's references; they go in `inputs` in the same forms as for `generate_asset` (a link, an upload or a saved image).
2. **Split the look from the layout.** The treatment (palette, light, materials, line, texture) goes in the drafts. Subject and placement (what's shown, where the empty space is) go in each prompt.
3. **Plan 2 to 6 drafts that differ from the first in one thing each.** Each is a `variants` entry with a short `label` and one of:
   - `inputs`: reference images (images only), plus `stylePrompt` to add text;
   - `stylePrompt` alone: a Style from a description;
   - `fromStyleId`: a copy of a Style's references and text. `keepReferences` keeps some of them, by `get_style`'s `position` + 1 (position 0 is 1); `inputs` adds new ones after those, or replaces them all without `keepReferences`. `stylePrompt` replaces the text, or `imagesOnly: true` drops it (not both);
   - `styleId`: a draft already made.

   To improve a Style, pass it as `baseStyleId` and make the first draft an unchanged copy (`fromStyleId` alone), so the others have something to beat.
4. **Write three prompts.** One close to the references and two with new subjects or compositions, each with its placement.
5. **Price it and ask.** A trial runs at 1K, medium quality, square, on their preset model, and every prompt runs the same way, so set `aspectRatio` (16:9 for blog headers), `imageSize`, `quality` or `modelId` now when the Style is for something else. Call `start_style_trial` with a fresh UUID `requestId`, a `name`, the `variants`, the `prompts`, those settings and `estimateOnly: true`. Nothing is made or charged. Tell the person `credits.total` for its `images` count on its `model`, and wait for a yes.
6. **Run it.** The same call, with the same `requestId` (the estimate recorded nothing), without `estimateOnly` and with `maxCredits` set to that total. Keep the `trialId`.
7. **Show the grid.** `get_style_trial` with the `trialId` and `waitSeconds: 20`, again the same way while any cell is `queued` or `processing`. Look at the `contactSheet` yourself: rows are prompts (P1, P2…), columns are drafts in `variants` order (A, B…). Then show the person each row's images, labelled like the tiles (P1·A), as the host shows images: each cell's `imageUrl` as a Markdown image, or its `webUrl`. Ask which they like best in each row. Each draft's references and text are in the answer if they want to see what's behind a letter.
8. **Record each pick.** `pick_style_trial_image` with the `trialId`, the row's `promptId` and the chosen cell's `variantId` (or the `trialId` and the cell's `assetId`), one call per prompt. Picking again for a prompt replaces its pick. The answer has the `tally` and the `leader`.
9. **Run more prompts when it's close.** With no `leader` (a tie) or a lead of one pick, offer one to three more prompts. Each costs one image per draft at the estimate's `perImage` credits. With no estimate at hand, get one: `start_style_trial` with a fresh `requestId`, `estimateOnly: true`, the trial's drafts as `{ styleId }` variants, the new prompts, and the trial's `settings` passed as `aspectRatio`, `imageSize`, `quality` and `modelId`. Say the total and wait for a yes. Then `run_style_trial_prompts` with the `trialId`, a fresh `requestId`, the `prompts` and `maxCredits` set to that total, and steps 7 and 8 for the new rows. Over 20 cells, read one row at a time with `promptId`. Still tied after that: ask them to choose between the tied drafts.
10. **Keep the winner.** Ask which draft to keep (usually the `leader`) and what happens to the rest, then `finish_style_trial` with the `trialId`, `keep` (that `variantId`), `as` and `others`:
    - `as: "new_style"` saves it as a new Style. Always pass `name`, or it's named from its label;
    - `as: "update_base"` writes it into the trial's `baseStyleId` Style, and every later image made with that Style changes. Ask first, naming the Style, even when they said to keep the better one;
    - `others`: `"drafts"` (the default: left in Drafts), `"archive"` (tossed; `restore_style` brings one back) or `"save"` (each becomes a Style too).

    If the unchanged copy wins, the Style already does best: say so, and finish only if they'd rather keep one of the others. Otherwise leave the trial open, and toss its drafts with `archive_style` if they agree.
11. **Report.** The kept `styleId` (pass it to `generate_asset`; its cover is being made), the tally, the `assetId`s of the winning images, what the others got wrong, and the credits used. If the library uses categories, `update_style` gives it a `category` and `description`.

For hero images, cards and anything that must sit inside a page: [Placement composition](references/placement-composition.md). To judge drafts or a trial someone else ran: [Reviewing Style candidates](references/reviewing-candidates.md).

## Drafts

- `list_styles` with `drafts: true` lists the drafts not tossed, and every row says `draft`. `archived: true` lists what's archived, tossed drafts included.
- A draft works by its `styleId` like any Style (`generate_asset`, `get_style`, `set_style_thumbnail`), but it stays out of the usual lists and can't be a default.
- Toss a draft with `archive_style`; `restore_style` un-tosses it, still a draft. `delete_style` deletes one for good.
- `update_style` with `draft: false` saves a draft as a Style without a trial. To try a change to a saved Style by hand, make a draft from it: `create_style` with `fromStyleId` and `draft: true`.

## Without the trial tools

Run the same loop by hand, with the `asset-sets` skill's batch steps and failures.

- Make each draft with `create_style`: `draft: true` and `fromStyleId` if it takes them; otherwise the source's references as `inputs` and its text as `stylePrompt`, named "(draft)", archived after if they lose.
- Give every image the same settings: `imageSize: "1K"`, `quality: "medium"` where the model offers it, one `aspectRatio`.
- Add up the credits (`list_models`, plus on the GPT models each draft's `imagesSent` from `list_styles` with `drafts: true`), say the total and wait for a yes.
- Start every prompt for every draft in one `generate_asset` call (up to 20 images, each with its draft's `styleId`) with a fresh `requestId` and `maxCredits`, check them in one `get_generation_status`, and show the images as its answer says.
- Ask which they like for each prompt and keep the tally yourself. Keep the winner as its own Style (`update_style` with `draft: false` for a draft) and ask about the rest. Change the original instead only when they ask, with `update_style`.

## Known failures

- **Running before saying the total.** Price every trial and every extra prompt first, and run only after a yes, with `maxCredits` set to the total.
- **The Style named in the prompt only.** Pass the `styleId`. Writing its name or pasting its text doesn't link the image to it.
- **Layout baked into a draft.** "Subject on the right, empty left side" in a Style makes every image empty on the left. Keep placement in each prompt.
- **Overwriting a shared Style to experiment.** Others' images change with it. Make drafts from it (`fromStyleId`), and use `update_base` only when the person chooses it.
- **Several things changed in one draft.** Then a win doesn't say what helped. Change one thing per draft against the first.
- **Judging on one prompt.** Results vary run to run. Three prompts at least.
- **Picking for the person.** Record only the picks they made. If they ask you to choose, say which and why, and record it once they agree.
- **Over `maxCredits` (`MAX_CREDITS_EXCEEDED`).** Nothing ran or was charged. Tell the person `creditsRequired`; with a yes, send the same call again, same `requestId`, with `maxCredits` at that total. A start picks up the trial the first call made, if it made one.
- **Too big a round.** Over 20 images in a call (with 6 drafts, 3 prompts at most) or `BATCH_REFERENCES_TOO_LARGE` (the round's references share 120 MiB): nothing ran. Send fewer prompts, with a new `requestId`; if the answer has a `trialId`, as `run_style_trial_prompts` on it. `BATCH_PREPARATION_TIMEOUT`: send the same call again with the same `requestId`.
- **Short of credits.** Nothing ran. Show `nextStep` and pause until the person says their plan or credits changed. Don't resend the same trial.
- **A timed-out or lost start or run.** Send the identical call again with the same `requestId`: it returns what the first one started and charges nothing again. A new `requestId` runs and charges every image a second time.
- **`IDEMPOTENCY_CONFLICT`.** That `requestId` already ran. Send the first call again unchanged to get its `trialId` and prompts. Never resend a trial under a new `requestId`: that charges it twice.
- **A timed-out read.** It doesn't mean the trial failed. Call `get_style_trial` again. Never run the prompts again because a read timed out.
- **A failed cell.** Its credits come back on their own. Ask for a pick among the rest. Running the prompt again runs every draft on it as a new row: quote that whole row first.
- **Finishing twice.** A finished trial can't be finished again. Change the kept Style with `update_style`, or start a new trial from it.
- **Relabelling old images.** Images made with no Style stay that way after you save a Style. Generate new examples with the `styleId`.

## Limits

- A trial has 1 to 6 drafts. `start_style_trial` runs 0 to 4 prompts (none makes the drafts only) and `run_style_trial_prompts` 1 to 4, at most 20 images per call. Every prompt runs with the trial's model, size, quality and aspect ratio.
- A Style or draft keeps up to 5 reference images. One with no references needs text.
- A draft can't be a default; save it first. Changing a brand's default Style is for owners and admins.
- Members with create access can make drafts, run trials and pick in a brand; view-only members can only read them. A trial's drafts live where the trial does.
- Subjects, Templates, Mockups and the other kinds aren't trialled. A Style with a type (`list_context_types`) can be a draft's source, but `update_base` replaces its text, which takes its type off: say so first. Change a typed Style's `fields` or `notes` with `expectedUpdatedAt` from `get_style`; on a conflict, read it again and retry once.
- Making the full matching set is the `asset-sets` skill.
