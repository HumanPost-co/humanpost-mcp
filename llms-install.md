# Install HumanPost MCP

Use the hosted Streamable HTTP endpoint at `https://us-central1-clickbaitcarousel.cloudfunctions.net/mcp`. No local server build is required.

The user must already have a HumanPost account and a scoped company API key from Dashboard → Settings → API & MCP. Ask them to enter the key through the client's secure environment or configuration, not in chat. Configure `Authorization: Bearer <their key>`. Never fetch credentials from unrelated files.

For clients supporting remote HTTP, configure the URL directly. Use the client's documented transport spelling (`streamableHttp`, `http`, or `streamable-http`); do not substitute deprecated SSE. The repository's `.mcp.json` is Claude/Grok-compatible; `mcp.json` uses Agent Plugins transport spelling; manual Cursor uses `${env:HUMANPOST_API_KEY}` while Cursor plugin variables use `${HUMANPOST_API_KEY}`.

Run MCP initialization, send `notifications/initialized`, discover `tools/list`, and call `get_context` using the user's configured key. Check the company and scopes. A 401 means fix the credentials; a 403 means obtain the needed scope. Do not disable authentication. Keep write approvals enabled. A setup check does not require posting, creating accounts, or consuming paid generation credits.

Public documentation: https://humanpost.com/docs/mcp
