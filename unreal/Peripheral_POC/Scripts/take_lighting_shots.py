#!/usr/bin/env python3
"""Day and night comparison stills of the interior lighting -> screenshots/lighting_pass/ (unease 0)."""
import sys, os, subprocess
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
out = os.path.join(root, "screenshots", "lighting_pass")
POV = {"living_seating": "500,985,165:200,720,110", "living_torchiere": "430,960,165:40,800,125", "kitchen": "700,1290,165:850,780,105",
       "hall_table_lamp": "150,1330,165:560,1450,100", "bedroom": "650,1415,424:850,1650,330", "bathroom": "620,1250,424:790,1180,360"}
only = sys.argv[1:]
def ue(code):
    subprocess.run([sys.executable, os.path.join(here, "uepy.py"), "-c", code, "300"], check=True, stdout=subprocess.DEVNULL)
EX = "exec(open(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + 'Scripts/%s').read())"
ue("UNEASE=0\nPRESET=1\nPULSE=-1\n" + EX % "set_unease.py")
for tod, label in (("night", "night"), ("afternoon", "day")):
    ue("TOD='%s'\n" % tod + EX % "timeofday.py")
    specs = ["%s_%s:%s" % (k, label, v) for k, v in POV.items() if not only or k in only]
    subprocess.run([sys.executable, os.path.join(here, "shot.py"), out] + specs, check=True, env=dict(os.environ, SHOT_WARMUP="200", SHOT_TICKS="30"), stdout=subprocess.DEVNULL)
from PIL import Image, ImageDraw
ks = [k for k in POV if os.path.exists(os.path.join(out, k + "_day.png"))]; tw, th = 640, 344
sheet = Image.new("RGB", (2 * tw, len(ks) * (th + 24)), (18, 18, 18)); d = ImageDraw.Draw(sheet)
for r, k in enumerate(ks):
    for cidx, label in enumerate(("day", "night")):
        im = Image.open(os.path.join(out, "%s_%s.png" % (k, label))).resize((tw - 4, th))
        sheet.paste(im, (cidx * tw + 2, r * (th + 24) + 22)); d.text((cidx * tw + 6, r * (th + 24) + 5), "%s  -  %s" % (k.replace("_", " "), label), fill=(230, 230, 230))
sheet.save(os.path.join(out, "_sheet_day_night.png")); print("done", len(os.listdir(out)))
