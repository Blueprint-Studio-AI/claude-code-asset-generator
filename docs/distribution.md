# Distribution and releases

The canonical package is this repository. The historical repository name and marketplace URL are retained so existing installations keep working.

## Change once

1. Edit `skills/` or `agents/` for workflow changes. Tool implementations live in the hosted service, not in platform adapters.
2. Bump `version` in root `plugin.json` for every package release. Shared metadata and OpenAI presentation are authored there; connection changes belong in `mcp.json`.
3. Run `python3 scripts/sync_distribution.py`. Commit the generated compatibility files and registry metadata with the source change.
4. Run local checks below. Validate real installation/OAuth in each host whose behavior changed. Schema checks do not prove host compatibility.
5. Merge a reviewed release and update the appropriate vendor listing. An accepted directory submission and a Git merge are different events.

The old `claude-code-marketplace` repository only needs changes when adding/removing a plugin or changing where it lives. Its Blueprint entry does not pin a release version. Its separate Conch entry is unrelated and must be preserved. Neither a skills change nor a new Blueprint release should require editing that catalog.

## Package formats

| Consumer | Files / release channel |
| --- | --- |
| OpenAI ChatGPT/Codex | Portable `plugin.json`, `skills/`, `mcp.json`; `extensions.com.openai` presentation. Official shared directory uses a reviewed submission with the remote MCP endpoint and skills. |
| Older Codex installations | Generated `.codex-plugin/plugin.json` and `.mcp.json`, referencing the same shared skills. |
| Claude Code/Cowork | Generated `.claude-plugin/plugin.json` and `.mcp.json`; same skills and optional agents. Direct marketplace install or separate official plugin review. |
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

Run official-schema validation of root `plugin.json`, `mcp.json`, and `server.json`, plus the Codex plugin validator and skill validators, before publication. Keep CI local. The GitHub OIDC workflow is a publication step only; it is not the test runner.

The sync checker fails on metadata drift, license mismatch, unsupported transports, or credential-bearing connection configuration. It performs no network calls, installs nothing, and changes no host settings.

For a clean committed release, a submission archive can be created without local configuration or build files:

```sh
git archive --format=zip --output=/tmp/blueprint-studio-plugin.zip HEAD \
  plugin.json mcp.json .claude-plugin/plugin.json .codex-plugin/plugin.json \
  .mcp.json skills agents LICENSE README.md docs
```

Inspect archive contents before uploading. Keep release icons under `assets/` and explicitly include that directory when added. Never archive the private monorepo or a working-directory wildcard. No credentials, developer environment files, or client fixtures belong in the package.

## Review boundaries

One source does not make marketplace releases atomic: each vendor may approve different versions at different times. Track the submitted and published version for each destination. Do not programmatically attest to policy compliance merely because validation passes.

Existing users receive workflow changes through their host's plugin update mechanism. Server fixes are deployed once to the shared service. Tool-definition changes still follow each host's refresh/review rules; preserve backward compatibility for clients with older cached definitions.

License: MIT for these public files. The private service remains separately licensed. Registry metadata is public CC0 data. Validate paid-service and upgrade-link behavior against each vendor's current publishing policies before submitting.
