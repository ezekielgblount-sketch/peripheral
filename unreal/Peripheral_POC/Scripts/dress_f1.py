"""Furnishes floor 1: entry and hall, living room, dining room, kitchen and nook, laundry / mudroom, half bath, den.
Run through dress_rooms.py. Positions are blueprint cm; PW(prop, room, wall, along) puts a thing against a wall."""
import unreal
import dress_lib as D
from dress_lib import P, PW, L, K, PF, HP, lamp, switch, fixture, shaded, room_light, border, hidden, no_shadow
LND, F1, C1, F2, C2, F3 = HP.LND, HP.F1, HP.C1, HP.F2, HP.C2, HP.F3


def twin(i, normal, alt, room_name, side, along, z, room, **kw):
    """A thing and its wrong twin for the anomaly day: the twin (tag dy<i>) stays hidden until anomaly i fires."""
    PW(normal, room_name, side, along, z, room=room, collide=False, tags=["dy%dn" % i], **kw)
    hidden(PW(alt, room_name, side, along, z, room=room, collide=False, tags=["dy%d" % i], **kw))


# ---------------- handrails, half-wall caps, crown moulding: one fixed mesh ----------------
fx = K.Kit()
u = lambda x, y, z: (x - L.OX, -(y - L.OY), z)


def rail(p0, p1):
    fx.tube("rail", u(*p0), u(*p1), 2.2, 10)
    for f in (0.1, 0.5, 0.9):
        m = [p0[i] + (p1[i] - p0[i]) * f for i in range(3)]
        fx.tube("brass", u(m[0], m[1], m[2] - 3), u(m[0], m[1], m[2] - 6), 0.7, 6)


def cap(x0, y0, x1, y1, z):
    fx.box("rail", x0 - 1 - L.OX, -(y1 + 1 - L.OY), z, x1 + 1 - L.OX, -(y0 - 1 - L.OY), z + 4)


def crown(name, key="white"):
    x0, y0, x1, y1 = HP.room(name)["rect"]; z = HP.room(name)["ceil"]
    for (a0, b0, a1, b1) in ((x0, y0, x1, y0 + 7), (x0, y1 - 7, x1, y1), (x0, y0, x0 + 7, y1), (x1 - 7, y0, x1, y1)):
        fx.box(key, a0 - L.OX, -(b1 - L.OY), z - 8, a1 - L.OX, -(b0 - L.OY), z)


rail((6, 1296, LND + 18 + 92), (6, 1464, F1 + 92))                                   # up flight, on the front wall
rail((180, 1082, LND + 92), (348, 1082, LND - 108 + 92))                             # basement flight
rail((470, 1192, 92), (106, 1192, F2 + 92))                                          # stair to floor 2
rail((175, 1434, F2 + 92), (539, 1434, F3 + 92))                                     # attic stair
cap(100, 1296, 112, 1464, F1 + 95); cap(376, 1076, 388, 1174, F1 + 95)
cap(100, 1284, 470, 1296, F2 + 91); cap(470, 1186, 482, 1284, F2 + 91)
cap(203, 1416, 539, 1428, F3 + 92); cap(203, 1528, 539, 1540, F3 + 92); cap(191, 1416, 203, 1540, F3 + 92)
crown("living", "oak"); crown("dining")
a = D.eas.spawn_actor_from_object(fx.save("dress_fixed", local=False), unreal.Vector(0, 0, 0))
a.set_actor_label("Rails_and_caps"); a.set_folder_path("Dress/Entry"); a.tags = ["dress"]
a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)

# ---------------- entry ----------------
r = "Entry"
P("doormat", 45, 1181, LND, (1, 0), r, collide=False)
for (tag, prop) in (("dy11n", "coats_one"), ("dy11", "coats_two")):                    # anomaly: two coats on the rail instead of one
    c = P(prop, 95, 1076.3, LND + 165, (0, 1), r, collide=False, tags=[tag])
    if tag == "dy11": hidden(c)
