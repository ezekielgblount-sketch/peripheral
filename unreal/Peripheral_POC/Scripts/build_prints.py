"""Imports SourceArt/Prints into /Game/Prints and makes one material per image (MP_<name>) from the M_Print master."""
import os, unreal
root = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
src = os.path.join(root, "SourceArt", "Prints")
mel, eal = unreal.MaterialEditingLibrary, unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
names = sorted(f[:-4] for f in os.listdir(src) if f.endswith(".png"))
tasks = []
for n in names:
    t = unreal.AssetImportTask()
    for k, v in (("filename", os.path.join(src, n + ".png")), ("destination_path", "/Game/Prints"), ("automated", True),
                 ("replace_existing", True), ("save", True)):
        t.set_editor_property(k, v)
    tasks.append(t)
at.import_asset_tasks(tasks)

path = "/Game/Materials/M_Print"
m = eal.load_asset(path) or at.create_asset("M_Print", "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
mel.delete_all_material_expressions(m)
m.set_editor_property("blend_mode", unreal.BlendMode.BLEND_MASKED)
m.set_editor_property("two_sided", True)                 # flat prints show from either side
tx = mel.create_material_expression(m, unreal.MaterialExpressionTextureSampleParameter2D, -600, 0)
tx.set_editor_property("parameter_name", "Tex"); tx.set_editor_property("texture", eal.load_asset("/Game/Prints/" + names[0]))
tint = mel.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -600, -250)
tint.set_editor_property("parameter_name", "Tint"); tint.set_editor_property("default_value", unreal.LinearColor(1, 1, 1, 1))
mul = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -300, -100)
mel.connect_material_expressions(tx, "RGB", mul, "A"); mel.connect_material_expressions(tint, "", mul, "B")
mel.connect_material_property(mul, "", unreal.MaterialProperty.MP_BASE_COLOR)
mel.connect_material_property(tx, "A", unreal.MaterialProperty.MP_OPACITY_MASK)
r = mel.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -300, 200)
r.set_editor_property("parameter_name", "Rough"); r.set_editor_property("default_value", 0.6)
mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
mel.recompile_material(m); eal.save_asset(path)
for n in names:
    p = "/Game/Materials/MP_" + n
    mi = eal.load_asset(p) or at.create_asset("MP_" + n, "/Game/Materials", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mi.set_editor_property("parent", m)
    mel.set_material_instance_texture_parameter_value(mi, "Tex", eal.load_asset("/Game/Prints/" + n))
    mel.set_material_instance_scalar_parameter_value(mi, "Rough", 0.95 if ("rug" in n or "label" in n) else 0.45)
    mel.update_material_instance(mi); eal.save_asset(p)
print("prints:", len(names))
