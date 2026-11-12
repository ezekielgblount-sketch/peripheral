"""The corridor that should not exist. The two closets at the far end of the upstairs hall are its first stretch: during the
loop the side wall of the house behind them is taken away and the corridor runs on outside, turns round the end of the thin
wall between the closets and comes back, so walking on brings Jack out of the other closet door without ever being moved.
Its far wall and the dividing wall are slid and stretched by BP_Loop, so the corridor can grow while he walks it.
Run after build_openings.py and build_interactive.py. Everything here is hidden with collision off until the loop starts.
Numbers are blueprint cm. Safe to re-run."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF, props_loop, house_plan as HP
importlib.reload(L); importlib.reload(props_loop); importlib.reload(HP)
F2, C2 = HP.F2, HP.C2
AX = HP.ANNEX
(X1A, X1B), (X2A, X2B) = AX["leg1"], AX["leg2"]          # leg 1 (closet B) and leg 2 (closet A): clear widths
WY, CAP0, YEND = AX["wall_y"], AX["cap0"], AX["yend"]
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


# ---- past the house wall: floor, ceiling, the two outer walls, the far plug ----
box("Floor_out", X2A - 12, WY, F2 - 15, X1B + 12, YEND, F2, "f_c_hall")
box("Ceiling_out", X2A - 12, WY, C2, X1B + 12, YEND, C2 + 15, "ceiling")
box("Wall_leg2_outer", X2A - 12, WY, F2, X2A, YEND, C2, "w_hall")
box("Wall_leg1_outer", X1B, WY, F2, X1B + 12, YEND, C2, "w_hall")
box("End_plug", X2A - 12, YEND, F2 - 15, X1B + 12, YEND + 12, C2 + 15, "w_hall")
box("Base_leg2_outer", X2A, WY, F2, X2A + 1.3, YEND, F2 + 9, "white", collide=False)
box("Base_leg1_outer", X1B - 1.3, WY, F2, X1B, YEND, F2 + 9, "white", collide=False)
# ---- the parts the game moves (BP_Loop): the far wall, and the wall between the two legs ----
box("Cap_wall", X2A - 12, CAP0, F2, X1B + 12, CAP0 + 12, C2, "w_hall", ["ax_capw"], movable=True)
prop("frame_landscape_a", "Cap_picture", (X1A + X1B) / 2.0, CAP0, F2 + 150, (0, -1), ["ax_cap"], movable=True)
box("Cap_base", X2A, CAP0 - 1.3, F2, X1B, CAP0, F2 + 9, "white", ["ax_cap"], movable=True, collide=False)
box("Divider_moving", X2B, WY, F2, X1A, CAP0 - AX["turn"], C2, "w_hall", ["ax_div"], movable=True)
# ---- what the retreating wall uncovers: more doors, more pictures, more ceiling lights ----
for i, y in enumerate((2300, 2700)):
    prop("false_door", "Door_leg1_%d" % i, X1B, y, F2, (-1, 0))
    prop("false_door", "Door_leg2_%d" % i, X2A, y + 180, F2, (1, 0))
for i, (m, y) in enumerate((("frame_school", 2500), ("frame_family_b", 2860))):
    prop(m, "Pic_leg1_%d" % i, X1B, y, F2 + 150, (-1, 0))
light("Annex_light_turn", (X2B + X1A) / 2.0, CAP0 - 55, 520, ["ax_l0"], shadows=True)
light("Annex_light_closet_b", (X1A + X1B) / 2.0, 1870, 380, shadows=True, radius=330)
light("Annex_light_closet_a", (X2A + X2B) / 2.0, 1870, 380, shadows=True, radius=330)
for i, y in enumerate((2400, 2800)):
    light("Annex_light_a%d" % i, (X1A + X1B) / 2.0, y, 420, ["ax_l%d" % (i + 1)])
    light("Annex_light_b%d" % i, (X2A + X2B) / 2.0, y, 420, ["ax_l%d" % (i + 1)])
# ---- the two closet doors: locked by day, they open during the loop ----
n = 0
for a in eas.get_all_level_actors():
    lbl = a.get_actor_label()
    for (door, tag) in (("Door_closet_b", "s_bdoor"), ("Door_closet_a", "s_adoor")):
        if lbl == door:
            a.tags = [t for t in a.tags if str(t) != tag] + [tag]; a.set_editor_property("LoopKey", True)
    if a.actor_has_tag("annex_hide"):
        n += 1
ctl = eas.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Loop"), unreal.Vector(0, 0, -500))
ctl.set_actor_label("Loop_controller"); ctl.set_folder_path(F); ctl.tags = ["annex"]
ctl.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
lb = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0))      # loop blackboard: X = running, Y = right calls in a row, Z = finished
lb.set_actor_label("Loop_blackboard"); lb.set_folder_path(F); lb.tags = ["annex", "lb"]
lb.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
print("annex built; pieces of side wall the loop takes away:", n)