P("shoes", 40, 1110, LND, (1, 0.3), r, collide=False)
hidden(P("shoes", 150, 1250, LND, (-0.4, 1), r, collide=False, tags=["dy14"]))         # anomaly: shoes that were not there before
fixture("ceiling_light_off", 90, 1180, C1, (1, 0), r, "entry", on=True); lamp("entry", 90, 1180, C1 - 22, 800, r, "entry", 520, on=True)
switch("entry", "light_switch", 0.2, 1245, LND + 120, (1, 0), r, "entry", on=True, stage=1)

# ---------------- hall, floor 1 ----------------
r = "Hall"
room_light("hall_main", "hall", 340, 1425, 800, sw=("x1", 14), on=False, stage=1, room=r, sw_tags=["ch_hall_switch"])      # its bulb is dead until the chore
room_light("hall_back", "hallb", 522, 1180, 600, sw=None, on=True, stage=1, room=r)
PW("secretary", "hall_main", "y1", 340, room=r); PW("frame_map", "hall_main", "y1", 340, 170, room=r, collide=False)
PW("barometer", "hall_main", "y1", 412, 165, room=r, collide=False); PW("jar_candle", "hall_main", "y1", 362, 110, 12, room=r, collide=False)
PW("frame_school", "hall_main", "y1", 60, 155, room=r, collide=False); PW("frame_school_b", "hall_main", "y1", 96, 150, room=r, collide=False)
PW("side_table", "hall_main", "x1", 196, room=r)
switch("hall_table", "table_lamp", 549, 1492, F1 + 55, (1, 0), r, "hall_table", lit=True); shaded("hall_table", 549, 1492, F1 + 88, 420, r, "hall_table", C1)
P("phone_cordless", 552, 1470, F1 + 55, (-1, 0.2), r, collide=False); P("key_bowl", 548, 1512, F1 + 55, (1, 0), r, collide=False)
for (tag, prop) in (("dy12n", "answering_machine"), ("dy12", "answering_machine_new")):   # anomaly: the message light starts blinking
    c = P(prop, 556, 1450, F1 + 55, (-1, 0), r, collide=False, tags=[tag])
    if tag == "dy12": hidden(c)
twin(13, "height_marks", "height_marks_b", "hall_main", "x1", 38, 70, r)              # anomaly: a new height mark above Jack's last one
PW("phone_book", "hall_main", "x1", 196, 38.2, 18, room=r, collide=False)
PW("vent", "hall_main", "y1", 200, 12, room=r, collide=False); PW("outlet", "hall_back", "x1", 40, 30, room=r, collide=False)
PW("frame_portrait", "hall_back", "x1", 150, 160, room=r, collide=False)
P("shoes", 130, 1520, F1, (0, -1), r, collide=False)

# ---------------- living room: antique white walls, honey oak trim; fireplace on the side wall ----------------
r = "Living"
PW("fireplace", "living", "y0", 287, room=r); PW("frame_landscape_b", "living", "y0", 287, 203, room=r, collide=False)
for (tag, prop) in (("dy1n", "banner_thankful"), ("dy1", "banner_thankfu")):          # anomaly: THANKFUL loses a letter
    c = PW(prop, "living", "y0", 287, 128, 31, room=r, collide=False, tags=[tag])
    if tag == "dy1": hidden(c)
for (tag, prop) in (("dy3n", "clock_mantel"), ("dy3", "clock_mantel_same")):          # anomaly: every clock shows the same time
    c = PW(prop, "living", "y0", 287, 146, 18, room=r, collide=False, tags=[tag])
    if tag == "dy3": hidden(c)
