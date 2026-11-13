---
name: styles
description: Builds reusable Styles in Blueprint Studio by testing drafts side by side on the same prompts. Use when the user wants a consistent look across assets, a Style from references or a description, to grow a brand's Style library, to compare Style candidates or to try variations of a Style. For making the matching set itself use asset-sets; for a whole brand from a website use brand-setup.
---

# Styles

A Style is a saved look: palette, light, materials, line and texture. Every image made with its `styleId` shares it. A Style made from reference images is images only unless you add text; a Style with no references needs text.

**The rule: try the drafts side by side on three different prompts, and keep the one the person chooses.** Their picks inform the choice; the tally doesn't make it. One good image is not a Style.

## Numbers

Measured on Blueprint Studio's MCP server, 28 Sep to 16 Oct 2026.

- A saved Style was passed on 0.7% of generations. Agents sent `styleId: "freestyle"` (no Style) 19 times as often. A Style named only in the prompt isn't applied.
- The same Style, model and settings can still give different results run to run. That is why one image proves nothing.

On 25 Styles run through the production generation path, 12 to 13 Nov 2026:

- With images only, the reference's subject leaked into 42% of images and text was printed in 32%. With each analysis model's text added, the subject leaked into 54 to 64% and text was printed in up to 46%.
- One score, the match to the look, favoured one analysis model's text. So test it: one draft images only, one with text.

## Steps

No `start_style_trial` among your tools (search for it first if tools load on demand)? Skip to Without the trial tools, below.

