"""Editor-side day/night preview (for screenshots). Set POC_NIGHT=1 for night. The game uses BP_World (N key) instead."""
import os, unreal
night = os.environ.get("POC_NIGHT", "0") == "1" or globals().get("NIGHT", False)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in eas.get_all_level_actors():
    if a.actor_has_tag("night_light"):
        a.set_is_temporarily_hidden_in_editor(not night)
    if a.actor_has_tag("day_light"):
        a.set_is_temporarily_hidden_in_editor(night)
        a.root_component.set_visibility(not night, True)     # the editor keeps a hidden sun lighting the sky otherwise
for a in eas.get_all_level_actors():                      # switchable lamps: show the lit look at night (and by day for those that start on)
    tags = [str(t) for t in a.tags]
    lit = night or "default_on" in tags
    if any(t.startswith("sw_") and t.endswith("_off") for t in tags):
        a.set_is_temporarily_hidden_in_editor(lit)
    elif any(t.startswith("sw_") for t in tags) and isinstance(a, unreal.StaticMeshActor):
        a.set_is_temporarily_hidden_in_editor(not lit)
    if "switch" in tags:
        a.static_mesh_component.set_static_mesh(a.get_editor_property("MeshOn" if lit else "MeshOff"))
    if any(t.startswith("an") and t[2:].isdigit() for t in tags):
        a.set_is_temporarily_hidden_in_editor(True)       # loop-sequence anomalies never show in editor stills
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
mpc = unreal.EditorAssetLibrary.load_asset("/Game/Materials/MPC_World")
unreal.MaterialLibrary.set_scalar_parameter_value(world, mpc, "Night", 1.0 if night else 0.0)
for a in eas.get_all_level_actors():                      # force the sky light to re-capture the new sky
    if isinstance(a, unreal.SkyLight):
        c = a.light_component
        c.set_editor_property("real_time_capture", False); c.recapture_sky(); c.set_editor_property("real_time_capture", True)
print("night" if night else "day")
