#!/bin/sh
# Run one loop play-test step in the editor's play mode: pl.sh STEP [GO x,y] [LOOK x,y]
here="$(cd "$(dirname "$0")" && pwd)"
python3 "$here/uepy.py" -c "STEP='$1'
GO='$2'
LOOK='$3'
exec(open(r'$here/pie_loop.py').read())" 60
