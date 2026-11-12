"""Windows (frames, sashes, glass), door frames, working doors, casings and baseboards, all taken from house_plan.py.
Safe to re-run: rebuilds everything tagged 'opening'. Numbers are blueprint cm."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, house_plan as HP
importlib.reload(L); importlib.reload(K); importlib.reload(HP)
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


def room_at(storey, x, y):
    return next((r for r in HP.rooms(storey, ghosts=True) if r["rect"][0] < x < r["rect"][2] and r["rect"][1] < y < r["rect"][3]), None)


def side_trims(o):
    """Casing finish on the low-t face and the high-t face of an opening: each takes the trim of the room it faces."""
    am = (o["a0"] + o["a1"]) / 2.0
    pts = [(o["t0"] - 5, am), (o["t1"] + 5, am)] if o["axis"] == "x" else [(am, o["t0"] - 5), (am, o["t1"] + 5)]
    rs = [room_at(o["storey"], *p) for p in pts]
    return tuple(HP.trim_mat(r) if r and not r["ghost"] else "white" for r in rs)


n_doors = 0
for o in HP.OPENINGS:
    lo, hi = side_trims(o)
    if o["kind"] == "window":
        window(o["axis"], o["t0"], o["t1"], o["a0"], o["a1"], o["z0"], o["z1"], o["inside"], o["style"], hi if o["inside"] > 0 else lo)
    elif o["kind"] == "door":
        d = door(o["name"], o["axis"], o["t0"], o["t1"], o["a0"], o["a1"], o["z0"], o["hinge"], o["swing"], key=o["key"], locked=o["locked"],
                 keys=(lo, hi), is_open=o["is_open"])
        d.tags = ["opening", "door"] + o["tags"]; n_doors += 1
    else:                                                    # a cased opening with no door
        z, top = o["z0"], o["z1"] - o["z0"]
        for (b0, b1, c0, c1) in ((o["a0"], o["a0"] + 2, z, z + top), (o["a1"] - 2, o["a1"], z, z + top), (o["a0"], o["a1"], z + top - 2, z + top)):
            bx(frames, lo, o["axis"], o["t0"], o["t1"], b0, b1, c0, c1)
        casing(o["axis"], o["t0"], -1, o["a0"], o["a1"], z, z + top, lo, False); casing(o["axis"], o["t1"], +1, o["a0"], o["a1"], z, z + top, hi, False)

# ---------------- baseboards: along every wall of every room, broken at doorways ----------------
n_base = 0
for r in HP.rooms():
    key = HP.FIN[r["fin"]][2]
    if not r["base"] or key is None:
        continue
    s, (x0, y0, x1, y1) = r["storey"], r["rect"]
    gaps = [o for o in HP.OPENINGS if o["storey"] == s and o["kind"] != "window" and abs(o["z0"] - r["floor"]) < 1]
    others = HP.rooms(s, ghosts=True)
    for (axis, face, outd, a0, a1) in (("x", x0, +1, y0, y1), ("x", x1, -1, y0, y1), ("y", y0, +1, x0, x1), ("y", y1, -1, x0, x1)):
        cuts = {a0, a1}
        for q in others:
            cuts |= {v for v in ((q["rect"][1], q["rect"][3]) if axis == "x" else (q["rect"][0], q["rect"][2])) if a0 < v < a1}
        for o in gaps:
            if o["axis"] == axis:
                cuts |= {v for v in (o["a0"] - 6.5, o["a1"] + 6.5) if a0 < v < a1}
        cuts = sorted(cuts)
        for (c0, c1) in zip(cuts[:-1], cuts[1:]):
            m, t = (c0 + c1) / 2.0, face - outd * 3.0                      # a point just behind this stretch of wall face
            p = (t, m) if axis == "x" else (m, t)
            if room_at(s, *p):
                continue                                                   # open to another part of the same space
            if any(o["axis"] == axis and o["t0"] - 1 <= t <= o["t1"] + 1 and o["a0"] - 6.6 < m < o["a1"] + 6.6 for o in gaps):
                continue
            bx(frames, key, axis, face, face + outd * 1.3, c0, c1, r["floor"], r["floor"] + 9); n_base += 1

for (kit, name, shadow) in ((frames, "openings_frames", True), (glass, "openings_glass", False)):
    sm = kit.save(name, local=False)
    a = eas.spawn_actor_from_object(sm, unreal.Vector(0, 0, 0))
    a.set_actor_label(name); a.set_folder_path("Openings"); a.tags = ["opening"]
    a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    a.static_mesh_component.set_cast_shadow(shadow)
print("openings built: doors", n_doors, "baseboard runs", n_base)
