#!/usr/bin/env python3
"""Writes Scripts/bp/paranoia.dsl (BP_Paranoia: small sounds from somewhere else in the house) and, with 'apply', creates the
small Blueprints of the second anomaly pass (BP_Glimpse, BP_OnlyMirror, BP_Paranoia) and the home video's switch (BP_Video) and writes their graphs.
BP_Paranoia runs only while an anomaly day is running (BP_Day). Every GapMin..GapMax seconds it plays one sound at a place
that is at least 6 m from Jack: the doorbell and a knock at the front door, the phone and the answering machine where they
stand, a burst from the television, and pipes, floorboards and footsteps at one of the spots it was given. One more event has no
sound: the lit lamps near him go dark for a third of a second."""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
V = lambda n: "(Variables|Default|Get%s)" % n
S = lambda n, v: "(Variables|Default|Set%s %s)" % (n, v)
GET = lambda arr, i: '(Utilities|Array|Get(acopy) :Array %s :"Dimension 1" %s)' % (arr, i)
# sound, volume, caption number (see ui_overlay.CAPTIONS), fixed place (index into Fixed) or None for a roaming spot
EVENTS = [("doorbell", 0.9, 8, 0), ("door_knock", 0.9, 9, 0), ("phone_ring", 0.8, 10, 1), ("machine_beep", 0.7, 11, 1), ("tv_burst", 0.7, 12, 2),
          ("pipe_knock", 0.9, 13, None), ("floor_creak", 0.9, 14, None), ("steps_above", 1.0, 15, None), ("floor_creak", 0.7, 14, None), ("pipe_knock", 0.7, 13, None),
          ("gravel_steps", 1.0, 16, 3), ("porch_creak", 0.9, 17, 0), ("door_close", 1.0, 18, None), ("water_drip", 0.8, 19, None)]


def case(i, e):
    snd, vol, cap, fixed = e
    where = GET(V("Fixed"), fixed) if fixed is not None else "spot"
    return f"""(:{i} (if (> (Math|Vector|VectorLength :A (- {where} camLoc)) 600.0)
          (Audio|PlaySoundatLocation :Sound "/Game/Audio/{snd}.{snd}" :Location {where} :VolumeMultiplier {vol} :AttenuationSettings "/Game/Audio/ATT_House.ATT_House")
          (Transformation|SetActorLocation :self {V("CP")} :NewLocation (Math|Vector|MakeVector :X {cap}.0 :Y now :Z (.z cpl)))
          {S("NextT", "(+ t (Math|Random|RandomFloatinRange :Min " + V("GapMin") + " :Max " + V("GapMax") + "))")}))"""


