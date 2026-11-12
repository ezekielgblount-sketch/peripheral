"""Furnishes the basement, the garage and the back yard. Run through dress_rooms.py. Chore objects (mower, bin, broom,
mailbox, garden soil) live in build_chores.py."""
import unreal
import dress_lib as D
from dress_lib import P, PW, L, K, PF, HP, lamp, switch, fixture, room_light, hidden
GR, B, F1, C1 = HP.GR, HP.B, HP.F1, HP.C1
G = HP.GARAGE; ZG = G["floor"]

# ---------------- basement: painted block, bare bulbs ----------------
r = "Basement"
PW("furnace", "b_mid", "x0", 60, room=r); PW("water_heater", "b_mid", "x0", 200, room=r)
PW("shelf_metal", "b_store", "y0", 150, room=r); PW("shelf_metal", "b_store", "y0", 300, room=r); PW("holiday_bins", "b_store", "x0", 200, room=r)
PW("box_misc", "b_store", "x0", 320, room=r); PW("box_books", "b_store", "x0", 380, room=r); PW("box_plain", "b_store", "y0", 450, room=r)
PW("workbench", "b_east", "x0", 200, room=r); PW("pegboard", "b_east", "x0", 200, 150, room=r, collide=False); PW("paint_cans", "b_east", "y1", 120, 0, 14, room=r)
P("armchair", 1060, 900, B, (-1, 0), r); P("tv_console", 1070, 1200, B, (-1, 0), r); P("crt_tv", 1066, 1200, B + 60, (-1, 0), r, collide=False)
P("box_fragile", 700, 1900, B, (0, -1), r); P("box_living", 760, 1905, B, (0.2, -1), r); P("box_kitchen", 705, 1900, B + 45, (0.1, -1), r); P("bike_kid", 1050, 1700, B, (-1, 0), r)
for i, (x, y) in enumerate(((475, 1125), (287, 832), (345, 1430), (287, 1765), (833, 900), (833, 1600))):
    P("ceiling_light_off", x, y, -HP.SLAB, (1, 0), r, collide=False, tags=["sw_bsmt_off", "default_on"]); P(PF.variant("ceiling_light_off", True), x, y, -HP.SLAB, (1, 0), r, collide=False, tags=["sw_bsmt", "default_on"])
    lamp("bsmt_%d" % i, x, y, -HP.SLAB - 24, 650, r, "bsmt", 560, on=True, shadows=(i in (0, 4)))
(sx, sy), f = HP.at("b_foot", "y1", 60, 0.2); switch("bsmt", "light_switch", sx, sy, B + 120, f, r, "bsmt", on=True, stage=1)

# ---------------- garage: workbench, pegboard tools, second fridge, holiday bins, bikes, hose ----------------
r = "Garage"
P("workbench", 300, G["y0"] + 0.3, ZG, (0, 1), r); P("pegboard", 300, G["y0"] + 0.3, ZG + 150, (0, 1), r, collide=False)
P("fridge", 520, G["y0"] + 0.3, ZG, (0, 1), r); P("gas_can", 130, G["y0"] + 22, ZG, (0, 1), r); P("paint_cans", 170, G["y0"] + 16, ZG, (0, 1), r)
P("shelf_metal", 759.7, 320, ZG, (-1, 0), r); P("holiday_bins", 759.7, 420, ZG, (-1, 0), r)
P("bike_adult", 640, 0, ZG, (0, 1), r); P("bike_kid", 560, 30, ZG, (0, 1), r)
P("ladder", 0.3, 556, ZG, (1, 0), r); P("box_plain", 40, -10, ZG, (1, 0), r); P("box_misc", 44, 40, ZG, (1, 0.1), r)
P("hose_reel", 780.3, 300, GR + 90, (1, 0), r, collide=False)
for i, (x, y) in enumerate(((250, 270), (560, 270))):
    P("ceiling_light_off", x, y, C1, (1, 0), r, collide=False, tags=["sw_garage_off"]); hidden(P(PF.variant("ceiling_light_off", True), x, y, C1, (1, 0), r, collide=False, tags=["sw_garage"]))
    lamp("garage_%d" % i, x, y, C1 - 24, 1400, r, "garage", 820, temp=4000)
switch("garage", "light_switch", 615, 579.8, F1 + 120, (0, -1), r, "garage", stage=1)

# ---------------- back yard: patio with a gas grill and plastic chairs, shed, garden bed, sprinkler ----------------
r = "Yard"
P("shed", 2570, -100, GR, (-1, 0), r)
P("grill", 1745, 1120, GR + 2, (-1, 0), r); P("patio_table", 1560, 1390, GR + 2, (1, 0), r)
for (x, y, f) in ((1490, 1390, (1, 0)), (1630, 1390, (-1, 0)), (1560, 1320, (0, 1)), (1570, 1470, (0.1, -1))):
    P("plastic_chair", x, y, GR + 2, f, r)
P("garden_frame", 1650, 2180, GR, (0, 1), r)
for x in (1550, 1650, 1750):
    P("veg_plants", x, 2180, GR, (0, 1), r, collide=False)
P("sprinkler", 2150, 1250, GR, (0.3, 1), r, collide=False); P("hose_coil", 1140, 1700, GR, (1, 0.4), r, collide=False)
P("toy_ball", 2000, 1400, GR, (1, 0), r, tags=["inspect"]); P("bike_kid", 1180, 700, GR, (0.3, 1), r)
print("basement, garage and yard dressed")
