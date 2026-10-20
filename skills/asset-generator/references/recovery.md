# Jobs and recovery

What to do when something didn't go to plan: sign-in, retries, timeouts, limits and unfinished jobs.

## Sign-in

Use the host's sign-in for Blueprint Studio when it has one, and open the fresh link in the same turn when it can. Sign-in attempts are short-lived: when resuming an earlier one, start a new attempt instead of reopening an old link. Never log callback codes or put them in files. If authentication tools are unavailable, direct Claude Code users to `/mcp` → `plugin:blueprint-studio:asset-generator` (Blueprint Studio) → Authenticate. The tools are connected once `get_workspace_context` answers.

If brands the user expects are missing, have them disconnect and connect again, then start a new chat.

## Which workspace

No `brandId` means the personal library, and the last brand used isn't remembered. Pass the same `brandId` on every call for that work: the start, the checks, downloads and Style changes. A brand's name in a prompt doesn't select it.

## Starting and retrying

- A fresh UUID `requestId` for each image you mean to make, variations included.
- `generate_asset` answers at once with a `jobId`. That is a job, not an image.
- A set of images (`images`) needs one `requestId` for the call; a set without one is refused.
- If the start's answer is lost or timed out and you have no `jobId`, resend the same `requestId` with identical arguments. For a set, that returns the jobs already started, even while the first call is still running. Never edit a request under an old `requestId` or mint a new one to recover. A conflict means the first request needs reconciling, not bypassing.
- An error can still carry a `jobId` (for example `ADMISSION_OUTCOME_UNKNOWN`). Check it.

## Checking

- `get_generation_status` with the `jobId` (or all of a set's `jobIds` in one call) and `waitSeconds: 20`. It answers as soon as the jobs finish. Honour `retryAfterSeconds` when it's there.
- Still running means check again the same way, not start another.
- A timed-out request or check is never proof that the job failed or that credits came back. A new request starts a second image and charges again.

## When a job fails

A failed job's credits are refunded automatically, and `nextStep` says how to retry with a new `requestId`. For a safety filter refusal, it also says how to reword. Report the reason; claim no refund the answer doesn't state.

## Limits and plans

- **Credit limit** (`GENERATION_LIMIT`, `MODEL_NOT_ENTITLED`, or `canAffordImage` false): show `nextStep` and hand the person `plansUrl`: people compare plans before paying, and the plans page is where they buy. If an answer ever carries `checkoutUrl` (a one-step checkout for Pro, valid 7 days), mention it after `plansUrl`, not instead of it. In a terminal, offer to open the link in their browser and open it only if they say yes. Then pause until they say the plan or credits changed, and check with `get_asset_generator_usage`. Don't retry.
- **Daily request limit** (`API_REQUEST_LIMIT`): wait until its `resetAt`. Don't retry before then.
- **Free credits don't reset.** Free's welcome credits are one-time and end on a date (`account.welcomeCredits` has how many and when). More come from a plan.
- **`PLAN_REQUIRED`:** API keys and the REST API are on Pro and Max. Signing in to the MCP works on every plan. Show `nextStep` and `plansUrl`, and don't retry with the key.
- Treat `checkoutUrl` like a share link: never write it into files, commits or logs.

## When the session must stop

Hand off what the next session needs: each unfinished `jobId` with its `brandId` and `requestId`, the exact arguments, the last status, and the next check to make. Never start a replacement image for a job you couldn't finish checking.
