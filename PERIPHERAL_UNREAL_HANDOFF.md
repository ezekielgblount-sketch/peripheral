# PERIPHERAL — Unreal Engine Handoff

This is the design + implementation spec for **Peripheral**, a first-person horror
game currently built as a browser game (Three.js + Vite, zero external assets —
every mesh is primitives, every sound is synthesised). It's fully playable at
build/revision **0.3** (source: `C:\Modding\peripheral`, live at
`https://ezekielgblount-sketch.github.io/peripheral/`).

This document exists to port the design to **Unreal Engine**. It captures every
system, every number, and every piece of content so nothing gets lost in
translation — visuals will improve substantially in UE (real lighting, materials,
possibly Nanite/Lumen), but the **mechanic and pacing** need to survive the move
unchanged. Where useful, each section notes which UE system is the natural home
for that piece (Blueprint state machine, Post Process Material, Niagara, etc.).

---

## 1. The core pitch

The game separates what the player is **looking at** from what the player can
**see**. Things go wrong at the edges of the frame and are always ordinary again
by the time the player centres them on-screen. Two systems make this work and
**must stay architecturally separate** in the UE port, same as in the JS build:

1. **The visual falloff** (a post-process effect) — purely cosmetic. Blur,
   desaturation, and dimming that increase with distance from screen centre.
2. **The anomaly state machine** (pure gameplay logic) — decides what is
   actually wrong in the world and when it's safe to change it. This never
   reads the post-process effect and is never hidden by it. A player who
   screenshots and zooms into a corner must see the anomaly is *genuinely*
   there, unblurred by anything but the post effect — the post effect and the
   "did the player see it" logic are two unrelated systems that happen to
   rhyme thematically.

**The one rule that matters most:** an anomaly may never visibly transition
on-screen. It only changes state on a frame where the player's view cone is
far enough away from it, or it's fully occluded. This was verified continuously
during development by scripting camera angles and asserting state transitions
only happened outside the visible cone — worth replicating as an automated or
manual QA pass in UE too.

---

## 2. Foveal / peripheral zones (angle thresholds)

All angle math is done as the angle between the camera's forward vector and the
direction from the eye to a world point (equivalently, dot product / cosine —
UE: `GetForwardVector() | (TargetLocation - EyeLocation).GetSafeNormal()`, or a
plain angle between vectors node).

| Zone | Threshold | Meaning |
|---|---|---|
| **Fovea** | within **11°** of forward | Dead centre. Anomalies resolve here. |
| **Near-periphery** | 11°–26° | Transitional zone, not directly used by any rule but reserved for tuning. |
| **Arm-safe zone** | beyond **40°** (or occluded) | Where an `ARMED` anomaly is allowed to flip to its wrong state. |
| **Resolve dwell** | **0.12 seconds** | How long the fovea must rest on an `ACTIVE` anomaly, unoccluded (raycast-confirmed), before it resolves. |
| **Resolve hysteresis** | fovea threshold widened to **15°** once dwell has started | Prevents flicker for an anomaly sitting right on the 11° boundary — once you've begun looking at it, minor drift doesn't reset the timer. |

