#!/bin/bash
# Usage: Scripts/pd.sh STEP [VAR=value ...]   e.g.  Scripts/pd.sh go GO=640,800,0     Runs pie_day.py in the playing editor.
P="$(cd "$(dirname "$0")/.." && pwd)"; STEP="$1"; shift
CODE="STEP='$STEP'"
for kv in "$@"; do CODE="$CODE
${kv%%=*}='${kv#*=}'"; done
CODE="$CODE
exec(open(r'$P/Scripts/pie_day.py').read())"
python3 "$P/Scripts/uepy.py" -c "$CODE" 60
