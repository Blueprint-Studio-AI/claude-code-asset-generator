# Delivery in detail

What to do with each image the user keeps.

## Show it

A completed `get_generation_status` returns a small preview you can see, plus `imageUrl`, `webUrl` (the image in the user's Asset Generator library), `libraryUrl`, a full-resolution `downloadUrl` and `suggestedFilename`.

- Where the host shows Blueprint Studio's image board in the chat, the person already sees the image. Don't repeat it as a Markdown image.
- Elsewhere, show `imageUrl` as a Markdown image.
- For a saved image, `download_asset` returns `downloadUrl`, `suggestedFilename`, its width, height and `bytes`, and a `saveCommand`, with no image. Add `preview: true` for a small preview (at most 64 KB) of an image you haven't seen. Don't call it to look at an image you just made: the check already showed it.
- Ask for `includeBase64` only when the image must be embedded in code. It returns base64 only for files up to 1.5 MB; a larger file gets a `base64Refused` note and the links.

## Save it into the project

Unless the user said not to:

1. Pick the place: the path they asked for, else `.blueprint.json` `outputDir`, else `./assets/`.
2. Name it from `suggestedFilename` or a short slug of the brief, and keep the real extension. Never rename JPEG bytes to `.png`.
3. With a shell: run `download_asset`'s `saveCommand` in that folder (a ready `curl -fsSL -o "<file>" "<url>"`, one permission prompt), or `mkdir -p assets && curl -fsSL -o "assets/<file>" "<downloadUrl>"` with the links the finished check returned. Otherwise use the host's download tool. Never paste base64 into a file by hand.
4. Update the code that should use it, when that is part of the task.

On Claude.ai, or any app with no project folder, skip this and give the person `downloadUrl`.

## Say where it is

- The saved path, and always the `webUrl`.
- The `libraryUrl` the first time, for everything they have made.
- The credits it used.
- The logo, if any: name what `officialAssetsUsed` lists ("used the white wordmark"). If they wanted their logo and the list is empty, say so.

## Offer to open it

On their machine: `open <path>` on macOS, `xdg-open <path>` on Linux, `start "" <path>` on Windows. Open it when they agree or asked to see it, never in headless or CI sessions.

## Share it

Make a public link with `share_asset` only when the user asks for one. Anyone with the link can see the image. The page hides the prompt, and the user can turn links off in Settings, under Shared links.

## Hand off

Keep the `assetId` and `styleId` of accepted images with the work. If a job is still running when the session must stop, hand off its `jobId` and `brandId` so the next session can check it.
