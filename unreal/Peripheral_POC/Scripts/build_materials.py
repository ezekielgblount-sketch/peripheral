"""Builds the PBR master material M_Surface (world-aligned, so wall and floor boxes need no UV work) and one
instance per surface key. Safe to re-run. Texture sets come from Scripts/tex/gen_surfaces.py."""
import os, json, unreal

MAT_DIR, TEX_DIR = "/Game/Materials", "/Game/Textures"
mel, eal = unreal.MaterialEditingLibrary, unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
root = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
manifest = json.load(open(os.path.join(root, "SourceArt", "Textures", "manifest.json")))
FN = "/Engine/Functions/Engine_MaterialFunctions01/Texturing/"

# key: (texture set, tint rgb, roughness scale, dirt amount)
KEYS = {
    "brick": ("brick", (1, 1, 1), 1.0, 0.25), "siding": ("siding", (1, 1, 1), 1.0, 0.3),
    # walls: every room has its own finish (living room damask, entry hall off-white paint, upstairs hall striped paper,
    # kitchen small-print paper, bathroom aqua paint, Jack's room dusty blue paint)
    "liv": ("damask", (1, 1, 1), 1.0, 0.15), "hall": ("paint", (0.86, 0.80, 0.66), 0.95, 0.3),
    "hall2": ("stripe", (1, 1, 1), 1.0, 0.2), "kit": ("ditsy", (1, 1, 1), 1.0, 0.22),
    "bath": ("paint", (0.72, 0.84, 0.80), 0.8, 0.25), "bed": ("paint", (0.50, 0.64, 0.80), 1.0, 0.25),
    "blk": ("paint", (0.42, 0.42, 0.42), 1.0, 0.0), "bsmt": ("concrete", (0.9, 0.9, 0.9), 1.0, 0.4),
    "ceiling": ("popcorn", (1, 1, 1), 1.0, 0.2), "trim": ("paint", (0.90, 0.87, 0.78), 0.75, 0.3),
    "rail": ("wood_plain", (0.6, 0.38, 0.3), 0.9, 0.2),
    "f_liv": ("oak_floor", (1.25, 0.92, 0.55), 0.9, 0.3), "f_hall": ("oak_floor", (1.25, 0.92, 0.55), 0.9, 0.3),
    "f_entry": ("linoleum", (0.9, 0.9, 0.95), 1.0, 0.45), "f_kit": ("tile_bath", (1.0, 0.97, 0.9), 1.4, 0.3),
    "f_stair": ("carpet_worn", (1.32, 1.18, 1.02), 1.0, 0.6), "f_hall2": ("carpet_worn", (1.32, 1.18, 1.02), 1.0, 0.55),
    "f_bath": ("tile_bath", (1, 1, 1), 1.0, 0.3), "f_bed": ("carpet_worn", (1.32, 1.18, 1.02), 1.0, 0.55),
    "f_blk": ("concrete", (0.6, 0.6, 0.6), 1.0, 0.0), "f_bsmt": ("concrete", (0.8, 0.8, 0.8), 1.0, 0.5),
    "roof": ("shingles", (1, 1, 1), 1.0, 0.3), "lawn": ("grass", (1, 1, 1), 1.0, 0.3),
    "concrete": ("concrete", (1, 1, 1), 1.0, 0.4), "asphalt": ("asphalt", (1, 1, 1), 1.0, 0.3),
    "garage_door": ("paint", (0.85, 0.83, 0.77), 0.7, 0.4), "bark": ("bark", (1, 1, 1), 1.0, 0.3),
    "leaf": ("foliage", (1, 1, 1), 1.0, 0.35), "nb_a": ("siding", (0.85, 0.74, 0.55), 1.0, 0.3),
    "nb_b": ("siding", (0.62, 0.72, 0.78), 1.0, 0.3), "nb_c": ("siding", (0.9, 0.86, 0.72), 1.0, 0.3),
    "glass_dark": ("plastic", (0.03, 0.04, 0.05), 0.25, 0.0),
    "shutter": ("paint", (0.06, 0.09, 0.08), 0.8, 0.3), "white": ("paint", (0.93, 0.92, 0.88), 0.7, 0.35),
    "fence": ("wood_plain", (0.62, 0.6, 0.58), 1.4, 0.6), "metal": ("metal", (1, 1, 1), 1.0, 0.3),
    "metal_dark": ("metal", (0.25, 0.25, 0.27), 1.0, 0.3), "door_red": ("paint", (0.36, 0.07, 0.06), 0.6, 0.3),
    "door_wood": ("wood_plain", (1.0, 0.82, 0.62), 0.9, 0.25), "brass": ("metal", (0.80, 0.62, 0.30), 1.2, 0.4),
    "chrome": ("metal", (0.92, 0.93, 0.95), 0.6, 0.15), "wood_dark": ("wood_plain", (0.55, 0.45, 0.4), 1.0, 0.3),
    "wood_light": ("wood_plain", (1.5, 1.3, 1.0), 1.0, 0.25), "black": ("plastic", (0.03, 0.03, 0.03), 1.0, 0.1),
    "plastic_beige": ("plastic", (0.78, 0.72, 0.6), 1.0, 0.3), "plastic_grey": ("plastic", (0.35, 0.35, 0.36), 1.0, 0.3),
    "cardboard": ("cardboard", (1, 1, 1), 1.0, 0.3), "fabric_brown": ("fabric", (0.36, 0.24, 0.15), 1.0, 0.35),
    "fabric_green": ("fabric", (0.25, 0.32, 0.2), 1.0, 0.35), "fabric_cream": ("fabric", (0.85, 0.8, 0.68), 1.0, 0.4),
    "fabric_blue": ("fabric", (0.2, 0.3, 0.5), 1.0, 0.3), "fabric_red": ("fabric", (0.5, 0.1, 0.08), 1.0, 0.3),
    "enamel": ("paint", (0.95, 0.95, 0.93), 0.35, 0.2), "enamel_gold": ("paint", (0.93, 0.91, 0.85), 0.4, 0.2),
    "enamel_avocado": ("paint", (0.38, 0.42, 0.18), 0.45, 0.25), "laminate": ("plastic", (0.86, 0.86, 0.83), 1.1, 0.3),
    "paper": ("paint", (0.9, 0.87, 0.78), 1.1, 0.4), "rubber": ("plastic", (0.05, 0.05, 0.05), 2.0, 0.2),
    "mirror": ("plastic", (0.42, 0.45, 0.47), 0.2, 0.0), "steel": ("metal", (0.75, 0.76, 0.78), 0.9, 0.2),
    "plastic_red": ("plastic", (0.6, 0.06, 0.05), 1.0, 0.25), "plastic_blue": ("plastic", (0.08, 0.2, 0.55), 1.0, 0.25),
    "plastic_yellow": ("plastic", (0.8, 0.62, 0.08), 1.0, 0.25), "plastic_green": ("plastic", (0.1, 0.4, 0.15), 1.0, 0.25),
    "fabric_plaid": ("fabric", (0.5, 0.3, 0.16), 1.0, 0.45), "fabric_white": ("fabric", (0.9, 0.9, 0.88), 1.0, 0.3),
    "vinyl": ("plastic", (0.45, 0.1, 0.08), 1.3, 0.35), "skin_grey": ("paint", (0.5, 0.5, 0.5), 1.0, 0.0),
    "tile_wall": ("tile_bath", (0.8, 0.95, 0.9), 1.0, 0.2),
    "jazz": ("jazz", (1, 1, 1), 1.0, 0.15), "confetti": ("confetti", (1, 1, 1), 1.0, 0.15),
    "fabric_hunter": ("fabric", (0.1, 0.24, 0.15), 1.0, 0.35), "fabric_burgundy": ("fabric", (0.38, 0.07, 0.1), 1.0, 0.35),
    "plastic_teal": ("plastic", (0.05, 0.5, 0.5), 1.0, 0.2), "plastic_purple": ("plastic", (0.35, 0.12, 0.55), 1.0, 0.2),
    "plastic_pink": ("plastic", (0.85, 0.15, 0.45), 1.0, 0.2), "plastic_lime": ("plastic", (0.45, 0.8, 0.1), 1.0, 0.2),
    "oak": ("wood_plain", (1.9, 1.25, 0.62), 0.85, 0.25), "shiplap": ("siding", (1.25, 1.24, 1.18), 1.0, 0.2), "cherry": ("wood_plain", (0.9, 0.42, 0.3), 0.8, 0.2),
    "copper": ("metal", (0.85, 0.45, 0.28), 1.2, 0.4), "car_paint": ("paint", (0.2, 0.33, 0.3), 0.5, 0.55), "fabric_tan": ("fabric", (0.6, 0.48, 0.34), 1.0, 0.4),
    "fabric_sage": ("fabric", (0.45, 0.52, 0.4), 1.0, 0.35), "fabric_navy": ("fabric", (0.08, 0.11, 0.22), 1.0, 0.3), "fabric_rust": ("fabric", (0.5, 0.16, 0.1), 1.0, 0.35),
    "plastic_mint": ("plastic", (0.6, 0.85, 0.72), 1.0, 0.2), "plastic_clear": ("plastic", (0.8, 0.84, 0.86), 0.5, 0.2), "liquid_blue": ("plastic", (0.1, 0.35, 0.8), 0.3, 0.0), "fabric_butter": ("fabric", (0.86, 0.78, 0.5), 1.0, 0.3),
    "quilt": ("quilt", (1, 1, 1), 1.0, 0.2), "floral_red": ("floral_red", (1, 1, 1), 1.0, 0.2), "globe": ("paint", (0.8, 0.72, 0.55), 0.6, 0.4),
    # ---- playtest round 1: "warm Americana family home". Painted walls, a colour per room; wallpaper only in the dining room and guest room.
    "w_hall": ("paint", (0.62, 0.54, 0.38), 0.95, 0.25), "w_liv": ("paint", (0.90, 0.82, 0.62), 0.95, 0.2),
    "w_den": ("paint", (0.59, 0.41, 0.22), 0.95, 0.25), "w_den_acc": ("paint", (0.17, 0.016, 0.026), 0.9, 0.2),
    "w_kit": ("paint", (0.95, 0.80, 0.38), 0.9, 0.22), "w_mud": ("paint", (0.82, 0.72, 0.55), 0.9, 0.3),
    "w_din": ("damask", (1, 1, 1), 1.0, 0.15), "w_par": ("paint", (0.37, 0.45, 0.31), 0.95, 0.2),
    "w_jack": ("paint", (0.07, 0.137, 0.33), 0.95, 0.2), "w_sib": ("paint", (0.59, 0.49, 0.78), 0.95, 0.2),
    "w_guest": ("floral", (1, 1, 1), 1.0, 0.15), "w_bath_blue": ("paint", (0.46, 0.66, 0.84), 0.75, 0.22),
    "w_bath_mauve": ("paint", (0.57, 0.28, 0.33), 0.75, 0.22), "w_bath_sea": ("paint", (0.42, 0.72, 0.59), 0.75, 0.22),
    "w_attic": ("paint", (0.86, 0.82, 0.70), 1.0, 0.3), "w_garage": ("paint", (0.60, 0.60, 0.57), 1.0, 0.55),
    "bsmt_ceil": ("wood_plain", (0.9, 0.75, 0.6), 1.0, 0.3),
    "f_oak": ("oak_floor", (1.25, 0.92, 0.55), 0.9, 0.3), "f_vinyl": ("vinyl", (1, 1, 1), 1.0, 0.35),
    "f_hex": ("hex", (1, 1, 1), 1.0, 0.3), "f_sq": ("sq", (1, 1, 1), 1.0, 0.3),
    "f_c_hall": ("carpet_worn", (1.32, 1.18, 1.02), 1.0, 0.5), "f_c_den": ("carpet_den", (1, 1, 1), 1.0, 0.3),
    "f_c_par": ("carpet_plush", (0.62, 0.36, 0.42), 1.0, 0.3), "f_c_sib": ("carpet_plush", (0.16, 0.50, 0.50), 1.0, 0.3),
    "f_c_jack": ("carpet_kids", (1, 1, 1), 1.0, 0.25), "f_c_guest": ("carpet_plush", (0.45, 0.55, 0.68), 1.0, 0.3),
    "f_c_loft": ("carpet_plush", (0.75, 0.36, 0.10), 1.0, 0.3), "f_garage": ("drive", (0.82, 0.82, 0.82), 1.0, 0.3),
    "drive": ("drive", (1, 1, 1), 1.0, 0.25), "soil": ("soil", (1, 1, 1), 1.0, 0.2), "soil_wet": ("soil", (0.42, 0.40, 0.38), 0.45, 0.1),
    "lawn_tall": ("grass", (1.45, 1.55, 0.85), 1.0, 0.2), "tile_mauve": ("tile_bath", (1.1, 0.72, 0.8), 1.0, 0.2),
    "tile_white": ("tile_bath", (1.3, 1.1, 1.1), 1.0, 0.2), "fabric_mauve": ("fabric", (0.6, 0.32, 0.38), 1.0, 0.3),
    "fabric_denim": ("fabric", (0.12, 0.2, 0.42), 1.0, 0.3), "fabric_lav": ("fabric", (0.6, 0.5, 0.78), 1.0, 0.3),
    "plastic_white": ("plastic", (0.9, 0.9, 0.88), 1.0, 0.3), "plastic_orange": ("plastic", (0.9, 0.35, 0.05), 1.0, 0.25),
    "pumpkin": ("paint", (0.85, 0.38, 0.08), 0.8, 0.2), "fabric_stripe": ("fabric", (0.5, 0.45, 0.3), 1.0, 0.3), "plastic_black": ("plastic", (0.035, 0.035, 0.04), 1.2, 0.15), "enamel_pink": ("paint", (0.9, 0.7, 0.68), 0.35, 0.2),
}


