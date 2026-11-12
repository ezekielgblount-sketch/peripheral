"""Builds the house shell from house_plan.py. Safe to re-run: it deletes and rebuilds everything tagged 'shell'.
Walls, floors and ceilings come from the room table (a wall is the gap between two rooms, split down the middle so each
face takes its own room's finish). The stair core, the attic loft and a few half walls are built by hand below."""
import sys, math, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, house_plan as HP
importlib.reload(L); importlib.reload(HP)
box, steps = L.box, L.steps
GR, LND, B, F1, C1, F2, C2, F3, SLAB = HP.GR, HP.LND, HP.B, HP.F1, HP.C1, HP.F2, HP.C2, HP.F3, HP.SLAB
removed = L.clear("shell")
out = []                                     # (x0, y0, z0, x1, y1, z1, material, folder)


def cut(z0, z1, holes):
    """[z0, z1] with the hole ranges taken out."""
    segs = [(z0, z1)]
    for (h0, h1) in holes:
        nxt = []
        for (a, b) in segs:
            if h1 <= a or h0 >= b:
                nxt.append((a, b))
            else:
                if h0 > a: nxt.append((a, h0))
                if h1 < b: nxt.append((h1, b))
        segs = nxt
    return [s for s in segs if s[1] - s[0] > 0.01]


def footprint(o):
    return (o["t0"], o["a0"], o["t1"], o["a1"]) if o["axis"] == "x" else (o["a0"], o["t0"], o["a1"], o["t1"])


def storey(s):
    rs = HP.rooms(s, ghosts=True)
    ops = [o for o in HP.OPENINGS if o["storey"] == s]
    allops = HP.OPENINGS                      # a door on one storey can cut the wall of the storey below (the sunken front door)
    bx0, by0, bx1, by1 = HP.BBOX[s]
    xs, ys = {bx0, bx0 + 20, bx1 - 20, bx1}, {by0, by0 + 20, by1 - 20, by1}
    for r in rs:
        xs |= {r["rect"][0], r["rect"][2]}; ys |= {r["rect"][1], r["rect"][3]}
    for o in allops:
        f = footprint(o); xs |= {f[0], f[2]}; ys |= {f[1], f[3]}
    xs, ys = sorted(v for v in xs if bx0 <= v <= bx1), sorted(v for v in ys if by0 <= v <= by1)

    def owner(i, j):
        if i < 0 or j < 0 or i >= len(xs) - 1 or j >= len(ys) - 1:
            return "OUT"
        cx, cy = (xs[i] + xs[i + 1]) / 2.0, (ys[j] + ys[j + 1]) / 2.0
        return next((r for r in rs if r["rect"][0] < cx < r["rect"][2] and r["rect"][1] < cy < r["rect"][3]), None)

    fol = "Shell/S%d" % s
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            if owner(i, j) is not None:
                continue
            x0, x1, y0, y1 = xs[i], xs[i + 1], ys[j], ys[j + 1]
            xm, ym = (x0 + x1) / 2.0, (y0 + y1) / 2.0
            holes = [(o["z0"], o["z1"]) for o in allops if x0 >= footprint(o)[0] - 0.01 and x1 <= footprint(o)[2] + 0.01
                     and y0 >= footprint(o)[1] - 0.01 and y1 <= footprint(o)[3] + 0.01]
            sides = []
            if x1 - x0 <= 20.01:
                sides += [((i - 1, j), (i + 1, j), "x1", (x0, y0, xm, y1)), ((i + 1, j), (i - 1, j), "x0", (xm, y0, x1, y1))]
            if y1 - y0 <= 20.01:
                sides += [((i, j - 1), (i, j + 1), "y1", (x0, y0, x1, ym)), ((i, j + 1), (i, j - 1), "y0", (x0, ym, x1, y1))]
            for (nb, opp, side, (a0, b0, a1, b1)) in sides:
                r, ro = owner(*nb), owner(*opp)
                if r == "OUT":
                    z0, z1 = HP.EXT_Z[s]
                    if isinstance(ro, dict) and not ro["ghost"]:
                        z0 = min(z0, ro["floor"] - SLAB)
                    m = HP.EXT_MAT[s]
                elif isinstance(r, dict) and not r["ghost"]:
                    z0, z1, m = r["floor"] - SLAB, r["ceil"], HP.wall_mat(r, side)
                else:
                    continue
                for (za, zb) in cut(z0, z1, holes):
                    out.append((a0, b0, za, a1, b1, zb, m, fol + "/Walls"))
    for r in HP.rooms(s):
        x0, y0, x1, y1 = r["rect"]
        if r["floor_mat"]:
            out.append((x0, y0, r["floor"] - 7.5, x1, y1, r["floor"], r["floor_mat"], fol + "/Floors"))
        if r["ceil_mat"]:
            out.append((x0, y0, r["ceil"], x1, y1, r["ceil"] + 7.5, r["ceil_mat"], fol + "/Ceilings"))
    for o in ops:                             # the strip of floor under each doorway
        if o["kind"] == "window":
            continue
        f = footprint(o)
        cx, cy = (f[0] + f[2]) / 2.0, (f[1] + f[3]) / 2.0
        probes = [(f[0] - 5, cy), (f[2] + 5, cy)] if o["axis"] == "x" else [(cx, f[1] - 5), (cx, f[3] + 5)]
        mats = [r["floor_mat"] for (px, py) in probes for r in HP.rooms(s) if r["rect"][0] < px < r["rect"][2] and r["rect"][1] < py < r["rect"][3] and r["floor_mat"]]
        out.append((f[0], f[1], o["z0"] - 7.5, f[2], f[3], o["z0"], (mats or ["f_oak"])[0], fol + "/Floors"))


