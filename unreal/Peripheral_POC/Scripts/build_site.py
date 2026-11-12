"""Our house's outside (roof, gables, garage, porch, chimney, shutters, rear deck) and the ground it sits on: lawns, the
driveway, the walk, the street. Safe to re-run: rebuilds everything tagged 'site'. Numbers are blueprint cm."""
import sys, math, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, house_plan as HP
importlib.reload(L); importlib.reload(K); importlib.reload(HP)
box, wallx, wally, steps = L.box, L.wallx, L.wally, L.steps
GR, LND, F1, C1, F2, C2, F3 = HP.GR, HP.LND, HP.F1, HP.C1, HP.F2, HP.C2, HP.F3
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L.clear("site")


def U(k, key, x0, y0, z0, x1, y1, z1):
    """Box given in blueprint coords, added to a kit that will sit at the Unreal origin."""
    k.box(key, x0 - L.OX, -(y1 - L.OY), z0, x1 - L.OX, -(y0 - L.OY), z1)


uy = lambda y: -(y - L.OY)


def world_mesh(k, name, label, tags=("site",), folder="Site", shadow=True):
    a = eas.spawn_actor_from_object(k.save(name, local=False), unreal.Vector(0, 0, 0))
    a.set_actor_label(label); a.set_folder_path(folder); a.tags = list(tags)
    a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC); a.static_mesh_component.set_cast_shadow(shadow)
    return a


# ---------------- the house from outside ----------------
k = K.Kit()
K.gable_roof(k, -50 - L.OX, 1100 - L.OX, uy(1980), uy(580), F3, pitch=HP.LOFT["pitch"])
U(k, "white", -54, 578, F2 - 22, -50, 1982, F2 - 2)                       # belt board under the upstairs overhang
for o in HP.OPENINGS:                                                      # shutters and a sill on every upstairs front window
    if o["kind"] == "window" and o["storey"] == 2 and o["axis"] == "x" and o["t0"] < -40 and o["style"] != "plain":
        a, b, z0, z1 = o["a0"], o["a1"], o["z0"], o["z1"]
        U(k, "shutter", -55, a - 38, z0 - 4, -50, a - 4, z1 + 4); U(k, "shutter", -55, b + 4, z0 - 4, -50, b + 38, z1 + 4)
        U(k, "white", -56, a - 4, z0 - 9, -44, b + 4, z0 - 3)
U(k, "brick", 240, 500, GR - 20, 360, 580, 800); U(k, "concrete", 234, 494, 800, 366, 586, 812)       # chimney, up the living room's side wall
# porch: stoop, a step, a small roof on two posts
U(k, "concrete", -160, 1081, GR - 20, -20, 1281, LND - 2); U(k, "concrete", -195, 1105, GR - 20, -160, 1257, GR + 6)
U(k, "roof", -178, 1071, 128, -20, 1291, 140); U(k, "white", -180, 1069, 110, -20, 1293, 128)
for y in (1085, 1265):
    U(k, "white", -168, y, LND - 2, -156, y + 12, 110)
# rear deck outside the kitchen door, with steps down to the patio
DX0, DX1, DY0, DY1 = 1100, 1330, 1150, 1450
U(k, "fence", DX0, DY0, -12, DX1, DY1, -2)
for (x, y) in ((DX0 + 5, DY0 + 5), (DX1 - 15, DY0 + 5), (DX0 + 5, DY1 - 15), (DX1 - 15, DY1 - 15)):
    U(k, "fence", x, y, GR, x + 10, y + 10, -12)
for i in range(7):
    U(k, "fence", DX1 + 28 * i, 1246, -22 - 17.5 * i - 4, DX1 + 28 * (i + 1), 1346, -22 - 17.5 * i)
for y in (DY0, DY1 - 4):
    U(k, "fence", DX0, y, 86, DX1, y + 4, 95)
    for x in range(DX0 + 5, DX1, 44):
        U(k, "fence", x, y, -2, x + 4, y + 4, 90)
U(k, "fence", DX1 - 4, DY0, 86, DX1, 1246, 95); U(k, "fence", DX1 - 4, 1346, 86, DX1, DY1, 95)
for y in list(range(DY0 + 40, 1246, 44)) + list(range(1350, DY1 - 4, 44)):
    U(k, "fence", DX1 - 4, y, -2, DX1, y + 4, 90)
# garage roof (lower, its own gable facing the side yard); it stops at the house wall
G = HP.GARAGE
K.gable_roof(k, -20 - L.OX, 780 - L.OX, uy(579), uy(G["y0"] - 20 - 30), F2, ov_gable=0, gable=None)
tri = [(-20 - L.OX, F2), (780 - L.OX, F2), (380 - L.OX, F2 + 400 * 5.0 / 12.0)]
k.prism_xz("siding", tri, uy(G["y0"]), uy(G["y0"] - 20))
world_mesh(k, "house_exterior", "HouseExterior")

