"""Creates the placeholder master material and one tinted instance per surface key.
Instances keep their names when the master is upgraded to full PBR later, so the shell never needs re-assigning."""
import unreal

MAT_DIR = "/Game/Materials"
KEYS = {
    # walls
    "brick": (0.36, 0.17, 0.12), "siding": (0.78, 0.76, 0.68), "liv": (0.33, 0.21, 0.12), "hall": (0.72, 0.66, 0.50),
    "kit": (0.80, 0.74, 0.52), "bath": (0.62, 0.74, 0.72), "bed": (0.55, 0.63, 0.74), "hall2": (0.70, 0.64, 0.52),
    "blk": (0.35, 0.35, 0.35), "bsmt": (0.42, 0.42, 0.40), "ceiling": (0.86, 0.84, 0.78), "trim": (0.85, 0.83, 0.76),
    "rail": (0.30, 0.19, 0.11),
    # floors
    "f_liv": (0.45, 0.30, 0.12), "f_hall": (0.42, 0.27, 0.14), "f_entry": (0.30, 0.31, 0.30), "f_kit": (0.62, 0.55, 0.38),
    "f_stair": (0.40, 0.33, 0.24), "f_hall2": (0.42, 0.35, 0.26), "f_bath": (0.70, 0.76, 0.74), "f_bed": (0.26, 0.32, 0.42),
    "f_blk": (0.30, 0.30, 0.30), "f_bsmt": (0.38, 0.38, 0.37),
    # outside
    "roof": (0.16, 0.14, 0.13), "lawn": (0.20, 0.33, 0.10), "concrete": (0.55, 0.54, 0.51), "asphalt": (0.10, 0.10, 0.10),
    "garage_door": (0.80, 0.79, 0.74), "bark": (0.20, 0.14, 0.09), "leaf": (0.13, 0.27, 0.08),
    "nb_a": (0.70, 0.62, 0.48), "nb_b": (0.55, 0.62, 0.66), "nb_c": (0.74, 0.72, 0.66), "glass_dark": (0.03, 0.04, 0.05),
}

at = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary
eal = unreal.EditorAssetLibrary

master_path = MAT_DIR + "/M_Surface"
master = eal.load_asset(master_path)
if master is None:
    master = at.create_asset("M_Surface", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    tint = mel.create_material_expression(master, unreal.MaterialExpressionVectorParameter, -400, 0)
    tint.set_editor_property("parameter_name", "Tint")
    tint.set_editor_property("default_value", unreal.LinearColor(0.5, 0.5, 0.5, 1))
    rough = mel.create_material_expression(master, unreal.MaterialExpressionScalarParameter, -400, 250)
    rough.set_editor_property("parameter_name", "Roughness")
    rough.set_editor_property("default_value", 0.85)
    mel.connect_material_property(tint, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(rough, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.recompile_material(master)
    eal.save_asset(master_path)

made = 0
for key, rgb in KEYS.items():
    p = "%s/MI_%s" % (MAT_DIR, key)
    mi = eal.load_asset(p)
    if mi is None:
        f = unreal.MaterialInstanceConstantFactoryNew()
        mi = at.create_asset("MI_" + key, MAT_DIR, unreal.MaterialInstanceConstant, f)
        mi.set_editor_property("parent", master)
        made += 1
    mel.set_material_instance_vector_parameter_value(mi, "Tint", unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1))
    eal.save_asset(p)
print("materials ready, new:", made, "total:", len(KEYS))
