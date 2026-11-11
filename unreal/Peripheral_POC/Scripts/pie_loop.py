"""Play-mode test helper for the loop and lamps. STEP = 'lamp' | 'right' | 'wrong' | 'info'."""
import unreal
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
GS = unreal.GameplayStatics
hud = GS.get_all_actors_of_class(w, unreal.HUD)[0]; pawn = GS.get_player_pawn(w, 0); pc = GS.get_player_controller(w, 0)
G = hud.get_editor_property; acts = GS.get_all_actors_of_class(w, unreal.Actor)
step = globals().get("STEP", "info")
if step == "lamp":
    a = next(x for x in acts if x.get_actor_label() == "Switch_torchiere"); GS.apply_damage(a, 1.0, pc, pawn, None)
if step in ("right", "wrong"):
    had = G("LoopK") >= 0
    back = had if step == "right" else not had
    pawn.set_actor_location(unreal.Vector(-400, 20, -30) if back else unreal.Vector(-270, 290, 92), False, True)
shown = sorted(a.get_actor_label() for a in acts if any(str(t).startswith("an") and str(t)[2:].isdigit() for t in a.tags) and not a.get_editor_property("hidden"))
print(step, "| mode", G("Mode"), "phase", G("LoopPhase"), "k", G("LoopK"), "streak", G("Streak"), "fade", round(G("Fade"), 2), "pawn", [round(v) for v in pawn.get_actor_location().to_tuple()],
      "anomaly shown", shown, "| torchiere lit", next(x for x in acts if x.get_actor_label() == "Switch_torchiere").get_editor_property("Shown"),
      "light", not next(x for x in acts if x.get_actor_label() == "Lamp_torchiere").get_editor_property("hidden"))
