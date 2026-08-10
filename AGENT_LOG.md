# Agent Log

Running record of what Claude did in each work session, in reverse-chronological
order (newest first). Written so either human can read a session's entry, look at
the diff, and decide whether to push — without needing to have watched the stream.

Convention: Claude commits locally with a clear message. **Pushing is a separate,
human decision** — read the entry below, check `git log` / `git diff`, then push
if it looks right.

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
