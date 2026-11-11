"""Editor-only preview of the loop corridor for screenshots. SHOW = True/False, S = how far the far wall has retreated (cm).
Nothing here is saved: run with SHOW=False afterwards to put the level back."""
import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
show = globals().get("SHOW", True); s = float(globals().get("S", 0.0)) if show else 0.0
face = -540.0 - s
for a in eas.get_all_level_actors():
    tags = [str(t) for t in a.tags]; l = a.get_actor_location()
    if "annex" in tags:
        a.set_actor_hidden_in_game(not show)
    if "annex_hide" in tags or a.get_actor_label() == "Door_upstairs_b":
        a.set_actor_hidden_in_game(show)
    if "ax_capw" in tags: a.set_actor_location(unreal.Vector(l.x, face - 6, l.z), False, False)
    if "ax_cap" in tags: a.set_actor_location(unreal.Vector(l.x, face, l.z), False, False)
    if "ax_l0" in tags: a.set_actor_location(unreal.Vector(l.x, face + 55, l.z), False, False)
    if "ax_div" in tags:
        sc = a.get_actor_scale3d(); a.set_actor_location(unreal.Vector(l.x, -387 - s / 2, l.z), False, False); a.set_actor_scale3d(unreal.Vector(sc.x, (86 + s) / 100.0, sc.z))
    if show and "ax_l1" in tags: a.set_actor_hidden_in_game(face > -890)
    if show and "ax_l2" in tags: a.set_actor_hidden_in_game(face > -1310)
print("corridor preview", show, s)
