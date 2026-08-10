# Peripheral / Isolation — Day 3 / Final Act

Detailed gameplay, narrative, and Unreal Engine implementation spec for the game's
final sequence, from Ezekiel. Preserved close to verbatim — this is implementation-
ready, not a brainstorm to re-derive from.

**Status: resolves the two open Day 3 questions from `AUDIT_REPORT.md` finding #1**
(sprint and the loud-transient rule) **and closes finding #6 and #9's "no designed
ending" concerns** — see the reconciliation note at the bottom of this file.

---

## Purpose of this act

Day 3 is the point where the game's psychological uncertainty finally becomes
immediate physical fear.

Until this sequence, the player has experienced: peripheral shapes, unexplained
sounds, missing objects, distorted memories, strange phone/answering-machine
behavior, changes in the house, possible glimpses of a humanoid presence — but has
never been able to prove that another person or creature is actually inside or
around the house.

Day 3 changes that. **The sequence should still preserve uncertainty for as long as
possible.**

---

## Act 1 — Jack returns home

Late afternoon transitioning toward sunset. The house should initially look largely
normal from outside — no obvious monster, no dramatic supernatural effects.

As Jack approaches: the front door is unlocked/partially open. Jack knows he locked
it before leaving.

**Do not** trigger a jump scare or an enormous musical sting. Instead: ambient
neighborhood sound quiets, interior house ambience becomes more noticeable, a
restrained tension layer begins, Jack's breathing may become slightly more audible.

Objective: check the house.

## Act 2 — Attempt to call for help

Jack tries to contact the police. The phone cannot establish a usable connection —
no signal, call failure, static, connection starts and drops, or the phone appears
functional but can't reach emergency services. Avoid an obviously supernatural
effect here — it should remain plausible that reception is simply poor.

## Act 3 — Jack arms himself

Jack obtains a kitchen knife. **Design rule: not the beginning of a combat system.**
The player cannot fight monsters. The knife exists as psychological reassurance and
character behavior only — no combat tutorial, no health bars, no attack prompts, no
enemy damage.

## Act 4 — Search the house

Jack searches the entire house — living room, kitchen, hallways, bathrooms, Jack's
room, other bedroom(s), closets, basement entrance, garage access, stairways,
utility spaces. The player repeatedly expects to discover somebody. Nobody is
found.

Subtle environmental uncertainty throughout: a door slightly open, a curtain moves,
something vaguely humanoid in peripheral vision, a coat resembling somebody
standing in a room, a floorboard sounds elsewhere, a room just searched produces
another noise. **Do not confirm an intruder.**

## Act 5 — Lockdown

Player secures the house: lock front door, lock back door, check windows, close
curtains, check basement/garage access. Temporary psychological comfort — the
player thinks "maybe somebody simply tried the door and left." Tension is allowed
to decrease.

## Act 6 — Normal night activities

Jack continues his normal routine: eat/drink, wash up, check collected evidence,
listen to recordings/music, examine photographs, prepare for bed, interact with
remaining comfort items. **Some previously acquired comfort items may now be
missing — the disappearance is never announced, the player simply notices.**
Deliberately slower section — the player should begin believing the immediate
danger has passed.

## Act 7 — Jack goes to sleep

Fade naturally into sleep. Avoid obvious nightmare-horror imagery immediately —
allow silence, then an unsettling dream about identity/family/forgotten
childhood/the house/1998/voices Jack almost recognizes, **not monsters**. Examples:
children laughing somewhere unseen, someone calling Jack by another name, a family
member saying "You came back," a door closing. Jack wakes abruptly.

## Act 8 — Jack wakes in the wrong room

Jack does NOT wake in his bedroom — a completely different room of the house. One
of the strongest reality-distortion moments in the game. No transition shown. The
player immediately notices different furniture, different room geometry, a
different doorway, no explanation. Jack's last memory is going to sleep in his own
bed.

## Act 9 — Total power failure

The house is completely dark, all power off. Darkness uses the established flat
five-color visual system — **no photographic darkness, no bloom.** Extremely
limited visibility. Objective: find a flashlight.

## Act 10 — Flashlight search

