# Install HumanPost MCP

Use the hosted Streamable HTTP endpoint at `https://humanpost.com/mcp`. No local server build is required.

For OAuth-capable clients, configure the URL without a fixed Authorization header. Follow the client’s Connect action to sign in to HumanPost, select exactly one company and grant the minimum scopes needed. Write scopes are off by default. Revoke a connection in HumanPost Settings → API Keys. Never ask for sign-in codes, passwords or tokens in chat.

For clients using API keys, create a scoped company key in Dashboard → Settings → API & MCP. Enter it through the client’s secure environment or configuration, not in chat. The legacy endpoint `https://us-central1-clickbaitcarousel.cloudfunctions.net/mcp` remains supported with `Authorization: Bearer <their key>`. Never fetch credentials from unrelated files. The repository’s `.mcp.json`, `config-cline.json` and `config-muse.json` retain this API-key setup.

Use the client’s documented transport spelling (`streamableHttp`, `http`, or `streamable-http`); do not substitute deprecated SSE. Run MCP initialization, send `notifications/initialized`, discover `tools/list`, and call `get_context`. Verify the company and scopes. A 401 requires connecting again; a scope error requires the user to grant the needed permission. Do not disable authentication. Keep write approvals enabled. Setup does not require posting, creating accounts, or consuming generation credits.

Public documentation: https://humanpost.com/docs/mcp
