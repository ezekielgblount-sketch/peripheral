# Isolation — Unreal Engine build (formerly Peripheral)

Horror game about the gap between what you're **looking at** and what you can **see**.
Things go wrong at the edge of the frame and stay uncertain even when you centre them.

## Project direction (2026-08-09 — read this first)

**Isolation supersedes Peripheral as the design.** Peripheral was a 2-hour brainstorm
prototype; Isolation is the matured version from the rest of the team, bigger in
scope, and it's the direction now. Team's explicit rule: **when the two designs
conflict, default to Isolation.** Not case-by-case — a standing rule.

`FEATURE_LIST.md` at repo root has the full comparison: what's resolved, what's new,
what's a straight duplicate. Read it before building anything the "don't" list below
would otherwise block — several of those rules have already flipped.

Project renamed: `unreal/Isolation/Isolation.uproject` (was `unreal/Peripheral/
Peripheral.uproject`). GitHub repo itself is still named `peripheral` — that's
Ezekiel's call as owner, deliberately left alone (live public Pages URL).

## The spec is not in this file

`PERIPHERAL_UNREAL_HANDOFF.md` at repo root is still the **source of truth for
mechanics and numbers not touched by the Isolation pivot** — most of the anomaly
system, the fovea/occlusion math, movement, audio design principles all carry over
unchanged (see `FEATURE_LIST.md`'s "Duplicates" section). Read it before implementing
anything. But where `FEATURE_LIST.md` records a resolved conflict, **that resolution
wins over the handoff spec**, not the other way around.

## Hard environment rules

- **Unreal Engine 5.8 exactly.** Not 5.7, not 5.9. Both machines match to the point
  release. Version mismatch is the #1 thing that breaks this workflow. 5.8 is also
  the only version with the embedded MCP server — the whole workflow depends on it.
- **Blueprints, not C++.** Nobody on this team writes code. When C++ breaks at 2am,
  nobody can debug it. If something seems to need C++, ask first.
- **MCP boot order: Unreal Editor fully open FIRST, then launch Claude Code from
  `unreal/`.** Reversed, MCP won't connect.
- **Commit before any significant agent work.** The MCP plugin is experimental and
  write-capable. The commit is the undo button.

## UNITS: the spec is metres, Unreal is centimetres

**Multiply every number in the handoff spec by 100.**

| Spec | Unreal |
|---|---|
| Ceiling 2.5 m | 250 uu |
| Eye height 1.65 m | 165 uu |
| Walk 2.6 m/s | 260 uu/s |
| Shift-walk 1.3 m/s | 130 uu/s |
| House 12 × 14 m | 1200 × 1400 uu |
| Doorway 0.9 m | 90 uu |
| Wall thickness 0.15 m | 15 uu |

Angles and seconds carry over unchanged (11°, 40°, 0.12 s).

Get this wrong once and every measurement after it is poisoned.

### Axes also don't match — this is a separate bug from the units one

The spec says so itself (§5): **"x and z horizontal, y up."** That's a
Three.js/web convention. **Unreal is x and y horizontal, z up.** The spec's
horizontal `z` axis is Unreal's `Y`, not Unreal's `Z` — copying axis letters
literally builds everything sideways (a "hallway" becomes a vertical shaft).

| Spec axis | Unreal axis |
|---|---|
| x (horizontal) | X |
| z (horizontal) | **Y** |
| y (up) | **Z** |

Worked example — the hallway (spec: x 4.5–7.5, z 3–14, in metres):
**Unreal X 450–750, Y 300–1400**, floor Z=0, ceiling Z=250.

Apply this to every room bound, anchor point, door, and window in §5 and §6 —
not just the hallway.

## Unreal's defaults violate our art direction

UE5 ships these **on by default**, and spec §13 forbids every one:

- Bloom
- Auto-exposure / eye adaptation
- Motion blur
- Lens flare
- Chromatic aberration
- Film grain

Fix: one **Post Process Volume, Unbound**, covering the level, with all of the above
zeroed and exposure locked to a fixed EV.

Also: spec §10 requires **roughness 1, metallic 0, and no specular highlights.**
Unreal's default material Specular is **0.5** — set it to **0** on every material.
A glint tells the player where to look, and controlling that is the entire game.

## Architecture: two systems that must stay separate

1. **The peripheral post-process.** Purely cosmetic. Never gameplay-authoritative.
   **Technique is changing per the Isolation pivot** — see below, don't build the
   handoff spec's version.
2. **The anomaly state machine.** Pure gameplay logic. Never reads the post-process,
   never hidden by it. This part is a confirmed duplicate between both designs —
   build it as the handoff spec describes, no change needed here.

They rhyme thematically. They must not touch in code.

### The one rule that matters most

**An anomaly may never visibly transition on-screen.** It changes state only on a
frame where the player's view cone is far enough away, or it's fully occluded.
`SetOff()` and `SetNormal()` are **instant** — no tween, no fade, no sound, no
animation. One frame. It must look like it was never anything else. This rule is
unchanged by the Isolation pivot.

### Peripheral vision technique — resolved in favor of Isolation (was open, see FEATURE_LIST.md #2)

The handoff spec's technique (radial blur + desaturate, ~20% of screen radius fully
sharp, dead centre always 100% clear) is **not what gets built**. Isolation's model:

- **Detail-reduction, not blur** — reduce internal edges, texture, and contrast
  differentiation while preserving silhouettes. Don't substitute a blur pass.
- **Nothing ever reaches full clarity, even centred, even under deliberate sustained
  focus.** Cap around 60–70% clarity at best. An anomaly's *state* (is it in its
  "wrong" configuration or not) stays a clean binary ground truth in the state
  machine — what's capped is the player's ability to visually *confirm* which one
  they're looking at. The uncertainty lives in the rendering layer, not the game
  state.
