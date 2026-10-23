# HumanPost MCP and agent plugins

Official integration package for [HumanPost](https://humanpost.com): manage social accounts, prepare video and image drafts, queue approved content, and inspect human posting status and analytics from an AI assistant.

HumanPost operates a hosted MCP service. This repository contains client configuration and a publishing skill; it does not contain the hosted server implementation. A HumanPost account, company access, and a scoped API key are required. Service usage and some actions may incur charges under your HumanPost plan.

## Connect

- Transport: **Streamable HTTP**
- Endpoint: `https://us-central1-clickbaitcarousel.cloudfunctions.net/mcp`
- Authentication: `Authorization: Bearer YOUR_HUMANPOST_API_KEY`
- [Setup and tools](https://humanpost.com/docs/mcp) · [API reference](https://humanpost.com/docs/api) · [Complete agent documentation](https://humanpost.com/llms.txt)

Create a key under **Dashboard → Settings → API & MCP**. Start with `accounts:read` and add only the scopes your workflow needs. Each key belongs to one company. Store it in your client's secret configuration; never commit it or paste it into a conversation. The service uses API keys today, not OAuth. No credential is included in this package.

### Cursor

Configure `HUMANPOST_API_KEY` in the plugin's Configure panel when installing the Cursor plugin. For manual installation, put this entry in your Cursor MCP settings and make the environment variable available to Cursor:

```json
{
  "mcpServers": {
    "humanpost": {
      "url": "https://us-central1-clickbaitcarousel.cloudfunctions.net/mcp",
      "headers": { "Authorization": "Bearer ${env:HUMANPOST_API_KEY}" }
    }
  }
}
```

### Claude Code

Add this repository as a marketplace, then install the plugin:

```text
/plugin marketplace add HumanPost-co/humanpost-mcp
/plugin install humanpost@humanpost
```

Set `HUMANPOST_API_KEY` in the process environment before launching Claude Code. Alternatively, use the `.mcp.json` entry in your project. Claude Code and the Claude web connector directory have different requirements; this plugin does not make the remote server OAuth-compatible.

### Grok Build / Grokbot

Grok Build supports Claude-compatible plugins. Add the repository using its plugin marketplace command:

```sh
grok plugin marketplace add HumanPost-co/humanpost-mcp
```

Install `humanpost` from the Marketplace tab and supply `HUMANPOST_API_KEY` in the client environment. The package includes both `.grok-plugin/plugin.json` and `.claude-plugin/plugin.json`. Review the configured MCP before enabling it. Official marketplace inclusion is separate from adding this publisher's marketplace.

### Muse Code

Merge the `mcp_servers.humanpost` entry from [config-muse.json](config-muse.json) into your Muse Code settings. It uses Muse's documented `streamable_http` transport and `${HUMANPOST_API_KEY}` environment interpolation. Install the publishing skill with:

```sh
muse skills install ./skills/humanpost-publishing --scope user
```

Muse Code configuration is separate from listing a connector in the consumer Muse directory. No consumer directory approval is claimed.

### Agent Skills / skills.sh / OpenClaw

```sh
npx skills add HumanPost-co/humanpost-mcp --skill humanpost-publishing
```

The skill uses a connected MCP or the documented REST API on hosts that can make HTTP requests. It cannot supply network or shell capabilities that the host does not have. Installing the skill does not configure credentials or grant company access.

### ChatGPT and Codex

The root `plugin.json` uses the portable Agent Plugins format, with OpenAI listing metadata. The public ChatGPT remote-MCP portal currently requires an authentication flow supported by the portal. HumanPost's API-key-only MCP cannot complete that flow today. Do not submit it as an unauthenticated connector or embed a key in the package. A hosted OAuth integration, domain verification, test account, and review walkthrough are required before public remote-MCP submission.

## Typical workflow

1. Call `get_context` to check company and scopes, then `list_accounts` to select the correct account.
2. Inspect accounts, posting queues, drafts, or analytics using the discovered tools.
3. Upload media and prepare a draft for review. Request an actual preview when needed.
4. Queue content only within the user's authorization. Preserve idempotency keys and returned operation IDs on retries.
5. Inspect the resulting post/task status. Queued and pending-approval states are not confirmed publication.

Tools are filtered by key scopes. Account provisioning, task creation, rendering, posting, schedule changes, and cancellations may cause external effects or consume credits. Do not auto-approve every tool. Availability and schemas come from live tool discovery; see the public documentation for details and limitations.

## Security and network access

The MCP config sends your key only to `us-central1-clickbaitcarousel.cloudfunctions.net/mcp`, HumanPost's Firebase-hosted service. The REST fallback uses the same host under `/publishingApi`. Documentation links go to `humanpost.com`. Uploads may use service-issued signed storage URLs; never send the API key to those URLs. The package has no lifecycle hooks, background processes, telemetry, dependency installers, or remote-code execution.

For a read-only health check without a key, `python3 scripts/check_endpoint.py` verifies that the public endpoint rejects unauthenticated initialization. An authenticated connection test is available in the HumanPost dashboard. A successful unauthenticated check does not validate every tool or company workflow.

## Privacy and support

The hosted service processes account, content, task, and analytics data for the company authorized by your key. See the [HumanPost Privacy Policy](https://humanpost.com/privacy-policy) and [Terms of Service](https://humanpost.com/terms-of-service). Contact [support@humanpost.co](mailto:support@humanpost.co) or [open an integration issue](https://github.com/HumanPost-co/humanpost-mcp/issues). Never include credentials or private customer content in a public issue.

The integration package is MIT licensed. The hosted HumanPost service and HumanPost branding are not licensed by that grant. Platform compatibility configurations and a submission do not imply marketplace endorsement or approval.
