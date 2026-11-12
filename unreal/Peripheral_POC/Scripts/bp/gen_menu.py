#!/usr/bin/env python3
"""Writes Scripts/bp/menu.dsl (the logic of the menu widget WBP_Menu) and, with 'apply', binds its buttons and writes the graph.
Screens come from the menu board (tag ub): X = 1 title, 2 pause, 3 settings, 4 how to play; a button writes its command to Y for
the director to act on. Settings live in a save object (slot "settings"), are applied at start-up and whenever a control moves,
and are written to disk when the settings screen closes."""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
from ui_menu import ROWS, PAGES
W = lambda n: "(Variables|WBP_Menu|Get%s)" % n
V = lambda n: "(Variables|Default|Get%s)" % n
S = lambda n, v: "(Variables|Default|Set%s %s)" % (n, v)
SG = lambda n: "(Class|BPSaveSettings|Get%s :self sv)" % n
SS = lambda n, v: "(Class|BPSaveSettings|Set%s :self sv :%s %s)" % (n, n, v)
LOC = lambda a: "(Transformation|GetActorLocation :self %s)" % a
VEC = lambda x, y, z: "(Math|Vector|MakeVector :X %s :Y %s :Z %s)" % (x, y, z)
SETLOC = lambda a, v: "(Transformation|SetActorLocation :self %s :NewLocation %s)" % (a, v)
VIS = lambda w, cond: '(if %s (Widget|SetVisibility :self %s :InVisibility "Visible") (else (Widget|SetVisibility :self %s :InVisibility "Collapsed")))' % (cond, w, w)
TXT = lambda w, t: "(Widget|SetText(Text) :self %s :InText %s)" % (w, t)
INT = lambda e: "(Utilities|Text|ToText(Integer) :Value %s)" % e
GUSQ = dict(Shadows="ShadowQuality", GI="GlobalIlluminationQuality", Refl="ReflectionQuality", Tex="TextureQuality", Fx="VisualEffectQuality", Post="PostProcessingQuality", AA="AntiAliasingQuality")
GUS_ROWS = ("WinMode", "Res", "VSync", "FpsCap", "Scale") + tuple(GUSQ)
PCT = ("Master", "Music", "Sfx", "Amb", "Motion", "Cap")
RES = [(1280, 720), (1600, 900), (1920, 1080), (2560, 1440), (3024, 1964), (3840, 2160)]


def pick(idx, vals):
    e = str(vals[-1])
    for i in range(len(vals) - 2, -1, -1):
        e = "(select (== %s %d) %s %s)" % (idx, i, vals[i], e)
    return e


push, read = [], []
for (name, page, label, kind, extra) in ROWS:
    c = W("C" + name)
    if kind == "combo":
        push.append("(ComboBox|SetSelectedIndex :self %s :Index %s)" % (c, SG(name)))
        body = [SS(name, "i_" + name)]
        if name in GUS_ROWS: body.append(S("GusDirty", "true"))
        if name == "Preset":
            body.append("(if (< i_Preset 4) %s)" % " ".join("(ComboBox|SetSelectedIndex :self %s :Index i_Preset)" % W("C" + q) for q in GUSQ))
        read.append("(bind i_%s (ComboBox|GetSelectedIndex :self %s))\n      (if (!= i_%s %s) %s)" % (name, c, name, SG(name), " ".join(body)))
    elif kind == "slider":
        push.append("(Class|Slider|SetValue :self %s :Value %s)" % (c, SG(name)))
        body = [SS(name, "f_" + name)] + ([S("GusDirty", "true")] if name in GUS_ROWS else [])
        shown = "(Math|Float|Round :A (* f_%s 100.0))" % name if name in PCT or name == "Sens" else "(Math|Float|Round :A f_%s)" % name
        read.append("(bind f_%s (Class|Slider|GetValue :self %s))\n      (if (!= f_%s %s) %s)\n      %s" % (name, c, name, SG(name), " ".join(body), TXT(W("Val" + name), INT(shown))))
    elif kind == "check":
        push.append("(Widget|SetIsChecked :self %s :InIsChecked %s)" % (c, SG(name)))
        body = [SS(name, "b_" + name)] + ([S("GusDirty", "true")] if name in GUS_ROWS else [])
        read.append("(bind b_%s (Widget|IsChecked :self %s))\n      (if (!= b_%s %s) %s)" % (name, c, name, SG(name), " ".join(body)))
    else:
        push.append("(Widget|SetSelectedKey :self %s :InSelectedKey (Utilities|Struct|MakeInputChord :Key %s :bShift false :bCtrl false :bAlt false :bCmd false))" % (c, SG(name)))
        read.append("(bind (k_%s s1_%s s2_%s s3_%s s4_%s) (Utilities|Struct|BreakInputChord :InputChord (Class|InputKeySelector|GetSelectedKey :self %s)))\n      %s\n      (Class|BPPlayer|Set%s :self pl :%s k_%s)"
                    % (name, name, name, name, name, c, SS(name, "k_" + name), name, name, name))
