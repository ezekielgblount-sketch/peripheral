#!/usr/bin/env python3
"""Drives the five-day story in editor play mode by script (no keys, no mouse): places the test pawn, presses "use" through
the test hooks, and prints the state after each day. Start play mode first. Usage: story_test.py [first_day]"""
import subprocess, sys, time, os, re
here = os.path.dirname(os.path.abspath(__file__))
def pd(step, **kw):
    out = subprocess.run([os.path.join(here, "pd.sh"), step] + ["%s=%s" % kv for kv in kw.items()], capture_output=True, text=True).stdout
    return out
def state():
    o = pd("info"); m = re.search(r"story day (\d+) phase (\d+) loop (\w+) (\d+) / (\d+)", o); k = re.search(r"loopK (-?\d+)", o)
    return dict(day=int(m.group(1)), phase=int(m.group(2)), loop=m.group(3) == "True", count=int(m.group(4)), need=int(m.group(5)), k=int(k.group(1)), raw=o.split("\n")[0][:230])
def wait_phase(ph, limit=40):
    for _ in range(limit):
        s = state()
        if s["phase"] == ph: return s
        time.sleep(1)
    print("  !! never reached phase", ph, state()["raw"]); return state()
F2 = 259
def chores(day):
    if day == 2:
        pd("use", GO="980,1480,259"); time.sleep(0.5)
        for i in range(5): pd("use", GO="990,1043,0"); time.sleep(0.9)
        pd("use", GO="-1050,660,-140"); time.sleep(0.6); pd("hold", HOLD="Chores_mail_pile_1", MODE="carry", GO="300,1420,0", LOOK="500,1420,90"); time.sleep(0.8); pd("drop")
        pd("use", GO="690,660,0"); time.sleep(20); pd("use", GO="690,660,0")
    if day == 3:
        for i in range(7):
            for j in range(9):
                pd("hold", HOLD="Chores_mower_1", MODE="push", GO="%d,%d,-140" % (1850 + i * 100 - 98, 200 + j * 100), LOOK="%d,%d,-48" % (1850 + i * 100 + 300, 200 + j * 100))
        pd("drop")
        for x in (1550, 1650, 1750):
            pd("hold", HOLD="Chores_watering_can_1", MODE="carry", GO="%d,2080,-140" % x); time.sleep(3)
        pd("drop"); pd("hold", HOLD="Chores_bulb_box_1", MODE="carry", GO="340,1425,0"); time.sleep(0.6)
    if day == 4:
        pd("hold", HOLD="Chores_trash_bag_1", MODE="carry", GO="40,470,-140", LOOK="80,470,-100"); time.sleep(0.6)
        pd("hold", HOLD="Chores_trash_bin_1", MODE="push", GO="-1230,600,-140", LOOK="-1000,600,-48"); time.sleep(0.6); pd("drop"); time.sleep(0.6)
        for (x, y) in ((120, 120), (300, 230), (520, 180), (200, 400), (400, 330), (600, 300), (90, 260), (330, 80)):
            pd("hold", HOLD="Chores_broom_1", MODE="push", GO="%d,%d,-138" % (x - 98, y), LOOK="%d,%d,-46" % (x + 200, y)); time.sleep(0.3)
        pd("drop")
def loop():
    """Walk the corridor the right way round each pass until the story ends the loop."""
    for n in range(14):
        s = state()
        if not s["loop"]: return s
        a, b = ("643,1850", "513,1850") if s["k"] < 0 else ("513,1850", "643,1850")     # nothing wrong: in by closet B and on round; something wrong: the other way
        pd("go", GO="639,1700,%d" % F2); time.sleep(0.5); pd("go", GO=a + ",%d" % F2); time.sleep(0.5); pd("go", GO=b + ",%d" % F2); time.sleep(0.5)
        pd("go", GO="639,1650,%d" % F2); time.sleep(0.7)
    return state()
def bed():
    wait_phase(5, 10); pd("suse", GO="980,1480,259"); return wait_phase(1, 30)
first = int(sys.argv[1]) if len(sys.argv) > 1 else 2
if "resume" not in sys.argv:
    pd("req", REQ=str(first)); s = wait_phase(1, 30); print("start:", s["raw"])
for day in range(first, 6):
    if "resume" not in sys.argv: chores(day)
    time.sleep(1.5); s = state(); print("day %d after chores:" % day, s["raw"])
    while s["loop"]:
        s = loop(); time.sleep(1.5); s = state(); print("  after a loop:", s["raw"])
    if day < 5:
        s = bed(); print("  woke:", s["raw"])
s = wait_phase(6, 10)
for go in ("190,860,259", "120,830,259", "300,880,259"):
    pd("suse", GO=go); time.sleep(0.6)
s = wait_phase(7, 10); print("memories:", s["raw"])
pd("go", GO="200,800,259", LOOK="200,600,400"); time.sleep(7.5)                      # face away from the door, wait
print("climax shown:", state()["raw"])
pd("go", GO="200,800,259", LOOK="50,1118,350"); time.sleep(3.5)                      # turn and look at it
s = wait_phase(8, 10); print("release:", s["raw"]); time.sleep(10)
pd("suse", GO="-560,150,-140"); time.sleep(0.5); pd("suse", GO="-560,150,-140"); time.sleep(0.5)      # the boxes are still in the car in this test
print("unpacked:", state()["raw"])
pd("suse", GO="250,700,0"); time.sleep(11)
print("end:", pd("info").split("\n")[0][:120])
