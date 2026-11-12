"""The things the nine daily chores use (tag 'chore'). BP_Chores finds them by tag. Safe to re-run.
Run after dress_rooms.py (the washer, dryer and hall light switch are dressing and are only tagged there)."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import dress_lib as D
importlib.reload(D)
from dress_lib import P, PW, HP, hidden
GR, F1, F2 = HP.GR, HP.F1, HP.F2
ZG = HP.GARAGE["floor"]
print("cleared", D.begin("chore"))
r = "Chores"
MOW = dict(x0=1850, y0=200, nx=7, ny=9)                       # the patch of back lawn that has grown long: 7 m x 9 m in 1 m squares
CURB = (-1125, 600)                                           # where the bin stands on collection day
# 1. mow the lawn: push mower in the garage by the back doorway; long grass in the yard, one strip tag per row
P("mower", 690, 60, ZG, (0, 1), r, tags=["push", "ch_mower"], movable=True)
for i in range(MOW["nx"]):
    for j in range(MOW["ny"]):
        a = P("grass_tall", MOW["x0"] + i * 100, MOW["y0"] + j * 100, GR, ((i * 7 + j * 3) % 5 - 2, 3), r, collide=False, tags=["grass", "grass_s%d" % i], movable=True)
        a.static_mesh_component.set_cast_shadow(False)
# 2. take out the trash: the kitchen bag goes in the wheeled bin, the bin goes to the curb
P("trash_bag", 652, 888, F1, (1, 0.3), r, tags=["carry", "ch_bag"])
P("trash_bin", 80, 470, ZG, (1, 0), r, tags=["push", "ch_bin"], movable=True)
# 3. get the mail
P("mailbox", CURB[0] - 20, 660, GR, (1, 0), r, tags=["ch_mailbox"], movable=True)
hidden(P("mailbox_open", CURB[0] - 20, 660, GR, (1, 0), r, tags=["ch_mailbox_open"], movable=True))
hidden(P("mail_pile", CURB[0] + 2, 660, GR + 106, (1, 0.2), r, collide=False, tags=["carry", "ch_mail"]))
# 4. do the dishes: a stack in the sink, a rack on the counter beside it
(sx, sy), f = HP.at("kitchen", "x1", 181, 30)
for i in range(5):
    P("plate_dirty", sx, sy, F1 + 80 + i * 1.4, (1, i * 0.4 - 1), r, collide=False, tags=["ch_plate"], movable=True)
(rx, ry), f = HP.at("kitchen", "x1", 106, 30)
P("dish_rack", rx, ry, F1 + 91, (0, 1), r, collide=False, tags=["ch_rack"])
for i in range(5):                                           # the same plates, clean, standing in the rack: shown one by one as they are washed
    c = hidden(P("plate", rx, ry - 12 + i * 6, F1 + 103, (1, 0), r, collide=False, tags=["ch_plate_clean"], movable=True))
    c.set_actor_rotation(unreal.Rotator(roll=82.0, pitch=0.0, yaw=0.0), False)
# 5. laundry: a basket of clothes by the washer
P("laundry_basket", 808, 642, F1, (1, 0), r, tags=["ch_basket"]); P("clothes_floor", 808, 642, F1 + 16, (0.3, 1), r, collide=False, tags=["ch_clothes"], movable=True)
# 6. water the garden bed: three patches of dry soil, each with a wet twin
P("watering_can", 1470, 2120, GR, (1, 0.5), r, tags=["carry", "ch_can"])
for i, x in enumerate((1550, 1650, 1750)):
    P("soil_dry", x, 2180, GR + 1, (0, 1), r, collide=False, tags=["ch_soil", "ch_soil%d" % i], movable=True)
    hidden(P("soil_wet", x, 2180, GR + 1, (0, 1), r, collide=False, tags=["ch_soil_wet", "ch_soilw%d" % i], movable=True))
# 7. sweep the garage: a push broom, and piles of dust and leaves
P("broom", 300, 548, ZG, (1, 0), r, tags=["push", "ch_broom"], movable=True)
for (x, y) in ((120, 120), (300, 230), (520, 180), (200, 400), (400, 330), (600, 300), (90, 260), (330, 80)):
    P("dust_pile", x, y, ZG, ((x * 7) % 5 - 2, 2), r, collide=False, tags=["ch_dust"], movable=True)
# 8. change the burnt-out bulb in the hall: a new bulb on the laundry shelf
PW("bulb_box", "mud", "x0", 150, 152.5, 12, room=r, tags=["carry", "ch_bulb"])
# 9. make the bed in Jack's room
PW("bed_unmade", "jack", "y1", 268, room=r, tags=["ch_bed"], movable=True)
hidden(PW("bed_made", "jack", "y1", 268, room=r, tags=["ch_bed_made"], movable=True))
print("chore objects placed")
