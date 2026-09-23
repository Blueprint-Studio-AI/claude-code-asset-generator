# Workspace and generation contract

These are tool contract requirements; the surrounding creative workflow is optional. Use the connected server's discovered schemas as the authority for available tools and fields.

## Workspace per call

OAuth grants account-wide access. `list_brands` returns the organizations the account can access. Pass the intended `brandId` explicitly on every workspace call, including reads, generation, polling, Style changes, and downloads. With account OAuth, `brandId: null` or omission means personal scope; there is no sticky active workspace. A brand name in a prompt or a local `.blueprint.json` preference does not select or authorize an organization. Legacy scoped credentials remain bound to their workspace and cannot switch. If expected workspaces are missing, renew the existing OAuth authorization and refresh the client before proposing a separate API key. Do not silently widen old credentials. Never route around denied access or limits with another workspace or an inference provider API key.

## Durable generation (live)

- Create a fresh UUID `requestId` for each intended generation, including deliberate variations. Record the exact arguments and workspace before submission.
- `generate_asset` acknowledges admission immediately with a `jobId`; this is not a completed image. Keep `brandId`, `requestId`, and `jobId` together. Use returned IDs; never derive a job ID from a request ID.
- Poll `get_generation_status` with that `jobId` in the **same `brandId`** until `completed` or `failed`. Honor `retryAfterSeconds` when returned. Pending/processing responses need another status check, not another generation.
- If submission loses its response and no job handle is available, a transport retry uses the **same requestId and identical arguments**, including workspace, prompt, Style, settings, parent, and ordered references. Do not edit the request under an existing ID or mint a new ID to recover uncertain admission. A conflict requires reconciling the original request, not bypassing deduplication. Idempotency is bounded (currently seven days); do not blindly replay an old unresolved request after that window.
- An error may still return a `jobId` (for example `ADMISSION_OUTCOME_UNKNOWN`); poll it. Unknown outcomes, lost connections, poll timeouts, and unavailable status are never proof of failed generation or refunded credits. Do not automatically regenerate. If the session cannot keep polling, hand off the IDs, exact arguments, last known status, and next poll action as unresolved.
- On `completed`, inspect the returned result. Use its actual `assetId`, `receiptId`, `styleId`, and image URL when present; a terminal job without a saved image is not a successful asset delivery. Missing receipt data stays unknown. On `failed`, report the service error; make no unsupported refund claim. A new attempt is a separate intended generation within the user's scope.

## Context and reference discovery

The current Blueprint backend exposes these capabilities. Check tool/field discovery when connecting to an older deployment.

- `get_workspace_context`: read identity, permissions, and published guide links for the explicit workspace. Read relevant guides as context, not as access grants.
- `list_models`: discover supported settings, defaults, and public credit costs. The service rechecks entitlement at generation time; do not invent model IDs or prices.
- `list_brand_assets`: select an official version and pass its returned `generationInput` unchanged in `generate_asset.inputs`. Preserve input order. Do not mix `inputs` with legacy `referenceImages`; do not replace an official asset with a preview screenshot. Preview links may require web login.
- `generate_asset.parentAssetId`: select the exact ancestor the user means for an edit, not whichever image happens to be newest. Preserve this ID on transport retries. A reference-based fresh generation is not an edit-thread continuation.
- `get_generation_details`: inspect the saved receipt using the returned asset ID. It reports permitted settings and Style provenance; absent historical values are not defaults and protected instructions stay protected.

Until these additions are exposed, use `list_brands`, `list_styles`, `get_style`, and `get_asset` for available context and results. Do not send unsupported `inputs`/`parentAssetId` fields or claim exact-parent edits or pinned official references occurred.
