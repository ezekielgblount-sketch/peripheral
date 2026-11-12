"""Places Jack's body (BP_Body, mesh from build_jack.py): one actor the player sees when he looks down (no head, no shadow)
and one that is never drawn and only casts his shadow. Both follow the player and play the walk, idle and crouch
animations. Safe to re-run."""
import sys, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
L.clear("shadow"); L.clear("jack_preview")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
cls = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Body")
sk = unreal.load_asset("/Game/Jack/SK_Jack")
idle = unreal.load_asset("/MoverExamples/Characters/Mannequins/Animations/Manny/MM_Idle")
for kind, label in ((0, "Jack_body"), (1, "Jack_shadow"), (2, "Jack_reflection")):
    a = eas.spawn_actor_from_class(cls, unreal.Vector(0, 0, -600))
    a.set_actor_label(label); a.set_folder_path("Interactive"); a.tags = ["shadow", "jack_fp"] if kind == 0 else ["shadow"]
    a.set_actor_scale3d(unreal.Vector(0.986, 0.986, 0.986))                 # 180.5 cm mesh -> 178 cm
    a.set_editor_property("Kind", kind); a.set_editor_property("State", -1)
    a.set_editor_property("Back", 15.0)                                      # the body stands a little behind the camera
    a.set_editor_property("CrouchH", 58.0)
    c = a.skeletal_mesh_component
    c.set_skinned_asset_and_update(sk); c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_collision_profile_name("NoCollision")
    c.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    c.set_editor_property("visibility_based_anim_tick_option", unreal.VisibilityBasedAnimTickOption.ALWAYS_TICK_POSE_AND_REFRESH_BONES)
    c.set_cast_shadow(kind == 1)
    if kind == 1:
        c.set_editor_property("render_in_main_pass", False); c.set_editor_property("render_in_depth_pass", False)
    if kind == 2:
        c.set_editor_property("owner_no_see", True)                          # BP_Body makes the player its owner
    c.set_editor_property("bounds_scale", 3.0); c.set_editor_property("forced_lod_model", 1)
acls = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Arms")
for side, n in ((1.0, "r"), (-1.0, "l")):                                     # first-person forearms (build_jack.arms)
    a = eas.spawn_actor_from_class(acls, unreal.Vector(0, 0, -600))
    a.set_actor_label("Jack_arm_" + n); a.set_folder_path("Interactive"); a.tags = ["shadow", "jack_fp"]
    a.set_actor_scale3d(unreal.Vector(0.986, 0.986, 0.986)); a.set_editor_property("Side", side)
    c = a.static_mesh_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(unreal.load_asset("/Game/Meshes/SM_jack_arm_" + n))
    c.set_collision_profile_name("NoCollision"); c.set_cast_shadow(False)
print("Jack's body, shadow and forearms placed")
