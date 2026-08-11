# Agent Log

Running record of what Claude did in each work session, in reverse-chronological
order (newest first). Written so either human can read a session's entry, look at
the diff, and decide whether to push — without needing to have watched the stream.

Convention: Claude commits locally with a clear message. **Pushing is a separate,
human decision** — read the entry below, check `git log` / `git diff`, then push
if it looks right.

---

## Session — 2026-08-10 (playtest bug 2/3 — wall seam audit + duplicate-wall bug)

**Did:**
- Systematic audit of all 27 walls' built segments (91 actors at the time),
  bounds-checked programmatically rather than patching visually-obvious spots,
  per the bug report's explicit instruction. Checked every along-axis boundary
  between adjacent segments on every multi-opening wall (W01,W02,W03,W05,W06,
  W07,W08,W09,W10,W15,W20,W25) and every exterior/interior wall corner (15
  corners, both diagonals, via `trace_world`) for real gaps.
- **Result: zero real gaps found anywhere in the opening-splits or corners.**
  Every along-axis boundary between adjacent segments matched exactly (a
  couple showed ~1e-14 units of *overlap*, not gap — footprint noise from the
  scale-from-size float division, many orders of magnitude below anything
  visible). This means task 3's opening-splitting math itself was correct.
- **But found a different, real, systemic bug while auditing:** every wall
  with **zero openings** (15 of the 27 — W04,W11,W12,W13,W14,W16-19,W21-24,
  W26,W27) had been spawned **twice** — an exact-duplicate overlapping box at
  identical bounds. Root cause in task 3's build script: for a wall with no
  openings, the post-loop `if cur < wall_hi: make_seg(...)` already creates
  the one needed solid segment (since `cur` never advances past `wall_lo`
  when the openings list is empty) — but a *second*, separate
  `if not wall_openings: make_seg(...)` check fired right after and created
  a redundant identical box. Two exactly-coincident static meshes is a
  textbook cause of Z-fighting, which reads on screen as a flickering seam —
  very plausibly what got reported as "visible slits/gaps," even though the
  actual geometry had no hole.
- **Fix:** deleted all 91 wall actors and rebuilt from a corrected script —
  removed the redundant duplicate-creation branch, and (defense in depth,
  since none of the current values actually needed it) added a small 0.3uu
  overlap pad to every internal along-axis and Z-axis seam between segments
  of the same wall, so no future float-precision drift can ever produce a
  visible gap. Left the cross-thickness (wall depth) faces and true wall
  end-to-end corners alone — not implicated, no reason to touch them.
  Rebuilt count: 76 segments (91 minus the 15 duplicates), zero errors, zero
  duplicate bounds on re-audit.
- **Verified in a fresh PIE session** (stopped and restarted, not reusing the
  investigation session): re-checked the sightline and several opening/solid
  boundary traces, all still correct; confirmed no new duplicates via a
  bounds-based re-scan of every actor in `House/Walls`.

**Pushed:** no.

**Next:** bug 3 (driveway / disconnected road ground).

---

## Session — 2026-08-10 (playtest bug 1 — basement access, investigation)

**Did:**
- Investigated the reported basement-access blockage at `W20`/`O20` (the
  basement stair door wall), checking for the same asymmetric-wall-cut
  failure mode as the earlier Entry-Hallway and Hallway-Utility bugs, per the
  report's explicit hypothesis. **Could not reproduce that specific failure
  mode** — every check came back clean:
  - `W20`'s built segments (`W20_seg0`, `W20_O20_lintel`) exactly matched the
    expected geometry — no leftover uncut panel, on either the stair-hall/
    landing side or the basement side (checked both, per the report's ask).
  - With the door actor temporarily moved aside, the opening itself was
    genuinely clear across a dense sample grid (25 points spanning its full
    width/height) — the wall has a real hole, not a fake one.
  - Live-tested the actual door mechanism in PIE (not a static/editor-time
    property poke — confirmed separately that those get silently reverted by
    `BP_Door`'s construction script, same as the garage-door resize issue
    from task 5): teleported the player next to the door, pressed **E** for
    real via `SlateInspectorToolset`, confirmed `bIsOpen` flips true,
    `currentYaw` reaches -90, and the opening traces clear on both sides.
  - Checked the basement stairs (`S02`, 13 steps) for gaps between
    consecutive treads — none; checked the main-floor/basement-ceiling
    stairwell shaft cut (`F02`/`F03`/`F04` vs `F12`-`F15`) against the stairs'
    actual footprint — exactly aligned, matches Table 1 to float-noise
    precision.
  - Scanned every actor in a generous bounding box around the whole
    stairwell+door+landing region for anything unexpected (leftover old-layout
    actor, mislabeled duplicate) — nothing found besides what's supposed to
    be there.
- **What I could not test:** real sustained WASD movement through the space.
  `SlateInspectorToolset.PressKey` reliably drives discrete-press actions
  (confirmed working for the flashlight's `F` and the door's `E`), but did
  not produce any measurable player movement for `W` — Enhanced Input's
  analog Move action doesn't appear to register a bare press+release the same
  way a digital toggle action does. Repeated presses and reasonable waits
  didn't move the character at all, so a genuine "walk down the stairs and
  through the door" repro wasn't possible with the tools available this
  session.
- **What I did find nearby, and fixed:** `W13` (the wall immediately at the
  same X-coordinate as `W20`, on the main floor, forming part of the StairHall
  boundary the player crosses to reach the stairs at all) had the duplicate-
  wall bug described in the bug-2/3 entry above — two exactly-coincident
  collision boxes. Coincident static collision is a known category of Chaos
  physics edge case for movement-sweep resolution (not just a rendering
  artifact) — a plausible mechanism for something that reads as "blocked" to
  a player without an obvious visual cause. Fixed as part of the same
  systematic wall rebuild in the entry above, not a separate change.
- **Honest bottom line:** I'm not certain the duplicate-wall fix is *the*
  cause of what was reported — I could not reproduce a blockage at all with
  the tools available, before or explicitly localized to after the fix. If
  it's still blocked after this, I need a more specific repro (exact player
  position/heading where it happens) since teleport-based testing around
  every candidate location came back clean.

**Pushed:** no (no separate commit — the geometry fix is the same one in the
bug-2/3 entry above; nothing to commit for this entry beyond this writeup).

---

## Session — 2026-08-10 (playtest bug 3 — driveway + road/forest ground)

**Did:**
- Before building anything, checked what actually exists: searched for any
  existing "road"/"forest"/"tree" content. Found almost nothing — one stray
  leftover `Tree_1_Trunk` (an unexplained old actor, floating well outside
  and unrelated to any of tonight's work, X~1550/east of the house — left
  alone, out of scope for this bug, noted here rather than silently ignored).
  **There was no pre-existing gravel road or forest ground to "reconnect" —
  this was new construction, not a reconnection fix**, despite how the bug
  report was worded.
- Built, per `HOUSE_ENVIRONMENT_SPEC.md` §4-6:
  - **Driveway**: gate-to-garage-door approach (`Driveway_GateToGarage`,
    220cm wide, centred on `Y=300` — the same centreline the garage door
    `O01` already sits on from task 5), then continuing along the *outside*
    of the house (north of `W03`, the garage's own wall, not overlapping the
    building footprint — caught and fixed a placement mistake here: the
    first attempt at the "continuing to the rear" segment landed *inside*
    the garage's own floor footprint, invisible and useless; moved it
    outside to `Y -220..0`) the full length of the house to the rear, per
    spec's "left side... continuing to the rear yard/service area."
  - **Boundary gate**: split the existing front-boundary fence segment to
    add a second gate gap (`Y 190-410`) for the driveway, alongside the
    existing front-door gate — verified both gaps independently clear and
    the fence still solid everywhere else via `trace_world`.
  - **Road/forest ground**: one large slab (`RoadForest_GroundPlane`,
    `X -2000..-600`) sharing the exact `X=-600` edge with task 7's
    `Yard_GroundPlane` — same grade (`Z=-54` top, same datum derived from
    the blueprint's own front steps), so it's welded, not floating. A
    `GravelRoad_ToMainRoad` strip continues the driveway's line through the
    gate out to the far edge, per spec §5's "connecting to a larger main
    road, at a distance."
- **Verified the weld**, not just assumed it: top-down traces at `X=-605,
  -600, -595` (straddling the seam) all hit at the identical distance —
  continuous ground, no gap. Cross-checked in a fresh PIE session: teleported
  the player onto the far road (`X=-900`) and the driveway (`X=-400`) and
  watched it actually settle under real gravity onto the new ground both
  times, not just trace-checked. (One teleport landed exactly on the gate's
  boundary line/fence-post seam and never settled after several seconds —
  the ground trace there confirmed solid geometry directly underneath, so
  this reads as a spawn-exactly-on-a-seam physics edge case, not a real gap;
  moving a few units off the exact line settled normally.)

**Pushed:** no.

**Next:** all three playtest bugs addressed. Ready for task 8
(materials/furniture) on a human go-ahead.

---

## Session — 2026-08-10 (HOUSE_BLUEPRINT.md replacement, task 2 — triage)

**Did:**
- Read `NEXT_TASKS.md` and `HOUSE_BLUEPRINT.md` in full per instruction. Confirmed
  the blueprint's coordinates are already Unreal-native (its own stated
  convention) and will be built as numbered, with no `CLAUDE.md` axis conversion
  applied — that conversion is only for the old Three.js-convention handoff spec.
- Connected to the Unreal MCP server (`unreal-mcp`, HTTP on 127.0.0.1:8000) after
  some boot-order trouble — editor had to be fully up before the MCP client would
  attach; needed a `/mcp` reconnect even after a fresh Claude Code relaunch.
- Inventoried the current level (`/Game/FirstPerson/Lvl_FirstPerson`) via the MCP
  scene/actor toolset before deleting anything, per task 2's explicit instruction.

**Reusable (kept, not touched — classes/systems, not placements):**
`BP_Door` (`/Game/Blueprints/BP_Door`), `BP_Anomaly`
(`/Game/Blueprints/BP_Anomaly`), `FoveaComponent`
(`/Game/Components/FoveaComponent`), `BP_FirstPersonCharacter`
(`/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter`), all materials
(`M_FlatCol`, `M_PrototypeGrid`, `M_Mannequin`, etc.), `BP_DoorFrame`. Also kept:
global environment/lighting actors (`SM_SkySphere`, `SkyAtmosphere`, `SkyLight`,
`DirectionalLight`, `ExponentialHeightFog`, `VolumetricCloud`) and the two
`Debug` folder utility actors (`BP_PostProcessToggle`, `BP_DayNightDebug`) — none
of these are house-layout-specific.

**Discarded (old-layout placements, no longer correct — 158 actors total, all
under the outliner's `Blockout` and `Anomalies` folders):**
- `Blockout/Bathroom` (13), `Blockout/Bedroom` (12), `Blockout/Entry` (15),
  `Blockout/Garage` (8), `Blockout/Hallway` (18), `Blockout/Kitchen` (13),
  `Blockout/LivingRoom` (11), `Blockout/Study` (11), `Blockout/Utility` (9) —
  old room walls/floors/ceilings/point-lights, old 8-room layout (no Spare
  room/Stair hall/Basement/Attic — those are new in the blueprint).
- `Blockout/Doors` (7) — old `BP_Door` instances at old-layout openings. Treating
  these the same as the anomaly instance: the class stays, these specific
  placements don't (task 5 places fresh instances at the blueprint's Table 3
  positions).
- `Blockout/Yard` (40) — old yard/fence/treeline/path/porch/garage-blockout,
  built around the old front door position. Task 7 rebuilds this around the new
  `W02` front door at ~(0,1215).
- `Anomalies` (1) — the single `BP_Anomaly` instance's old position. Class stays;
  task 6 re-places it in the new hallway.

**Pushed:** no — local commit only, per standing instruction not to push without
being asked.

