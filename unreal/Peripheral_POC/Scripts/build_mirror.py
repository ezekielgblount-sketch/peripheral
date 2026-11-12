"""Makes the wall mirrors show Jack. For every mirror_wall prop in the level: a small render target, a glass plane in front
of the prop's grey mirror face that draws it, and a BP_Mirror camera that films the room from behind the wall.
Run after dress_rooms.py and build_shadow.py. Safe to re-run."""
import sys, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
eal, mel = unreal.EditorAssetLibrary, unreal.MaterialEditingLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
DIR = "/Game/Jack"
W, H = 104.0, 80.0                                   # the glass of the mirror_wall prop
L.clear("mirror_view")


def target(i):
    path = "%s/RT_Mirror_%d" % (DIR, i)
    rt = eal.load_asset(path) or at.create_asset("RT_Mirror_%d" % i, DIR, unreal.TextureRenderTarget2D, unreal.TextureRenderTargetFactoryNew())
    rt.set_editor_property("size_x", 416); rt.set_editor_property("size_y", 320)                 # small on purpose: his face stays soft
    rt.set_editor_property("render_target_format", unreal.TextureRenderTargetFormat.RTF_RGBA16F)
    eal.save_asset(path)
    return rt


def material():
    m = eal.load_asset(DIR + "/M_MirrorView") or at.create_asset("M_MirrorView", DIR, unreal.Material, unreal.MaterialFactoryNew())
    mel.delete_all_material_expressions(m)
    E = lambda cls, x, y: mel.create_material_expression(m, cls, x, y)
    C = mel.connect_material_expressions
    uv = E(unreal.MaterialExpressionTextureCoordinate, -1300, 0)
    half = E(unreal.MaterialExpressionConstant2Vector, -1300, 150); half.set_editor_property("r", 0.5); half.set_editor_property("g", 0.5)
    s1 = E(unreal.MaterialExpressionSubtract, -1100, 0); C(uv, "", s1, "A"); C(half, "", s1, "B")
    fu = E(unreal.MaterialExpressionScalarParameter, -1300, 300); fu.set_editor_property("parameter_name", "ScaleU"); fu.set_editor_property("default_value", SCALE_U)
    fv = E(unreal.MaterialExpressionScalarParameter, -1300, 400); fv.set_editor_property("parameter_name", "ScaleV"); fv.set_editor_property("default_value", SCALE_V)
    ap = E(unreal.MaterialExpressionAppendVector, -1100, 320); C(fu, "", ap, "A"); C(fv, "", ap, "B")
    mu = E(unreal.MaterialExpressionMultiply, -900, 100); C(s1, "", mu, "A"); C(ap, "", mu, "B")
    ad = E(unreal.MaterialExpressionAdd, -700, 100); C(mu, "", ad, "A"); C(half, "", ad, "B")
    t = E(unreal.MaterialExpressionTextureSampleParameter2D, -500, 100); t.set_editor_property("parameter_name", "View")
    t.set_editor_property("texture", target(0)); t.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
    C(ad, "", t, "UVs")
    tint = E(unreal.MaterialExpressionConstant3Vector, -500, 400); tint.set_editor_property("constant", unreal.LinearColor(0.50, 0.45, 0.37, 1))   # old glass, dimmed and warmed to sit in the room
    out = E(unreal.MaterialExpressionMultiply, -250, 200); C(t, "RGB", out, "A"); C(tint, "", out, "B")
    mel.connect_material_property(out, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    mel.recompile_material(m); eal.save_asset(DIR + "/M_MirrorView")
    return m


# the camera frames 1.15x the glass; a mirror picture is flipped left to right
SCALE_U, SCALE_V = -0.87, 0.87
m = material()
cls = eal.load_blueprint_class("/Game/Blueprints/BP_Mirror")
plane = unreal.load_asset("/Engine/BasicShapes/Plane")
props = [a for a in eas.get_all_level_actors() if isinstance(a, unreal.StaticMeshActor) and a.static_mesh_component.static_mesh
         and a.static_mesh_component.static_mesh.get_name() == "SM_mirror_wall"]
for i, p in enumerate(props):
    tr = p.get_actor_transform()
    n = tr.rotation.rotator().get_forward_vector()                       # the glass faces the prop's +X
    c = unreal.MathLibrary.transform_location(tr, unreal.Vector(3.6, 0, 0))
    rt = target(i)
    mi_path = "%s/MI_MirrorView_%d" % (DIR, i)
    mi = eal.load_asset(mi_path) or at.create_asset("MI_MirrorView_%d" % i, DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi, m); mel.set_material_instance_texture_parameter_value(mi, "View", rt); eal.save_asset(mi_path)
    g = eas.spawn_actor_from_object(plane, c, unreal.MathLibrary.make_rot_from_zy(n, unreal.Vector(0, 0, -1)))
    g.set_actor_label("Mirror_glass_%d" % i); g.set_folder_path("Interactive"); g.tags = ["mirror_view"]
    g.set_actor_scale3d(unreal.Vector(W / 100.0, H / 100.0, 1.0))
    gc = g.static_mesh_component; gc.set_material(0, mi); gc.set_collision_profile_name("NoCollision"); gc.set_cast_shadow(False)
    gc.set_mobility(unreal.ComponentMobility.MOVABLE)
    a = eas.spawn_actor_from_class(cls, unreal.Vector(c.x - n.x * 200, c.y - n.y * 200, c.z))
    a.set_actor_label("Mirror_camera_%d" % i); a.set_folder_path("Interactive"); a.tags = ["mirror_view"]
    a.set_editor_property("C", c); a.set_editor_property("N", n)
    cc = a.capture_component2d
    cc.set_editor_property("texture_target", rt); cc.set_editor_property("capture_source", unreal.SceneCaptureSource.SCS_SCENE_COLOR_HDR)
    cc.set_editor_property("capture_every_frame", False); cc.set_editor_property("capture_on_movement", False)
    cc.set_editor_property("always_persist_rendering_state", True); cc.set_editor_property("override_custom_near_clipping_plane", True)
    print("mirror", i, p.get_actor_label(), [round(v) for v in c.to_tuple()], [round(v, 2) for v in n.to_tuple()])
print("mirrors:", len(props))
