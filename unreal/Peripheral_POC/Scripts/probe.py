mel = unreal.MaterialEditingLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
m = at.create_asset("M_Probe", "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
FN = "/Engine/Functions/Engine_MaterialFunctions01/Texturing/"
for fn in ("WorldAlignedTexture", "WorldAlignedNormal"):
    e = mel.create_material_expression(m, unreal.MaterialExpressionMaterialFunctionCall, 0, 0)
    e.set_material_function(unreal.load_asset(FN + fn))
    c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -300, 0)
    print(fn, "inputs:", [str(n) for n in mel.get_material_expression_input_names(e)] if hasattr(mel, "get_material_expression_input_names") else "n/a",
          "outputs:", [str(n) for n in mel.get_material_expression_output_names(e)])
print([n for n in dir(mel) if "static" in n or "switch" in n])
print([n for n in dir(unreal) if n.startswith("MaterialExpressionTransform") or n.startswith("MaterialExpressionStaticSwitch") or n in ("MaterialExpressionWorldPosition","MaterialExpressionVertexNormalWS","MaterialExpressionPixelNormalWS")])
print([str(x) for x in list(unreal.MaterialVectorCoordTransformSource)] if hasattr(unreal,"MaterialVectorCoordTransformSource") else "", [n for n in dir(unreal) if "PositionTransform" in n or "MaterialVectorCoord" in n])
unreal.EditorAssetLibrary.delete_asset("/Game/Materials/M_Probe")
