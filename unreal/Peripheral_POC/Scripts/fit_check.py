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
    return [a.get_actor_label() for a in (hits or [])]


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


LND, F1, F2, B = -126, 0, 259, -252
up = [(50, 1251 + 28 * i + 14, LND + 18 * (i + 1)) for i in range(6)]
down = [(180 + 28 * i + 14, 1080, LND - 18 * (i + 1)) for i in range(6)]
upper = [(470 - 28 * i - 14, 1190, 18.5 * (i + 1)) for i in range(13)]

ok = all([
    walk("front door", [(-70, 1136, LND), (60, 1136, LND)]),
    walk("entry landing", [(60, 1136, LND), (130, 1080, LND), (130, 1200, LND), (50, 1200, LND)]),
    walk("up flight", up, lift=STAIR),
    walk("up flight top", [(50, 1460, F1), (160, 1460, F1)]),
    walk("basement flight", down, lift=STAIR),
    walk("basement foot", [(390, 1080, B), (450, 1080, B)]),
    walk("hall floor 1", [(160, 1460, F1), (300, 1365, F1), (525, 1365, F1), (525, 1085, F1), (425, 1080, F1)]),
    walk("kitchen door", [(525, 1345, F1), (650, 1345, F1)]),
    walk("kitchen length", [(740, 1500, F1), (740, 650, F1)]),
    walk("living room door", [(515, 1090, F1), (515, 960, F1), (300, 800, F1), (60, 660, F1)]),
    walk("stair to floor 2", upper, lift=STAIR),
    walk("stair to floor 2 ends", [(525, 1300, F1), (525, 1190, F1)]),
    walk("upstairs arrival", [(60, 1190, F2), (40, 1310, F2)]),
    walk("upstairs hall", [(60, 1190, F2), (40, 1310, F2), (520, 1310, F2), (520, 1195, F2), (510, 1440, F2)]),
    walk("bathroom door", [(520, 1195, F2), (640, 1195, F2), (740, 1235, F2)]),
    walk("bedroom door", [(510, 1430, F2), (640, 1430, F2), (740, 1600, F2)]),
])
print("FIT CHECK:", "ALL PASS" if ok else "FAILURES ABOVE")