def tex(name, suffix):
    return eal.load_asset("%s/T_%s_%s" % (TEX_DIR, name, suffix))


def build_master():
    path = MAT_DIR + "/M_Surface"
    m = eal.load_asset(path) or at.create_asset("M_Surface", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    mel.delete_all_material_expressions(m)
    E = lambda cls, x, y: mel.create_material_expression(m, cls, x, y)

    def scalar(name, default, y):
        e = E(unreal.MaterialExpressionScalarParameter, -1700, y)
        e.set_editor_property("parameter_name", name); e.set_editor_property("default_value", default)
        return e

    def texobj(name, default, sampler, y):
        e = E(unreal.MaterialExpressionTextureObjectParameter, -1700, y)
        e.set_editor_property("parameter_name", name); e.set_editor_property("texture", default)
        e.set_editor_property("sampler_type", sampler)
        return e

    def call(fn, y):
        e = E(unreal.MaterialExpressionMaterialFunctionCall, -1100, y)
        e.set_material_function(unreal.load_asset(FN + fn))
        mel.connect_material_expressions(pos, "", e, "WorldPosition")
        if fn == "WorldAlignedTexture":
            mel.connect_material_expressions(nrm, "", e, "World Space Normal")
        return e

    def xyz_out(e):
        names = [str(n) for n in mel.get_material_expression_output_names(e)]
        return next((n for n in names if "XYZ" in n), names[0])

    def size3(src, y):
        a = E(unreal.MaterialExpressionAppendVector, -1400, y)
        mel.connect_material_expressions(src, "", a, "A"); mel.connect_material_expressions(src, "", a, "B")
        b = E(unreal.MaterialExpressionAppendVector, -1300, y)
        mel.connect_material_expressions(a, "", b, "A"); mel.connect_material_expressions(src, "", b, "B")
        return b

    def local_switch(world_expr, transform_cls, y):
        t = E(transform_cls, -1500, y)
        for prop, enum_name, want in (("transform_source_type", None, "WORLD"), ("transform_type", None, "LOCAL")):
            cur = t.get_editor_property(prop)
            val = next(v for v in type(cur) if str(v).split(".")[-1].split(":")[0].endswith(want))
            t.set_editor_property(prop, val)
        mel.connect_material_expressions(world_expr, "", t, "")
        sw = E(unreal.MaterialExpressionStaticSwitchParameter, -1300, y)
        sw.set_editor_property("parameter_name", "LocalSpace"); sw.set_editor_property("default_value", False)
        mel.connect_material_expressions(t, "", sw, "True"); mel.connect_material_expressions(world_expr, "", sw, "False")
        return sw

    pos = local_switch(E(unreal.MaterialExpressionWorldPosition, -1700, -900), unreal.MaterialExpressionTransformPosition, -900)
    nrm = local_switch(E(unreal.MaterialExpressionVertexNormalWS, -1700, -700), unreal.MaterialExpressionTransform, -700)

    tile = size3(scalar("TileSize", 100.0, 0), 0)
    gsize = size3(scalar("GrungeSize", 300.0, 900), 900)

    bc = call("WorldAlignedTexture", -300)
    mel.connect_material_expressions(texobj("BaseColorTex", tex("paint", "BC"), unreal.MaterialSamplerType.SAMPLERTYPE_COLOR, -300), "", bc, "TextureObject")
    mel.connect_material_expressions(tile, "", bc, "TextureSize")
    nm = call("WorldAlignedNormal", 100)
    mel.connect_material_expressions(texobj("NormalTex", tex("paint", "N"), unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL, 100), "", nm, "TextureObject")
    mel.connect_material_expressions(tile, "", nm, "TextureSize")
    rg = call("WorldAlignedTexture", 500)
    mel.connect_material_expressions(texobj("RoughTex", tex("paint", "R"), unreal.MaterialSamplerType.SAMPLERTYPE_MASKS, 500), "", rg, "TextureObject")
    mel.connect_material_expressions(tile, "", rg, "TextureSize")
    gr = call("WorldAlignedTexture", 900)
    mel.connect_material_expressions(texobj("GrungeTex", tex("grunge", "BC"), unreal.MaterialSamplerType.SAMPLERTYPE_COLOR, 900), "", gr, "TextureObject")
    mel.connect_material_expressions(gsize, "", gr, "TextureSize")

    tint = E(unreal.MaterialExpressionVectorParameter, -800, -500)
    tint.set_editor_property("parameter_name", "Tint"); tint.set_editor_property("default_value", unreal.LinearColor(1, 1, 1, 1))
    tinted = E(unreal.MaterialExpressionMultiply, -600, -300)
    mel.connect_material_expressions(bc, xyz_out(bc), tinted, "A"); mel.connect_material_expressions(tint, "", tinted, "B")

    gmask = E(unreal.MaterialExpressionComponentMask, -800, 900)
    gmask.set_editor_property("r", True); gmask.set_editor_property("g", False); gmask.set_editor_property("b", False); gmask.set_editor_property("a", False)
    mel.connect_material_expressions(gr, xyz_out(gr), gmask, "")
    one = E(unreal.MaterialExpressionConstant, -800, 800); one.set_editor_property("r", 1.0)
    dirt = E(unreal.MaterialExpressionLinearInterpolate, -600, 850)      # 1 where clean, darker where the grunge map is dark
    mel.connect_material_expressions(one, "", dirt, "A"); mel.connect_material_expressions(gmask, "", dirt, "B")
    mel.connect_material_expressions(scalar("DirtAmount", 0.25, 1050), "", dirt, "Alpha")
    final = E(unreal.MaterialExpressionMultiply, -350, -200)
    mel.connect_material_expressions(tinted, "", final, "A"); mel.connect_material_expressions(dirt, "", final, "B")
    mel.connect_material_property(final, "", unreal.MaterialProperty.MP_BASE_COLOR)

    rmask = E(unreal.MaterialExpressionComponentMask, -800, 500)
    rmask.set_editor_property("r", True); rmask.set_editor_property("g", False); rmask.set_editor_property("b", False); rmask.set_editor_property("a", False)
    mel.connect_material_expressions(rg, xyz_out(rg), rmask, "")
    rmul = E(unreal.MaterialExpressionMultiply, -600, 500)
    mel.connect_material_expressions(rmask, "", rmul, "A"); mel.connect_material_expressions(scalar("RoughScale", 1.0, 650), "", rmul, "B")
    rsat = E(unreal.MaterialExpressionSaturate, -450, 500)
    mel.connect_material_expressions(rmul, "", rsat, "")
    mel.connect_material_property(rsat, "", unreal.MaterialProperty.MP_ROUGHNESS)

    mel.connect_material_property(nm, xyz_out(nm), unreal.MaterialProperty.MP_NORMAL)
    mel.connect_material_property(scalar("Metallic", 0.0, 1250), "", unreal.MaterialProperty.MP_METALLIC)
    mel.connect_material_property(scalar("Specular", 0.4, 1400), "", unreal.MaterialProperty.MP_SPECULAR)
    mel.recompile_material(m)
    eal.save_asset(path)
    return m


def build_lamp():
    """Glowing lamp-shade / bulb materials. They only glow at night: the glow is multiplied by MPC_World.Night (0 or 1)."""
    mpc_path = MAT_DIR + "/MPC_World"
    mpc = eal.load_asset(mpc_path)
    if mpc is None:
        mpc = at.create_asset("MPC_World", MAT_DIR, unreal.MaterialParameterCollection, unreal.MaterialParameterCollectionFactoryNew())
        eal.save_asset(mpc_path)
    want = {"Night": 0.0, "Unease": 0.0, "Motion": 1.0, "Frozen": 0.0, "Fade": 0.0}
    have = set(str(n) for n in mpc.get_scalar_parameter_names())
    if set(want) - set(have):
        arr = []
        for n, v in want.items():
            sp = unreal.CollectionScalarParameter(); sp.set_editor_property("parameter_name", n); sp.set_editor_property("default_value", v); arr.append(sp)
        mpc.set_editor_property("scalar_parameters", arr); eal.save_asset(mpc_path)
    path = MAT_DIR + "/M_Lamp"
    m = eal.load_asset(path) or at.create_asset("M_Lamp", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    mel.delete_all_material_expressions(m)
    col = mel.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -700, 0)
    col.set_editor_property("parameter_name", "Color"); col.set_editor_property("default_value", unreal.LinearColor(1.0, 0.82, 0.55, 1))
    st = mel.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -700, 250)
    st.set_editor_property("parameter_name", "Glow"); st.set_editor_property("default_value", 0.0)
    night = mel.create_material_expression(m, unreal.MaterialExpressionCollectionParameter, -700, 400)
    night.set_editor_property("collection", mpc); night.set_editor_property("parameter_name", "Night")
    tm = mel.create_material_expression(m, unreal.MaterialExpressionTime, -700, 520)
    def sc(name, y):
        e = mel.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -700, y)
        e.set_editor_property("parameter_name", name); e.set_editor_property("default_value", 0.0); return e
    g = mel.create_material_expression(m, unreal.MaterialExpressionCustom, -450, 300)
    g.set_editor_property("output_type", unreal.CustomMaterialOutputType.CMOT_FLOAT1)
    ins = []
    for n in ("Glow", "Night", "T", "Blink", "Always"):
        ci = unreal.CustomInput(); ci.set_editor_property("input_name", n); ins.append(ci)
    g.set_editor_property("inputs", ins)
    g.set_editor_property("code", "return Glow * max(Night, Always) * lerp(1.0, step(0.45, frac(T * 1.7)), Blink);")
    mel.connect_material_expressions(st, "", g, "Glow"); mel.connect_material_expressions(night, "", g, "Night"); mel.connect_material_expressions(tm, "", g, "T")
    mel.connect_material_expressions(sc("Blink", 620), "", g, "Blink"); mel.connect_material_expressions(sc("Always", 720), "", g, "Always")
    mul = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -250, 100)
    mel.connect_material_expressions(col, "", mul, "A"); mel.connect_material_expressions(g, "", mul, "B")
    mel.connect_material_property(mul, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mel.connect_material_property(col, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.recompile_material(m); eal.save_asset(path)
    for name, glow, c in (("lamp_on", 700.0, (1.0, 0.85, 0.6)), ("lamp_off", 0.0, (0.9, 0.88, 0.8)), ("lamp_dim", 30.0, (0.3, 1.0, 0.5)),
                          ("lamp_shade", 45.0, (0.86, 0.74, 0.52)), ("lamp_lava", 60.0, (0.9, 0.1, 0.45)), ("lamp_star", 5.0, (0.55, 1.0, 0.45)), ("lamp_blink", 40.0, (0.3, 1.0, 0.3)), ("lamp_led", 25.0, (1.0, 0.2, 0.1))):
        for pre in ("MI_", "MIL_"):
            p = "%s/%s%s" % (MAT_DIR, pre, name)
            mi = eal.load_asset(p) or at.create_asset(pre + name, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
            mi.set_editor_property("parent", m)
            mel.set_material_instance_scalar_parameter_value(mi, "Glow", glow)
            mel.set_material_instance_scalar_parameter_value(mi, "Blink", 1.0 if name == "lamp_blink" else 0.0)
            mel.set_material_instance_scalar_parameter_value(mi, "Always", 1.0 if name in ("lamp_blink", "lamp_led") else 0.0)
            mel.set_material_instance_vector_parameter_value(mi, "Color", unreal.LinearColor(c[0], c[1], c[2], 1))
            mel.update_material_instance(mi); eal.save_asset(p)


def build_glass():
    path = MAT_DIR + "/M_Glass"
    m = eal.load_asset(path) or at.create_asset("M_Glass", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    mel.delete_all_material_expressions(m)
    m.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    m.set_editor_property("two_sided", True)
    m.set_editor_property("translucency_lighting_mode", unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
    E = lambda cls, x, y: mel.create_material_expression(m, cls, x, y)
    col = E(unreal.MaterialExpressionConstant3Vector, -400, -200); col.set_editor_property("constant", unreal.LinearColor(0.55, 0.6, 0.55, 1))
    mel.connect_material_property(col, "", unreal.MaterialProperty.MP_BASE_COLOR)
    gr = E(unreal.MaterialExpressionMaterialFunctionCall, -700, 100)
    gr.set_material_function(unreal.load_asset(FN + "WorldAlignedTexture"))
    to = E(unreal.MaterialExpressionTextureObject, -1000, 100); to.set_editor_property("texture", tex("grunge", "BC"))
    sz = E(unreal.MaterialExpressionConstant3Vector, -1000, 300); sz.set_editor_property("constant", unreal.LinearColor(170, 170, 170, 1))
    mel.connect_material_expressions(to, "", gr, "TextureObject"); mel.connect_material_expressions(sz, "", gr, "TextureSize")
    msk = E(unreal.MaterialExpressionComponentMask, -450, 100)
    msk.set_editor_property("r", True); msk.set_editor_property("g", False); msk.set_editor_property("b", False); msk.set_editor_property("a", False)
    mel.connect_material_expressions(gr, "XYZ Texture", msk, "")
    a0 = E(unreal.MaterialExpressionConstant, -450, 250); a0.set_editor_property("r", 0.30)      # dusty where the grunge map is dark
    a1 = E(unreal.MaterialExpressionConstant, -450, 320); a1.set_editor_property("r", 0.07)
    lerp = E(unreal.MaterialExpressionLinearInterpolate, -250, 200)
    mel.connect_material_expressions(a0, "", lerp, "A"); mel.connect_material_expressions(a1, "", lerp, "B"); mel.connect_material_expressions(msk, "", lerp, "Alpha")
    mel.connect_material_property(lerp, "", unreal.MaterialProperty.MP_OPACITY)
    r = E(unreal.MaterialExpressionConstant, -250, 400); r.set_editor_property("r", 0.08)
    mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    sp = E(unreal.MaterialExpressionConstant, -250, 470); sp.set_editor_property("r", 0.5)
    mel.connect_material_property(sp, "", unreal.MaterialProperty.MP_SPECULAR)
    mel.recompile_material(m)
    eal.save_asset(path)


master = build_master()
build_glass()
build_lamp()
for key, (ts, tint, rough, dirt) in KEYS.items():
    for prefix, local in (("MI_", False), ("MIL_", True)):
        p = "%s/%s%s" % (MAT_DIR, prefix, key)
        mi = eal.load_asset(p)
        if mi is None:
            mi = at.create_asset(prefix + key, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        mi.set_editor_property("parent", master)
        mel.set_material_instance_texture_parameter_value(mi, "BaseColorTex", tex(ts, "BC"))
        mel.set_material_instance_texture_parameter_value(mi, "NormalTex", tex(ts, "N"))
        mel.set_material_instance_texture_parameter_value(mi, "RoughTex", tex(ts, "R"))
        mel.set_material_instance_scalar_parameter_value(mi, "TileSize", float(manifest[ts]["size_cm"]))
        mel.set_material_instance_scalar_parameter_value(mi, "RoughScale", rough)
        mel.set_material_instance_scalar_parameter_value(mi, "GrungeSize", 1700.0 if key in ("lawn", "leaf", "asphalt", "concrete", "roof") else 300.0)
        mel.set_material_instance_scalar_parameter_value(mi, "DirtAmount", dirt)
        mel.set_material_instance_scalar_parameter_value(mi, "Metallic", float(manifest[ts].get("metallic", 0.0)))
        mel.set_material_instance_vector_parameter_value(mi, "Tint", unreal.LinearColor(tint[0], tint[1], tint[2], 1))
        mel.set_material_instance_static_switch_parameter_value(mi, "LocalSpace", local)
        mel.update_material_instance(mi)
        eal.save_asset(p)
if eal.does_asset_exist(MAT_DIR + "/M_Probe"):
    eal.delete_asset(MAT_DIR + "/M_Probe")
print("master rebuilt, instances:", len(KEYS))
