"""Second anomaly pass (tag 'anom'): things from Joel's older lists that were not in the game yet.
  - false positives: ordinary things the height and width of a person, left in dim corners
  - edge-of-eye changes (BP_Anomaly): a floor lamp that leans, a portrait that turns its heads away, someone at the end of the upstairs hall
  - figures seen through glass (BP_Glimpse): at Jack's bedroom window from the yard, outside the living room window from indoors
  - someone who is only in the mirror (BP_OnlyMirror); someone crossing a far doorway (BP_Passer)
  - six more changes made while Jack is out of the room (BP_Day numbers 15 to 20; build_day.py reads the list from here)
  - small sounds from elsewhere in the house (BP_Paranoia)
Run after dress_rooms.py, build_openings.py and build_story.py, and before build_day.py. Safe to re-run."""
import sys, math, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import dress_lib as D
importlib.reload(D)
from dress_lib import P, PW, L, K, PF, HP, hidden
F1, F2, B, GR = HP.F1, HP.F2, HP.B, HP.GR
eas, eal = D.eas, unreal.EditorAssetLibrary
MORE_NAMES = ["A fifth door upstairs", "The SOLD sign lost its smile", "Wedding photo is face-down", "A kitchen cabinet is open", "A tap is running",
              "Half-bath door is wide open"]
