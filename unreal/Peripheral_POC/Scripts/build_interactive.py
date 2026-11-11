"""Interactive things: the kitchen drawer, the two peripheral anomalies, world controller, ambient sounds, door sounds.
Safe to re-run: rebuilds everything tagged 'interactive'."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF
importlib.reload(L)
import props_small as PS
import props_90s as P9
import props_home as PH
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

# world controller (day/night, quality keys, room tone)
w = eas.spawn_actor_from_class(cls("BP_World"), unreal.Vector(0, 0, 300))
w.set_actor_label("World"); w.set_folder_path("Interactive"); w.tags = ["interactive"]
wbp = eal.load_asset("/Game/Blueprints/BP_World")
unreal.get_default_object(wbp.generated_class()).set_editor_property("SndTone", snd("room_tone"))
eal.save_asset("/Game/Blueprints/BP_World")


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
