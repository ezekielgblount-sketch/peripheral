#!/usr/bin/env python3
"""Stills of the three presets for unease levels 8-10 (Subtle, Medium, Heavy), each between bursts and at the peak of one
-> screenshots/unease_stages/presets/, plus one contact sheet. The burst is held with the Pulse parameter so stills match."""
import sys, os, subprocess
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
out = os.path.join(root, "screenshots", "unease_stages", "presets")
POV = {"living": "500,985,165:200,720,110", "kitchen": "700,1290,165:850,780,105"}
NAMES = ("subtle", "medium", "heavy")
def ue(code):
    subprocess.run([sys.executable, os.path.join(here, "uepy.py"), "-c", code, "300"], check=True, stdout=subprocess.DEVNULL)
EX = "exec(open(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + 'Scripts/set_unease.py').read())"
quick = len(sys.argv) > 1
jobs = [(room, lv, p, b) for room in (("living",) if quick else ("living", "kitchen")) for lv in ((10,) if quick else (8, 9, 10)) for p in range(3) for b in (0, 1)]
first = True
for room, lv, p, b in jobs:
    ue("UNEASE=%d\nPRESET=%d\nPULSE=%d\n" % (lv * 10, p, b) + EX)
    name = "%s_level_%02d_%s_%s" % (room, lv, NAMES[p], "burst" if b else "between")
    env = dict(os.environ, SHOT_WARMUP="30" if first else "2", SHOT_TICKS="8"); first = False
    subprocess.run([sys.executable, os.path.join(here, "shot.py"), out, "%s:%s" % (name, POV[room])], check=True, env=env, stdout=subprocess.DEVNULL)
ue("UNEASE=0\nPRESET=1\nPULSE=-1\n" + EX)
from PIL import Image, ImageDraw
for room in set(j[0] for j in jobs):
    lvs = sorted(set(j[1] for j in jobs)); tw, th = 560, 301
    sheet = Image.new("RGB", (6 * tw, len(lvs) * (th + 26) + 4), (18, 18, 18)); d = ImageDraw.Draw(sheet)
    for r, lv in enumerate(lvs):
        for p in range(3):
            for b in (0, 1):
                im = Image.open(os.path.join(out, "%s_level_%02d_%s_%s.png" % (room, lv, NAMES[p], "burst" if b else "between"))).resize((tw - 4, th))
                x, y = (p * 2 + b) * tw + 2, r * (th + 26) + 24
                sheet.paste(im, (x, y)); d.text((x + 4, y - 18), "level %d  %s  %s" % (lv, NAMES[p].upper(), "peak of a burst" if b else "between bursts"), fill=(230, 230, 230))
    sheet.save(os.path.join(out, "_sheet_%s_presets.png" % room))
print("done", len(os.listdir(out)))
