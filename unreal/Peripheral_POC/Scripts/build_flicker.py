"""Light-function material for the one old fixture that flickers: a faint shimmer with an occasional short dip."""
import unreal
mel, eal = unreal.MaterialEditingLibrary, unreal.EditorAssetLibrary
path = "/Game/Materials/M_Flicker"
m = eal.load_asset(path) or unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_Flicker", "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
mel.delete_all_material_expressions(m)
m.set_editor_property("material_domain", unreal.MaterialDomain.MD_LIGHT_FUNCTION)
tm = mel.create_material_expression(m, unreal.MaterialExpressionTime, -600, 0)
c = mel.create_material_expression(m, unreal.MaterialExpressionCustom, -350, 0)
c.set_editor_property("output_type", unreal.CustomMaterialOutputType.CMOT_FLOAT1)
ci = unreal.CustomInput(); ci.set_editor_property("input_name", "T"); c.set_editor_property("inputs", [ci])
c.set_editor_property("code", "float f = 0.94 + 0.06 * sin(T * 47.0) * sin(T * 3.1);\nfloat dip = step(0.95, frac(sin(floor(T * 9.0) * 12.9898) * 43758.5453));\nreturn saturate(f - dip * 0.4);")
mel.connect_material_expressions(tm, "", c, "T")
mel.connect_material_property(c, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
mel.recompile_material(m); eal.save_asset(path); print("flicker material built")
