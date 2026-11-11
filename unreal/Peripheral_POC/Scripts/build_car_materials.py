"""Car paint with wear that follows the body (sun-faded top panels, road dirt low down and behind the wheels, light rust
on the wheel-arch lips and sills, a scuff at the dent), plus the few extra surface keys the car uses. Safe to re-run."""
import os, json, unreal
MAT_DIR, TEX_DIR = "/Game/Materials", "/Game/Textures"
mel, eal = unreal.MaterialEditingLibrary, unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
root = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
manifest = json.load(open(os.path.join(root, "SourceArt", "Textures", "manifest.json")))
KEYS = {   # also listed here so the car does not depend on a full material rebuild
    "plastic_amber": ("plastic", (0.85, 0.36, 0.04), 0.5, 0.2), "lens_red": ("plastic", (0.5, 0.03, 0.03), 0.4, 0.2),
    "wheel_steel": ("paint", (0.5, 0.5, 0.49), 0.9, 0.65), "bumper": ("plastic", (0.15, 0.155, 0.16), 1.6, 0.45),
    "fabric_grey": ("fabric", (0.3, 0.31, 0.34), 1.0, 0.4), "headliner": ("fabric", (0.7, 0.69, 0.65), 1.0, 0.3),
    "dash": ("plastic", (0.09, 0.095, 0.105), 1.4, 0.3),
}
master = eal.load_asset(MAT_DIR + "/M_Surface")
for key, (ts, tint, rough, dirt) in KEYS.items():
    for prefix, local in (("MI_", False), ("MIL_", True)):
        p = "%s/%s%s" % (MAT_DIR, prefix, key)
        mi = eal.load_asset(p) or at.create_asset(prefix + key, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        mi.set_editor_property("parent", master)
        for n, sfx in (("BaseColorTex", "BC"), ("NormalTex", "N"), ("RoughTex", "R")):
            mel.set_material_instance_texture_parameter_value(mi, n, eal.load_asset("%s/T_%s_%s" % (TEX_DIR, ts, sfx)))
        for n, v in (("TileSize", float(manifest[ts]["size_cm"])), ("RoughScale", rough), ("GrungeSize", 300.0), ("DirtAmount", dirt),
                     ("Metallic", float(manifest[ts].get("metallic", 0.0)))):
            mel.set_material_instance_scalar_parameter_value(mi, n, v)
        mel.set_material_instance_vector_parameter_value(mi, "Tint", unreal.LinearColor(tint[0], tint[1], tint[2], 1))
        mel.set_material_instance_static_switch_parameter_value(mi, "LocalSpace", local)
        mel.update_material_instance(mi); eal.save_asset(p)

path = MAT_DIR + "/M_CarPaint"
m = eal.load_asset(path) or at.create_asset("M_CarPaint", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
mel.delete_all_material_expressions(m)
E = lambda cls, x, y: mel.create_material_expression(m, cls, x, y)


def to_local(src, cls, y):
    t = E(cls, -700, y)
    for prop, want in (("transform_source_type", "WORLD"), ("transform_type", "LOCAL")):
        cur = t.get_editor_property(prop)
        t.set_editor_property(prop, next(v for v in type(cur) if str(v).split(".")[-1].split(":")[0].endswith(want)))
    mel.connect_material_expressions(src, "", t, "")
    return t


lp = to_local(E(unreal.MaterialExpressionWorldPosition, -950, 0), unreal.MaterialExpressionTransformPosition, 0)
nl = to_local(E(unreal.MaterialExpressionVertexNormalWS, -950, 200), unreal.MaterialExpressionTransform, 200)
tint = E(unreal.MaterialExpressionVectorParameter, -700, 400)
tint.set_editor_property("parameter_name", "Tint"); tint.set_editor_property("default_value", unreal.LinearColor(0.115, 0.215, 0.19, 1))
c = E(unreal.MaterialExpressionCustom, -400, 100)
c.set_editor_property("output_type", unreal.CustomMaterialOutputType.CMOT_FLOAT4)
ins = []
for n in ("LP", "N", "Tint"):
    ci = unreal.CustomInput(); ci.set_editor_property("input_name", n); ins.append(ci)
c.set_editor_property("inputs", ins)
c.set_editor_property("code", r"""
struct NF {
  float h(float3 p) { p = frac(p * 0.3183099 + 0.1); p *= 17.0; return frac(p.x * p.y * p.z * (p.x + p.y + p.z)); }
  float n(float3 x) { float3 i = floor(x), f = frac(x); f = f * f * (3.0 - 2.0 * f);
    return lerp(lerp(lerp(h(i), h(i + float3(1,0,0)), f.x), lerp(h(i + float3(0,1,0)), h(i + float3(1,1,0)), f.x), f.y),
                lerp(lerp(h(i + float3(0,0,1)), h(i + float3(1,0,1)), f.x), lerp(h(i + float3(0,1,1)), h(i + float3(1,1,1)), f.x), f.y), f.z); }
  float fbm(float3 x) { return 0.5 * n(x) + 0.25 * n(x * 2.03 + 7.1) + 0.125 * n(x * 4.01 + 3.3) + 0.125 * n(x * 8.1 + 1.7); }
};
NF nf;
const float AXR = -115.0, AXF = 128.0, AXZ = 29.0;
float n1 = nf.fbm(LP * 0.035), n2 = nf.fbm(LP * 0.16 + 31.0), n3 = nf.n(LP * 1.3);
float3 base = Tint.rgb;
float lum = dot(base, float3(0.3, 0.59, 0.11));
float3 chalk = lerp(base, lum.xxx, 0.5) * 1.35 + 0.03;
// sun fade: the roof, bonnet and boot have gone flat and pale; sides keep more colour and a little shine
float up = saturate(N.z * 1.5 - 0.35);
float fade = up * (0.4 + 0.6 * smoothstep(0.3, 0.7, n1));
float3 col = lerp(base, chalk, fade * 0.8);
float rough = lerp(0.36, 0.74, fade);
float peel = up * smoothstep(0.585, 0.615, n1 * 0.75 + n2 * 0.25);            // patches where the clear coat has gone
col = lerp(col, chalk * 1.15 + 0.03, peel * 0.6); rough = lerp(rough, 0.92, peel);
// road dirt: a film low on the body, heavier behind each wheel and across the tail
float side = 1.0 - saturate(N.z * 2.0);
float dR = LP.x - AXR, dF = LP.x - AXF;
float low = smoothstep(60.0, 24.0, LP.z + 18.0 * (n1 - 0.5));
float splash = max(smoothstep(-33.0, -40.0, dR) * smoothstep(-105.0, -45.0, dR), smoothstep(-33.0, -40.0, dF) * smoothstep(-105.0, -45.0, dF)) * smoothstep(72.0, 32.0, LP.z);
float tail = smoothstep(0.5, 0.95, -N.x) * smoothstep(92.0, 50.0, LP.z) * 0.45;
float dirt = saturate(low * 0.7 + splash * 0.55 + tail) * (0.5 + 0.5 * n2) * side;
col = lerp(col, float3(0.19, 0.155, 0.115), dirt * 0.78); rough = lerp(rough, 0.95, dirt);
// light rust: bubbling on the wheel-arch lips (worst low on the rear arches) and a few spots along the sills
float2 pr = float2(dR, LP.z - AXZ), pf = float2(dF, LP.z - AXZ);
float lr = length(pr), lf = length(pf);
float lipR = smoothstep(42.0, 34.0, lr) * step(32.5, lr), lipF = smoothstep(39.5, 34.0, lf) * step(32.5, lf);
float bias = n2 * 0.65 + n3 * 0.35;
float rust = lipR * smoothstep(0.50 - 0.14 * smoothstep(12.0, -20.0, pr.y), 0.60, bias) + lipF * smoothstep(0.56, 0.64, bias) * 0.8;
rust += smoothstep(30.5, 24.0, LP.z) * smoothstep(0.60, 0.66, bias) * 0.8;
rust = saturate(rust) * step(0.4, abs(N.y) + abs(N.x));
float halo = saturate(lipR * smoothstep(0.42, 0.6, bias) * 0.5 - rust);
col = lerp(col, col * float3(1.1, 0.8, 0.6), halo);
col = lerp(col, lerp(float3(0.27, 0.105, 0.04), float3(0.09, 0.04, 0.02), n3), rust); rough = lerp(rough, 0.93, rust);
// the dent: scraped down to primer in thin horizontal streaks
float sc = smoothstep(13.0, 4.0, length(float2(LP.x + 178.0, (LP.z - 60.0) * 1.5))) * step(LP.y, -60.0);
float streak = smoothstep(0.52, 0.62, nf.n(float3(LP.x * 0.18, LP.z * 2.6, 3.0)));
col = lerp(col, float3(0.42, 0.42, 0.40), sc * streak * 0.7); rough = lerp(rough, 0.8, sc * streak);
// stone chips on the nose
float chips = smoothstep(0.6, 0.9, N.x) * smoothstep(0.80, 0.84, nf.n(LP * 2.1 + 9.0));
col = lerp(col, float3(0.3, 0.3, 0.29), chips * 0.6);
return float4(saturate(col), rough);
""")
mel.connect_material_expressions(lp, "", c, "LP"); mel.connect_material_expressions(nl, "", c, "N"); mel.connect_material_expressions(tint, "", c, "Tint")
rgb = E(unreal.MaterialExpressionComponentMask, -150, 50)
for ch, v in (("r", True), ("g", True), ("b", True), ("a", False)): rgb.set_editor_property(ch, v)
a = E(unreal.MaterialExpressionComponentMask, -150, 250)
for ch, v in (("r", False), ("g", False), ("b", False), ("a", True)): a.set_editor_property(ch, v)
mel.connect_material_expressions(c, "", rgb, ""); mel.connect_material_expressions(c, "", a, "")
mel.connect_material_property(rgb, "", unreal.MaterialProperty.MP_BASE_COLOR)
mel.connect_material_property(a, "", unreal.MaterialProperty.MP_ROUGHNESS)
sp = E(unreal.MaterialExpressionConstant, -150, 400); sp.set_editor_property("r", 0.45)
mel.connect_material_property(sp, "", unreal.MaterialProperty.MP_SPECULAR)
mel.recompile_material(m); eal.save_asset(path)
print("car materials built")
