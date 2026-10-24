# HumanPost MCP and agent plugins

Official integration package for [HumanPost](https://humanpost.com): request TikTok and Instagram account setup, prepare video and carousel drafts, and coordinate posting at scale through HumanPost’s human operators. Track account setup, posting progress, published links and performance from your AI assistant.

HumanPost operates a hosted MCP service. This repository contains client configuration and a publishing skill; it does not contain the hosted server implementation. A HumanPost account and company access are required. OAuth-capable clients use HumanPost sign-in; company-scoped API keys remain available for manual configurations. Service usage and some actions may incur charges under your HumanPost plan.

## Connect

- Transport: **Streamable HTTP**
- Endpoint: `https://humanpost.com/mcp`
- Authentication: OAuth 2.1 authorization code with S256 PKCE and dynamic client registration. Company-scoped API keys are also supported.
- [Setup and tools](https://humanpost.com/docs/mcp) · [API reference](https://humanpost.com/docs/api) · [Complete agent documentation](https://humanpost.com/llms.txt)

Create a key under **Dashboard → Settings → API & MCP**. Start with `accounts:read` and add only the scopes your workflow needs. Each key belongs to one company. Store it in your client's secret configuration; never commit it or paste it into a conversation. OAuth users select one company and minimum permissions in the consent screen. Writes are off by default. Access tokens expire after 15 minutes; refresh tokens rotate and expire after seven days. Revoke a connection under Settings → API Keys. No credential is included in this package.

### Cursor

The Cursor plugin uses the canonical OAuth endpoint. Install it and use Cursor’s Connect action to sign in to HumanPost. For manual setup:

```json
{
  "mcpServers": {
    "humanpost": { "url": "https://humanpost.com/mcp" }
  }
}
```

If you use a company API key instead, configure an Authorization header in your private Cursor settings with `Bearer ${env:HUMANPOST_API_KEY}`.

### Cline

Merge [config-cline.json](config-cline.json) into Cline's MCP settings. Replace `YOUR_HUMANPOST_API_KEY` in your local settings with your scoped key. Keep that settings file private. The transport value is `streamableHttp`; keep `autoApprove` empty and review tool calls. Cline CLI uses `~/.cline/data/settings/cline_mcp_settings.json` by default and supports `CLINE_MCP_SETTINGS_PATH` for an isolated configuration.

### Claude Code

Add this repository as a marketplace, then install the plugin:

```text
/plugin marketplace add HumanPost-co/humanpost-mcp
/plugin install humanpost@humanpost
```

Set `HUMANPOST_API_KEY` in the process environment before launching Claude Code. Alternatively, use the `.mcp.json` entry in your project. The compatibility `.mcp.json` uses an environment-supplied API key. For native OAuth instead, run `claude mcp add --transport http humanpost https://humanpost.com/mcp` and use Claude Code’s MCP authentication flow. Claude web directory approval is separate from installing this plugin.

### Grok Build

Grok Build supports Claude-compatible plugins. Add the repository using its plugin marketplace command:

```sh
grok plugin marketplace add HumanPost-co/humanpost-mcp
```

Install `humanpost` from the Marketplace tab and supply `HUMANPOST_API_KEY` in the client environment. The package includes both `.grok-plugin/plugin.json` and `.claude-plugin/plugin.json`. Review the configured MCP before enabling it. Official marketplace inclusion is separate from adding this publisher's marketplace.

### Grok Bot

Grok Bot has a separate [app-directory submission form](https://x.ai/bot/marketplace/submit-a-plugin), which also covers Cursor. The Grok Build CLI instructions above apply to Build; they do not install the Bot app plugin. This repository includes the Cursor marketplace manifest and the canonical OAuth MCP entry for app-directory review.

Ask your Bot to add a custom MCP server called HumanPost at `https://humanpost.com/mcp`, then use its Authorize card. In HumanPost, choose one company and the minimum scopes needed; writes are off by default. Start with `accounts:read`. Grok Bot connections are account-level, so revoke a test connection in HumanPost Settings → API Keys and remove the temporary connector when finished.

Marketplace approval is separate from adding a private custom connection. The Grok Bot-specific application was submitted and acknowledged on October 24, 2026; marketplace review is pending. No approved Bot listing is claimed.

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

The root `plugin.json` and `mcp.json` use the portable Agent Plugins format. The portable MCP entry uses the OAuth endpoint and discovers its authorization server.

For OpenAI portal upload, use **humanpost-openai-plugin-1.0.3.zip** from the [release](https://github.com/HumanPost-co/humanpost-mcp/releases/tag/v1.0.3). Its root `mcp.json` uses the documented OpenAI authentication extension from [openai/mcp.json](openai/mcp.json): OAuth with DCR and read-only default scopes. This separate bundle preserves strict portable-schema compatibility for other hosts. No client secret, access token or API key is bundled.

The endpoint is deployed and its browser consent, scope enforcement, refresh and revocation were live-tested using an isolated test company. OpenAI developer identity verification, publisher setup and marketplace review are still required. A prepared package is not an approved listing.

To reproduce a published release, check out its matching Git tag first, then build both archives with `python3 scripts/build_release.py --output-dir /tmp/humanpost-release`. Later documentation commits do not alter previously published archives.

## Typical workflow

1. Call `get_context` to check company and scopes, then `list_accounts` to select the correct account.
2. Inspect accounts, posting queues, drafts, or analytics using the discovered tools.
3. Upload media and prepare a draft for review. Request an actual preview when needed.
4. Queue content only within the user's authorization. Preserve idempotency keys and returned operation IDs on retries.
5. Inspect the resulting post/task status. Queued and pending-approval states are not confirmed publication.

The server advertises its tool catalog and enforces key scopes when each tool is called. Discovery alone does not grant permission to invoke a tool. Account provisioning, task creation, rendering, posting, schedule changes, and cancellations may cause external effects or consume credits. Do not auto-approve every tool. Availability and schemas come from live tool discovery; see the public documentation for details and limitations.

## Security and network access

OAuth clients connect to `humanpost.com/mcp` and discover authorization endpoints on the same HumanPost origin. The compatibility API-key configs send your key only to `us-central1-clickbaitcarousel.cloudfunctions.net/mcp`, HumanPost's Firebase-hosted service. The REST fallback uses the same host under `/publishingApi`. Documentation links go to `humanpost.com`. Uploads may use service-issued signed storage URLs; never send the API key to those URLs. The package has no lifecycle hooks, background processes, telemetry, dependency installers, or remote-code execution.

For a read-only health check without a key, `python3 scripts/check_endpoint.py` verifies that the public endpoint rejects unauthenticated initialization. An authenticated connection test is available in the HumanPost dashboard. A successful unauthenticated check does not validate every tool or company workflow.

## Privacy and support

The hosted service processes account, content, task, and analytics data for the company authorized by your connection or API key. See the [HumanPost Privacy Policy](https://humanpost.com/privacy-policy) and [Terms of Service](https://humanpost.com/terms-of-service). Contact [support@humanpost.co](mailto:support@humanpost.co) or [open an integration issue](https://github.com/HumanPost-co/humanpost-mcp/issues). Never include credentials or private customer content in a public issue.

The integration package is MIT licensed. The hosted HumanPost service and HumanPost branding are not licensed by that grant. Platform compatibility configurations and a submission do not imply marketplace endorsement or approval.
