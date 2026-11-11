"""Our house's exterior (roof, gables, garage, porch, chimney, shutters, rear deck) and the ground it sits on.
Safe to re-run: rebuilds everything tagged 'site'. Numbers are blueprint cm unless a helper says otherwise."""
import sys, math, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K
importlib.reload(L); importlib.reload(K)
box, wallx, wally, steps = L.box, L.wallx, L.wally, L.steps

GR, LND, F1, F2, C2 = -140, -126, 0, 259, 503      # grade, entry landing, floor 1, floor 2, ceiling 2
L.clear("site"); L.clear("site_tmp")
S = dict(folder="Site", tag="site")


gable_roof = K.gable_roof


def U(k, key, x0, y0, z0, x1, y1, z1):
    """Box given in blueprint coords, added to a kit that will sit at the Unreal origin."""
    k.box(key, x0 - L.OX, -(y1 - L.OY), z0, x1 - L.OX, -(y0 - L.OY), z1)


def uy(y):
    return -(y - L.OY)


# ---------------- house exterior mesh (one static mesh at the world origin) ----------------
k = K.Kit()
gable_roof(k, -50 - L.OX, 920 - L.OX, uy(1720), uy(580), C2 + 15)
U(k, "white", -54, 578, F2 - 22, -50, 1722, F2 - 2)                       # belt board under the siding overhang
# chimney on the far end wall
ch = K.Kit()                                                              # its own actor: the loop corridor runs through here, so the loop hides it
U(ch, "brick", 520, 1720, GR - 20, 640, 1790, 800)
U(ch, "concrete", 514, 1716, 800, 646, 1796, 812)
# shutters and white trim around the three front floor-2 windows
for (a, b) in ((800, 920), (1265, 1355), (1480, 1600)):
    z0, z1 = F2 + 90, F2 + 220
    U(k, "shutter", -55, a - 38, z0 - 4, -50, a - 4, z1 + 4)
    U(k, "shutter", -55, b + 4, z0 - 4, -50, b + 38, z1 + 4)
    U(k, "white", -56, a - 4, z0 - 9, -44, b + 4, z0 - 3)                 # sill
# porch: stoop, roof and two posts
U(k, "concrete", -160, 1036, GR - 20, -20, 1236, LND - 2)
U(k, "concrete", -195, 1060, GR - 20, -160, 1212, GR + 6)
U(k, "roof", -178, 1026, 128, -20, 1246, 140)
U(k, "white", -180, 1024, 110, -20, 1248, 128)
for y in (1040, 1220):
    U(k, "white", -168, y, LND - 2, -156, y + 12, 110)
# rear deck outside the kitchen door, with steps down to the yard
U(k, "fence", 920, 980, -12, 1140, 1180, -2)
for (x, y) in ((925, 985), (1125, 985), (925, 1165), (1125, 1165)):
    U(k, "fence", x, y, GR, x + 10, y + 10, -12)
for i in range(7):
    U(k, "fence", 1140 + 28 * i, 1030, -22 - 17.5 * i - 4, 1140 + 28 * (i + 1), 1130, -22 - 17.5 * i)
for y in (980, 1176):
    U(k, "fence", 920, y, 86, 1140, y + 4, 95)
    for x in range(925, 1140, 43):
        U(k, "fence", x, y, -2, x + 4, y + 4, 90)
U(k, "fence", 1136, 980, 86, 1140, 1030, 95); U(k, "fence", 1136, 1130, 86, 1140, 1180, 95)
# garage roof (lower, its own gable) and the gable end wall
gable_roof(k, -20 - L.OX, 780 - L.OX, uy(579), uy(110), 150, ov_gable=0, gable=None)     # stops at the house wall
tri = [(-20 - L.OX, 150), (780 - L.OX, 150), (380 - L.OX, 150 + 400 * 5.0 / 12.0)]
k.prism_xz("siding", tri, uy(160), uy(140))
house = k.save("house_exterior")
a = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_object(house, unreal.Vector(0, 0, 0))
a.set_actor_label("HouseExterior"); a.set_folder_path("Site"); a.tags = ["site"]
a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
a = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_object(ch.save("chimney"), unreal.Vector(0, 0, 0))
a.set_actor_label("Chimney"); a.set_folder_path("Site"); a.tags = ["site", "annex_hide"]
a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)

