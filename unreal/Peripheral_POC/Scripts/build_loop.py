"""The loop sequence's set dressing, in the upstairs hall: a clock (BP_Loop turns its second hand) and the things that can be
wrong on a pass. Each wrong thing is an actor tagged an<N>, hidden until its pass; the normal thing it replaces is tagged
an<N>n. BP_Loop swaps them while Jack is in the corridor and cannot see the hall. Run after dress_rooms.py and
build_interactive.py (they rebuild the actors this script tags), then build_annex.py. Safe to re-run."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF, props_story, props_loop, props_small, props_90s, props_home, props_lived, props_pool, props_r1
importlib.reload(props_loop)
F2 = 259
L.clear("loop")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a_ in eas.get_all_level_actors():        # start clean: drop old loop tags, mark the peripheral anomalies
    tg = [t for t in a_.tags if not (str(t).startswith("an") and str(t)[2:3].isdigit()) and str(t) != "periph"]
    if a_.get_actor_label().startswith("Anomaly_"):
        tg.append("periph")
    if len(tg) != len(a_.tags) or "periph" in [str(t) for t in tg]:
        a_.tags = tg


def put(mesh, label, x, y, z, face, tags, movable=False):
    a = K.place(mesh if not isinstance(mesh, str) else PF.get(mesh), label, x, y, z, face=face, folder="Loop", tag="loop", collide=False, movable=movable)
    a.tags = ["loop"] + tags
    if any(t.startswith("an") and t[2:].isdigit() for t in tags):
        a.set_actor_hidden_in_game(True); a.set_is_temporarily_hidden_in_editor(True)
    return a


def normal(label, tag):
    for a in eas.get_all_level_actors():
        if a.get_actor_label() == label:
            a.tags = [t for t in a.tags if not str(t).startswith("an")] + [tag]; return a
    raise RuntimeError("missing " + label)


WALL = 1415.7                    # the upstairs gallery wall that has the attic door in it (its face looks toward -Y)
# 0: a door that should not be there, on the gallery wall
put("false_door", "Loop_false_door", 430, WALL, F2, (0, -1), ["an0"])
# 1: the family photo in the back hall: the child is gone from the picture
put("frame_family_a", "Loop_family_photo_ok", 578.3, 1500, F2 + 150, (1, 0), ["an1n"]); put("frame_family_b", "Loop_family_photo", 578.3, 1500, F2 + 150, (1, 0), ["an1"])
# 2: the school photo hangs upside down
school = next(a_.get_actor_label() for a_ in eas.get_all_level_actors() if a_.get_actor_label().startswith("Hall2_frame_school_b"))
up = put("frame_school_b", "Loop_school_photo", 300, WALL, F2 + 152, (0, -1), ["an2"]); normal(school, "an2n")
r = up.get_actor_rotation(); up.set_actor_rotation(unreal.Rotator(roll=180.0, pitch=r.pitch, yaw=r.yaw), False)
# 3: the hall clock runs backward (always there; only its second hand changes direction)
put("wall_clock", "Loop_clock", 500, WALL, F2 + 186, (0, -1), [])
put("clock_hand", "Loop_clock_hand", 500, WALL - 3.1, F2 + 186, (0, -1), ["an_clockhand"], movable=True)
# 4: a chair stands at the front end of the hall, turned to face the wall
put("spindle_chair", "Loop_chair", -8, 1340, F2, (-1, 0), ["an4"])
# 5: a television is on in Jack's room: cold light spills out of his doorway
g = eas.spawn_actor_from_class(unreal.PointLight, L.to_ue(770, 1345, F2 + 95))
g.set_actor_label("Loop_tv_glow"); g.set_folder_path("Loop"); g.tags = ["loop", "an5"]; g.set_actor_hidden_in_game(True); g.set_is_temporarily_hidden_in_editor(True)
c = g.light_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
c.set_editor_property("intensity", 260.0); c.set_editor_property("attenuation_radius", 520.0); c.set_editor_property("cast_shadows", True)
c.set_editor_property("light_color", unreal.Color(r=120, g=160, b=255, a=255))
c.set_editor_property("light_function_material", unreal.EditorAssetLibrary.load_asset("/Game/Materials/M_Flicker"))
print("loop set built")
