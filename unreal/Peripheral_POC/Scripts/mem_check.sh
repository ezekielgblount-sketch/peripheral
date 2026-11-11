#!/bin/sh
# Memory guard: prints the editor's real footprint and free memory. Exit 1 when the editor is over the limit (default 12 GB),
# which means: save, quit and relaunch it before doing anything heavy.
LIMIT_GB=${1:-12}
top -l 1 -o mem -n 12 -stats pid,command,mem | grep -i unreal
memory_pressure | tail -1
sysctl -n vm.swapusage
PID=$(pgrep -f "Peripheral_POC.uproject" | head -1)
[ -z "$PID" ] && { echo "editor not running"; exit 0; }
KB=$(footprint -p "$PID" 2>/dev/null | awk '/phys_footprint:/ {print $2 $3; exit}')
echo "editor footprint: $KB"
GB=$(top -l 1 -pid "$PID" -stats mem | tail -1 | awk '{v=$1; if (v ~ /G/) {sub(/G.*/,"",v); print int(v)} else print 0}')
[ "$GB" -ge "$LIMIT_GB" ] && { echo "OVER LIMIT (${GB}G >= ${LIMIT_GB}G): restart the editor"; exit 1; }
exit 0
