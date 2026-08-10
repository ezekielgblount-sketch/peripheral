# Peripheral — Unreal Engine build

Horror game about the gap between what you're **looking at** and what you can **see**.
Things go wrong at the edge of the frame and are ordinary again by the time you centre them.

## The spec is not in this file

`PERIPHERAL_UNREAL_HANDOFF.md` at repo root is the **source of truth** for every
number, every anomaly, every audio cue, every threshold. Read it before implementing
anything. This file only covers how we work in Unreal.

If this file and the handoff spec disagree, **the handoff spec wins.**

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

1. **The peripheral post-process** (blur + desaturate + dim toward screen edges).
   Purely cosmetic. Never gameplay-authoritative.
2. **The anomaly state machine.** Pure gameplay logic. Never reads the post-process,
   never hidden by it.

They rhyme thematically. They must not touch in code.

### The one rule that matters most

**An anomaly may never visibly transition on-screen.** It changes state only on a
frame where the player's view cone is far enough away, or it's fully occluded.
`SetOff()` and `SetNormal()` are **instant** — no tween, no fade, no sound, no
animation. One frame. It must look like it was never anything else.

## Conventions

```
unreal/Peripheral/       (.uproject lives here — this is the project root)
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
- Palette is five colours (spec §10). The Act 2 flashlight warm `#FFE6B8` is the
  only saturated colour permitted anywhere in the game.

## The "don't" list (spec §13 — not suggestions)

- No jumpscares, screamer stings, or loud transients. Ever.
- No blood, gore, or written lore.
- The entity never chases, touches, or kills the player.
- No stamina, inventory, collectibles, or notes. No jump, no crouch, no sprint.
- No post-processing beyond the single peripheral pass.
- The buyer's name is local-only. Never networked, never logged, never analytics.

If something "doesn't feel scary," the fix is **visibility and pacing**, never a
startle.

## Workflow

- **`AGENT_LOG.md` at repo root is the review point.** After a work session,
  write a short entry there: what changed, whether it was pushed, what's next.
  Commit locally always. **Ask before pushing** unless the human driving the
  session has already said to push — either teammate should be able to read the
  log, check `git diff`, and decide before it goes to the remote.
- One driver at a time. Unreal has no live multi-user editing. Discord call, one
  person streams and drives, everyone else feeds ideas.
- Push when you finish a chunk, say so in chat, next person pulls before starting.
- `.uasset` and `.umap` are binary and **cannot be merged**. If two people edit the
  same asset, one version wins. This is why push-then-pull is a rule, not a habit.

## Current state

- Repo also contains the original browser prototype (Three.js + Vite) at root, live
  at `ezekielgblount-sketch.github.io/peripheral`. **Do not move those files** — the
  GitHub Pages workflow builds from root. The Unreal project lives in `unreal/` only.
- Unreal build: starting fresh from the handoff spec. Not a line-by-line port.

### Next up

First slice: block out the hallway, strip the First Person template (no gun, no
jump), and get **one** anomaly running the full five-state machine — anomaly #10,
the hallway-end figure. Grey box and a black capsule. If the look-away/look-back
loop feels right, everything else is content.