keys_to_player = " ".join("(Class|BPPlayer|Set%s :self pl :%s %s)" % (n, n, SG(n)) for n in ("KFwd", "KBack", "KLeft", "KRight", "KUse", "KCrouch", "KLight"))
gus = "\n      ".join(["(bind gus (Settings|GetGameUserSettings))", "(bind wm %s)" % SG("WinMode"),
    '(if (== wm 0) (Settings|SetFullscreenMode :self gus :InFullscreenMode "Windowed") (elif (== wm 1) (Settings|SetFullscreenMode :self gus :InFullscreenMode "WindowedFullscreen") (else (Settings|SetFullscreenMode :self gus :InFullscreenMode "Fullscreen"))))',
    "(bind ri %s)" % SG("Res"),
    "(Settings|SetScreenResolution :self gus :Resolution (Utilities|Struct|MakeIntPoint :X %s :Y %s))" % (pick("ri", [r[0] for r in RES]), pick("ri", [r[1] for r in RES])),
    "(Settings|SetVSyncEnabled :self gus :bEnable %s)" % SG("VSync"),
    "(Settings|SetFrameRateLimit :self gus :NewLimit %s)" % pick(SG("FpsCap"), ["30.0", "60.0", "120.0", "0.0"]),
    "(Settings|SetResolutionScaleNormalized :self gus :NewScaleNormalized (/ %s 100.0))" % SG("Scale")]
    + ["(Settings|Set%s :self gus :Value %s)" % (fn, SG(n)) for n, fn in GUSQ.items()]
    + ["(Settings|ApplySettings :self gus :bCheckForCommandLineOverrides false)", S("GusDirty", "false")])
mix = " ".join('(Audio|SetSoundMixClassOverride :InSoundMixModifier "/Game/Audio/Mix_Settings.Mix_Settings" :InSoundClass "/Game/Audio/SC_%s.SC_%s" :Volume (* %s %s) :Pitch 1.0 :FadeInTime 0.05 :bApplyToChildren true)'
               % (c, c, SG("Master"), SG(v)) for c, v in (("Music", "Music"), ("SFX", "Sfx"), ("Ambience", "Amb")))
finds = "\n  ".join('(bind f_%s (Actor|GetAllActorswithTag :Tag "%s")) (for a_%s f_%s %s)' % (k, t, k, k, S(k, "a_" + k)) for k, t in (("UB", "ub"), ("BB", "bb"), ("SB", "sb"), ("CP", "cp"), ("QB", "qb")))
BTN = {"BtnDay1": 1, "BtnChore": 2, "BtnLoop": 3, "BtnResume": 4, "BtnTitle": 5, "BtnQuit": 6, "BtnPQuit": 6}
events = []
for b_, cmd in BTN.items():
    events.append("(event OnClicked(%s)\n  (bind l %s)\n  %s)" % (b_, LOC(V("UB")), SETLOC(V("UB"), VEC("(.x l)", "%d.0" % cmd, "(.z l)"))))