Jack searches the room; a flashlight is located nearby (e.g. inside a drawer),
physically searched for, not handed over. Once acquired it becomes the player's
main source of confidence. **Visual rule: no realistic bright cone with bloom** —
instead it increases clarity/value within a controlled viewing region using the
game's five-color palette. Should feel helpful without making the player feel fully
safe.

## Act 11 — Investigate the blackout

The breaker needs checking. The panel is outside, at the rear of the house. The
player must leave the house — significant because the outside world has previously
meant relief; tonight it no longer feels completely safe.

## Act 12 — Walk to the back of the house

Jack exits with the flashlight. Environmental audio is important: wind, distant
insects, leaves, house creaking, gravel underfoot, occasional distant movement. No
obvious creature sound, no chase yet.

## Act 13 — Breaker interaction

Open panel → identify main breaker → switch OFF → short pause → switch ON. Power
restored, interior lights visible through parts of the house. **No loud musical
victory cue** — instead the familiar low electrical hum returns. Brief moment of
relief.

## Act 14 — The window sighting

One of the most important visual moments in the game. From behind the house, the
architecture lets Jack look through a rear window, through part of the interior,
toward another window near the front of the house — an unusually deep sightline.

A humanoid figure is standing inside. **Not** centered in an empty room like a
monster showcase — partially obscured by a doorway, standing beyond furniture,
visible between architectural elements, mostly silhouette, slightly outside Jack's
direct gaze initially. The player may notice it first through peripheral vision.

## Act 15 — Player focuses on the figure

**Uses the existing fovea/focus mechanic directly.** If the player immediately
turns toward it, the figure becomes extremely difficult to resolve; the focus
mechanic may allow slightly more definition. Perceivable: humanoid height, thin
body, head, shoulders, possibly unnatural posture. **Not perceivable:** face, skin
texture, eyes, detailed clothing, clear creature anatomy. The player thinks "there
is absolutely someone inside my house" but still can't identify what it is.

## Act 16 — The figure disappears

**Important — this is a different technique from the existing anomaly system's
instant swap.** Do not teleport it. Animate something moving extremely quickly
sideways or backward out of view — the player perceives motion more than anatomy.
Sequence: figure present → player notices → player focuses → a fraction of a
second of stillness → rapid movement out of frame. No scream, no music sting, no
jump scare. Just movement, then silence.

## Act 17 — First footsteps

A moment later, Jack hears footsteps — initially very faint, possibly from the
opposite side of the house. The player can't precisely determine location.
Footsteps begin slowly, then become faster.

## Act 18 — Footsteps accelerate

Footsteps become faster, heavier, closer — direction should feel like something
coming around the house toward Jack. **The creature itself is never shown.** First
true flight response. Objective: GET INSIDE.

## Act 19 — Running sequence

**The player sprints toward the back entrance — player-controlled, not a forced
camera sequence.** Short, intense. Not a conventional monster chase — the player
never looks back and sees a creature running behind them. The threat exists
entirely through footsteps, breathing, environmental sound, peripheral movement,
increasing proximity. Footsteps should intelligently stay behind/near the player
via spatial audio. As Jack reaches the back door, footsteps sound extremely close.

## Act 20 — Enter the house

Jack gets inside, closes and locks the back door. ~1 second of silence. Then a
sound elsewhere — front door movement, a latch, floorboard, door closing, subtle
wood creak. Implication: whatever was outside has entered another way.

## Act 21 — Hide objective

Objective: HIDE. Several hiding locations, no single obviously-correct one:

- **Under Jack's bed** — extremely restricted view (floor, doorway gap, furniture
  legs, limited hallway visibility), audio-dominant.
- **Shower** — close curtain/door, remain crouched, extremely limited visibility.
  Possible sound: water pipe ticking, bathroom fan slowing, house noises.
- **Basement, behind stacked boxes** — riskiest to reach (requires traveling
  farther). Small gaps allow limited visibility. Possibly the most psychologically
  intense option.

## Act 22 — Hiding system

Once in a valid spot, the game enters a tension state. **Important: nothing
obvious happens.** No monster walks dramatically past, no face peers under the
bed, no creature pulls open the curtain, no scripted enemy search animation.
Silence, maybe extremely subtle house ambience. The longer nothing happens, the
more uncomfortable the player becomes.

## Act 23 — The intruder is inside

