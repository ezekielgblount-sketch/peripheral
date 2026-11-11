"""Interactive things: the kitchen drawer, the two peripheral anomalies, world controller, ambient sounds, door sounds.
Safe to re-run: rebuilds everything tagged 'interactive'."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF
importlib.reload(L)
import props_small as PS
import props_90s as P9
import props_home as PH
import props_lived as PL
import props_story as PST
try:
    import props_pool as PP
except ImportError:
    pass
F1, F2 = 0, 259
L.clear("interactive")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
snd = lambda n: eal.load_asset("/Game/Audio/" + n)
cls = lambda n: eal.load_blueprint_class("/Game/Blueprints/" + n)


def spawn_bp(bp, label, x, y, z, face, mesh, folder="Interactive"):
    import math
    yaw = math.degrees(math.atan2(-face[1], face[0]))
    a = eas.spawn_actor_from_class(cls(bp), L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
    a.set_actor_label(label); a.set_folder_path(folder); a.tags = ["interactive"]
    c = a.static_mesh_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(PF.get(mesh))
    return a


# kitchen drawer (slides out 38 cm)
d = spawn_bp("BP_Mover", "Drawer_kitchen", 900 - 58, 895, F1 + 70, (-1, 0), "drawer_60")
d.set_editor_property("OpenYaw", 0.0); d.set_editor_property("Slide", unreal.Vector(38, 0, 0)); d.set_editor_property("Speed", 6.0)
d.set_editor_property("SndOpen", snd("drawer_slide"))

# door sounds
for a in eas.get_all_level_actors():
    if a.actor_has_tag("door"):
        a.set_editor_property("SndOpen", snd("door_creak")); a.set_editor_property("SndLocked", snd("locked_rattle"))

# anomaly 1: the family photo above the couch. Unwatched, the child is gone from the picture.
p = spawn_bp("BP_Anomaly", "Anomaly_family_photo", 105, 601, F1 + 155, (0, 1), "frame_family_a")
p.set_editor_property("HomeMesh", PF.get("frame_family_a")); p.set_editor_property("AltMesh", PF.get("frame_family_b"))
p.set_editor_property("Range", 900.0); p.set_editor_property("ArmTime", 0.6)
# anomaly 2: the tin robot on Jack's dresser. Unwatched, it slides along the dresser and turns toward the bed.
t = spawn_bp("BP_Anomaly", "Anomaly_toy_robot", 604, 1568, F2 + 83, (1, 0), "toy_robot")
t.set_editor_property("HomeMesh", PF.get("toy_robot")); t.set_editor_property("AltMesh", PF.get("toy_robot"))
t.set_editor_property("AltOffset", unreal.Vector(6, 26, 0)); t.set_editor_property("AltYaw", -62.0)
t.set_editor_property("Range", 700.0); t.set_editor_property("ArmTime", 0.6)

# anomaly 3 (kitchen): a chair at the table. Unwatched, it is pulled out and turned toward the room.
ch = spawn_bp("BP_Anomaly", "Anomaly_kitchen_chair", 760, 1392, F1, (1, 0.15), "kitchen_chair")
ch.set_editor_property("HomeMesh", PF.get("kitchen_chair")); ch.set_editor_property("AltMesh", PF.get("kitchen_chair"))
ch.set_editor_property("AltOffset", unreal.Vector(-34, 22, 0)); ch.set_editor_property("AltYaw", 125.0)
ch.set_editor_property("Range", 800.0); ch.set_editor_property("ArmTime", 0.6)

# ---------------- Day One story objects ----------------
GR, LND, B = -140, -126, -252
def static(mesh, label, x, y, z, face, tags, movable=True, collide=True):
    a = K.place(PF.get(mesh), label, x, y, z, face=face, folder="Interactive/Story", tag="interactive", collide=collide, movable=movable)
    a.tags = ["interactive"] + tags
    return a
def mover(label, mesh, x, y, z, face, tags, yaw=0.0, slide=(0, 0, 0), speed=4.0, sound="drawer_slide"):
    m = spawn_bp("BP_Mover", label, x, y, z, face, mesh, "Interactive/Story")
    m.tags = ["interactive"] + tags
    m.set_editor_property("OpenYaw", yaw); m.set_editor_property("Slide", unreal.Vector(*slide)); m.set_editor_property("Speed", speed)
    m.set_editor_property("SndOpen", snd(sound)); m.set_editor_property("SndLocked", snd("stuck_lock"))
    return m

static("car", "Car", -520, 360, GR, (1, 0), ["s_car"])
hint = eas.spawn_actor_from_class(unreal.PointLight, L.to_ue(-700, 330, GR + 90))            # objective hint glow, moved by the director
hint.set_actor_label("Objective_hint"); hint.set_folder_path("Interactive/Story"); hint.tags = ["interactive", "s_hint"]
hc = hint.light_component
hc.set_mobility(unreal.ComponentMobility.MOVABLE); hc.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
hc.set_editor_property("intensity", 55.0); hc.set_editor_property("attenuation_radius", 150.0); hc.set_editor_property("cast_shadows", False)
hc.set_editor_property("light_color", unreal.Color(r=255, g=214, b=150, a=255))
static("box_carry_a", "Box_A", -702, 328, GR + 58.6, (-1, 0), ["carry", "s_boxa"])
static("box_carry_b", "Box_B", -702, 394, GR + 58.6, (-1, 0.1), ["carry", "s_boxb"])
static("mail_pile", "Mail", 62, 1160, LND + 0.3, (1, 0.3), ["carry", "s_mail"])
static("breaker_panel", "Breaker_panel", 420, 1032, B + 150, (0, 1), [], movable=False)
mover("Breaker_lever", "breaker_lever", 420, 1043, B + 156, (0, 1), ["s_lever"], slide=(0, 0, -7), speed=14.0, sound="click")
mover("Window_sash", "window_sash", -8.5, 726.4, F1 + 64, (1, 0), ["s_sash"], slide=(0, 0, 46), speed=3.0)
mover("Fridge_door", "fridge_door", 827, 682.5, F1 + 6, (0, -1), ["s_fridge"], yaw=100.0, speed=3.0, sound="door_creak")
for i, (dx, dy, z) in enumerate(((20, -12, 41), (18, 14, 41), (24, -6, 67), (20, 12, 93))):
    t_ = spawn_bp("BP_Trash", "Fridge_food_%d" % i, 898 - dx - 14, 645 + dy, F1 + z, (-1, 0), "food_%d" % i, "Interactive/Story")
    t_.tags = ["interactive", "trash"]
for a in eas.get_all_level_actors():
    lbl = a.get_actor_label()
    if lbl == "Door_front":
        a.tags = list(a.tags) + ["s_door"]; a.set_editor_property("StickCount", 1); a.set_editor_property("SndLocked", snd("stuck_lock"))
    if lbl == "Door_upstairs_a":                              # the parents' room: the door opens, but Jack will not go in
        a.tags = list(a.tags) + ["s_pdoor"]; a.set_editor_property("Locked", False)
    if isinstance(a, unreal.PlayerStart):
        a.set_actor_location_and_rotation(L.to_ue(-835, 360, GR + 92), unreal.Rotator(roll=0, pitch=0, yaw=0), False, False)
blk = L.box("Blocker_parents_room", 152, 1384, F2, 239, 1390, F2 + 203, "blk", "Interactive/Story", "interactive")
blk.set_actor_hidden_in_game(True)
bb = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(1, 0, 0))      # shared settings: X = camera-motion intensity
bb.set_actor_label("Settings_blackboard"); bb.set_folder_path("Interactive"); bb.tags = ["interactive", "bb"]
bb.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)

# game mode uses the director HUD; hand it the task-note images
hud = eal.load_asset("/Game/Blueprints/BP_HUD")
unreal.get_default_object(hud.generated_class()).set_editor_property("Notes", [eal.load_asset("/Game/Prints/ui_task_%d" % i) for i in range(1, 11)])
eal.save_asset("/Game/Blueprints/BP_HUD")
gm = eal.load_asset("/Game/Blueprints/BP_GameMode")
unreal.get_default_object(gm.generated_class()).set_editor_property("hud_class", hud.generated_class())
eal.save_asset("/Game/Blueprints/BP_GameMode")


def ambient(label, wave, x, y, z, inner, falloff, vol):
    a = eas.spawn_actor_from_class(unreal.AmbientSound, L.to_ue(x, y, z))
    a.set_actor_label(label); a.set_folder_path("Interactive/Audio"); a.tags = ["interactive"]
    ac = a.audio_component
    ac.set_sound(snd(wave)); ac.set_editor_property("volume_multiplier", vol)
    ac.set_editor_property("override_attenuation", True)
    att = ac.get_editor_property("attenuation_overrides")
    att.set_editor_property("attenuation_shape_extents", unreal.Vector(inner, 0, 0))
    att.set_editor_property("falloff_distance", falloff)
    ac.set_editor_property("attenuation_overrides", att)
    return a


ambient("Amb_fridge", "fridge_hum", 865, 645, 90, 60, 520, 0.5)
ambient("Amb_clock", "clock_tick", 560, 708, 155, 80, 650, 0.9)
ambient("Amb_outdoor_front", "outdoor_day", -500, 1100, 100, 500, 1400, 0.9)
ambient("Amb_outdoor_back", "outdoor_day", 1500, 1100, 100, 500, 1400, 0.8)
ambient("Amb_outdoor_far_front", "outdoor_day", -1900, 1100, 100, 900, 2500, 0.9)

# player sounds
bp = eal.load_asset("/Game/Blueprints/BP_Player")
cdo = unreal.get_default_object(bp.generated_class())
for var, wave in (("StepCarpet", "step_carpet"), ("StepWood", "step_wood"), ("StepTile", "step_tile"), ("SndClick", "click")):
    cdo.set_editor_property(var, snd(wave))
eal.save_asset("/Game/Blueprints/BP_Player")
print("interactive built")