dsl = f"""(event EventBeginPlay
  (bind f_CP (Actor|GetAllActorswithTag :Tag "cp")) (for a_CP f_CP {S("CP", "a_CP")})
  (bind f_D (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Day.BP_Day_C")) (for a_D f_D {S("DayRef", "a_D")})
  {S("NextT", "40.0")})

(event EventTick (DeltaSeconds)
  (if (> {V("FlickT")} 0.0)
    {S("FlickT", "(- " + V("FlickT") + " DeltaSeconds)")}
    (if (<= {V("FlickT")} 0.0)
      (bind sws2 (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Switch.BP_Switch_C"))
      (for sw2 sws2 (Class|BPSwitch|SetShown :self sw2 :Shown -1))))
  (bind dr {V("DayRef")})
  (if (and (Class|BPDay|GetRunning :self dr) (not (Class|BPDay|GetOver :self dr)))
    (bind t (+ {V("T")} DeltaSeconds))
    {S("T", "t")}
    (if (> t {V("NextT")})
      {S("NextT", "(+ t 4.0)")}
      (bind pcm (Game|GetPlayerCameraManager :PlayerIndex 0))
      (bind camLoc (Camera|GetCameraLocation :self pcm))
      (bind now (Utilities|Time|GetGameTimeinSeconds))
      (bind cpl (Transformation|GetActorLocation :self {V("CP")}))
      (bind spots {V("Spots")})
      (bind spot {GET("spots", "(Math|Random|RandomIntegerinRange :Min 0 :Max (- (Utilities|Array|Length :TargetArray spots) 1))")})
      (switch int (Math|Random|RandomIntegerinRange :Min 0 :Max {len(EVENTS)})
        {chr(10).join("        " + case(i, e) for i, e in enumerate(EVENTS))}
        ; the lights near him dip: every lit lamp within 7 m goes dark for a third of a second (its switch puts it back)
        (:{len(EVENTS)} (bind sws (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Switch.BP_Switch_C"))
          (for sw sws
            (if (and (Class|BPSwitch|GetOn :self sw) (< (Math|Vector|VectorLength :A (- (Transformation|GetActorLocation :self sw) camLoc)) 700.0))
              (bind grp (Actor|GetAllActorswithTag :Tag (Class|BPSwitch|GetGroup :self sw)))
              (for ga grp (Rendering|SetActorHiddenInGame :self ga :bNewHidden true))))
          {S("FlickT", "0.33")}
          {S("NextT", "(+ t (Math|Random|RandomFloatinRange :Min " + V("GapMin") + " :Max " + V("GapMax") + "))")})))))
"""
open(os.path.join(here, "paranoia.dsl"), "w").write(dsl)
print("paranoia.dsl written,", len(dsl.splitlines()), "lines")
if len(sys.argv) > 1 and sys.argv[1] == "apply":
    import bp_tool as B
    SMA = "/Script/Engine.StaticMeshActor"
    def arr(n, name, t):
        return B.call(B.BT, "add_variable", {"blueprint": B.bp_ref(n), "name": name, "type_name": t, "graph": None, "container_type": "ARRAY"})
    def editable(n, *ks):
        for k in ks:
            B.call(B.BT, "set_variable_instance_editable", {"blueprint": B.bp_ref(n), "variable_name": k, "instance_editable": True})
    which = sys.argv[2:] or ["BP_Glimpse", "BP_OnlyMirror", "BP_Paranoia", "BP_Video", "BP_Hint", "BP_Passer"]
    if "BP_Passer" in which:
        print(B.create("BP_Passer", SMA))
        for k in ("T", "Cool", "Time", "Range", "MinDist"):
            B.add_var("BP_Passer", k, "float")
        B.add_var("BP_Passer", "Moving", "bool"); B.add_var("BP_Passer", "A", "Vector"); B.add_var("BP_Passer", "B", "Vector")
        editable("BP_Passer", "B", "Time", "Range", "MinDist")
        print(json.dumps(B.write("BP_Passer", os.path.join(here, "passer.dsl")))[:1500])
    if "BP_Hint" in which:
        print(B.create("BP_Hint", "/Script/Engine.PointLight"))
        B.add_obj_var("BP_Hint", "HudRef", "/Game/Blueprints/BP_HUD.BP_HUD_C")
        for k in ("Marker", "Door", "Fridge", "PDoor", "Bed"):
            B.add_obj_var("BP_Hint", k, "/Script/Engine.Actor")
        print(json.dumps(B.write("BP_Hint", os.path.join(here, "hint.dsl")))[:1500])
    if "BP_Video" in which:
        print(B.create("BP_Video", SMA))
        B.add_var("BP_Video", "On", "bool"); B.add_obj_var("BP_Video", "StoryRef", "/Game/Blueprints/BP_Story.BP_Story_C")
        print(json.dumps(B.write("BP_Video", os.path.join(here, "video.dsl")))[:1500])
    if "BP_Glimpse" in which:
        print(B.create("BP_Glimpse", SMA))
        for k in ("Range", "MinDist", "T", "Cool"):
            B.add_var("BP_Glimpse", k, "float")
        B.add_var("BP_Glimpse", "Up", "bool"); editable("BP_Glimpse", "Range", "MinDist")
        print(json.dumps(B.write("BP_Glimpse", os.path.join(here, "glimpse.dsl")))[:1500])
    if "BP_OnlyMirror" in which:
        print(B.create("BP_OnlyMirror", SMA))
        print(json.dumps(B.write("BP_OnlyMirror", os.path.join(here, "onlymirror.dsl")))[:1500])
    if "BP_Paranoia" in which:
        print(B.create("BP_Paranoia", SMA))
        for k in ("T", "NextT", "GapMin", "GapMax", "FlickT"):
            B.add_var("BP_Paranoia", k, "float")
        B.add_obj_var("BP_Paranoia", "CP", "/Script/Engine.Actor"); B.add_obj_var("BP_Paranoia", "DayRef", "/Game/Blueprints/BP_Day.BP_Day_C")
        arr("BP_Paranoia", "Spots", "Vector"); arr("BP_Paranoia", "Fixed", "Vector"); editable("BP_Paranoia", "Spots", "Fixed", "GapMin", "GapMax")
        print(json.dumps(B.write("BP_Paranoia", os.path.join(here, "paranoia.dsl")))[:3000])