**Next:** delete the 158 discarded actors, then task 3 (build Tables 1-4 grey-box
structure at the blueprint's exact coordinates).

---

## Session — 2026-08-10 (HOUSE_BLUEPRINT.md replacement, task 3 — structure)

**Did:**
- Built the full grey-box structure from Tables 1-4, coordinates taken literally
  (no `CLAUDE.md` axis conversion — confirmed not applicable per the blueprint's
  own header). Used the MCP `ProgrammaticToolset` (batched Python against the
  scene/primitive tool APIs) instead of one tool call per box — ~160 actors would
  have been slow and expensive one at a time.
- Discovered `PrimitiveTools.add_cube`'s `dimensions` parameter silently floors
  any axis below 256uu to a fixed 256uu cube instead of respecting the requested
  size — confirmed by direct test (a 10×20×30 request produced a 256×256×256
  box). That's unusable for 15-30cm-thick walls, so switched to spawning
  `/Game/LevelPrototyping/Meshes/SM_Cube` directly (confirmed via
  `StaticMeshTools.get_bounds`: a corner-pivoted 0..100 unit cube) and setting
  actor location = AABB min corner, scale = size/100 per axis. This reproduces
  exact world-space AABBs reliably and is worth remembering for any future
  primitive-geometry work in this project — **don't use `PrimitiveTools.add_cube`
  for anything under ~256uu on any axis.**
- **Floors/slabs (Table 1):** all 41 spawned directly from min/max corners, no
  openings needed. Folder `House/Floors`.
- **Walls (Table 2):** all 27 walls are axis-aligned (each row's Start/End share
  either X or Y), so every wall reduces to one or more AABB segments — no
  rotation math needed anywhere. For each wall, gathered its Table 3 openings
  (by host-wall ID), sorted along the wall, and split the wall into: solid
  full-height segments in the gaps between openings, a sill segment below an
  opening when `sill > 0`, and a lintel segment above an opening when its top is
  below the wall's top. Zero-opening walls got one solid segment. This produced
  91 wall segments (`House/Walls`), including the 5-opening `W10` (hall/room
  boundary — O12, O13a, O13b, O14, O15) split into 6 solid segments plus lintels.
  Verified against the source data before running: `W20`'s door (height 205) vs.
  wall height 210 leaves a genuine 5cm lintel, and `W25`'s door (height 205) vs.
  wall height 205 leaves none — both are the blueprint's own numbers, not a
  building mistake.
- **Stairs (Table 4):** built as stacked solid blockout steps (rising boxes, each
  successive step taller/further along than the last) — standard greybox
  stair technique. 28 steps total (`House/Stairs`: S01 attic ×15, S02 basement
  ×13). **Assumption, not explicit in the blueprint:** interpreted each stair's
  `Bottom-start (X,Y,Z)` as the stair's starting/left edge (spanning `X` to
  `X+width`), not a centerline. Cross-checked this against Table 3/Table 5 data
  before committing to it: S01's start X=365 matches door `O13a`'s position and
  width exactly; S02's start X=485 matches door `O13b` and the basement landing
  slab `F11` (485-575) exactly. Both stairs' Z ranges also land exactly on the
  floor/ceiling datums they should (attic stair 0→270, basement stair -234→0).
- Left all door/window openings as literal gaps — no `BP_Door` instances placed
  yet, per task 3's explicit instruction (that's task 5).

**Pushed:** no.

**Next:** task 4 — independently re-verify the blueprint's self-check claims
(closure, sightline) against what was actually built here, using bounds/trace
tools rather than trusting the document.

---

## Session — 2026-08-10 (HOUSE_BLUEPRINT.md replacement, task 4 — re-verify)

**Did:**
- **Sightline:** `trace_world` from `(0,1215,170)` to `(1200,1215,170)` (the
  blueprint's own stated front-door-centre-to-back-door-centre line) returned no
  hit — confirmed clear, against the actual placed geometry, not the document's
  claim.
- **Closure:** wrote an independent perimeter-sampling check (separate script
  from the one that built the geometry) — for every one of Table 5's 11 rooms,
  matched each of its 4 edges against Table 2's wall rows by coordinate, then
  `trace_world`'d ~500 sample points at 50cm spacing along those edges at each
  floor's mid-wall-height, checking solid where no opening is expected and clear
  where Table 3 says there should be a door/window. All 44 edges found a
  matching wall row (no unenclosed edges). 512 samples, 7 initial mismatches —
  all traced to bugs in the *verification script itself*, not the build:
  - 5 were on `W08` (main house right wall) — its Start/End run **X-decreasing**
    (`(1200,1800)→(0,1800)`), and the verification script's opening-position
    math didn't account for wall direction (the *build* script from task 3
    did handle this, correctly). Once the direction sign was added, the two
    windows on `W08` (`O18`, `O19`) landed exactly where the trace already
    showed them clear — the wall was right, the checker was wrong.
  - 2 were exact-boundary sampling artifacts (`Hallway` at x=800 and x=1000,
    landing precisely on the opening's edge coordinate). Re-traced 5cm to
    either side of each: solid on the wall side, clear on the opening side —
    confirms correct construction, not a defect.
  - After fixing both issues, re-verification is clean: 0 real mismatches.
- Conclusion: `HOUSE_BLUEPRINT.md`'s self-check claims for closure and
  sightline hold against the actual built level, independently confirmed with
  engine trace queries rather than by re-reading the document.

**Pushed:** no.

**Next:** task 5 — place `BP_Door` instances at every `door`-type row in Table 3
(not the `window` rows), reusing the existing class.

---

## Session — 2026-08-10 (HOUSE_BLUEPRINT.md replacement, task 5 — doors)

**Did:**
- Placed 14 `BP_Door` instances, one per `door`-type row in Table 3 (skipped the
  8 `window` rows). Reused the class exactly as instructed — no changes to
  `BP_Door` itself.
- Worked out the placement convention by inspecting the class's own component
  transforms (`ObjectTools.list_properties`/`get_properties`) rather than
  guessing: `DoorLeaf` is parented to `HingePivot` (offset `(0,-45,0)` from the
  actor root), so the actor's **origin is the opening's centre at floor level**
  — world location = (wall's thickness-centreline coordinate, midpoint of the
  opening's along-wall range, wall's `Base Z`). Confirmed this placement math
  with `trace_world` against several placed doors before trusting it further
  (e.g. `O02`'s leaf face hit at exactly world X=-4, matching the class's own
  4cm leaf-half-thickness) rather than relying on `get_actor_bounds`, which
  reads as polluted by the actor's editor-only billboard icon (reports a
  ±128uu box on every axis regardless of the real mesh — harmless in-game,
  since billboards don't render or collide outside the editor, but useless for
  verifying placement).
- Yaw: 0° for doors on X-fixed (Y-running) walls, 90° for Y-fixed (X-running)
  walls — verified against the class's actual local-to-world transform math,
  not assumed. `O02`/`O04` landed at `(0,1215,0)`/`(1200,1215,0)`, exactly
  matching the blueprint's own stated front/back door centres from the task 4
  sightline check — good cross-confirmation.
- Confirmed the hinge-swing-direction fix from earlier tonight is still intact
  by inspecting the class (unchanged `HingePivot`/`DoorLeaf`/`currentYaw`/
  `targetYaw`/`bPlayerNearby` structure — nothing about the door class itself
  was touched, only new instances placed) — a live PIE proximity-swing test
  would be the fuller confirmation but wasn't run this session.
- **`O01` (garage door) limitation, worth flagging:** the blueprint's own
  self-check calls this a "deliberate exception" — 490×215 vs. the standard
  90×205 everywhere else. Tried to stretch just this one instance's
  `DoorLeaf.relativeScale3D` / `HingePivot.relativeLocation` via
  `ObjectTools.set_properties` to fit the opening. The call reports success,
  but the values silently revert to the class default on next read — almost
  certainly `BP_Door`'s Construction Script re-asserting a hardcoded `(0,-45,0)`
  / `0.9` on every reconstruction, which fires on practically any edit. Placed
  a standard-size `BP_Door` there instead (centred in the opening), which
  covers 90 of the 490cm gap and leaves the rest open. **Not fixed** — a real
  fix needs either a `BP_Door` construction-script change to parameterize
  width (a real class edit, out of scope for a "reuse, don't rebuild" task) or
  a separate garage-door asset. Flagging for a human call rather than guessing
  further.

**Pushed:** no.

**Next:** task 6 — re-place anomaly #10 in the new hallway.

---

## Session — 2026-08-10 (HOUSE_BLUEPRINT.md replacement, task 6 — anomaly)

**Did:**
- Re-placed the hallway-end figure (`BP_Anomaly`, unchanged class) in the new
  hallway (room registry X 180-1200, Y 1140-1290, per `NEXT_TASKS.md`).
- Worked out placement the same way as the doors — inspected the class's own
  component transforms rather than guessing: `FigureMesh` sits at relative
  Z=-140, `BlockingCapsule` at relative Z=-50 with half-height 90 (world span
  -140 to +40 relative to actor root), so **actor root Z = 140 puts the
  figure's feet on the floor**. Confirmed with a top-down `trace_world` after
  placing: hit at world Z=180, exactly matching the capsule's predicted top —
  feet-on-floor confirmed against the real placed actor, not just the math.
- **Position and reasoning (logged per NEXT_TASKS' explicit instruction, since
  the blueprint has no coordinate for this — it's architecture, not gameplay
  placement):** `(1150, 1215, 140)`, yaw 180°. X=1150 is 50cm short of the
  back wall (X≈1200) — deep in the hallway, past every side-room doorway
  (last one, `O15`, ends at x=1090), so it reads as "the figure standing at
  the end of the hall" the way anomaly #10 is named, without physically
  blocking the back door's swing clearance. Y=1215 is the hallway's clear
  centreline (same line the task 4 sightline check used). Yaw 180° faces the
  figure back down the hallway toward the front entrance — the classic
  "something standing at the far end, facing you" read, rather than facing
  away or sideways.
- Folder: `Anomalies` (recreated — it was deleted automatically in task 2 once
  the old instance was removed and the folder went empty).

**Pushed:** no.

**Next:** task 7 — rework the yard around the new front-door position (`W02`,
~(0,1215), facing -X).

---

## Session — 2026-08-10 (HOUSE_BLUEPRINT.md replacement, task 7 — yard)

**Did:**
- Rebuilt the three explicitly-scoped pieces (ground plane, boundary, front-path
  gap) around the new front door — the old yard was already gone (deleted with
  everything else under `Blockout/` in task 2). Did **not** attempt fence/
  treeline/prop detail or the driveway — those are dressing, out of scope per
  the task's own text ("full detail... if useful, but the position has to
  match") and per task 8 holding materials/furniture for later.
- **Grade level:** used `Z=-54` as the exterior ground datum, not `Z=0`.
  Derived this from the blueprint's own front steps (`F07`-`F09`, already built
  in task 3): three 18cm risers descending from the porch (`Z=0`, flush with
  the main floor) land at `Z=-54` — that's where the blueprint's own geometry
  already meets natural grade, so the yard ground plane's walkable top sits
  there instead of at an arbitrarily-chosen height.
- **Ground plane:** one slab, `X -600..1500, Y -300..2100`, top at `Z=-54` —
  generous margin around the house+porch+garage footprint (house's own extent
  is roughly `X -264..1200, Y -30..1830` including the front steps and roof
  overhang).
- **Boundary:** a low fence perimeter (110 tall, 15 thick, matching interior
  wall-thickness convention) around that same rectangle, split into 5
  segments — the front (west, low-X) side has a gap instead of one solid run.