for b_, scr in (("BtnSettings", 3), ("BtnPSettings", 3), ("BtnHow", 4), ("BtnPHow", 4), ("BtnChapters", 5), ("BtnPChapters", 5)):
    events.append("(event OnClicked(%s)\n  (bind l %s)\n  %s)" % (b_, LOC(V("UB")), SETLOC(V("UB"), VEC("%d.0" % scr, "0.0", "(.x l)"))))
for b_ in ("BtnSetBack", "BtnHowBack", "BtnChapBack"):
    events.append("(event OnClicked(%s)\n  (bind l %s)\n  %s)" % (b_, LOC(V("UB")), SETLOC(V("UB"), VEC("(.z l)", "0.0", "(.z l)"))))
for i in range(len(PAGES)):
    events.append("(event OnClicked(BtnTab%d)\n  %s)" % (i, S("Page", str(i))))
REQ = {"BtnContinue": 9, "BtnDay_1": 1, "BtnDay_2": 2, "BtnDay_3": 3, "BtnDay_4": 4, "BtnDay_5": 5}
for b_, q in REQ.items():          # the story controller picks these up from the request board
    events.append("(event OnClicked(%s)\n  %s)" % (b_, SETLOC(V("QB"), VEC("%d.0" % q, "0.0", "0.0"))))
ALLBTN = list(BTN) + list(REQ) + ["BtnSettings", "BtnPSettings", "BtnHow", "BtnPHow", "BtnSetBack", "BtnHowBack", "BtnChapters", "BtnPChapters", "BtnChapBack"] + ["BtnTab%d" % i for i in range(len(PAGES))]

