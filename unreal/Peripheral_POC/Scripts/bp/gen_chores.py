#!/usr/bin/env python3
"""Writes Scripts/bp/chores.dsl (the logic of BP_Chores) and, with 'apply', creates its variables and writes the graph.
The nine chores, in list order: 0 mow, 1 trash, 2 mail, 3 dishes, 4 laundry, 5 water the garden, 6 sweep, 7 bulb, 8 bed."""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
OX, OY = 450.0, 1150.0
ue = lambda x, y: (x - OX, -(y - OY))
CURB, HALL = ue(-1125, 600), ue(340, 1425)
REFS = dict(CB="cb", CP="cp", Mower="ch_mower", Bin="ch_bin", Bag="ch_bag", Mailbox="ch_mailbox", MailboxOpen="ch_mailbox_open", Mail="ch_mail",
            Washer="ch_washer", Dryer="ch_dryer", Clothes="ch_clothes", Can="ch_can", Broom="ch_broom", BulbBox="ch_bulb", Bed="ch_bed",
            BedMade="ch_bed_made", Rack="ch_rack", HallSwitch="ch_hall_switch")
V = lambda n: "(Variables|Default|Get%s)" % n
S = lambda n, v: "(Variables|Default|Set%s %s)" % (n, v)
LOC = lambda a: "(Transformation|GetActorLocation :self %s)" % a
D2 = lambda a, b: "(Math|Vector|Distance2D(Vector) :V1 %s :V2 %s)" % (a, b)
VEC = lambda x, y, z: "(Math|Vector|MakeVector :X %s :Y %s :Z %s)" % (x, y, z)
SND = lambda n, vol=0.7: '(Audio|PlaySound2D :Sound "/Game/Audio/%s.%s" :VolumeMultiplier %s)' % (n, n, vol)
HIDE = lambda a, h: "(Rendering|SetActorHiddenInGame :self %s :bNewHidden %s)" % (a, h)
COLL = lambda a, c: "(Collision|SetActorEnableCollision :self %s :bNewActorEnableCollision %s)" % (a, c)
CAP = lambda i: "(Transformation|SetActorLocation :self %s :NewLocation %s)" % (V("CP"), VEC("%d.0" % i, "now", "0.0"))

