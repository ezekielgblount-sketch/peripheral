"""Windows (frames, sashes, glass), door frames, working doors, casings and baseboards.
Safe to re-run: rebuilds everything tagged 'opening'. Numbers are blueprint cm."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K
importlib.reload(L); importlib.reload(K)
LND, F1, F2 = -126, 0, 259
L.clear("opening")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
frames, glass = K.Kit(), K.Kit()


def bx(k, key, axis, t0, t1, a0, a1, z0, z1):
    """Box in wall space: t = across the wall, a = along it. axis 'x' means the wall's thickness runs along X."""
    t0, t1 = min(t0, t1), max(t0, t1)
    x0, x1, y0, y1 = (t0, t1, a0, a1) if axis == "x" else (a0, a1, t0, t1)
    k.box(key, x0 - L.OX, -(y1 - L.OY), z0, x1 - L.OX, -(y0 - L.OY), z1)


def casing(axis, face, out, a0, a1, z0, z1, key, sill):
    """Trim around an opening on one wall face. out = +1/-1, the direction the face looks."""
    f0, f1 = face, face + out * 1.6
    bx(frames, key, axis, f0, f1, a0 - 6.5, a0, z0, z1 + 6.5)
    bx(frames, key, axis, f0, f1, a1, a1 + 6.5, z0, z1 + 6.5)
    bx(frames, key, axis, f0, f1, a0, a1, z1, z1 + 6.5)
    if sill:
        bx(frames, key, axis, f0, face + out * 5.5, a0 - 9, a1 + 9, z0 - 3, z0)
        bx(frames, key, axis, f0, f1, a0 - 6.5, a1 + 6.5, z0 - 9.5, z0 - 3)


def window(axis, t0, t1, a0, a1, z0, z1, inside, kind="double", in_key="trim"):
    tm = (t0 + t1) / 2.0
    for (b0, b1, c0, c1) in ((a0, a1, z0, z0 + 2), (a0, a1, z1 - 2, z1), (a0, a0 + 2, z0, z1), (a1 - 2, a1, z0, z1)):
        bx(frames, "white", axis, t0, t1, b0, b1, c0, c1)                                  # liner
    for (b0, b1, c0, c1) in ((a0 + 2, a1 - 2, z0 + 2, z0 + 6.5), (a0 + 2, a1 - 2, z1 - 6.5, z1 - 2),
                             (a0 + 2, a0 + 6.5, z0 + 2, z1 - 2), (a1 - 6.5, a1 - 2, z0 + 2, z1 - 2)):
        bx(frames, "white", axis, tm - 2, tm + 2, b0, b1, c0, c1)                          # sash
    zm, w = (z0 + z1) / 2.0, a1 - a0
    if kind == "double":
        bx(frames, "white", axis, tm - 2, tm + 2, a0 + 2, a1 - 2, zm - 2.2, zm + 2.2)
    if kind == "picture":
        for am in (a0 + w * 0.22, a1 - w * 0.22):
            bx(frames, "white", axis, tm - 2.5, tm + 2.5, am - 2.5, am + 2.5, z0 + 2, z1 - 2)
        bx(frames, "white", axis, tm - 2, tm + 2, a0 + 2, a0 + w * 0.22, zm - 2.2, zm + 2.2)
        bx(frames, "white", axis, tm - 2, tm + 2, a1 - w * 0.22, a1 - 2, zm - 2.2, zm + 2.2)
    bx(glass, "glass", axis, tm - 0.3, tm + 0.3, a0 + 2, a1 - 2, z0 + 2, z1 - 2)
    casing(axis, t1 if inside > 0 else t0, inside, a0, a1, z0, z1, in_key, True)
    casing(axis, t0 if inside > 0 else t1, -inside, a0, a1, z0, z1, "white", True)


