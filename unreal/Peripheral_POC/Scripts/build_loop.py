"""The loop sequence's set dressing: one clock (its second hand is turned by the game director) and five anomalies made from
the house's own things. Each anomaly is an actor tagged an<N> (hidden until its pass); the normal thing it replaces is tagged
an<N>n. Run after dress_rooms.py and build_interactive.py (they rebuild the actors this script tags). Safe to re-run."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF, props_story, props_loop, props_small, props_90s, props_home, props_lived, props_pool
importlib.reload(props_loop)
F1 = 0
L.clear("loop")
for a_ in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():        # start clean: drop old loop tags, mark the peripheral anomalies
    tg = [t for t in a_.tags if not (str(t).startswith("an") and str(t)[2:3].isdigit()) and str(t) != "periph"]
    if a_.get_actor_label().startswith("Anomaly_"):
        tg.append("periph")
    if len(tg) != len(a_.tags) or "periph" in [str(t) for t in tg]:
        a_.tags = tg
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


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


# 0: a door that should not be there, on the blank stair wall of the hall
put("false_door", "Loop_false_door", 330, 1251.3, F1, (0, 1), ["an0"])
# 1: the family photo above the chair by the piano: the child is gone from the picture
put("frame_family_b", "Loop_family_photo", 215, 601.7, F1 + 150, (0, 1), ["an1"])
# 2: the THANKFUL banner on the mantel is spelled wrong (the right one is placed here too, so the two can be swapped)
put("banner_thankful", "Loop_banner", 531.5, 708, F1 + 124, (-1, 0), ["an2n"]); put("banner_wrong", "Loop_banner_wrong", 531.5, 708, F1 + 124, (-1, 0), ["an2"])
# 3: the hall clock runs backward (always there; only its second hand changes direction)
put("wall_clock", "Loop_clock", 385, 1251.3, F1 + 178, (0, 1), [])
put("clock_hand", "Loop_clock_hand", 385, 1254.4, F1 + 178, (0, 1), ["an_clockhand"], movable=True)
# 4: the chair by the piano has been pulled out and turned to face the wall
put("spindle_chair", "Loop_chair", 200, 668, F1, (0, -1), ["an4"]); normal("Living_spindle_chair_1", "an4n")
# 5: the television is on, showing nothing
put(PF.variant("flat_tv", True), "Loop_tv", 250, 1012, F1 + 66, (0, -1), ["an5"]); normal("Living_flat_tv_1", "an5n")
g = eas.spawn_actor_from_class(unreal.PointLight, L.to_ue(250, 975, F1 + 95))
g.set_actor_label("Loop_tv_glow"); g.set_folder_path("Loop"); g.tags = ["loop", "an5"]; g.set_actor_hidden_in_game(True); g.set_is_temporarily_hidden_in_editor(True)
c = g.light_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
c.set_editor_property("intensity", 45.0); c.set_editor_property("attenuation_radius", 260.0); c.set_editor_property("cast_shadows", False)
c.set_editor_property("light_color", unreal.Color(r=150, g=175, b=235, a=255))
print("loop set built")
