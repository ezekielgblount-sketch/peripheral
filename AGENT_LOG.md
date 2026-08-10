# Agent Log

Running record of what Claude did in each work session, in reverse-chronological
order (newest first). Written so either human can read a session's entry, look at
the diff, and decide whether to push — without needing to have watched the stream.

Convention: Claude commits locally with a clear message. **Pushing is a separate,
human decision** — read the entry below, check `git log` / `git diff`, then push
if it looks right.

---

## Session — 2026-08-10 — unattended overnight build, STAGE 2 (block out 7 rooms)

Continuing the numbered stages from the STAGE 1 session below, same unattended
rules (commit after each stage, log blockers instead of grinding on them).

**Did:**
- Reverse-engineered the hallway's construction convention before building
  anything, per instruction. Confirmed via `get_actor_transform`/
  `get_actor_bounds` on all 7 existing hallway actors: mesh is
  `/Game/LevelPrototyping/Meshes/SM_Cube` (a 100×100×100uu unit cube), material
  is `/Game/LevelPrototyping/Materials/M_PrototypeGrid` applied as a
  **component-level `OverrideMaterials[0]`** on each actor's
  `StaticMeshComponent0` (not a mesh-asset default). Confirmed the mesh's
  pivot sits at its **local-space min corner**, not centroid — an actor's
  world-space `location` is therefore the wall/floor/ceiling's min corner, and
  `scale.x/y/z × 100` gives its size in that axis. Derived the exact formula
  from the hallway's 7 actors (all checked out consistent) for a room with
  interior clear-space `X[xMin,xMax] × Y[yMin,yMax]`, floor at Z=0, ceiling
  250uu up, 15uu wall thickness:
  - `Wall_W`: loc `(xMin-15, yMin, 0)`, scale `(0.15, (yMax-yMin)/100, 2.5)`
  - `Wall_E`: loc `(xMax, yMin, 0)`, scale `(0.15, (yMax-yMin)/100, 2.5)`
  - `Wall_S`: loc `(xMin-15, yMin-15, 0)`, scale `((xMax-xMin+30)/100, 0.15, 2.5)`
  - `Wall_N`: loc `(xMin-15, yMax, 0)`, scale `((xMax-xMin+30)/100, 0.15, 2.5)`
  - `Ceiling`: loc `(xMin-15, yMin-15, 250)`, scale `((xMax-xMin+30)/100, (yMax-yMin+30)/100, 0.15)`
  - `Floor`: loc `(xMin-15, yMin-15, -15)`, scale `((xMax-xMin+30)/100, (yMax-yMin+30)/100, 0.15)`

  In words: N/S end-cap walls and the ceiling/floor slabs span the room's
  **full outer footprint** (interior + both 15uu wall thicknesses on that
  axis), so they overlap the E/W walls in the corners; E/W walls span only the
  **plain interior range** on Y, flush between the N/S caps. This matches the
  hallway exactly (verified the formula against all 7 existing hallway actors
  before using it on new rooms — every predicted bound matched the real one).
  Validated by placing one test wall with the formula and reading
  `get_actor_bounds` back before doing the other 41 (came out exactly as
  predicted, X[435,450]×Y[0,300]×Z[0,250] for the Entry west wall), then
  deleted the test actor and rebuilt it for real inside the batch below.
