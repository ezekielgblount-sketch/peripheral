import sys, os, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
step = os.environ.get("STEP", globals().get("STEP", "info"))
def actors(cls=unreal.Actor): return unreal.GameplayStatics.get_all_actors_of_class(w, cls)
def by_label(lbl): return next(a for a in actors() if a.get_actor_label() == lbl)
pawn = unreal.GameplayStatics.get_player_pawn(w, 0); pc = unreal.GameplayStatics.get_player_controller(w, 0)
def look_at(x, y, z):
    cam = pawn.get_actor_location() + unreal.Vector(0, 0, 76)
    pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(cam, L.to_ue(x, y, z)))
if step == "info":
    print("pawn", pawn.get_class().get_name(), pawn.get_actor_location())
elif step == "door":
    d = by_label("Door_front"); print("door yaw before", round(d.get_actor_rotation().yaw, 1))
    unreal.GameplayStatics.apply_damage(d, 1.0, pc, pawn, None)
elif step == "door2":
    d = by_label("Door_front"); print("door yaw after", round(d.get_actor_rotation().yaw, 1), "open", d.get_editor_property("Open"))
elif step == "goto_photo":
    pawn.set_actor_location(L.to_ue(300, 850, 92), False, True); look_at(280, 601, 160)
elif step == "look_away":
    look_at(300, 1019, 160)
elif step == "look_back":
    look_at(280, 601, 160)
elif step == "goto_robot":
    pawn.set_actor_location(L.to_ue(760, 1480, 259 + 92), False, True); look_at(604, 1568, 259 + 95)
elif step == "robot_away":
    look_at(880, 1400, 259 + 150)
elif step == "robot_back":
    look_at(610, 1542, 259 + 95)
for n in ("Anomaly_family_photo", "Anomaly_toy_robot"):
    a = by_label(n)
    print(n, "state", a.get_editor_property("State"), "timer", round(a.get_editor_property("Timer"), 2), "mesh", a.static_mesh_component.static_mesh.get_name(), "yaw", round(a.get_actor_rotation().yaw))
if step == "drawer":
    d = by_label("Drawer_kitchen"); print("drawer before", d.get_actor_location()); unreal.GameplayStatics.apply_damage(d, 1.0, pc, pawn, None)
if step == "drawer2":
    print("drawer after", by_label("Drawer_kitchen").get_actor_location())
if step == "lights":
    print("night lights:", len([a for a in actors() if a.actor_has_tag("night_light")]), "hidden:", len([a for a in actors() if a.actor_has_tag("night_light") and a.is_hidden()]))
