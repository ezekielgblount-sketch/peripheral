"""Places the chore controller (BP_Chores) and the anomaly-day controller (BP_Day) and hands them their lists (tag 'day').
Run after dress_rooms.py, build_chores.py and build_interactive.py. Safe to re-run."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, house_plan as HP, props_furniture as PF, build_anoms, build_anoms2
importlib.reload(HP)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
L.clear("day")
NAMES = ["Family photo: everyone faces away", "THANKFUL banner lost a letter", "Fridge magnet moved, drawing gained a figure", "Every clock shows 3:17",
         "Parents' door is ajar", "Washed dishes are back in the sink", "A strip of lawn is long again", "Television is on (static)",
         "Dining chair pulled out", "A light is back on", "Upstairs hall is longer", "Two coats on the rail", "Answering machine: 1 new message",
         "New height mark above Jack's", "Shoes by the door"] + build_anoms.MORE_NAMES + build_anoms2.MORE_NAMES      # 15 onward: the second anomaly pass (build_anoms.py)
N = len(NAMES)
acts = eas.get_all_level_actors()
def first(tag):
    return next((a.get_actor_location() for a in acts if a.actor_has_tag(tag)), None)
special = {4: L.to_ue(50, 1180, HP.F2 + 100), 5: L.to_ue(1048, 1043, HP.F1 + 90), 6: L.to_ue(2150, 600, HP.GR + 20), 9: unreal.Vector(0, 0, 0),
           10: L.to_ue(639, HP.HALL_CAP["y"], HP.F2 + 120)}
probes = []
for i in range(N):
    p = special.get(i) or first("dy%d" % i) or first("dy%dn" % i)
    if p is None:
        raise RuntimeError("no place found for anomaly %d" % i)
    probes.append(p)
def spawn(bp, label):
    a = eas.spawn_actor_from_class(eal.load_blueprint_class("/Game/Blueprints/" + bp), unreal.Vector(0, 0, -600))
    a.set_actor_label(label); a.set_folder_path("Day"); a.tags = ["day"]
    a.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    return a
ch = spawn("BP_Chores", "Chore_controller")
day = spawn("BP_Day", "Day_controller")
for k, v in (("Probes", probes), ("ShowTags", ["dy%d" % i for i in range(N)]), ("HideTags", ["dy%dn" % i for i in range(N)]),
             ("Seen", [False] * N), ("IsFired", [False] * N), ("DayLen", 1200.0), ("GapMin", 35.0), ("GapMax", 75.0), ("Names", NAMES)):
    day.set_editor_property(k, v)
cp = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, -100, 0))      # caption board: X = which caption, Y = when it was set
cp.set_actor_label("Caption_blackboard"); cp.set_folder_path("Day"); cp.tags = ["day", "cp"]; cp.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
for a in acts:
    if a.get_actor_label() == "Sun":
        a.tags = [t for t in a.tags if str(t) != "sun"] + ["sun"]
print("day built; anomaly spots:", len(probes))