if __name__ == "__main__":
    print("cleared", D.begin("anom"))
    r = "Anom"
    before = [a for a in eas.get_all_level_actors() if isinstance(a, unreal.StaticMeshActor) and not a.actor_has_tag("anom")
              and any(a.actor_has_tag(t) for t in ("dress", "story", "chore", "interactive", "site"))]
    placed = []
    def keep(a):
        placed.append(a); return a

    def bx(a):
        o, e = a.get_actor_bounds(False); return (o.x - e.x, o.y - e.y, o.z - e.z, o.x + e.x, o.y + e.y, o.z + e.z)
    solid = [(a.get_actor_label(), bx(a)) for a in before]
    solid = [(n, c) for (n, c) in solid if c[3] - c[0] < 700 and c[4] - c[1] < 700]            # leave out the merged shell pieces
    solid = [(n, (c[0] - 1, c[1] - 1, c[2], c[3] + 1, c[4] + 1, c[5])) for (n, c) in solid]     # flat things (posters, charts) have no thickness of their own
    def hits(b):
        return [n for (n, c) in solid if min(b[3], c[3]) - max(b[0], c[0]) > 0.1 and min(b[4], c[4]) - max(b[1], c[1]) > 0.1 and min(b[5], c[5]) - max(b[2], c[2]) > 2]
    def near_opening(x, y, z, pad=80):
        for o in HP.OPENINGS:
            if o["kind"] == "window":                       # nothing tall or framed goes in front of a window
                if not (z - 30 <= o["z0"] <= z + 250):
                    continue
            elif not (o["z0"] - 30 <= z <= o["z0"] + 30):
                continue
            (ox0, ox1, oy0, oy1) = (o["t0"], o["t1"], o["a0"], o["a1"]) if o["axis"] == "x" else (o["a0"], o["a1"], o["t0"], o["t1"])
            if ox0 - pad < x < ox1 + pad and oy0 - pad < y < oy1 + pad:
                return True
        return False
    def free(prop, room_name, sides, w, d, h, collide=True, inset=1.0, zoff=0.0, spawn=True, tags=()):
        """Put a prop against the first clear stretch of wall in a room (tries each side in turn, corners first)."""
        rm = HP.room(room_name); x0, y0, x1, y1 = rm["rect"]; z = rm["floor"] + zoff
        for side in sides:
            length = (y1 - y0) if side in ("x0", "x1") else (x1 - x0)
            steps = sorted(range(int(w / 2 + 6), int(length - w / 2 - 6), 18), key=lambda v: min(v, length - v) if zoff == 0 else abs(v - length * 0.42))
            for along in steps:
                (x, y), f = HP.at(room_name, side, along, inset)
                cx, cy = x + f[0] * d / 2.0, y + f[1] * d / 2.0
                hw, hd = (w / 2.0, d / 2.0) if f[0] == 0 else (d / 2.0, w / 2.0)
                c = L.to_ue(cx, cy, z)
                if hits((c.x - hw, c.y - hd, z + 1, c.x + hw, c.y + hd, z + h)) or near_opening(cx, cy, rm["floor"], 80 if zoff == 0 else 45):
                    continue
                if not spawn:
                    solid.append((prop, (c.x - hw, c.y - hd, z, c.x + hw, c.y + hd, z + h)))
                    return (x, y, f)
                a = keep(P(prop, x, y, z + (h / 2.0 if zoff else 0.0), f, r, collide=collide, tags=tags)); solid.append((a.get_actor_label(), bx(a)))
                return a
        print("NO ROOM for", prop, "in", room_name)

    # ---- false positives ----
    free("draped_boxes", "b_rec", ("x1", "y1"), 64, 56, 170); free("draped_boxes", "guest", ("y1", "x0"), 64, 56, 170)
    free("mop_bucket", "kitchen", ("y0", "x0", "y1"), 40, 44, 172, collide=False); free("mop_bucket", "b_mid", ("x0", "y1"), 40, 44, 172, collide=False)
    free("coat_chair", "den", ("y1", "x1", "x0"), 64, 48, 110) or free("coat_chair", "living", ("x1", "y1", "x0"), 64, 48, 110); free("tall_plant", "hall_main", ("y0", "y1", "x1"), 50, 42, 180, collide=False)
    free("box_stack_tall", "sibling", ("x1", "y1", "y0", "x0"), 56, 56, 172) or free("box_stack_tall", "pcloset", ("x1", "y1", "y0"), 56, 56, 172) or free("box_stack_tall", "b_rec", ("y0", "x1"), 56, 56, 172); free("box_stack_tall", "b_east", ("y1", "x0"), 56, 56, 172)
    free("curtain_bunched", "b_store", ("x0", "y0"), 52, 30, 196, collide=False); free("curtain_bunched", "dining", ("x0", "y1"), 52, 30, 196, collide=False)
    lamp_at = free("empty_spot", "den", ("x0", "y1", "x1"), 46, 46, 170, collide=False)

    # ---- edge of the eye ----
    ANOM = eal.load_blueprint_class("/Game/Blueprints/BP_Anomaly")
    def periph(label, home, alt, x, y, z, face, day, rng=900.0, arm=0.5):
        a = eas.spawn_actor_from_class(ANOM, L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=math.degrees(math.atan2(-face[1], face[0]))))
        a.set_actor_label(label); a.set_folder_path("Anom"); a.tags = ["anom", "ent", "ent%d" % day, "periph"]
        c = a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(home); c.set_collision_profile_name("NoCollision")
        for k, v in (("HomeMesh", home), ("AltMesh", alt), ("Range", rng), ("ArmTime", arm)):
            a.set_editor_property(k, v)
        return keep(a)
    lp = lamp_at.get_actor_location(); lyaw = lamp_at.get_actor_rotation().yaw; eas.destroy_actor(lamp_at); placed.remove(lamp_at)
    periph("Anom_floor_lamp", PF.variant("floor_lamp", False), PF.get("floor_lamp_lean"), lp.x + 450, 1150 - lp.y, F1,
           (math.cos(math.radians(lyaw)), -math.sin(math.radians(lyaw))), 2)
    px, py, pf = free("portrait", "hall_main", ("y1", "x1", "y0"), 60, 8, 50, inset=0.3, zoff=130.0, spawn=False)
    periph("Anom_portrait", PF.get("frame_portrait"), PF.get("frame_portrait_turned"), px, py, F1 + 152, pf, 3, arm=0.6)

    # ---- family snapshots on the walls (not anomalies: the house simply has more of the family in it) ----
    for n, room_name, sides in (("bday", "dining", ("y0", "x1")), ("bike", "hall_main", ("x1", "y0")), ("xmas", "living", ("x1", "y1")), ("dock", "den", ("x1", "y0")),
                                ("beach", "gallery", ("y1", "y0")), ("driveway", "hall_back", ("x1", "y1")), ("baby", "parents", ("y1", "x0")), ("yard", "guest", ("x1", "y0")),
                                ("dock", "back_hall_s", ("x1", "x0")), ("xmas", "arrival", ("x0", "y0")), ("bday", "jack", ("y0", "x1")), ("beach", "kitchen", ("y1", "x0"))):
        free("frame_snap_" + n, room_name, sides, 40, 8, 36, collide=False, inset=0.3, zoff=132.0)
    periph("Anom_hall_end", PF.get("empty_spot"), PF.get("entity_figure"), -6, 1350, F2, (1, 0), 4, rng=1300.0, arm=0.3)

    # ---- seen through glass ----
    GL = eal.load_blueprint_class("/Game/Blueprints/BP_Glimpse")
    def glimpse(label, x, y, z, face, day, rng, mind, mesh="entity_void"):
        a = eas.spawn_actor_from_class(GL, L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=math.degrees(math.atan2(-face[1], face[0]))))
        a.set_actor_label(label); a.set_folder_path("Anom"); a.tags = ["anom", "ent", "ent%d" % day]
        c = a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(PF.get(mesh))
        c.set_collision_profile_name("NoCollision"); c.set_cast_shadow(False)
        a.set_editor_property("Range", rng); a.set_editor_property("MinDist", mind)
        return a
    glimpse("Glimpse_jack_window", 1101, 1352, F2 + 91, (1, 0), 3, 3200.0, 650.0, "figure_window")          # from the back yard: someone at his old bedroom window
    glimpse("Glimpse_living_window", -46, 840, F1 - 34, (1, 0), 4, 900.0, 260.0)      # from the living room: someone outside, close to the glass

    # ---- movement in a doorway: someone crosses the far end of a view, off to the side of where he is looking ----
    PS = eal.load_blueprint_class("/Game/Blueprints/BP_Passer")
    def passer(label, a, b, z, day, secs, rng, mind):
        yaw = math.degrees(math.atan2(-(b[1] - a[1]), b[0] - a[0]))
        p = eas.spawn_actor_from_class(PS, L.to_ue(a[0], a[1], z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        p.set_actor_label(label); p.set_folder_path("Anom"); p.tags = ["anom", "ent", "ent%d" % day]
        c = p.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(PF.get("entity_void"))
        c.set_collision_profile_name("NoCollision"); c.set_cast_shadow(False)
        for k, v in (("B", L.to_ue(b[0], b[1], z)), ("Time", secs), ("Range", rng), ("MinDist", mind)):
            p.set_editor_property(k, v)
    passer("Passer_upstairs", (640, 1200), (640, 1500), F2, 4, 1.5, 1100.0, 380.0)       # across the far end of the upstairs hall, from the back hall
    passer("Passer_kitchen", (690, 1290), (690, 1490), F1, 4, 1.2, 900.0, 300.0)         # past the kitchen doorway, seen from the front hall

    # ---- only in the mirror ----
    OM = eal.load_blueprint_class("/Game/Blueprints/BP_OnlyMirror")
    def in_mirror(label, x, y, z, face, day):
        a = eas.spawn_actor_from_class(OM, L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=math.degrees(math.atan2(-face[1], face[0]))))
        a.set_actor_label(label); a.set_folder_path("Anom"); a.tags = ["anom", "ent", "ent%d" % day]
        c = a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(PF.get("entity_void"))
        c.set_collision_profile_name("NoCollision"); c.set_cast_shadow(False); c.set_editor_property("owner_no_see", True)
        return a
    in_mirror("Mirror_figure_parents", 2, 965, F2, (1, -0.2), 4)
    in_mirror("Mirror_figure_living", 425, 668, F1, (-0.3, 1), 3)

    # ---- changed while he was out of the room: BP_Day numbers 15 to 20 ----
    (dx, dy), df = HP.at("gallery", "y1", 430, 0.3)
    hidden(P("false_door", dx, dy, F2, df, r, collide=False, tags=["dy15"]))
    for (tag, prop) in (("dy16n", "sign_sold"), ("dy16", "sign_sold_b")):
        s = P(prop, -640, 1490, GR, (-1, 0.25), r, collide=False, tags=[tag], movable=True)
        if tag == "dy16": hidden(s)
    (mx, my), mf = HP.at("living", "y0", 287, 20)
    P("frame_stand_wedding", mx + 44, my - 6, F1 + 146, mf, r, collide=False, tags=["dy17n"], movable=True)
    hidden(P("frame_facedown", mx + 44, my - 8, F1 + 146, mf, r, collide=False, tags=["dy17"], movable=True))
    hidden(P("cabinet_door_ajar", 1046, 983, F1 + 141.5, (-1, 0), r, collide=False, tags=["dy18"]))
    hidden(P("tap_stream", 1056, 1043, F1 + 111, (-1, 0), r, collide=False, tags=["dy19"]))
    hidden(P("empty_spot", 856, 745, F1 + 100, (1, 0), r, collide=False, tags=["dy20"]))          # a marker: the door itself is found by its tag
    for a in eas.get_all_level_actors():
        if a.get_actor_label() == "Door_halfbath":
            a.tags = [t for t in a.tags if str(t) != "dy_bdoor"] + ["dy_bdoor"]

    # ---- sounds from elsewhere ----
    pc = eas.spawn_actor_from_class(eal.load_blueprint_class("/Game/Blueprints/BP_Paranoia"), unreal.Vector(0, 0, -760))
    pc.set_actor_label("Paranoia_controller"); pc.set_folder_path("Anom"); pc.tags = ["anom"]
    acts = eas.get_all_level_actors()
    first = lambda tag, d: next((a.get_actor_location() for a in acts if a.actor_has_tag(tag)), d)
    pc.set_editor_property("Fixed", [L.to_ue(-10, 1180, HP.LND + 110), first("dy12n", L.to_ue(300, 1400, F1 + 90)), first("dy7n", L.to_ue(673, 1880, F1 + 96)),
                                  L.to_ue(-420, 1000, GR + 20)])          # 3: the gravel by the front walk
    pc.set_editor_property("Spots", [L.to_ue(*p) for p in ((800, 1300, B + 200), (300, 800, B + 200), (300, 1350, F2 + 20), (120, 1480, F2 + 120), (180, 880, F2 + 20),
                                                           (900, 880, F2 + 20), (900, 1380, F2 + 20), (830, 1150, F1 + 20), (300, 1750, F1 + 20), (720, 720, F1 + 20))])
    pc.set_editor_property("GapMin", 45.0); pc.set_editor_property("GapMax", 110.0)

    # ---- report anything that now sits inside something else ----
    old = [(n, c) for (n, c) in solid if n not in [a.get_actor_label() for a in placed]]
    for a in placed:
        b = bx(a); h = [n for (n, c) in old if min(b[3], c[3]) - max(b[0], c[0]) > 3 and min(b[4], c[4]) - max(b[1], c[1]) > 3 and min(b[5], c[5]) - max(b[2], c[2]) > 3]
        lo = a.get_actor_location()
        print(("OVERLAP " if h else "clear   ") + a.get_actor_label(), (round(lo.x + 450), round(1150 - lo.y), round(lo.z)), h[:4])
    print("anoms placed")
