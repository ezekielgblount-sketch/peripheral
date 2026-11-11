#!/bin/bash
# Usage: mcp.sh <method> '<params json>'   - minimal JSON-RPC client for the Unreal MCP server
URL=${UNREAL_MCP_URL:-http://localhost:8000/mcp}
SID_FILE=${TMPDIR:-/tmp}/unreal_mcp_sid
H=(-H "Content-Type: application/json" -H "Accept: application/json, text/event-stream")
if [ ! -s "$SID_FILE" ] || [ "$1" = "init" ]; then
  curl -s -m 20 -D - -o /dev/null "${H[@]}" -X POST "$URL" -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"poc-cli","version":"0.1"}}}' | tr -d '\r' | awk -F': ' 'tolower($1)=="mcp-session-id"{print $2}' > "$SID_FILE"
  SID=$(cat "$SID_FILE"); [ -n "$SID" ] && H+=(-H "Mcp-Session-Id: $SID")
  curl -s -m 20 -o /dev/null "${H[@]}" -X POST "$URL" -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
  [ "$1" = "init" ] && { echo "session=$SID"; exit 0; }
fi
SID=$(cat "$SID_FILE"); [ -n "$SID" ] && H+=(-H "Mcp-Session-Id: $SID")
P="$2"; [ -z "$P" ] && P='{}'
curl -s -m ${MCP_TIMEOUT:-120} "${H[@]}" -X POST "$URL" -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"$1\",\"params\":$P}" | sed 's/^data: //'
