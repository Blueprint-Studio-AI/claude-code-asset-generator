# Reviewing Style candidates

For judging drafts, Styles or a trial someone already ran, or running a small comparison when the user asks for one.

## Judge what's there

- Review the images you were given, or a trial's grid: `get_style_trial` with the `trialId` they give you returns the `contactSheet`, every cell, and each draft's references and text in full. Run more prompts only if the user asked for them, and say what they cost and wait for a yes first.
- Keep the treatment separate from the subject and the placement when you judge. A strong layout can hide a weak Style.
- Base every finding on images you actually viewed.

## For each draft, note

- **Fidelity:** does it match the references and the brand?
- **Range:** does it hold on different subjects, or only on the prompt closest to its references?
- **Leaks:** did a reference's subject, or text from the references or the Style, turn up where the prompt didn't ask for it?
- **Lettering and logos:** accurate, or garbled?
- **Use:** would it work in its real slot, at its real size?
- **Failures:** what broke, and on which prompt.

## Reading the tally

- A pick is the person's favourite for one prompt, and the tally counts picks per draft. `leader` is null on a tie or before any pick.
- A lead of one pick is weak. Say so, and offer one to three more prompts, priced first, before the trial is finished.
- A draft that wins only on the prompt closest to its references has shown fidelity, not range.
- Your own read is advice. Record only the person's picks.

## Running a comparison

- Use the workspace the user named, and pass its `brandId` on every call.
- Make the candidates drafts in one trial (`start_style_trial`, or by hand where it isn't offered), not edits to a shared Style. Every prompt runs with the same settings; let each draft differ from the first in one thing.
- Say the credit total (from `estimateOnly: true`, or added up by hand where the trial tools aren't offered) and wait for a yes before anything runs, even within a budget the user set. Run with `maxCredits` set to that total.
- A review doesn't permit finishing the trial, writing into a shared Style (`update_base`) or publishing anything. Leave the drafts in Drafts unless the user says otherwise.

## Report

A short comparison: the tally, what each draft does well, where it fails, the `variantId` and `styleId` of the one you'd keep and the `assetId`s of its best images, and any cell still running (the `trialId` and the next check).
