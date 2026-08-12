"""Minimal stdio MCP server that serves a single mock JIRA ticket.

Lets the jira-bugfix demo run end-to-end without a real Jira instance.
Implements just enough of the MCP protocol (tools/list, tools/call) to back
the `get_issue` tool.

Usage:
    python3 mock_jira_mcp.py

Test with a JSON-RPC message on stdin:
    printf '%s' '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python3 mock_jira_mcp.py
"""

import json
import sys
from pathlib import Path

TICKETS = {}

_ticket_path = Path(__file__).parent / "PROJ-102.json"
if _ticket_path.exists():
    TICKETS[_ticket_path.stem] = json.loads(_ticket_path.read_text())

TOOLS = [
    {
        "name": "get_issue",
        "description": "Fetch a JIRA issue by its key (e.g. PROJ-102) as a JSON object.",
        "inputSchema": {
            "type": "object",
            "properties": {"key": {"type": "string"}},
            "required": ["key"],
        },
    }
]


def handle(params):
    """Return a list of (text_response, is_error)."""
    method = params.get("method")

    if method == "initialize":
        return [{"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "mock-jira", "version": "1.0.0"}}], False

    if method == "notifications/initialized":
        return [None], False

    if method == "tools/list":
        return [{"tools": TOOLS}], False

    if method == "tools/call":
        args = params["params"].get("arguments", {})
        key = args.get("key", "").upper()
        ticket = TICKETS.get(key)
        if not ticket:
            return [json.dumps({"error": f"issue {key} not found"})], True
        return [json.dumps(ticket)], False

    return [json.dumps({"error": f"unsupported method: {method}"})], True


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        rid = msg.get("id")
        texts, is_error = handle(msg)
        for text in texts:
            if text is None:
                continue
            base = {"jsonrpc": "2.0", "id": rid}
            if is_error:
                base["error"] = {"code": -32000, "message": text}
            else:
                base["result"] = {"content": [{"type": "text", "text": text}]}
            sys.stdout.write(json.dumps(base) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
