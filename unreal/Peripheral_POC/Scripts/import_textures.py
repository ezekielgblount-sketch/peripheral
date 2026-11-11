"""Imports SourceArt/Textures PNGs into /Game/Textures with the right compression and colour-space settings."""
import os, json, unreal
root = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
src = os.path.join(root, "SourceArt", "Textures")
dest = "/Game/Textures"
tasks = []
for f in sorted(os.listdir(src)):
    if not f.endswith(".png"):
        continue
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", os.path.join(src, f))
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", False)
    tasks.append(t)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
n = 0
for f in sorted(os.listdir(src)):
    if not f.endswith(".png"):
        continue
    name = f[:-4]
    tex = unreal.EditorAssetLibrary.load_asset("%s/%s" % (dest, name))
    if tex is None:
        print("missing", name); continue
    if name.endswith("_N"):
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
        tex.set_editor_property("srgb", False)
    elif name.endswith("_R"):
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
        tex.set_editor_property("srgb", False)
    else:
        tex.set_editor_property("srgb", True)
    unreal.EditorAssetLibrary.save_asset("%s/%s" % (dest, name))
    n += 1
print("imported", n, "textures")
