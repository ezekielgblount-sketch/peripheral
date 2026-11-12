#!/usr/bin/env python3
"""Writes Scripts/bp/day.dsl (BP_Day: the anomaly test day) and, with 'apply', creates its variables and writes the graph.
One in-game day: a clock, the sun crossing the sky, and anomalies fired at random, each only while its spot is out of the
player's view (outside the field of view, or behind a wall). Every one that fires is logged with its time; a later look at it is logged too.
Anomaly numbers: 0 family photo, 1 THANKFUL banner, 2 fridge magnet and drawing, 3 clocks, 4 parents' door ajar, 5 dishes back,
6 lawn strip long again, 7 television on, 8 dining chair pulled out, 9 a light back on, 10 hallway longer, 11 two coats,
12 answering machine, 13 height mark, 14 shoes by the door, 15 a fifth door upstairs, 16 the SOLD sign lost its smile,
17 wedding photo face-down, 18 a kitchen cabinet open, 19 a tap running, 20 the half-bath door wide open.
The list is as long as ShowTags: build_day.py decides how many there are."""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
V = lambda n: "(Variables|Default|Get%s)" % n
S = lambda n, v: "(Variables|Default|Set%s %s)" % (n, v)
LOC = lambda a: "(Transformation|GetActorLocation :self %s)" % a
VEC = lambda x, y, z: "(Math|Vector|MakeVector :X %s :Y %s :Z %s)" % (x, y, z)
GET = lambda arr, i: '(Utilities|Array|Get(acopy) :Array %s :"Dimension 1" %s)' % (arr, i)
SETEL = lambda arr, i, v: "(Utilities|Array|SetArrayElem :TargetArray %s :Index %s :Item %s)" % (arr, i, v)


def view(name, point):
    """Binds <name>d (distance), <name>a (angle off the view centre, degrees) and <name>b (a wall is in the way)."""
    return f"""(bind {name}t (- {point} camLoc))
    (bind {name}d (+ (Math|Vector|VectorLength :A {name}t) 0.001))
    (bind {name}a (Math|Trig|Acos(Degrees) :A (/ (Math|Vector|DotProduct :A fwd :B {name}t) {name}d)))
    (bind ({name}h {name}b) (Collision|LineTraceByChannel :Start camLoc :End (+ camLoc (* {name}t (/ (- {name}d 30.0) {name}d)))))"""


