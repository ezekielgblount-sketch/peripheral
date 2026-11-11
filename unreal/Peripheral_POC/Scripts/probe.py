L_ = unreal.EditorActorSubsystem
for a in unreal.get_editor_subsystem(L_).get_all_level_actors():
    if a.actor_has_tag("probe"): unreal.get_editor_subsystem(L_).destroy_actor(a)
unreal.EditorAssetLibrary.delete_asset("/Game/Meshes/SM_probe_quad")
def props(cls):
    o = cls(); return [n for n in dir(o) if not n.startswith("_") and n not in dir(unreal.StructBase)]
print(unreal.GeometryScript_MeshDeformers.apply_iterative_smoothing_to_mesh.__doc__.split("Args")[0])
print(props(unreal.GeometryScriptIterativeMeshSmoothingOptions))
print(unreal.GeometryScript_Primitives.append_torus.__doc__.split("Args")[0], props(unreal.GeometryScriptRevolveOptions))
print(unreal.GeometryScript_Primitives.append_capsule.__doc__.split("Args")[0])
print(unreal.GeometryScript_MeshSubdivide.apply_pn_tessellation.__doc__.split("Args")[0] if hasattr(unreal.GeometryScript_MeshSubdivide,"apply_pn_tessellation") else dir(unreal.GeometryScript_MeshSubdivide)[-8:])