def merged(bs):
    """Join boxes that share a face and a finish, along Y and then along X."""
    for (lo, hi) in ((1, 4), (0, 3)):
        groups = {}
        for b in bs:
            groups.setdefault(tuple(v for k, v in enumerate(b) if k not in (lo, hi)), []).append(b)
        bs = []
        for g in groups.values():
            g.sort(key=lambda b: b[lo])
            cur = list(g[0])
            for b in g[1:]:
                if abs(b[lo] - cur[hi]) < 0.01:
                    cur[hi] = b[hi]
                else:
                    bs.append(tuple(cur)); cur = list(b)
            bs.append(tuple(cur))
    return bs


with unreal.ScopedSlowTask(1, "Building shell"):
    for s in (0, 1, 2):
        storey(s)
    for n, (x0, y0, z0, x1, y1, z1, m, fol) in enumerate(merged(out)):
        box("%s_%03d" % (fol.split("/")[-1][:1] + fol.split("/")[1], n), x0, y0, z0, x1, y1, z1, m, fol)

    # ---------------- the sunken entry and the two flights off its landing ----------------
    e, st = "Shell/Entry", HP.STAIRS
    box("Landing_mass", 0, 1076, B - SLAB, 180, 1284, LND - 2, "w_hall", e); box("Landing_mass_b", 0, 1284, B - SLAB, 100, 1296, LND - 2, "w_hall", e)
    box("Landing_floor", 0, 1076, LND - 2, 180, 1284, LND, "f_oak", e); box("Landing_floor_b", 0, 1284, LND - 2, 100, 1296, LND, "f_oak", e)
    steps("S_up", "y", 1296, +1, 0, 100, 6, 18, 28, LND + 18, "f_stair", solid_to=B - SLAB)
    box("Top_of_up_flight", 0, 1464, B - SLAB, 100, 1559, F1, "f_oak", "Shell/Stairs")
    steps("S_down", "x", 180, +1, 1076, 1174, 6, -18, 28, LND - 18, "f_stair", solid_to=B - SLAB)
    box("Foot_of_basement_flight", 348, 1076, B - 7.5, 376, 1174, B, "f_bsmt", "Shell/Stairs")
    steps("S_upper", "x", 470, -1, 1186, 1284, 13, 18.5, 28, 18.5, "f_stair", solid_to=F1, soffit=37, soffit_before=180)
    box("Under_stair_floor", 180, 1186, -7.5, 470, 1284, F1, "f_oak", "Shell/Stairs")
    box("Wall_over_landing", 106, 1174, 150, 180, 1186, C1, "w_hall", "Shell/Stairs")                 # closes the side of the top steps, which pass over the entry
    box("Ret_under_stair", 180, 1186, B - SLAB, 186, 1284, -SLAB, "w_hall", e)
    box("Ret_hall_edge", 100, 1296, B - SLAB, 106, 1559, F1, "w_hall", e)
    box("Half_wall_over_up_flight", 100, 1296, F1, 112, 1464, F1 + 95, "w_hall", "Shell/Stairs")
    box("Half_wall_basement_well", 376, 1076, F1, 388, 1174, F1 + 95, "w_hall", "Shell/Stairs")
    # round the stairwell upstairs: slab edges and the half walls on them
    box("Half_wall_gallery", 100, 1283.6, C1, 470, 1296, F2 + 91, "w_hall", "Shell/Stairs")
    box("Half_wall_stair_end", 469.6, 1186, C1, 482, 1284, F2 + 91, "w_hall", "Shell/Stairs")
    box("Riser_arrival", 104, 1186, 236, 106.4, 1284, F2, "f_c_hall", "Shell/Stairs")
    box("Front_overhang_soffit", -50, 580, C1, -20, 1980, F2, "siding", "Shell/S2")

    # ---------------- the far end of the upstairs back hall: a wall an anomaly can move back ----------------
    hc = HP.HALL_CAP
    cap = box("Hall_end_wall", hc["x0"], hc["y"] - 6, F2, hc["x1"], hc["y"] + 6, C2, "w_hall", "Shell/S2")
    cap.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE); cap.tags = ["shell", "dy_hallcap"]
    cb = box("Hall_end_base", hc["x0"], hc["y"] + 6, F2, hc["x1"], hc["y"] + 7.3, F2 + 9, "white", "Shell/S2", collide=False)
    cb.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE); cb.tags = ["shell", "dy_hallcap"]

    # ---------------- attic stair and loft ----------------
    a, lf = "Shell/Attic", HP.LOFT
    w0, wy0, w1, wy1 = lf["well"]
    steps("S_attic", "x", 175, +1, 1428, 1528, 13, 18.5, 28, F2 + 18.5, "f_stair", solid_to=F2)
    for (nm, x0, y0, x1, y1) in (("a", -50, 580, 1100, wy0), ("b", -50, wy1, 1100, 1980), ("c", -50, wy0, w0, wy1), ("d", w1, wy0, 1100, wy1)):
        box("Loft_floor_" + nm, x0, y0, C2 + 7.5, x1, y1, F3, "f_c_loft", a)
    box("Loft_rail_s", w0, wy0 - 12, C2, w1, wy0 + 0.4, F3 + 92, "w_hall", a); box("Loft_rail_n", w0, wy1 - 0.4, C2, w1, wy1 + 12, F3 + 92, "w_hall", a)
    box("Loft_rail_w", w0 - 12, wy0 - 12, C2 + 7.5, w0 + 0.4, wy1 + 12, F3 + 92, "w_hall", a)
    box("Loft_riser", w1 - 0.4, wy0, F3 - 23, w1 + 2, wy1, F3, "f_c_loft", a)
    roof_z = lambda x: F3 + (575.0 - abs(x - lf["ridge_x"])) * lf["pitch"] - 6.0             # underside of the roof lining
    for (nm, xa, xb) in (("w", lf["x0"] - 12, lf["x0"]), ("e", lf["x1"], lf["x1"] + 12)):
        box("Loft_knee_" + nm, xa, lf["y0"] - 12, F3, xb, lf["y1"], roof_z(lf["x0"]) + 2, "w_attic", a)
    k = K.Kit()
    ang = math.degrees(math.atan(lf["pitch"]))
    ux, uy = (lambda x: x - L.OX), (lambda y: -(y - L.OY))
    yc, ylen = (uy(lf["y0"] - 12) + uy(lf["y1"])) / 2.0, lf["y1"] - lf["y0"] + 12
    for sg in (-1, 1):                                                         # the two sloping ceilings
        xe = lf["x0"] if sg < 0 else lf["x1"]
        run = abs(lf["ridge_x"] - xe)
        cx, cz = (xe + lf["ridge_x"]) / 2.0, (roof_z(xe) + roof_z(lf["ridge_x"])) / 2.0 + 4
        k.obox("shiplap", ux(cx), yc, cz, run / math.cos(math.radians(ang)) + 10, ylen, 8, pitch=(ang if sg < 0 else -ang))
    tri = [(ux(lf["x0"]), F3), (ux(lf["x1"]), F3), (ux(lf["x1"]), roof_z(lf["x1"])), (ux(lf["ridge_x"]), roof_z(lf["ridge_x"])), (ux(lf["x0"]), roof_z(lf["x0"]))]
    k.prism_xz("w_attic", tri, uy(lf["y1"]), uy(lf["y1"]) + 5)                # gable end, inside face
    k.prism_xz("w_attic", tri, uy(lf["y0"]), uy(lf["y0"]) + 12)               # the partition that closes the loft off from the rest of the attic
    act = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_object(k.save("loft_lining", local=False), unreal.Vector(0, 0, 0))
    act.set_actor_label("Loft_lining"); act.set_folder_path(a); act.tags = ["shell"]
    act.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)

print("shell rebuilt. removed:", removed, "boxes:", len(merged(out)), "| floors 1+2 gross sq ft:", round(HP.area_sqft()))
