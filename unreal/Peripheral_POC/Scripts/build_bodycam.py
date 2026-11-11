"""Bodycam lens post-process: barrel distortion, soft edges (centre stays sharp), colour fringing at the edges only,
noise in the shadows, mild compression softness. Adds it to the PP_Base volume. Safe to re-run."""
import unreal
mel, eal = unreal.MaterialEditingLibrary, unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
path = "/Game/Materials/M_Bodycam"
m = eal.load_asset(path) or at.create_asset("M_Bodycam", "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
mel.delete_all_material_expressions(m)
m.set_editor_property("material_domain", unreal.MaterialDomain.MD_POST_PROCESS)
locs = [v for v in unreal.BlendableLocation]
after = [v for v in locs if "AFTER_TONEMAPPING" in str(v).upper()]
m.set_editor_property("blendable_location", after[0] if after else locs[0])
E = lambda cls, x, y: mel.create_material_expression(m, cls, x, y)
st = E(unreal.MaterialExpressionSceneTexture, -900, 0)
st.set_editor_property("scene_texture_id", unreal.SceneTextureId.PPI_POST_PROCESS_INPUT0)
sp = E(unreal.MaterialExpressionScreenPosition, -900, 250)
tm = E(unreal.MaterialExpressionTime, -900, 400)


def scalar(name, v, y):
    e = E(unreal.MaterialExpressionScalarParameter, -900, y)
    e.set_editor_property("parameter_name", name); e.set_editor_property("default_value", v)
    return e


params = [("Barrel", 0.11), ("EdgeBlur", 2.6), ("Fringe", 2.2), ("ShadowNoise", 0.05), ("Soft", 0.45)]
c = E(unreal.MaterialExpressionCustom, -400, 100)
c.set_editor_property("output_type", unreal.CustomMaterialOutputType.CMOT_FLOAT3)
names = ["Scene", "UV", "T"] + [p[0] for p in params]
ins = []
for n in names:
    ci = unreal.CustomInput(); ci.set_editor_property("input_name", n); ins.append(ci)
c.set_editor_property("inputs", ins)
c.set_editor_property("code", r"""
float2 c = UV - 0.5;
float r2 = dot(c, c);
float2 uv = 0.5 + c * (1.0 + Barrel * r2 * 2.0) / (1.0 + Barrel);            // barrel distortion, corners stay inside the image
float2 px = View.ViewSizeAndInvSize.zw;
float edge = smoothstep(0.10, 0.42, r2);                                     // 0 in the centre, 1 toward the corners
float rad = Soft + EdgeBlur * edge;
float3 col = 0;
const float2 taps[9] = { float2(0,0), float2(1,0), float2(-1,0), float2(0,1), float2(0,-1), float2(.7,.7), float2(-.7,.7), float2(.7,-.7), float2(-.7,-.7) };
for (int i = 0; i < 9; i++)
{
    float2 o = taps[i] * rad * px;
    float2 f = c * Fringe * edge * px * 2.0;                                 // red and blue pulled apart, edges only
    col.r += SceneTextureLookup(ViewportUVToSceneTextureUV(saturate(uv + o + f), 14), 14, false).r;
    col.g += SceneTextureLookup(ViewportUVToSceneTextureUV(saturate(uv + o), 14), 14, false).g;
    col.b += SceneTextureLookup(ViewportUVToSceneTextureUV(saturate(uv + o - f), 14), 14, false).b;
}
col /= 9.0;
float lum = dot(col, float3(0.3, 0.59, 0.11));
float2 q = floor(UV * View.ViewSizeAndInvSize.xy / 2.0);                      // 2-pixel sensor noise
float n = frac(sin(dot(q + floor(T * 24.0) * 17.0, float2(12.9898, 78.233))) * 43758.5453);
col += (n - 0.5) * ShadowNoise * (1.0 - smoothstep(0.0, 0.4, lum)) * 2.0;
return col;
""")
mel.connect_material_expressions(st, "Color", c, "Scene")
mel.connect_material_expressions(sp, "ViewportUV", c, "UV")
mel.connect_material_expressions(tm, "", c, "T")
for i, (n, v) in enumerate(params):
    mel.connect_material_expressions(scalar(n, v, 550 + i * 100), "", c, n)
mel.connect_material_property(c, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
mel.recompile_material(m); eal.save_asset(path)
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label() == "PP_Base":
        s = a.settings
        wb = unreal.WeightedBlendable(); wb.set_editor_property("weight", 1.0); wb.set_editor_property("object", m)
        wbs = unreal.WeightedBlendables(); wbs.set_editor_property("array", [wb])
        s.set_editor_property("weighted_blendables", wbs)
        for k, v in (("override_scene_fringe_intensity", True), ("scene_fringe_intensity", 0.0),
                     ("override_color_saturation", True), ("color_saturation", unreal.Vector4(0.9, 0.9, 0.9, 1.0)),
                     ("override_film_grain_intensity", True), ("film_grain_intensity", 0.35),
                     ("override_motion_blur_amount", True), ("motion_blur_amount", 0.3),
                     ("override_vignette_intensity", True), ("vignette_intensity", 0.38)):
            s.set_editor_property(k, v)
        a.set_editor_property("settings", s)
        print("bodycam post added; location", m.get_editor_property("blendable_location"))
