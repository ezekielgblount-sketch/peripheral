#!/usr/bin/env python3
"""Writes Scripts/bp/story.dsl (BP_Story: the five-day arc) and, with 'apply', creates its variables and writes the graph.

BP_Story sits on top of the pieces that already exist and only steers them:
  the director (BP_HUD) for fades, unease and Day One; BP_Chores for the chores; BP_Day for out-of-sight anomalies;
  BP_Loop for the corridor loop. It never moves the player except to stand him up beside his bed each morning.
Day (0 = not in the story) and Phase:
  1 day running (chores)   2 the day's event (loops)   3 a second loop (day 4)   5 go to bed   10 night (fade, card, autosave)
  6 the parents' room (day 5)   7 the climax   8 the ending (unpack, the photo)   9 over
Chores by day: day 2 bed, dishes, mail, laundry; day 3 mow, water, bulb; day 4 trash, sweep."""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
CHORE_DAY = {0: 3, 1: 4, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 3, 8: 2}           # chore number -> the day it is on the list
UNEASE = {2: (10, 30), 3: (30, 50), 4: (50, 80), 5: (80, 100)}
GAPS = {2: (70, 120), 3: (45, 80), 4: (30, 60), 5: (25, 45)}
CARDS = {2: "Day 2   -   Settling in", 3: "Day 3   -   Things move", 4: "Day 4   -   Losing grip", 5: "Day 5   -   Facing it"}
V = lambda n: "(Variables|Default|Get%s)" % n
S = lambda n, v: "(Variables|Default|Set%s %s)" % (n, v)
LOC = lambda a: "(Transformation|GetActorLocation :self %s)" % a
VEC = lambda x, y, z: "(Math|Vector|MakeVector :X %s :Y %s :Z %s)" % (x, y, z)
SETLOC = lambda a, v: "(Transformation|SetActorLocation :self %s :NewLocation %s)" % (a, v)
D2 = lambda a, b: "(Math|Vector|Distance2D(Vector) :V1 %s :V2 %s)" % (a, b)
HIDE = lambda a, h: "(Rendering|SetActorHiddenInGame :self %s :bNewHidden %s)" % (a, h)
SND = lambda n, vol=0.7: '(Audio|PlaySound2D :Sound "/Game/Audio/%s.%s" :VolumeMultiplier %s)' % (n, n, vol)
HUD = lambda fn, pin, v: "(Class|BPHUD|Set%s :self hud :%s %s)" % (fn, pin, v)
NOTE = lambda s: S("Note", '"%s"' % s)
TAGS = lambda var, tag: '(bind f_%s (Actor|GetAllActorswithTag :Tag "%s")) (for a_%s f_%s %s)' % (var, tag, var, var, S(var, "a_" + var))
TYPED = lambda var, cls: '(bind t_%s (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/%s.%s_C")) (for b_%s t_%s %s)' % (var, cls, cls, var, var, S(var, "b_" + var))


def by_day(d):
    """Pick a number by the day (2..5)."""
    return "(select (== day 2) %s (select (== day 3) %s (select (== day 4) %s %s)))" % (d[2], d[3], d[4], d[5])


def str_by_day(d):
    return '(select (== day 2) "%s" (select (== day 3) "%s" (select (== day 4) "%s" "%s")))' % (d[2], d[3], d[4], d[5])


done = "true"
for i, dy in CHORE_DAY.items():
    done = "(and %s (or (!= day %d) (Class|BPChores|GetD%d :self ch)))" % (done, dy, i)
loop_start = lambda need: " ".join([S("Need", str(need)), S("LoopOn", "true"), "(Class|BPLoop|SetStreak :self lp :Streak 0)", "(Class|BPLoop|SetWas :self lp :Was false)",
                                    SETLOC(V("LB"), VEC("1.0", "0.0", "0.0")), SND("house_groan", 0.35)])
