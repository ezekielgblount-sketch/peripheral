#!/bin/bash
# Start, stop or restart MY background editor for this project (never touches an editor Joel opened on another project).
# Usage: Scripts/editor.sh start|stop|restart     Save the level before stop/restart.
P="$(cd "$(dirname "$0")/.." && pwd)"
PAT="UnrealEditor.app/Contents/MacOS/UnrealEditor.*Peripheral_POC.uproject"
stop() { pkill -f "$PAT"; for i in $(seq 1 30); do pgrep -f "$PAT" >/dev/null || break; /bin/sleep 2; done; }
start() {
  R="$P/Saved/Autosaves/PackageRestoreData.json"      # a leftover restore file makes the editor wait on a hidden prompt
  [ -f "$R" ] && mv "$R" "${TMPDIR:-/tmp}/PackageRestoreData_$(date +%s).json"
  open -g -n "/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app" --args "$P/Peripheral_POC.uproject" -ModelContextProtocolStartServer -nosplash
  for i in $(seq 1 90); do [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/mcp)" = "405" ] && break; /bin/sleep 5; done
  /bin/sleep 25; echo "editor up"
}
case "$1" in stop) stop;; start) start;; restart) stop; start;; esac