PW("bookshelf_white", "living", "y0", 95, room=r); PW("bookshelf_white", "living", "y0", 480, room=r)
P("keepsake_box", 480, 608, F1 + 55, (0, 1), r, collide=False); P("albums", 95, 610, F1 + 11, (0, 1), r, collide=False)
P("rug_oriental", 287, 800, F1, (0, 1), r, collide=False)
P("sofa_butter", 287, 930, F1, (0, -1), r); P("coffee_table_glass", 287, 800, F1, (0, -1), r)
P("candy_dish", 262, 770, F1 + 45.4, (1, 0), r, collide=False); P("magazine", 318, 786, F1 + 45.8, (0.9, 0.3), r, collide=False)
P("vhs_tape", 300, 760, F1 + 46, (0.8, 0.5), r, tags=["inspect"])
P("armchair_cream", 96, 760, F1, (1, 0.25), r)
P("side_table", 420, 905, F1, (0, -1), r)
switch("living_table", "table_lamp_drum", 420, 880, F1 + 55, (1, 0), r, "living_table", lit=True); shaded("living_table", 420, 880, F1 + 100, 750, r, "living_table", C1, 480)
PW("piano", "living", "x1", 200, room=r); P("piano_bench", 487, 800, F1, (-1, 0), r)
P("globe", 556, 748, F1 + 108, (-1, 0), r, collide=False); P("bust", 556, 852, F1 + 108, (-1, 0), r, collide=False)
switch("piano", "piano_lamp", 556, 800, F1 + 108, (-1, 0), r, "piano", lit=True); lamp("piano", 542, 800, F1 + 128, 250, r, "piano", 300)
PW("frame_landscape_a", "living", "x1", 200, 180, room=r, collide=False)
twin(0, "frame_family_a", "frame_family_c", "living", "y1", 200, 150, r)              # anomaly: the family now has their backs to the camera
PW("mirror_wall", "living", "y1", 330, 165, room=r, collide=False); PW("spindle_chair", "living", "y1", 120, room=r)
PW("curtain_rod", "living", "x0", 240, 224, 2, room=r, collide=False)
PW("curtain_living", "living", "x0", 96, 32, 3, room=r, collide=False); PW("curtain_living", "living", "x0", 384, 32, 3, room=r, collide=False)
P("fake_plant", 28, 632, F1, (1, 0), r); switch("torchiere", "torchiere", 30, 1030, F1, (1, 0), r, "torchiere", lit=True)
lamp("torchiere", 30, 1030, F1 + 184, 3800, r, "torchiere", 340, temp=2950, spot=(90, 80)); lamp("torchiere_spill", 30, 1030, F1 + 176, 140, r, "torchiere", 220, temp=2950, shadows=False)
fixture("ceiling_fan", 287, 832, C1, (1, 0), r, "living"); lamp("living_fan", 287, 832, C1 - 52, 300, r, "living", 520)
(sx, sy), f = HP.at("living", "y1", 440, 0.2); switch("living", "light_switch", sx, sy, F1 + 120, f, r, "living")
PW("thermostat", "living", "y1", 400, 150, room=r, collide=False); PW("outlet", "living", "x0", 60, 30, room=r, collide=False)

# ---------------- dining room: the one room with the cream damask paper ----------------
r = "Dining"
P("rug_oriental", 287, 1765, F1, (1, 0), r, collide=False)
P("dining_table", 287, 1765, F1, (0, 1), r)
for (x, y, f) in ((225, 1688, (0, 1)), (345, 1688, (0, 1)), (225, 1842, (0, -1)), (170, 1765, (1, 0)), (404, 1765, (-1, 0))):
    P("spindle_chair", x, y, F1, f, r)
P("spindle_chair", 345, 1842, F1, (0, -1), r, tags=["dy8n"])                           # anomaly: this chair is pulled out, as if someone just stood up
hidden(P("spindle_chair", 372, 1890, F1, (-0.45, -1), r, collide=False, tags=["dy8"]))
PW("hutch", "dining", "y1", 470, room=r)
PW("side_table", "dining", "x1", 70, room=r); P("fruit_bowl", 550, 1641, F1 + 55, (-1, 0), r, collide=False)
PW("frame_portrait", "dining", "x1", 70, 165, room=r, collide=False); PW("frame_landscape_a", "dining", "y0", 440, 165, room=r, collide=False)
PW("curtain_living", "dining", "x0", 96, 32, 3, room=r, collide=False); PW("curtain_living", "dining", "x0", 304, 32, 3, room=r, collide=False)
PW("curtain_rod", "dining", "x0", 199, 224, 2, room=r, collide=False)
P("jar_candle", 287, 1740, F1 + 76.5, (1, 0), r, collide=False); P("jar_candle", 287, 1790, F1 + 76.5, (1, 0), r, collide=False)
room_light("dining", "dining", 287, 1765, 900, sw=("y0", 372), on=False, stage=2, prop="pendant", drop=70, room=r)

