#!/usr/bin/env python3
"""Writes Scripts/bp/front.dsl (BP_Front) and, with 'apply', creates the Blueprint and writes its graph.

BP_Front is everything round 1 added around the director (BP_HUD) without rewriting the director's own very large graph
(rewriting it drove the editor to 65 GB of memory). It steers the director from outside:
  - the menu board and the mouse: any menu shows the pointer and unlocks it from the window; play captures it again
  - the title: director mode 9 (which the director itself ignores); a slow look round the new house behind the menu
  - New game (Day One and its drive in), the chore day (F5), pause (Esc), back to title, quit
  - music: six looping slots crossfaded by unease
  - the Accessibility cap on unease
The director's old keyboard title menu, pause menu and music are switched off from here."""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
V = lambda n: "(Variables|Default|Get%s)" % n
S = lambda n, v: "(Variables|Default|Set%s %s)" % (n, v)
LOC = lambda a: "(Transformation|GetActorLocation :self %s)" % a
VEC = lambda x, y, z: "(Math|Vector|MakeVector :X %s :Y %s :Z %s)" % (x, y, z)
SETLOC = lambda a, v: "(Transformation|SetActorLocation :self %s :NewLocation %s)" % (a, v)
HG = lambda n: "(Class|BPHUD|Get%s :self hud)" % n
HS = lambda n, v: "(Class|BPHUD|Set%s :self hud :%s %s)" % (n, n, v)
UB = lambda x, y, z: SETLOC(V("UB"), VEC(x, y, z))
TAGS = lambda var, tag: '(bind f_%s (Actor|GetAllActorswithTag :Tag "%s")) (for a_%s f_%s %s)' % (var, tag, var, var, S(var, "a_" + var))
SLOTS = ["music_title", "music_day1_calm", "music_unease_low", "music_unease_mid", "music_unease_high", "music_loop_sequence"]
CONDS = ["(== mode 9)", "(and inplay (< u 15.0))", "(and inplay (and (>= u 15.0) (< u 45.0)))", "(and inplay (and (>= u 45.0) (< u 75.0)))", "(and inplay (>= u 75.0))", "(== mode 6)"]
VIEWS = [(50, 150, 92, -6, 135), (170, -250, 92, -5, 49), (-300, -370, 92, -3, 24), (290, 0, 351, -8, -57), (-1380, 730, -47, -2, 33)]      # living room, kitchen, hall, Jack's room, the car


def pick(col):
    e = str(float(VIEWS[-1][col]))
    for i in range(len(VIEWS) - 2, -1, -1):
        e = "(select (== mv %d) %s %s)" % (i, float(VIEWS[i][col]), e)
    return e


music0 = "\n  ".join(S("Mus%d" % i, '(Audio|SpawnSound2D :Sound "/Game/Audio/%s.%s" :VolumeMultiplier 0.01 :bAutoDestroy false)' % (n, n)) for i, n in enumerate(SLOTS))
fade = "\n  ".join('''(bind w%d (Math|Interpolation|FInterpTo :Current %s :Target (select %s 1.0 0.0) :DeltaTime DeltaSeconds :InterpSpeed 0.7))
  %s
  (Class|AudioComponent|SetVolumeMultiplier :self %s :VolumeMultiplier (+ 0.001 (* 0.6 w%d)))''' % (i, V("Vol%d" % i), c, S("Vol%d" % i, "w%d" % i), V("Mus%d" % i), i) for i, c in enumerate(CONDS))
