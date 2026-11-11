import sys, os, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
GS = unreal.GameplayStatics
step = globals().get("STEP", "info")
acts = GS.get_all_actors_of_class(w, unreal.Actor)
by = lambda lbl: next(a for a in acts if a.get_actor_label() == lbl)
hud = GS.get_all_actors_of_class(w, unreal.HUD)[0]
pawn = GS.get_player_pawn(w, 0); pc = GS.get_player_controller(w, 0)
hit = lambda a: GS.apply_damage(a, 1.0, pc, pawn, None)
G = hud.get_editor_property
if step == "start":
    hud.set_editor_property("Mode", 1); hud.set_editor_property("FadeTarget", 0.0); pc.set_ignore_move_input(False); pc.set_ignore_look_input(False)
elif step == "t1": by("Box_A").set_actor_location(by("Box_A").get_actor_location() + unreal.Vector(-80, 0, 30), False, True)
elif step == "t2": by("Box_A").set_actor_location(L.to_ue(-60, 1136, -100), False, True)
elif step == "t3a": hit(by("Door_front"))
elif step == "t3b": hit(by("Door_front"))
elif step == "t4": by("Box_A").set_actor_location(L.to_ue(120, 1200, -126), False, True); by("Box_B").set_actor_location(L.to_ue(150, 1090, -126), False, True)
elif step == "t5": by("Mail").set_actor_location(L.to_ue(860, 770, 92), False, True)
elif step == "t6": hit(by("Breaker_lever"))
elif step == "t7": hit(by("Window_sash"))
elif step == "t8":
    hit(by("Fridge_door"))
    for a in acts:
        if a.actor_has_tag("trash"): hit(a)
elif step == "t9a": hit(by("Door_upstairs_a")); pawn.set_actor_location(L.to_ue(195, 1330, 259 + 92), False, True)
elif step == "t9b": pawn.set_actor_location(L.to_ue(740, 1480, 259 + 92), False, True)
elif step == "t10": hud.set_editor_property("Mode", 3); hud.set_editor_property("Step", 0); hud.set_editor_property("T", 6.5)
elif step == "skip": hud.set_editor_property("T", 41.5)
print(step, "| mode", G("Mode"), "task", G("Task"), "step", G("Step"), "T", round(G("T"), 1), "unease", round(G("Unease"), 1), "target", G("Target"), "fade", round(G("Fade"), 2),
      "noteT", round(G("NoteT"), 1), "power", G("Power"), "| pawn", [round(v) for v in pawn.get_actor_location().to_tuple()],
      "lights on", len([a for a in acts if a.actor_has_tag("power_light") and not a.is_hidden_ed() and not a.get_editor_property("hidden")]),
      "trash", len([a for a in acts if a.actor_has_tag("trash")]), "door yaw", round(by("Door_front").get_actor_rotation().yaw))
if step == "drive":
    hud.set_editor_property("Mode", 5); hud.set_editor_property("T", 0.0); hud.set_editor_property("FadeTarget", 0.0); pawn.set_actor_enable_collision(False)
if step in ("drive", "car"):
    c = by("Car"); print("car", [round(v) for v in c.get_actor_location().to_tuple()], "yaw", round(c.get_actor_rotation().yaw), "boxA", [round(v) for v in by("Box_A").get_actor_location().to_tuple()], "hint", [round(v) for v in by("Objective_hint").get_actor_location().to_tuple()])
