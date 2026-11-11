"""Lighting materials: the light function for the one old fixture that flickers, and lit / unlit bulb and shade materials
for lamps the player switches (they glow whenever the lamp is on, day or night). Safe to re-run."""
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

lamp = eal.load_asset("/Game/Materials/M_Lamp")
at = unreal.AssetToolsHelpers.get_asset_tools()
for name, glow, col in (("bulb_lit", 700.0, (1.0, 0.85, 0.6)), ("shade_lit", 60.0, (0.86, 0.74, 0.52)), ("shade_unlit", 0.0, (0.86, 0.8, 0.66)),
                        ("halogen_lit", 900.0, (1.0, 0.9, 0.7)), ("tv_static", 2.2, (0.45, 0.55, 0.8))):
    for pre in ("MI_", "MIL_"):
        pth = "/Game/Materials/%s%s" % (pre, name)
        mi = eal.load_asset(pth) or at.create_asset(pre + name, "/Game/Materials", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        mi.set_editor_property("parent", lamp)
        mel.set_material_instance_scalar_parameter_value(mi, "Glow", glow)
        mel.set_material_instance_scalar_parameter_value(mi, "Blink", 0.0)
        mel.set_material_instance_scalar_parameter_value(mi, "Always", 1.0)
        mel.set_material_instance_vector_parameter_value(mi, "Color", unreal.LinearColor(col[0], col[1], col[2], 1))
        mel.update_material_instance(mi); eal.save_asset(pth)
print("lit / unlit lamp materials built")
