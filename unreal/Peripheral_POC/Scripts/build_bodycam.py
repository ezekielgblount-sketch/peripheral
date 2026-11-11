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
names = ["Scene", "UV", "T", "U"] + [p[0] for p in params]
ins = []
for n in names:
    ci = unreal.CustomInput(); ci.set_editor_property("input_name", n); ins.append(ci)
c.set_editor_property("inputs", ins)
c.set_editor_property("code", r"""
// U = unease 0..1 (levels 1-10 are U = 0.1 .. 1.0). Colour is kept; the picture breaks up like damaged tape and bad digital
// video seen through Jack's own eyes. The centre always stays clear so the peripheral mechanic can be trusted.
float2 c = UV - 0.5;
float r2 = dot(c, c);
float e1 = smoothstep(0.05, 0.3, U), e2 = smoothstep(0.3, 0.6, U), e3 = smoothstep(0.55, 0.85, U), e4 = smoothstep(0.8, 1.0, U);
float clearMask = smoothstep(0.012, 0.11 - 0.04 * e3, r2);
float frame = floor(T * 24.0);
#define H(x) frac(sin((x) * 12.9898) * 43758.5453)
float hF = H(frame), hS = H(floor(T * 3.0) + 7.0), hQ = H(floor(T * 8.0) + 3.0);
float2 uv = 0.5 + c * (1.0 + Barrel * r2 * 2.0) / (1.0 + Barrel);
// --- digital block glitches: macroblocks that slip sideways for a few frames, only in the periphery ---
float2 blk = floor(UV * float2(18.0, 11.0));
float hb = H(blk.x * 3.1 + blk.y * 17.7 + floor(T * 5.0) * 1.3);
float blockOn = step(1.0 - (0.02 * e2 + 0.07 * e3 + 0.12 * e4), hb) * clearMask;
uv.x += blockOn * (H(hb * 91.0) - 0.5) * (0.03 + 0.07 * e4);
// --- pixelation patches ---
float pixOn = step(1.0 - (0.03 * e3 + 0.08 * e4), H(blk.y * 5.3 + blk.x * 1.9 + floor(T * 2.0))) * clearMask;
float2 grid = View.ViewSizeAndInvSize.xy / lerp(1.0, 14.0, pixOn);
uv = lerp(uv, (floor(uv * grid) + 0.5) / grid, pixOn);
// --- tape: slow wobble, a tracking band that rolls through, horizontal tears ---
float wob = (e1 * 0.0008 + e2 * 0.0016) * sin(UV.y * 40.0 + T * 2.7) + e3 * 0.0022 * sin(UV.y * 7.0 + T * 9.0);
float rollY = frac(T * 0.08 + 0.37 * hS);
float inRoll = smoothstep(0.045, 0.0, abs(UV.y - rollY)) * step(0.5 - 0.3 * e3, hS) * e2;
float row = floor(UV.y * 60.0);
float tear = step(1.0 - (0.015 * e2 + 0.05 * e3 + 0.1 * e4), H(row * 7.7 + frame)) * (H(row + frame * 3.0) - 0.5) * (0.02 + 0.05 * e4);
uv.x += (wob + inRoll * 0.025 + tear) * clearMask;
uv.y += e4 * step(0.93, hQ) * 0.04 * clearMask;                                       // a skipped frame
float2 px = View.ViewSizeAndInvSize.zw;
float edge = smoothstep(0.10 - 0.05 * e3, 0.42 - 0.2 * e3, r2);
float rad = Soft + EdgeBlur * edge * (1.0 + 2.0 * e3) + e2 * 0.6 * clearMask;
// --- chromatic split: radial at the edges, plus whole-channel slips during glitch bursts ---
float burst = step(1.0 - (0.04 * e1 + 0.1 * e2 + 0.2 * e3 + 0.3 * e4), hQ);
float2 split = c * px * 2.0 * (Fringe * edge * (1.0 + 3.0 * e1 + 7.0 * e2 + 10.0 * e3))
             + float2((e2 * 3.0 + e3 * 6.0 + e4 * 8.0 + burst * 14.0) * px.x, 0) * clearMask;
float3 col = 0;
const float2 taps[9] = { float2(0,0), float2(1,0), float2(-1,0), float2(0,1), float2(0,-1), float2(.7,.7), float2(-.7,.7), float2(.7,-.7), float2(-.7,-.7) };
for (int i = 0; i < 9; i++)
{
    float2 o = taps[i] * rad * px;
    col.r += SceneTextureLookup(ViewportUVToSceneTextureUV(clamp(uv + o + split, 0.003, 0.997), 14), 14, false).r;
    col.g += SceneTextureLookup(ViewportUVToSceneTextureUV(clamp(uv + o, 0.003, 0.997), 14), 14, false).g;
    col.b += SceneTextureLookup(ViewportUVToSceneTextureUV(clamp(uv + o - split, 0.003, 0.997), 14), 14, false).b;
}
col /= 9.0;
float lum = dot(col, float3(0.3, 0.59, 0.11));
// --- grade: warm and slightly yellowed at 0; it turns colder and a little sickly, but stays in colour ---
float3 warm = col * float3(1.05, 1.0, 0.92);
float3 sick = lerp(col, lum.xxx, 0.22 * e3 + 0.12 * e4) * lerp(float3(0.95, 1.0, 1.06), float3(0.9, 1.03, 1.1), e3);
sick += float3(0.0, 0.012, 0.03) * e2 * (1.0 - lum) - float3(0.0, 0.0, 0.03) * e3 * lum;   // cyan shadows, yellowed highlights
col = lerp(warm, sick, saturate(U * 1.2));
col = lerp(col, (col - 0.5) * 1.12 + 0.5, e3 * 0.7);                                      // harder contrast near the bottom
// colour channels trade places inside glitching blocks; brief posterised patches
col = lerp(col, col.gbr, blockOn * step(0.5, H(hb * 13.0)) * e3);
col = lerp(col, floor(col * 5.0) / 5.0, pixOn * 0.8);
col += inRoll * float3(0.10, 0.12, 0.16) * clearMask;
col += e1 * (1.0 - e2) * step(0.985, hF) * smoothstep(0.004, 0.0, abs(UV.y - frac(hF * 7.0))) * 0.4;     // rare single-frame line
col *= 1.0 - e3 * step(0.93, hS) * step(frac(T * 3.0), 0.1) * 0.7 * clearMask;                // momentary dropout
// faint interlace shimmer only (no TV-style scanline overlay)
col *= 1.0 - e2 * 0.05 * step(0.5, frac(UV.y * View.ViewSizeAndInvSize.y * 0.5 + frame * 0.5)) * clearMask;
// noise
float2 q = floor(UV * View.ViewSizeAndInvSize.xy / 2.0);
float n = frac(sin(dot(q + frame * 17.0, float2(12.9898, 78.233))) * 43758.5453);
col += (n - 0.5) * (ShadowNoise * (1.0 - smoothstep(0.0, 0.4, lum)) * 2.0 + (0.025 * e1 + 0.05 * e2 + 0.07 * e3 + 0.06 * e4) * (0.4 + 0.6 * clearMask));
return saturate(col);
""")
mel.connect_material_expressions(st, "Color", c, "Scene")
mel.connect_material_expressions(sp, "ViewportUV", c, "UV")
mel.connect_material_expressions(tm, "", c, "T")
un = E(unreal.MaterialExpressionCollectionParameter, -900, 480)
un.set_editor_property("collection", eal.load_asset("/Game/Materials/MPC_World")); un.set_editor_property("parameter_name", "Unease")
mel.connect_material_expressions(un, "", c, "U")
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
