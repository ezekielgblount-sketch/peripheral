"""Section 4b fit check: stands a 178 cm tall, 35 cm radius player capsule along every route in the slice
(doorways, halls, all three stair flights) and reports anything it touches. Run inside the editor."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
importlib.reload(L)

R, HH, LIFT, STAIR = 35.0, 89.0, 3.0, 22.0
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
STATIC = [unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY1]


def blocked(x, y, floor_z, lift=LIFT):
    hits = unreal.SystemLibrary.capsule_overlap_actors(world, L.to_ue(x, y, floor_z + HH + lift), R, HH, STATIC, None, [])
    return [a.get_actor_label() for a in (hits or []) if not a.actor_has_tag("door") and not a.actor_has_tag("carry")]      # doors open; frames stay


def walk(name, pts, step=10.0, lift=LIFT):
    """pts: (x, y, floor_z). Flat legs are sampled every `step` cm; a leg that changes height is sampled at its ends only.
    Stairs use lift=STAIR: the capsule is raised one riser so it tests width and headroom, not the next step's edge
    (the real player steps up; a standing-still overlap test cannot)."""
    bad = []
    for (a, b) in zip(pts[:-1], pts[1:]):
        n = 1 if abs(a[2] - b[2]) > 0.01 else max(1, int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) / step))
        for i in range(n + 1):
            f = i / float(n)
            p = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] if f < 1 else b[2])
            h = blocked(p[0], p[1], p[2], lift)
            if h:
                bad.append((tuple(round(v) for v in p), sorted(set(h))[:3]))
    print("%-28s %s" % (name, "PASS" if not bad else "FAIL x%d  first: %s" % (len(bad), bad[0])))
    return not bad


import house_plan as HP
importlib.reload(HP)
LND, F1, F2, F3, B, GR = HP.LND, HP.F1, HP.F2, HP.F3, HP.B, HP.GR
S = HP.STAIRS
flight = lambda k, mid: [((S[k]["start"] + S[k]["sign"] * (S[k]["tread"] * i + 14), mid) if S[k]["axis"] == "x" else (mid, S[k]["start"] + S[k]["sign"] * (S[k]["tread"] * i + 14)))
                         + (S[k]["first_top"] + S[k]["rise"] * i,) for i in range(S[k]["n"])]
res = []
for o in HP.OPENINGS:                                        # every doorway, walked straight through
    if o["kind"] == "window":
        continue
    am, z = (o["a0"] + o["a1"]) / 2.0, o["z0"]
    pts = [(o["t0"] - 55, am, z), (o["t1"] + 55, am, z)] if o["axis"] == "x" else [(am, o["t0"] - 55, z), (am, o["t1"] + 55, z)]
    if o.get("name") == "Door_garage":
        pts = [(am, o["t0"] - 40, z), (am, o["t1"] + 55, z)]
    res.append(walk(o.get("name", "opening s%d %s %d" % (o["storey"], o["axis"], o["a0"])), pts))
res += [
    walk("entry landing", [(60, 1181, LND), (130, 1125, LND), (60, 1181, LND), (50, 1245, LND)]),
    walk("up flight", flight("up", 50), lift=STAIR),
    walk("up flight top", [(50, 1512, F1), (160, 1512, F1)]),
    walk("basement flight", flight("down", 1125), lift=STAIR),
    walk("basement foot", [(390, 1125, B), (520, 1125, B), (520, 1240, B)]),
    walk("hall floor 1", [(160, 1512, F1), (300, 1420, F1), (525, 1420, F1), (525, 1130, F1), (425, 1125, F1)]),
    walk("stair to floor 2", flight("upper", 1235), lift=STAIR),
    walk("stair to floor 2 ends", [(525, 1340, F1), (525, 1235, F1)]),
    walk("upstairs arrival", [(60, 1235, F2), (40, 1356, F2)]),
    walk("upstairs gallery", [(40, 1356, F2), (640, 1356, F2), (640, 1235, F2)]),
    walk("back hall", [(639, 800, F2), (639, 1720, F2), (515, 1720, F2), (515, 1580, F2)]),
    walk("attic stair landing", [(105, 1478, F2), (135, 1478, F2)]),
    walk("attic flight", flight("attic", 1478), lift=STAIR),
    walk("loft", [(575, 1478, F3), (640, 1478, F3), (640, 1800, F3), (450, 1800, F3), (450, 1600, F3)]),
    walk("living room", [(515, 1010, F1), (515, 985, F1), (60, 985, F1), (45, 700, F1)]),
    walk("dining room", [(295, 1625, F1), (470, 1625, F1), (470, 1860, F1), (470, 1625, F1), (80, 1625, F1), (80, 1900, F1)]),
    walk("kitchen", [(650, 1390, F1), (674, 1345, F1), (674, 920, F1), (685, 905, F1), (674, 1345, F1), (950, 1345, F1), (950, 1000, F1), (950, 1295, F1), (1030, 1295, F1)]),
    walk("den", [(860, 1520, F1), (860, 1570, F1), (630, 1590, F1), (630, 1765, F1), (630, 1590, F1), (940, 1570, F1)]),
    walk("mudroom and half bath", [(685, 800, F1), (700, 660, F1), (770, 745, F1), (960, 745, F1)]),
    walk("parents' suite", [(50, 1120, F2), (200, 1100, F2), (288, 1045, F2), (480, 1045, F2), (288, 1045, F2), (288, 745, F2), (450, 745, F2)]),
    walk("sibling's room", [(760, 845, F2), (900, 860, F2), (1000, 860, F2)]),
    walk("Jack's room", [(760, 1345, F2), (900, 1345, F2), (880, 1420, F2)]),
    walk("hall bath", [(760, 1717, F2), (800, 1790, F2), (950, 1830, F2)]),
    walk("guest room", [(390, 1695, F2), (250, 1760, F2), (60, 1760, F2)]),
    walk("basement", [(520, 1125, B), (640, 1125, B), (830, 700, B), (880, 1860, B), (640, 1745, B), (345, 1745, B), (345, 1340, B), (525, 1340, B), (525, 1235, B)]),
]
if "GARAGE" in globals().get("EXTRA", "GARAGE"):
    g = HP.GARAGE
    res += [walk("garage steps", [(695, 540, F1)] + [(630 - 28 * i - 14, 525, F1 - 17.5 * (i + 1)) for i in range(7)], lift=STAIR),
            walk("garage floor", [(405, 525, g["floor"]), (405, 300, g["floor"]), (380, 100, g["floor"]), (700, 165, g["floor"]), (880, 165, GR + 2)])]
print("FIT CHECK:", "ALL PASS" if all(res) else "FAILURES ABOVE", "(%d routes)" % len(res))