dsl = f"""(event UserInterface|EventConstruct
  {finds}
  (if (not (SaveGame|DoesSaveGameExist :SlotName "settings" :UserIndex 0))
    (SaveGame|SaveGametoSlot :SaveGameObject (SaveGame|CreateSaveGameObject :SaveGameClass "/Game/Blueprints/BP_SaveSettings.BP_SaveSettings_C") :SlotName "settings" :UserIndex 0))
  (bind sv0 (Utilities|Casting|CastToBP_SaveSettings :Object (SaveGame|LoadGamefromSlot :SlotName "settings" :UserIndex 0))
    (:then {S("Save", "sv0")} {S("Ready", "true")})
    (:CastFailed)))

(event UserInterface|EventTick (MyGeometry InDeltaTime)
  (bind ub {V("UB")})
  (bind ubl {LOC("ub")})
  (bind screen (Math|Float|Round :A (.x ubl)))
  {VIS(W("TitleBox"), "(== screen 1)")}
  {VIS(W("PauseBox"), "(== screen 2)")}
  {VIS(W("SettingsBox"), "(== screen 3)")}
  {VIS(W("HowBox"), "(== screen 4)")}
  {VIS(W("ChapterBox"), "(== screen 5)")}
  {VIS(W("Dim"), "(> screen 1)")}
  (bind page {V("Page")})
  {" ".join(VIS(W("Page%d" % i), "(== page %d)" % i) for i in range(len(PAGES)))}
  ; keyboard and controller: give the first button of a screen the focus when that screen opens
  (bind last {V("LastScreen")})
  (if (!= screen last)
    {S("LastScreen", "screen")}
    (if (== screen 1) (Widget|SetFocus :self {W("BtnDay1")}))
    (if (== screen 2) (Widget|SetFocus :self {W("BtnResume")}))
    (if (== screen 3) (Widget|SetFocus :self {W("BtnTab0")}))
    (if (== screen 4) (Widget|SetFocus :self {W("BtnHowBack")}))
    (if (and (== last 3) {V("Inited")})
      (SaveGame|SaveGametoSlot :SaveGameObject {V("Save")} :SlotName "settings" :UserIndex 0)))
  (if (and {V("Ready")} {V("HavePlayer")})
    (bind sv {V("Save")})
    (bind pl {V("PlayerRef")})
    (if (not {V("Inited")})
      ; first frame: put the saved values on the controls and switch them all on
      {(chr(10) + "      ").join(push)}
      (Audio|PushSoundMixModifier :InSoundMixModifier "/Game/Audio/Mix_Settings.Mix_Settings")
      {keys_to_player}
      {S("GusDirty", "true")}
      {S("Inited", "true")})
    (if (== screen 3)
      {(chr(10) + "      ").join(read)})
    (if (or (== screen 3) (< (Utilities|Time|GetGameTimeinSeconds) 2.0))
      ; cheap ones are simply written every frame while the settings are open
      (bind bbl {LOC(V("BB"))})
      {SETLOC(V("BB"), VEC(SG("Motion"), SG("Sens"), "(.z bbl)"))}
      {SETLOC(V("SB"), VEC(SG("Fov"), "(select " + SG("Invert") + " -1.0 1.0)", SG("Cap")))}
      (bind cpl {LOC(V("CP"))})
      {SETLOC(V("CP"), VEC("(.x cpl)", "(.y cpl)", "(select " + SG("Subs") + " 1.0 0.0)"))}
      {mix})
    (if {V("GusDirty")}
      {gus}))
  (if (not {V("HavePlayer")})
    (bind pl0 (Utilities|Casting|CastToBP_Player :Object (Player|GetOwningPlayerPawn))
      (:then {S("PlayerRef", "pl0")} {S("HavePlayer", "true")})
      (:CastFailed))))

{(chr(10) + chr(10)).join(events)}
"""
open(os.path.join(here, "menu.dsl"), "w").write(dsl)
print("menu.dsl written,", len(dsl.splitlines()), "lines")
if len(sys.argv) > 1 and sys.argv[1] == "apply":
    import bp_tool as B
    from mcp_tool import call
    WB = {"refPath": "/Game/UI/WBP_Menu.WBP_Menu"}
    for k in ("UB", "BB", "SB", "CP", "QB"):
        call(B.BT, "add_object_variable", {"blueprint": WB, "name": k, "object_class": {"refPath": "/Script/Engine.Actor"}, "graph": None, "container_type": None})
    call(B.BT, "add_object_variable", {"blueprint": WB, "name": "Save", "object_class": {"refPath": "/Game/Blueprints/BP_SaveSettings.BP_SaveSettings_C"}, "graph": None, "container_type": None})
    call(B.BT, "add_object_variable", {"blueprint": WB, "name": "PlayerRef", "object_class": {"refPath": "/Game/Blueprints/BP_Player.BP_Player_C"}, "graph": None, "container_type": None})
    for k in ("Ready", "Inited", "GusDirty", "HavePlayer"):
        call(B.BT, "add_variable", {"blueprint": WB, "name": k, "type_name": "bool", "graph": None, "container_type": None})
    for k in ("Page", "LastScreen"):
        call(B.BT, "add_variable", {"blueprint": WB, "name": k, "type_name": "int", "graph": None, "container_type": None})
    for b_ in ALLBTN:
        r = call("UMGToolSet.UMGToolSet", "BindToEventProperty", {"widgetBlueprint": WB, "eventName": "OnClicked", "propertyName": b_, "propertyClass": {"refPath": "/Script/UMG.Button"}})
        if not (isinstance(r, dict) and r.get("returnValue")): print("bind", b_, json.dumps(r)[:200])
    r = call(B.BT, "write_graph_dsl", {"graph": {"refPath": "/Game/UI/WBP_Menu.WBP_Menu:EventGraph"}, "code": dsl})
    print(json.dumps(r)[:3000])
