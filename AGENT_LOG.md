# Agent Log

Running record of what Claude did in each work session, in reverse-chronological
order (newest first). Written so either human can read a session's entry, look at
the diff, and decide whether to push — without needing to have watched the stream.

Convention: Claude commits locally with a clear message. **Pushing is a separate,
human decision** — read the entry below, check `git log` / `git diff`, then push
if it looks right.

---

## Session — 2026-08-09 (FoveaComponent + BP_Anomaly state machine)

**Did:**
- Built `FoveaComponent` (`/Game/Components/FoveaComponent`, `ActorComponent`)
  per handoff spec §2: `GetAngleTo(WorldLocation) -> Angle` (finds the owner's
  camera via `GetComponentByClass`, angle between camera forward and the
  normalized eye→target direction, via dot product + `Acos(Degrees)` — no
  separate radians conversion needed, that node returns degrees directly) and
  `IsOccluded(WorldLocation, IgnoreActor) -> bool` (line trace, Visibility
  channel, from camera eye to target, ignoring `IgnoreActor`).
- Built `BP_Anomaly` (`/Game/Blueprints/BP_Anomaly`, base `Actor`) per §3's
  five-state machine (DORMANT/ARMED/ACTIVE/RESOLVING/SPENT). State is a plain
  `int` (`CurrentState`, 0-4) rather than a Blueprint enum — attempting to
  create a `UserDefinedEnum` through the Blueprint-creation tool froze the
  live MCP-connected editor behind an unresponsive error dialog mid-session
  (see caveat below); the int fallback has identical behavior, just less
  self-documenting in the variable list, worth revisiting if a proper enum
  path turns up later. `SetOff()`/`SetNormal()` are each a single
  `SetVisibility` call on the mesh — no timeline, no interpolation, confirmed
  instant. `EventTick` implements the transition rules verbatim: ARMED→ACTIVE
  only when fovea angle > 40° or occluded; ACTIVE→RESOLVING after a 0.12s
  dwell inside the fovea cone (11°, widened to 15° once dwell has started)
  unoccluded; RESOLVING calls `SetNormal()` and moves to SPENT on the very
  next tick, nothing more. DORMANT/SPENT are no-ops — Director/re-arm timing
  is intentionally not built yet. Debug hook: `F9` (via `AutoReceiveInput`)
  calls `DebugForceArm()`, which flips DORMANT→ARMED directly, to let the
  transition chain be tested without the Director existing.
- Mesh is `SM_Cylinder` scaled to ~180cm/35cm-radius as a placeholder
  humanoid capsule, material `MI_Anomaly_Dark` (instance of the existing
  `M_FlatCol`, base color set to linear-space `#1A1916` — the palette's
  darkest tone per `CLAUDE.md`).
- Attached a `FoveaComponent` instance to `BP_FirstPersonCharacter` (the
  player pawn).
- Placed one `BP_Anomaly` instance in `Lvl_FirstPerson` — anomaly #10, the
  hallway-end figure — at (600, 1325, 140), yaw −90°, facing back down the
  hallway. Derived from the existing hallway blockout's actual measured walls
  (X 450–750 inner, Y 300–1400, far wall at Y=1400), not assumed from spec
  numbers alone. Labeled `BP_Anomaly_HallwayEnd_10`, outliner folder
  `Anomalies`. Also noted in passing: `PlayerStart_0` sits at (0,0,302),
  outside the hallway entirely, in leftover First-Person-template geometry —
  the hallway blockout isn't connected to the current spawn point yet.
- **Mid-session incident**: the `UserDefinedEnum`-creation attempt above hung
  the live Unreal Editor behind what was almost certainly an asset-factory
  error dialog — every MCP call timed out, including read-only ones, until a
  human found and dismissed the dialog in the actual editor window. No data
  was lost (the in-progress `FoveaComponent` was still in memory once
  unstuck, just unsaved) but it's a sharp edge worth flagging: don't attempt
  enum-asset creation through `BlueprintTools.create` again without checking
  whether the plugin has grown proper support for it.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** visually confirm the state machine loop (arm via F9, look away past
40°/occlude, look back and hold for >0.12s, confirm the figure appears/
disappears with no visible tween) in PIE before building anything on top of
it. After that: wire the Director/PlayerProfile arming logic (§4), then the
remaining 11 anomalies reusing this same base class.

---

## Session — 2026-08-09 (template strip + hallway blockout)

**Did:**
- Stripped the First Person template character (`BP_FirstPersonCharacter`):
  confirmed there is no gun/projectile logic anywhere in the project (this
  UE 5.8 template ships gunless — no weapon mesh, no fire/projectile nodes,
  no Weapon/Gun/Projectile-named assets), so nothing to remove there. Removed
  jump entirely: deleted the `IA_Jump` event nodes and the `Character|Jump`/
  `StopJumping` calls from `EventGraph` (both the enhanced-input and
  touch-input paths), and removed the `IA_Jump` key mappings (SpaceBar,
  gamepad face-button-bottom) from `IMC_Default`. Left the unused `IA_Jump`
  asset file in place rather than deleting it.