# ---------------- kitchen and nook: butter cream, fruit border under the ceiling, sheet vinyl ----------------
r = "Kitchen"
PW("fridge_body", "kitchen", "x1", 38, room=r, tags=["fridge"]); PW("popcorn_tin", "kitchen", "x1", 38, 168, 32, room=r, collide=False)
PW("cab_base_60", "kitchen", "x1", 106, room=r); PW("cab_sink_90", "kitchen", "x1", 181, room=r)
PW("cab_drawer_shell", "kitchen", "x1", 256, room=r); PW("stove", "kitchen", "x1", 324, room=r)
PW("cab_upper_90", "kitchen", "x1", 121, 140, room=r); PW("cab_upper_90", "kitchen", "x1", 309, 140, room=r)
PW("valance_red", "kitchen", "x1", 168, 172, 1, room=r, collide=False)
for along in (214, 304, 379):
    PW("cab_base_90" if along < 350 else "cab_base_60", "kitchen", "y0", along, room=r)
PW("cab_upper_90", "kitchen", "y0", 214, 140, room=r); PW("cab_upper_90", "kitchen", "y0", 304, 140, room=r)
PW("microwave", "kitchen", "y0", 300, 91, 2, room=r); PW("cereal_a", "kitchen", "y0", 380, 91, 20, room=r, collide=False)
PW("mugs", "kitchen", "y0", 214, 91, 24, room=r, collide=False); PW("rooster", "kitchen", "y0", 250, 91, 20, room=r, collide=False)
PW("dish_towel", "kitchen", "x1", 324, 80, 69, room=r, collide=False); PW("cookie_tin", "kitchen", "x1", 106, 91, 22, room=r, collide=False)
for (tag, prop) in (("dy2n", "fridge_magnets"), ("dy2", "fridge_magnets_b")):         # anomaly: a magnet has slid down the fridge, and the drawing gained a figure
    c = PW(prop, "kitchen", "x1", 62, 156, 71.4, room=r, collide=False, tags=[tag])
    if tag == "dy2": hidden(c)
hidden(PW("kid_drawing_b", "kitchen", "x1", 47, 134, 71.7, room=r, collide=False, tags=["dy2"]))
PW("hutch", "kitchen", "x0", 150, room=r); PW("mail_keys", "kitchen", "x0", 110, 94, 26, room=r, collide=False); PW("tablet", "kitchen", "x0", 190, 94, 26, room=r, collide=False)
PW("wall_phone", "kitchen", "x0", 420, 140, room=r, collide=False); PW("calendar_wall", "kitchen", "x0", 380, 160, room=r, collide=False)
PW("note_mom", "kitchen", "x0", 452, 150, room=r, tags=["inspect"])
twin(3, "clock_kitchen", "clock_wall_same", "kitchen", "y1", 110, 190, r)
P("kitchen_table", 800, 1180, F1, (1, 0), r); P("fruit_bowl", 800, 1160, F1 + 76, (1, 0), r, collide=False); P("laptop", 802, 1212, F1 + 76, (1, 0.2), r, collide=False)
for (x, y, f) in ((716, 1150, (1, 0)), (716, 1215, (1, 0.1)), (884, 1180, (-1, 0)), (800, 1290, (0, -1))):
    P("kitchen_chair", x, y, F1, f, r)
P("kitchen_bin", 604, 882, F1, (1, 0), r)
room_light("kitchen", "kitchen", 833, 1010, 1000, sw=("x0", 466), on=True, stage=2, room=r)
room_light("kitchen", "kitchen", 800, 1210, 700, on=True, room=r, prop="pendant", drop=70)
fixture("track_light", 990, 1090, C1, (1, 0), r, "kitchen", on=True)
for y in (1040, 1090, 1140):
    lamp("track_%d" % y, 996, y, C1 - 20, 380, r, "kitchen", 280, temp=3000, shadows=(y == 1090), on=True, spot=(-58, 38))
