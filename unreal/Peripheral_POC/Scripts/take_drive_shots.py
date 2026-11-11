#!/usr/bin/env python3
"""Screenshots matched to Joel's reference photos (A-G) -> screenshots/drive_session/<area>/."""
import sys, os, subprocess
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
F2 = 259
AREAS = {
    "A_piano_corner": ["piano:175,810,150:92,620,105"],
    "B_living_seating": ["seating:345,900,150:345,620,95", "wide:500,985,165:200,720,110"],
    "C_built_in_bookcases": ["shelves:430,868,150:573,868,120"],
    "D_fireplace": ["mantel:420,708,140:573,708,125"],
    "E_entry_hall": ["secretary:388,1375,150:388,1512,90", "entry:150,1225,34:20,1080,-110"],
    "F_dining_kitchen": ["hutch:770,1110,150:590,1100,115", "valance_pendant:740,1290,125:890,1370,190", "kitchen:640,640,160:820,1300,90"],
    "G_jacks_room": ["desk:770,1500,%d:885,1530,%d" % (F2 + 150, F2 + 85), "room:650,1415,%d:850,1650,%d" % (F2 + 160, F2 + 70), "dresser:820,1500,%d:600,1600,%d" % (F2 + 150, F2 + 90)],
    "H_arrival": ["car_boot_and_boxes:-930,560,-10:-620,350,-80", "car_side:-560,700,-40:-520,360,-80", "drivers_seat_view:-512,396,-27:-100,420,-40", "front:-1500,300,60:300,1000,150"],
    "I_parents_tech": ["tv:250,860,130:250,1010,90"],
}
for area, specs in AREAS.items():
    env = dict(os.environ, SHOT_WARMUP="40")
    subprocess.run([sys.executable, os.path.join(here, "shot.py"), os.path.join(root, "screenshots", "drive_session", area)] + specs, check=True, env=env, stdout=subprocess.DEVNULL)
print("drive_session shots done")
