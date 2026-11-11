"""Places the actor that casts Jack's shadow (BP_Shadow). Its mesh is left out of the picture itself and only casts a shadow.
Safe to re-run."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, props_furniture as PF, props_shadow
importlib.reload(props_shadow)
L.clear("shadow")
for n in ("shadow_body", "shadow_body_alt"):
    PF.get(n, rebuild=True)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
a = eas.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Shadow"), unreal.Vector(0, 0, -600))
a.set_actor_label("Jack_shadow"); a.set_folder_path("Interactive"); a.tags = ["shadow"]
c = a.static_mesh_component
c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(PF.get("shadow_body"))
c.set_collision_profile_name("NoCollision"); c.set_cast_shadow(True)
c.set_editor_property("render_in_main_pass", False); c.set_editor_property("render_in_depth_pass", False)
print("shadow caster placed")