Subtle audio implies something probably entered — a door latch, one distant
floorboard, very faint movement, a distant object shifting — then nothing. **Never
reveal where the intruder is. No enemy UI, no detection indicator, no "enemy
nearby" meter.** The player decides when it feels safe to leave.

## Act 24 — Waiting mechanic

No event forces the player out. They can wait as long as they want. The game
intentionally exploits uncertainty — there's no clear signal the threat is gone.
Eventually the player has to choose to come out.

## Act 25 — Exit hiding

The house looks empty. Flashlight still works. Cautious exploration begins. No
music, footsteps are gone, no obvious changes. Objective may simply become "look
around."

## Act 26 — False safety

Tension shifts from "they're coming" to "where did they go?" The player checks
nearby areas, nothing happens. **Do not jump scare immediately on leaving hiding.**
Allow checking a hallway, looking through a doorway, entering another room,
listening, focusing behind themselves, seeing nothing. The player starts believing
the intruder may have left.

## Act 27 — Final jump scare

After enough post-hide exploration to lower immediate expectation: **the game's
first and only major traditional jump scare. This ends the game.**

**This is an intentional, explicit exception to "no jump scares."** It works
specifically because the entire game has trained the player to expect
psychological uncertainty instead of a conventional horror attack — one final
violation of that trained expectation lands hard precisely because it's the only
one.

**Even here, do not necessarily reveal the entity clearly.** Possible
presentation: sudden humanoid movement enters extreme close range, flashlight
knocked aside, Jack is grabbed, camera violently shifts, a dark humanoid outline
occupies the frame, extremely brief partial facial/structural information,
immediate cut to black. Roughly 0.25–0.75 seconds of incomplete information —
enough to shock, not enough to definitively understand what attacked Jack.

**Audio for this moment only** may use a sudden impact/collision/abrupt sound
spike — the only place in the game this is permitted. Avoid a generic stock
horror scream; prefer something physical and confusing. Example: movement →
collision → Jack's breath/gasp → flashlight hits floor → blackout.

## Act 28 — Cut to black

Immediately after: cut to black. Do not show Jack being killed, no death
animation, no explanation of the entity, no aftermath shown. Allow silence, then
the title card:

**PERIPHERAL**
*(tagline) YOU ONLY SAW WHAT YOU WERE LOOKING FOR.*

Credits/ending sequence follows.

---

## Unreal Engine systems required

Structure as modular systems, not one giant Level Blueprint:

**`BP_Day3Controller`** — controls major narrative state. State enum:
`DAY3_RETURN, DOOR_DISCOVERED, HOUSE_SEARCH, HOUSE_SECURED, NIGHT_ROUTINE, SLEEP,
WRONG_ROOM, BLACKOUT, FLASHLIGHT_FOUND, BREAKER_OBJECTIVE, POWER_RESTORED,
FIGURE_SEEN, FOOTSTEPS_STARTED, PLAYER_FLEEING, HOUSE_REENTERED, HIDE_PHASE,
INTRUDER_INSIDE, PLAYER_EXITED_HIDE, FINAL_SEARCH, FINAL_SCARE, GAME_END`

**`BP_HidingSpot`** — reusable hiding-spot actor. Properties: `HidingType`,
`EntryTransform`, `ExitTransform`, `CameraTransform`, `CanEnter`, `IsOccupied`,
`VisibilityRestrictions`, `AudioProfile`. Instances: Bed, Shower, BasementBoxes.

**`BP_BreakerPanel`** — `OpenPanel()`, `PowerOff()`, `PowerOn()`,
`NotifyDay3Controller()`.

**`BP_FigureSighting`** — figure spawn, peripheral visibility, gaze detection,
focus detection, rapid exit animation, event completion. **Not a normal AI enemy —
a scripted perceptual event.** Do not build this on the existing `BP_Anomaly` base
class — it needs actual fast physical-movement animation to exit frame, not the
anomaly system's instant off-screen swap.

**`BP_FootstepThreat`** — spatial audio during the running sequence. Variables:
`ThreatDistance`, `StepFrequency`, `StepVolume`, `Direction`, `ChaseIntensity`. As
the player approaches the back door, `ThreatDistance` decreases, step frequency
increases. The threat actor itself doesn't need to be visually rendered.

**`BP_IntruderAudioDirector`** — after re-entry: entry sounds, floorboard events,
environmental movement, silence timing. No visible AI pathfinding needed during
hiding unless later design requires it.

