"""Imports SourceArt/Audio WAVs into /Game/Audio; loops are marked looping."""
import os, unreal
root = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
src = os.path.join(root, "SourceArt", "Audio")
tasks = []
for f in sorted(os.listdir(src)):
    if f.endswith(".wav"):
        t = unreal.AssetImportTask()
        for k, v in (("filename", os.path.join(src, f)), ("destination_path", "/Game/Audio"), ("automated", True), ("replace_existing", True), ("save", True)):
            t.set_editor_property(k, v)
        tasks.append(t)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
for n in ("room_tone", "fridge_hum", "outdoor_day", "tape_hiss", "clock_tick", "music_dayone", "underwater", "car_engine"):
    w = unreal.EditorAssetLibrary.load_asset("/Game/Audio/" + n)
    w.set_editor_property("looping", True); unreal.EditorAssetLibrary.save_asset("/Game/Audio/" + n)
print("audio imported:", len(tasks))
