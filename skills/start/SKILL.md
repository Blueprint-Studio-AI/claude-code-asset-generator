---
name: start
description: Guided first run for Blueprint Studio. Says what it does and the user's real free allowance, offers three starters, then makes, saves and links a first image from one pick. Use right after the plugin is installed or connected, when the user runs start, asks what Blueprint Studio can do or how to get started, asks what images or visual assets you can make for them, or wants a first image and hasn't made one with Blueprint Studio yet.
---

# Start

Take a new user from "just installed" to a first image with one pick. This is a welcome, not a tour: keep every step short.

1. **Read the account.** Call `get_workspace_context` once, without `brandId`. If the Blueprint connection isn't signed in yet, tell the user to open `/mcp`, authenticate Blueprint Studio (`asset-generator`), and run this again.
2. **Two lines, real numbers.** First line: Blueprint Studio makes images for their product or brand (hero images, icons, social posts) and saves each one to their Blueprint library. Second line: their plan and allowance from `account` and `defaultImage`, for example "You're on Free: 20 credits a month, and a default image costs 3, so about 6 images." Quote only returned numbers. Credits are weighted, so never say one image is one credit. If `gettingStarted.nextStep` says a default image isn't affordable, show `plansUrl` and when credits reset, and stop.
3. **Three starters, one pick.** Offer exactly three, plus "or describe yours in one line". Use `gettingStarted.suggestedUserPrompts` when present: they are Blueprint's own starters, the same ones as its setup page. Otherwise offer a hero image for their website, an app icon and a social post, naming the product when this project's README or package manifest makes it obvious. Ask one multiple-choice question with the host's question tool when it has one; otherwise print a numbered list and wait.
4. **Make it now.** After the pick, ask nothing else. Call `generate_asset` with the starter (or their line) as `prompt`, a fresh UUID `requestId`, and `aspectRatio` only when the starter implies one (16:9 for a hero, 1:1 for an icon or post). Leave `brandId`, `styleId`, `modelId`, `imageSize` and `quality` unset, so it is the default image in their personal library. Poll `get_generation_status` with the returned `jobId` until `completed` or `failed`. If they picked brand setup, follow the brand-setup steps in `gettingStarted` and the `brand-manager` skill instead, then offer a first image with the new brand.
5. **Deliver it** as the `asset-generator` skill's Delivery section says: look at the preview, save the file into the project (the requested path, `.blueprint.json` `outputDir`, else `./assets/`), give the saved path, the `webUrl` and the `libraryUrl`, say what it cost, and offer to open it.
6. **One next step.** Offer a variation, or setting up their brand from their website so later images match it.

On `GENERATION_LIMIT`, `MODEL_NOT_ENTITLED` or `API_REQUEST_LIMIT`, follow [the MCP contract](../asset-generator/references/mcp-contract.md): show `plansUrl`, keep the request and pause. Never start another generation because a request or a poll timed out.
