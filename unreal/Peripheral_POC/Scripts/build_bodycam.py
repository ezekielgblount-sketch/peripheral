"""Bodycam lens post-process: barrel distortion, slightly soft rim (centre stays sharp), colour fringing at the edges,
noise in the shadows, and the unease look (tape and digital break-up that arrives in bursts). Added to PP_Base. Safe to re-run."""
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


params = [("Barrel", 0.11), ("EdgeBlur", 1.1), ("Fringe", 2.2), ("ShadowNoise", 0.05), ("Soft", 0.45)]
c = E(unreal.MaterialExpressionCustom, -400, 100)
c.set_editor_property("output_type", unreal.CustomMaterialOutputType.CMOT_FLOAT3)
names = ["Scene", "UV", "T", "U", "P", "PF"] + [p[0] for p in params]
ins = []
for n in names:
    ci = unreal.CustomInput(); ci.set_editor_property("input_name", n); ins.append(ci)
c.set_editor_property("inputs", ins)
c.set_editor_property("code", r"""
// U = unease 0..1 (levels 1-10 are U = 0.1 .. 1.0). P = preset for levels 8-10 (0 subtle, 1 medium, 2 heavy).
// PF = pulse held for still pictures (0 = live, 1 = held calm, 2 = held at the peak of a burst). Colour is kept; the picture breaks up like worn tape seen through
// Jack's own eyes. Nothing here blurs: the centre stays sharp at every level and the strong effects come in bursts that pass.
float2 c = UV - 0.5;
float r2 = dot(c, c);
float e1 = smoothstep(0.05, 0.3, U), e2 = smoothstep(0.3, 0.6, U), e3 = smoothstep(0.55, 0.8, U), e4 = smoothstep(0.72, 1.0, U);
float pg = P < 1.0 ? lerp(0.5, 1.0, saturate(P)) : lerp(1.0, 1.7, saturate(P - 1.0));
float hi = e4 * pg;                                        // strength of the top band
float clearMask = smoothstep(0.012, 0.12, r2);             // 0 where you are looking, 1 toward the edges
float ctr = 0.3 + 0.7 * clearMask;
float frame = floor(T * 24.0);
#define H(x) frac(sin((x) * 12.9898) * 43758.5453)
float2 px = View.ViewSizeAndInvSize.zw;
float W3 = dot(float3(1, 1, 1), float3(0.3, 0.59, 0.11));
// ---- pulses: every few seconds there may be one burst of 0.5 to 2 s; short stutters fall between them ----
float slot = lerp(6.0, 3.6, saturate(e3 * 0.5 + hi * 0.4));
float si = floor(T / slot), sf = frac(T / slot);
float on = step(1.0 - saturate(0.25 * e2 + 0.3 * e3 + 0.3 * hi), H(si * 1.37 + 2.0));
float st = 0.08 + 0.45 * H(si * 3.11 + 5.0), ln = (0.5 + 0.9 * H(si * 7.3 + 1.0) + 0.5 * hi) / slot;
float pulse = on * smoothstep(st, st + 0.02, sf) * (1.0 - smoothstep(st + ln, st + ln + 0.05, sf));
float sf2 = frac(T / 1.3);
float blip = step(1.0 - (0.12 * e3 + 0.22 * hi), H(floor(T / 1.3) * 5.7 + 9.0)) * step(0.4, sf2) * step(sf2, 0.49);
pulse = PF > 0.5 ? PF - 1.0 : pulse;
blip = PF > 0.5 ? 0.0 : blip;
float hit = saturate(pulse + blip);
float hF = H(frame), hF2 = H(frame * 1.7 + 4.0);
float2 uv = 0.5 + c * (1.0 + Barrel * r2 * 2.0) / (1.0 + Barrel);
// ---- wobble: the lines of the picture sway slowly, harder in a burst ----
float sway = (0.0006 * e1 + 0.0012 * e2 + 0.0014 * e3 + 0.0012 * hi) * sin(UV.y * 9.0 + T * 1.7) + (0.0005 * e2 + 0.0008 * hi) * sin(UV.y * 43.0 - T * 6.0);
sway += hit * (0.0018 + 0.002 * hi) * sin(UV.y * 5.0 + T * 13.0);
uv.x += sway * ctr;
// ---- tracking band: a strip that rolls through the picture during a burst; the lines inside it slip sideways ----
float bandY = frac(0.15 + T * 0.23 + H(si));
float bandH = 0.035 + 0.05 * hi;
float inBand = smoothstep(bandH, bandH * 0.4, abs(UV.y - bandY)) * pulse * saturate(e2 + hi);
float row = floor(UV.y * View.ViewSizeAndInvSize.y / 3.0);
float rowN = H(row * 3.7 + frame * 1.3);
uv.x += inBand * ((rowN - 0.5) * 0.05 + 0.02) * (0.45 + 0.55 * clearMask);
// ---- line tears: a few groups of lines jump sideways for a frame or two ----
float tearRow = floor(UV.y * 90.0);
float tear = step(1.0 - (0.03 + 0.05 * hi) * hit * saturate(e2 + hi), H(tearRow * 7.7 + frame)) * (H(tearRow + frame * 3.0) - 0.5) * (0.03 + 0.05 * hi);
uv.x += tear * (0.4 + 0.6 * clearMask);
// ---- head-switching noise: the last lines at the very bottom lean and shiver ----
float hs = smoothstep(0.955, 1.0, UV.y) * saturate(e2 + hi);
uv.x += hs * (0.015 + 0.03 * hF) * (UV.y - 0.955) * 22.0;
// ---- frame stutter: the picture hops and drops half its lines for a couple of frames ----
float stut = step(0.86 - 0.1 * hi, hF2) * hit * saturate(e3 + hi);
uv.y += stut * (0.006 + 0.012 * hi) * ctr;
float vres = View.ViewSizeAndInvSize.y / 2.0;
uv.y = lerp(uv.y, (floor(uv.y * vres) + 0.5) / vres, stut * clearMask);
// ---- digital block slips: at the edges only, in a burst only ----
float2 blk = floor(UV * float2(20.0, 12.0));
float hb = H(blk.x * 3.1 + blk.y * 17.7 + floor(T * 6.0) * 1.3);
float blockOn = step(1.0 - (0.015 * e3 + 0.03 * hi) * hit, hb) * clearMask;
uv.x += blockOn * (H(hb * 91.0) - 0.5) * 0.05;
// lens softness at the rim only. It does not grow with unease.
float edge = smoothstep(0.12, 0.42, r2);
float rad = Soft + EdgeBlur * edge;
// ---- chromatic split: radial at the edges, plus red and blue slipping sideways (hard for a moment in a burst) ----
float2 split = c * px * 2.0 * Fringe * edge * (1.0 + 1.0 * e1 + 1.2 * e2 + 1.0 * e3 + 0.8 * hi)
             + float2((1.2 * e2 + 1.8 * e3 + 2.0 * hi + hit * (5.0 + 9.0 * hi)) * px.x, 0) * clearMask;
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
// ---- colour bleed: colour smears to the right of where it belongs while the brightness detail stays sharp ----
float bleed = saturate(0.35 * e2 + 0.35 * e3 + 0.3 * hi + 0.5 * hit);
float3 sm = 0;
for (int j = 1; j <= 4; j++)
    sm += SceneTextureLookup(ViewportUVToSceneTextureUV(clamp(uv - float2(j * (3.0 + 5.0 * bleed) * px.x, 0), 0.003, 0.997), 14), 14, false).rgb;
sm *= 0.25;
float lum = dot(col, float3(0.3, 0.59, 0.11));
float3 chroma = lerp(col - lum, (sm - dot(sm, float3(0.3, 0.59, 0.11))) * (1.0 + 0.5 * bleed), bleed * (0.35 + 0.65 * clearMask));
col = lum + chroma;
// ---- grade: warm and slightly yellowed at 0; colder and a little sickly later, still in colour ----
float3 warm = col * float3(1.05, 1.0, 0.92);
float3 sick = lerp(col, lum.xxx, 0.15 * e3) * lerp(float3(0.95, 1.0, 1.06), float3(0.92, 1.03, 1.08), e3);
sick += float3(0.0, 0.012, 0.03) * e2 * (1.0 - lum) - float3(0.0, 0.0, 0.03) * e3 * lum;
col = lerp(warm, sick, saturate(U * 1.2));
float dr = sin(T * 0.37) + 0.5 * sin(T * 0.83 + 2.0);                                   // the colour cast drifts
col *= 1.0 + (0.02 * e3 + 0.02 * hi + 0.012 * hit * hi) * float3(-dr, dr, -0.6 * dr);
float crush = 0.012 * e2 + 0.02 * e3 + 0.02 * hi;                                        // crushed shadows
col = saturate((col - crush) / (1.0 - crush * 1.6));
col = lerp(col, col * col * (3.0 - 2.0 * col), 0.2 * e3 + 0.12 * hi);
// ---- what the burst adds on top ----
float streak = step(0.72, rowN) * H(floor(UV.x * 40.0 + rowN * 30.0) + frame);
col += inBand * (float3(0.10, 0.11, 0.13) + streak * 0.45) * (0.5 + 0.5 * clearMask);
float barY = frac(T * 0.11 + H(si + 3.0));                                               // rolling bar
float bar = smoothstep(0.16, 0.0, abs(UV.y - barY)) * (0.4 * pulse + 0.15 * e3 * (0.5 + 0.5 * sin(T * 0.5))) * saturate(e2 + hi);
col *= 1.0 - bar * (0.22 + 0.12 * hi);
float dq = H(floor(UV.y * View.ViewSizeAndInvSize.y / 2.0) * 1.3 + frame * 7.0);         // tape dropouts: short white dashes
float dash = step(1.0 - (0.002 * e2 + 0.004 * e3 + 0.01 * hit * (1.0 + hi)), dq) * step(frac(UV.x * 3.0 + dq * 9.0), 0.08 + 0.1 * dq);
col += dash * 0.5 * (0.3 + 0.7 * clearMask);
col += e1 * (1.0 - e2) * step(0.985, hF) * smoothstep(0.004, 0.0, abs(UV.y - frac(hF * 7.0))) * 0.4;     // rare single-frame line, low levels
col += hs * (H(row + frame) - 0.3) * 0.25;
col *= 1.0 - stut * 0.25;
col *= 1.0 - e2 * 0.04 * step(0.5, frac(UV.y * View.ViewSizeAndInvSize.y * 0.5 + frame * 0.5)) * clearMask;   // faint interlace shimmer
// ---- grain: heavier as it gets worse, strongest in the shadows, with colour noise from level 6 ----
float2 q = floor(UV * View.ViewSizeAndInvSize.xy / 2.0);
float n = frac(sin(dot(q + frame * 17.0, float2(12.9898, 78.233))) * 43758.5453);
float n2 = frac(sin(dot(q + frame * 29.0, float2(39.346, 11.135))) * 24634.6345);
float g = ShadowNoise * (1.0 - smoothstep(0.0, 0.4, lum)) * 2.0 + (0.03 * e1 + 0.05 * e2 + 0.05 * e3 + 0.05 * hi + 0.05 * hit) * (0.55 + 0.45 * clearMask);
col += (n - 0.5) * g + (float3(n2, n, 1.0 - n2) - 0.5) * g * 0.5 * saturate(e3 + hi);
return saturate(col);
""")
mel.connect_material_expressions(st, "Color", c, "Scene")
mel.connect_material_expressions(sp, "ViewportUV", c, "UV")
mel.connect_material_expressions(tm, "", c, "T")
mpc = eal.load_asset("/Game/Materials/MPC_World")
have = set(str(n) for n in mpc.get_scalar_parameter_names())
arr = list(mpc.get_editor_property("scalar_parameters"))
for n, v in (("Preset", 1.0), ("Pulse", 0.0)):                 # added without touching the existing entries
    if n not in have:
        sp = unreal.CollectionScalarParameter(); sp.set_editor_property("parameter_name", n); sp.set_editor_property("default_value", v); arr.append(sp)
for sp in arr:
    if str(sp.get_editor_property("parameter_name")) == "Pulse" and sp.get_editor_property("default_value") != 0.0:
        sp.set_editor_property("default_value", 0.0); have = set()
if len(arr) != len(have):
    mpc.set_editor_property("scalar_parameters", arr); eal.save_asset("/Game/Materials/MPC_World")
for n, pin, y in (("Preset", "P", 1100), ("Pulse", "PF", 1200)):
    e = E(unreal.MaterialExpressionCollectionParameter, -900, y)
    e.set_editor_property("collection", mpc); e.set_editor_property("parameter_name", n)
    mel.connect_material_expressions(e, "", c, pin)
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