- Built all 7 rooms fully sealed (6 actors each = 42 total: `SM_Cube` +
  `M_PrototypeGrid` override, matching pattern above), each in its own
  `Blockout/<RoomName>` outliner folder, named `Wall_<Room>_W/E/S/N`,
  `Ceiling_<Room>`, `Floor_<Room>`:
  - Entry: X[450,750] Y[0,300]
  - LivingRoom: X[0,450] Y[0,600]
  - Kitchen: X[750,1200] Y[0,600]
  - Bathroom: X[0,450] Y[600,1000]
  - Bedroom: X[750,1200] Y[600,1000]
  - Study: X[0,450] Y[1000,1400]
  - Utility: X[750,1200] Y[1000,1400]

  Per instruction, no openings cut yet and no dedup with the hallway or
  adjacent rooms — each room is an independent sealed box, including a
  duplicate wall anywhere it touches the hallway or another new room (e.g.
  Entry has its own wall along the hallway's south face). That's intentional,
  not a mistake — Stage 3 cuts openings and is easier to reason about against
  simple independent boxes than an already-deduped wall graph.
  Post-build spot-checked `get_actor_bounds` on 3 actors across 3 different
  rooms (Utility floor, Bathroom south wall, Entry ceiling) against the hand
  computed expected values — all matched exactly, no drift.
- Saved all dirty assets (`AssetTools.save_assets([])`) — produced 49 new
  external-actor/external-object package files under `Content/
  __ExternalActors__/` and `Content/__ExternalObjects__/` (OFPA, one file per
  new actor plus a few shared external objects), no modifications to any
  previously-tracked file. Confirmed via `git status` before committing.

**Blocked / not resolved:** nothing this stage — no blockers hit.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** Stage 3 — cut doorway openings connecting all 7 new rooms + the
hallway into one walkable loop.

---

## Session — 2026-08-10 — unattended overnight build, STAGE 3 (cut doorways)

**Did:**
- Chose door height **210uu** (leaving a 40uu header strip below the 250uu
  ceiling). Reasoning: no number is given anywhere in the spec/handoff for
  this, so this is a judgment call — 210uu is a standard real-world door-height
  proportion (matches ~2.1m, a normal residential door) and leaves enough
  header room above it to read visually as a proper opening with a lintel once
  door frames/leaves go in during the Stage 6 door Blueprint work, rather than
  a floor-to-ceiling gap that would look wrong with a frame inserted later.
  Opening width is the one fixed number from the spec: 90uu.
- Mechanically, cut each shared wall into 3 pieces (2 full-height side jambs,
  Z[0,250], + 1 header spanning the opening's width at Z[210,250]) by
  `remove_from_scene` on the original wall actor, then `add_to_scene_from_class`
  ×3 (or ×5 where a single wall needed two separate openings — see below),
  each new piece getting the same mesh/material setup as Stage 2
  (`SM_Cube` + `OverrideMaterials[M_PrototypeGrid]`) and filed into the same
  `Blockout/<Room>` folder the original wall belonged to. Named
  `Wall_<Room>_<Side>_JambX`/`_HeaderX`.
- **Two walls needed two separate openings each, not one**: `Wall_Hallway_W`
  borders both Bathroom (Y600-1000) and Study (Y1000-1400) along its full
  Y300-1400 span, and `Wall_Hallway_E` borders both Bedroom and Utility the
  same way. Each of those became **5 pieces** (jamb / header / middle-pier
  jamb / header / jamb) instead of 3 — the general instruction's "3 pieces"
  assumed one opening per wall, which doesn't hold for the hallway's long
  side walls. Everywhere else, one opening per wall as expected (3 pieces).
- Verified a sample of the new header pieces with `get_actor_bounds` after
  creation (3 spot-checks across different rooms/orientations) — all matched
  the intended opening X/Y span and Z[210,250] exactly.
- **Openings cut, by center coordinate** (all 90uu wide, header Z210-250):
  - Hallway ↔ Bathroom: shared wall at X=450, opening centered **Y=800**
    (Y[755,845]) — cuts `Wall_Hallway_W` (one of its two) and `Wall_Bathroom_E`.
  - Hallway ↔ Bedroom: shared wall at X=750, opening centered **Y=800**
    (Y[755,845]) — cuts `Wall_Hallway_E` (one of two) and `Wall_Bedroom_W`.
  - Hallway ↔ Study: shared wall at X=450, opening centered **Y=1200**
    (Y[1155,1245]) — cuts `Wall_Hallway_W` (the other of two) and `Wall_Study_E`.
  - Hallway ↔ Utility: shared wall at X=750, opening centered **Y=1200**
    (Y[1155,1245]) — cuts `Wall_Hallway_E` (the other of two) and `Wall_Utility_W`.
  - Entry ↔ Hallway: shared wall at Y=300, opening centered **X=600**
    (X[555,645]) — cuts `Wall_Entry_N` and `Wall_Hallway_S`.
  - Entry ↔ Living room: shared wall at X=450, opening centered **Y=150**
    (Y[105,195]) — cuts `Wall_Entry_W` and `Wall_LivingRoom_E`.
  - Entry ↔ Kitchen: shared wall at X=750, opening centered **Y=150**
    (Y[105,195]) — cuts `Wall_Entry_E` and `Wall_Kitchen_W`.
  - Front door (Entry ↔ exterior, exterior not built): Entry's south wall,
    opening centered **X=600** (X[555,645]) — cuts `Wall_Entry_S` only, no
    matching cut on the far side since there's nothing built there yet. No
    door-frame prop, per instruction (Stage 6 handles that separately).
- **Room-connectivity graph after all cuts**: Entry connects to Living room,
  Kitchen, Hallway, and the exterior (front door). Hallway connects to Entry,
  Bathroom, Bedroom, Study, and Utility. Every room is reachable from Entry
  in one hop except the two behind the hallway's far cuts, which are also one
  hop from Hallway — so at most two hops from Entry to any room. Confirmed
  fully connected, no isolated rooms, no dead-end walkable pockets.
- Saved and confirmed via `git status`: 43 new external-actor packages (the
  replacement segments) and 13 deletions (the original sealed walls that got
  cut), no unexpected changes elsewhere.

**Blocked / not resolved:** nothing this stage.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** Stage 4 — placeholder lighting for the 7 new rooms.

---

## Session — 2026-08-10 — unattended overnight build, STAGE 1 (anomaly bug fix)

Human is offline for the rest of this session. Working the numbered stages
they left in order, committing after each, logging blockers instead of
retrying them for hours.

**Did:**
- Added the three debug-print points the human asked for before going
  further: F9 press (unconditional, in `DebugForceArm`), a 0.5s-interval
  state/angle/occluded status print in `EventTick`, and confirmation prints
  inside `SetOff()`/`SetNormal()`. All print to both screen and the Output
  Log (`bPrintToLog` default true) so they're readable after the fact via
  `LogsToolset.GetLogEntries`, not just by watching the screen live.
- Adding the periodic status print initially introduced a real bug of my
  own: the DSL round-trip merged my new "every 0.5s" check into the *same*
  if/elif chain as the `CurrentState==1` (ARMED) check, so the real
  state-machine logic silently stopped running every time the debug print
  fired. Caught this by inspecting the actual compiled node graph
  (`get_node_infos`/`find_nodes`) rather than trusting `read_graph_dsl`'s
  text output, and fixed it by wiring both ends of the debug-print branch
  back into the real check via `connect_pins`. Worth remembering:
  `read_graph_dsl` has multiple known rendering bugs now (this one, plus
  cosmetic ones below) — treat its output as a rough guide, verify anything
  that matters against the actual node graph.
- **Re-investigated two "bugs" I flagged earlier in this same session and
  retracted both** — I misread this DSL's grammar: a plain statement
  following another inside an `(if ...)` body is just a second sequential
  "then" statement, *not* an implicit else. Only an explicit `(elif ...)` or
  `(else ...)` sublist creates a false-branch. Once I re-read them correctly,
  the ARMED branch (`SetOff()` + state-advance together, correctly gated on
  looking away) and the ACTIVE dwell-timer accumulation were both already
  correct as originally built. Also confirmed the F9 InputKey node genuinely
  is wired to `DebugForceArm` and `AutoReceiveInput=Player0` is set correctly
  — `read_graph_dsl` just can't render `K2Node_InputKey` bodies at all
  (shows an empty event), which is what made it look disconnected.
- Started a real PIE session myself (`EditorAppToolset.StartPIE`/`StopPIE`)
  and read the Output Log afterward — confirmed `PlayerFovea` resolves
  correctly in `BeginPlay` (no "accessed None" anywhere) and `GetAngleTo`/
  `IsOccluded` return sane live values. Also found, retroactively, two
  `"BP_Anomaly: forced ARMED (debug)"` log lines from the human's actual
  test session — **F9 did successfully arm it**, twice (almost certainly
  two separate PIE launches, since nothing resets CurrentState back to
  DORMANT mid-session on purpose yet).
- **Actual confirmed bug, now fixed**: the placeholder mesh (`SM_Cylinder`)
  had no collision geometry, matching the "walked straight through" report.
  `StaticMeshTools.generate_convex_collisions` failed silently (returns
  `false`, no error detail) on this mesh — it's Nanite-enabled and has no
  legacy LOD data (`get_vertex_count` reports "-1 LODs"), which the
  generator likely can't handle. Rather than fight a shared prototype mesh
  asset (used elsewhere in the level) for hours, added a dedicated
  `CapsuleComponent` (`BlockingCapsule`, half-height 90, radius 35, offset
  to match the figure's footprint) as the actual collision volume, and tied
  its `CollisionEnabled` to the same `SetOff()`/`SetNormal()` calls that
  toggle mesh visibility — `QueryAndPhysics` when the figure is visible,
  `NoCollision` when it's not. This also fixes a design problem the naive
  "just add collision to the mesh" approach would have had: collision
  independent of visibility would have meant an invisible wall standing in
  the Normal state, which is its own bug.
- **Best explanation for "the figure never appears" during the human's
  actual test**: everything downstream of F9 checks out healthy in
  isolation, so the likely explanation is that the 40° arm-safe threshold
  is a bigger turn than it sounds — nearly a quarter-turn away from dead
  centre, not a small glance aside. If the look-away pass during testing
  didn't cross 40°, `SetOff()` genuinely never fires, which isn't a bug.
  Next test pass: either turn further, or exploit the occlusion path
  instead (duck around anything that blocks line of sight — that also
  satisfies the ARMED→ACTIVE condition regardless of angle).

**Blocked / not resolved:** `SM_Cylinder`'s missing collision itself (the
asset-level Nanite/LOD issue) — worked around via the capsule component
above rather than fixing the mesh, per the "don't retry a blocked thing for
hours" instruction. Someone should eventually check why this shared
prototype mesh has no LODs/collision if it matters beyond this one actor.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** Stage 2 — block out the remaining 7 rooms.

---

## Session — 2026-08-09 (2) (connect spawn to the hallway)

**Did:**
- Human reported being unable to find the hallway in PIE at all. Root cause:
  `PlayerStart_0` was still sitting at (0, 0, 302) in leftover First-Person-
  template geometry, nowhere near the hallway (X 450–750, Y 300–1400) — this
  had already been flagged as a known gap in the previous entry but not yet
  fixed. Moved `PlayerStart_0` to (600, 350, 110), yaw 90°, just inside the
  hallway's south entrance, facing up the corridor toward the anomaly at the
  far end. Saved; only the `PlayerStart_0` external-actor package changed.
- This was a test-convenience fix, not a real level-flow decision — the
  hallway box is still fully sealed (no connection to the old template room)
  and there's no reason yet to think the final game's spawn belongs here.
  Whoever builds out the rest of the house should feel free to relocate
  `PlayerStart_0` again once there's an actual front door/entry to spawn at.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** same as last entry (duplicate `Floor_Hallway` cleanup, confirm the
state-machine loop in PIE, then Director/PlayerProfile wiring) — this session
was purely unblocking the test, no new content.

---

## Session — 2026-08-09 (hallway test lighting + geometry re-check)

**Did:**
- The hallway blockout was pitch black in PIE (sealed box, only the
  template's outdoor sun/sky exist, can't reach through solid walls) — added
  two placeholder `PointLight`s inside it at (600, 700, 200) and
  (600, 1100, 200), 15000 lumens, 900uu attenuation radius each, plain white.
  Bright/flat on purpose, just enough to see the state-machine test by — not
  tuned to Act 1's dim mood, that's a later pass. Filed under
  `Blockout/Hallway` alongside the walls.
- Re-ran `get_actor_bounds` on all 6 (well — 7, see below) hallway actors to
  rule out a geometry bug rather than assume the blackness was lighting-only.
  Confirmed: inner walkable space is exactly **X[450,750] × Y[300,1400] ×
  Z[0,250]**, matching both the spec and the original blockout session's
  numbers. West/east walls at X 435–450 / 750–765, south wall (entrance,
  contradicting an earlier assumption that end was open — it isn't, this
  is a fully sealed box) at Y 285–300, north wall (far end) at Y 1400–1415,
  ceiling at Z 250–265, floor at Z −15–0, all Y/X-spanning correctly. No
  geometry bug — the blackness was lighting only, as suspected.
- Found (not fixed, flagging for whoever touches this next): the `Blockout/
  Hallway` folder has **two** `Floor_Hallway` actors with identical bounds,
  fully overlapping duplicates. Harmless for now (same volume, doesn't affect
  the clear-space measurement above) but worth deleting one next time this
  area gets touched — likely a leftover from the original blockout session.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** the duplicate `Floor_Hallway` cleanup mentioned above. Otherwise
unchanged from last entry — confirm the anomaly state-machine loop in PIE
(now that the hallway is actually visible), then Director/PlayerProfile
wiring.

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