1. **Read what's there.** `list_styles` in the workspace, with the same `brandId` on every call; `list_styles` with `drafts: true` lists drafts already made. `get_style` on the nearest ones shows their references and text in full. Look at the user's references; they go in `inputs` in the same forms as for `generate_asset` (a link, an upload or a saved image).
2. **Split the look from the layout.** The treatment (palette, light, materials, line, texture) goes in the drafts. Subject and placement (what's shown, where the empty space is) go in each prompt.
3. **Plan 2 to 5 drafts that differ from the first in one thing each.** A trial holds 6, so one stays free for an idea mid-trial. Drafts whose references come from the same five pictures converge: when they're to differ in their references, find references first (the `find-references` skill), one direction per draft. Each is a `variants` entry with a short `label` and one of:
   - `inputs`: reference images (images only), plus `stylePrompt` to add text;
   - `stylePrompt` alone: a Style from a description;
   - `fromStyleId`: a copy of a Style's references and text. `keepReferences` keeps some of them, by the `number` `get_style` gives each reference (its `position` + 1); `inputs` adds new ones after those, or replaces them all without `keepReferences` (5 in all at most). `stylePrompt` replaces the text, or `imagesOnly: true` drops it (not both);
   - `styleId`: a draft already made.

   To improve a Style, pass it as `baseStyleId` and make the first draft an unchanged copy (`fromStyleId` alone), so the others have something to beat.
4. **Write three prompts.** One close to the references and two with new subjects or compositions, each with its placement.
5. **Price it and ask.** A trial runs at 1K, medium quality, square, on their preset model, and every prompt runs the same way, so set `aspectRatio` (16:9 for blog headers), `imageSize`, `quality` or `modelId` now when the Style is for something else. Call `start_style_trial` with a fresh UUID `requestId`, a `name`, the `baseStyleId` when improving a Style, the `variants`, the `prompts`, those settings and `estimateOnly: true`. Nothing is made or charged. Tell the person `credits.total` for its `images` count on its `model`, and wait for a yes.
6. **Run it.** The same call, with the same `requestId` (the estimate recorded nothing), without `estimateOnly` and with `maxCredits` set to that total. If anything changed since the estimate, estimate again first. Keep the `trialId`.
7. **Show the grid.** `get_style_trial` with the `trialId` and `waitSeconds: 20`, again the same way while any cell is `queued` or `processing`. Look at the `contactSheet` yourself: rows are prompts (P1, P2…), columns are drafts in `variants` order (A, B…). Then show the person each row's images, labelled like the tiles (P1·A), as the host shows images: each cell's `imageUrl` as a Markdown image, or its `webUrl`. Ask which they like best in each row. The contact sheet holds 20 tiles at most, the latest rows; pass `promptId` for an older row's. Each draft's `references` (with links) and `stylePrompt` are in the answer if they want to see what's behind a letter.
8. **Record each pick.** `pick_style_trial_image` with the `trialId`, the row's `promptId` and the chosen cell's `variantId` (or the `trialId` and the cell's `assetId`), one call per prompt. Picking again for a prompt replaces its pick. The answer has the `tally` and the `leader` (the most picks; null on a tie). Each `tally` entry is a draft's `picks` out of its `prompts`, the prompts it has an image in, so say it that way: "B 3 of 4, E 1 of 1". A draft that joined late has had fewer chances, not a worse record.
9. **Run more prompts when it's close.** With no `leader` (a tie), a lead of one pick, or a draft with fewer prompts doing as well per prompt (E 1 of 1 beside B 3 of 4), offer one to three more prompts. Each costs `perPrompt` credits (one image in every draft), as `get_style_trial` and `pick_style_trial_image` answer. Say the total and wait for a yes. Then `run_style_trial_prompts` with the `trialId`, a fresh `requestId`, the `prompts` and `maxCredits` set to that total, and steps 7 and 8 for the new rows. Still tied, or a lead of one, after that: ask them to choose between the leading drafts.
10. **Add a draft for a new idea.** When the person has a new idea mid-trial ("try it warmer"), every draft fails the same way, or a tie looks like a different set of references might break it, offer one more draft in this trial, not a new trial. `add_style_trial_draft` takes the `trialId`, a `requestId` and one `variant` (step 3's fields); the draft gets the next letter and runs in every later round.
    - Estimate first: the call with a fresh `requestId`, `estimateOnly: true`, and `rerunPrompts: true` once prompts have run. It makes nothing.
    - Refused because the trial has 6 drafts, its most: ask which to drop, and tell them what the refusal's `nextStep` says to do and anything it says about that draft's images and picks. Once they agree, do it, then the estimate again with a fresh `requestId`.
    - Priced, before any prompt has run: it costs nothing now; go on to No rerun. Otherwise tell the person `credits.total` for its `images` (the earlier prompts run for the new draft alone), and that without the rerun the draft joins from the next prompt and costs nothing now. Either way each later prompt has one more image. Wait for their choice.
    - The rerun: the same call with the same `requestId` (the estimate recorded nothing), without `estimateOnly` and with `maxCredits` set to that total; if anything changed since the estimate, estimate again first. Then step 7 for the earlier rows: show each with the new letter's image and ask whether it changes their pick, and step 8 for any that does.
    - No rerun: the call with a fresh `requestId` and `rerunPrompts` left out. To run the earlier prompts for it later, send this same call again with the same `requestId` and `rerunPrompts: true` (priced first, as its `nextStep` says); a new `requestId` would add a second draft.
    - Either way every later prompt has one more image (`variant.creditsPerImage`): quote the next round from a fresh `get_style_trial`'s `perPrompt`.
    - No `add_style_trial_draft` among your tools, even after searching for it? Offer a new trial with the current drafts as `{ styleId }` variants plus the new one, the same `baseStyleId` and the trial's `settings`, priced first.
11. **Keep the winner.** The tally informs; the person decides. Ask which draft to keep (usually the `leader`), whether it becomes a new Style or goes into the base (when the trial has one: name it and say every later image made with it changes), and what happens to the rest, then `finish_style_trial` with the `trialId`, `keep` (that `variantId`), `as` and `others`:
    - `as: "new_style"` saves it as a new Style. Always pass a `name` (ask, or suggest one);
    - `as: "update_base"` (no `name`) writes it into the trial's `baseStyleId` Style, and every later image made with that Style changes. First check that `get_style_trial`'s `baseStyleId` is the Style they mean (the id `list_styles` gives the name they used); if it isn't, take the no-base route below. Ask first, naming the Style and saying every later image made with it changes, unless they asked for that Style by name to be changed ("update Product Shots with B"); "keep the better one" or "the base" isn't that. Send it without `confirmUpdateBase`;
    - `others`: `"drafts"` (the default: left in Drafts), `"archive"` (tossed; `restore_style` brings one back) or `"save"` (each becomes a Style too).

    `UPDATE_BASE_NEEDS_CONFIRMATION` means someone else makes images with the base Style, or it's a default, and nothing changed. Tell the person what its `error` says (who else uses it, or whose default it is) and that every later image made with it changes, for everyone who uses it. Ask even if they chose `update_base` already: they hadn't heard this. After a yes, send the same finish with `confirmUpdateBase: true`; on a no, offer `as: "new_style"`. A Style that only they make images with, and that isn't a default, needs no confirmation.

    `TRIAL_NO_BASE`, or a base that isn't the Style they named: nothing changed. Say which Style the trial started from (none or one since deleted, as `TRIAL_NO_BASE` says, or another), and offer `as: "new_style"` with a name, or writing it into the Style they named by hand (`update_style`, as in Without the trial tools). That changes it for everyone who uses it, so ask first, naming it, even when they named it. After a write by hand the trial stays open: ask about tossing its drafts (`archive_style`).

    If the unchanged copy wins, the Style already does best: say so, and finish only if they'd rather keep one of the others. Otherwise leave the trial open, and toss its drafts with `archive_style` if they agree.
12. **Report.** The kept `styleId` (pass it to `generate_asset`), the tally as picks out of prompts, the `assetId`s of the winning images, what the others got wrong, and the credits used. A new Style gets a cover made, and so does a base whose cover was a reference it lost; otherwise after `update_base` the old cover stays, so offer `set_style_thumbnail` with one of its new references. If the library uses categories, `update_style` gives it a `category` and `description` (they don't change its images).

For hero images, cards and anything that must sit inside a page: [Placement composition](references/placement-composition.md). To judge drafts or a trial someone else ran: [Reviewing Style candidates](references/reviewing-candidates.md).

## Drafts

- `list_styles` with `drafts: true` lists the drafts not tossed, and every row says `draft`. `archived: true` lists what's archived, tossed drafts included.
- A draft works by its `styleId` like any Style (`generate_asset`, `get_style`, `set_style_thumbnail`), but it stays out of the usual lists and can't be a default.
- Toss a draft with `archive_style`; `restore_style` un-tosses it, still a draft. `delete_style` deletes one for good.
- `update_style` with `draft: false` saves a draft as a Style without a trial. To try a change to a saved Style by hand, make a draft from it: `create_style` with `fromStyleId` and `draft: true`.

## Without the trial tools

For a host that doesn't have them yet: a connection made before they were added, or one that hasn't loaded them. Run the same loop by hand, with the `asset-sets` skill's batch steps and failures.

- Make each draft with `create_style`: `draft: true` and `fromStyleId` where `create_style` has them; otherwise the source's references as `inputs` and its text as `stylePrompt`, named "(draft)", archived after if they lose.
- Give every image the same settings: `imageSize: "1K"`, `quality: "medium"` where the model offers it, one `aspectRatio`.
- Add up the credits (`list_models`, plus on the GPT models each draft's `imagesSent` from `list_styles`, with `drafts: true` for drafts), say the total and wait for a yes.
- Start every prompt for every draft in one `generate_asset` call (up to 20 images, each with its draft's `styleId`) with a fresh `requestId` and `maxCredits` set to that total, check them in one `get_generation_status`, and show the images as its answer says.
- Ask which they like for each prompt and keep the tally yourself, as picks out of prompts. A new idea mid-way is one more draft: price its images on the prompts already run, or let it join from the next prompt; either way each later prompt has one more image. Say the total and wait for a yes, for every extra prompt too, however few images. Keep the winner as its own Style (`update_style` with a `name` without "(draft)", and `draft: false` for a draft) and ask about the rest. Change the original instead only after they confirm it, naming it and saying that every image made with it from now on changes, for anyone who uses it: `update_style` with the winner's text (or `imagesOnly: true`) and references (`removeReferenceImages`, `addInputs`). On a typed original, new text takes its type off: say so first.

## Known failures

- **Running before saying the total.** Price every trial, every extra prompt and every rerun for an added draft first, and run only after a yes, with `maxCredits` set to the total.
- **The Style named in the prompt only.** Pass the `styleId`. Writing its name or pasting its text doesn't link the image to it.
- **Layout baked into a draft.** "Subject on the right, empty left side" in a Style makes every image empty on the left. Keep placement in each prompt.
- **Overwriting a shared Style to experiment.** Others' images change with it. Make drafts from it (`fromStyleId`), and use `update_base` only when the person chooses it. A write of text or references into a saved Style by hand (`update_style`: the no-base route, after a finish, or because a `nextStep` says so) gets no server check: ask first, naming it and saying it changes for everyone who uses it, even when they named it.
- **Confirming for the person.** `confirmUpdateBase: true` goes only on the finish sent after `UPDATE_BASE_NEEDS_CONFIRMATION`, once the person has heard what its `error` says and said yes. Never on a first finish, and never because they chose `update_base` before they knew who else uses the Style.
- **A new trial for one more idea.** It runs and charges every draft again. Add the idea to the open trial with `add_style_trial_draft` (step 10) where you have it.
- **Reading a late draft as losing.** E 1 of 1 isn't behind B 3 of 4: it has been in one prompt. Say picks out of prompts, and offer more prompts before calling it.
- **Several things changed in one draft.** Then a win doesn't say what helped. Change one thing per draft against the first.
- **Judging on one prompt.** Results vary run to run. Three prompts at least.
- **Picking for the person.** Record only the picks they made. If they ask you to choose, say which and why, and record it once they agree.
- **A refused round.** Nothing ran or was charged.
  - `MAX_CREDITS_EXCEEDED` (over `maxCredits`): tell the person `creditsRequired` and wait for a yes.
  - Short of credits: show `nextStep` and pause until they say their plan or credits changed.
  - `TOO_MANY_PROMPTS`: a round is one batch of 20 images at most, its drafts times its prompts (with 6 drafts, 3 prompts; with 5, 4). At the start, plan fewer drafts or prompts per round; mid-trial every round runs every draft, so fewer prompts. At the trial's 20 prompts, follow its `nextStep`. `BATCH_REFERENCES_TOO_LARGE` (a round's references share 120 MiB): fewer prompts. Price the smaller round (`estimateOnly: true` for a start, `perPrompt` times its prompts for a run) and run it after a yes.
  - Then, for a refused start or run: if the answer has a `trialId`, its drafts exist: run the prompts on it with `run_style_trial_prompts`, a new `requestId` and `maxCredits` set to the total they agreed to; if its drafts' references are too large even for one prompt, toss them (`archive_style`) and start a new trial with fewer or smaller ones. Otherwise nothing was made: send the start again with a new `requestId` and that `maxCredits`.
  - `BATCH_PREPARATION_TIMEOUT`: send the same call again with the same `requestId`.
  - A refused `add_style_trial_draft`: its `nextStep` says whether the draft was added. Not added: after a yes, send it again with a new `requestId` and `maxCredits` set to the total they just agreed to. Added without its rerun: follow its `nextStep`; if it offers no rerun, the draft joins from the next prompt: tell the person.
- **A timed-out or lost start, run or added draft.** Send the identical call again with the same `requestId`: it returns what the first one started and charges nothing again. A new `requestId` runs and charges every image a second time.
- **`IDEMPOTENCY_CONFLICT`.** That `requestId` already ran something else. Send that first call again unchanged to see what it made; anything new gets a new `requestId`, priced first. Never resend the same trial or round under a new `requestId`: that charges it twice.
- **A timed-out read.** It doesn't mean the trial failed. Call `get_style_trial` again. Never run the prompts again because a read timed out.
- **A failed cell.** Its credits come back on their own. Ask for a pick among the rest. Running the prompt again runs every draft on it as a new row: quote its `perPrompt`, wait for a yes, then step 9's run with `maxCredits` set to it.
- **Finishing twice.** A finished trial can't be finished again. Change the kept Style with `update_style` (asked first, as above), or start a new trial from it. A timed-out finish is different: send the identical finish again, with `confirmUpdateBase` only if the call that timed out had it. It completes one that stopped part-way and changes nothing twice; `TRIAL_FINISHED` naming the same kept Style means the first one finished. Without that call to hand, read `get_style_trial`: `status` finished with the kept Style shows it went through.
- **Relabelling old images.** Images made with no Style stay that way after you save a Style. Generate new examples with the `styleId`.

## Limits

- A trial has 1 to 6 drafts, those added later included. `start_style_trial` runs 0 to 4 prompts (none makes the drafts only) and `run_style_trial_prompts` 1 to 4, at most 20 images per call. A trial runs 20 prompts at most, so an added draft's rerun is one batch. Every prompt runs with the trial's model, size, quality and aspect ratio.
- A Style or draft keeps up to 5 reference images. One with no references needs text.
- A draft can't be a default; save it first. Changing a brand's default Style is for owners and admins.
- Members with create access can make drafts, run trials and pick in a brand; view-only members can only read them. A trial's drafts live where the trial does.
- Subjects, Templates, Mockups and the other kinds aren't trialled. A Style with a type (`list_context_types`) can be a draft's source: a copy keeps the type, and `imagesOnly` is refused on it. A draft with its own `stylePrompt` has no type, so writing that one back with `update_base` takes the base's type off: say so first. Change a typed Style's `fields` or `notes` with `expectedUpdatedAt` from `get_style`; on a conflict, read it again and retry once.
- Making the full matching set is the `asset-sets` skill.