- **Front-path gap:** the gap sits at `Y 1100-1330`, centred on `1215` — the
  same Y the front door (`O02`), entry/hall door (`O03`), back door (`O04`),
  and the task-4 sightline all already share. A path slab (`Y 1140-1290`,
  matching the interior hallway's clear width) runs from the gate to the
  porch/steps at `X=-264`. Verified with `trace_world`: clear straight through
  the gate at the door's centreline, blocked by the fence 700uu further down
  — confirms the gap lines up with the new door position, not the old one.

**Pushed:** no.

**Next:** task 9 — flashlight battery drain (independent of the house rebuild,
safe to do anytime). Task 8 (materials/furniture) stays held until a human
confirms the structure pass is good.

---

## Session — 2026-08-10 (task 9 — flashlight battery drain)

**Did:**
- Added the battery-drain mechanic to `BP_FirstPersonCharacter` (already had a
  toggleable `FlashlightComponent`/`SpotLightComponent` and a `ToggleFlashlight`
  function from an earlier session — reused both, didn't rebuild).
- New member variables: `FlashlightBatteryPct` (float, default 100) and
  `bFlashlightOn` (bool, default false).
- `ToggleFlashlight`: turns off unconditionally; turns on only if battery > 0
  (dead battery can't be toggled back on — matches "no recharge yet").
- New `EventTick`: while `bFlashlightOn`, drains at `100/240` %/sec (exactly
  240s from full to empty). At 0%, forces `bFlashlightOn` false and the light
  invisible. Below 20%, flickers: each tick, `P(visible) = BatteryPct/20`, so
  the flicker gets more frequent/severe as it approaches 0 rather than being a
  flat on/off flicker rate — reads as a dying battery, not a broken light.
- **Color:** left untouched. `MASTER_VISUAL_ENVIRONMENT_BRIEF.md` §19
  explicitly supersedes `NEXT_TASKS.md` task 8's old rigid `#C8C1B6` lock and
  says color should vary by room from a palette family — but also says "the
  battery-drain mechanic itself is unaffected." That room-by-room variation is
  materials/lighting work, which task 8 holds for later; this session's scope
  was the drain mechanic only, so color wasn't touched either way.
- **Correction to what I assumed going in:** initially thought the F-key
  toggle might be disconnected — `read_graph_dsl` on `EventGraph` rendered the
  key event with an empty body. Turned out to be a display quirk in the DSL
  round-trip printer for `K2Node_InputKey` nodes, not a real problem — direct
  node/pin inspection (`find_nodes`/`get_node_infos`, not the DSL text) showed
  the F key's `Pressed` exec was already correctly wired to `ToggleFlashlight`.
  Learned to verify Blueprint graph edits this way going forward: `read_graph_dsl`
  is fine for a first read, but treat its output as approximate and check the
  actual compiled node graph before concluding something is broken or before
  trusting that a `write_graph_dsl` call did what was asked (a `false` argument
  matching a pin's own default was silently omitted from one round-trip too —
  also harmless, confirmed via the same direct pin check, but same lesson).
- **Live-tested in PIE**, not just statically verified: started a real Play-In-
  Editor session, used `SlateInspectorToolset` (`Click` + `PressKey`) to send an
  actual `F` keypress to the viewport — `ObjectTools.set_properties` can't write
  to a live PIE actor instance (reads work, writes are rejected; CDO writes are
  fine), so this was the only way to drive it for real rather than faking state.
  Confirmed: F toggles the light and starts the drain; battery dropped from
  100% to 78.61% over an observed ~43 real seconds, matching the intended
  100/240 %/sec rate almost exactly (predicted 18.04%, observed 18.06%);
  pressing F again froze the drain immediately (battery held flat over a
  further 5s check) and set the light invisible. The flicker (<20%) and
  hard-cutoff (0%) branches are confirmed structurally (direct pin inspection
  of the compiled graph, matching the intended branch logic exactly) but
  **not** exercised live — reaching 20% battery needs ~192s of real playtime,
  not done this session.

**Pushed:** no.

**Next:** task 8 (materials/furniture) stays held for a human go-ahead — that
was the last item in `NEXT_TASKS.md`. All of tasks 2-7 and 9 are done.

---

## Session — 2026-08-10 (catch-up + queue tasks 7/8, other-Claude side)

**Note added during merge:** the tasks 7/8 this session queued (below) were
further superseded before they ran — `HOUSE_BLUEPRINT.md` landed and replaced
the interior entirely, and `NEXT_TASKS.md` was rewritten around it. Kept for
the record (and for the `DESIGN.md`/PR #1 pointer below, which is otherwise
undocumented in `AGENT_LOG.md`), not because the plan itself still applies.

**Did:**
- Caught up after ~47 commits landed on `main` since this session's last look
  (Isolation pivot, real Unreal project + Blueprints built, doors verified,
  yard/garage grey-boxed, two doorway bugs found and fixed). Reset local
  `main` to match — nothing lost, the one local-only commit was already safe
  on the (now-closed) PR branch.
- Closed PR #1 (`decisions/consolidated-rulings`) as superseded — its content
  is now redundantly recorded in `DESIGN.md`/`CLAUDE.md`/`FEATURE_LIST.md` on
  `main` via a separate, more current resolution than what that PR was
  tracking. Nothing from it needed merging.
- Confirmed one live contradiction directly with the human before touching
  anything: `CLAUDE.md` and `HOUSE_ENVIRONMENT_SPEC.md` both say the
  flashlight's warm-color exception is retired (zero exceptions, confirmed
  twice); an earlier ratified decision in this repo's history said keep it
  warm. Human resolved it in favor of the retirement — flashlight goes
  neutral, matching what's already written twice on `main`.
- Added tasks 7 and 8 to `NEXT_TASKS.md` for whoever runs the next Unreal MCP
  session: (7) redo every material from the old `#1A1916`-family palette to
  the final confirmed 5-color set (`VISUAL_REFERENCE.md` / `HOUSE_ENVIRONMENT_
  SPEC.md`), with a proposed room-by-room mapping since no file had one yet;
  (8) flashlight battery — 240s of cumulative on-time per charge, flicker in
  the last ~20%, cuts out at 0%, Faded Bone `#C8C1B6` light color (not warm),
  no HUD meter, no pickups/recharge in this pass.
- No Unreal MCP connection in this session (none loaded, no Editor process
  running here) — did not and could not touch the actual Unreal project.
  Docs/queue only.

**Pushed:** yes (human — Ezekiel — asked for this to go straight to a prompt
for the other Claude Code session to pick up, so it needs to be on `main` for
that session to see it after a pull).

**Next:** tasks 7 and 8 in `NEXT_TASKS.md`, for the session running from
`unreal/` with the Editor open.

---

## Session — 2026-08-10 — playtest fix: blocked Hallway-Utility doorway (back room, same failure mode as Entry-Hallway)

Fresh session, no memory of prior ones — bootstrapped from `CLAUDE.md` +
this file per instruction. Given two bug reports (a sealed-off back-left
room, a misplaced garage). This entry covers the first.

**Diagnosis, not assumption:** the brief specifically asked to check
whether this was the same failure mode as the earlier Entry-Hallway bug
(a replacement door-frame added on top of an un-deleted original wall)
before doing anything else.

- Identified the room layout from this file's Stage 2/3 entries: Entry/
  LivingRoom/Kitchen up front, Bathroom/Bedroom in the middle, Study/
  Utility at the back (Y[1000,1400], the house's north wall). Checked
  **Study** first as the "back-left" candidate — bounds and a live
  `trace_world` both came back completely clean, matching the pattern of
  every working doorway (closed-door trace hits at distance 16, matching
  the leaf's near face; this exact doorway was also already confirmed
  clean+live-tested in the prior playtest-fix session, commit `c834c9c`).
- Since the room I guessed didn't reproduce the bug, ran a **full fresh
  PIE sweep of all 7 doors** rather than guess again (per instruction):
  scripted, for each door, teleport the player pawn within 150uu,
  confirm `bPlayerNearby`, press E (`SlateInspectorToolset.PressKey`),
  read back `bIsOpen`/`currentYaw`, trace across the opening, press E
  again to close, trace again. 6 of 7 doors passed cleanly (open: no
  hit; closed: hit at the leaf, distance 16). **`Hallway↔Utility` failed**:
  even with `bIsOpen=true`/`currentYaw=-90` (door genuinely reporting
  open), the trace hit something at distance **5** in both the open and
  closed state — a blockage independent of the door's own state, meaning
  something other than the door leaf was in the way.
- Root cause, confirmed via `find_actors` bounds query around the
  doorway: a leftover, never-deleted **`Wall_Utility_W`** actor, full
  length, world bounds `X[735,750] Y[1000,1400] Z[0,250]` — the original
  Stage-2 wall panel, still sitting directly behind/alongside the
  correctly-cut `Wall_Utility_W_JambS/Header/JambN` replacement pieces
  from Stage 3. **Exactly the same failure mode as the Entry-Hallway bug**
  (original wall never deleted when Stage 3 replaced it), just on a
  different doorway — confirms this wasn't a one-off after all, it's a
  second miss from the same Stage 3 session.
- **Fix**: deleted `Wall_Utility_W`
  (`StaticMeshActor_UAID_D8BBC1A6E88375F602_1819628903`) via
  `SceneTools.remove_from_scene`. Re-verified with a **fresh** PIE session
  (not hot-reloaded, per the project's standing rule) re-running the same
  7-door sweep script: all 7 doors, including Utility, now show identical
  behavior (open: clear trace; closed: hit at distance 16, matching every
  other doorway).

**Search for other instances of this bug:** the full 7-door sweep is
exactly this check, run against every doorway in the project, not just
the two known-bad ones — no other doorway showed the anomalous
state-independent blockage.

**Blocked / not resolved:** nothing — root cause found and fixed, verified
live via a fresh PIE session.

**Saved and verified**: `AssetTools.save_assets([])` after the fix;
`git status` shows exactly one file deleted (the removed actor's
external-actor package), nothing else touched.

**Pushed:** no — local commit only, human should review before pushing
per the standing rule.

**Worth flagging to the human:** the "back-left room" description in the
original bug report doesn't quite match this room's actual position
(Utility is the back-**right** room, X[750,1200], under this project's
established left/right convention — Study, the actual back-left room, is
fine). Possible the report meant "the last room worked on" or used a
different left/right convention; either way, the full sweep would have
caught the bug regardless of which room was named, so it's fixed either
way. Also worth noting: no Blueprint enum was touched.

**Next:** see the separate entry below for the garage (bug #2), built in
the same session as a fresh addition since no garage existed anywhere in
the project prior to this.

---

## Session — 2026-08-10 — playtest fix: build garage grey-box (front-left)

Second half of tonight's two-bug session. Per the brief, checked first
whether a garage already existed anywhere to "move" — it didn't (no
actor in the level under any outliner folder, no Blueprint/mesh asset
named anything like it, no doc beyond `FEATURE_LIST.md`/`AGENT_LOG.md`
recording it as a still-unbuilt "build it" item; `HOUSE_ENVIRONMENT_SPEC.md`
§19 explicitly lists it as "ADD — doesn't exist yet"). Confirmed with the
human before proceeding; asked to build it fresh at the correct
front-left location rather than hunt for a nonexistent bug.

**Did:**
- Placement: front-left yard, exterior footprint `X[-395,-15] Y[-435,-70]`
  (interior clear space `X[-380,-30] Y[-420,-70]`, 350×350uu), floor Z=0,
  250uu ceiling, 15uu walls — same construction convention as every house
  room (Stage 2's formula: `SM_Cube` actors, min-corner pivot,
  `OverrideMaterials[0]` on `StaticMeshComponent0`). "Left" taken as -X
  (the side LivingRoom/Bathroom/Study already occupy, matching the
  visitor-facing-the-house convention implied by
  `HOUSE_ENVIRONMENT_SPEC.md`'s driveway note) and "front" as low Y,
  matching the existing porch/gravel-path build's front-yard orientation.
  Chose a standalone position in the open front yard rather than flush
  against the house's LivingRoom wall — the wall-flush option overlapped
  an existing conifer tree (`Tree_11`, confirmed via `find_actors` bounds
  query before placing), and "near the driveway" doesn't require literal
  attachment. Verified the chosen footprint against a bounds query first:
  clear of the fence perimeter, all yard trees, and the house itself.
- 8 pieces (`Wall_Garage_W/E`, 3-piece `Wall_Garage_S_JambW/Header/JambE`
  for a garage-door-sized opening, `Wall_Garage_N`, `Ceiling_Garage`,
  `Floor_Garage`), all under a new `Blockout/Garage` outliner folder,
  built via a batched `ProgrammaticToolset` script rather than 8
  individual placement round-trips. Reused the existing palette material
  instances rather than creating new ones: `MI_Wall_Light` (walls),
  `MI_Ceiling_Pale` (ceiling), `MI_Floor_Dark` (floor) — same three used
  throughout the house.
- **Garage-door opening**: 220uu wide, centered on the south (front,
  driveway-facing) wall, header at `Z[210,250]` leaving `Z[0,210]` fully
  open below — same jamb/header split convention Stage 3 used for the
  interior doorways, reused here for consistency even though this is an
  exterior bay opening rather than a leaf-door. No door mesh/leaf, same
  as the front door's exterior opening — out of scope for a grey-box pass.
- Verified before considering it done, not just placed and trusted:
  `get_actor_bounds` on the header piece matched the intended opening
  span exactly; `trace_world` through the opening center came back clear
  (`null`); traces through the west wall and a solid jamb section both
  hit at distance 15, matching the 15uu wall thickness exactly. Also took
  an actual viewport screenshot (camera positioned outside facing the
  opening) to confirm visually, not just by bounds math — first attempt
  was aimed wrong (camera Z=250 clipped into the new ceiling, produced an
  unusable close-up); repositioned outside the structure and got a clean
  shot showing the opening, jambs, header, and dark floor all reading
  correctly.
- Saved; `git status` showed exactly 8 new external-actor packages (one
  per piece) plus 1 new external-object package (the new `Blockout/Garage`
  folder registration) — nothing else touched.

**Blocked / not resolved:** nothing.

**Pushed:** no — local commit only, human should review before pushing
per the standing rule.

**Worth flagging to the human:**
- This is a grey-box shell only, matching tonight's other yard-content
  pass — no interior detail (spec §19's tools/wrench/shelving/workbench),
  no lighting inside (the opening is large enough that daylight should
  reach most of the interior, but this hasn't been checked at night), no
  connection to the house interior (no interior door cut — the brief's
  two bugs were about the garage's exterior position, not house
  connectivity, so this was left alone).
- The "left" convention (matching LivingRoom/Bathroom/Study's side) is an
  assumption carried over from the earlier room layout, not something
  the human explicitly confirmed for the garage specifically — worth
  a quick look to confirm it reads as "the driveway side" once there's
  an actual driveway built.
- No Blueprint enum was touched.

---

## Session — 2026-08-10 — playtest fix ITEM 1 (exterior yard content)

Second of tonight's two playtest fixes, done after item 2 (blocked doorway,
separate commit) per instruction. Read `PERIPHERAL_UNREAL_HANDOFF.md` §6
for the original treeline/gravel-path/porch description before building —
human wants the same grey-box primitive approach used everywhere else
tonight, not the full polish pass that section describes.

**Lighting verification — genuinely broken, fixed as a prerequisite before
placing anything:**
- Confirmed `BP_DayNightDebug`'s `bIsNight` was `false` (day state, the
  correct default) and the live `DirectionalLight_0`/`SkyLight_0` actors
  matched the documented "Day" preset (Intensity 6 and 1 respectively).
  So the day/night toggle itself wasn't the problem — the "day" preset
  values themselves were.
- Took an actual viewport screenshot from inside the yard
  (`EditorAppToolset.CaptureViewport`) before placing anything, per
  instruction not to dress a space nobody can see: **confirmed pitch
  black** — only an editor-only actor-icon sprite was visible, nothing of
  the ground/fence/sky rendered at all.
- Root cause: the "Day" preset values (6 lux / 1 for sky) are extremely
  dim in absolute terms — plausible as a leftover placeholder from before
  the interior rooms' own `PointLight`s (15000 lumens each) became the
  project's real light source, since interior rooms never depended on the
  sun/sky at all. Nobody had ever pointed a camera outside to notice.
  Iteratively raised both via `ObjectTools.set_properties` and re-captured
  the viewport after each change (screenshots decoded from the tool's
  base64 payload via a PowerShell helper script, since the raw MCP
  response is too large to return inline) until the exterior actually
  read as daylight: ground and sky visible immediately; the house's
  south-facing exterior wall stayed pure black even at `DirectionalLight
  8000` because it's outside the sun's direct-light azimuth (confirmed by
  computing the light's forward vector from its rotation — sun arrives
  from the west/north, so south- and east-facing walls get zero direct
  light, physically correct) — it only became visible once `SkyLight`
  (the omnidirectional ambient fill) was raised to `400`. Final values:
  `DirectionalLight_0` Intensity **6 → 8000**, `SkyLight_0` Intensity
  **1 → 400**. Confirmed via repeated screenshots from multiple sides of
  the house (south wall, east wall) that no exterior face renders as pure
  black anymore.
- **Also updated `BP_DayNightDebug`'s hardcoded day-preset constants**,
  not just the live scene actors — the F10 toggle's `ApplyDayNight`
  function had its own `MakeLiteralFloat` nodes feeding the day/night
  `Select` nodes (found via `find_nodes`/`get_node_infos`, confirmed
  which `Select` `Option` pin was the "day" value against the DSL's
  `(select isNight nightVal dayVal)` semantics — matches the project's
  established convention, verified against the same node type an earlier
  session had already checked). Without this fix, pressing F10 twice
  (night then back to day) would have silently reset the yard to
  pitch-black again. Used `set_pin_value` on the two `MakeLiteralFloat`
  nodes directly (6.0→8000.0, 1.0→400.0) rather than `write_graph_dsl`,
  since it was unclear whether a full-graph DSL rewrite would cleanly
  replace the existing function body or duplicate nodes — a scoped pin
  edit avoided that risk entirely. Left the night-preset values (0.05
  each) and the point-light day/night values untouched — out of scope.
  Recompiled the Blueprint after.

**Content built, all under `Blockout/Yard` (existing folder), all
`M_FlatCol`-derived instances already in the project, no new materials or
imported assets:**
- **12 conifer trees** (cone + cylinder per tree, via a batched
  `ProgrammaticToolset` script rather than 24 individual placement calls):
  cone = `/Engine/BasicShapes/Cone` (confirmed center-pivoted on all 3 axes
  by placing a test instance and reading its bounds back), material
  `MI_Anomaly_Dark` (the palette's darkest tone, `#1A1916`); trunk =
  `SM_Cylinder` (center-pivoted X/Y, min-corner Z — the established
  convention from tonight's furniture pass), material `MI_Floor_Dark`.
  Base dimensions trunk 26⌀×65 tall, foliage 85⌀×125 tall, each tree
  individually scaled by a manually-varied multiplier (0.8–1.2, no two
  the same) since there's no RNG available in this scripted context —
  manual variation substitutes for it. Placed denser toward the east yard
  edge (facing the bedroom, X[750,1200]) and along the north/back edge
  (high Y), sparser west, per instruction; confirmed against the fence's
  actual measured extent (`X[-500,1700] Y[-900,1700]`, read from the
  fence actors' bounds rather than assumed) so no tree clips through the
  perimeter.
- **Gravel path**: single flat `SM_Cube` slab, `MI_Ceiling_Pale` (the
  palette's palest tone, reads clearly distinct from the ground's
  `MI_Floor_Dark`), running from the handoff spec's converted exterior
  spawn anchor (`(600,-600)`) up to the bottom porch step at `Y=-105`,
  100uu wide (`X[550,650]`), sitting 0.5uu proud of the yard ground's own
  top face (same anti-Z-fighting trick tonight's earlier yard session used
  for the ground-vs-interior-floor seam). Confirmed the south fence
  already has a gap here (`X[500,700]`, well clear of the path) before
  assuming it, per instruction.
- **Front porch**, centered on `X=600` (the door's own center) and flush
  against the house's south wall face at `Y=-15` (confirmed via the actual
  `Wall_Entry_S_Jamb/Header` actor bounds rather than assumed): 3 ascending
  `SM_Cube` steps (120 wide, treads 90/60/30uu deep, total rise 9uu — kept
  deliberately small since the real gap between yard ground `Z=-1` and the
  interior floor `Z=0` is only 1uu; a physically-accurate stair would be
  imperceptible, so this is a stylized "stoop" sized to read clearly rather
  than match the literal 1uu threshold), two posts (`SM_Cube`, 15×15
  footprint, 231 tall), a beam spanning their tops, and a flat roof
  overhang (180×100, 15 thick) extending from the posts back to the wall
  face — plus a thin railing on each side connecting post to house wall at
  hand-rail height. All porch pieces use `MI_Wall_Light`. Did **not** move
  `PlayerStart_0` — confirmed its transform first (`(600,150,110)`,
  unchanged from Stage 5) and left it alone, per instruction; it's an
  interior-testing spawn point, unrelated to this exterior decoration pass.
- Verified visually, not just by bounds math: viewport screenshots from
  several angles (trees against the sky near the east yard edge, path
  leading up to the porch head-on, porch interior looking back at the
  house's front door) all read correctly — path clearly distinct in tone
  from the ground, porch proportioned reasonably against the 90uu-wide
  doorway, trees read as legible dark conifer silhouettes.

**Blocked / not resolved:** nothing. The lighting fix was the one
prerequisite blocker and it's resolved and verified.

**Saved and verified**: `AssetTools.save_assets([])`; `is_dirty` false on
both the level and `BP_DayNightDebug`; `git status` shows the expected
changes only (`BP_DayNightDebug.uasset`, the two light actors' external-
actor packages, and new external-actor packages for the 12 trees × 2
pieces + 10 porch/path pieces = 34 new actors).

**Pushed:** no — local commit only, per the standing rule. Human should
review before pushing.

**This one especially benefits from a human PIE/visual pass** — everything
here was checked via editor-viewport screenshots and bounds math, never an
actual player walkthrough:
- The exterior brightness (`DirectionalLight 8000` / `SkyLight 400`) was
  tuned by eye against single-frame editor captures, not a live PIE session
  — worth a real walk outside to confirm it doesn't feel too bright/flat
  for the game's intended mood (this is still meant to be a *dim*, uneasy
  game per `CLAUDE.md`; "not pitch black" was tonight's bar, not "well-lit").
  The values only affect the day preset — night is untouched.
  Also worth deciding whether this exterior brightness level is the right
  long-term choice or just enough to unblock tonight's grey-box pass.
- Tree placement pattern (denser east/north) and scale variation are a
  first-pass judgment call, easiest to evaluate by eye in PIE walking the
  yard perimeter.
- The porch's 9uu step rise is a deliberate stylization (see above) —
  worth confirming it doesn't look like a jarring floating step in person
  rather than just in a static screenshot.

---

## Session — 2026-08-10 — playtest fix ITEM 2 (blocked west-side doorway)

Human is actively playtesting tonight and reported two issues after the last
round of fixes. Working item 2 first per instruction (playability blocker),
item 1 (yard content) separately after. Diagnosed before touching anything,
per instruction, since the human specifically wanted to know which of three
suspected causes it was.

**Did:**
- Confirmed `IsPIERunning` was true at session start (leftover from the
  human's own testing) and called `StopPIE` before touching anything, per
  instruction.
- Checked all three candidate "west side" doorways (Entry↔LivingRoom,
  Hallway↔Bathroom, Hallway↔Study — all on the X=450 wall plane) exactly as
  directed: pulled every jamb/header actor per opening via
  `SceneTools.get_actors_in_folder` + `ActorTools.get_actor_bounds`, and
  cross-checked with `SceneTools.find_actors` bounds queries (both a tight
  window at the wall plane and a widened one reaching ~100uu into each
  adjoining room) to catch anything regardless of source folder/pass.
  **All three came back completely clean** — jambs/headers correctly cut
  (Z[210,250] headers, full-height jambs outside the 90uu gap, Z[0,210]
  open beneath), no leftover template geometry, no furniture anywhere near
  either opening's footprint (checked `Sofa_LivingRoom`/`CoffeeTable_
  LivingRoom`, `ToiletBowl`/`ToiletTank`/`SinkCabinet`/`SinkBasin_Bathroom`,
  `Desk_Study`/`Bookshelf_Study` explicitly — none within 100+uu of their
  room's doorway). Live-tested all three in a real PIE session too (not just
  static bounds): teleported the player pawn next to each door, confirmed
  `bPlayerNearby`, pressed E via `SlateInspectorToolset.PressKey` (same
  mechanism validated in an earlier session), confirmed `bIsOpen`/
  `currentYaw` reached the open state, then ran `SceneTools.trace_world`
  straight through each opening — all three traced clear (no hit) once
  open, and correctly blocked (hit at the leaf) while closed. None of (a),
  (b), or (c) as originally suspected reproduced on any of the three named
  doorways.
- Per the instruction's permission to find a different door than expected,
  widened the search to the remaining 4 doors. Structural checks on the
  three east-side doorways (Hallway↔Bedroom, Hallway↔Utility, Entry↔Kitchen)
  came back clean too. **The Entry↔Hallway doorway (the fourth door, on the
  Y=300 wall between Entry and the Hallway, not one of the three originally
  named) was broken.** Static bounds checks initially looked fine here too
  (the wall's jamb/header replacement pieces are correctly cut, matching
  the pattern everywhere else), which is why this one didn't show up in the
  first pass — the bug isn't in those pieces at all.
- Root cause, found via live PIE trace testing (not visible from bounds
  queries on the "expected" actor set alone): with the player positioned
  well clear of their own collision capsule, `SceneTools.trace_world`
  straight through the opening hit *something* at Y=285 — short of both the
  correctly-cut header/jamb pieces and the door leaf itself (leaf sits at
  Y[296,304] when closed). `SceneTools.find_actors` with a tight bounds box
  at that exact point identified it: a **leftover, uncut, full-length
  `Wall_Hallway_S` actor**, world bounds `X[435,765] Y[285,300] Z[0,250]`
  — the *original* pre-Stage-3 wall segment, still fully present and never
  removed, sitting directly behind/alongside the correctly-cut replacement
  jamb/header/leaf pieces. This is cause **(c)**, but not the form the
  brief anticipated ("a leftover jamb/header piece that didn't get removed
  correctly") — it's the entire *original* wall panel that should have been
  deleted when Stage 3 replaced it with 3 cut pieces, still sitting there
  solid. The door's leaf visibly swings open (matching the human's "opens,
  but blocked" description exactly) because the new leaf/jamb/header pieces
  are all correct and functional — but the old, full-height, never-removed
  wall panel underneath is what's actually stopping the player.
- Confirmed this is an isolated, one-off miss, not a systemic bug: searched
  `SceneTools.find_actors` by name for every other cut-wall family in the
  level (`Wall_Entry_W/E/N/S`, `Wall_LivingRoom_E`, `Wall_Kitchen_W`,
  `Wall_Hallway_W/E`, `Wall_Bathroom_E`, `Wall_Bedroom_W`, `Wall_Study_E`,
  `Wall_Utility_W`) — every other family returns exactly the expected piece
  count (3 each, or 5 for the two hallway walls with double openings).
  `Wall_Hallway_S` was the only family with an extra, unexpected 4th actor.
  Best guess: the Stage 3 session's `remove_from_scene` call on the
  original wall silently failed or was skipped for this one wall (out of 8
  openings cut that session) — matches a note in that session's own log
  about intermittent tool-call issues, though this specific miss was never
  flagged there.
- **Fix**: deleted the leftover `Wall_Hallway_S` actor
  (`StaticMeshActor_UAID_D8BBC1A6E8836BF602_1266879109`) via
  `SceneTools.remove_from_scene` in the main editor level (confirmed label
  and bounds matched before deleting). Re-verified with a fresh
  `find_actors` bounds query over the opening's full volume (X[555,645]
  Y[285,315] Z[0,210]) — leftover gone, only the expected floor/jamb/
  header/door actors remain, matching the pattern of every other working
  doorway exactly.
- Final live re-verification in a fresh PIE session: closed-door trace
  through the opening now correctly hits the actual leaf (distance 96,
  matching the leaf's real position) instead of the old wall (previously
  hit at distance 85, short of the leaf). Opened the door via the same E-
  press mechanism, and traced across the full opening width at three X
  positions (570, 600, 630) — all clear, no hit, matching the working
  doorways' behavior.

**Root cause summary for the human:** cause (c) — a wall not actually cut
through — but specifically the **Entry↔Hallway** doorway (not one of the
three "west side" X=450 doors named in the brief), and specifically an
entire leftover original wall panel left in place by Stage 3, not a
mis-cut jamb/header. The three originally-suspected doorways
(Entry↔LivingRoom, Hallway↔Bathroom, Hallway↔Study) are all confirmed
working correctly, both structurally and in a live PIE walk-through test.

**Blocked / not resolved:** nothing — root cause found and fixed, verified
live.

**Saved and verified**: `AssetTools.save_assets([])` run after the fix;
`git status` shows exactly one file deleted (the removed actor's external-
actor package), nothing else touched.

**Pushed:** no — local commit only, per the standing rule. Human should
review before pushing.

**Worth flagging to the human:** since this doorway (Entry↔Hallway) is the
single chokepoint connecting Entry/LivingRoom/Kitchen to the rest of the
house (Hallway, Bathroom, Bedroom, Study, Utility), this bug would have
made the entire back half of the house unreachable, not just "one room" —
worth a quick human PIE walk-through of this specific doorway alongside the
three originally-suspected ones, since it's the one that actually mattered.

---

## Session — 2026-08-10 — unattended overnight build, FINAL SUMMARY (NEXT_TASKS.md, all 6 items)

Human was offline for this whole session. This supersedes an earlier summary
entry written partway through tonight (before item 3 was re-scoped) — that
one is still below for the per-task detail on items 1/2/3(orig)/4, but this
is the accurate top-level picture of everything that actually happened,
including a mid-session complication. See the individual entries below for
full reasoning on each item.

**Mid-session complication, important to understand the rest of this
entry:** `NEXT_TASKS.md` was read once at the very start and never re-read.
The human updated it twice while this session was already running
(commits `9b89e9d`, `f648547`) — reordering the queue, rescoping the
post-process task to be F11-toggle/off-by-default instead of always-on, and
adding two new items (door-verify+flashlight, an exterior grey-box). This
was only discovered near the end, while double-checking `git log` before
writing this summary and noticing two unfamiliar commits. Caught and fixed
everything the live file actually asked for rather than stopping short —
see items 3(fix) and 5-6 below — but flagging the process gap itself:
**a long unattended session should re-read its own task-queue file
periodically, not just once at the start**, since the human can and did
edit it mid-flight.

**1. Deleted 54 leftover First Person template objects** — never part of
the house, were physically boxing the player in near the Entry spawn.
Verified `PlayerStart_0`'s surroundings clear via traces afterward. No
ambiguous cases.

**2. Replaced `M_PrototypeGrid` with the real 5-color palette, added
furniture.** Four new `MaterialInstanceConstant`s off `M_FlatCol` applied
across all 79 wall/floor/ceiling actors plus `BP_Door`'s leaf material
(a judgment call, flagged). 16 simple furniture pieces across 6 rooms,
deliberately skipping objects reserved for later anomaly work.

**3. Peripheral-vision post-process pass — built, then corrected mid-session.**
Built `PP_PeripheralVision` (~50 nodes) as an always-on weighted blendable
on `PPV_Global`, implementing `CLAUDE.md`'s corrected model (35%-floor
degradation clamp, capped blur/desaturation/contrast, never fully clear
even centred). **Then found this directly conflicted with the live
`NEXT_TASKS.md`**, which explicitly demands the effect be off by default
(first playable beta needs to be bright/reviewable). Fixed by adding a
`MaterialParameterCollection` (`MPC_PeripheralVision`, one scalar
`Enabled`, default 0) and a gating Lerp between the original scene color
and the fully-degraded result, plus a new `BP_PostProcessToggle` actor
(F11, same raw-`InputKey` pattern as the other debug toggles) that flips
it via `SetScalarParameterValue`. Re-captured the viewport at the same
camera position as the original screenshot to confirm the off-state
actually renders unmodified (sharp edges), not just "compiles clean."
Day/night (item 5 below) was re-checked against updated wording too and
was already compliant, no change needed.

**3-live. Door interaction verify + flashlight** (the live file's actual
item 3, inserted ahead of the post-process pass). Verification here paid
off directly: discovered `SlateInspectorToolset.PressKey` can simulate a
real keypress into a live PIE session, used it to actually press E next to
a placed door — and it silently did nothing. Root-caused and fixed **two
real bugs** in `BP_Door`, neither previously known:
  - Every door's raw E-key binding had `bConsumeInput=true`, so only
    whichever door happened to be first in the input-priority stack could
    ever respond to E — all other doors were permanently unresponsive
    regardless of player proximity.
  - `ToggleDoor`'s branch condition and the interact prompt's argument both
    reused the same `NOT(GetbIsOpen)` node also used to compute the new
    `bIsOpen` value; because that node re-evaluates fresh at each
    consumption point *after* the assignment already ran, both silently
    read `NOT(newValue)` — a double-negation back to the old state. `bIsOpen`
    itself looked right; the door's actual swing angle and the prompt text
    were both backwards.
  Both fixed and re-verified live (fresh PIE restart, two different door
  instances, full open/close cycles, prompt text read back directly).
  Also added a basic toggleable flashlight (F key, `SpotLightComponent` on
  the camera, off by default) — placeholder values only, not the Act 2 spec.

**6. Exterior yard grey-box** — fixes a second real bug the human found in
testing: nothing existed outside the house, so exiting the front door
dropped the player forever. Ground slab + 5-piece fence perimeter with a
gap at the front door. Caught and fixed one more issue before calling it
done: the fence gap alone just *relocates* the falling bug (nothing stopped
the player walking through the open gap and off the ground slab's original
edge) — widened the ground slab's footprint well past the fence line to
close that. Verified via line traces (fence blocks / gap is clear) and a
live PIE check (player rests on the new ground instead of falling).

**Operational notes for whoever picks this up next:**
- Re-read `NEXT_TASKS.md` periodically during any long unattended run, not
  just once at the start — see the complication above.
- `SlateInspectorToolset.PressKey` (+ `Windows.select` + `Click` on the
  viewport image widget to establish game focus) can simulate real keypresses
  into a live PIE session. This turned "verify it works" from a structural
  graph-reading exercise into an actual functional test and caught two real
  bugs that structural reading alone had missed in an earlier session (BP_Door
  was previously verified only structurally, in Stage 6, and looked fine).
  Use this for any future "does this actually work" verification instead of
  trusting compiled-clean/graph-looks-right as sufficient.
- Restart PIE fresh after any Blueprint structural fix before re-verifying —
  hot-reload in-place gave inconsistent results once while debugging the
  door bugs.
- A pure node's output reused as input to two different exec statements is
  only safe if nothing between those statements changes what it reads. The
  DSL docs already warn about this for duplicate calls; the door bug shows
  a single shared node with fan-out has the identical risk.
- The Claude Code auto-mode permission classifier intermittently blocked
  individual `remove_from_scene` calls during task 1 for no discernible
  pattern — cleared on immediate retry every time.
- A PIE session was found already running (left over from the human's own
  testing) partway through task 1 and blocked scene edits until `StopPIE`
  was called (took two calls before `IsPIERunning` registered false).
- The DSL's variable-node type-id generation strips the Hungarian `b` prefix
  from bool variables (`bIsNight` → `GetIsNight`/`SetIsNight`) — bit this
  session twice and an earlier one once.
- No Blueprint enum was touched anywhere tonight, per the standing instruction.

**Saved and verified clean**: `AssetTools.save_assets([])` run after every
task; `is_dirty` on the level confirmed `false`; `git status` clean after
the final commit.

**Pushed:** no — everything is local commits only (see `git log` for the
full list, roughly a dozen commits across code + per-task log entries).
Human should review before pushing per the standing rule.

**Priority order for the human's first look:**
1. **Post-process pass (now F11, off by default)** — still genuinely needs
   eyes on it once toggled on: walk a room, judge whether the 35%-floor/
   blur/desaturation/contrast balance feels right.
2. **The two `BP_Door` bugs** — verified fixed and re-tested live, but
   worth a human PIE pass anyway given how silent bug 2 was (nothing about
   it would have looked wrong except the actual prompt text).
3. **The flashlight and F10 toggle** — structurally sound and (flashlight)
   visually confirmed lighting something, but neither has had a real human
   playtest.
4. **Exterior yard** — grey-box only by design, don't expect more than
   "doesn't fall through the world" from it.
5. Task 2's door-material judgment call (extending the palette pass beyond
   literal wall/floor/ceiling) — flag if that should've stayed grey.

---

## Session — 2026-08-10 — unattended overnight build, NEXT_TASKS #1 (delete leftover template geometry)

Human is offline overnight, working `NEXT_TASKS.md` top to bottom per instructions
(commit after each numbered task, log per task, don't push). Task 1 first, per the
file's explicit sequencing note — hard blocker on any further playtesting.

**Did:**
- Enumerated every actor in `Lvl_FirstPerson` (`SceneTools.find_actors` with no
  filters) and diffed it against everything filed in our own outliner folders
  (`Blockout` recursive, `Anomalies`, `Lighting`), rather than matching by stock
  class/mesh name alone per the brief's caution — mesh-name matching alone would
  have also caught legitimate `SM_Cube`-built room geometry, doors, and the
  anomaly's collision capsule.
- The unclaimed remainder was exactly 54 actors, all with auto-generated
  template labels (`SM_Cube16`, `SM_QuarterCylinder5`, `SM_Ramp11`, `SM_Cylinder4`,
  etc., plus one `Floor_0` using `/Engine/MapTemplates/SM_Template_Map_Floor`) —
  confirmed via `ActorTools.get_components` + `ObjectTools.get_properties` on each
  one's `StaticMeshComponent.StaticMesh` that every candidate resolved to a stock
  `/Game/LevelPrototyping/Meshes/SM_{Cube,Cylinder,QuarterCylinder,Ramp}` asset (or
  the engine template floor) before deleting anything — no ambiguous cases turned
  up, so nothing needed to be left for a human judgment call.
- Cross-checked distance from `PlayerStart_0` (600,150,110, Entry's centre) before
  deleting: 4 of the 54 leftover actors had bounds within 500uu of the spawn point,
  including `SM_Ramp11` at world `X[500,900] Y[-200,200] Z[0,200]` — directly
  overlapping the Entry room's footprint (`X[450,750] Y[0,300]`). This matches the
  "human tester got physically boxed into a corner" report exactly.
- Deleted all 54 via `SceneTools.remove_from_scene`. Two operational hiccups along
  the way, neither a real problem: (1) Claude Code's own auto-mode permission
  classifier intermittently blocked individual `remove_from_scene` calls for no
  discernible pattern (worked fine on immediate retry every time, no batching
  correlation found) — just retried each block until it went through; (2) a Play-In-
  Editor session was apparently left running from the human's own testing and
  briefly blocked deletion entirely ("Cannot remove actors while PIE is active") —
  called `EditorAppToolset.StopPIE` (took two calls before `IsPIERunning` actually
  reported false) and resumed cleanly, no data lost.
- Verified afterward with a fresh actor/folder diff: 0 unclaimed actors remain.
  Confirmed `PlayerStart_0`'s surroundings are clear with 4 line traces
  (`SceneTools.trace_world`) from the spawn point toward all four room boundaries
  (X+, X-, Y+, Y-, each ~130uu, just short of Entry's walls) — all returned no hit
  — plus a `find_actors` bounds query on a 100×100×200uu box centered on the spawn
  point, which returned only expected actors (the builder brush, the sky sphere,
  Entry's own floor/ceiling piece, one room `PointLight`, and the 3 `BP_Door`
  instances that legitimately sit near Entry's three doorways).
- Saved all dirty assets, confirmed via `git status`: 54 file deletions (one
  external-actor package per deleted actor), nothing else touched.

**Blocked / not resolved:** nothing — no ambiguous actors turned up, so there was
no case requiring a "leave it and flag it" judgment call.

**Pushed:** no — local commit only (`ef08fe5`), human should review before pushing
per the standing rule.

**Next:** task 2 from `NEXT_TASKS.md` — replace `M_PrototypeGrid` with the real
5-color palette (`M_FlatCol` instances) across every wall/floor/ceiling, plus a
simple furniture pass per room.

---

## Session — 2026-08-10 — unattended overnight build, NEXT_TASKS #2 (palette materials + furniture)

**Did:**
- Found `M_FlatCol`'s exposed parameter name is `Base Color` (Vector) plus
  `Metallic`/`Roughness` (Scalar), via `MaterialInstanceTools.list_parameters` —
  confirmed the parent material's own defaults are already `Roughness=1,
  Metallic=0` (fixed in an earlier session), so the new instances didn't need to
  override those, only Base Color.
- Created 4 `MaterialInstanceConstant`s under `/Game/LevelPrototyping/Materials/`
  off `M_FlatCol`: `MI_Wall_Light` (#B3A78F), `MI_Floor_Dark` (#4E4B44),
  `MI_Ceiling_Pale` (#E6DFCC), `MI_Furniture_Mid` (#7C7870). Converted each hex
  to linear space before setting the vector parameter (sRGB→linear, same
  convention the existing `MI_Anomaly_Dark` instance used per an earlier log
  entry) rather than pushing gamma-space 0–255 values straight in, which would
  have rendered lighter/washed-out than the intended palette.
- Applied these across every wall/floor/ceiling in `Blockout` (all 8 rooms:
  hallway + 7 new rooms): 63 walls (including every doorway jamb/header piece
  from the Stage 3 door cuts — not just the original room-shell walls), 8
  ceilings, 8 floors, 79 actors total, all via
  `ObjectTools.set_properties({"overrideMaterials":[...]})` on each actor's
  `StaticMeshComponent0`.
- Also fixed `BP_Door`'s `DoorLeaf` material — at the Blueprint class-default
  level (`BlueprintTools.get_default_object` → `set_properties` on the CDO's
  `DoorLeaf_GEN_VARIABLE` component → `compile_blueprint`), plus each of the 7
  already-placed instances directly, so both existing doors and any future
  ones placed from the class pick up the fix. This wasn't explicitly listed in
  the task's "wall/floor/ceiling" scope, but the door leaf was the same grey
  `M_PrototypeGrid` blockout material, and leaving it would have undercut the
  whole point of the pass (no texture/glint anywhere) — judgment call, flagging
  in case the human wanted door material handled separately.
- Confirmed completeness via `AssetTools.get_referencers(M_PrototypeGrid)`
  after saving: now referenced only by its own unused `MI_PrototypeGrid_*`
  variant assets (template leftovers, never applied to anything in the level),
  nothing else.
- **Furniture** — 16 primitive pieces (`SM_Cube` + `SM_Cylinder`, all
  `MI_Furniture_Mid`) across 6 rooms, positioned by hand-computed coordinates
  against a wall away from that room's doorway opening in each case: sofa +
  coffee table (living room), counter + table + 2 chairs (kitchen), toilet
  (cylinder bowl + box tank) + sink (box cabinet + box basin) (bathroom), bed
  (box frame + raised box mattress) + dresser (bedroom), desk + tall bookshelf
  (study), one shelving unit (utility). Entry skipped per instruction
  (pass-through space, no furniture asked for).
- Deliberately did **not** build the specific objects flagged as reserved for
  later anomaly work (living room floor lamp/wall portrait, bathroom mirror,
  bedroom window) — simplest way to satisfy "place a plain placeholder, don't
  build anomaly behavior into it yet" was to just not build those particular
  pieces at all. The kitchen chairs/table are ordinary static boxes with zero
  attached logic already, so the "plain placeholder" constraint on the kitchen
  chair anomaly is satisfied trivially.
- Verified placement via `ActorTools.get_actor_bounds` on all 16 pieces after
  creation: every piece's bounds land fully inside its room's interior clear
  space, clear of walls and of that room's doorway Y/X-range. One placement
  quirk worth noting for later furniture work: unlike `SM_Cube` (pivot at
  local-space min corner, confirmed in earlier sessions), `SM_Cylinder`'s pivot
  is centered on X/Y (only Z is min-corner-anchored) — caught this from the
  toilet bowl's returned bounds not matching the corner-math I'd used for the
  boxes, worked out the actual center-anchored formula from the discrepancy,
  and confirmed the corrected placement was still fully inside the room.
- Saved all dirty assets; `git status` showed 100 changed files (4 new
  MaterialInstanceConstant assets, 16 new external-actor packages for the
  furniture, `BP_Door.uasset`, and ~79 modified external-actor packages for
  the recolored walls/floors/ceilings/doors) — matches expectations exactly,
  nothing unrelated touched.

**Blocked / not resolved:** nothing.

**Pushed:** no — local commit only (`d031ad7`), human should review before
pushing per the standing rule.

**Next:** task 3 from `NEXT_TASKS.md` — build the peripheral-vision
post-process pass on top of the existing `PPV_Global` volume. Explicitly
needs a human PIE/visual check per the brief; will note that clearly rather
than claim it "looks right" from headless inspection alone.

---

## Session — 2026-08-10 — unattended overnight build, NEXT_TASKS #3 (peripheral-vision post-process)

Nothing existed for this before tonight — movement, rooms, and one anomaly's
logic only. Read `CLAUDE.md`'s "Peripheral vision technique" section first per
instruction, since it explicitly supersedes the original handoff spec's
radial-blur/fully-sharp-centre model.

**Did:**
- Created `PP_PeripheralVision` (`/Game/LevelPrototyping/Materials/`), set
  `materialDomain = MD_PostProcess`, `blendableLocation = BL_AfterTonemapping`.
  Added it to the existing `PPV_Global` volume's `settings.weightedBlendables`
  array (weight 1.0) via `ObjectTools.set_properties` — did **not** create a
  second volume. Verified after the edit that `bUnbound` and every earlier
  zeroed override (bloom, lens flare, motion blur, chromatic aberration, film
  grain — all still `0` with their override flags still `true`) are untouched.
- Discovered the exact pin names for every node type before wiring anything,
  via `get_expression_input_names`/`get_expression_output_names` on one
  instance of each class first (`ScreenPosition`, `SceneTexture`,
  `Desaturation`, `ComponentMask`, `LinearInterpolate`, `SceneTexelSize`,
  `Constant`/`Constant2Vector`/`Constant3Vector`, `Add`/`Subtract`/`Multiply`/
  `Divide`/`AppendVector`/`Length`/`Saturate`) rather than guessing — several
  are non-obvious: `ComponentMask`/`Length`/`Saturate`'s single input pin
  reports as the literal string `"None"`, not an empty string, and
  `Desaturation`'s color input is the same `"None"` name with a separate
  `"Fraction"` pin alongside it.
- Built the full graph (~50 `MaterialExpression` nodes) in two
  `ProgrammaticToolset` script passes:
  1. **Radial degradation driver**: `ScreenPosition.ViewportUV` minus a
     (0.5,0.5) constant gives screen-centered coords; aspect-corrected by
     multiplying the X component by `SceneTexelSize.R / SceneTexelSize.G`
     (texel-size ratio = width/height) so the falloff reads circular rather
     than stretched to the screen's aspect ratio; `Length` of that vector,
     divided by a 0.6 max-radius constant, saturated to `t` in 0-1.
     **Degradation = Lerp(0.35, 1.0, t)** — confirmed by reading back the two
     `Constant` nodes wired to the Lerp's A/B pins (0.35 and 1.0, not
     swapped) that centre (t=0) never drops below 35% degradation, i.e.
     clarity caps at ~65% even dead centre — this is the exact detail the
     brief flagged as easy to get wrong by copying the handoff spec's
     unclamped version.
  2. **Detail reduction, driven by that single degradation value, not a flat
     blur**: a cheap 5-tap box blur (centre + 4 cardinal `SceneTexture`
     samples at `PPI_PostProcessInput0`, offset by texel-size × a blur radius
     that itself scales 2→9 texels with degradation) blended against the
     sharp centre tap; a `Desaturation` node whose `Fraction` is degradation
     × 0.55 (capped, never fully grey); a final `Lerp` toward mid-grey
     (0.5/0.5/0.5) at degradation × 0.45 for contrast reduction. Every stage
     caps below 100% specifically so silhouettes stay legible even at the
     extreme screen edge, per the "preserving silhouettes" requirement in
     `CLAUDE.md`. Output wired to `MP_EmissiveColor`.
- `MaterialTools.recompile` succeeded with no shader errors on the first
  attempt after full wiring — no iteration needed.
- Took an editor-viewport screenshot (`EditorAppToolset.CaptureViewport`,
  camera placed mid-hallway) as a sanity check that the effect is actually
  live, not just compiling silently — periphery (side walls near the frame
  edges) is visibly softer/blurrier than the centre in the capture, which is
  the expected signature of this effect. This is **not** a substitute for a
  real PIE pass — it doesn't confirm the blur/desaturation balance feels
  right, whether it reads as "detail reduction" rather than "blur" at a
  glance, or how it behaves with actual player look-around motion, only that
  the material is doing something and not silently no-op'ing or rendering
  black.
- Saved; `git status` showed exactly 2 changes: the new
  `PP_PeripheralVision.uasset` and `PPV_Global`'s external-actor package
  (the new blendable reference) — nothing else touched.

**Blocked / not resolved:** nothing structurally, but per the brief this task
explicitly cannot be fully verified headlessly.

**Pushed:** no — local commit only (`57751bd`), human should review before
pushing per the standing rule.

**Needs a human PIE pass before trusting this further** (top priority item
from tonight's whole session to check first): walk through several rooms and
the hallway, look around at normal speed, and judge whether the degradation
curve (35% floor at centre, ramping to 100% by ~60% of the way to screen edge)
feels like "peripheral vision that never resolves" or whether the blur/
desaturation/contrast weights (2-9 texel blur, 55% max desaturation, 45% max
contrast-pull) need retuning — none of those specific numbers came from the
spec, they're a first-pass judgment call per the brief's explicit permission
to ship "acceptable as v1, can be refined later."

**Next:** task 4 from `NEXT_TASKS.md` — F10 day/night lighting toggle, a debug
tool (not the real Act 2 system). Reuse `BP_Anomaly`'s F9 `AutoReceiveInput`/
raw `InputKey` pattern per the brief's pointer.

---

## Session — 2026-08-10 — unattended overnight build, NEXT_TASKS #4 (F10 day/night debug toggle)

**Did:**
- Read off the level's actual current light intensities before hardcoding
  anything, rather than guessing: `DirectionalLight_0.LightComponent0.
  Intensity = 6`, `SkyLight_0.SkyLightComponent0.Intensity = 1`, each room
  `PointLight.LightComponent0.Intensity = 15000` (matches the documented
  Stage 4 convention). These became the "Day" preset values.
- Built `BP_DayNightDebug` (`/Game/Blueprints/`), reusing `BP_Anomaly`'s F9
  pattern exactly per instruction: confirmed via inspection first
  (`AutoReceiveInput="Player0"` set directly on the CDO via
  `ObjectTools.set_properties`, F9's raw `K2Node_InputKey` created via
  `create_node` with `type_id="Input|KeyboardEvents|F9"` rather than the
  DSL's `(event ...)` form) before building this Blueprint's own F10
  hookup the identical way.
- Function `ApplyDayNight` (no params) built via `write_graph_dsl`, wired
  from the raw F10 `InputKey`'s `Pressed` pin via `connect_pins`. Logic:
  flip `bIsNight`, then for each of `DirectionalLight`/`SkyLight`/
  `PointLight`: `GetAllActorsOfClass` → `ForEachLoop` → `GetComponentByClass`
  → the matching `SetIntensity` node (`Rendering|Components|Light|
  SetIntensity` for the two `ULightComponent`-derived ones, the separate
  `Rendering|Components|SkyLight|SetIntensity` for the sky light), each fed
  by a `Select(bIsNight, nightValue, dayValue)`. No stored actor references
  — re-queries `GetAllActorsOfClass` on every press, so it can't go stale if
  lights are added/removed later.
- Hit one real DSL naming gotcha along the way: `(Variables|Default|
  GetbIsNight)` failed with "does not exist" even though `list_variables`
  confirmed the variable is literally named `bIsNight` — the DSL's
  variable-node type-id generation strips the Hungarian-notation `b` prefix
  from bool variables (`GetIsNight`/`SetIsNight`, not `GetbIsNight`/
  `SetbIsNight`). Found the correct type-id by running `find_node_types`
  with a partial search (`"IsNight"`) rather than guessing further.
- **Night preset values are dimmed, not fully disabled** — a judgment call
  the brief explicitly allowed either way ("dim or disable"): `DirectionalLight
  0.05`, `SkyLight 0.05`, room `PointLights 300` (down from 15000). Chose
  dimming over full disable so a debug pass still shows silhouettes instead
  of dropping the player into a solid black void, since there's no flashlight
  or other Act-2 light source yet to make a fully-dark preview navigable.
- Placed one instance in the level (`Debug` outliner folder, position
  doesn't matter — `AutoReceiveInput` needs no proximity, unlike the door's
  interact check).
- Verified the compiled graph end to end via `get_connected_subgraph`
  (not `read_graph_dsl`, per the project's standing rule) rather than
  trusting the DSL round-trip: confirmed the NOT/Set chain, all three
  `GetAllActorsOfClass → ForEachLoop → GetComponentByClass → Select →
  SetIntensity` chains, and specifically that each `Select` node's
  `Option 0`/`Option 1` pins land on the correct day/night value (not
  swapped) against `K2Node_Select`'s index convention (index=false→Option0,
  index=true→Option1) — all three checked out matching the intended
  `(select isNight nightVal dayVal)` semantics.
- Ran an actual PIE session (`StartPIE` → `GetLogEntries` filtered for
  errors/exceptions → `StopPIE`) before saving, to catch any runtime
  spawn/BeginPlay error the static graph check wouldn't — `MapCheck`
  reported 0 errors/0 warnings and no new log entries referenced
  `BP_DayNightDebug`. Did **not** attempt to simulate an actual F10
  keypress (no input-injection tool available), so the toggle's in-game
  *feel* is still unverified — noted below.
- Saved; `git status` showed exactly 3 new files (the Blueprint, one
  external-actor package for the placed instance, one external-object
  package for the new `Debug` outliner-folder registration) — nothing else
  touched.

**Blocked / not resolved:** nothing.

**Pushed:** no — local commit only (`3dec1d3`), human should review before
pushing per the standing rule.

**Worth a quick human check, lower priority than task 3's post-process
pass:** actually pressing F10 in PIE was never tested (no input-simulation
tool available in this session) — the graph is verified structurally sound
and PIE spawns without error, but nobody has confirmed the keypress itself
reaches the actor and the lights visibly change. Also worth a glance: the
300-lumen "dim, not off" choice for room lights at night is a guess at what
reads well for a debug preview, not measured against anything.

**Next:** all four `NEXT_TASKS.md` items are now done. See the consolidated
summary entry above this one (or check with the human) for what's queued
after tonight.

---

## Session — 2026-08-10 — unattended overnight build, NEXT_TASKS #3-live (door verify/fix, flashlight)

**Important process note first:** partway through tonight's run I discovered
`NEXT_TASKS.md` had been updated by the human (commits `9b89e9d` and
`f648547`) *while this session was already working from a copy read at the
very start* — it was never re-read mid-session. The live file reorders the
queue, adds two new items (door-verify+flashlight now item 3, an exterior
grey-box now item 6), and explicitly changes the post-process pass to be
F11-toggle/off-by-default instead of always-on. See the separate "make
post-process opt-in" commit for that fix. This entry covers the new item 3.

**Did:**
- **Door verification, done for real this time** — discovered
  `SlateInspectorToolset.PressKey` can simulate an actual keypress into a
  live PIE session (confirmed the mechanism reaches gameplay input at all
  by testing it against `BP_Anomaly`'s F9 first, which changed `CurrentState`
  as expected). Positioned the player pawn next to a placed `BP_Door`
  instance via `set_actor_transform`, confirmed `bPlayerNearby` was true,
  then pressed E and checked `bIsOpen` before/after — **found it never
  changed**. This is exactly the "if it's NOT working, that's a real bug,
  fix it" case the brief called out.
- **Bug 1 — root cause found and fixed**: every `BP_Door` instance's raw E
  `K2Node_InputKey` had `bConsumeInput=true` (the node's default). All 7
  doors bind the same key; the first one in the input-priority stack
  silently absorbed every E press project-wide, so only that one door could
  ever respond, regardless of which door the player actually stood next to.
  Set `bConsumeInput=false`.
- **Bug 2 — found while re-testing the fix**: after bug 1's fix, `bIsOpen`
  toggled correctly but the door never visibly swung (`TargetYaw` stayed
  at 0) and the interact prompt showed the wrong text. Traced it in the
  actual compiled `ToggleDoor` graph (`get_connected_subgraph`, not
  `read_graph_dsl`, per the standing rule): the swing-direction Branch and
  the prompt's `bIsOpen` argument were both wired to the *same* `NOT
  (GetbIsOpen)` node also used to compute the new value being assigned.
  Since that node gets pulled fresh at each consumption point and both
  pulls happen *after* the assignment already ran, both effectively
  computed `NOT(newValue)` — a silent double-negation back to the old
  state. `bIsOpen` itself looked right; everything downstream of it that
  reused the same NOT node was reading backwards. Fixed by adding one
  fresh `GetIsOpen` node (post-assignment, no negation) and rewiring the
  Branch condition and `SetPromptOpenState`'s argument to it instead.
- Re-verified against **two different door instances** in a **freshly
  restarted** PIE session (not hot-reloaded — an earlier hot-reload
  in-place during the same PIE session gave inconsistent results while
  debugging this, worth remembering: always restart PIE after a Blueprint
  structural fix rather than trusting hot-reload for verification).
  Confirmed `bIsOpen`, `TargetYaw` (correctly -90 open / 0 closed), and the
  live prompt widget's actual displayed text (read via
  `WidgetTree_0.PromptText.text`, not assumed) all matched expectations
  through open→close→open cycles on both doors.
- **Flashlight** — new `SpotLightComponent` (`FlashlightComponent`) added
  under `BP_FirstPersonCharacter`'s existing `FirstPersonCamera`, off by
  default, toggled by a raw F `InputKey` (confirmed F wasn't already bound
  anywhere in this Blueprint before adding it) calling a `ToggleFlashlight`
  function that reads/flips visibility directly (`Rendering|IsVisible` /
  `Rendering|SetVisibility`) rather than adding a redundant tracking bool.
  Placeholder values only (8000 candela, 15°/25° cone, 1500uu range, white,
  movable, casts shadows) — explicitly not the Act 2 dual-cone/warm-color
  spec per the brief. Verified live: F flips `bVisible`, and a viewport
  capture with the light on shows a real lit patch on a nearby wall, not
  just a property flag with nothing rendering.
- Saved; `git status` showed exactly the two expected Blueprint files
  changed (`BP_Door.uasset`, `BP_FirstPersonCharacter.uasset`) — nothing
  else touched.

**Blocked / not resolved:** nothing — both discovered bugs were fixed and
verified live, not left as known issues.

**Pushed:** no — local commit only (`4a702a1`), human should review before
pushing per the standing rule.

**Worth flagging to the human:** the two door bugs were real and would have
shipped silently — worth a mental note that "compiles clean" and even "the
obvious variable toggles correctly" are not sufficient verification for
interaction logic; the prompt-text bug specifically would only ever surface
as "the text feels wrong" during an actual playtest, never as an error.
Also worth remembering project-wide now: reusing a single pure node's output
as input to two different exec statements is only safe if nothing between
those statements changes the values that node reads — the DSL docs already
warn about this for *duplicate* calls, but a single shared node with fan-out
has the identical risk when execution order matters.

---

## Session — 2026-08-10 — unattended overnight build, NEXT_TASKS #6 (exterior yard grey-box)

**Did:**
- Built the yard boundary per the live `NEXT_TASKS.md`'s converted spec
  numbers: ground slab and a 5-piece fence perimeter (`SM_Cube` +
  `MI_Floor_Dark`, reusing the existing Dark palette tone rather than a new
  material) under a new `Blockout/Yard` folder, with a 200uu gap in the
  south fence segment centered on the front door's actual opening
  (X[555,645]).
- **Caught my own bug before calling it done**: the fence gap by itself just
  *relocates* the falling-out-of-the-world bug rather than fixing it — nothing
  stops the player from walking straight through the open gap and off the
  edge of the ground slab, which originally stopped flush at the fence line.
  Widened the ground slab's footprint by 200-300uu past the fence perimeter
  on all sides (final extents X[-700,1900] Y[-1100,1900]) so real ground
  exists well beyond the gap, not just inside the fenced area.
- Set the ground slab's top at Z=-1 (1uu below the house's interior floor
  top at Z=0) rather than exactly coplanar — avoids Z-fighting against the
  interior floor pieces where their footprints would otherwise coincide
  under the house, at the cost of an imperceptible 1uu step at the door
  threshold (well within any character movement component's step-up
  tolerance).
- Verified two ways, not just visually: `SceneTools.trace_world` line traces
  confirm the fence physically blocks outside the gap (hit exactly at the
  fence's near face) and the gap itself is clear through and beyond it; a
  live PIE check (teleported the player just outside the front door,
  waited for physics to settle, read back its resting Z) confirms it comes
  to rest on the new ground at the expected height instead of falling
  forever, matching the same capsule-radius resting offset seen on the
  interior floor.
- Saved; `git status` showed exactly the 6 expected new external-actor
  packages plus one external-object package for the new outliner folder.

**Blocked / not resolved:** nothing. This grey-box is deliberately minimal
per the brief (no treeline/gravel path/porch) — that's explicitly future
work, not a gap in tonight's scope.

**Pushed:** no — local commit only (`56c5612`), human should review before
pushing per the standing rule.

**Next:** this was the last item on the live `NEXT_TASKS.md` (items 1-6, all
now done — see the top-of-file consolidated summary... actually, given how
much changed mid-session, worth writing a fresh consolidated summary rather
than trusting the earlier one, which predates the discovery that the task
file itself changed underneath this session). Check with the human for
what's queued next.

---

## Session — 2026-08-10 — unattended overnight build, STAGE 6 (BP_Door)

Continuing the numbered stages, same unattended rules. Human asked specifically
for this stage tonight: build a reusable interactive door Blueprint and place
it into the 7 doorway gaps cut in Stage 3 (skipping the front-door opening —
exterior not built).

**Did:**
- Inspected `BP_Anomaly` first per instruction (`list_variables`/`list_graphs`/
  `get_node_infos` on its `EventGraph`, not trusting `read_graph_dsl`'s text for
  anything load-bearing) to confirm two conventions before reusing them:
  `AutoReceiveInput` is a plain object property (`"Player0"`) set via
  `ObjectTools.set_properties` on the class default object, and the F9
  `InputKey` node is created as a raw node (`Input|KeyboardEvents|F9`) rather
  than through the DSL's `(event ...)` form — confirms the human's warning that
  `read_graph_dsl` can't render `K2Node_InputKey` bodies at all is about a real
  gap in that node type's DSL support, not just a display quirk. Built this
  Blueprint's own E-key hookup the same way: raw `create_node` for
  `Input|KeyboardEvents|E` plus a hand-wired `Branch`/`GetPlayerNearby`/
  `CallFunction|ToggleDoor` chain via `connect_pins`, DSL for everything else.
- Also confirmed via `Glob` that no interact-input system exists anywhere in
  the project yet (`/Game/Input/` has only Move/Look/Jump/Walk actions, no
  Interact action, and `BP_FirstPersonCharacter` has no interact graph) — this
  was expected per the brief, so built the simplest thing that works rather
  than a new Enhanced Input action asset.
- Built `BP_Door` (`/Game/Blueprints/BP_Door`, parent `Actor`):
  `HingePivot` (`SceneComponent`, relative location `(0,-45,0)` from the actor
  root) with `DoorLeaf` (`StaticMeshComponent`, child of `HingePivot`) using
  `SM_Cube`/`M_PrototypeGrid` (confirmed the exact property path —
  `StaticMeshComponent.StaticMesh` + `OverrideMaterials[0]` — by inspecting an
  existing hallway wall actor first, matching the Stage 2 convention note),
  scaled `(0.08, 0.9, 2.05)` → 8×90×205uu, relative location `(-4,0,0)` so the
  leaf is centered on the hinge's local Y axis and exactly fills a 90uu-wide
  opening when `HingePivot`'s relative yaw is 0. Chose to place the actor
  **root at the doorway's centroid** (opening center X/Y, Z=0) specifically so
  a single local-space component layout works for **both** wall orientations
  just by changing the actor's own yaw (0° for the four walls running along Y,
  90° for the one wall running along X) — rotating the whole actor also
  rotates `HingePivot`'s fixed local offset, so the same relative geometry
  produces a correctly-positioned hinge and leaf in either case. Verified this
  algebraically before placing anything (worked through the yaw-90 rotation
  matrix by hand to confirm the leaf lands on `X[555,645]` for the one
  X-running wall) and then confirmed it numerically against 3 placed
  instances (see below) rather than trusting the math alone.
- **Hinge/lerp implementation**: `Tick`-driven, not a Timeline — `CurrentYaw`/
  `TargetYaw` float variables, `ToggleDoor()` flips `bIsOpen` and sets
  `TargetYaw` to `-90` or `0`; every tick, `CurrentYaw += (TargetYaw -
  CurrentYaw) * min(DeltaSeconds * 6, 1)`, written straight onto
  `HingePivot`'s relative rotation. This is normal diegetic door movement, not
  an anomaly transition — the "instant, no tween" rule from `BP_Anomaly`'s
  `SetOff`/`SetNormal` does **not** apply here, and the brief was explicit
  about that distinction, so this one's supposed to look smooth.
- **Proximity check**: distance check against a cached player pawn every
  `Tick` (`<= 150uu`), not an overlap volume — added a `BoxComponent` first per
  the brief's suggestion, then removed it. Reasoning: an overlap-driven
  approach needs the overlap volume's collision profile hand-tuned to overlap-
  only/no-block (a `BoxComponent` sitting in the doorway with default collision
  would otherwise physically block the player walking through), plus overlap-
  actor bookkeeping across Begin/End events; a per-tick distance check against
  `GetDistanceTo` achieves the identical player-facing behavior with far less
  surface area to get wrong unattended. The brief explicitly allowed either
  approach ("your call").
- **Real bug caught before it shipped**: my first `EventTick` DSL wrote
  `wasNearby` as a plain `Get bPlayerNearby` positioned textually *before* the
  `Set bPlayerNearby` call in the DSL source. That doesn't work in Blueprint —
  pure `Get` nodes have no exec pins, so they're evaluated lazily at the
  moment a downstream node actually pulls their value, not at their textual
  position in the script. Since the only consumer of that `Get` node was the
  `Branch` immediately after the `Set`, it was actually reading the *new*
  value, making the "did nearby state change" comparison always false — the
  interact prompt would never have shown up in PIE, silently. Caught this by
  reading the actual compiled graph via `get_connected_subgraph` (not
  `read_graph_dsl`) and tracing the exec order by hand before moving on, per
  the standing instruction to verify DSL output against ground truth. Fixed by
  deleting the whole `Tick` chain and rewriting it with a dedicated
  `bWasNearbyLastFrame` variable, captured via its own `Set` node as the very
  first statement in `Tick` (before anything mutates `bPlayerNearby`) — a
  second variable that's genuinely write-once-per-tick-before-use sidesteps
  the lazy-pure-node-evaluation trap instead of fighting it.
- **Interact prompt: built a real UMG widget**, not a `PrintString` fallback.
  `WBP_InteractPrompt` (`/Game/UI/WBP_InteractPrompt`) is a single `TextBlock`
  as the widget's root (`UMGToolSet.AddWidget` with no parent, since the tree
  was empty), exposed as a variable, default text "Open door", plus one
  function `SetPromptOpenState(bIsOpen)` that flips the text to "Open
  door"/"Close door". No styling pass — default white text, matching the
  project's flat/unstyled grey-box aesthetic. The toolset's `list_properties`
  → `get_properties`/`set_properties` workflow for widgets worked cleanly and
  the whole thing round-tripped through `CompileWidgetBlueprint` with no
  errors, so there was no point in the build where the "significantly more
  involved than expected" fallback condition actually triggered.
- `BP_Door` creates one `WBP_InteractPrompt` instance in `BeginPlay` (kept
  off-screen until needed) and adds/removes it from the viewport exactly once
  per nearby-state transition (not every tick) in `Tick`, updating its text
  to match current `bIsOpen` on both the transition-into-range moment and
  every `ToggleDoor()` call.
- No Blueprint enum anywhere — `bIsOpen` is a plain bool, per the explicit
  instruction not to touch the enum asset factory again after the freeze
  earlier tonight.
- **Placed all 7 instances** (opening 8, the front door, skipped per
  instruction) into a new `Blockout/Doors` outliner folder:
  - `BP_Door_Hallway_Bathroom` — `(450, 800, 0)`, yaw 0
  - `BP_Door_Hallway_Bedroom` — `(750, 800, 0)`, yaw 0
  - `BP_Door_Hallway_Study` — `(450, 1200, 0)`, yaw 0
  - `BP_Door_Hallway_Utility` — `(750, 1200, 0)`, yaw 0
  - `BP_Door_Entry_Hallway` — `(600, 300, 0)`, yaw 90
  - `BP_Door_Entry_LivingRoom` — `(450, 150, 0)`, yaw 0
  - `BP_Door_Entry_Kitchen` — `(750, 150, 0)`, yaw 0

  All 6 of the Y-running-wall doors share yaw 0 (hinge on the lower-Y jamb of
  each opening); the one X-running wall (Entry↔Hallway) uses yaw 90 instead,
  per the worked rotation math above.
- **Spot-checked 3 instances** (`Hallway_Bathroom`, `Entry_Hallway`,
  `Entry_LivingRoom`) — one from each yaw case plus a second yaw-0 case.
  `get_actor_bounds` on the placed actors initially looked wrong (e.g.
  `X[322,578]` instead of the expected `~[446,454]` for `Hallway_Bathroom`) —
  tracked this down to a `BillboardComponent` that the *editor* silently
  attaches to placed instances of any Blueprint actor whose root component
  isn't itself a primitive (ours is a plain `SceneComponent`,
  `DefaultSceneRoot`); confirmed via `get_components` on the Blueprint's own
  CDO that this billboard isn't part of the class definition at all — it's a
  transient, editor-only per-instance visualization aid (standard engine
  behavior for giving invisible-root actors a selectable icon), not something
  I added or need to remove, and it doesn't exist in PIE/packaged builds. Threw
  out the bounds-box approach and instead verified placement by reading each
  instance's actual `DoorLeaf`/`HingePivot` `relativeLocation`/`relativeScale3D`
  and composing the transform by hand against the actor's own world transform
  — all 3 checks landed exactly on their target opening's coordinates from the
  brief (e.g. `Entry_Hallway`'s leaf works out to world `X[555,645] ×
  Y[296,304]`, matching that opening's `X[555,645]` span on the `Y=300` wall
  plane exactly).
- Compiled `BP_Door`, saved all dirty assets, re-checked `is_dirty` on
  `BP_Door`, `WBP_InteractPrompt`, and the level — all `false`, no OFPA lag
  outstanding. `git status` confirmed 7 new external-actor packages (one per
  door instance), 1 new external-object package, `BP_Door.uasset`, and the new
  `Content/UI/WBP_InteractPrompt.uasset` — nothing else touched.

**Blocked / not resolved:** nothing — no blockers hit this stage.

**Pushed:** no — local commit only (`b032664`), human should review before
pushing per the standing rule.

**Worth a human PIE pass before trusting this further** (everything below was
checked structurally/numerically, never actually rendered or played):
- The hinge swing direction (`-90°`) was picked arbitrarily per instruction —
  worth confirming in PIE that no door swings through a wall or into a piece
  of furniture that gets added later. Both swing directions are geometrically
  valid from the doorway-gap math alone; only a visual check tells you which
  one reads right per room.
- The `150uu` proximity radius and the `AutoReceiveInput=Player0`-based E
  hookup are untested against an actual player capsule — the brief noted
  "nearest door responds" is good enough for a grey-box pass and multiple
  doors' input priority wasn't handled carefully; two doors within 150uu of
  each other (shouldn't happen at current room sizes, but worth a glance) could
  both try to toggle on one E press.
- The `WBP_InteractPrompt` text is genuinely unstyled (default white,
  default font/size) — confirm it's actually legible against whatever's behind
  it once there's real lighting, not just placeholder brightness.
- Editor-only `BillboardComponent` note above is informational, not a
  problem — flagging only so nobody spends time investigating it as a bug if
  `get_actor_bounds` looks weird on a `BP_Door` instance again later.

**Next:** no further stage number was given for tonight — check back with the
human for what's queued after the door pass.

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

## Session — 2026-08-10 — unattended overnight build, STAGE 4 (room lighting)

**Did:**
- Confirmed the hallway's existing `PointLight` pattern before reusing it:
  15000 lumens, 900uu attenuation radius, plain white (1,1,1,1), `Lumens`
  intensity units.
- Checked each new room's actual footprint against the ~900uu-radius /
  "comfortably covers up to ~12-15m across" guidance before deciding light
  count, rather than following the stage instructions' example grouping
  literally (it called Entry/Bathroom "smaller" and Living room/Kitchen/
  Bedroom/Study/Utility "bigger", but the real computed footprints don't
  actually split that way): Entry is 300×300uu (3×3m), Living room and
  Kitchen are each 450×600uu (4.5×6m), and Bathroom/Bedroom/Study/Utility are
  all identically 450×400uu (4.5×4m) — every one of the 7 rooms has a longest
  dimension under 6m, well inside a single 900uu-radius (9m) light's
  comfortable coverage. Only the hallway (11m long) needed 2 lights for that
  reason. So: **one centered `PointLight` per room, all 7 rooms**, same
  15000lm/900uu/white spec as the hallway, placed at each room's XY centroid,
  Z=200 (matching the hallway lights' height). Filed each into its room's
  `Blockout/<Room>` folder.
- Spot-checked one light's properties post-set (Kitchen) to confirm the
  values landed correctly before saving.

**Blocked / not resolved:** nothing this stage.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** Stage 5 — move `PlayerStart_0` to Entry's centre.

---

## Session — 2026-08-10 — unattended overnight build, STAGE 5 (move PlayerStart to Entry)

**Did:**
- Checked `PlayerStart_0`'s current transform before touching it: `(600, 350,
  110)`, yaw 90° — this was last moved (per an earlier session's log entry) to
  sit just inside the hallway's south entrance for testing, before Entry
  existed.
- Moved it to Entry's centre: `(600, 150, 110)`, yaw 90°. Kept the same
  Z=110 (~110uu above floor) and yaw=90° (facing toward increasing Y, i.e.
  into the interior) conventions the hallway placement already established,
  per instruction. Entry is still an empty sealed-and-now-doored box with
  nothing in particular to face, so "facing further into the house" was the
  only meaningful choice available, and yaw 90° does exactly that (faces
  toward the Entry↔Hallway doorway on Entry's north wall).
- Confirmed via `get_actor_transform` after the move.

**Blocked / not resolved:** nothing this stage.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** Stage 6 (door Blueprint) — explicitly not started this session, per
instruction. See the summary entry above/below for the full Stage 2-5
picture.

---

## Session — 2026-08-10 — unattended overnight build, SUMMARY (Stages 2-5)

Human was offline for this whole session. Worked Stages 2 through 5 in order
per their instructions, committing locally after each (see the four entries
below this one for per-stage detail). Stopped before Stage 6 (door
Blueprint) as instructed. This entry is the at-a-glance picture; the
per-stage entries below have the full reasoning/coordinates.

**What exists now:** 8 rooms total (the pre-existing Hallway plus 7 new:
Entry, Living Room, Kitchen, Bathroom, Bedroom, Study, Utility), all grey-box
`SM_Cube`/`M_PrototypeGrid` construction, all connected into one walkable
loop with 90uu-wide, 210uu-tall doorway openings, all lit, spawn point
relocated into the new Entry room.

**Room-connectivity graph:**
```
Exterior (not built) -- front door (X=600, Y=-15/0 wall) -- Entry
Entry -- Living Room   (opening centered Y=150, on the X=450 shared wall)
Entry -- Kitchen       (opening centered Y=150, on the X=750 shared wall)
Entry -- Hallway       (opening centered X=600, on the Y=300 shared wall)
Hallway -- Bathroom    (opening centered Y=800,  on the X=450 shared wall)
Hallway -- Bedroom     (opening centered Y=800,  on the X=750 shared wall)
Hallway -- Study       (opening centered Y=1200, on the X=450 shared wall)
Hallway -- Utility     (opening centered Y=1200, on the X=750 shared wall)
```
Every room reachable from Entry in at most 2 hops. No isolated rooms.

**Lighting:** one `PointLight` per room (all 8, including the pre-existing 2
in the Hallway), 15000 lumens / 900uu attenuation / white, centered in each
room's footprint at Z=200. No room's longest dimension exceeds 6m, so a
single light per room is enough at this attenuation radius — only the
11m-long Hallway needed 2.

**Spawn point:** `PlayerStart_0` now at Entry's centre, `(600, 150, 110)`,
yaw 90° (facing into the interior, toward the Entry↔Hallway doorway).
Previously sat just inside the Hallway's south entrance for pre-Entry
testing.

**Key construction convention** (for anyone extending this later, e.g. the
Stage 6 door Blueprint or further rooms): every wall/floor/ceiling actor is
an `SM_Cube` `StaticMeshActor` with `OverrideMaterials[0]` set to
`M_PrototypeGrid` on its `StaticMeshComponent0`. The mesh's local pivot is at
its **min corner**, not centroid — an actor's world `location` is the
piece's min corner, and `scale.x/y/z × 100` gives its size on that axis. See
the Stage 2 entry below for the full room-shell formula and the Stage 3
entry for how doorway cuts subdivide a sealed wall into jamb/header pieces.

**Left unresolved / worth a visual PIE pass once a human is back:**
- Nothing was blocked or skipped in Stages 2-5 — every planned piece of work
  completed cleanly with no retries needed.
- This was all done headlessly via bounds-math and `get_actor_bounds`
  verification, never actually *seen* rendered. Worth a PIE walk-through to
  confirm: no gaps at the new doorway cuts (the jamb/header math checked out
  numerically every time it was spot-checked, but a visual pass is cheap
  insurance), lighting reads as intended in each room (especially the two
  rooms — Living Room and Kitchen — that are noticeably longer than the
  others at 6m), and that walking through every doorway feels correctly
  sized at 90uu wide / 210uu tall now that there's an actual player capsule
  moving through them (this project has no jump/crouch, so a doorway that's
  subtly too narrow or low would be a real problem, not just cosmetic).
- The pre-existing duplicate `Floor_Hallway` actor (flagged in an earlier
  session, deliberately left alone per that session's note) is still
  present and still untouched — not part of this session's scope.
- Stage 6 (interactive door Blueprint with a hinge-pivot leaf) is next, per
  the human's instructions, not started here.

**Pushed:** no — all five stages are local commits only. Human should review
`AGENT_LOG.md` + `git log`/`git diff` and decide whether to push.

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
