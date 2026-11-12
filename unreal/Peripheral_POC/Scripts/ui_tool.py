#!/usr/bin/env python3
"""Host-side helpers for building menu widgets (UMG) through the editor's UMG toolset."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_tool import call
U = "UMGToolSet.UMGToolSet"; O = "editor_toolset.toolsets.object.ObjectTools"; A = "editor_toolset.toolsets.asset.AssetTools"
FONT = {"fontObject": {"refPath": "/Engine/EngineFonts/Roboto.Roboto"}, "fontMaterial": "None", "typefaceFontName": "Regular", "size": 20, "letterSpacing": 0, "skewAmount": 0,
        "bForceMonospaced": False, "bMaterialIsStencil": False, "monospacedWidth": 1,
        "outlineSettings": {"outlineSize": 0, "bMiteredCorners": False, "bSeparateFillAlpha": False, "bApplyOutlineToDropShadows": False, "outlineMaterial": "None", "outlineColor": {"r": 0, "g": 0, "b": 0, "a": 1}}}


def font(size, face="Regular"):
    f = dict(FONT); f["size"] = size; f["typefaceFontName"] = face; return f


def col(r, g, b, a=1.0):
    return {"specifiedColor": {"r": r, "g": g, "b": b, "a": a}, "colorUseRule": "UseColor_Specified"}


def pad(l, t=None, r=None, b=None):
    t = l if t is None else t
    return {"left": l, "top": t, "right": l if r is None else r, "bottom": t if b is None else b}


class Builder:
    def __init__(self, folder, name):
        self.path = "%s/%s.%s" % (folder, name, name); self.wb = {"refPath": self.path}; self.errors = []
        r = call(U, "CreateWidgetBlueprint", {"folderPath": folder, "assetName": name, "parentClass": {"refPath": "/Script/UMG.UserWidget"}})
        if "returnValue" not in r or not r["returnValue"]:
            print("create:", json.dumps(r)[:300])

    def setp(self, ref, values, what=""):
        r = call(O, "set_properties", {"instance": ref, "values": json.dumps(values)})
        if isinstance(r, dict) and r.get("isError"):
            self.errors.append((what, str(r)[:300]))

    def add(self, cls, name, parent=None, props=None, slot=None, var=False):
        r = call(U, "AddWidget", {"widgetBlueprint": self.wb, "widgetClass": {"refPath": "/Script/UMG." + cls}, "widgetDisplayName": name, "parentWidget": parent, "childIndex": -1})
        if "returnValue" not in r:
            self.errors.append((name, str(r)[:300])); return None
        w = r["returnValue"]
        if props: self.setp(w["widget"], props, name)
        if slot and isinstance(w["slot"], dict): self.setp(w["slot"], slot, name + " slot")
        if var: call(U, "ToggleWidgetAsVariable", {"widgetBlueprint": self.wb, "widget": w["widget"], "bIsVariable": True})
        return w["widget"]

    def text(self, name, parent, s, size=20, face="Regular", slot=None, var=False, color=(0.92, 0.9, 0.84), just="Left", wrap=0):
        p = {"text": s, "font": font(size, face), "colorAndOpacity": col(*color), "justification": just}
        if wrap: p.update({"autoWrapText": True, "wrapTextAt": wrap})
        return self.add("TextBlock", name, parent, p, slot, var)

    def button(self, name, parent, label, size=24, slot=None, width=None):
        b = self.add("Button", name, parent, {"backgroundColor": {"r": 0.05, "g": 0.05, "b": 0.06, "a": 0.85}, "isFocusable": True}, slot, True)
        self.text("Txt" + name, b, label, size, slot={"padding": pad(14, 6)})
        return b

    def finish(self):
        r = call(U, "CompileWidgetBlueprint", {"widgetBlueprint": self.wb})
        s = call(A, "save_asset", {"asset": self.wb}) if False else None
        print("compiled:", json.dumps(r)[:300], "| errors:", len(self.errors))
        for e in self.errors[:12]:
            print("  ", e)