_door_mesh = {}
def door_mesh(width, key, knob="brass"):
    name = "door_%d_%s" % (round(width), key)
    if name not in _door_mesh:
        k = K.Kit()
        k.box(key, 0, -1.75, 0.8, width, 1.75, 201)
        for s in (-1, 1):
            k.tube(knob, (width - 7, s * 1.75, 91), (width - 7, s * 5.5, 91), 1.1, 10)
            k.sphere(knob, width - 7, s * 6.6, 91, 2.9, 5, sy=0.7)
            k.cyl(knob, width - 7, s * 1.75, 91, 3.2, 0.5, 14, roll=-s * 90)
        for z in (20, 180):
            k.box("chrome", -0.6, -2.2, z, 0.6, 2.2, z + 9)
        _door_mesh[name] = k.save(name)
    return _door_mesh[name]


mover_cls = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Mover")
def door(name, axis, t0, t1, a0, a1, z, hinge, swing, key="door_wood", locked=False, keys=("trim", "trim"), top=203, is_open=False):
    """hinge: 'lo' or 'hi' end of the opening along the wall. swing: +1/-1, the side of the wall the door opens toward.
    keys: casing material on the low-t face and the high-t face (None = no casing)."""
    for (b0, b1, c0, c1) in ((a0, a0 + 2, z, z + top), (a1 - 2, a1, z, z + top), (a0, a1, z + top - 2, z + top)):
        bx(frames, keys[0] or keys[1] or "trim", axis, t0, t1, b0, b1, c0, c1)
    if keys[0]:
        casing(axis, t0, -1, a0, a1, z, z + top, keys[0], False)
    if keys[1]:
        casing(axis, t1, +1, a0, a1, z, z + top, keys[1], False)
    width = (a1 - a0) - 4.6
    ha = a0 + 2.3 if hinge == "lo" else a1 - 2.3
    ht = (t1 - 2.0) if swing > 0 else (t0 + 2.0)
    da = 1.0 if hinge == "lo" else -1.0
    bp_pos = (ht, ha) if axis == "x" else (ha, ht)
    bp_dir = (0.0, da) if axis == "x" else (da, 0.0)
    bp_n = (float(swing), 0.0) if axis == "x" else (0.0, float(swing))
    d = unreal.Vector(bp_dir[0], -bp_dir[1], 0); n = unreal.Vector(bp_n[0], -bp_n[1], 0)      # Unreal-space directions
    sign = 1.0 if (d.x * n.y - d.y * n.x) > 0 else -1.0
    yaw = unreal.MathLibrary.find_look_at_rotation(unreal.Vector(0, 0, 0), d).yaw
    a = eas.spawn_actor_from_class(mover_cls, L.to_ue(bp_pos[0], bp_pos[1], z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
    a.set_actor_label(name); a.set_folder_path("Openings/Doors"); a.tags = ["opening", "door"]
    c = a.static_mesh_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_static_mesh(door_mesh(width, key))
    a.set_editor_property("OpenYaw", sign * 96.0)
    a.set_editor_property("Speed", 3.5)
    a.set_editor_property("Locked", locked)
    if is_open:                                             # placed open in the editor; the Blueprint works back to the closed pose
        a.set_actor_rotation(unreal.Rotator(roll=0, pitch=0, yaw=yaw + sign * 96.0), False)
        a.set_editor_property("Open", True)
    return a


def base(axis, face, out, a0, a1, z, gaps=(), key="trim"):
    """Baseboard along a wall face from a0 to a1, skipping door gaps."""
    cur = a0
    for (g0, g1) in sorted(gaps):
        if g0 - 6.5 > cur:
            bx(frames, key, axis, face, face + out * 1.3, cur, g0 - 6.5, z, z + 9)
        cur = g1 + 6.5
    if cur < a1:
        bx(frames, key, axis, face, face + out * 1.3, cur, a1, z, z + 9)


# ---------------- windows ----------------
window("x", -20, 0, 700, 940, 60, 210, +1, "picture", "rail")
for a in (1055, 1191):
    window("x", -20, 0, a, a + 25, LND + 20, LND + 203, +1, "plain")
window("x", -20, 0, 1560, 1660, 90, 220, +1)
window("x", 900, 920, 760, 880, 107, 207, -1)
window("x", 900, 920, 1300, 1420, 90, 220, -1)
window("y", 1700, 1720, 300, 420, 90, 220, -1)
for (a0, a1) in ((800, 920), (1265, 1355), (1480, 1600)):
    window("x", -50, -30, a0, a1, F2 + 90, F2 + 220, +1)
window("x", 900, 920, 800, 920, F2 + 90, F2 + 220, -1)
window("x", 900, 920, 1200, 1280, F2 + 120, F2 + 200, -1, "plain")
window("x", 900, 920, 1465, 1585, F2 + 90, F2 + 220, -1)
window("y", 1700, 1720, 676, 796, F2 + 90, F2 + 220, -1)

# ---------------- doors ----------------
door("Door_front", "x", -20, 0, 1090, 1181, LND, "lo", +1, key="door_red", keys=("white", "trim"))
door("Door_kitchen_rear", "x", 900, 920, 1030, 1121, F1, "lo", -1, key="enamel", keys=("trim", "white"))
door("Door_garage", "y", 580, 600, 655, 746, F1, "lo", +1, locked=True, keys=(None, "trim"))
door("Door_living", "y", 1019, 1031, 470, 561, F1, "hi", -1, keys=("rail", "trim"), is_open=True)
door("Door_kitchen", "x", 574, 586, 1300, 1391, F1, "hi", +1, is_open=True)
door("Door_dining", "y", 1514, 1526, 250, 341, F1, "lo", +1, locked=True, keys=("trim", None))
door("Door_halfbath", "y", 1544, 1556, 640, 731, F1, "lo", +1, locked=True, keys=("trim", None))
door("Door_bath", "x", 566, 578, 1150, 1241, F2, "lo", +1, is_open=True)
door("Door_bedroom", "x", 566, 578, 1385, 1476, F2, "lo", +1, is_open=True)
door("Door_upstairs_a", "y", 1371, 1383, 150, 241, F2, "lo", +1, locked=True, keys=("trim", None))
door("Door_upstairs_b", "y", 1494, 1506, 472, 553, F2, "lo", +1, locked=True, keys=("trim", None))

# ---------------- baseboards ----------------
base("x", 0, +1, 600, 1019, F1, key="rail"); base("x", 574, -1, 600, 1019, F1, key="rail")            # living room
base("y", 600, +1, 0, 574, F1, key="rail"); base("y", 1019, -1, 0, 574, F1, [(470, 561)], key="rail")
base("x", 586, +1, 600, 1544, F1, [(1300, 1391)]); base("x", 900, -1, 600, 1544, F1, [(1030, 1121)])    # kitchen
base("y", 600, +1, 586, 900, F1, [(655, 746)]); base("y", 1544, -1, 586, 900, F1, [(640, 731)])
base("y", 1514, -1, 112, 574, F1, [(250, 341)]); base("x", 574, -1, 1031, 1514, F1, [(1300, 1391)])     # hall, floor 1
base("y", 1251, +1, 112, 470, F1); base("y", 1031, +1, 388, 574, F1, [(470, 561)])
base("x", -30, +1, 1141, 1371, F2); base("y", 1371, -1, -30, 446, F2, [(150, 241)])                     # hall, floor 2
base("y", 1251, +1, 100, 470, F2); base("y", 1141, +1, -30, 106, F2); base("y", 1141, +1, 482, 566, F2)
base("x", 566, -1, 1141, 1494, F2, [(1150, 1241), (1385, 1476)]); base("x", 458, +1, 1383, 1494, F2)
base("y", 1494, -1, 458, 566, F2, [(472, 553)])
base("x", 578, +1, 1356, 1700, F2, [(1385, 1476)]); base("x", 900, -1, 1356, 1700, F2)                  # bedroom
base("y", 1356, +1, 578, 900, F2); base("y", 1700, -1, 578, 900, F2)

for (kit, name, shadow) in ((frames, "openings_frames", True), (glass, "openings_glass", False)):
    sm = kit.save(name, local=False)
    a = eas.spawn_actor_from_object(sm, unreal.Vector(0, 0, 0))
    a.set_actor_label(name); a.set_folder_path("Openings"); a.tags = ["opening"]
    a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    a.static_mesh_component.set_cast_shadow(shadow)
print("openings built")