Occlusion is checked via a raycast from the eye to the anomaly's anchor point,
ignoring the anomaly's own root actor (so a door can't occlude itself) and
ignoring anything flagged "no-occlude" (glass panes, mirror planes — thin
see-through dressing that shouldn't count as blocking line of sight).

**UE implementation note:** this maps cleanly to a component (`UFoveaComponent`
or similar) on the player pawn that every anomaly actor queries each tick:
`GetAngleTo(WorldPos)`, `IsOccluded(WorldPos, IgnoreActor)`. Keep it as a
service the anomalies pull from, not something that pushes state into them.

---

## 3. The anomaly state machine

Every anomaly-capable object runs the same five-state machine, independent of
what it visually does. **This should be a reusable Blueprint interface or base
class in UE** (`BP_Anomaly` / `UAnomalyComponent`) that every anomaly actor
implements via two functions: `SetOff()` and `SetNormal()` — both **instant**,
no tween, no fade, no sound, no animation.

```
DORMANT   → the Director may select ("arm") it
ARMED     → chosen, but still normal. Flips to SetOff() ONLY on a frame where
            the player's fovea is beyond the 40° arm-safe threshold, OR the
            object is occluded. Never flips near screen centre.
ACTIVE    → visibly wrong. Sits here indefinitely until looked at.
RESOLVING → the fovea has rested within the (possibly hysteresis-widened)
            fovea cone, unoccluded, for >0.12s. On the VERY NEXT tick it calls
            SetNormal() and moves to SPENT. One frame. It must look like it
            was never anything else.
SPENT     → cooldown of 60–120s (random) before returning to DORMANT, AND it
            may only re-arm once the player has left and is in a different
            room than the one it resolved in.
```

Implementation was ~90 lines of plain state-machine logic (`game/anomaly.js`,
`game/fovea.js` in the source) — no physics, no animation blueprints needed for
the state transitions themselves (though the *visual* result of `SetOff`/
`SetNormal` can obviously use whatever UE visual tooling is appropriate, as long
as the change itself is a single instant swap, not a lerp).

### All 12 anomalies (current build)

Each has a "normal" state, an "off" (wrong) state, its home room, and an anchor
point (roughly chest/object height) used for all angle/occlusion math.

| # | Object | Room | Normal | Off |
|---|---|---|---|---|
| 1 | Floor lamp | Living room | Upright, shade level | Base tilts ~6°, shade tilts ~30°, leaning |
| 2 | Wall portrait | Living room | Painted figure faces forward | Head rotated ~62° toward the room |
| 3 | Coat on hook | Entry | Hangs flat (empty) | Hangs with volume — torso, hem, shoulders — as if worn |
| 4 | Kitchen chair | Kitchen | Tucked under the table | Pulled out, turned ~126° to face the hall |
| 5 | Bathroom door | Hallway | Ajar 15° | Wide open, 88° |
| 6 | Hallway phantom door | Hallway | Doesn't exist (invisible) | A fifth doorway (with frame) appears on the west wall where there were four |
| 7 | Bathroom mirror | Bathroom | Empty flat grey plane | A dark humanoid figure stands "in" the reflection |
| 8 | Bedroom window figure | Bedroom | Empty treeline beyond the window | A humanoid figure stands in the trees |
| 9 | Living-room window figure | Living room | Empty yard | A humanoid figure stands outside the window |
| 10 | Hallway-end figure | Hallway | Empty | A humanoid figure stands at the far end of the long hallway sightline, facing back down it |
| 11 | Realtor portrait (exterior sign) | Yard | Agent's face has two dots + a smiling mouth arc | Smile removed — only the two dots remain. Head outline identical; **only the interior of the face changes**. The subtlest anomaly in the game. |
| 12 | Yard sign (exterior sign) | Yard, **Act 2 only** | Full "HOME FOR SALE / SOLD / [buyer name]" sign | SOLD banner and buyer name both absent — a blank line where the name was |

All the "a figure is standing there" reveals (#7, #8, #9, #10) use **one shared
humanoid silhouette mesh** so the presence reads as a single consistent thing
across every reveal — this is deliberate and should carry over to UE (one
Blueprint actor, reused, not a different model per reveal). Model shape: a
simple standing figure, feet planted at ground level (critical — see §9 on a
floating-geometry bug that was fixed during development), slightly hunched, no
face, arms at sides, roughly leaning 3–4° forward. Flat matte near-black
material, no detail.

The Act 2 entity (§6) uses the same shared silhouette, scaled ~1.02×.

---

## 4. The Director (`game/director.js`) and PlayerProfile (`game/profile.js`)

The Director decides **what** goes wrong and **when**, biased by a live profile
of how this specific player looks and moves. It's deliberately simple — a stats
object and a weighted random picker, not machine learning — but it's real and
worth preserving as-is; it's what makes replays feel personalized.

### PlayerProfile — sampled every tick

- **Yaw velocity**: rolling mean and peak (rad/s) → classifies the player as a
  "fast twitcher" (mean > 1.4 rad/s) or a slow sweeper.
- **Dwell histogram**: a coarse angular grid (12 azimuth bins around the
  player's smoothed movement heading × 5 elevation bins, −60° to +60°) tracking
  where the fovea spends time. Used to compute a **neglect score** (0–1) for any
  candidate world position: how far below-average that angular bin's dwell time
  is. A position in a bin the player almost never looks toward scores near 1.
- **Room dwell times and visit order.**
- **Check-behind rate**: fraction of room entries where the player turned more
  than 120° within 3 seconds of entering (i.e., checking what's behind them).
- **Wall-hugging EMA**: how close to a room's edges (vs. its centre) the player
  walks, smoothed over time.

### Director — arming logic

- Only active during Act 1 (with one exception — see the yard sign in §12,
  which is armed once explicitly at the Act 2 transition, not by this loop).
- Picks a new interval every time it arms something: base **25–40s** random,
  nudged −4s for confirmed fast-twitchers or +4s for very slow sweepers
  (floor of 18s).
- To choose *which* dormant anomaly to arm: for every `DORMANT` candidate,
  compute a weight = `(0.15 + neglectScore) × inViewPenalty × roomBonus`, where
  `inViewPenalty` = 0.15 if the player is currently looking almost straight at
  the candidate (cos > 0.9, i.e. within ~26°) else 1.0 (never arm something the
  player is staring at *right now*, even though it won't flip until they look
  away), and `roomBonus` = 0.7 if the candidate is in the player's *current*
  room (mild preference for anomalies in rooms the player isn't already in, so
  the reveal is something they return to). Then a standard weighted-random pick.

**UE mapping**: this is plain gameplay code — a `UPlayerProfileComponent` on
the pawn sampling every tick, and a `ADirectorActor` or subsystem holding a
timer and doing the weighted pick over an array of registered anomaly actors.
No need for Behavior Trees or EQS; this is simpler than that and should stay
simple.

---

## 5. The house — full geometry spec

Single storey. All coordinates in metres, `x` and `z` horizontal, `y` up, floor
at `y = 0`. **Ceiling height 2.5m, doorway width 0.9m, wall thickness 0.15m,
player eye height 1.65m** — keep these; they're tuned to feel "real, cramped,
not cavernous," matching the original design brief.

### Room bounding boxes (x-min, z-min, x-max, z-max)

| Room | x range | z range |
|---|---|---|
| Entry | 4.5 – 7.5 | 0 – 3 |
| Living room | 0 – 4.5 | 0 – 6 |
| Kitchen | 7.5 – 12 | 0 – 6 |
| Hallway | 4.5 – 7.5 | 3 – 14 |
| Bathroom | 0 – 4.5 | 6 – 10 |
| Bedroom | 7.5 – 12 | 6 – 10 |
| Study | 0 – 4.5 | 10 – 14 |
| Utility | 7.5 – 12 | 10 – 14 |

Whole house footprint: 12m × 14m. The hallway (4.5–7.5 × 3–14, ~11m long) is
the longest sightline in the house and where most anomalies pay off, per the
original design brief — preserve this in the UE layout.

### Key anchors

| Anchor | Position (x, y, z) | Purpose |
|---|---|---|
| Spawn (outside) | (6, 0, −6) | Act 1 start, on the gravel path, facing the door |
| Front door | (6, 0, 0) | The only exterior door |
| Entry centre | (6, 0, 1.5) | — |
| Bed | (10.5, 0, 8.4) | Bedroom, ends Act 1 |
| Study wake spot | (2.2, 0, 12.4) | Where the player wakes for Act 2 |
| Breaker box | (11, 0, 14) | On the north exterior wall, deliberately around the dark side of the house |

### Doors

Four interior doorways along the hallway plus the front door — **all now
functionally openable** (E to toggle, current-state-aware prompt: "Open door" /
"Close door"), except:
- The **bathroom door** — its angle is entirely driven by its own anomaly state
  (ajar 15° normal / 88° "wide open" off) and is deliberately *not* manually
  interactive, so the anomaly logic never fights player input.
- The **phantom fifth door** (anomaly #6) — doesn't exist in the normal state,
  so it's never interactive either.

Door leaf: a hinge pivot at one edge, leaf swings to −90° when open, lerped at
rate 6 (i.e., `angle += (target - angle) * min(1, dt * 6)` per tick) for normal
player-driven opens — **except** the bathroom-door anomaly, which snaps
instantly (no lerp) per the "never animate an anomaly transition" rule.

### Windows

Four windows: living room (west wall) and study (west wall), kitchen (east
wall, over the sink) and bedroom (east wall, facing the treeline). Sill height
0.95m, head height 2.05m. Glass is a thin, mostly-transparent pane flagged
"no-occlude" for line-of-sight purposes (an anomaly can be seen or hidden
through it normally, but the glass itself never blocks an occlusion raycast).

### Rooms, walls, and colliders

Every wall segment doubles as a collision volume (axis-aligned box). Floor and
ceiling are also solid collision planes. In the JS build this was ~46
axis-aligned boxes total (house + yard fences etc.) resolved against a vertical
capsule player collider via closest-point-on-rectangle math — in UE this is
just standard wall geometry with collision enabled and a capsule component on
the pawn; nothing special needed here, the JS version was a from-scratch
implementation of exactly what UE gives you for free.

---

## 6. The yard

Fenced perimeter (roughly x: −5 to 17, z: −9 to 17, fence height 1.1m) around
the house, with a gap at the front for the gravel path. A dozen-ish low-poly
conifer silhouettes form a treeline, denser to the east (facing the bedroom
window) and along the back. A gravel path runs from the spawn point to a small
porch (three steps, railing, two posts, a beam, and a flat roof overhang
sheltering the door and the porch light) at the front door.

**Breaker box**: mounted on the exterior north wall near the east corner —
deliberately placed so reaching it means walking around the dark side of the
house, out of sight of the door. Small metal box, a hinged cover, a switch.

### The Act 2 entity

Uses the shared humanoid silhouette (§3). Follows the exact same rules as every
anomaly:
- Only ever occupies positions **outside the player's fovea** (spawned at least
  ~55–110° off the player's current forward, checked again after placement to
  confirm it's genuinely outside a 42° cone).
- Holds perfectly still.
- **Removed the exact frame the player centres it** (within the 11° fovea cone,
  unoccluded) — it does not fade or flee, it's just gone.
- Each time it's dismissed this way, its next placement distance shrinks by 2m
  (floor of 4m) and a 3–6s cooldown passes before it reappears elsewhere.
- It does not chase, does not touch the player, cannot kill them. This is by
  design and should **not change** — it's a scoped, controlled scare.

**The cricket-silence cue** (arguably the single best scare in the build,
worth extra care in the UE port): a continuous ambient cricket-bed sound plays
outside. Whenever the entity is within **15m** of the player and has an
unoccluded line of sight, the crickets **stop abruptly** (~0.4s fade, not
instant, not a slow fade — fast). They resume **6 seconds** after the entity is
no longer near/visible (~0.6s fade back in). This is never explained to the
player, and never should be.

---

## 7. Player controller

- **Movement**: WASD relative to yaw only (no vertical look affects movement
  direction). Walk speed **2.6 m/s**, Shift-held slow walk **1.3 m/s**. There is
  intentionally no run — default pace is already unhurried, per the original
  design brief; do not add a sprint.
- **Collision**: vertical capsule, radius 0.3m, height 1.7m, resolved against
  axis-aligned world geometry.
- **Camera**: standard yaw/pitch mouselook, pitch clamped to just under ±90°,
  sensitivity tuned to feel deliberate rather than twitchy (exact JS value was
  0.0022 rad per mouse-movement-unit — treat as a starting point, UE's
  different input pipeline will need its own tuning pass).
- **Eye height** 1.65m while standing (feet at y=0).

### The flashlight (Act 2 only)

This was **widened significantly during development** after a review pass
flagged that a narrow beam undermines the entire peripheral mechanic (nothing
visible off-centre = nothing to notice going wrong off-centre). Final spec:

- **Hot cone**: ~38° full angle, ~26m range, moderate penumbra/falloff
  (equivalent Unreal spotlight: `InnerConeAngle` ~13°, `OuterConeAngle` ~19°
  as a starting translation, tune to taste — the JS SpotLight penumbra
  parameter doesn't map 1:1).
- **Dim wide fill**: ~82° full angle, ~15m range, low intensity — enough that
  shapes are *noticeable* at the edge of vision without being *identifiable* at
  a glance. This is the important one for the mechanic; don't cut it to save
  performance.
- Colour: warm (`#FFE6B8`) — **the only saturated/warm colour permitted
  anywhere in the game.** Everything else stays in the grey/beige palette (§10).
- Never runs out of battery in this build (no battery mechanic — don't add one
  without a design conversation first, it wasn't asked for).

---

## 8. Full act flow

### Act 1 — Settling in

1. Player spawns outside on the gravel path at (6, 0, −6), flat grey daylight,
   facing the door.
2. Walk in, open the door (any door now, but the front door is the entry point).
3. After ~8 seconds inside, a HUD line fades in low on screen: *"Settle in.
   Unpack, wash up, then get some sleep."*
4. Two optional, **non-gating** chores are available:
   - **Unpack** at the dresser (bedroom) — interacting slides a drawer open
     (animated lerp, ~5 rate) and marks the chore done.
   - **Shower** — interacting **freezes player input for 10 real seconds**
     (movement and look both locked; this uses a countdown ticked in the fixed
     update loop, not a real-time timer, so pausing the game genuinely pauses
     the shower too). During the freeze: a filtered running-water sound plays,
     an animated translucent water column + six looping droplet streaks appear
     under the showerhead behind a ribbed multi-strip curtain, and a slow,
     dissonant 5-note descending piano phrase plays (~9–11s, roughly filling
     the freeze). At the end, control returns and the chore completes.
   - Completing both updates the HUD objective text; completing neither is
     completely fine.
5. **The bed is never gated.** A player who beelines straight for it can sleep
   in under 30 seconds — Act 2 just has a thinner player-profile to work with
   as a consequence, not a blocked path.
6. During Act 1, the Director is active (see §4), arming one anomaly roughly
   every 25–40 seconds.
7. Interacting with the bed ends Act 1.

### Transition

Screen fades to black (1.2s), audio cuts to true silence, holds for **3
seconds**, then a single low sub-bass swell plays (~3s, peaking around 1.2s
in), then a further ~2.6s beat before Act 2 begins. Total transition is
roughly 6–7 seconds of held tension — resist the urge to shorten this.

### Act 2 — The power

1. Player **wakes on the study floor** (not the bedroom — this is deliberate
   misdirection), at (2.2, 0, 12.4), camera starting tilted (pitch ≈ −0.55 rad,
   plus a decaying camera roll of 0.5 rad) and righting itself smoothly over
   **2 seconds** (cubic ease-out). Player input is locked during this.
2. All interior lights are dead. The flashlight turns on (§7). Objective line:
   *"The breaker is outside."*
3. Exterior is genuinely dark: near-black ambient, a faint cold moonlight
   directional light (~0.08 intensity), treeline barely separable.
4. The entity (§6) roams per its rules; crickets gate on proximity.
5. Player must leave the house, walk to the breaker's dark corner (11, 0, 14),
   and interact.
6. **Flipping the breaker**: power returns (interior lights back on, porch
   light on), yard/interior colours warm back toward the daytime palette,
   crickets return loudly/immediately (no fade-in — the threat has visibly
   passed), the entity is hidden and does not return. This does **not** end
   the game yet — see the epilogue below.

### Epilogue — key and lock-up (new in revision 0.3)

This was added specifically to give the ending more weight — instead of the
game simply stopping the moment the lights come back, the player has one more
small, quiet task.

1. On breaker flip: new phase, objective *"Find your keys and lock up before
   you go."* A house key (small prop — ring + shaft + one tooth, on the entry
   table) becomes interactable.
2. Player goes back inside, picks up the key ("Take the key"). This:
   - Hides the key mesh.
   - **Disables** the normal front-door open/close interactable.
   - **Enables** a new interactable at the exact same spot: "Lock the door".
   - Updates the objective: *"Lock the door on your way out."*
3. Interacting with the door at that point force-closes it (regardless of its
   current open/closed state) and locks it — this triggers the actual ending:
   fade to black (~1.6s hold, ~0.9s fade), then the end card.

### Ending

A plain card: **"PERIPHERAL — END OF BUILD 0.1"** (version string should be
bumped for the UE build) with a "return to menu" option. No jumpscare, no
final reveal, no written lore — consistent with the original brief's explicit
"don't" list (see §13).

---

## 9. Signage (exterior, revision 0.2 addition)

All hand-authored on the JS side as `<canvas>`-drawn textures — in UE this
becomes either baked textures or, if you want the name to stay dynamic and
private, a Render Target + UMG/Slate-drawn text, or simplest: a runtime
material parameter collection driving a text render component. The *design*
intent matters more than the literal implementation:

- **Buyer name**: on the main menu, a single quiet text field labelled "BUYER"
  under a thin rule (styled like a line on a realtor's form — no modal, no
  explanatory prompt). Persisted locally only (in the JS build: browser
  `localStorage`; in UE: local save game / config, **never networked**).
  Sanitised: trimmed, capped at 22 characters, letters/space/hyphen/apostrophe
  only, rendered UPPERCASE. Empty input falls back to **"NEW OWNER"** — a
  deliberate, not-broken-feeling default.
- **Yard sign**: at the end of the gravel path, angled toward the road, two
  posts, ~0.9×0.6m board, reads "HOME FOR SALE" / rule / "SOLD TO" / the
  buyer's name, with a crooked ~20°-rotated hand-applied "SOLD" banner across
  one corner. This is an **anomaly** — see #12 in §3: in Act 2 only, the name
  and SOLD banner are simply absent.
- **Realtor placard**: smaller, stapled to the fence near the gate — agency
  name, a fake phone number, a flat vector portrait (circle head, simple
  shoulders, two dots for eyes, a curved smile). This is **also an anomaly** —
  see #11 in §3: the smile disappears, nothing else changes.
- **Two OPEN HOUSE flyers**: stapled to the fence and a porch post, rain-faded,
  barely legible. Pure set dressing, no interactivity, no anomaly behavior.
- **Inspection notice**: small card on the front door, checkboxes all ticked,
  reads "STRUCTURE — NO FINDINGS." Pure set dressing.
- All signage is drawn with a "weathered" treatment — uneven ink, blotches,
  speckle noise, a couple of percent rotation off true. Nothing in this world
  is crisp; carry that texture-work ethos into whatever UE does for these
  (even baked textures should not look print-perfect).
- **Privacy rule to preserve exactly**: the buyer's name appears **once**, on
  the yard sign, and then later, conspicuously does not. It is never repeated
  anywhere else in the game, never addressed to the player, never spelled out
  as a threat. Don't add uses of the name beyond this.

---

## 10. Art direction / palette

Flat, matte, desaturated. Only five colours in the entire game, plus one
deliberate exception:

| Name | Hex | Use |
|---|---|---|
| Black | `#1A1916` | Darkest — shadows, dark figures |
| Dark | `#4E4B44` | Wood, trim, fences, dark fabric |
| Mid | `#7C7870` | Metal, chairs, mid-tone surfaces |
| Light | `#B3A78F` | Walls, counters, pale fabric |
| Pale | `#E6DFCC` | Ceilings, lightest surfaces, title text |
| **Warm (exception)** | `#FFE6B8` | **Only** the Act 2 flashlight beam. Nothing else in the game may be warm/saturated. |

Materials: roughness 1, metalness 0 throughout (matte everywhere) — no
specular highlights, no glints, because a glint would tell the player where to
look, and this game is entirely about controlling that. **This is a hard
constraint carrying into UE**: keep roughness maxed and metallic at zero on
every surface material; resist the temptation to add PBR detail that
introduces highlights. No bloom, no lens flare, no colour-grading LUT beyond
what's described here.

Lighting:
- **Act 1**: dim ambient + a hemisphere light + five weak point lights in
  household fixtures (living room lamp, kitchen, hallway ×2, bathroom).
  Overcast/stale feeling, not dark.
- **Act 2**: near-black ambient, a very faint cold-moonlight directional light,
  the flashlight doing almost all the work. Save the true dark for here.

---

## 11. The peripheral post-process effect

This is the visual half of the core mechanic (§1) — cosmetic only, never
gameplay-authoritative. JS implementation: render scene to a target, then a
single fullscreen shader pass. **UE equivalent: a Post Process Material**
(or a custom post-process pass if more control is needed) applied via a Post
Process Volume covering the whole level (or unbound, global).

Algorithm (GLSL logic, portable to a UE material graph or custom HLSL node):

```
r = distance from screen centre (UV 0.5,0.5), aspect-corrected, normalized so
    ~1.0 = screen edge, ~1.4 = corners
p = smoothstep(0.20, 0.95, r)         // "peripheral amount" — ~20% of the
                                       // screen radius stays fully sharp,
                                       // then degrades quickly past that
color = radialBlur(scene, uv, p * blurStrength)   // 8-tap radial blur,
        taps offset along the direction from centre to this pixel, scaled by p
color = mix(color, luminance(color), p * 0.82)     // desaturate toward grey
color = color * mix(1.0, 0.55, p)                  // dim toward the edges
```

Tuning notes from the JS build:
- The blur offset scale was small (`p * 0.006` in UV space at the render
  target's resolution) — 8 taps was enough to read as "mush" without an
  obvious box-blur look; more taps read better if perf allows.
- Desaturation was pushed hard (0.82 mix factor) — the edges should look
  closer to black-and-white than full colour even before considering the blur.
- Brightness dropped to 55% at full periphery.
- **Do not substitute a vignette for this effect.** A vignette darkens edges
  but doesn't blur or desaturate, and testing showed the blur+desaturation
  combination is what actually sells "you can't resolve detail out there,"
  which is the entire point.
- This pass runs at 60fps target on integrated graphics at 1080p in the JS
  build and was the single most expensive part of the frame — worth profiling
  early in UE since Post Process Materials have their own cost profile.

---

## 12. Audio design

Every sound in the JS build is synthesised at runtime via the Web Audio API —
no audio files. In UE this maps to **MetaSounds** (recommended — UE5's
node-based synthesis graph is a very close conceptual match to what was built)
or, if simplicity is preferred, pre-rendered one-shot/loop assets baked once
from equivalent synthesis and imported normally. Either is fine; the important
thing is the *design*, not the literal DSP implementation:

- **House tone**: a very low (54Hz + 55.3Hz, i.e. a slow ~1.3Hz beat/detune),
  quiet drone through a lowpass filter, active while inside during Act 1.
  Fades in/out over ~0.6s.
- **Cricket bed**: band-limited filtered noise with a fast (~13Hz) tremolo for
  a trill character, continuous outside. Gates per the entity-proximity rule
  in §6 — this is the single most important sound cue in the game; treat it
  with more care than anything else in the audio pass.
- **Airy piano ambient**: sparse, slow, struck-note synth piano (a few sine
  partials through a lowpass envelope, ~2.6s decay per note) through a
  generated convolution reverb (a ~2.8s decaying noise impulse) for air/space.
  One or two notes at a time, spaced 5.5–13.5s apart depending on act (Act 1:
  brighter, A-minor-ish scale, more frequent; Act 2: lower register, sparser).
  Silenced entirely during the Act 1→2 transition for the held-silence beat.
- **Shower cue**: a distinct 5-note **descending, dissonant** phrase (closer
  chromatic/tritone-flavored intervals rather than the open ambient scale),
  timed to roughly span the 10-second shower freeze.
- **Sub-bass transition swell**: two close sine oscillators (38Hz + 41Hz)
  ramping up over ~1.2s and back down over ~1.8s — plays once, after the held
  silence, going into Act 2.
- **Thud**: short pitch-dropping sine (160Hz→60Hz) with a fast decay — used for
  doors, picking up the key, generic soft impacts.
- **Clack**: short filtered noise burst (highpass ~1500Hz) — used for the
  breaker switch and locking the door. Distinct from "thud," reads as a firm
  mechanical action.
- **Footsteps**: filtered noise bursts, triggered every ~0.72m of travel,
  timbre differs by surface — lowpass/warm for wood floors indoors, bandpass
  for gravel outdoors. Surface is inferred from whether the player is inside
  any room's bounding box.
- **Running water** (shower): bandpass+highpass filtered looping noise, faded
  in/out over 0.3–0.4s around the shower freeze window.

General mixing note: everything stays quiet and textural except the two
"event" sounds (swell, clack) — the game should never have a loud transient
moment. This is a hard constraint from the original brief (§13) and should
guide MetaSound graph levels directly: no sound in this game should read as a
jump-scare sting.

---

## 13. Explicit constraints (preserve these — they are the whole design point)

Carried over verbatim from the original design brief and reconfirmed during
development. These are not suggestions:

- **No jumpscares, screamer stings, or loud transients**, ever. Nothing in the
  game confirms itself. If a UE feature (Sequencer camera shake, a stinger
  sound cue, whatever) is being considered "to make it scarier," the answer is
  no — the fix for "doesn't feel scary" in this design is *visibility* (making
  sure something is genuinely perceivable in peripheral vision, per the
  flashlight widening in §7) and *pacing*, not a startle.
- **No blood, gore, or written lore.** The house is ordinary and that's the
  horror. Nothing should explain the anomalies or the entity.
- **The entity never chases, touches, or kills the player.** It gets closer
  each time it reappears, and that's the entire escalation — do not add a
  catch/death state without a design conversation.
- **No stamina bar, inventory, collectibles, or notes to read.** The key (§8
  epilogue) is a narrow, deliberate exception — one object, one use, no
  inventory UI, picked up and consumed immediately by its single interaction.
  Don't generalize this into a broader item system.
- **No post-processing beyond the one peripheral pass** (§11) — no bloom, no
  chromatic aberration, no film grain, no colour grading LUT stacked on top.
- **The buyer name appears exactly once** (§9) and is never sent anywhere,
  never logged, never used for analytics. Treat it as sacred local-only data.
- Roughly **8 minutes** end to end is the target pacing for a full playthrough
  (Act 1 + transition + Act 2 + epilogue).

---

## 14. Menu / UI flow

Three items on the main menu: **Start**, and (below it) the quiet BUYER text
field (§9) — no separate "enter your name" screen, no modal. Pause is bound to
Escape, dims the last frame rather than blanking it, offers Resume / Exit to
menu. Exit-to-menu language explicitly notes a browser tab can't close itself
— **this specific copy doesn't need to carry over to UE** (a standalone build
*can* quit), but the underlying idea — no unnecessary "are you sure" friction,
menu always reachable, no settings/options/graphics presets in this build —
should.

HUD: a single faint centre dot (not a full crosshair), low-on-screen fading
objective text lines (fade in over ~1.4s, hold, fade out — see the exact
objective copy throughout §8), and a small `[E] <action>` interact prompt that
tracks whatever the player's centred on within range. Controls are shown once
on the main menu and never repeated as on-screen tutorial text during play.

Controls: **WASD** move, mouse look, **Shift** walk slower, **E** interact,
**Esc** pause. No jump, no crouch, no sprint.

---

## 15. Source reference map (for translating logic 1:1 if useful)

The JS/Three.js source is organized as below — useful if a programmer wants to
read the actual logic rather than just this spec while building the UE
equivalent. All paths relative to `C:\Modding\peripheral\src\`.

```
main.js                 bootstrap, fixed-step game loop, interaction dispatch
constants.js             every tunable number in one place (§2, §5, §7 sourced from here)

core/
  renderer.js             render target + resize handling
  input.js                pointer lock, keyboard, mouse delta, interact edge
  audio.js                ALL synthesis — every sound in §12 is here
  collision.js             capsule-vs-AABB resolve()
  loop.js                  fixed-step update / variable-rate render

world/
  house.js                 room geometry, walls, windows, doors, room bounds, anchors (§5)
  yard.js                   fence, treeline, porch, breaker box (§6)
  props.js                  every furniture + anomaly prop (§3), chores (§8), the key
  figure.js                 the one shared humanoid silhouette mesh (§3)
  lighting.js               Act 1 / Act 2 light rigs (§10)
  signage.js                all exterior signs, buyer-name canvas rendering (§9)

game/
  player.js                 movement, camera, flashlight (§7)
  fovea.js                  angle tests + occlusion raycasts (§2)
  anomaly.js                 the 5-state machine (§3)
  director.js                 arming logic + pacing (§4)
  profile.js                   PlayerProfile stats (§4)
  acts.js                       Act 1 / transition / Act 2 / epilogue / ending (§8)

fx/
  peripheral.js             the post-process shader (§11)

ui/
  menu.js                   main menu, pause, end card, buyer field (§14)
  hud.js                     objective lines, interact prompt, screen fades

util/
  text.js                    buyer-name sanitisation (§9)
```

Total source is ~130KB across ~28 files — small enough to read end-to-end in
an afternoon if a line-by-line port is ever wanted instead of a fresh UE
implementation from this spec.

---

## 16. What's explicitly left for the UE team to improve

The brief always said Unreal will make this look better — here's where the JS
build was deliberately kept simple and UE should be allowed to do more:

- **Lighting/shadows**: JS used basic PCF soft shadows on one shadow-casting
  light at a time for performance. UE's Lumen/ray-traced options can do this
  properly — but keep the *exposure levels* and the Act 1 "overcast, not dark"
  vs. Act 2 "genuinely dark" feel matched to §10.
- **Materials**: flat MeshStandardMaterial (roughness 1, metalness 0) with
  vertex colours only. UE can add subtle surface variation (fabric weave,
  wood grain) as long as **no specular highlight or glint becomes visible** —
  this is a hard constraint (§10), not a suggestion to relax.
- **The humanoid silhouette** (§3): currently built from boxes. A sculpted or
  better-proportioned mesh is very welcome — keep it faceless, matte,
  near-black, and still (no idle animation) to preserve the "is that... no,
  it's nothing" ambiguity.
- **Signage textures** (§9): currently canvas-drawn at runtime. Static baked
  textures in UE are fine and will look better — just keep the buyer-name
  portion dynamic somehow (render target, runtime material parameter, or
  simplest: swap between a couple of pre-baked "blank" variants and composite
  text) since it has to reflect what the player typed.
- **Water/shower effect** (§8): currently a translucent cylinder + a handful
  of looping cylinder droplets. This is a great candidate for a proper Niagara
  particle system in UE — keep the ~10 second duration and the "curtain
  mostly obscures it" framing.

Everything else in this document is a **constraint**, not a starting point —
the pacing, the state machine rules, the angle thresholds, the audio cues, and
the explicit "don't" list in §13 are the actual design and should transfer
as close to verbatim as the engine allows.
