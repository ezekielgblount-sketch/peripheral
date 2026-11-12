#!/usr/bin/env python3
"""Builds the menu widget WBP_Menu: title, pause, how to play, and the five settings pages. Layout only; its logic is
Scripts/bp/gen_menu.py. Run with the editor open: python3 Scripts/ui_menu.py"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui_tool import Builder, col, pad, font
LEVELS = ["Low", "Medium", "High", "Epic"]
# name -> (page, label, kind, extra). kind: combo [options] | slider (min, max) | check | key
ROWS = [
    ("WinMode", 0, "Window mode", "combo", ["Windowed", "Borderless", "Full screen"]),
    ("Res", 0, "Resolution", "combo", ["1280 x 720", "1600 x 900", "1920 x 1080", "2560 x 1440", "3024 x 1964", "3840 x 2160"]),
    ("VSync", 0, "V-sync", "check", None),
    ("FpsCap", 0, "Frame rate cap", "combo", ["30", "60", "120", "Unlimited"]),
    ("Fov", 0, "Field of view", "slider", (70, 110)),
    ("Preset", 1, "Overall preset", "combo", LEVELS + ["Custom"]),
    ("Shadows", 1, "Shadows", "combo", LEVELS), ("GI", 1, "Global illumination", "combo", LEVELS), ("Refl", 1, "Reflections", "combo", LEVELS),
    ("Tex", 1, "Textures", "combo", LEVELS), ("Fx", 1, "Effects", "combo", LEVELS), ("Post", 1, "Post-processing", "combo", LEVELS),
    ("AA", 1, "Anti-aliasing", "combo", LEVELS), ("Scale", 1, "Resolution scale (upscaling)", "slider", (50, 100)),
    ("Master", 2, "Master volume", "slider", (0, 1)), ("Music", 2, "Music", "slider", (0, 1)), ("Sfx", 2, "Sound effects", "slider", (0, 1)), ("Amb", 2, "Ambience", "slider", (0, 1)),
    ("Sens", 3, "Mouse sensitivity", "slider", (0.1, 1.5)), ("Invert", 3, "Invert Y", "check", None),
    ("KFwd", 3, "Walk forward", "key", None), ("KBack", 3, "Walk back", "key", None), ("KLeft", 3, "Step left", "key", None), ("KRight", 3, "Step right", "key", None),
    ("KUse", 3, "Use / pick up", "key", None), ("KCrouch", 3, "Crouch", "key", None), ("KLight", 3, "Flashlight", "key", None),
    ("Motion", 4, "Camera motion intensity", "slider", (0, 1)), ("Cap", 4, "Unease effect intensity cap", "slider", (0, 1)), ("Subs", 4, "Subtitles", "check", None),
]
PAGES = ["Display", "Graphics", "Audio", "Controls", "Accessibility"]
HOW = ("W A S D  walk          Mouse  look          E  use, pick up, push, put down\n"
       "C  crouch              F  flashlight         Esc  pause (frees the mouse)\n\n"
       "Day One: follow the note in the corner.\n"
       "Chore day (F5): do the list. Things in the house change when you are not looking.\n"
       "F6 shows what has changed so far, and whether you have looked at it since.\n"
       "The Loop (L): something in the hall changed: go back the way you came. Nothing changed: keep going.\n\n"
       "Test keys: 1-0 and minus set the unease level, F1 shows the unease bar, N day / night, H loosens the shadow.")

if __name__ == "__main__":
    b = Builder("/Game/UI", "WBP_Menu")
    C = lambda l, t, r, bt, ax0, ay0, ax1, ay1, alx=0, aly=0: {"layoutData": {"offsets": {"left": l, "top": t, "right": r, "bottom": bt}, "anchors": {"minimum": {"x": ax0, "y": ay0}, "maximum": {"x": ax1, "y": ay1}}, "alignment": {"x": alx, "y": aly}}}
    root = b.add("CanvasPanel", "Root")
    b.add("Border", "Dim", root, {"brushColor": {"r": 0, "g": 0, "b": 0, "a": 0.66}}, C(0, 0, 0, 0, 0, 0, 1, 1), True)
    # ---- title ----
    tb = b.add("VerticalBox", "TitleBox", root, None, C(120, -230, 620, 560, 0, 0.5, 0, 0.5), True)
    b.text("TitleLogo", tb, "PERIPHERAL", 64, "Bold", {"padding": pad(0, 0, 0, 6)})
    b.text("TitleSub", tb, "visual proof of concept  -  playtest round 1", 16, slot={"padding": pad(4, 0, 0, 34)}, color=(0.7, 0.68, 0.62))
    for n, lab in (("BtnDay1", "Play  -  Day One"), ("BtnChore", "Play  -  Chore day (anomaly test)"), ("BtnLoop", "Play  -  The Loop"), ("BtnSettings", "Settings"), ("BtnHow", "How to play"), ("BtnQuit", "Quit")):
        b.button(n, tb, lab, 24, {"padding": pad(0, 5)})
    # ---- pause ----
    pb = b.add("VerticalBox", "PauseBox", root, None, C(-230, -220, 460, 460, 0.5, 0.5, 0.5, 0.5), True)
    b.text("PauseTitle", pb, "Paused", 44, "Bold", {"padding": pad(0, 0, 0, 24), "horizontalAlignment": "HAlign_Center"})
    for n, lab in (("BtnResume", "Resume"), ("BtnPSettings", "Settings"), ("BtnPHow", "How to play"), ("BtnTitle", "Back to the title"), ("BtnPQuit", "Quit")):
        b.button(n, pb, lab, 24, {"padding": pad(0, 5)})
    b.text("PauseHint", pb, "The mouse is free while this menu is open.\nResume (or Esc) takes it back.", 15, slot={"padding": pad(0, 18, 0, 0)}, color=(0.7, 0.68, 0.62), just="Center")
    # ---- how to play ----
    hb = b.add("Border", "HowBox", root, {"brushColor": {"r": 0.03, "g": 0.03, "b": 0.035, "a": 0.92}, "padding": pad(34, 26)}, C(-520, -300, 1040, 600, 0.5, 0.5, 0.5, 0.5), True)
    hv = b.add("VerticalBox", "HowV", hb)
    b.text("HowTitle", hv, "How to play", 36, "Bold", {"padding": pad(0, 0, 0, 18)})
    b.text("HowText", hv, HOW, 19, slot={"padding": pad(0, 0, 0, 22)}, wrap=960)
    b.button("BtnHowBack", hv, "Back", 22, {"horizontalAlignment": "HAlign_Left"})
    # ---- settings ----
    sb = b.add("Border", "SettingsBox", root, {"brushColor": {"r": 0.03, "g": 0.03, "b": 0.035, "a": 0.94}, "padding": pad(30, 22)}, C(-540, -360, 1080, 720, 0.5, 0.5, 0.5, 0.5), True)
    sv = b.add("VerticalBox", "SettingsV", sb)
    b.text("SetTitle", sv, "Settings", 36, "Bold", {"padding": pad(0, 0, 0, 12)})
    tabs = b.add("HorizontalBox", "Tabs", sv, None, {"padding": pad(0, 0, 0, 14)})
    for i, pg in enumerate(PAGES):
        b.button("BtnTab%d" % i, tabs, pg, 20, {"padding": pad(0, 0, 8, 0)})
    scroll = b.add("ScrollBox", "Scroll", sv, None, {"size": {"value": 1.0, "sizeRule": "Fill"}})
    pages = [b.add("VerticalBox", "Page%d" % i, scroll, None, None, True) for i in range(len(PAGES))]
    for (name, page, label, kind, extra) in ROWS:
        row = b.add("HorizontalBox", "Row" + name, pages[page], None, {"padding": pad(0, 7)})
        b.text("Lab" + name, row, label, 20, slot={"size": {"value": 0.42, "sizeRule": "Fill"}, "verticalAlignment": "VAlign_Center"})
        fill = {"size": {"value": 0.44, "sizeRule": "Fill"}, "verticalAlignment": "VAlign_Center"}
        if kind == "combo":
            b.add("ComboBoxString", "C" + name, row, {"defaultOptions": extra, "selectedOption": extra[0], "font": font(18)}, fill, True)
        elif kind == "slider":
            b.add("Slider", "C" + name, row, {"minValue": extra[0], "maxValue": extra[1], "value": extra[0], "stepSize": (extra[1] - extra[0]) / 20.0, "isFocusable": True}, fill, True)
        elif kind == "check":
            b.add("CheckBox", "C" + name, row, None, {"size": {"value": 0.44, "sizeRule": "Fill"}, "verticalAlignment": "VAlign_Center", "horizontalAlignment": "HAlign_Left"}, True)
        else:
            b.add("InputKeySelector", "C" + name, row, {"bAllowModifierKeys": False, "bAllowGamepadKeys": False}, fill, True)
        b.text("Val" + name, row, "", 18, slot={"size": {"value": 0.14, "sizeRule": "Fill"}, "verticalAlignment": "VAlign_Center", "padding": pad(14, 0, 0, 0)}, var=True, color=(0.75, 0.73, 0.66))
    foot = b.add("HorizontalBox", "Foot", sv, None, {"padding": pad(0, 14, 0, 0)})
    b.button("BtnSetBack", foot, "Back", 22)
    b.text("SetHint", foot, "Changes apply at once and are kept between launches.", 15, slot={"padding": pad(18, 0, 0, 0), "verticalAlignment": "VAlign_Center"}, color=(0.7, 0.68, 0.62))
    b.finish()