- Set `CharMoveComp.MaxWalkSpeed = 260` (was the template default 600). Added
  a new `IA_Walk` Input Action (Boolean, Left Shift mapped in `IMC_Default`)
  wired in `EventGraph`: Started → `SetMaxWalkSpeed(130)`, Completed/Canceled
  → `SetMaxWalkSpeed(260)`, both through `GetCharacterMovement()`.
- Set `BaseEyeHeight = 165` (was the untouched engine default of 64). Caveat:
  this template's actual FPS camera is attached through the `FirstPersonMesh`
  skeletal component (Manny mannequin), not driven by `BaseEyeHeight` — socket
  attachment data isn't exposed through the available inspection tools, so I
  could not headlessly verify the *rendered* camera height is actually 165uu.
  Worth a visual check in PIE before trusting this number for anomaly framing.
- Blocked out the first hallway grey-box per `CLAUDE.md`'s worked axis-
  conversion example: interior clear space X[450,750] × Y[300,1400] ×
  Z[0,250], walls at 15uu thickness sitting outside that span (verified via
  `get_actor_bounds`). Six `SM_Cube` actors (floor/ceiling/4 walls) using
  `M_PrototypeGrid`, grouped under outliner folder `Blockout/Hallway`. Fully
  enclosed box — no door openings, since none were specified and this is a
  grey-box pass only.
- Along the way, hit a live merge conflict in this file from a concurrent
  session (`git pull` had landed `FEATURE_LIST.md`/`VISUAL_REFERENCE.md` work
  from origin and left this file mid-conflict) — it resolved itself before I
  touched it (someone else finished the merge in parallel), so no action was
  needed on my end beyond confirming `git status` was clean before continuing.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** visually confirm eye height in PIE (see caveat above) before relying