begin = "\n".join('  (bind f_%s (Actor|GetAllActorswithTag :Tag "%s"))\n  (for a_%s f_%s %s)' % (k, t, k, k, S(k, "a_" + k)) for k, t in REFS.items())
dsl = f"""(event EventBeginPlay
{begin}
  (bind plates0 (Actor|GetAllActorswithTag :Tag "ch_plate"))
  (for p0 plates0 {S("SinkLoc", LOC("p0"))} (break))
  {S("WasherHome", LOC(V("Washer")))}
  {S("DryerHome", LOC(V("Dryer")))}
  {S("MowSnd", '(Audio|SpawnSound2D :Sound "/Game/Audio/mower_loop.mower_loop" :VolumeMultiplier 0.55 :bAutoDestroy false)')}
  {S("WashSnd", '(Audio|SpawnSound2D :Sound "/Game/Audio/washer_loop.washer_loop" :VolumeMultiplier 0.5 :bAutoDestroy false)')}
  {S("DrySnd", '(Audio|SpawnSound2D :Sound "/Game/Audio/dryer_loop.dryer_loop" :VolumeMultiplier 0.5 :bAutoDestroy false)')}
  {S("PourSnd", '(Audio|SpawnSound2D :Sound "/Game/Audio/water_pour.water_pour" :VolumeMultiplier 0.5 :bAutoDestroy false)')}
  (Audio|Components|Audio|SetPaused :self {V("MowSnd")} :bPause true)
  (Audio|Components|Audio|SetPaused :self {V("WashSnd")} :bPause true)
  (Audio|Components|Audio|SetPaused :self {V("DrySnd")} :bPause true)
  (Audio|Components|Audio|SetPaused :self {V("PourSnd")} :bPause true)
  (bind pl0 (Utilities|Casting|CastToBP_Player :Object (Game|GetPlayerPawn :PlayerIndex 0))
    (:then {S("PlayerRef", "pl0")})
    (:CastFailed)))

(event EventTick (DeltaSeconds)
  (bind cb {V("CB")})
  (bind cbl {LOC("cb")})
  (bind pl {V("PlayerRef")})
  (bind pc (Game|GetPlayerController :PlayerIndex 0))
  (bind ploc {LOC("pl")})
  (bind now (Utilities|Time|GetGameTimeinSeconds))
  (bind active (> (.y cbl) 0.5))
  ; TestUse lets a script press "use" for a play-mode test
  (bind use (and active (or {V("TestUse")} (and (Game|Player|WasInputKeyJustPressed :self pc :Key (Class|BPPlayer|GetKUse :self pl)) (not (Input|IsMoveInputIgnored :self pc))))))
  (bind held (Class|BPPlayer|GetHeld :self pl))
  (bind carrying (Class|BPPlayer|GetCarrying :self pl))
  (bind pushing (Class|BPPlayer|GetPushing :self pl))
  ; ---------------- 0. mow the lawn: the long grass is cut short wherever the mower passes ----------------
  (bind mowing (and active (and pushing (== held {V("Mower")}))))
  (Audio|Components|Audio|SetPaused :self {V("MowSnd")} :bPause (not mowing))
  (if mowing
    (bind mloc {LOC(V("Mower"))})
    (bind grass (Actor|GetAllActorswithTag :Tag "grass"))
    {S("Left", "0")}
    (for g grass
      (if (> (.z (Transformation|GetActorScale3D :self g)) 0.5)
        (if (< {D2(LOC("g"), "mloc")} 78.0)
          (Transformation|SetActorScale3D :self g :NewScale3D {VEC("1.0", "1.0", "0.16")})
          (else {S("Left", "(+ " + V("Left") + " 1)")}))))
    (if (and (< {V("Left")} 3) (not {V("D0")})) {S("D0", "true")} {SND("click", 0.5)})
    (if (> (- now {V("CapT")}) 4.0) {S("CapT", "now")} {CAP(1)}))
  ; the day can ask for one strip to grow back (request 2)
  (if (and (> (.z cbl) 1.5) (< (.z cbl) 2.5))
    (bind strip (Actor|GetAllActorswithTag :Tag "grass_s3"))
    (for gs strip (Transformation|SetActorScale3D :self gs :NewScale3D {VEC("1.0", "1.0", "1.0")}))
    (Transformation|SetActorLocation :self cb :NewLocation {VEC("(.x cbl)", "(.y cbl)", "0.0")}))
  ; ---------------- 1. trash: bag into the wheeled bin, bin to the curb ----------------
  (if (and active (== {V("TrashS")} 0))
    (if (< {D2(LOC(V("Bag")), LOC(V("Bin")))} 115.0)
      {HIDE(V("Bag"), "true")}
      {COLL(V("Bag"), "false")}
      (Class|BPPlayer|SetCarrying :self pl :Carrying false)
      {SND("box_thump", 0.7)}
      {S("TrashS", "1")}))
  (if (and active (== {V("TrashS")} 1))
    (if (and (< {D2(LOC(V("Bin")), VEC(CURB[0], CURB[1], "0.0"))} 230.0) (not (and pushing (== held {V("Bin")}))))
      {S("TrashS", "2")} {S("D1", "true")} {SND("click", 0.5)}))
  ; ---------------- 2. mail: open the box, carry the mail indoors ----------------
  (if (and use (and (== {V("MailS")} 0) (< {D2("ploc", LOC(V("Mailbox")))} 190.0)))
    {HIDE(V("Mailbox"), "true")} {HIDE(V("MailboxOpen"), "false")} {HIDE(V("Mail"), "false")}
    {SND("mailbox", 0.7)}
    {S("MailS", "1")})
  (if (and active (== {V("MailS")} 1))
    (if (> (.x {LOC(V("Mail"))}) -430.0) {S("MailS", "2")} {S("D2", "true")} {SND("click", 0.5)}))
  ; ---------------- 3. dishes: one plate per press, from the sink to the rack ----------------
  (bind dn {V("DishN")})
  (if (and use (and (< dn 5) (and (< {D2("ploc", V("SinkLoc"))} 150.0) (> (- now {V("UseT")}) 0.7))))
    (bind plates (Actor|GetAllActorswithTag :Tag "ch_plate"))
    (bind clean (Actor|GetAllActorswithTag :Tag "ch_plate_clean"))
    {HIDE('(Utilities|Array|Get(acopy) :Array plates :"Dimension 1" (- 4 dn))', "true")}
    {HIDE('(Utilities|Array|Get(acopy) :Array clean :"Dimension 1" dn)', "false")}
    {SND("dish_wash", 0.7)} {CAP(5)}
    {S("UseT", "now")}
    {S("DishN", "(+ dn 1)")}
    (if (== dn 4) {S("D3", "true")} {SND("click", 0.5)}))
  ; the day can put the washed dishes back in the sink (request 1)
  (if (and (> (.z cbl) 0.5) (< (.z cbl) 1.5))
    (bind plates2 (Actor|GetAllActorswithTag :Tag "ch_plate"))
    (for p2 plates2 {HIDE("p2", "false")})
    (bind clean2 (Actor|GetAllActorswithTag :Tag "ch_plate_clean"))
    (for c2 clean2 {HIDE("c2", "true")})
    {S("DishN", "0")}
    (Transformation|SetActorLocation :self cb :NewLocation {VEC("(.x cbl)", "(.y cbl)", "0.0")}))
  ; ---------------- 4. laundry: washer, then dryer ----------------
  (bind ls {V("LaunS")})
  (bind nearW (< {D2("ploc", V("WasherHome"))} 175.0))
  (if (and use (and (== ls 0) nearW))
    {HIDE(V("Clothes"), "true")} {SND("cloth", 0.7)} {S("LaunS", "1")} {S("LaunT", "0.0")})
  (if (and use (and (== ls 2) nearW))
    {SND("cloth", 0.7)} {S("LaunS", "3")} {S("LaunT", "0.0")} {S("D4", "true")})
  (Audio|Components|Audio|SetPaused :self {V("WashSnd")} :bPause (!= ls 1))
  (Audio|Components|Audio|SetPaused :self {V("DrySnd")} :bPause (!= ls 3))
  (if (or (== ls 1) (== ls 3))
    (bind lt (+ {V("LaunT")} DeltaSeconds))
    {S("LaunT", "lt")}
    (bind shake {VEC("(* 0.5 (Math|Trig|Sin(Radians) (* now 41.0)))", "(* 0.4 (Math|Trig|Sin(Radians) (* now 53.0)))", "0.0")})
    (if (== ls 1)
      (Transformation|SetActorLocation :self {V("Washer")} :NewLocation (+ {V("WasherHome")} shake))
      (else (Transformation|SetActorLocation :self {V("Dryer")} :NewLocation (+ {V("DryerHome")} shake))))
    (if (and (< lt 0.3) active) {CAP(2)})
    (if (> lt 18.0)
      {SND("buzzer", 0.5)} {CAP(3)}
      {S("LaunS", "(+ ls 1)")}))
  ; ---------------- 5. water the garden: stand at each dry patch with the can ----------------
  (bind wn {V("WaterN")})
  (if (and active (and (< wn 3) (and carrying (== held {V("Can")}))))
    (bind dry (Actor|GetAllActorswithTag :Tag "ch_soil"))
    (bind patch (Utilities|Array|Get(acopy) :Array dry :"Dimension 1" wn))
    (if (< {D2("ploc", LOC("patch"))} 175.0)
      (bind wt (+ {V("WaterT")} DeltaSeconds))
      {S("WaterT", "wt")}
      (Audio|Components|Audio|SetPaused :self {V("PourSnd")} :bPause false)
      (if (< wt 0.1) {CAP(4)})
      (if (> wt 2.2)
        (bind wet (Actor|GetAllActorswithTag :Tag "ch_soil_wet"))
        {HIDE("patch", "true")}
        {HIDE('(Utilities|Array|Get(acopy) :Array wet :"Dimension 1" wn)', "false")}
        {S("WaterN", "(+ wn 1)")} {S("WaterT", "0.0")}
        (if (== wn 2) {S("D5", "true")} {SND("click", 0.5)}))
      (else (Audio|Components|Audio|SetPaused :self {V("PourSnd")} :bPause true)))
    (else (Audio|Components|Audio|SetPaused :self {V("PourSnd")} :bPause true)))
  ; ---------------- 6. sweep the garage: push the broom through each pile ----------------
  (if (and active (and pushing (== held {V("Broom")})))
    (bind bl {LOC(V("Broom"))})
    (bind dust (Actor|GetAllActorswithTag :Tag "ch_dust"))
    {S("Left", "0")}
    (for d dust
      (if (> (.z (Transformation|GetActorScale3D :self d)) 0.5)
        (if (< {D2(LOC("d"), "bl")} 62.0)
          (Transformation|SetActorScale3D :self d :NewScale3D {VEC("0.05", "0.05", "0.05")})
          {HIDE("d", "true")}
          {SND("sweep", 0.6)}
          (else {S("Left", "(+ " + V("Left") + " 1)")}))))
    (if (and (== {V("Left")} 0) (not {V("D6")})) {S("D6", "true")} {SND("click", 0.5)}))
  ; ---------------- 7. the hall bulb: carry the new bulb under the dead fixture ----------------
  (if (and active (and (not {V("D7")}) (and carrying (== held {V("BulbBox")}))))
    (if (< {D2("ploc", VEC(HALL[0], HALL[1], "0.0"))} 120.0)
      {HIDE(V("BulbBox"), "true")}
      (Class|BPPlayer|SetCarrying :self pl :Carrying false)
      {SND("click", 0.8)}
      {S("D7", "true")}
      (bind sw (Utilities|Casting|CastToBP_Switch :Object {V("HallSwitch")})
        (:then (Class|BPSwitch|SetStage :self sw :Stage 1) (Class|BPSwitch|SetOn :self sw :On true))
        (:CastFailed))))
  ; ---------------- 8. make the bed ----------------
  (if (and use (and (not {V("D8")}) (< {D2("ploc", LOC(V("Bed")))} 200.0)))
    {HIDE(V("Bed"), "true")} {COLL(V("Bed"), "false")} {HIDE(V("BedMade"), "false")}
    {SND("cloth", 0.8)}
    {S("D8", "true")})
  ; ---------------- report: one bit per finished chore ----------------
  (bind mask (+ (+ (+ (select {V("D0")} 1.0 0.0) (select {V("D1")} 2.0 0.0)) (+ (select {V("D2")} 4.0 0.0) (select {V("D3")} 8.0 0.0)))
               (+ (+ (select {V("D4")} 16.0 0.0) (select {V("D5")} 32.0 0.0)) (+ (+ (select {V("D6")} 64.0 0.0) (select {V("D7")} 128.0 0.0)) (select {V("D8")} 256.0 0.0)))))
  {S("TestUse", "false")}
  (bind cb2 {LOC("cb")})
  (Transformation|SetActorLocation :self cb :NewLocation {VEC("mask", "(.y cb2)", "(.z cb2)")}))
"""
open(os.path.join(here, "chores.dsl"), "w").write(dsl)
print("chores.dsl written,", len(dsl.splitlines()), "lines")
if len(sys.argv) > 1 and sys.argv[1] == "apply":
    import bp_tool as B
    N = "BP_Chores"
    for k in REFS:
        B.add_obj_var(N, k, "/Script/Engine.Actor")
    B.add_obj_var(N, "PlayerRef", "/Game/Blueprints/BP_Player.BP_Player_C")
    B.add_var(N, "TestUse", "bool")
    for k in ("MowSnd", "WashSnd", "DrySnd", "PourSnd"):
        B.add_obj_var(N, k, "/Script/Engine.AudioComponent")
    for i in range(9):
        B.add_var(N, "D%d" % i, "bool")
    for k in ("DishN", "WaterN", "TrashS", "MailS", "LaunS", "Left"):
        B.add_var(N, k, "int")
    for k in ("LaunT", "WaterT", "UseT", "CapT"):
        B.add_var(N, k, "float")
    for k in ("SinkLoc", "WasherHome", "DryerHome"):
        B.add_var(N, k, "Vector")
    print(json.dumps(B.write(N, os.path.join(here, "chores.dsl")))[:3000])
