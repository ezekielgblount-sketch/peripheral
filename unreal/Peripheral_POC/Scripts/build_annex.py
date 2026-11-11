"""The corridor that should not exist: it leaves the upstairs hall by the door at the end of the hall leg, turns twice and
comes back out of the parents' door, so walking on brings Jack back to where he started without ever being moved.
Its far end is a wall and a divider the game slides and stretches (BP_Loop), so the corridor can grow while he walks it.
Run after build_interactive.py (it rebuilds the parents-room blocker this script tags). Everything here is hidden with collision off until the loop sequence starts. Numbers are blueprint cm. Safe to re-run."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF, props_loop
importlib.reload(L); importlib.reload(props_loop)
F2, C2 = 259, 503
YEND = 2630                      # how far the corridor shell runs: the far wall can retreat 9 m, short of the house next door
CAP0 = 1690                      # where the far wall rests: just inside the house's own side wall
X1A, X1B = 458, 564              # leg 1 (in from the hall leg): clear width
X2A, X2B = 140, 251              # leg 2 (back out through the parents' door)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L.clear("annex")
F = "Annex"


def box(name, x0, y0, z0, x1, y1, z1, m, tags=(), movable=False, collide=True):
    a = L.box(name, x0, y0, z0, x1, y1, z1, m, F, "annex", collide=collide)
    a.tags = ["annex"] + list(tags)
    if movable:
        a.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    a.set_actor_hidden_in_game(True)
    return a


def prop(mesh, name, x, y, z, face, tags=(), movable=False):
    a = K.place(PF.get(mesh) if isinstance(mesh, str) else mesh, name, x, y, z, face=face, folder=F, tag="annex", collide=False, movable=movable)
    a.tags = ["annex"] + list(tags); a.set_actor_hidden_in_game(True)
    return a


def light(name, x, y, lumens, tags=(), shadows=False, radius=420):
    a = eas.spawn_actor_from_class(unreal.PointLight, L.to_ue(x, y, C2 - 24))
    a.set_actor_label(name); a.set_folder_path(F); a.tags = ["annex"] + list(tags); a.set_actor_hidden_in_game(True)
    c = a.light_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
    c.set_editor_property("intensity", lumens); c.set_editor_property("use_temperature", True); c.set_editor_property("temperature", 2700.0)
    c.set_editor_property("attenuation_radius", radius); c.set_editor_property("source_radius", 4.0); c.set_editor_property("soft_source_radius", 6.0)
    c.set_editor_property("cast_shadows", shadows)
    prop(PF.variant("ceiling_light", True), name + "_fixture", x, y, C2, (1, 0), tags)


# ---- inside the house: paper over the blockout faces the corridor shows ----
box("Skin_leg_end_a", X1A, 1506, F2, 472, 1508, C2, "hall2"); box("Skin_leg_end_b", 553, 1506, F2, 566, 1508, C2, "hall2")
box("Skin_leg_end_top", 472, 1506, F2 + 203, 553, 1508, C2, "hall2")
box("Skin_bedroom_wall", X1B, 1508, F2, 566, 1700, C2, "hall2")
box("Skin_parents_a", X2A, 1383, F2, 150, 1385, C2, "hall2"); box("Skin_parents_b", 241, 1383, F2, X2B, 1385, C2, "hall2")
box("Skin_parents_top", 150, 1383, F2 + 203, 241, 1385, C2, "hall2")
box("Wall_leg2_outer", X2A - 12, 1383, F2, X2A, YEND, C2, "hall2")
box("Divider_fixed", X2B, 1383, F2, 446, 1494, C2, "hall2")
# ---- past the house wall ----
box("Floor_out", X2A - 12, 1700, F2 - 15, X1B + 12, YEND, F2, "f_hall2")
box("Ceiling_out", X2A - 12, 1700, C2, X1B + 12, YEND, C2 + 15, "ceiling")
box("Wall_leg1_outer", X1B, 1700, F2, X1B + 12, YEND, C2, "hall2")
box("End_plug", X2A - 12, YEND, F2 - 15, X1B + 12, YEND + 12, C2 + 15, "hall2")
# baseboards on the fixed walls
box("Base_leg2_outer", X2A, 1385, F2, X2A + 1.3, YEND, F2 + 9, "trim", collide=False)
box("Base_leg1_outer", X1B - 1.3, 1508, F2, X1B, YEND, F2 + 9, "trim", collide=False)
box("Base_divider_fixed", X2B - 1.3, 1385, F2, X2B, 1494, F2 + 9, "trim", collide=False)

# ---- the parts the game moves (BP_Loop): the far wall, and the divider between the two legs ----
box("Cap_wall", X2A - 12, CAP0, F2, X1B + 12, CAP0 + 12, C2, "hall2", ["ax_capw"], movable=True)
prop("annex_cap_trim", "Cap_trim", (X2A + X1B) / 2.0, CAP0, F2, (0, -1), ["ax_cap"], movable=True)
prop("frame_landscape_a", "Cap_picture", (X1A + X1B) / 2.0, CAP0, F2 + 150, (0, -1), ["ax_cap"], movable=True)
box("Divider_moving", X2B, 1494, F2, X1A, CAP0 - 110, C2, "hall2", ["ax_div"], movable=True)
box("Base_divider_l", X2B - 1.3, 1494, F2, X2B, CAP0 - 110, F2 + 9, "trim", ["ax_div"], movable=True, collide=False)
box("Base_divider_r", X1A, 1494, F2, X1A + 1.3, CAP0 - 110, F2 + 9, "trim", ["ax_div"], movable=True, collide=False)

# ---- what the retreating wall uncovers: more doors, more pictures, more ceiling lights ----
for i, y in enumerate((1880, 2280)):
    prop("false_door", "Door_leg1_%d" % i, X1B, y, F2, (-1, 0))
    prop("false_door", "Door_leg2_%d" % i, X2A, y + 200, F2, (1, 0))
for i, (m, y) in enumerate((("frame_school", 2080), ("frame_family_b", 2440))):
    prop(m, "Pic_leg1_%d" % i, X1B, y, F2 + 150, (-1, 0))
light("Annex_light_turn", (X2B + X1A) / 2.0, CAP0 - 55, 520, ["ax_l0"], shadows=True)
light("Annex_light_leg2", (X2A + X2B) / 2.0, 1470, 380, shadows=True, radius=330)
for i, y in enumerate((1980, 2400)):
    light("Annex_light_a%d" % i, (X1A + X1B) / 2.0, y, 420, ["ax_l%d" % (i + 1)])
    light("Annex_light_b%d" % i, (X2A + X2B) / 2.0, y, 420, ["ax_l%d" % (i + 1)])

# ---- house pieces in the corridor's way: hidden (collision off) while the loop runs ----
n = 0
for a in eas.get_all_level_actors():
    tg = [t for t in a.tags if str(t) != "annex_hide"]
    lbl = a.get_actor_label()
    if lbl.startswith("W2_right_a") or lbl in ("Blocker_parents_room", "Tree_24", "Chimney"):      # the side wall, the Day One blocker, a tree whose crown reaches in
        tg.append("annex_hide"); n += 1
    if len(tg) != len(a.tags) or "annex_hide" in [str(t) for t in tg]:
        a.tags = tg
for lbl in ("F2_b4_blk_f", "F2_b5_blk_f"):
    for a in eas.get_all_level_actors():
        if a.get_actor_label() == lbl:
            a.static_mesh_component.set_material(0, L.mat("f_hall2"))
for a in eas.get_all_level_actors():                       # the door at the end of the hall leg: locked by day, opens during the loop
    if a.get_actor_label() == "Door_upstairs_b":
        a.tags = [t for t in a.tags if str(t) != "s_bdoor"] + ["s_bdoor"]; a.set_editor_property("LoopKey", True)
ctl = eas.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Loop"), unreal.Vector(0, 0, -500))
ctl.set_actor_label("Loop_controller"); ctl.set_folder_path(F); ctl.tags = ["annex"]
ctl.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
lb = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0))      # loop blackboard: X = running, Y = right calls in a row, Z = finished
lb.set_actor_label("Loop_blackboard"); lb.set_folder_path(F); lb.tags = ["annex", "lb"]
lb.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
print("annex built; house pieces hidden during the loop:", n)