- This directly affects the not-yet-built post-process pass (handoff §11). Doesn't
  affect the anomaly state machine or fovea/occlusion math — those are unchanged.

## Conventions

```
unreal/Isolation/       (.uproject lives here — this is the project root)
  Content/
    Blueprints/    BP_Anomaly (base), BP_Director, BP_PeripheralCharacter
    Components/    FoveaComponent, PlayerProfileComponent
    Levels/        L_House
    Materials/     M_Flat (roughness 1, metallic 0, specular 0)
    Audio/         MetaSounds
```

- Anomaly actors implement the base class and override `SetOff()` / `SetNormal()`.
- `FoveaComponent` is a **service the anomalies pull from** — `GetAngleTo()`,
  `IsOccluded()`. It never pushes state into them.
- ~~Palette is five colours (spec §10). The Act 2 flashlight warm `#FFE6B8` is the
  only saturated colour permitted anywhere in the game.~~ **Superseded — final
  palette confirmed twice (`VISUAL_REFERENCE.md`, `HOUSE_ENVIRONMENT_SPEC.md`),
  zero exceptions, including the flashlight:**

  | Name | Hex |
  |---|---|
  | Void Charcoal | `#0B0A08` |
  | Soot Brown | `#211E1A` |
  | Dust Taupe | `#49433D` |
  | Dead Beige | `#776F65` |
  | Faded Bone | `#C8C1B6` |

  Materials already built against the old palette (`#1A1916` family) need
  redoing — this is a real, known rework item, not optional cleanup.

## The "don't" list (spec §13 — still true except where Isolation overrides it)

- ~~No jumpscares, screamer stings, or loud transients. Ever.~~ **One narrow,
  explicit exception: the single Act 27 jump scare in `DAY3_FINAL_ACT_SPEC.md` —
  the game's one and only ending, deliberately justified in that doc as landing
  hard *because* it's the only violation of this rule in the whole game. Not a
  precedent for anything else. Everywhere else, including the Day 3 chase itself
  (Acts 17–19, footsteps + cricket-silence), this rule still holds exactly as
  written — that sequence reuses the existing quiet dread technique, not a new
  sting.**
- No blood, gore, or written lore. **(unchanged)**
- ~~The entity never chases, touches, or kills the player.~~ **Isolation has a Day 3
  running-footsteps/back-door sequence that reads as chase-adjacent — build to
  Isolation's version. It still never touches/kills the player (that part holds);
  the "never approaches fast" part doesn't. See `DAY3_FINAL_ACT_SPEC.md`.**
- ~~No stamina, inventory, collectibles, or notes.~~ **Isolation's collectible-memory
  and comfort-item-attrition systems are a core pillar — build them.** No stamina,
  no jump, no crouch still hold everywhere. ~~No sprint~~ **one narrow exception:
  Act 19's running-inside sequence in `DAY3_FINAL_ACT_SPEC.md`, player-controlled,
  scoped to that sequence only — not a general movement-system change.**
- No post-processing beyond the single peripheral pass — **still true, but see the
  Isolation vision-technique section above for what that pass actually is now.**
- The buyer's name is local-only... **N/A, Isolation has a named protagonist
  (Jack), not an anonymous player — the buyer-sign mechanic is retired. See
  `FEATURE_LIST.md` #1.**

If something "doesn't feel scary," the fix is **visibility and pacing**, never a
startle. This one's unchanged.

## Workflow

- **`AGENT_LOG.md` at repo root is the review point.** After a work session,
  write a short entry there: what changed, whether it was pushed, what's next.
  Commit locally always. **Ask before pushing** unless the human driving the
  session has already said to push — either teammate should be able to read the
  log, check `git diff`, and decide before it goes to the remote.
- One driver at a time. Unreal has no live multi-user editing. Discord call, one
  person streams and drives, everyone else feeds ideas.
- **Only the Unreal-connected session commits `unreal/`.** A second Claude session
  working the same local checkout in parallel (docs, chat-driven git ops, whatever)
  must not `git add`/`commit` anything under `unreal/` — that session doesn't know
  about OFPA's save lag (external-actor package files can land on disk a beat
  *after* the main asset save) and can commit a level mid-write. Root-level docs
  (`CLAUDE.md`, `FEATURE_LIST.md`, `AGENT_LOG.md`, etc.) are fine from either
  session, same rule as always — commit locally, ask before pushing.
- Push when you finish a chunk, say so in chat, next person pulls before starting.
- `.uasset` and `.umap` are binary and **cannot be merged**. If two people edit the
  same asset, one version wins. This is why push-then-pull is a rule, not a habit.

## Current state

- Repo also contains the original browser prototype (Three.js + Vite) at root, live
  at `ezekielgblount-sketch.github.io/peripheral`. **Do not move those files** — the
  GitHub Pages workflow builds from root. The Unreal project lives in `unreal/` only.
- Unreal build: starting fresh from the handoff spec. Not a line-by-line port.

### Next up

First slice (movement, one anomaly's state machine, the full house grey-boxed,
doors, flashlight, day/night toggle) is done — see `AGENT_LOG.md` for the full
build history. Currently in the playtesting/bug-fixing pass on that build.

`DAY3_FINAL_ACT_SPEC.md` — the full final-act design, from Ezekiel — is written
and implementation-ready, but **deliberately not being built yet.** Per the agreed
build order: prove the core loop, the space, and the visual/audio identity first;
the big Isolation-scale systems (this spec, collectibles, comfort-item attrition)
are Phase 4, after the smaller single-evening experience is solid. Don't start on
it just because it's ready — wait for an explicit go-ahead.
