#!/usr/bin/env python3
"""Take screenshots through the open editor's level viewport (Lumen lighting included).
Usage: shot.py out_dir name:x,y,z:tx,ty,tz ...   (blueprint coords, cm)
The viewport is redrawn on several editor ticks before each picture so lighting and exposure settle."""
import sys, os, subprocess, time
here = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.abspath(sys.argv[1]); os.makedirs(out_dir, exist_ok=True)
HEAD = """
import sys
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
"""
TICKS = int(os.environ.get("SHOT_TICKS", "25"))


def ue(code):
    subprocess.run([sys.executable, os.path.join(here, "uepy.py"), "-c", HEAD + code, "300"], check=True,
                   stdout=subprocess.DEVNULL)


for spec in sys.argv[2:]:
    name, p, t = spec.split(":")[:3]
    out = os.path.join(out_dir, name + ".png")
    tmp = os.path.join(out_dir, name + "_pending.png")
    ue(f"""
p = L.to_ue({p}); t = L.to_ue({t})
ues.set_level_viewport_camera_info(p, unreal.MathLibrary.find_look_at_rotation(p, t))
""")
    for _ in range(TICKS):
        ue("unreal.EditorLevelLibrary.editor_invalidate_viewports()")
    ue(f'unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, r"{tmp}")')
    t0 = time.time()
    while not os.path.exists(tmp) and time.time() - t0 < 60:
        ue("unreal.EditorLevelLibrary.editor_invalidate_viewports()")
    time.sleep(0.5)
    if os.path.exists(tmp):
        os.replace(tmp, out)
        print("ok", out)
    else:
        print("MISSING", out)
