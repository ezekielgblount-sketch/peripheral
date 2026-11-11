#!/usr/bin/env python3
"""Run Python inside the open Unreal Editor (via the Saved/PyInbox watcher in Content/Python/init_unreal.py).
Usage: uepy.py script.py [timeout_s]   |   uepy.py -c "code" [timeout_s]"""
import sys, os, time, uuid
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
inbox = os.path.join(root, "Saved", "PyInbox"); os.makedirs(inbox, exist_ok=True)
if sys.argv[1] == "-c": code = sys.argv[2]; rest = sys.argv[3:]
else: code = open(sys.argv[1]).read(); rest = sys.argv[2:]
timeout = float(rest[0]) if rest else 300
name = "%d_%s" % (time.time() * 1000, uuid.uuid4().hex[:6])
tmp = os.path.join(inbox, name + ".part"); open(tmp, "w").write(code); os.replace(tmp, os.path.join(inbox, name + ".py"))
out = os.path.join(inbox, name + ".out"); t0 = time.time()
while not os.path.exists(out):
    if time.time() - t0 > timeout: sys.exit("timed out waiting for the editor")
    time.sleep(0.2)
txt = open(out).read(); os.remove(out)
status, _, body = txt.partition("\n"); print(body.rstrip())
sys.exit(0 if status == "OK" else 1)
