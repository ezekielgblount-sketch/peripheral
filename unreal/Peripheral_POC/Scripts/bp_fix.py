#!/usr/bin/env python3
"""Apply text substitutions to a DSL file and try to compile it. Usage: bp_fix.py BP file.dsl 'old=>new' ..."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bp_tool as B
bp, path = sys.argv[1], sys.argv[2]
s = open(path).read()
for sub in sys.argv[3:]:
    a, b = sub.split("=>")
    s = s.replace(a, b)
open(path, "w").write(s)
print(json.dumps(B.write(bp, path))[:1200])
