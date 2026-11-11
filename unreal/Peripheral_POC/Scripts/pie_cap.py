#!/usr/bin/env python3
"""Save the current play-mode picture. Usage: pie_cap.py out.png"""
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_tool import call
r = call("EditorToolset.EditorAppToolset", "CaptureViewport", {"captureTransform": None, "annotations": None, "bShowUI": False})
try:
    open(sys.argv[1], "wb").write(base64.b64decode(r["returnValue"]["image"]["data"])); print("ok", sys.argv[1])
except Exception as e:
    print("fail", str(r)[:200])