dsl = f"""(event EventBeginPlay
  (bind f_CB (Actor|GetAllActorswithTag :Tag "cb")) (for a_CB f_CB {S("CB", "a_CB")})
  (bind f_DB (Actor|GetAllActorswithTag :Tag "db")) (for a_DB f_DB {S("DB", "a_DB")})
  (bind f_SB (Actor|GetAllActorswithTag :Tag "sb")) (for a_SB f_SB {S("SB", "a_SB")})
  (bind f_Sun (Actor|GetAllActorswithTag :Tag "sun")) (for a_Sun f_Sun {S("Sun", "a_Sun")}))

(event EventTick (DeltaSeconds)
  (bind cbl {LOC(V("CB"))})
  (if (and (> (.y cbl) 0.5) (not {V("Running")}))
    {S("Running", "true")} {S("T", "0.0")} {S("TryT", "0.0")}
    {S("NextT", "(Math|Random|RandomFloatinRange :Min 25.0 :Max 45.0)")}
    (bind blk (Actor|GetAllActorswithTag :Tag "s_blocker"))
    (for b blk (Collision|SetActorEnableCollision :self b :bNewActorEnableCollision false)))
  (if {V("Running")}
    (bind t (+ {V("T")} DeltaSeconds))
    {S("T", "t")}
    (bind pcm (Game|GetPlayerCameraManager :PlayerIndex 0))
    (bind camLoc (Camera|GetCameraLocation :self pcm))
    (bind fwd (Math|Vector|GetForwardVector :InRot (Camera|GetCameraRotation :self pcm)))
    (bind edge (+ (* 0.5 (.x {LOC(V("SB"))})) 14.0))
    ; the sun crosses the sky over the length of the day
    (bind f (Math|Float|Clamp(Float) :Value (/ t {V("DayLen")}) :Min 0.0 :Max 1.0))
    (Transformation|SetActorRotation :self {V("Sun")} :NewRotation (Math|Rotator|MakeRotator :Roll 0.0
      :Pitch (- -16.0 (* 44.0 (Math|Trig|Sin(Radians) (* f 3.14159)))) :Yaw (- 205.0 (* 185.0 f))))
    (Transformation|SetActorLocation :self {V("DB")} :NewLocation {VEC(V("Mask"), "t", "(select " + V("Over") + " 1.0 0.0)")})
    ; has the player looked straight at anything that changed?
    (bind order {V("FiredOrder")})
    (for i (range (Utilities|Array|Length :TargetArray order))
      (bind idx {GET("order", "i")})
      (if (not {GET(V("Seen"), "idx")})
        {view("s", GET(V("Probes"), "idx"))}
        (if (and (and (< sa 20.0) (not sb)) (and (< sd 900.0) (> (- t {GET(V("FiredTime"), "i")}) 2.0)))
          {SETEL(V("Seen"), "idx", "true")})))
    (bind chores (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Chores.BP_Chores_C"))
    (for c chores {S("DishDone", "(Class|BPChores|GetD3 :self c)")} {S("MowDone", "(Class|BPChores|GetD0 :self c)")})
    (if (and (not {V("Over")}) (or (> (.x cbl) 510.5) (> t {V("DayLen")})))
      {S("Over", "true")}
      (Audio|PlaySound2D :Sound "/Game/Audio/click.click" :VolumeMultiplier 0.8))
    ; ---------------- try to fire one anomaly: only somewhere the player cannot see ----------------
    (if (and (and (not {V("Over")}) (> t {V("NextT")})) (> (- t {V("TryT")}) 1.0))
      {S("TryT", "t")}
      {S("R", "(Math|Random|RandomIntegerinRange :Min 0 :Max (- (Utilities|Array|Length :TargetArray " + V("ShowTags") + ") 1))")}
      (bind r {V("R")})
      {S("LightOK", "false")}
      (if (== r 9)
        (bind sws (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Switch.BP_Switch_C"))
        (for sw sws
          (if (not (Class|BPSwitch|GetOn :self sw))
            {view("l", LOC("sw"))}
            (if (and (> ld 300.0) (or (> la edge) lb))
              {S("LightCand", "sw")} {S("LightOK", "true")}
              {SETEL(V("Probes"), "9", LOC("sw"))}))))
      {view("p", GET(V("Probes"), "r"))}
      (bind unseen (and (> pd 250.0) (or (> pa edge) pb)))
      (bind ok (and (not {GET(V("IsFired"), "r")})
                 (and (select (== r 9) {V("LightOK")} unseen)
                      (and (or (!= r 5) {V("DishDone")}) (or (!= r 6) {V("MowDone")})))))
      (if ok
        {SETEL(V("IsFired"), "r", "true")}
        (Utilities|Array|Add :TargetArray {V("FiredOrder")} :NewItem r)
        (Utilities|Array|Add :TargetArray {V("FiredTime")} :NewItem t)
        {S("Mask", "(+ " + V("Mask") + " (Math|Float|Power :Base 2.0 :Exp (Math|Conversions|ToFloat(Integer) r)))")}
        {S("NextT", "(+ t (Math|Random|RandomFloatinRange :Min " + V("GapMin") + " :Max " + V("GapMax") + "))")}
        (switch int (select (== r 4) 0 (select (== r 5) 1 (select (== r 6) 2 (select (== r 9) 3 (select (== r 10) 4 (select (== r 20) 5 6))))))
          (:0 (bind doors (Actor|GetAllActorsOfClasswithTag :ActorClass "/Game/Blueprints/BP_Mover.BP_Mover_C" :Tag "s_pdoor"))
              (for d doors
                (bind cr (Class|BPMover|GetClosedRot :self d))
                (Class|BPMover|SetClosedRot :self d :ClosedRot (Math|Rotator|MakeRotator :Roll (.roll cr) :Pitch (.pitch cr) :Yaw (+ (.yaw cr) (* 0.15 (Class|BPMover|GetOpenYaw :self d)))))))
          (:1 (Transformation|SetActorLocation :self {V("CB")} :NewLocation {VEC("(.x cbl)", "(.y cbl)", "1.0")}))
          (:2 (Transformation|SetActorLocation :self {V("CB")} :NewLocation {VEC("(.x cbl)", "(.y cbl)", "2.0")}))
          (:3 (Class|BPSwitch|SetOn :self {V("LightCand")} :On true))
          (:4 (bind caps (Actor|GetAllActorswithTag :Tag "dy_hallcap"))
               (for cp caps (Transformation|SetActorLocation :self cp :NewLocation (+ {LOC("cp")} {VEC("0.0", "80.0", "0.0")}))))
          (:5 (bind bdoors (Actor|GetAllActorsOfClasswithTag :ActorClass "/Game/Blueprints/BP_Mover.BP_Mover_C" :Tag "dy_bdoor"))
              (for bd bdoors
                (bind br (Class|BPMover|GetClosedRot :self bd))
                (Class|BPMover|SetClosedRot :self bd :ClosedRot (Math|Rotator|MakeRotator :Roll (.roll br) :Pitch (.pitch br) :Yaw (+ (.yaw br) (* 0.92 (Class|BPMover|GetOpenYaw :self bd)))))))
          (:Default
            (bind show (Actor|GetAllActorswithTag :Tag {GET(V("ShowTags"), "r")}))
            (for a show (Rendering|SetActorHiddenInGame :self a :bNewHidden false))
            (bind hide (Actor|GetAllActorswithTag :Tag {GET(V("HideTags"), "r")}))
            (for h hide (Rendering|SetActorHiddenInGame :self h :bNewHidden true) (Collision|SetActorEnableCollision :self h :bNewActorEnableCollision false))))))))
"""
open(os.path.join(here, "day.dsl"), "w").write(dsl)
print("day.dsl written,", len(dsl.splitlines()), "lines")
if len(sys.argv) > 1 and sys.argv[1] == "apply":
    import bp_tool as B
    N = "BP_Day"
    def arr(name, t, struct=False):
        if struct:
            return B.call(B.BT, "add_struct_variable", {"blueprint": B.bp_ref(N), "name": name, "struct_type": {"refPath": t}, "graph": None, "container_type": "ARRAY"})
        return B.call(B.BT, "add_variable", {"blueprint": B.bp_ref(N), "name": name, "type_name": t, "graph": None, "container_type": "ARRAY"})
    for k in ("CB", "DB", "SB", "Sun"):
        B.add_obj_var(N, k, "/Script/Engine.Actor")
    B.add_obj_var(N, "LightCand", "/Game/Blueprints/BP_Switch.BP_Switch_C")
    arr("Probes", "Vector"); arr("ShowTags", "name"); arr("HideTags", "name"); arr("FiredOrder", "int"); arr("FiredTime", "float"); arr("Seen", "bool"); arr("IsFired", "bool")
    for k in ("T", "NextT", "TryT", "DayLen", "Mask", "GapMin", "GapMax"):
        B.add_var(N, k, "float")
    for k in ("Running", "Over", "LightOK", "DishDone", "MowDone"):
        B.add_var(N, k, "bool")
    B.add_var(N, "R", "int")
    for k in ("Probes", "ShowTags", "HideTags", "Seen", "IsFired", "DayLen", "GapMin", "GapMax"):
        B.call(B.BT, "set_variable_instance_editable", {"blueprint": B.bp_ref(N), "variable_name": k, "instance_editable": True})
    print(json.dumps(B.write(N, os.path.join(here, "day.dsl")))[:3000])
