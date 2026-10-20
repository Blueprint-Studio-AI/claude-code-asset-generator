# Distribution and releases

The canonical package is this repository. The historical repository name and marketplace URL are retained so existing installations keep working.

## One source for every platform

Edit shared content here once. Do not maintain copies of skills or generation logic for each host.

| Authored source | Used by |
| --- | --- |
| `plugin.json` | Canonical name, release version, license, description, OpenAI presentation, and the MCP Registry one-liner |
| `mcp.json` | Canonical remote MCP connection (`type` and `url`); its `X-Blueprint-Plugin` version header is generated |
| `skills/` | Shared workflows: each skill's `SKILL.md`, its `references/`, and `evals/evals.json` try-it prompts. The hosted server also returns the Markdown as how-to guides (`get_guide` and MCP resources) for hosts without the plugin. There are no agents: hosts other than Claude Code ignore them, so their content lives in skill references |
| Hosted Blueprint API | All tools, permissions, brand data, and generation behavior |

`scripts/sync_distribution.py` generates `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.mcp.json`, and `server.json` from these, and writes the version into `mcp.json`'s header and the skills' `pluginVersion` sentence. Commit the generated files so hosts can install directly from Git. OpenAI and Cursor support the root Agent Plugins format; a separate Cursor source copy is unnecessary.

Backend and permission services live in the private monorepo; this public repository contains packaging and optional guidance only. Do not add tokens, production fixtures, client-private notes, or internal source links.

## Change once

1. Edit `skills/` for workflow changes. Keep each `SKILL.md` short (the rule, steps, measured numbers with dates, known failures, limits), put depth in its `references/`, and never link into another skill's folder; name the sibling skill instead. Tool implementations live in the hosted service, not in platform adapters.
2. Bump `version` in root `plugin.json` for every package release. Shared metadata and OpenAI presentation are authored there, and the MCP Registry's 100-character one-liner lives under `extensions.io.modelcontextprotocol.registry.description`; connection changes belong in `mcp.json`.
3. Run `python3 scripts/sync_distribution.py`. Commit the generated compatibility files and registry metadata with the source change. It sets the `X-Blueprint-Plugin: blueprint-studio/<version>` header in `mcp.json` (current Codex and other Agent Plugins hosts) and the release in the `pluginVersion` sentence of the `start` and `asset-generator` skills, which ask the agent to pass it to `get_workspace_context`. `.mcp.json` (Claude Code, older Codex) stays exactly as it was before 2.10.0: type and URL, no header, nothing that changes between releases. Claude Code keeps each sign-in under a hash of that server config, so 2.10.0 and 2.10.1, which sent the header there, made every Claude Code user sign in again after updating. Codex keys sign-ins on the server name and URL only, so the header is safe in `mcp.json`. `server.json` leaves it out: the Registry lists the server for every client, not only this plugin.
4. Run local checks below. Validate real installation/OAuth in each host whose behavior changed. Schema checks do not prove host compatibility.
5. Merge a reviewed release and update the appropriate vendor listing. An accepted directory submission and a Git merge are different events.
6. If `skills/` changed, the hosted server's guides change only when its copy is regenerated from the released commit and deployed; until then `get_guide` serves the previous release's text.
7. The hosted server compares each connection's release (the header, else the `pluginVersion` passed to `get_workspace_context`) with the release it pins (its `MCP_SERVER_VERSION` and guide copy). Once that deploys, `get_workspace_context` tells users of an older plugin to update (`pluginUpdate`): once per session when the plugin says its release, and at most once a day when a Claude Code plugin connection says nothing. That is a release before 2.10.0, such as a copy synced from Claude's Directory that can't update until the Directory has the new release, unless the connection has passed `pluginVersion` before. So merge the release here before the server that pins it deploys, or users are told to update to a version they can't get yet.

The old `claude-code-marketplace` repository only needs changes when adding/removing a plugin or changing where it lives. Its Blueprint entry does not pin a release version. Its separate Conch entry is unrelated and must be preserved. Neither a skills change nor a new Blueprint release should require editing that catalog.

## Package formats

| Consumer | Files / release channel |
| --- | --- |
| OpenAI ChatGPT/Codex | Portable `plugin.json`, `skills/`, `mcp.json`; `extensions.com.openai` presentation. Official shared directory uses a reviewed submission with the remote MCP endpoint and skills. |
| Older Codex installations | Generated `.codex-plugin/plugin.json` and `.mcp.json`, referencing the same shared skills. |
| Claude Code/Cowork | Generated `.claude-plugin/plugin.json` and `.mcp.json`; same skills. Direct marketplace install or separate official plugin review. |
| Cursor | Portable root package; no duplicated Cursor skill tree. Official marketplace review is separate. Do not claim a tested host until it has been exercised. |
| Claude chat connector | Same HTTPS MCP endpoint and OAuth; separate connector-directory review, no cloned backend. |
| MCP Registry | Generated `server.json`; existing explicitly triggered OIDC publication workflow. |
| GitHub/VS Code discovery | Curated listing of the same remote server; inclusion in another registry does not guarantee inclusion here. |

Official references: [Agent Plugins](https://agent-plugins.org/), [OpenAI packaging](https://developers.openai.com/plugins/build/plugins), [Claude format](https://code.claude.com/docs/en/plugins-reference), [Cursor format](https://cursor.com/docs/reference/plugins), [MCP Registry](https://modelcontextprotocol.io/registry/remote-servers).

## Local checks

```sh
python3 scripts/sync_distribution.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
claude plugin validate .
git diff --check
```

Run official-schema validation of root `plugin.json`, `mcp.json`, and `server.json`, plus the Codex plugin-creator `validate_plugin.py` and skill-creator `quick_validate.py` on each `skills/*` directory when available, before publication. Validation requires no generation calls or credentials. Keep CI local. The GitHub OIDC workflow is a publication step only; it is not the test runner.

The sync checker fails on metadata drift, license mismatch, unsupported transports, or credential-bearing connection configuration: a header whose name looks like a credential (`Authorization`, cookies, tokens, keys, secrets, sessions) or any header other than the generated version header is refused. The tests also fail if Claude Code's `.mcp.json` would change between releases. It performs no network calls, installs nothing, and changes no host settings.

For a clean committed release, a submission archive can be created without local configuration or build files:

```sh
git archive --format=zip --output=/tmp/blueprint-studio-plugin.zip HEAD \
  plugin.json mcp.json .claude-plugin/plugin.json .codex-plugin/plugin.json \
  .mcp.json skills LICENSE README.md docs
```

Inspect archive contents before uploading. Keep release icons under `assets/` and explicitly include that directory when added. Never archive the private monorepo or a working-directory wildcard. No credentials, developer environment files, or client fixtures belong in the package.

## Review boundaries

One source does not make marketplace releases atomic: each vendor may approve different versions at different times. Track the submitted and published version for each destination. Do not programmatically attest to policy compliance merely because validation passes.

Existing users receive workflow changes through their host's plugin update mechanism. Server fixes are deployed once to the shared service. Tool-definition changes still follow each host's refresh/review rules; preserve backward compatibility for clients with older cached definitions.

License: MIT for these public files. The private service remains separately licensed. Registry metadata is public CC0 data. Validate paid-service and upgrade-link behavior against each vendor's current publishing policies before submitting.
