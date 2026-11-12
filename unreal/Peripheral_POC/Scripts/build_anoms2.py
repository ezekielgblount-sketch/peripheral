"""Third anomaly pass (tag 'anom2'): what was still missing from Joel's lists after build_anoms.py.
  - the last of the handoff's twelve: the jacket that hangs as if worn, the kitchen chair turned to face the hall, the sign's
    name line gone blank (BP_Day numbers 21 to 23), someone in the bathroom mirror, someone standing in the trees behind the house
  - more ordinary person-shaped things: a dress form, a robe on a hook, coveralls on a nail, an ironing board with a shirt on it
Run after build_anoms.py and before build_day.py. Safe to re-run."""
import sys, math, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import dress_lib as D
importlib.reload(D)
from dress_lib import P, L, PF, HP, hidden
F1, F2, B, GR = HP.F1, HP.F2, HP.B, HP.GR
eas, eal = D.eas, unreal.EditorAssetLibrary
MORE_NAMES = ["The mud room jacket hangs as if worn", "A kitchen chair faces the hall", "The sign's WELCOME HOME is blank"]
if __name__ == "__main__":
    print("cleared", D.begin("anom2"))
    r = "Anom2"
    acts = eas.get_all_level_actors()
    before = [a for a in acts if isinstance(a, unreal.StaticMeshActor) and any(a.actor_has_tag(t) for t in ("dress", "story", "chore", "interactive", "site", "anom"))]
    placed = []
    def bx(a):
        o, e = a.get_actor_bounds(False); return (o.x - e.x, o.y - e.y, o.z - e.z, o.x + e.x, o.y + e.y, o.z + e.z)
    solid = [(a.get_actor_label(), bx(a)) for a in before]
    solid = [(n, (c[0] - 1, c[1] - 1, c[2], c[3] + 1, c[4] + 1, c[5])) for (n, c) in solid if c[3] - c[0] < 700 and c[4] - c[1] < 700]
    def hits(b):
        return [n for (n, c) in solid if min(b[3], c[3]) - max(b[0], c[0]) > 0.1 and min(b[4], c[4]) - max(b[1], c[1]) > 0.1 and min(b[5], c[5]) - max(b[2], c[2]) > 2]
    def near_opening(x, y, z, pad=80):
        for o in HP.OPENINGS:
            if o["kind"] == "window":
                if not (z - 30 <= o["z0"] <= z + 250):
                    continue
            elif not (o["z0"] - 30 <= z <= o["z0"] + 30):
                continue
            (ox0, ox1, oy0, oy1) = (o["t0"], o["t1"], o["a0"], o["a1"]) if o["axis"] == "x" else (o["a0"], o["a1"], o["t0"], o["t1"])
            if ox0 - pad < x < ox1 + pad and oy0 - pad < y < oy1 + pad:
                return True
        return False
    def free(prop, room_name, sides, w, d, h, collide=True):
        """Put a prop against the first clear stretch of wall in a room (each side in turn, corners first)."""
        rm = HP.room(room_name); x0, y0, x1, y1 = rm["rect"]; z = rm["floor"]
        for side in sides:
            length = (y1 - y0) if side in ("x0", "x1") else (x1 - x0)
            for along in sorted(range(int(w / 2 + 6), int(length - w / 2 - 6), 18), key=lambda v: min(v, length - v)):
                (x, y), f = HP.at(room_name, side, along, 1.0)
                cx, cy = x + f[0] * d / 2.0, y + f[1] * d / 2.0
                hw, hd = (w / 2.0, d / 2.0) if f[0] == 0 else (d / 2.0, w / 2.0)
                c = L.to_ue(cx, cy, z)
                if hits((c.x - hw, c.y - hd, z + 1, c.x + hw, c.y + hd, z + h)) or near_opening(cx, cy, rm["floor"]):
                    continue
                a = P(prop, x, y, z, f, r, collide=collide); placed.append(a); solid.append((a.get_actor_label(), bx(a)))
                return a
        print("NO ROOM for", prop, "in", room_name)

    # ---- false positives ----
    free("dress_form", "guest", ("x0", "y1", "x1", "y0"), 46, 46, 180)
    free("robe_hook", "pbath", ("x0", "y1", "x1"), 62, 18, 186, collide=False); free("robe_hook", "bath", ("x0", "y1", "y0"), 62, 18, 186, collide=False)
    free("coveralls_hung", "b_mid", ("y0", "x1", "y1"), 60, 30, 180, collide=False); free("coveralls_hung", "b_east", ("y1", "x0", "x1"), 60, 30, 180, collide=False)
    free("ironing_board_up", "back_hall_n", ("x1", "x0"), 48, 22, 172, collide=False) or free("ironing_board_up", "alcove", ("x0", "y1", "y0"), 48, 22, 172, collide=False)
    free("ironing_board_up", "b_rec", ("x1", "y1", "x0"), 48, 22, 172, collide=False)

    # ---- someone in the bathroom mirror (the edge-of-eye rule: there until looked at) ----
    ANOM = eal.load_blueprint_class("/Game/Blueprints/BP_Anomaly")
    def periph(label, home, alt, x, y, z, face, day, rng, arm):
        a = eas.spawn_actor_from_class(ANOM, L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=math.degrees(math.atan2(-face[1], face[0]))))
        a.set_actor_label(label); a.set_folder_path("Anom2"); a.tags = ["anom2", "ent", "ent%d" % day, "periph"]
        c = a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(home); c.set_collision_profile_name("NoCollision"); c.set_cast_shadow(False)
        for k, v in (("HomeMesh", home), ("AltMesh", alt), ("Range", rng), ("ArmTime", arm)):
            a.set_editor_property(k, v)
    periph("Anom_bath_mirror", PF.get("empty_spot"), PF.get("figure_mirror"), 900, 1665.8, F2 + 150, (0, 1), 3, 520.0, 0.4)
    periph("Anom_halfbath_mirror", PF.get("empty_spot"), PF.get("figure_mirror"), 990, 603.8, F1 + 150, (0, 1), 4, 420.0, 0.4)

    # ---- someone standing in the trees behind the house, seen from Jack's bedroom window or from the yard ----
    g = eas.spawn_actor_from_class(eal.load_blueprint_class("/Game/Blueprints/BP_Glimpse"), L.to_ue(3170, 1500, GR), unreal.Rotator(roll=0, pitch=0, yaw=180))
    g.set_actor_label("Glimpse_treeline"); g.set_folder_path("Anom2"); g.tags = ["anom2", "ent", "ent2"]
    c = g.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(PF.get("entity_void")); c.set_collision_profile_name("NoCollision"); c.set_cast_shadow(False)
    g.set_editor_property("Range", 3800.0); g.set_editor_property("MinDist", 900.0)

    # ---- changed while he was out of the room: BP_Day numbers 21 to 23 ----
    def retag(label, tag):
        for a in acts:
            if a.get_actor_label() == label:
                a.tags = [t for t in a.tags if str(t) != tag] + [tag]; a.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
                return a
        print("MISSING", label)
    retag("Mud_coat_hooks_1", "dy21n")
    hidden(P("coat_hooks_worn", 850, 650, F1 + 165, (-1, 0), r, collide=False, tags=["dy21"], movable=True))
    retag("Kitchen_kitchen_chair_1", "dy22n")
    hidden(P("kitchen_chair", 662, 1136, F1, (-1, 0.55), r, collide=False, tags=["dy22"], movable=True))
    P("sign_rider", -640, 1490, GR, (-1, 0.25), r, collide=False, tags=["dy23n"], movable=True)
    hidden(P("sign_rider_blank", -640, 1490, GR, (-1, 0.25), r, collide=False, tags=["dy23"], movable=True))

    for a in placed:
        lo = a.get_actor_location(); print("placed", a.get_actor_label(), (round(lo.x + 450), round(1150 - lo.y), round(lo.z)), round(a.get_actor_rotation().yaw))
    print("anoms2 placed")
