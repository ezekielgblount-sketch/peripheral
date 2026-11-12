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
LOOPS = ("room_tone", "fridge_hum", "outdoor_day", "tape_hiss", "clock_tick", "music_dayone", "underwater", "car_engine", "house_groan",
         "mower_loop", "washer_loop", "dryer_loop", "water_pour", "tv_static",
         "music_title", "music_day1_calm", "music_unease_low", "music_unease_mid", "music_unease_high", "music_loop_sequence")
eal = unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
# sound classes, so the Audio settings can turn music, effects and ambience up and down separately
def asset(name, cls, factory):
    return eal.load_asset("/Game/Audio/" + name) or at.create_asset(name, "/Game/Audio", cls, factory)
master = asset("SC_Master", unreal.SoundClass, unreal.SoundClassFactory())
kids = {k: asset("SC_" + k, unreal.SoundClass, unreal.SoundClassFactory()) for k in ("Music", "SFX", "Ambience")}
master.set_editor_property("child_classes", list(kids.values()))
for c in kids.values():
    c.set_editor_property("parent_class", master)
mix = asset("Mix_Settings", unreal.SoundMix, unreal.SoundMixFactory())
AMB = ("room_tone", "fridge_hum", "outdoor_day", "clock_tick", "tape_hiss", "underwater", "lights_hum", "house_groan")
for f in sorted(os.listdir(src)):
    if not f.endswith(".wav"):
        continue
    n = f[:-4]; w = eal.load_asset("/Game/Audio/" + n)
    w.set_editor_property("looping", n in LOOPS)
    w.set_editor_property("sound_class_object", kids["Music" if n.startswith("music_") else "Ambience" if n in AMB else "SFX"])
    eal.save_asset("/Game/Audio/" + n)
for n in ("SC_Master", "SC_Music", "SC_SFX", "SC_Ambience", "Mix_Settings"):
    eal.save_asset("/Game/Audio/" + n)
print("audio imported:", len(tasks), "| sound classes: Master > Music, SFX, Ambience")
