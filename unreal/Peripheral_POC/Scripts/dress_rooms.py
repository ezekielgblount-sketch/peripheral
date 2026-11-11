"""Furnishes every room in the slice. Safe to re-run: rebuilds everything tagged 'dress'. Positions are blueprint cm."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF
importlib.reload(L); importlib.reload(K); importlib.reload(PF)
import props_small as PS
import props_90s as P9
import props_home as PH
import props_lived as PL
import props_story as PST
try:
    import props_pool as PP
except ImportError:
    pass
importlib.reload(PS)
LND, F1, C1, F2, C2 = -126, 0, 244, 259, 503
L.clear("dress")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
count = {}

def P(prop, x, y, z, face, room, collide=True, tag=None):
    count[prop] = count.get(prop, 0) + 1
    a = K.place(PF.get(prop), "%s_%s_%d" % (room, prop, count[prop]), x, y, z, face=face, folder="Dress/" + room, tag="dress", collide=collide)
    if tag:
        a.tags = ["dress", tag]
    if tag == "inspect":
        a.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    return a

def lamp(name, x, y, z, lumens, room, radius=600, color=(255, 214, 160), shadows=True, always=False):
    """A warm bulb. Lamps are off by day; the day/night switch turns them on (tag 'night_light')."""
    a = eas.spawn_actor_from_class(unreal.PointLight, L.to_ue(x, y, z))
    a.set_actor_label("Lamp_" + name); a.set_folder_path("Dress/" + room); grp = {"entry": 1, "hall": 1, "kitchen_800": 2, "kitchen_1250": 2, "hall2": 3, "bath": 4}.get(name, 4)
    a.tags = ["dress", "power_light", "power_%d" % grp] if always else ["dress", "night_light"]
    c = a.light_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
    c.set_editor_property("intensity", lumens)
    c.set_editor_property("light_color", unreal.Color(r=color[0], g=color[1], b=color[2], a=255))
    c.set_editor_property("attenuation_radius", radius)
    c.set_editor_property("source_radius", 4.0)
    c.set_editor_property("cast_shadows", shadows)
    if not always:
        a.set_actor_hidden_in_game(True)             # off by day; BP_World un-hides lamps at night
    return a

def border(x0, y0, x1, y1, z, prop, room):
    """Wallpaper border strip around a room, just under the ceiling, in 1 m pieces."""
    for y in range(int(y0) + 50, int(y1) + 50, 100):
        P(prop, x0 + 0.3, min(y, y1 - 50), z, (1, 0), room, collide=False); P(prop, x1 - 0.3, min(y, y1 - 50), z, (-1, 0), room, collide=False)
    for x in range(int(x0) + 50, int(x1) + 50, 100):
        P(prop, min(x, x1 - 50), y0 + 0.3, z, (0, 1), room, collide=False); P(prop, min(x, x1 - 50), y1 - 0.3, z, (0, -1), room, collide=False)

# ---------------- entry and stair core ----------------
r = "Entry"
P("doormat", 45, 1136, LND, (1, 0), r, collide=False)
P("coat_hooks", 95, 1033, LND + 165, (0, 1), r, collide=False)
P("light_switch", 2, 1200, LND + 120, (1, 0), r, collide=False); lamp("entry", 90, 1140, LND + 215, 700, r, 450, always=True)
fx = K.Kit()                                                 # handrails and half-wall caps, in world coordinates
def u(x, y, z): return (x - L.OX, -(y - L.OY), z)
def rail(p0, p1):
    fx.tube("rail", u(*p0), u(*p1), 2.2, 10)
    for f in (0.1, 0.5, 0.9):
        m = [p0[i] + (p1[i] - p0[i]) * f for i in range(3)]
        fx.tube("brass", u(m[0], m[1], m[2] - 3), u(m[0] + (p0[3] if len(p0) > 3 else 0), m[1], m[2] - 6), 0.7, 6)
def cap(x0, y0, x1, y1, z):
    fx.box("rail", x0 - 1 - L.OX, -(y1 + 1 - L.OY), z, x1 + 1 - L.OX, -(y0 - 1 - L.OY), z + 4)
rail((6, 1251, LND + 18 + 92), (6, 1419, F1 + 92))                                   # up flight, on the front wall
rail((180, 1037, LND + 92), (348, 1037, LND - 108 + 92))                             # basement flight
rail((470, 1147, 92), (106, 1147, F2 + 92))                                          # stair to floor 2
cap(100, 1251, 112, 1419, F1 + 95); cap(376, 1031, 388, 1129, F1 + 95)
cap(100, 1239, 470, 1251, F2 + 91); cap(470, 1141, 482, 1239, F2 + 91)
def crown(x0, y0, x1, y1, z):                               # white crown moulding round a room
    for (a0, b0, a1, b1) in ((x0, y0, x1, y0 + 7), (x0, y1 - 7, x1, y1), (x0, y0, x0 + 7, y1), (x1 - 7, y0, x1, y1)):
        fx.box("white", a0 - L.OX, -(b1 - L.OY), z - 8, a1 - L.OX, -(b0 - L.OY), z)
crown(0, 600, 574, 1019, C1)
for y in (700, 900, 1100, 1300, 1480):                      # kitchen ceiling beams
    fx.box("wood_dark", 586 - L.OX, -(y + 7 - L.OY), C1 - 12, 900 - L.OX, -(y - 7 - L.OY), C1)
for i in range(18):                                         # shiplap ceiling in Jack's room
    fx.box("shiplap", 578 - L.OX, -(1356 + (i + 1) * 19.1 - L.OY), C2 - 2 - (i % 2) * 0.4, 900 - L.OX, -(1356 + i * 19.1 - L.OY), C2)
a = eas.spawn_actor_from_object(fx.save("dress_fixed", local=False), unreal.Vector(0, 0, 0))
a.set_actor_label("Rails_and_caps"); a.set_folder_path("Dress/Entry"); a.tags = ["dress"]
a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)

# ---------------- hall, floor 1 ----------------
r = "Hall"
P("ceiling_light_off", 340, 1380, C1, (1, 0), r, collide=False); lamp("hall", 340, 1380, C1 - 22, 900, r, always=True)
P("side_table", 572, 1460, F1, (-1, 0), r); P("table_lamp", 547, 1460, F1 + 55, (1, 0), r, collide=False)
lamp("hall_table", 547, 1460, F1 + 88, 350, r, 400)
P("frame_school", 200, 1512, F1 + 155, (0, -1), r, collide=False); P("frame_school_b", 160, 1512, F1 + 150, (0, -1), r, collide=False)
P("secretary", 388, 1513, F1, (0, -1), r); P("frame_school", 372, 1500, F1 + 117, (0.2, -1), r, collide=False); P("jar_candle", 410, 1500, F1 + 110, (0, -1), r, collide=False)
P("frame_map", 388, 1512.5, F1 + 170, (0, -1), r, collide=False); P("barometer", 470, 1512, F1 + 165, (0, -1), r, collide=False)
P("key_bowl", 548, 1478, F1 + 55, (1, 0), r, collide=False); P("phone_book", 556, 1460, F1 + 38.2, (-1, 0), r, collide=False); P("height_marks", 573.6, 1294, F1 + 70, (-1, 0), r, collide=False)
P("faded_rect", 573.8, 1180, F1 + 160, (-1, 0), r, collide=False)
P("phone_cordless", 552, 1438, F1 + 55, (-1, 0.2), r, collide=False)
P("light_switch", 572, 1420, F1 + 120, (-1, 0), r, collide=False); P("outlet", 572, 1100, F1 + 30, (-1, 0), r, collide=False)
P("vent", 300, 1512, F1 + 12, (0, -1), r, collide=False)

# ---------------- living room (reference photos A-D): piano corner, seating, built-ins, fireplace, parents' TV ----------------
r = "Living"
P("rug_oriental", 330, 800, F1, (0, 1), r, collide=False)
P("piano", 92, 603, F1, (0, 1), r); P("piano_bench", 92, 690, F1, (0, 1), r)
P("globe", 40, 618, F1 + 108, (1, 0), r, collide=False); P("piano_lamp", 100, 616, F1 + 108, (0, 1), r, collide=False); P("bust", 150, 618, F1 + 108, (0, 1), r, collide=False)
lamp("piano", 100, 630, F1 + 128, 250, r, 300)
P("frame_landscape_a", 92, 601, F1 + 180, (0, 1), r, collide=False); P("spindle_chair", 200, 603, F1, (0, 1), r)
P("sofa_butter", 345, 603, F1, (0, 1), r); P("mirror_wall", 345, 601, F1 + 170, (0, 1), r, collide=False)
P("bracket_pitcher", 262, 601, F1 + 150, (0, 1), r, collide=False); P("bracket_pitcher", 428, 601, F1 + 150, (0, 1), r, collide=False)
P("sign_faith", 262, 601, F1 + 192, (0, 1), r, collide=False)
P("coffee_table_glass", 345, 722, F1, (0, 1), r); P("vhs_tape", 372, 742, F1 + 46, (0.8, 0.5), r, tag="inspect")
P("candy_dish", 318, 748, F1 + 45.4, (1, 0), r, collide=False); P("remote_ziplock", 380, 770, F1 + 45.4, (0.4, 1), r, collide=False)
P("side_table", 492, 603, F1, (0, 1), r); P("table_lamp_drum", 492, 628, F1 + 55, (1, 0), r, collide=False); P("jar_candle", 478, 640, F1 + 55, (1, 0), r, collide=False)
lamp("living_table", 492, 628, F1 + 100, 650, r, 550)
P("armchair_cream", 5, 930, F1, (1, 0), r); P("chair_sage", 5, 800, F1, (1, 0.12), r); P("fake_plant", 26, 1000, F1, (1, 0), r)
P("entertainment_center", 250, 1017, F1, (0, -1), r); P("flat_tv", 250, 1012, F1 + 66, (0, -1), r, collide=False)
P("dvd_player", 250, 1008, F1 + 35.5, (0, -1), r, collide=False); P("console_2010", 302, 1008, F1 + 66, (0, -1), r, collide=False)
P("router", 198, 1010, F1 + 66, (0, -1), r, collide=False); P("fall_stems", 180, 1004, F1 + 66, (0, -1), r, collide=False)
P("frame_portrait", 250, 1017.5, F1 + 172, (0, -1), r, collide=False); P("faded_rect", 112, 1017.8, F1 + 160, (0, -1), r, collide=False)
P("fireplace", 573, 708, F1, (-1, 0), r); P("frame_landscape_b", 573, 708, F1 + 203, (-1, 0), r, collide=False)
P("bookshelf_white", 573, 868, F1, (-1, 0), r); P("keepsake_box", 566, 845, F1 + 55, (-1, 0), r, collide=False); P("albums", 564, 878, F1 + 11, (-1, 0), r, collide=False)
P("ottoman", 488, 760, F1, (1, 0), r)
P("curtain_rod", 2, 820, F1 + 224, (1, 0), r, collide=False)
P("curtain_living", 3, 672, F1 + 32, (1, 0), r, collide=False); P("curtain_living", 3, 966, F1 + 32, (1, 0), r, collide=False)
P("ceiling_fan", 300, 810, C1, (1, 0), r, collide=False); lamp("living_fan", 300, 810, C1 - 52, 700, r)
P("thermostat", 1, 985, F1 + 150, (1, 0), r, collide=False)
P("light_switch", 450, 1017, F1 + 120, (0, -1), r, collide=False); P("outlet", 130, 601, F1 + 30, (0, 1), r, collide=False)
P("charger", 2, 1000, F1 + 30, (1, 0), r, collide=False); P("vent", 572, 930, F1 + 12, (-1, 0), r, collide=False)

# ---------------- kitchen (honey-maple cabinets, yellow walls, red floral valance, ceiling beams) ----------------
r = "Kitchen"
P("fridge_body", 898, 645, F1, (-1, 0), r, tag="fridge"); P("popcorn_tin", 866, 645, F1 + 168, (1, 0), r, collide=False)
P("cab_base_60", 898, 715, F1, (-1, 0), r); P("cab_sink_90", 898, 820, F1, (-1, 0), r)
P("cab_drawer_shell", 898, 895, F1, (-1, 0), r); P("stove", 898, 965, F1, (-1, 0), r)
P("cab_upper_90", 898, 730, F1 + 140, (-1, 0), r); P("cab_upper_90", 898, 950, F1 + 140, (-1, 0), r)
P("valance_red", 897, 820, F1 + 172, (-1, 0), r, collide=False); P("valance_red", 897, 1360, F1 + 186, (-1, 0), r, collide=False)
P("microwave", 896, 715, F1 + 91, (-1, 0), r); P("cereal_a", 875, 1005, F1 + 91, (-1, 0.3), r, collide=False)
P("hutch", 587, 1100, F1, (1, 0), r)
P("kitchen_table", 845, 1360, F1, (1, 0), r); P("pendant", 845, 1360, C1, (1, 0), r, collide=False)
P("kitchen_chair", 762, 1332, F1, (1, 0), r); P("kitchen_chair", 845, 1470, F1, (0, -1), r)
P("wall_phone", 588, 1262, F1 + 140, (1, 0), r, collide=False); P("wall_clock", 588, 820, F1 + 185, (1, 0), r, collide=False)
for y in (800, 1250):
    P("ceiling_light_off", 743, y, C1, (1, 0), r, collide=False); lamp("kitchen_%d" % y, 743, y, C1 - 22, 1100, r, 700, (255, 228, 190), always=True)
P("light_switch", 588, 1410, F1 + 120, (1, 0), r, collide=False); P("outlet", 898, 880, F1 + 110, (-1, 0), r, collide=False)

# ---------------- upstairs hall ----------------
r = "Hall2"
P("ceiling_light_off", 250, 1310, C2, (1, 0), r, collide=False); lamp("hall2", 250, 1310, C2 - 22, 900, r, always=True)
P("frame_school_b", 330, 1369, F2 + 152, (0, -1), r, collide=False); P("kid_drawing", 392, 1369, F2 + 140, (0, -1), r, collide=False)
P("light_switch", 564, 1262, F2 + 120, (-1, 0), r, collide=False); P("vent", -28, 1210, F2 + 12, (1, 0), r, collide=False)

# ---------------- Jack's bedroom ----------------
r = "Bedroom"
P("bed_unmade", 736, 1698, F2, (0, -1), r)
P("teddy", 664, 1612, F2, (0.6, -1), r, tag="inspect")
P("dresser", 580, 1600, F2, (1, 0), r); P("boombox", 584, 1626, F2 + 83, (1, 0), r, tag="inspect")
P("desk_wood", 898, 1525, F2, (-1, 0), r); P("chair_red", 786, 1530, F2, (1, 0.1), r)
P("lamp_mint", 876, 1484, F2 + 76.6, (-1, 0.4), r, collide=False); P("cd_player", 866, 1574, F2 + 76.6, (-1, 0), r, collide=False); lamp("bed_desk", 872, 1488, F2 + 108, 400, r, 450)
P("craft_drawers", 628, 1698, F2, (0, -1), r)
P("toy_blocks", 700, 1440, F2, (1, 0.3), r, collide=False); P("toy_ball", 884, 1440, F2, (1, 0), r, tag="inspect")
P("toy_car", 756, 1462, F2, (0.6, 1), r, tag="inspect")
P("chart_alphabet", 579, 1520, F2 + 155, (1, 0), r, collide=False); P("chart_fractions", 820, 1357, F2 + 165, (0, 1), r, collide=False)
P("shelf_wall", 700, 1357, F2 + 120, (0, 1), r, collide=False)
P("curtain_bed", 664, 1697, F2 + 78, (0, -1), r, collide=False); P("curtain_bed", 808, 1697, F2 + 78, (0, -1), r, collide=False)
P("curtain_bed", 897, 1452, F2 + 78, (-1, 0), r, collide=False); P("curtain_bed", 897, 1598, F2 + 78, (-1, 0), r, collide=False)
P("pc_monitor", 892, 1548, F2 + 75, (-1, 0), r, collide=False); P("pc_keyboard", 851, 1548, F2 + 75, (-1, 0), r, collide=False)
P("pc_tower", 898, 1598, F2, (-1, 0), r)
P("glow_stars", 736, 1600, C2 - 2.2, (1, 0), r, collide=False); P("poster_band", 648, 1357, F2 + 165, (0, 1), r, collide=False)
P("plush_pile", 866, 1658, F2, (-1, -0.3), r, collide=False); P("handheld", 720, 1590, F2 + 52, (0.4, -1), r, tag="inspect"); P("card_binder", 640, 1440, F2, (0.8, 0.5), r, collide=False)
P("learning_tablet", 800, 1640, F2, (0.3, 1), r, collide=False); P("backpack", 838, 1412, F2, (-0.6, 0.6), r, collide=False)
P("ceiling_light_off", 740, 1530, C2, (1, 0), r, collide=False); lamp("bedroom", 740, 1530, C2 - 22, 900, r)
P("light_switch", 580, 1492, F2 + 120, (1, 0), r, collide=False); P("outlet", 580, 1680, F2 + 30, (1, 0), r, collide=False)

# ---------------- bathroom ----------------
r = "Bath"
P("bathtub", 898, 1235, F2, (-1, 0), r)
P("shower_curtain", 824, 1275, F2 + 22, (-1, 0), r, collide=False)
P("toilet", 770, 1342, F2, (0, -1), r); P("vanity", 782, 1128, F2, (0, 1), r)
P("medicine_cabinet", 782, 1127, F2 + 150, (0, 1), r, collide=False)
P("towels_deco", 640, 1342, F2 + 125, (0, -1), r, collide=False); P("toilet_set", 770, 1342, F2, (0, -1), r, collide=False)
P("seashell_soap", 765, 1142, F2 + 82, (0, 1), r, collide=False); P("mouthwash", 812, 1140, F2 + 82, (0, 1), r, collide=False)
P("doormat", 780, 1235, F2, (0, 1), r, collide=False)
P("ceiling_light_off", 700, 1235, C2, (1, 0), r, collide=False); lamp("bath", 700, 1235, C2 - 22, 900, r, 500, (255, 236, 205), always=True)
P("light_switch", 580, 1262, F2 + 120, (1, 0), r, collide=False)
# ---------------- lived-in clutter: the family left mid-day and never got back to tidy ----------------
r = "Lived"
P("note_mom", 587, 1235, F1 + 150, (1, 0), r, tag="inspect")
P("calendar_wall", 587, 1440, F1 + 160, (1, 0), r, collide=False)
P("laptop", 846, 1392, F1 + 76, (1, 0.2), r, collide=False); P("fruit_bowl", 846, 1330, F1 + 76, (1, 0), r, collide=False)
P("cookie_tin", 612, 1150, F1 + 94, (1, 0), r, collide=False); P("tablet", 614, 1105, F1 + 94, (1, 0.3), r, collide=False); P("mugs", 872, 760, F1 + 91, (-1, 0), r, collide=False)
P("rooster", 872, 892, F1 + 91, (-1, 0.3), r, collide=False); P("charger", 898, 880, F1 + 110, (-1, 0), r, collide=False); P("sconce", 899, 1250, F1 + 165, (-1, 0), r, collide=False)
P("mug_sink" if False else "dishes", 868, 800, F1 + 91.6, (-1, 0.2), r, collide=False)
P("dish_towel", 829, 965, F1 + 80, (-1, 0), r, collide=False); P("mail_keys", 612, 1060, F1 + 94, (1, 0.2), r, collide=False)
P("shoes", 40, 1075, LND, (1, 0.3), r, collide=False); P("shoes", 130, 1470, F1, (0, -1), r, collide=False)
P("magazine", 262, 765, F1 + 45.8, (0.9, 0.3), r, collide=False); P("remote_mug", 236, 748, F1 + 45.8, (0.3, 1), r, collide=False)
P("magazine", 300, 960, F1 + 51, (0.2, -1), r, collide=False)
P("clothes_floor", 690, 1610, F2, (1, 0.4), r, collide=False); P("clothes_floor", 660, 1500, F2, (0.2, 1), r, collide=False)
P("homework", 862, 1500, F2 + 76.7, (-1, 0.2), r, tag="inspect"); P("homework", 760, 1425, F2, (0.7, 0.6), r, collide=False)
P("laundry_basket", 612, 1305, F2, (1, 0), r)
P("towel_floor", 700, 1290, F2, (1, 0.5), r, collide=False); P("bath_bits", 790, 1140, F2 + 82, (0, 1), r, collide=False)
P("clothes_floor", 110, 640, F1, (0.5, 1), r, collide=False)
for a_ in eas.get_all_level_actors():                       # fan blades left a dark blotch on the ceiling: no shadows from them
    if "ceiling_fan" in a_.get_actor_label() or "glow_stars" in a_.get_actor_label():
        a_.static_mesh_component.set_cast_shadow(False)
        a_.static_mesh_component.set_editor_property("affect_distance_field_lighting", False)
print("dressed:", sum(count.values()), "props")