# ---------------- garage ----------------
g = dict(folder="Site/Garage", tag="site")
d0, d1, dh = G["door"]
wallx("G_front", -20, 0, G["y0"] - 20, 580, GR, F2, "brick", "w_garage", [(d0, d1, GR, GR + dh)], **g)
wallx("G_rear", 760, 780, G["y0"] - 20, 580, GR, F2, "w_garage", "brick", [(120, 211, GR + 2, GR + 205)], **g)      # a plain doorway out to the back yard
wally("G_side", G["y0"] - 20, G["y0"], -20, 780, GR, F2, "brick", "w_garage", (), **g)
box("G_floor", -20, G["y0"] - 20, GR - 20, 780, 580, G["floor"], "f_garage", **g)
box("G_ceiling", 0, G["y0"], C1, 760, 580, C1 + 10, "w_garage", **g)
box("G_house_landing", 630, 470, GR, 760, 580, F1, "concrete", **g)
steps("G_steps", "x", 630, -1, 470, 580, 7, -17.5, 28, -17.5, "concrete", solid_to=GR, folder="Site/Garage", tag="site")
box("G_step_rail", 500, 467, GR, 630, 470, F1 + 90, "fence", **g)
box("G_door_trim_top", -24, d0 - 8, GR + dh, -20, d1 + 8, GR + dh + 12, "white", **g)
box("G_rear_step", 780, 105, GR - 20, 840, 226, GR + 2, "concrete", **g)
gd = K.Kit()                                                               # the big door: four panels high, eight across. E rolls it up.
w = (d1 - d0) / 2.0
for i in range(4):
    gd.box("garage_door", 0, -w, i * 53.25 + 1, 4, w, (i + 1) * 53.25 - 1)
    for j in range(8):
        gd.box("garage_door", -1.2, -w + 6 + j * (2 * w - 12) / 8.0, i * 53.25 + 8, 0, -w + 6 + (j + 1) * (2 * w - 12) / 8.0 - 6, (i + 1) * 53.25 - 8)
gd.box("metal_dark", 2, -w, 0, 3.5, w, dh)
door = eas.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Mover"), L.to_ue(-12, (d0 + d1) / 2.0, GR), unreal.Rotator(roll=0, pitch=0, yaw=0))
door.set_actor_label("GarageDoor"); door.set_folder_path("Site/Garage"); door.tags = ["site", "door", "garage_door"]
door.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE); door.static_mesh_component.set_static_mesh(gd.save("garage_door"))
for kx, v in (("OpenYaw", 0.0), ("Slide", unreal.Vector(0, 0, dh - 8.0)), ("Speed", 1.6)):
    door.set_editor_property(kx, v)

# ---------------- ground ----------------
gr = dict(folder="Site/Ground", tag="site")
Y0, Y1 = -5200, 7000
box("Lawn_front", -900, Y0, GR - 30, -20, Y1, GR, "lawn", **gr)
box("Lawn_side_garage", -20, Y0, GR - 30, 3400, G["y0"] - 20, GR, "lawn", **gr)
box("Lawn_notch", 780, G["y0"] - 20, GR - 30, 1100, 580, GR, "lawn", **gr)
box("Lawn_rear", 1100, G["y0"] - 20, GR - 30, 3400, 1980, GR, "lawn", **gr)
box("Lawn_side_far", -20, 1980, GR - 30, 3400, Y1, GR, "lawn", **gr)
box("Lawn_rear_far", 3400, Y0, GR - 30, 6500, Y1, GR, "lawn", **gr)
box("Sidewalk", -1020, Y0, GR - 30, -900, Y1, GR + 3, "concrete", **gr)
box("Verge", -1170, Y0, GR - 30, -1020, Y1, GR, "lawn", **gr)
box("Curb", -1185, Y0, GR - 30, -1170, Y1, GR + 3, "concrete", **gr)
box("Street", -2085, Y0, GR - 40, -1185, Y1, GR - 12, "asphalt", **gr)
box("Curb_far", -2100, Y0, GR - 30, -2085, Y1, GR + 3, "concrete", **gr)
box("Verge_far", -2250, Y0, GR - 30, -2100, Y1, GR, "lawn", **gr)
box("Sidewalk_far", -2370, Y0, GR - 30, -2250, Y1, GR + 3, "concrete", **gr)
box("Lawn_far", -6500, Y0, GR - 30, -2370, Y1, GR, "lawn", **gr)
box("Driveway", -1170, d0 - 25, GR - 20, -20, d1 + 25, GR + 2, "drive", **gr)          # clear concrete: cracks and oil stains, nothing standing on it
box("Driveway_apron", -1190, d0 - 40, GR - 20, -1170, d1 + 40, GR - 2, "drive", **gr)
box("Walk", -900, 1131, GR - 20, -195, 1231, GR + 2, "concrete", **gr)
box("Patio", 1330, 1050, GR - 20, 1760, 1560, GR + 2, "concrete", **gr)
box("Walk_garage_rear", 840, 105, GR - 20, 1100, 226, GR + 1.5, "concrete", **gr)
print("site built")