on it for anomaly angle math. First anomaly (hallway-end figure, #10) is next:
grey box + black capsule, full five-state machine, per the handoff spec.

---

## Session — 2026-08-09 (Isolation pivot)

**Did:**
- Team decided Isolation supersedes Peripheral as the project direction —
  Peripheral was the 2-hour brainstorm, Isolation is the matured version from
  the rest of the team. Standing rule going forward: default to Isolation on
  any conflict between the two designs, not a case-by-case call.
- Resolved all six `FEATURE_LIST.md` "needs a decision" items against that
  rule (see the file — vision-clarity technique, collectibles, chase-adjacent
  Day 3 sequence, and back door/garage are all "build it"; house topology is
  deferred as a later layer, not rejected; buyer-sign mechanic is retired).
- Updated `CLAUDE.md`: flagged the vision-technique change (detail-reduction,
  never fully clear even centred, ~60-70% clarity cap — supersedes the
  handoff spec's radial-blur/fully-sharp-centre model), updated the "don't"
  list to show which rules flipped vs. which still hold, corrected the
  doc-precedence note (`FEATURE_LIST.md` resolutions now outrank the handoff
  spec where they conflict).
- No code changed. Anomaly state machine, fovea/occlusion math, and movement
  are confirmed duplicates between the two designs — unaffected by this pivot,
  no rework needed there.

**Pushed:** no — commit locally, human should review before pushing (this one
touches the "don't" list the whole project has been building against, worth
an actual look before it goes to the remote).

**Next:** the FoveaComponent + anomaly state machine build (already queued)
proceeds unchanged. The vision-clarity correction applies to a *different*,
not-yet-started task — the actual peripheral post-process pass (handoff §11)
— build that one to the corrected spec when it comes up, not the handoff
doc's version.

## Session — 2026-08-09 (2)

**Did:**
- First real commit of the FirstPerson template project content (`Config/`,
  `Content/`, `Peripheral.uproject`). The previous session only committed
  scaffolding (`.gitattributes`/`.gitignore`/`CLAUDE.md`) — the project itself
  had never been checked in, so this commit is also the initial import.
- Found an existing `PostProcessVolume` (`PPV_Global`) in `Lvl_FirstPerson`,
  left over from an interrupted prior session. It existed but did nothing —
  `bUnbound` was `false` and every override flag was `false`. Set
  `bUnbound=true`, zeroed Bloom, Lens Flare, Film Grain, Motion Blur, and
  Chromatic Aberration (Scene Fringe + Start Offset) via override, and locked
  exposure by setting Auto Exposure Method to Manual with Bias overridden to 0.
- Fixed Specular on all 5 project materials (`M_PrototypeGrid`, `M_FlatCol`,
  `M_Mannequin`, `M_SimpleGlow`, `M_GradientGlow`) — Unreal's default material
  Specular is 0.5 and was left unconnected (hardcoded) on every one of them.
  Wired a `Constant(0)` into `MP_Specular` on each and recompiled. Roughness/
  Metallic on the level materials (`M_PrototypeGrid`, `M_FlatCol`) were already
  correct (1/0) — no change needed there.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** strip the First Person template (remove gun/projectile logic, remove
jump input), tune movement (walk 260uu/s, shift-held slow walk 130uu/s, confirm
eye height 165uu), block out the first hallway grey-box.

---

## Session — 2026-08-09 (feature-list comparison)

**Did:**
- Read `PERIPHERAL_UNREAL_HANDOFF.md` and `CLAUDE.md` per instruction, then
  compared them against `Isolation — Master Game Feature List.pdf` and
  `Chat GPT ISOLATION FINAL.pdf` (both from `~/Downloads` — turned out to be
  byte-identical, same 69-section document in both files).
- Saved the comparison as `FEATURE_LIST.md` at repo root: a **Needs a
  decision** section (6 items, most-important-first) for anything that
  conflicts with the existing spec, a **New** section for content with no
  conflict, and a **Duplicates** section (named, not repeated) for what
  Isolation already covers the same way Peripheral does.
- Did not resolve anything — no code or spec changes, purely a comparison
  document.

**The six flagged conflicts, briefly:** (1) whether "Isolation" is the same
project as Peripheral or a different one — everything else depends on this;
(2) Isolation's focus mechanic wants vision to stay capped below 100% clarity
even under deliberate attention, where Peripheral's model is centred = always
fully sharp (reinforces, and adds a wrinkle to, the blur-vs-detail-reduction
conflict already on file from the `VISUAL_REFERENCE.md` session); (3) the
existing "no inventory/collectibles" rule vs. Isolation's collectible-memory
and comfort-item-attrition systems, which are a core pillar of that design,
not incidental; (4) "entity never chases" vs. the Day 3 running-footsteps/
back-door climax; (5) Peripheral's fovea/occlusion/collision systems assume a
static level, Isolation wants the house topologically unreliable; (6) the
shipped house has one exterior door, Isolation needs a back door and garage.
Full detail, quotes, and section citations are in the file itself.

**Pushed:** yes (human — Ezekiel — asked for it explicitly, same as the
session above).

**Next:** decision #1 above blocks everything else in this document — worth
resolving before any of the "New" section gets built, since several of those
items (collectibles, comfort-item attrition, day/night structure) only make
sense once it's settled whether this extends Peripheral or starts a new
project.

---

## Session — 2026-08-09 (web prototype side)

**Did:**
- Saved `Peripheral_Art_Direction_Spec.txt` (from `~/Downloads`) as
  `VISUAL_REFERENCE.md` at repo root, reformatted to markdown, content
  otherwise unedited team input.
- Flagged three conflicts at the top of that file instead of resolving them:
  1. **Palette** — five different hex values than what's shipped in
     `src/constants.js`, and the new spec drops the flashlight's warm-color
     exception (`#FFE6B8`) the brief calls for and the game currently
     renders. *(Note: this also conflicts with the palette `CLAUDE.md`
     documents for the Unreal build — see "Conventions" there, which
     confirms `#FFE6B8` as the flashlight's one saturated exception. Same
     conflict, now live on both sides of the port.)*
  2. **Peripheral-vision technique** — shipped `fx/peripheral.js` is a radial
     blur + desaturation pass, matching the brief and `CLAUDE.md`'s "two
     systems must stay separate" architecture. The new spec explicitly
     rejects blur in favor of edge/detail-reduction preserving silhouettes.
  3. *(Minor)* HUD crosshair dot is always-on; new spec wants it hidden until
     something is interactable.
- No code changed to resolve any of these.

**Pushed:** yes (human — Ezekiel — asked for it explicitly).

**Next:** the palette/technique conflict needs a decision from whoever owns
final say on art direction before either `constants.js` or `fx/peripheral.js`
(web) / the UE materials and post-process volume get touched.

---

## Session — 2026-08-09

**Did:**
- Added `unreal/` scaffolding: `.gitattributes` (LFS rules for future binary
  assets), UE5-specific `.gitignore` entries, `CLAUDE.md` (units conversion,
  UE5 post-process defaults that violate the art direction, anomaly state
  machine architecture).
- Confirmed UE 5.8 installed at `X:\UE_5.8`.

**Pushed:** yes — commit `9d3b241`, scaffolding only, no engine-generated files.

**Next:** create the First Person Blueprint project in `unreal/`, enable the
Unreal MCP plugin + All Toolsets, verify MCP with a read-only session before any
write actions.
