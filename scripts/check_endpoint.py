"""Check the public HumanPost MCP authentication boundary without credentials."""
import json
import urllib.error
import urllib.request

request = urllib.request.Request(
    "https://us-central1-clickbaitcarousel.cloudfunctions.net/mcp",
    data=json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-11-25", "capabilities": {},
                   "clientInfo": {"name": "humanpost-listing-check", "version": "1.0.0"}},
    }).encode(),
    headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    method="POST",
)
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        raise SystemExit(f"Unexpected unauthenticated success: HTTP {response.status}")
except urllib.error.HTTPError as error:
    body = json.load(error)
    if error.code != 401 or body.get("error", {}).get("code") != "unauthorized":
        raise SystemExit(f"Unexpected authentication result: HTTP {error.code}")
    print("PASS: public MCP responds and rejects unauthenticated initialization with HTTP 401.")
