---
name: start
description: Router and guided first run for Blueprint Studio Asset Generator. Use right after install or connecting, when the user runs start, asks what Blueprint Studio can do or how to get started, asks what images you can make, or wants a first image and has none yet. Routes other jobs to asset-generator, asset-sets, brand-setup, official-logos or styles.
---

# Start

Take a new user from "just connected" to a first image, and send every other job to the right place.

**The rule: one question at most, then make something.**

## Numbers

Measured on Blueprint Studio's MCP server, 28 Sep to 18 Oct 2026.

- About one session in six read the account and ended with no image tried (16%, 3 to 16 Oct). Offering three starters in the same turn fixes that.
- A first image takes about 20 seconds once started: median 20 s, 90th percentile 41 s.
- Three in four sessions start by reading the account. That one call has everything a welcome needs.

## Route by what the user wants

| The user wants | Use |
|---|---|
| One image, an edit, or a real image for a page | the `asset-generator` skill |
| Several images that match: an icon set, a series, one campaign in several sizes | the `asset-sets` skill |
| Their brand saved from their website or a few images | the `brand-setup` skill |
| Their logo in an image, or logos added or labelled | the `official-logos` skill |
| A look they can reuse across many images | the `styles` skill |

If the user asks for Blueprint Studio or Asset Generator by name, use it for that request. Don't silently swap in another tool.

## First run

1. **Read the account.** Call `get_workspace_context` once, without `brandId`. Pass `pluginVersion: "2.11.1"` (this plugin's release) so it can say when a newer plugin is out. If the tools aren't signed in, use the host's sign-in for Blueprint Studio. In Claude Code, run `/mcp`, pick `plugin:blueprint-studio:asset-generator` and choose Authenticate. Carry on once `get_workspace_context` answers.
2. **Two lines, real numbers.** Line one: Asset Generator makes images for their product or brand (hero images, icons, social posts) and saves each one to their library. Line two: their plan and balance, from `account.creditSummary` and `defaultImage`. For example: "You're on Free with {credits left} welcome credits (one-time, until {date}), and a default image costs {defaultImage credits}." Fill in only numbers the call returned. Credits are weighted, so never say one image is one credit.
3. **Three starters, one pick.** Offer exactly three, plus "or describe yours in one line". Use `gettingStarted.suggestedUserPrompts` when present; if they pick the brand one, follow the `brand-setup` skill and offer a first image in the new brand after. Otherwise offer a hero image for their website, an app icon and a social post, naming the product when the project's README makes it obvious. Ask once, with the host's question tool if it has one.
4. **Make it.** Call `generate_asset` with the pick as `prompt` (drop a lead-in like "Use Blueprint Studio Asset Generator to"), a fresh UUID `requestId`, and `aspectRatio` only when the starter implies one (16:9 for a hero, 1:1 for an icon or post). Leave `modelId`, `imageSize` and `quality` out: a first image is the 2K default, even a hero. If `library.defaultBrandId` is set (their only brand), pass it as `brandId`, with the `styleId` from `list_styles` that fits. Then call `get_generation_status` with the `jobId` and `waitSeconds: 20` until it is `completed` or `failed`.
5. **Deliver it** as the `asset-generator` skill's Delivery section says: show it, save it into the project, give the path and the `webUrl`, and say what it cost.
6. **One next step.** Offer a variation, or setting up their brand from their website so later images match.

## Known failures

- **Reading and leaving.** The account call alone isn't a welcome. Offer the starters in the same turn.
- **Can't afford a first image.** When `gettingStarted.nextStep` or `canAffordImage` says so, show `nextStep` and hand the person `plansUrl`, where they can compare plans and pay. Offer to open it in their browser and open it only if they say yes. Then stop. Don't retry.
- **A timed-out check.** It doesn't mean the image failed. Call `get_generation_status` again with the same `jobId`. Never start another generation because a request or a check timed out: that charges twice.
- **A newer plugin.** If the answer has `pluginUpdate`, tell the user once, in one sentence, with its `nextStep`, then carry on.

## Limits

- It makes one first image. A set goes to the `asset-sets` skill.
- It doesn't save a brand itself; the `brand-setup` skill does, when they pick it or after the first image.
- It is a welcome, not a tour: no feature lists.
