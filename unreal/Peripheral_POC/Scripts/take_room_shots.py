#!/usr/bin/env python3
"""Final screenshots: every room from 3 angles, day and night, with a 178 cm mannequin for scale.
Usage: take_room_shots.py day|night [room ...]   -> screenshots/<room>/<room>_<n>_<day|night>.png"""
import sys, os, subprocess
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
LND, F1, F2 = -126, 0, 259
E = 160
ROOMS = {   # room: (mannequin x,y,z), [(camera xyz, target xyz) x3]
    "entry": ((70, 1136, LND), [((150, 1090, -10), (20, 1330, -40)), ((150, 1225, LND + E), (10, 1100, LND + 90)), ((160, 1460, E), (40, 1150, -60))]),
    "living_room": ((430, 870, F1), [((540, 985, E), (150, 700, 90)), ((60, 960, E), (430, 700, 80)), ((330, 640, 150), (260, 1010, 70))]),
    "kitchen": ((700, 1080, F1), [((700, 1300, E), (850, 760, 100)), ((640, 640, E), (820, 1300, 90)), ((880, 1190, E), (650, 900, 100))]),
    "hallway": ((330, 1380, F1), [((540, 1420, E), (150, 1150, 60)), ((160, 1460, E), (540, 1330, 120)), ((525, 1070, E), (500, 1480, 110))]),
    "upstairs_hall": ((250, 1310, F2), [((20, 1300, F2 + E), (500, 1320, F2 + 120)), ((540, 1310, F2 + E), (60, 1300, F2 + 110)), ((60, 1190, F2 + E), (300, 1190, F2 - 60))]),
    "bedroom": ((760, 1450, F2), [((650, 1410, F2 + E), (850, 1650, F2 + 70)), ((880, 1680, F2 + E), (620, 1420, F2 + 80)), ((870, 1400, F2 + E), (640, 1640, F2 + 80))]),
    "bathroom": ((680, 1240, F2), [((610, 1290, F2 + E), (860, 1200, F2 + 70)), ((800, 1320, F2 + 165), (700, 1150, F2 + 100)), ((620, 1160, F2 + E), (800, 1330, F2 + 60))]),
    "exterior": ((-250, 1136, -140), [((-1500, 300, 60), (300, 1000, 150)), ((-1100, 2600, 30), (-1500, -800, 150)), ((1900, 1500, 60), (900, 1100, 150))]),
}
mode = sys.argv[1]
rooms = sys.argv[2:] or list(ROOMS)


def ue(code):
    subprocess.run([sys.executable, os.path.join(here, "uepy.py"), "-c", code, "300"], check=True, stdout=subprocess.DEVNULL)


PRE = "import sys\nsys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + 'Scripts')\nimport poc_lib as L, meshkit as K, props_furniture as PF\n"
ue("NIGHT=%s\nexec(open(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + 'Scripts/daynight.py').read())" % (mode == "night"))
for r in rooms:
    (mx, my, mz), cams = ROOMS[r]
    ue(PRE + "L.clear('mannequin')\nK.place(PF.get('mannequin'), 'Mannequin', %s, %s, %s, face=(1, 0.4), folder='Temp', tag='mannequin', collide=False)" % (mx, my, mz))
    specs = ["%s_%d_%s:%s,%s,%s:%s,%s,%s" % ((r, i + 1, mode) + c + t) for i, (c, t) in enumerate(cams)]
    subprocess.run([sys.executable, os.path.join(here, "shot.py"), os.path.join(root, "screenshots", r)] + specs, check=True)
ue(PRE + "L.clear('mannequin')")
ue("NIGHT=False\nexec(open(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + 'Scripts/daynight.py').read())")