border("kitchen", "border_1m_fruit", room=r)
PW("outlet", "kitchen", "x1", 256, 110, room=r, collide=False); PW("vent", "kitchen", "x0", 300, 12, room=r, collide=False)

# ---------------- laundry / mudroom ----------------
r = "Mud"
PW("washer", "mud", "x0", 58, room=r, tags=["ch_washer"], movable=True); PW("dryer", "mud", "x0", 130, room=r, tags=["ch_dryer"], movable=True)
PW("laundry_shelf", "mud", "x0", 94, 150, room=r, collide=False)
PW("coat_hooks", "mud", "x1", 50, 165, room=r, collide=False); PW("shoes", "mud", "y1", 30, 0, 20, room=r, collide=False)
PW("backpack", "mud", "x1", 215, 0, 22, room=r, collide=False)
room_light("mud", "mud", 718, 725, 700, sw=("y1", 160), on=True, stage=2, room=r)

# ---------------- half bath: powder blue, small mosaic floor ----------------
r = "Halfbath"
PW("toilet", "halfbath", "x1", 195, room=r); PW("vanity", "halfbath", "y0", 128, room=r)
PW("medicine_cabinet", "halfbath", "y0", 128, 150, room=r, collide=False); PW("towel_bar", "halfbath", "y1", 150, 125, room=r, collide=False)
PW("seashell_soap", "halfbath", "y0", 112, 82, 16, room=r, collide=False); PW("toilet_set", "halfbath", "x1", 195, room=r, collide=False)
room_light("halfbath", "halfbath", 970, 725, 600, sw=("x0", 212), on=False, stage=2, room=r)

# ---------------- family room / den: tan walls, burgundy accent wall, dark multi-tone carpet ----------------
r = "Den"
PW("entertainment_center", "den", "y1", 87, room=r)                                   # the television stands against the burgundy wall
for (tag, on) in (("dy7n", False), ("dy7", True)):                                    # anomaly: the television is on, showing static
    c = P(PF.variant("flat_tv", on), 673, 1954, F1 + 66, (0, -1), r, collide=False, tags=[tag])
    if on: hidden(c)
g = lamp("tv_glow", 673, 1880, F1 + 96, 160, r, "none", 420, temp=9000, shadows=False); g.tags = ["dress", "dy7"]
PW("dvd_player", "den", "y1", 87, 35.5, 8, room=r, collide=False); PW("console_2010", "den", "y1", 139, 66, 8, room=r, collide=False)
PW("router", "den", "y1", 35, 66, 8, room=r, collide=False)
P("loveseat_tan", 770, 1660, F1, (0, 1), r); P("rug", 745, 1800, F1, (0, 1), r, collide=False)
PW("couch", "den", "x1", 248, room=r); P("armchair_rust", 1040, 1905, F1, (-0.75, -0.65), r)
P("tv_tray", 900, 1790, F1, (1, 0), r); P("remote_mug", 900, 1790, F1 + 62, (0.3, 1), r, collide=False); P("toy_bin", 1036, 1500, F1, (-1, 0), r)
PW("bookshelf", "den", "x1", 60, room=r)
twin(3, "clock_den", "clock_wall_same", "den", "y0", 74, 188, r)
PW("frame_portrait", "den", "y0", 440, 165, room=r, collide=False); PW("faded_rect", "den", "x0", 420, 160, room=r, collide=False)
PW("curtain_living", "den", "x1", 110, 32, 3, room=r, collide=False); PW("curtain_living", "den", "x1", 386, 32, 3, room=r, collide=False)
PW("curtain_rod", "den", "x1", 248, 224, 2, room=r, collide=False)
switch("den_lamp", "floor_lamp", 1050, 1575, F1, (-1, 0), r, "den_lamp", lit=True); lamp("den_lamp", 1050, 1575, F1 + 150, 500, r, "den_lamp", 420)
room_light("den", "den", 833, 1711, 800, sw=("y0", 400), on=False, stage=3, room=r)
print("floor 1 dressed")