dsl = f"""(event EventBeginPlay
  {TAGS("UB", "ub")} {TAGS("CB", "cb")} {TAGS("LB", "lb")} {TAGS("QB", "qb")}
  {TAGS("Bed", "ch_bed")} {TAGS("BoxA", "s_boxa")} {TAGS("BoxB", "s_boxb")} {TAGS("OpenA", "st_open_a")} {TAGS("OpenB", "st_open_b")}
  {TAGS("Keep", "st_keepsake")} {TAGS("Albums", "st_albums")} {TAGS("Tape", "st_tape")} {TAGS("Photo", "st_photo")} {TAGS("Climax", "st_climax")} {TAGS("Shelf", "st_shelf")}
  {TYPED("HudRef", "BP_HUD")} {TYPED("LoopRef", "BP_Loop")} {TYPED("DayRef", "BP_Day")} {TYPED("ChoreRef", "BP_Chores")} {TYPED("PlayerRef", "BP_Player")} {TYPED("FrontRef", "BP_Front")}
  (bind ents (Actor|GetAllActorswithTag :Tag "ent"))
  (for e ents (Actor|Tick|SetActorTickEnabled :self e :bEnabled false))
  (if (not (SaveGame|DoesSaveGameExist :SlotName "progress" :UserIndex 0))
    (SaveGame|SaveGametoSlot :SaveGameObject (SaveGame|CreateSaveGameObject :SaveGameClass "/Game/Blueprints/BP_SaveSettings.BP_SaveSettings_C") :SlotName "progress" :UserIndex 0))
  (bind sv0 (Utilities|Casting|CastToBP_SaveSettings :Object (SaveGame|LoadGamefromSlot :SlotName "progress" :UserIndex 0))
    (:then {S("Save", "sv0")}
           (if (> (Class|BPSaveSettings|GetStartDay :self sv0) 0)
             {S("StartReq", "(Class|BPSaveSettings|GetStartDay :self sv0)")}
             (Class|BPSaveSettings|SetStartDay :self sv0 :StartDay 0)
             (SaveGame|SaveGametoSlot :SaveGameObject sv0 :SlotName "progress" :UserIndex 0)))
    (:CastFailed)))

(event EventTick (DeltaSeconds)
  (bind hud {V("HudRef")})
  (bind lp {V("LoopRef")})
  (bind dc {V("DayRef")})
  (bind ch {V("ChoreRef")})
  (bind pl {V("PlayerRef")})
  (bind sv {V("Save")})
  (bind pc (Game|GetPlayerController :PlayerIndex 0))
  (bind ploc {LOC("pl")})
  (bind mode (Class|BPHUD|GetMode :self hud))
  {S("P0", V("Phase"))}
  (bind p0 {V("P0")})
  (bind day {V("Day")})
  (bind t (+ {V("T")} DeltaSeconds))
  {S("T", "t")}
  (bind use (or {V("TestUse")} (and (Game|Player|WasInputKeyJustPressed :self pc :Key (Class|BPPlayer|GetKUse :self pl)) (not (Input|IsMoveInputIgnored :self pc)))))
  ; ---------------- chapter select / continue: the menu leaves a day number on the request board ----------------
  (bind qbl {LOC(V("QB"))})
  (if (> (.x qbl) 0.5)
    ; (a value read from a board is read again each time it is used, so keep it before the board is cleared)
    {S("ReqN", "(select (> (.x qbl) 8.5) (Math|Integer|Max(Integer) :A 1 :B (Class|BPSaveSettings|GetDay :self sv)) (Math|Float|Round :A (.x qbl)))")}
    {SETLOC(V("QB"), VEC("0.0", "0.0", "0.0"))}
    (if (== mode 9)
      {S("StartReq", V("ReqN"))}
      (else
        ; a day picked in the middle of a game: remember it, and start the level again from clean
        (Class|BPSaveSettings|SetStartDay :self sv :StartDay {V("ReqN")})
        (SaveGame|SaveGametoSlot :SaveGameObject sv :SlotName "progress" :UserIndex 0)
        (Game|OpenLevel(byName) :LevelName "POC_VisualSlice"))))
  (if (and (> {V("StartReq")} 0) (> (Utilities|Time|GetGameTimeinSeconds) 0.5))
    {S("ReqN", V("StartReq"))}
    {S("StartReq", "0")}
    (if (== {V("ReqN")} 1)
      {SETLOC(V("UB"), VEC("1.0", "1.0", "1.0"))}
      (else
        (Class|BPFront|SetChoreStart :self {V("FrontRef")} :ChoreStart true)
        {S("Day", "(- " + V("ReqN") + " 1)")} {S("Phase", "10")} {S("T", "0.0")} {S("Woke", "false")}
        {HUD("Fade", "Fade", "1.0")} {HUD("FadeTarget", "FadeTarget", "1.0")})))
  ; ---------------- day 1 is the director's own Day One; it becomes ours when he lies down ----------------
  (if (and (== day 0) (or (== mode 5) (== mode 1))) {S("Day", "1")} {S("Phase", "1")})
  (if (and (== day 1) (and (== mode 3) (not {V("Lay")})))
    ; he lies down on his own bed (the director still thinks the bed is where it was in the small house)
    {S("Lay", "true")}
    (Transformation|SetActorLocation :self pl :NewLocation {VEC("530.0", "-410.0", "418.0")}))
  (if (and (== day 1) (and (== mode 3) (>= (Class|BPHUD|GetStep :self hud) 1)))
    {HUD("Mode", "Mode", "8")} {HUD("FadeTarget", "FadeTarget", "1.0")} {HUD("Power", "Power", "true")}
    (bind cbl0 {LOC(V("CB"))})
    {SETLOC(V("CB"), VEC("(.x cbl0)", "1.0", "(.z cbl0)"))}
    {S("Phase", "10")} {S("T", "0.0")} {S("Woke", "false")})
  (if (>= day 2)
    ; unease climbs through the day; the day's anomalies keep their own pace
    (bind prog (Math|Float|Clamp(Float) :Value (/ {V("DayT")} 420.0) :Min 0.0 :Max 1.0))
    {S("DayT", "(+ " + V("DayT") + " DeltaSeconds)")}
    (if (and (< p0 7) (!= p0 10))
      {HUD("Target", "Target", "(+ " + by_day({k: v[0] for k, v in UNEASE.items()}) + " (* prog (- " + by_day({k: v[1] for k, v in UNEASE.items()}) + " " + by_day({k: v[0] for k, v in UNEASE.items()}) + ")))")})
    (Class|BPDay|SetOver :self dc :Over false))
  ; ---------------- night: fade, the day card, autosave, wake beside the bed ----------------
  (if (== p0 10)
    (if (<= t 7.0) {HUD("FadeTarget", "FadeTarget", "1.0")})
    (if (and (> t 2.5) (not {V("Woke")}))
      {S("Woke", "true")}
      {S("Day", "(+ day 1)")}
      {S("DayT", "0.0")}
      {S("Card", str_by_day(CARDS))}
      {S("CardT", "4.5")}
      (Class|BPSaveSettings|SetDay :self sv :Day day)
      (SaveGame|SaveGametoSlot :SaveGameObject sv :SlotName "progress" :UserIndex 0)
      (Class|BPDay|SetT :self dc :T 0.0) (Class|BPDay|SetDayLen :self dc :DayLen 600.0)
      (Transformation|SetActorLocation :self pl :NewLocation {VEC("450.0", "-330.0", "351.0")})
      (Pawn|SetControlRotation :self pc :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 180.0))
      (Collision|SetActorEnableCollision :self pl :bNewActorEnableCollision true))
    (if (> t 7.0)
      {HUD("FadeSpeed", "FadeSpeed", "0.5")} {HUD("FadeTarget", "FadeTarget", "0.0")}
      (Input|ResetIgnoreMoveInput :self pc) (Input|ResetIgnoreLookInput :self pc)
      (Class|BPDay|SetGapMin :self dc :GapMin {by_day({k: float(v[0]) for k, v in GAPS.items()})})
      (Class|BPDay|SetGapMax :self dc :GapMax {by_day({k: float(v[1]) for k, v in GAPS.items()})})
      (bind e2 (Actor|GetAllActorswithTag :Tag "ent2"))
      (for a2 e2 (Actor|Tick|SetActorTickEnabled :self a2 :bEnabled true))
      (if (>= day 3) (bind e3 (Actor|GetAllActorswithTag :Tag "ent3")) (for a3 e3 (Actor|Tick|SetActorTickEnabled :self a3 :bEnabled true)))
      (if (>= day 4) (bind e4 (Actor|GetAllActorswithTag :Tag "ent4")) (for a4 e4 (Actor|Tick|SetActorTickEnabled :self a4 :bEnabled true)))
      {S("Note", str_by_day({2: "the list. start with the bed.", 3: "more to do. the yard.", 4: "there was something you were going to do.", 5: "stay. no. go upstairs."}))}
      {S("Phase", "1")} {S("T", "0.0")}))
  ; ---------------- phase 1: the day's chores ----------------
  (if (and (== p0 1) (>= day 2))
    (if {done}
      {S("T", "0.0")}
      (if (== day 2)
        {S("Phase", "5")} {NOTE("that is everything. go to bed.")}
        (else
          {S("Phase", "2")}
          {S("Note", '(select (== day 3) "the closet at the end of the upstairs hall is open." "something upstairs is wrong. the closet.")')}
          (if (== day 3) {loop_start(1)} (else (if (== day 4) {loop_start(3)} (else {loop_start(5)}))))))))
  ; ---------------- the corridor loop: it runs until he has made enough right calls and is back in the hall ----------------
  (if {V("LoopOn")}
    (bind lbl {LOC(V("LB"))})
    {S("Count", "(Math|Float|Round :A (.y lbl))")}
    (if (and (>= (.y lbl) (Math|Conversions|ToFloat(Integer) {V("Need")})) (> (.y ploc) -600.0))
      {S("LoopOn", "false")}
      (bind doors (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Mover.BP_Mover_C"))
      (for d doors
        (if (and (Class|BPMover|GetLoopKey :self d) (Class|BPMover|GetOpen :self d)) (Game|Damage|ApplyDamage :DamagedActor d :BaseDamage 1.0)))
      {SETLOC(V("LB"), VEC("0.0", "0.0", "0.0"))}
      (bind ax (Actor|GetAllActorswithTag :Tag "annex"))
      (for a ax {HIDE("a", "true")} (Collision|SetActorEnableCollision :self a :bNewActorEnableCollision false))
      (bind axh (Actor|GetAllActorswithTag :Tag "annex_hide"))
      (for h axh {HIDE("h", "false")} (Collision|SetActorEnableCollision :self h :bNewActorEnableCollision true))
      {SND("click", 0.6)}
      {S("T", "0.0")}
      (if (== day 3)
        ; the first time the house stretched. Afterwards their door stands open.
        (bind pd (Actor|GetAllActorsOfClasswithTag :ActorClass "/Game/Blueprints/BP_Mover.BP_Mover_C" :Tag "s_pdoor"))
        (for q pd (if (not (Class|BPMover|GetOpen :self q)) (Game|Damage|ApplyDamage :DamagedActor q :BaseDamage 1.0)))
        {S("Phase", "5")} {NOTE("their door is open. not yet. go to bed.")}
        (elif (and (== day 4) (== p0 2))
          {S("Phase", "3")} {NOTE("it is not finished. the closet again.")} {loop_start(3)}
          (elif (== day 4)
            {S("Phase", "5")} {NOTE("go to bed. please.")}
            (else
              {S("Phase", "6")} {NOTE("their room. the box, the albums, the tape.")}
              (bind pd5 (Actor|GetAllActorsOfClasswithTag :ActorClass "/Game/Blueprints/BP_Mover.BP_Mover_C" :Tag "s_pdoor"))
              (for q5 pd5 (if (not (Class|BPMover|GetOpen :self q5)) (Game|Damage|ApplyDamage :DamagedActor q5 :BaseDamage 1.0)))))))))
  ; ---------------- phase 5: bed ----------------
  (if (and (== p0 5) (and use (< {D2("ploc", LOC(V("Bed")))} 210.0)))
    {HUD("FadeSpeed", "FadeSpeed", "0.8")} {HUD("FadeTarget", "FadeTarget", "1.0")}
    (Input|SetIgnoreMoveInput :self pc :bNewMoveInput true)
    {NOTE("")} {S("Phase", "10")} {S("T", "0.0")} {S("Woke", "false")})
  ; ---------------- day 5, phase 6: the parents' room. Three things hold the last memories ----------------
  (if (== p0 6)
    (if (and use (and (not {V("M0")}) (< {D2("ploc", LOC(V("Keep")))} 150.0)))
      {S("M0", "true")} {NOTE("hospital bracelets. three of them. mine is the smallest.")} {SND("click", 0.4)})
    (if (and use (and (not {V("M1")}) (< {D2("ploc", LOC(V("Albums")))} 150.0)))
      {S("M1", "true")} {NOTE("every page has the date in her handwriting. the last one is this spring.")} {SND("cloth", 0.5)})
    (if (and use (and (not {V("M2")}) (< {D2("ploc", LOC(V("Tape")))} 150.0)))
      {S("M2", "true")} {NOTE("JACK - 5TH BIRTHDAY. he is laughing behind the camera the whole time.")} {SND("click", 0.4)})
    (if (and {V("M0")} (and {V("M1")} {V("M2")}))
      {S("Phase", "7")} {S("T", "0.0")} {S("Shown", "false")}))
  ; ---------------- phase 7: the one earned moment. It waits behind him; when he faces it, it does not turn into a coat. Then it lets go ----------------
  (if (== p0 7)
    (bind pcm (Game|GetPlayerCameraManager :PlayerIndex 0))
    (bind cam (Camera|GetCameraLocation :self pcm))
    (bind fwd (Math|Vector|GetForwardVector :InRot (Camera|GetCameraRotation :self pcm)))
    (bind to (- (+ {LOC(V("Climax"))} (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 110.0)) cam))
    (bind dist (+ (Math|Vector|VectorLength :A to) 0.001))
    (bind ang (Math|Trig|Acos(Degrees) :A (/ (Math|Vector|DotProduct :A fwd :B to) dist)))
    (if (and (not {V("Shown")}) (and (> t 6.0) (> ang 95.0)))
      {S("Shown", "true")} {HIDE(V("Climax"), "false")} {S("T", "0.0")} {S("Look", "0.0")}
      {HUD("Target", "Target", "100.0")} {SND("house_groan", 0.55)} {NOTE("")})
    (if {V("Shown")}
      (if (< ang 28.0) {S("Look", "(+ " + V("Look") + " DeltaSeconds)")})
      (if (> {V("Look")} 2.2)
        {HIDE(V("Climax"), "true")}
        {HUD("Target", "Target", "0.0")}
        {SND("cloth", 0.4)}
        {NOTE("it was only ever me.")}
        {S("Phase", "8")} {S("T", "0.0")})))
  ; ---------------- phase 8: the house is quiet. Unpack the two boxes; put one photo on the shelf beside theirs ----------------
  (if (== p0 8)
    {HUD("Target", "Target", "0.0")}
    (if (and (> t 9.0) (and (not {V("U0")}) (not {V("U1")}))) {NOTE("unpack. both boxes.")})
    (if (and use (and (not {V("U0")}) (< {D2("ploc", LOC(V("BoxA")))} 170.0)))
      {S("U0", "true")} {SETLOC(V("OpenA"), LOC(V("BoxA")))} {HIDE(V("OpenA"), "false")} {HIDE(V("BoxA"), "true")}
      (Collision|SetActorEnableCollision :self {V("BoxA")} :bNewActorEnableCollision false) {SND("box_thump", 0.6)})
    (if (and use (and (not {V("U1")}) (< {D2("ploc", LOC(V("BoxB")))} 170.0)))
      {S("U1", "true")} {SETLOC(V("OpenB"), LOC(V("BoxB")))} {HIDE(V("OpenB"), "false")} {HIDE(V("BoxB"), "true")}
      (Collision|SetActorEnableCollision :self {V("BoxB")} :bNewActorEnableCollision false) {SND("box_thump", 0.6)})
    (if (and {V("U0")} (and {V("U1")} (not {V("U2")})))
      {NOTE("one more thing. the mantel in the living room, next to theirs.")}
      (if (and use (< {D2("ploc", LOC(V("Shelf")))} 190.0))
        {S("U2", "true")} {HIDE(V("Photo"), "false")} {SND("click", 0.5)} {NOTE("")} {S("T", "0.0")}))
    (if (and {V("U2")} (> t 5.0)) {HUD("FadeSpeed", "FadeSpeed", "0.4")} {HUD("FadeTarget", "FadeTarget", "1.0")})
    (if (and {V("U2")} (> t 9.0))
      {HUD("Mode", "Mode", "4")} {HUD("FadeTarget", "FadeTarget", "0.0")} {S("Phase", "9")}
      (Class|BPSaveSettings|SetDay :self sv :Day 1)
      (SaveGame|SaveGametoSlot :SaveGameObject sv :SlotName "progress" :UserIndex 0)))
  {S("CardT", "(- " + V("CardT") + " DeltaSeconds)")}
  {S("TestUse", "false")})
"""
open(os.path.join(here, "story.dsl"), "w").write(dsl)
print("story.dsl written,", len(dsl.splitlines()), "lines")
if len(sys.argv) > 1 and sys.argv[1] == "apply":
    import bp_tool as B
    N = "BP_Story"
    print(json.dumps(B.create(N, "/Script/Engine.StaticMeshActor"))[:160])
    for k in ("Day", "StartDay"):
        B.add_var("BP_SaveSettings", k, "int")
    B.call(B.BT, "compile_blueprint", {"blueprint": B.bp_ref("BP_SaveSettings"), "warnings_as_errors": False})
    for k in ("UB", "CB", "LB", "QB", "Bed", "BoxA", "BoxB", "OpenA", "OpenB", "Keep", "Albums", "Tape", "Photo", "Climax", "Shelf"):
        B.add_obj_var(N, k, "/Script/Engine.Actor")
    for k, c in (("FrontRef", "BP_Front"), ("HudRef", "BP_HUD"), ("LoopRef", "BP_Loop"), ("DayRef", "BP_Day"), ("ChoreRef", "BP_Chores"), ("PlayerRef", "BP_Player"), ("Save", "BP_SaveSettings")):
        B.add_obj_var(N, k, "/Game/Blueprints/%s.%s_C" % (c, c))
    for k in ("Day", "Phase", "P0", "Need", "Count", "StartReq", "ReqN"):
        B.add_var(N, k, "int")
    for k in ("T", "DayT", "CardT", "Look"):
        B.add_var(N, k, "float")
    for k in ("Lay", "LoopOn", "Woke", "Shown", "M0", "M1", "M2", "U0", "U1", "U2", "TestUse"):
        B.add_var(N, k, "bool")
    for k in ("Note", "Card"):
        B.add_var(N, k, "string")
    for k in ("StartReq", "TestUse", "Day", "Phase"):
        B.call(B.BT, "set_variable_instance_editable", {"blueprint": B.bp_ref(N), "variable_name": k, "instance_editable": True})
    print(json.dumps(B.write(N, os.path.join(here, "story.dsl")))[:3000])
