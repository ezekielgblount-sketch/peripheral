"""Play-mode test helper for the chore day. STEP = 'start' | 'info' | 'go' | 'use' | 'hold' | 'drop' | 'look'.
GO = 'x,y,z' blueprint cm (pawn feet-level floor z); HOLD = actor label; MODE = 'carry' | 'push'. Test only: the game never moves the player."""
import sys, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
GS = unreal.GameplayStatics
pawn = GS.get_player_pawn(w, 0); pc = GS.get_player_controller(w, 0)
acts = GS.get_all_actors_of_class(w, unreal.Actor)
by = lambda lbl: next(a for a in acts if a.get_actor_label() == lbl)
tag = lambda t: [a for a in acts if a.actor_has_tag(t)]
step = globals().get("STEP", "info")
cb = tag("cb")[0]; ch = by("Chore_controller"); day = by("Day_controller")
if step == "start":
    hud = GS.get_all_actors_of_class(w, unreal.HUD)[0]
    for k, v in (("Mode", 1), ("Fade", 0.0), ("FadeTarget", 0.0)):
        try: hud.set_editor_property(k, v)
        except Exception as e: print("hud", k, e)
    pc.reset_ignore_move_input(); pc.reset_ignore_look_input()
    cb.set_actor_location(unreal.Vector(0, 1, 0), False, False)
if step in ("go", "use", "hold") and globals().get("GO"):
    x, y, z = [float(v) for v in GO.split(",")]
    pawn.set_actor_location(L.to_ue(x, y, z + 92), False, True)
    if globals().get("LOOK"):
        tx, ty, tz = [float(v) for v in LOOK.split(",")]
        pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(pawn.get_actor_location(), L.to_ue(tx, ty, tz)))
if step == "hold":
    a = by(HOLD); pawn.set_editor_property("Held", a); a.set_actor_enable_collision(False)
    pawn.set_editor_property("Carrying", MODE == "carry"); pawn.set_editor_property("Pushing", MODE == "push")
if step == "drop":
    pawn.set_editor_property("Carrying", False); pawn.set_editor_property("Pushing", False)
if step == "use":
    ch.set_editor_property("TestUse", True)
G = ch.get_editor_property
uncut = sum(1 for a in tag("grass") if a.get_actor_scale3d().z > 0.5)
dust = sum(1 for a in tag("ch_dust") if a.get_actor_scale3d().z > 0.5)
p = pawn.get_actor_location()
print(step, "| board", [round(v, 1) for v in cb.get_actor_location().to_tuple()], "| done", "".join("1" if G("D%d" % i) else "0" for i in range(9)),
      "| grass left", uncut, "dust left", dust, "dishes", G("DishN"), "laundry", G("LaunS"), round(G("LaunT"), 1), "water", G("WaterN"), "trash", G("TrashS"), "mail", G("MailS"),
      "| pawn bp", round(p.x + 450), round(1150 - p.y), round(p.z),
      "| day t", round(day.get_editor_property("T")), "fired", list(day.get_editor_property("FiredOrder")), "seen", [i for i, v in enumerate(day.get_editor_property("Seen")) if v])