**`BP_FinalScareTrigger`** — only active once: player completed hiding, player
exited hiding, minimum post-hide exploration time elapsed, player entered one of
several valid final-scare zones. Prevents the scare firing immediately on leaving
hiding.

---

## Pacing target

```
RETURN HOME → SUSPICION → SEARCH → FALSE RELIEF → NORMAL ROUTINE → SLEEP →
DISORIENTATION → DARKNESS → PROBLEM SOLVING → TEMPORARY RELIEF → FIGURE → PANIC →
RUN → HIDE → SILENCE → UNCERTAINTY → FALSE SAFETY → FINAL SHOCK → BLACK
```

---

## Critical design rules

1. Do not visually show a creature chasing Jack.
2. Running footsteps create the chase.
3. Do not reveal the entity through normal gameplay.
4. The humanoid through the window must remain visually ambiguous.
5. The movement away from the window should be extremely fast but physically
   animated rather than teleporting.
6. The hiding sequence is primarily driven by silence.
7. No enemy detection meter.
8. No combat.
9. The kitchen knife does not turn the game into an action game.
10. Do not tell the player which hiding spot is safest.
11. Do not attack the player while they remain hidden.
12. Make the player voluntarily leave hiding because silence has become
    unbearable.
13. Give the player a short period of apparent safety after leaving.
14. The final jump scare is the FIRST and ONLY major conventional jump scare in
    the game.
15. Immediately cut to black after the final scare.
16. Even the final scare should preserve uncertainty about exactly what the
    entity is.
17. Preserve the five-color matte visual direction throughout the entire
    sequence.
18. No bloom.
19. No lens flare.
20. No glossy/specular materials.
21. Peripheral vision mechanics must remain active throughout the sequence.
22. The player's fear should mostly come from what they hear and what they THINK
    they saw.

---

## Design intent

The final act should make the player realize that the game's greatest source of
fear was never actually seeing the threat. For hours the player has trained
themselves to check corners, look behind themselves, study shadows, listen to
footsteps, question objects, use eye tracking to investigate peripheral movement.

When something finally appears to enter the house, all of those habits become
useless. The player hides. Nothing happens. The silence becomes worse than the
chase. Eventually the player convinces themselves it is safe. They leave hiding.
They begin looking again. And only when they finally believe they have regained
control does the game take that control away. Cut to black.

---

## Reconciliation against `AUDIT_REPORT.md`

- **Finding #1 (Day 3 loud-transient/sprint contradiction) — resolved, not
  ignored.** Sprint is confirmed real and intentional (Act 19), scoped narrowly to
  that one running sequence — an explicit, on-the-record exception, not an
  oversight. The chase audio itself (footsteps + cricket-silence, Acts 17–19) is
  NOT a loud transient — it reuses the existing cricket-silence dread technique
  rather than a new sting, so "no loud transients" holds there. The **only** loud-
  transient exception is the single Act 27 jump scare, which the doc itself
  explicitly justifies as a deliberate, one-time violation of that rule — this
  should be reflected in `CLAUDE.md`'s don't-list as a precise, scoped exception,
  not a blanket reversal.
- **Finding #6 (no designed resolution to the mystery) — resolved.** Act 28 is a
  real, designed ending (cut to black, title card, tagline, credits). The identity
  mystery itself isn't necessarily "solved" on-screen, but the *game* now has a
  definitive designed ending, which is what was actually missing.
- **Finding #9 (Act 1/2 single-night structure vs. 3-day structure unmapped) —
  partially resolved, one naming collision worth fixing.** This document
  establishes Day 3 has its own internal beat structure. **Naming collision:**
  the original handoff spec uses "Act 1" / "Act 2" for the single-evening
  structure's two halves; this document uses "Act 1" through "Act 28" for beats
  *within* Day 3 alone. Recommend renaming this document's beats (e.g. "Beat 1–28"
  or "Sequence 1–28") before either gets referenced in code or further docs, to
  avoid two unrelated things both being called "Act" in the same project.
- **No fail state introduced.** The final scare is not a pass/fail branch — it's
  the deterministic ending. This resolves the audit's concern about whether this
  would be the game's first fail state: it isn't one, nothing else changes about
  the game's no-death, no-combat, no-game-over design language.