dsl = f"""(event EventBeginPlay
  {TAGS("UB", "ub")} {TAGS("SB", "sb")} {TAGS("CB", "cb")}
  (bind huds (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_HUD.BP_HUD_C"))
  (for h huds {S("HudRef", "h")})
  {music0})

(event EventTick (DeltaSeconds)
  (bind hud {V("HudRef")})
  (bind pc (Game|GetPlayerController :PlayerIndex 0))
  (bind pawn (Game|GetPlayerPawn :PlayerIndex 0))
  (if (not {V("Init")})
    ; the director's own title (keyboard image menu, old camera spots) is retired: mode 9 is ours
    {S("Init", "true")}
    {HS("Mode", "9")}
    (Class|AudioComponent|SetVolumeMultiplier :self {HG("Music")} :VolumeMultiplier 0.001))
  (bind mode {HG("Mode")})
  ; ---------------- the menu board: X = screen showing (0 = play), Y = the button just pressed ----------------
  (bind ubl0 {LOC(V("UB"))})
  {S("Screen", "(Math|Float|Round :A (.x ubl0))")}
  {S("Cmd", "(Math|Float|Round :A (.y ubl0))")}
  (bind screen {V("Screen")})
  (bind cmd {V("Cmd")})
  (if (> cmd 0) {UB("(.x ubl0)", "0.0", "(.z ubl0)")})
  (bind sbl {LOC(V("SB"))})
  ; any menu frees the mouse (pointer shown, not locked to the window); it is captured again only when play resumes
  (bind menuOn (select (> screen 0) 1 0))
  (if (!= menuOn {V("CursorOn")})
    (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor (== menuOn 1))
    (if (== menuOn 1)
      (Input|SetInputModeGameAndUI :PlayerController pc :InMouseLockMode "DoNotLock" :bHideCursorDuringCapture false)
      (else (Input|SetInputModeGameOnly :PlayerController pc)))
    {S("CursorOn", "menuOn")})
  ; the director's old pause menu must never show: ours is the widget
  {HS("Paused", "false")}
  ; ---------------- accessibility: a cap on the unease effects ----------------
  (if (> {HG("Target")} (* 100.0 (.z sbl))) {HS("Target", "(* 100.0 (.z sbl))")})
  ; ---------------- music: six named slots, crossfaded by where the game is and how high the unease is ----------------
  (bind u {HG("Unease")})
  (bind inplay (and (!= mode 9) (and (!= mode 6) (!= mode 4))))
  {fade}
  ; ---------------- the title: a slow look round the house; the view moves on every ten seconds ----------------
  (if (== mode 9)
    (bind mt (+ {V("MenuT")} DeltaSeconds))
    {S("MenuT", "mt")}
    (bind mv {V("MenuV")})
    (if (> mt 9.4) {HS("FadeTarget", "1.0")})
    (if (> mt 10.0)
      {S("MenuV", "(select (>= mv 4) 0 (+ mv 1))")}
      {S("MenuT", "0.0")}
      {HS("FadeTarget", "0.0")})
    (Transformation|SetActorLocation :self pawn :NewLocation {VEC("(+ " + pick(0) + " (* 16.0 (Math|Trig|Sin(Radians) (* mt 0.21))))", pick(1), pick(2))})
    (Pawn|SetControlRotation :self pc :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch {pick(3)} :Yaw (+ {pick(4)} (* 5.0 (Math|Trig|Sin(Radians) (* mt 0.17))))))
    {HS("Target", "18.0")})
  ; ---------------- New game: the director's Day One, starting with the drive in ----------------
  (if (and (== mode 9) (== cmd 1))
    {HS("Mode", "5")} {HS("T", "0.0")} {HS("Fade", "1.0")} {HS("FadeSpeed", "0.5")} {HS("Target", "0.0")} {HS("FadeTarget", "0.0")}
    {UB("0.0", "0.0", "1.0")}
    (Collision|SetActorEnableCollision :self pawn :bNewActorEnableCollision false)
    {HS("Engine", '(Audio|SpawnSound2D :Sound "/Game/Audio/car_engine.car_engine" :VolumeMultiplier 0.55 :bAutoDestroy false)')})
  (if (== cmd 3) {HS("LoopStart", "true")} {UB("0.0", "0.0", "1.0")})
  ; ---------------- the chore day (F5, its menu line, or the story asking for a day to begin) ----------------
  (if (or (== cmd 2) (Game|Player|WasInputKeyJustPressed :self pc :Key "F5")) {S("ChoreStart", "true")})
  (if {V("ChoreStart")}
    {S("ChoreStart", "false")}
    (if (== mode 9)
      (Transformation|SetActorLocation :self pawn :NewLocation {VEC("-150.0", "-270.0", "92.0")})
      (Pawn|SetControlRotation :self pc :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 0.0))
      {HS("Fade", "1.0")} {HS("FadeSpeed", "0.6")} {HS("FadeTarget", "0.0")})
    {HS("Mode", "8")} {HS("Power", "true")} {HS("Target", "10.0")}
    (Collision|SetActorEnableCollision :self pawn :bNewActorEnableCollision true)
    (Input|ResetIgnoreMoveInput :self pc)
    (Input|ResetIgnoreLookInput :self pc)
    (bind gp8 (Actor|GetAllActorswithTag :Tag "periph"))
    (for hp8 gp8 (Actor|Tick|SetActorTickEnabled :self hp8 :bEnabled false))
    (bind cbl8 {LOC(V("CB"))})
    {SETLOC(V("CB"), VEC("(.x cbl8)", "1.0", "(.z cbl8)"))}
    {UB("0.0", "0.0", "1.0")})
  (if (== cmd 5) (Game|OpenLevel(byName) :LevelName "POC_VisualSlice"))
  (if (== cmd 6) (Game|QuitGame))
  ; ---------------- pause (Esc): the game keeps running underneath, Jack stands still, the mouse is released ----------------
  (bind esc (Game|Player|WasInputKeyJustPressed :self pc :Key "Escape"))
  (bind playing (or (or (== mode 1) (== mode 3)) (or (== mode 6) (== mode 8))))
  (if (and esc (> screen 2))
    {UB("(.z ubl0)", "0.0", "(.z ubl0)")})
  (if (and (and esc (== screen 0)) playing)
    (Input|SetIgnoreMoveInput :self pc :bNewMoveInput true)
    (Input|SetIgnoreLookInput :self pc :bNewLookInput true)
    {UB("2.0", "0.0", "2.0")})
  (if (and (== screen 2) (or esc (== cmd 4)))
    (Input|ResetIgnoreMoveInput :self pc)
    (Input|ResetIgnoreLookInput :self pc)
    {UB("0.0", "0.0", "2.0")}))
"""
open(os.path.join(here, "front.dsl"), "w").write(dsl)
print("front.dsl written,", len(dsl.splitlines()), "lines")
if len(sys.argv) > 1 and sys.argv[1] == "apply":
    import bp_tool as B
    N = "BP_Front"
    print(json.dumps(B.create(N, "/Script/Engine.StaticMeshActor"))[:160])
    for k in ("UB", "SB", "CB"):
        B.add_obj_var(N, k, "/Script/Engine.Actor")
    B.add_obj_var(N, "HudRef", "/Game/Blueprints/BP_HUD.BP_HUD_C")
    for i in range(6):
        B.add_obj_var(N, "Mus%d" % i, "/Script/Engine.AudioComponent"); B.add_var(N, "Vol%d" % i, "float")
    for k in ("Screen", "Cmd", "CursorOn", "MenuV"):
        B.add_var(N, k, "int")
    B.add_var(N, "MenuT", "float")
    for k in ("Init", "ChoreStart"):
        B.add_var(N, k, "bool")
    B.call(B.BT, "set_variable_instance_editable", {"blueprint": B.bp_ref(N), "variable_name": "ChoreStart", "instance_editable": True})
    print(json.dumps(B.write(N, os.path.join(here, "front.dsl")))[:3000])
