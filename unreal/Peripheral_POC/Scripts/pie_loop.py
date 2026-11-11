"""Play-mode test helper for the loop. STEP = 'start' | 'info' | 'go' (GO = 'x,y' blueprint cm, upstairs; LOOK = 'x,y' optional).
'go' only places the test pawn so a script can walk the route; the game itself never moves the player."""
import sys, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
GS = unreal.GameplayStatics
hud = GS.get_all_actors_of_class(w, unreal.HUD)[0]; pawn = GS.get_player_pawn(w, 0); pc = GS.get_player_controller(w, 0)
acts = GS.get_all_actors_of_class(w, unreal.Actor)
by = lambda lbl: next(a for a in acts if a.get_actor_label() == lbl)
step = globals().get("STEP", "info")
if step == "start":
    hud.set_editor_property("LoopStart", True)
if step == "go":
    x, y = [float(v) for v in globals()["GO"].split(",")]
    pawn.set_actor_location(L.to_ue(x, y, 259 + 92), False, True)
    if globals().get("LOOK"):
        tx, ty = [float(v) for v in globals()["LOOK"].split(",")]
        pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(pawn.get_actor_location(), L.to_ue(tx, ty, 259 + 92)))
c = by("Loop_controller"); G = c.get_editor_property; lb = by("Loop_blackboard").get_actor_location()
p = pawn.get_actor_location()
shown = sorted(a.get_actor_label() for a in acts if any(str(t).startswith("an") and str(t)[2:3].isdigit() for t in a.tags) and not a.get_editor_property("hidden"))
cap = by("Cap_wall").get_actor_location(); dv = by("Divider_moving")
print(step, "| mode", hud.get_editor_property("Mode"), "fade", round(hud.get_editor_property("Fade"), 2), "| board", [round(v, 1) for v in lb.to_tuple()],
      "| pawn bp", round(p.x + 450), round(1150 - p.y), round(p.z), "| entry", G("Entry"), "k", G("K"), "streak", G("Streak"), "ok", G("Ok"),
      "stretch", G("Stretch"), "S", round(G("S")), "of", round(G("SMax")), "moving", G("Moving"),
      "| far wall bp y", round(1150 - cap.y - 6), "divider len", round(dv.get_actor_scale3d().y * 100),
      "| corridor shown", not by("Wall_leg2_outer").get_editor_property("hidden"), "side wall hidden", by("W2_right_a_0_a").get_editor_property("hidden"),
      "| door A yaw", round(by("Door_upstairs_a").get_actor_rotation().yaw), "door B yaw", round(by("Door_upstairs_b").get_actor_rotation().yaw),
      "| wrong things shown", shown)
