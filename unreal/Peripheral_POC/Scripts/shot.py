#!/usr/bin/env python3
"""Take screenshots through the open editor's level viewport (Lumen lighting included).
Usage: shot.py out_dir name:x,y,z:tx,ty,tz ...   (blueprint coords, cm)
The viewport is redrawn on several editor ticks before each picture so lighting and exposure settle,
then the picture is captured with the MCP CaptureViewport tool."""
import sys, os, subprocess, base64
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from mcp_tool import call
out_dir = os.path.abspath(sys.argv[1]); os.makedirs(out_dir, exist_ok=True)
HEAD = """
import sys
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
try:
    unreal.EditorLevelLibrary.editor_set_game_view(True)
except Exception:
    pass
"""
TICKS = int(os.environ.get("SHOT_TICKS", "25"))
REDRAW = "unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_invalidate_viewports()"


def ue(code):
    subprocess.run([sys.executable, os.path.join(here, "uepy.py"), "-c", HEAD + code, "300"], check=True,
                   stdout=subprocess.DEVNULL)


SPEED = """
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label() == "PP_Base":
        st = a.settings
        st.set_editor_property("auto_exposure_speed_up", %s); st.set_editor_property("auto_exposure_speed_down", %s)
        a.set_editor_property("settings", st)
"""
ue(SPEED % (20.0, 20.0))          # let exposure settle instantly for stills; restored below
import time
for _ in range(int(os.environ.get('SHOT_WARMUP', '40'))):      # let sky capture and bounce light settle after a day/night switch
    ue(REDRAW); time.sleep(0.05)
for spec in sys.argv[2:]:
    name, p, t = spec.split(":")[:3]
    out = os.path.join(out_dir, name + ".png")
    ue(f"""
p = L.to_ue({p}); t = L.to_ue({t})
ues.set_level_viewport_camera_info(p, unreal.MathLibrary.find_look_at_rotation(p, t))
""")
    for _ in range(TICKS):
        ue(REDRAW); time.sleep(0.05)
    r = call("EditorToolset.EditorAppToolset", "CaptureViewport", {"captureTransform": None, "annotations": None, "bShowUI": False})
    try:
        data = base64.b64decode(r["returnValue"]["image"]["data"])
        with open(out, "wb") as f:
            f.write(data)
        try:
            from PIL import Image
            im = Image.open(out).convert("RGB"); im.thumbnail((1600, 1600)); im.save(out)
        except ImportError:
            pass
        print("ok", out)
    except Exception as e:
        print("MISSING", out, str(r)[:200], e)
ue(SPEED % (1.2, 0.7))
