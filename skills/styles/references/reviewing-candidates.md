# Reviewing Style candidates

For judging Styles or examples someone already made, or running a small Style comparison when the user asks for one.

## Judge what's there

- Review the examples you were given. Generate more only if the user asked for new ones.
- Keep the treatment separate from the subject and the placement when you judge. A strong layout can hide a weak Style.
- Base every finding on outputs you actually viewed.

## For each candidate, note

- **Fidelity:** does it match the references and the brand?
- **Range:** does it hold on different subjects, or only the one it was tuned on?
- **Lettering and logos:** accurate, or garbled?
- **Use:** would it work in its real slot, at its real size?
- **Failures:** what broke, and on which brief.

## Running a comparison

- Use the workspace the user named, and pass its `brandId` on every call.
- Get categories from `list_styles`, create the candidate before its examples, and generate the examples with its `styleId`.
- Keep model, size and quality fixed, and change one thing per round.
- Finish with a thumbnail (`set_style_thumbnail`) and check the examples with `list_assets` filtered by the `styleId`.
- Stay within the budget and scope the user set. A review doesn't permit overwriting a shared Style or publishing anything.

## Report

A short comparison: what each candidate does well, where it fails, the `styleId` and `assetId` of the examples you'd keep, and any job still running (its `jobId` and the next check).
