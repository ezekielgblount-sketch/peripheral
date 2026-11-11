#!/usr/bin/env python3
"""POV screenshots across unease levels (0-10) and times of day -> screenshots/unease_stages/."""
import sys, os, subprocess
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
out = os.path.join(root, "screenshots", "unease_stages")
POV = {"living": "500,985,165:200,720,110", "kitchen": "700,1290,165:850,780,105", "bedroom": "650,1415,424:850,1650,330"}
def ue(code):
    subprocess.run([sys.executable, os.path.join(here, "uepy.py"), "-c", code, "300"], check=True, stdout=subprocess.DEVNULL)
EX = "exec(open(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + 'Scripts/%s').read())"
def shoot(tod, room, levels, warm):
    ue("TOD='%s'\n" % tod + EX % "timeofday.py")
    for i, lv in enumerate(levels):
        ue("UNEASE=%d\n" % (lv * 10) + EX % "set_unease.py")
        env = dict(os.environ, SHOT_WARMUP=str(warm if i == 0 else 4))
        subprocess.run([sys.executable, os.path.join(here, "shot.py"), out, "%s_%s_level_%02d:%s" % (room, tod, lv, POV[room])], check=True, env=env, stdout=subprocess.DEVNULL)
shoot("afternoon", "living", range(0, 11), 260)
shoot("afternoon", "kitchen", (0, 5, 10), 120)
shoot("afternoon", "bedroom", (0, 5, 10), 120)
shoot("morning", "living", (0, 3, 6, 10), 260)
shoot("golden", "living", (0, 3, 6, 10), 260)
shoot("night", "living", (0, 3, 6, 10), 260)
ue("UNEASE=0\n" + EX % "set_unease.py"); ue("TOD='afternoon'\n" + EX % "timeofday.py")
print("done", len(os.listdir(out)))
