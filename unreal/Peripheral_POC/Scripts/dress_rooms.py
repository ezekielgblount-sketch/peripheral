"""Furnishes every room in the slice. Safe to re-run: rebuilds everything tagged 'dress'. Positions are blueprint cm."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF
importlib.reload(L); importlib.reload(K); importlib.reload(PF)
import props_small as PS
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
    return a


def lamp(name, x, y, z, lumens, room, radius=600, color=(255, 214, 160), shadows=True):
    """A warm bulb. Lamps are off by day; the day/night switch turns them on (tag 'night_light')."""
    a = eas.spawn_actor_from_class(unreal.PointLight, L.to_ue(x, y, z))
    a.set_actor_label("Lamp_" + name); a.set_folder_path("Dress/" + room); a.tags = ["dress", "night_light"]
    c = a.light_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
    c.set_editor_property("intensity", lumens)
    c.set_editor_property("light_color", unreal.Color(r=color[0], g=color[1], b=color[2], a=255))
    c.set_editor_property("attenuation_radius", radius)
    c.set_editor_property("source_radius", 4.0)
    c.set_editor_property("cast_shadows", shadows)
    c.set_visibility(False)
    return a


# ---------------- entry and stair core ----------------
r = "Entry"
P("doormat", 45, 1136, LND, (1, 0), r, collide=False)
P("coat_hooks", 95, 1033, LND + 165, (0, 1), r, collide=False)
P("box_fragile", 158, 1229, LND, (-1, 0.2), r)
P("light_switch", 2, 1200, LND + 120, (1, 0), r, collide=False)
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
a = eas.spawn_actor_from_object(fx.save("dress_fixed", local=False), unreal.Vector(0, 0, 0))
a.set_actor_label("Rails_and_caps"); a.set_folder_path("Dress/Entry"); a.tags = ["dress"]
a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)

# ---------------- hall, floor 1 ----------------
r = "Hall"
P("ceiling_light_off", 340, 1380, C1, (1, 0), r, collide=False); lamp("hall", 340, 1380, C1 - 22, 900, r)
P("side_table", 572, 1460, F1, (-1, 0), r); P("table_lamp", 547, 1460, F1 + 55, (1, 0), r, collide=False)
lamp("hall_table", 547, 1460, F1 + 88, 350, r, 400)
P("frame_school", 200, 1512, F1 + 155, (0, -1), r, collide=False); P("frame_school_b", 160, 1512, F1 + 150, (0, -1), r, collide=False)
P("box_misc", 440, 1488, F1, (0, -1), r); P("box_plain", 502, 1488, F1, (0.2, -1), r); P("box_books", 468, 1488, F1 + 45, (0, -1), r)
P("light_switch", 572, 1420, F1 + 120, (-1, 0), r, collide=False); P("outlet", 572, 1100, F1 + 30, (-1, 0), r, collide=False)
P("vent", 300, 1512, F1 + 12, (0, -1), r, collide=False)

# ---------------- living room ----------------
r = "Living"
P("rug", 290, 800, F1, (0, 1), r, collide=False)
P("couch", 280, 603, F1, (0, 1), r)
P("coffee_table", 280, 722, F1, (0, 1), r)
P("side_table", 420, 603, F1, (0, 1), r); P("table_lamp", 420, 628, F1 + 55, (1, 0), r, collide=False)
lamp("living_table", 420, 628, F1 + 90, 500, r, 500)
P("armchair", 62, 668, F1, (0.75, 0.66), r)
P("tv_console", 250, 1016, F1, (0, -1), r); P("crt_tv", 215, 1014, F1 + 60, (0, -1), r)
P("vcr", 284, 1010, F1 + 35, (0, -1), r, collide=False); P("vhs_stack", 300, 1004, F1 + 60, (0.3, -1), r, collide=False)
P("bookshelf", 572, 780, F1, (-1, 0), r)
P("floor_lamp", 30, 975, F1, (1, 0), r); lamp("living_floor", 45, 975, F1 + 150, 800, r)
P("curtain_rod", 2, 820, F1 + 224, (1, 0), r, collide=False)
P("curtain_living", 3, 684, F1 + 32, (1, 0), r, collide=False); P("curtain_living", 3, 956, F1 + 32, (1, 0), r, collide=False)
P("frame_school", 205, 601, F1 + 152, (0, 1), r, collide=False); P("frame_school_b", 352, 601, F1 + 150, (0, 1), r, collide=False)
P("box_living", 500, 650, F1, (-1, 0.15), r); P("box_plain", 498, 652, F1 + 45, (-1, -0.2), r); P("box_books", 130, 996, F1, (-0.4, -1), r)
P("box_fragile", 520, 720, F1, (-1, 0.4), r)
P("light_switch", 450, 1017, F1 + 120, (0, -1), r, collide=False); P("outlet", 130, 601, F1 + 30, (0, 1), r, collide=False)
P("outlet", 2, 1000, F1 + 30, (1, 0), r, collide=False); P("vent", 572, 640, F1 + 12, (-1, 0), r, collide=False)

# ---------------- kitchen ----------------
r = "Kitchen"
P("fridge", 898, 645, F1, (-1, 0), r, tag="fridge")
P("cab_base_60", 898, 715, F1, (-1, 0), r); P("cab_sink_90", 898, 820, F1, (-1, 0), r)
P("cab_drawer_shell", 898, 895, F1, (-1, 0), r); P("stove", 898, 965, F1, (-1, 0), r)
P("cab_upper_90", 898, 730, F1 + 140, (-1, 0), r); P("cab_upper_90", 898, 950, F1 + 140, (-1, 0), r)
P("curtain_kitchen", 897, 820, F1 + 172, (-1, 0), r, collide=False)
P("kitchen_table", 845, 1360, F1, (1, 0), r)
P("kitchen_chair", 762, 1332, F1, (1, 0), r); P("kitchen_chair", 760, 1392, F1, (1, 0.15), r); P("kitchen_chair", 845, 1470, F1, (0, -1), r)
P("wall_phone", 588, 1262, F1 + 140, (1, 0), r, collide=False)
P("wall_clock", 588, 820, F1 + 185, (1, 0), r, collide=False)
P("box_kitchen", 868, 715, F1 + 91, (-1, 0.1), r); P("box_kitchen", 612, 905, F1, (1, 0.1), r); P("box_plain", 612, 965, F1, (1, -0.05), r)
P("box_fragile", 845, 1350, F1 + 76, (-1, 0.3), r)
for y in (800, 1250):
    P("ceiling_light_off", 743, y, C1, (1, 0), r, collide=False); lamp("kitchen_%d" % y, 743, y, C1 - 22, 1100, r, 700, (255, 228, 190))
P("light_switch", 588, 1410, F1 + 120, (1, 0), r, collide=False); P("outlet", 898, 880, F1 + 110, (-1, 0), r, collide=False)

# ---------------- upstairs hall ----------------
r = "Hall2"
P("ceiling_light_off", 250, 1310, C2, (1, 0), r, collide=False); lamp("hall2", 250, 1310, C2 - 22, 900, r)
P("frame_school_b", 330, 1369, F2 + 152, (0, -1), r, collide=False); P("kid_drawing", 392, 1369, F2 + 140, (0, -1), r, collide=False)
P("light_switch", 564, 1262, F2 + 120, (-1, 0), r, collide=False); P("vent", -28, 1210, F2 + 12, (1, 0), r, collide=False)

# ---------------- Jack's bedroom ----------------
r = "Bedroom"
P("bed_twin", 736, 1698, F2, (0, -1), r)
P("teddy", 740, 1575, F2 + 55, (0.3, -1), r, collide=False)
P("dresser", 580, 1600, F2, (1, 0), r); P("boombox", 584, 1626, F2 + 83, (1, 0), r, collide=False)
P("desk", 898, 1525, F2, (-1, 0), r); P("chair_wood", 800, 1530, F2, (1, 0.1), r)
P("table_lamp", 872, 1488, F2 + 75, (1, 0), r, collide=False); lamp("bed_desk", 872, 1488, F2 + 108, 400, r, 450)
P("toy_chest", 628, 1698, F2, (0, -1), r)
P("toy_blocks", 700, 1440, F2, (1, 0.3), r, collide=False); P("toy_ball", 826, 1418, F2, (1, 0), r, collide=False)
P("toy_car", 756, 1462, F2, (0.6, 1), r, collide=False)
P("poster_space", 579, 1520, F2 + 150, (1, 0), r, collide=False); P("poster_shapes", 800, 1357, F2 + 150, (0, 1), r, collide=False)
P("shelf_wall", 700, 1357, F2 + 120, (0, 1), r, collide=False)
P("curtain_bed", 664, 1697, F2 + 78, (0, -1), r, collide=False); P("curtain_bed", 808, 1697, F2 + 78, (0, -1), r, collide=False)
P("curtain_bed", 897, 1452, F2 + 78, (-1, 0), r, collide=False); P("curtain_bed", 897, 1598, F2 + 78, (-1, 0), r, collide=False)
P("box_jack", 612, 1522, F2, (1, 0.3), r); P("box_misc", 868, 1400, F2, (-1, 0.2), r); P("box_plain", 860, 1650, F2, (-1, 0.2), r)
P("ceiling_light_off", 740, 1530, C2, (1, 0), r, collide=False); lamp("bedroom", 740, 1530, C2 - 22, 900, r)
P("light_switch", 580, 1492, F2 + 120, (1, 0), r, collide=False); P("outlet", 580, 1680, F2 + 30, (1, 0), r, collide=False)

# ---------------- bathroom ----------------
r = "Bath"
P("bathtub", 898, 1235, F2, (-1, 0), r)
P("shower_curtain", 824, 1275, F2 + 22, (-1, 0), r, collide=False)
P("toilet", 770, 1342, F2, (0, -1), r); P("vanity", 782, 1128, F2, (0, 1), r)
P("medicine_cabinet", 782, 1127, F2 + 150, (0, 1), r, collide=False)
P("towel_bar", 640, 1342, F2 + 125, (0, -1), r, collide=False)
P("doormat", 780, 1235, F2, (0, 1), r, collide=False)
P("ceiling_light_off", 700, 1235, C2, (1, 0), r, collide=False); lamp("bath", 700, 1235, C2 - 22, 900, r, 500, (255, 236, 205))
P("light_switch", 580, 1262, F2 + 120, (1, 0), r, collide=False)
print("dressed:", sum(count.values()), "props")