# ---------------- garage (blockout inside) ----------------
g = dict(folder="Site/Garage", tag="site")
wallx("G_front", -20, 0, 140, 580, GR, 150, "brick", "blk", [(222, 497, GR, GR + 213)], **g)
wallx("G_rear", 760, 780, 140, 580, GR, 150, "blk", "brick", (), **g)
wally("G_side", 140, 160, -20, 780, GR, 150, "brick", "blk", (), **g)
box("G_floor", -20, 140, GR - 20, 780, 580, GR + 2, "concrete", **g)
box("G_ceiling", 0, 160, 150, 760, 580, 160, "blk", **g)
box("G_house_landing", 640, 480, GR, 760, 580, F1, "concrete", **g)
steps("G_steps", "x", 640, -1, 480, 580, 7, -17.5, 28, -17.5, "concrete", solid_to=GR, folder="Site/Garage", tag="site")
gd = K.Kit()
for i in range(4):                                                         # four door panels with a shadow line between
    gd.box("garage_door", 0, -137.5, i * 53.25 + 1, 4, 137.5, (i + 1) * 53.25 - 1)
    for j in range(4):
        gd.box("garage_door", -1.2, -132 + j * 67, i * 53.25 + 8, 0, -132 + j * 67 + 62, (i + 1) * 53.25 - 8)
gd.box("metal_dark", 2, -137.5, 0, 3.5, 137.5, 213)
K.place(gd.save("garage_door"), "GarageDoor", -12, 359.5, GR, face=(1, 0), folder="Site/Garage", tag="site")
box("G_door_trim_top", -24, 214, GR + 213, -20, 505, GR + 225, "white", **g)

# ---------------- ground ----------------
gr = dict(folder="Site/Ground", tag="site")
Y0, Y1 = -5200, 7000
box("Lawn_front", -900, Y0, GR - 30, -20, Y1, GR, "lawn", **gr)
box("Lawn_side_garage", -20, Y0, GR - 30, 3400, 140, GR, "lawn", **gr)
box("Lawn_notch", 780, 140, GR - 30, 920, 580, GR, "lawn", **gr)
box("Lawn_rear", 920, 140, GR - 30, 3400, 1720, GR, "lawn", **gr)
box("Lawn_side_far", -20, 1720, GR - 30, 3400, Y1, GR, "lawn", **gr)
box("Lawn_rear_far", 3400, Y0, GR - 30, 6500, Y1, GR, "lawn", **gr)
box("Sidewalk", -1020, Y0, GR - 30, -900, Y1, GR + 3, "concrete", **gr)
box("Verge", -1170, Y0, GR - 30, -1020, Y1, GR, "lawn", **gr)
box("Curb", -1185, Y0, GR - 30, -1170, Y1, GR + 3, "concrete", **gr)
box("Street", -2085, Y0, GR - 40, -1185, Y1, GR - 12, "asphalt", **gr)
box("Curb_far", -2100, Y0, GR - 30, -2085, Y1, GR + 3, "concrete", **gr)
box("Verge_far", -2250, Y0, GR - 30, -2100, Y1, GR, "lawn", **gr)
box("Sidewalk_far", -2370, Y0, GR - 30, -2250, Y1, GR + 3, "concrete", **gr)
box("Lawn_far", -6500, Y0, GR - 30, -2370, Y1, GR, "lawn", **gr)
box("Driveway", -1170, 215, GR - 20, -20, 505, GR + 2, "concrete", **gr)
box("Driveway_apron", -1190, 200, GR - 20, -1170, 520, GR - 2, "concrete", **gr)
box("Walk", -900, 1086, GR - 20, -195, 1186, GR + 2, "concrete", **gr)
print("site built")
