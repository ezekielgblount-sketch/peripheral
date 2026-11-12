"""Interactive things: the kitchen drawer, the two peripheral anomalies, world controller, ambient sounds, door sounds.
Safe to re-run: rebuilds everything tagged 'interactive'."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF, house_plan as HP
importlib.reload(L); importlib.reload(HP)
import props_r1, props_yard, props_loop
import props_small as PS
import props_90s as P9
import props_home as PH
import props_lived as PL
import props_story as PST
try:
    import props_pool as PP
except ImportError:
    pass
F1, F2 = HP.F1, HP.F2
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
(kx, ky), kf = HP.at("kitchen", "x1", 256, 58)
d = spawn_bp("BP_Mover", "Drawer_kitchen", kx, ky, F1 + 70, kf, "drawer_60")
d.set_editor_property("OpenYaw", 0.0); d.set_editor_property("Slide", unreal.Vector(38, 0, 0)); d.set_editor_property("Speed", 6.0)
d.set_editor_property("SndOpen", snd("drawer_slide"))

# door sounds
for a in eas.get_all_level_actors():
    if a.actor_has_tag("door"):
        a.set_editor_property("SndOpen", snd("drawer_slide" if a.actor_has_tag("garage_door") else "door_creak")); a.set_editor_property("SndLocked", snd("locked_rattle"))

# the one mechanic, in the periphery: the family photo in the upstairs hall, and the tin robot on Jack's dresser
(px, py), pf = HP.at("gallery", "y1", 250, 0.3)
p = spawn_bp("BP_Anomaly", "Anomaly_family_photo", px, py, F2 + 150, pf, "frame_family_a")
p.set_editor_property("HomeMesh", PF.get("frame_family_a")); p.set_editor_property("AltMesh", PF.get("frame_family_b"))
p.set_editor_property("Range", 900.0); p.set_editor_property("ArmTime", 0.6)
(tx, ty), tf = HP.at("jack", "x0", 394, 24)
t = spawn_bp("BP_Anomaly", "Anomaly_toy_robot", tx, ty, F2 + 83, tf, "toy_robot")
t.set_editor_property("HomeMesh", PF.get("toy_robot")); t.set_editor_property("AltMesh", PF.get("toy_robot"))
t.set_editor_property("AltOffset", unreal.Vector(6, 26, 0)); t.set_editor_property("AltYaw", -62.0)
t.set_editor_property("Range", 700.0); t.set_editor_property("ArmTime", 0.6)
for a_ in (p, t):
    a_.tags = ["interactive", "periph"]

# ---------------- Day One story objects ----------------
GR, LND, B = HP.GR, HP.LND, HP.B
CAR = (-520, 150)                                              # where the car ends up on the driveway
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

static("car", "Car", CAR[0], CAR[1], GR, (1, 0), ["s_car"])
hint = eas.spawn_actor_from_class(unreal.PointLight, L.to_ue(CAR[0] - 180, CAR[1] - 30, GR + 90))            # objective hint glow, moved by the director
hint.set_actor_label("Objective_hint"); hint.set_folder_path("Interactive/Story"); hint.tags = ["interactive", "s_hint"]
hc = hint.light_component
hc.set_mobility(unreal.ComponentMobility.MOVABLE); hc.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
hc.set_editor_property("intensity", 55.0); hc.set_editor_property("attenuation_radius", 150.0); hc.set_editor_property("cast_shadows", False)
hc.set_editor_property("light_color", unreal.Color(r=255, g=214, b=150, a=255))
static("box_carry_a", "Box_A", CAR[0] - 182, CAR[1] - 32, GR + 58.6, (-1, 0), ["carry", "s_boxa"])
static("box_carry_b", "Box_B", CAR[0] - 182, CAR[1] + 34, GR + 58.6, (-1, 0.1), ["carry", "s_boxb"])
static("mail_pile", "Mail", 62, 1205, LND + 0.3, (1, 0.3), ["carry", "s_mail"])
(bx_, by_), bf = HP.at("b_foot", "y0", 44, 1)
static("breaker_panel", "Breaker_panel", bx_, by_, B + 150, bf, [], movable=False)
mover("Breaker_lever", "breaker_lever", bx_, by_ + 11, B + 156, bf, ["s_lever"], slide=(0, 0, -7), speed=14.0, sound="click")
mover("Window_sash", "window_sash", -8.5, 746.4, F1 + 64, (1, 0), ["s_sash"], slide=(0, 0, 46), speed=3.0)
(fx_, fy_), ff = HP.at("kitchen", "x1", 38, 0.3)                # the fridge body stands here, facing into the kitchen
mover("Fridge_door", "fridge_door", fx_ - 71, fy_ + 37.5, F1 + 6, (0, -1), ["s_fridge"], yaw=100.0, speed=3.0, sound="door_creak")
for i, (dx, dy, z) in enumerate(((20, -12, 41), (18, 14, 41), (24, -6, 67), (20, 12, 93))):
    t_ = spawn_bp("BP_Trash", "Fridge_food_%d" % i, fx_ - dx - 14, fy_ + dy, F1 + z, (-1, 0), "food_%d" % i, "Interactive/Story")
    t_.tags = ["interactive", "trash"]
for a in eas.get_all_level_actors():
    lbl = a.get_actor_label()
    if lbl == "Door_front":
        a.tags = [t for t in a.tags if str(t) != "s_door"] + ["s_door"]; a.set_editor_property("StickCount", 1); a.set_editor_property("SndLocked", snd("stuck_lock"))
    if lbl == "Door_parents":                                 # the parents' room: on Day One the door opens, but Jack will not go in
        a.tags = [t for t in a.tags if str(t) != "s_pdoor"] + ["s_pdoor"]
    if isinstance(a, unreal.PlayerStart):
        a.set_actor_location_and_rotation(L.to_ue(CAR[0] - 315, CAR[1], GR + 92), unreal.Rotator(roll=0, pitch=0, yaw=0), False, False)
blk = L.box("Blocker_parents_room", 5, 1166, F2, 96, 1172, F2 + 203, "blk", "Interactive/Story", "interactive")
blk.set_actor_hidden_in_game(True); blk.tags = ["interactive", "s_blocker"]; blk.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
def board(label, tag, v):
    """A shared value three numbers wide: Blueprints read and write its location."""
    a = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*v))
    a.set_actor_label(label); a.set_folder_path("Interactive/Boards"); a.tags = ["interactive", tag]
    a.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
board("Settings_blackboard", "bb", (1, 0.6, 0))        # X camera-motion intensity, Y mouse speed, Z power stage
board("Settings_blackboard_2", "sb", (90, 1, 1))       # X field of view, Y look up/down sign (-1 = inverted), Z unease cap 0..1
board("Menu_blackboard", "ub", (1, 0, 1))              # X screen (0 play, 1 title, 2 pause, 3 settings, 4 how to play), Y button pressed, Z screen to go back to
board("Chore_blackboard", "cb", (0, 0, 0))             # X chores-done bits, Y 1 while the chore day runs, Z request from the day (1 dishes back, 2 lawn strip)
board("Day_blackboard", "db", (0, 0, 0))               # X anomalies-fired bits, Y seconds into the day, Z caption to show

# game mode uses the director HUD; hand it the task-note images
hud = eal.load_asset("/Game/Blueprints/BP_HUD")
unreal.get_default_object(hud.generated_class()).set_editor_property("Notes", [eal.load_asset("/Game/Prints/ui_task_%d" % i) for i in range(1, 11)])
UI_NAMES = (["ui_menu_%d" % i for i in range(5)] + ["ui_pause_%d" % i for i in range(3)] + ["ui_howto"] + ["ui_settings_%d_%d" % (c, q) for c in range(3) for q in range(4)]
            + ["ui_loop_%d" % i for i in range(5)] + ["ui_preset_%d" % i for i in range(3)]
            + ["ui_row_cam_%d_%d" % (c, o) for c in range(3) for o in range(2)] + ["ui_row_gfx_%d_%d" % (q, o) for q in range(4) for o in range(2)]
            + ["ui_row_mouse_%d_%d" % (m, o) for m in range(5) for o in range(2)] + ["ui_set_head", "ui_set_foot"])            # menu and on-screen text, drawn as images
unreal.get_default_object(hud.generated_class()).set_editor_property("UI", [eal.load_asset("/Game/Prints/" + n) for n in UI_NAMES])
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


ambient("Amb_fridge", "fridge_hum", 1045, 900, 90, 60, 520, 0.5)
ambient("Amb_clock", "clock_tick", 287, 615, 150, 80, 650, 0.9)
ambient("Amb_outdoor_front", "outdoor_day", -500, 1300, 100, 500, 1400, 0.9)
ambient("Amb_outdoor_back", "outdoor_day", 1700, 1100, 100, 700, 1800, 0.8)
ambient("Amb_outdoor_far_front", "outdoor_day", -1900, 1100, 100, 900, 2500, 0.9)

# player sounds
bp = eal.load_asset("/Game/Blueprints/BP_Player")
cdo = unreal.get_default_object(bp.generated_class())
for var, wave in (("StepCarpet", "step_carpet"), ("StepWood", "step_wood"), ("StepTile", "step_tile"), ("SndClick", "click")):
    cdo.set_editor_property(var, snd(wave))
eal.save_asset("/Game/Blueprints/BP_Player")
print("interactive built")
