# Production brief

For a set made to a brief: an output folder, a credit budget, and a handoff someone else can resume.

## Before starting

- **Keep to the brief.** Its workspace, its output folder and its budget. Don't widen it into brand administration or publishing.
- **Resolve the workspace.** No `brandId` means the personal library. If `get_workspace_context` returns `library.defaultBrandId` (the user's only brand), use it unless told otherwise. Pass the same `brandId` on every call, checks included.
- **Pick a Style per item.** In a brand, pass the `styleId` that fits each item; with none, an image gets no Style. `isBrandDefault` in `list_styles` is only a suggestion.
- **Budget in credits, not images.** Credits are weighted by model, size and quality. Price the set from `defaultImage` or `list_models` before starting, and keep it inside the budget.

## Resuming earlier jobs

A brief can hand over job ids from an earlier session. Check them with `get_generation_status` (`jobIds`, `waitSeconds: 20`) in their original workspace before starting anything new. A job that timed out earlier may have finished. If all you have is a set's `requestId` and its exact arguments, sending that identical call again returns its jobs without charging again.

## Checking the work

View each output's preview at the size and place it will be used. Check composition, lettering, the logo, cropping, and how it sits with its neighbours in the set. Keep the stronger version of anything you revise.

## Handing off

Return, for the person or the next session:

- each saved file path with its image's `webUrl`;
- the `assetId` and `styleId` of every accepted image;
- what you saw: strengths, weak items, anything that needs a human eye;
- every unfinished job: its `jobId`, `brandId`, the set's `requestId`, exact arguments, last status and the next check to make.
