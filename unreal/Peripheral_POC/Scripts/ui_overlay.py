#!/usr/bin/env python3
"""Builds the in-game overlay widget WBP_Overlay (chore list, clock, the F6 list of what has changed, captions) and its logic.
Run with the editor open: python3 Scripts/ui_overlay.py"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui_tool import Builder, col, pad, font
import bp_tool as B
from mcp_tool import call
CHORES = ["Mow the back lawn", "Take out the trash, bin to the curb", "Get the mail", "Do the dishes", "Run the laundry (washer, then dryer)",
          "Water the garden bed", "Sweep the garage", "Change the hall light bulb", "Make the bed in Jack's room"]
CAPTIONS = ["", "[lawn mower running]", "[washing machine running]", "[buzzer]", "[water pouring]", "[dishes clink in the sink]", "[the house groans]", "[a breaker clunks; the power hums]",
            "[doorbell]", "[knocking at the front door]", "[a phone rings]", "[answering machine beeps]", "[television static]", "[pipes knock]",
            "[a floorboard creaks]", "[footsteps overhead]"]
N_LOG = 15
CHORE_DAY = {0: 3, 1: 4, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 3, 8: 2}           # as in bp/gen_story.py
BUILD = "layout" in sys.argv
if BUILD:
  b = Builder("/Game/UI", "WBP_Overlay")
if BUILD:
  C = lambda l, t, r, bt, ax0, ay0, ax1, ay1, alx=0, aly=0: {"layoutData": {"offsets": {"left": l, "top": t, "right": r, "bottom": bt}, "anchors": {"minimum": {"x": ax0, "y": ay0}, "maximum": {"x": ax1, "y": ay1}}, "alignment": {"x": alx, "y": aly}}}
  root = b.add("CanvasPanel", "Root")
  cbx = b.add("Border", "ChoreBox", root, {"brushColor": {"r": 0, "g": 0, "b": 0, "a": 0.42}, "padding": pad(16, 12)}, C(-30, 30, 430, 380, 1, 0, 1, 0, 1, 0), True)
  cv = b.add("VerticalBox", "ChoreV", cbx)
  b.text("Clock", cv, "8:00", 22, "Bold", {"padding": pad(0, 0, 0, 6)}, var=True)
  for i, c in enumerate(CHORES):
      b.text("Ch%d" % i, cv, c, 16, slot={"padding": pad(0, 2)}, var=True)
  b.text("ChHint", cv, "E: use, pick up, push.   F6: what has changed.", 12, slot={"padding": pad(0, 8, 0, 0)}, color=(0.7, 0.68, 0.62))
  lbx = b.add("Border", "LogBox", root, {"brushColor": {"r": 0.02, "g": 0.02, "b": 0.03, "a": 0.86}, "padding": pad(22, 16)}, C(40, 40, 760, 560, 0, 0, 0, 0), True)
  lv = b.add("VerticalBox", "LogV", lbx)
  b.text("LogTitle", lv, "What has changed so far  (F6 hides this)", 22, "Bold", {"padding": pad(0, 0, 0, 10)})
  for i in range(N_LOG):
      b.text("Lg%d" % i, lv, "", 16, slot={"padding": pad(0, 2)}, var=True)
  b.text("LogFoot", lv, "Each change happened while that spot was out of your view.", 12, slot={"padding": pad(0, 10, 0, 0)}, color=(0.7, 0.68, 0.62))
  b.text("DayOver", root, "The day is over.  F6 shows what changed and whether you looked at it.", 22, "Bold", C(0, 90, 900, 40, 0.5, 0, 0.5, 0, 0.5, 0), var=True, just="Center")
  b.text("Caption", root, "", 22, slot=C(0, -120, 1000, 40, 0.5, 1, 0.5, 1, 0.5, 0), var=True, just="Center")
  b.text("Note", root, "", 24, "Italic", C(46, -130, 900, 80, 0, 1, 0, 1, 0, 0), var=True, color=(0.93, 0.9, 0.82), wrap=860)
  b.text("Card", root, "", 54, "Bold", C(0, -40, 1400, 90, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5), var=True, just="Center")
  b.finish()

W = lambda n: "(Variables|WBP_Overlay|Get%s)" % n
V = lambda n: "(Variables|Default|Get%s)" % n
S = lambda n, v: "(Variables|Default|Set%s %s)" % (n, v)
LOC = lambda a: "(Transformation|GetActorLocation :self %s)" % a
VIS = lambda w, cond: '(if %s (Widget|SetVisibility :self %s :InVisibility "HitTestInvisible") (else (Widget|SetVisibility :self %s :InVisibility "Collapsed")))' % (cond, w, w)
STR = lambda w, s: "(Widget|SetText(Text) :self %s :InText (Utilities|Text|ToText(String) :InString %s))" % (w, s)
APP = lambda a, b_: "(Utilities|String|Append :A %s :B %s)" % (a, b_)
ISTR = lambda e: "(Utilities|String|ToString(Integer) :InInt %s)" % e
GET = lambda arr, i: '(Utilities|Array|Get(acopy) :Array %s :"Dimension 1" %s)' % (arr, i)


def clock(sec):
    """A day runs 8:00 to 18:00 over DayLen seconds: text like 9:05."""
    mf = "(+ 480.0 (* (/ %s daylen) 600.0))" % sec
    h = "(Math|Float|Truncate :A (/ %s 60.0))" % mf
    mm = "(Math|Float|Truncate :A (- %s (* 60.0 (Math|Conversions|ToFloat(Integer) %s))))" % (mf, h)
    return APP(APP(ISTR(h), '":"'), APP('(select (< %s 10) "0" "")' % mm, ISTR(mm)))


def pick(idx, vals):
    e = '"%s"' % vals[-1]
    for i in range(len(vals) - 2, -1, -1):
        e = '(select (== %s %d) "%s" %s)' % (idx, i, vals[i], e)
    return e


finds = "\n  ".join('(bind f_%s (Actor|GetAllActorswithTag :Tag "%s")) (for a_%s f_%s %s)' % (k, t, k, k, S(k, "a_" + k)) for k, t in (("CB", "cb"), ("DB", "db"), ("CP", "cp")))
chores = "\n    ".join(STR(W("Ch%d" % i), APP('(select (Class|BPChores|GetD%d :self ch) "[x]  " "[  ]  ")' % i, '"%s"' % c)) for i, c in enumerate(CHORES))
logs = "\n    ".join("(if (> n %d) %s (else %s))" % (i, STR(W("Lg%d" % i), APP(APP(clock(GET("times", str(i))), '"    "'), APP(GET("names", GET("order", str(i))),
        '(select %s "     -  looked at since: yes" "     -  looked at since: no")' % GET("seen", GET("order", str(i)))))), STR(W("Lg%d" % i), '""')) for i in range(N_LOG))
dsl = f"""(event UserInterface|EventConstruct
  {finds}
  (bind days (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Day.BP_Day_C"))
  (for d days {S("DayRef", "d")})
  (bind chs (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Chores.BP_Chores_C"))
  (for c chs {S("ChoreRef", "c")})
  (bind sts (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Story.BP_Story_C"))
  (for st0 sts {S("StoryRef", "st0")}))

(event UserInterface|EventTick (MyGeometry InDeltaTime)
  (bind cbl {LOC(V("CB"))})
  (bind dbl {LOC(V("DB"))})
  (bind cpl {LOC(V("CP"))})
  (bind active (> (.y cbl) 0.5))
  (bind over (> (.z dbl) 0.5))
  (bind day {V("DayRef")})
  (bind ch {V("ChoreRef")})
  (bind daylen (Class|BPDay|GetDayLen :self day))
  (if (Game|Player|WasInputKeyJustPressed :self (Widget|GetOwningPlayer) :Key "F6") {S("ShowLog", "(not " + V("ShowLog") + ")")})
  (if (and over (not {V("WasOver")})) {S("WasOver", "true")} {S("ShowLog", "true")})
  (bind st {V("StoryRef")})
  (bind sday (Class|BPStory|GetDay :self st))
  {VIS(W("ChoreBox"), "(and active (or (== sday 0) (and (and (>= sday 2) (<= sday 4)) (== (Class|BPStory|GetPhase :self st) 1))))")}
  {VIS(W("LogBox"), "(and active " + V("ShowLog") + ")")}
  {VIS(W("DayOver"), "(and over (== sday 0))")}
  {VIS(W("Clock"), "(== sday 0)")}
  {VIS(W("Card"), "(> (Class|BPStory|GetCardT :self st) 0.0)")}
  {STR(W("Card"), "(Class|BPStory|GetCard :self st)")}
  {STR(W("Note"), APP("(Class|BPStory|GetNote :self st)", '(select (Class|BPStory|GetLoopOn :self st) ' + APP(APP('"     something changed: go back the way you came. nothing changed: keep going.   "', ISTR("(Class|BPStory|GetCount :self st)")), APP('" of "', ISTR("(Class|BPStory|GetNeed :self st)"))) + ' "")'))}
  {" ".join(VIS(W("Ch%d" % i), "(or (== sday 0) (== sday %d))" % CHORE_DAY[i]) for i in range(len(CHORES)))}
  (bind now (Utilities|Time|GetGameTimeinSeconds))
  (bind cap (Math|Float|Round :A (.x cpl)))
  {VIS(W("Caption"), "(and (> (.z cpl) 0.5) (and (> cap 0) (< (- now (.y cpl)) 3.5)))")}
  {STR(W("Caption"), pick("cap", CAPTIONS))}
  (if active
    {STR(W("Clock"), clock("(.y dbl)"))}
    {chores})
  (if (and active {V("ShowLog")})
    (bind order (Class|BPDay|GetFiredOrder :self day))
    (bind times (Class|BPDay|GetFiredTime :self day))
    (bind seen (Class|BPDay|GetSeen :self day))
    (bind names (Class|BPDay|GetNames :self day))
    (bind n (Utilities|Array|Length :TargetArray order))
    {logs}))
"""
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bp", "overlay.dsl"), "w").write(dsl)
WB = {"refPath": "/Game/UI/WBP_Overlay.WBP_Overlay"}
call(B.BT, "add_variable", {"blueprint": B.bp_ref("BP_Day"), "name": "Names", "type_name": "string", "graph": None, "container_type": "ARRAY"})
call(B.BT, "set_variable_instance_editable", {"blueprint": B.bp_ref("BP_Day"), "variable_name": "Names", "instance_editable": True})
print("day compile:", json.dumps(call(B.BT, "compile_blueprint", {"blueprint": B.bp_ref("BP_Day"), "warnings_as_errors": False}))[:200])
for k in ("CB", "DB", "CP"):
    call(B.BT, "add_object_variable", {"blueprint": WB, "name": k, "object_class": {"refPath": "/Script/Engine.Actor"}, "graph": None, "container_type": None})
call(B.BT, "add_object_variable", {"blueprint": WB, "name": "DayRef", "object_class": {"refPath": "/Game/Blueprints/BP_Day.BP_Day_C"}, "graph": None, "container_type": None})
call(B.BT, "add_object_variable", {"blueprint": WB, "name": "StoryRef", "object_class": {"refPath": "/Game/Blueprints/BP_Story.BP_Story_C"}, "graph": None, "container_type": None})
call(B.BT, "add_object_variable", {"blueprint": WB, "name": "ChoreRef", "object_class": {"refPath": "/Game/Blueprints/BP_Chores.BP_Chores_C"}, "graph": None, "container_type": None})
for k in ("ShowLog", "WasOver"):
    call(B.BT, "add_variable", {"blueprint": WB, "name": k, "type_name": "bool", "graph": None, "container_type": None})
print(json.dumps(call(B.BT, "write_graph_dsl", {"graph": {"refPath": "/Game/UI/WBP_Overlay.WBP_Overlay:EventGraph"}, "code": dsl}))[:2500])
