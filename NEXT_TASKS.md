# Next Tasks — queued, not yet started

Read this after finishing whatever's currently in progress (check `AGENT_LOG.md`
for the most recent session to see where things stand). Work top to bottom,
same discipline as the last overnight run: commit after each numbered task,
write an `AGENT_LOG.md` entry per task, don't push, don't stop to ask for
confirmation unless something is genuinely ambiguous enough to guess wrong.

Avoid creating Blueprint enums via the asset factory — known to freeze the
editor. Plain int/byte variables instead, same pattern already used in
`BP_Anomaly`.

---

## 1. Delete leftover First Person template practice geometry

The stock template ships with ~55 demo/practice objects (`SM_Cube`,
`SM_Cylinder`, `SM_QuarterCylinder`, `SM_Ramp` instances, from the very first
actor inventory taken when MCP access was first verified) — an obstacle
course that was never part of our house design. `PlayerStart` now sits at
Entry's centre (moved there in Stage 5 of the last session) and a human
tester got physically boxed into a corner by this leftover junk — no jump
exists by design, so this is a hard blocker, not cosmetic.

Identify actors NOT under our own organizational outliner folders (our
geometry is grouped — hallway under `Blockout/Hallway`, the 7 new rooms under
whatever folder naming the last session used, the anomaly under
`Anomalies`). Delete everything else matching those stock class names.
Double-check `PlayerStart`'s surroundings specifically are clear after
deletion — walk/trace a short radius around it and confirm nothing solid is
overlapping.

---

## 2. Replace the grey placeholder material with real palette colors, add simple room-defining furniture

Every wall/floor/ceiling currently uses `M_PrototypeGrid` — the grey-box
blockout material. Replace it project-wide with **flat colors from the
existing 5-color palette**, not textures — `CLAUDE.md`/handoff spec §10 is a
hard constraint here: matte, no surface detail, no highlights, because any
texture/glint tells the player where to look and undercuts the entire
mechanic. Use `M_FlatCol` instances (already fixed for specular=0,
roughness=1, metallic=0 in an earlier session) in these colors:

| Surface | Color | Hex |
|---|---|---|
| Walls | Light | `#B3A78F` |
| Floors | Dark | `#4E4B44` |
| Ceilings | Pale | `#E6DFCC` |

Apply consistently across every room, not per-room variation — the palette is
deliberately uniform, distinctness comes from furniture, not wall color.

**Furniture** — simple primitive shapes (boxes/cylinders combined, same
approach as the existing hallway/anomaly geometry, no imported assets), one
or two per room, enough to make each room read as what it is:

- Bedroom: bed (a low wide box + a slightly raised box for the mattress),
  dresser (a box)
- Bathroom: toilet (box + cylinder), sink (box + basin shape)
- Kitchen: counter (box along a wall), table + a couple chairs (boxes)
- Living room: sofa (box), coffee table (low box)
- Study: desk (box), bookshelf (tall thin box)
- Utility: shelving unit (box)
- Entry: skip, or a small table — it's a pass-through space

**Important — don't collide with future anomaly work.** Several of these
rooms have specific objects reserved for anomalies later (handoff spec §3):
the living room's floor lamp and wall portrait, the kitchen chair, the
bathroom mirror, the bedroom window. If a natural furniture placement would
be one of those specific objects, place a plain placeholder version with no
special logic — it gets upgraded into a real anomaly actor in a later
session, don't build anomaly behavior into it now.

Use the same `M_FlatCol` palette on furniture too (Mid `#7C7870` works well
for furniture pieces — metal/chairs/mid-tone surfaces per spec §10).

---

## 3. Verify door interaction end-to-end, add a basic toggleable flashlight

**Door check first, not a rebuild.** Stage 6 (already committed —
`b032664`, `BP_Door`) should already give E-to-interact door opening with a
hinge swing and an on-screen prompt. Before building anything new here,
actually verify it works: walk up to a placed `BP_Door` instance in PIE
(or via whatever headless verification MCP allows), confirm E toggles it
open/closed and the prompt text updates. If it's already working, note that
in `AGENT_LOG.md` and move on — don't rebuild something that isn't broken.
If it's NOT working, that's a real bug, fix it before continuing.

**Flashlight — new, keep it simple.** A basic toggleable flashlight, not
the full Act 2 spec from `PERIPHERAL_UNREAL_HANDOFF.md` §7 (that has a
precise dual-cone hot/fill setup and a specific warm hex color — worth doing
properly later, not tonight). Tonight's version: a single `SpotLight`
component attached to the camera, reasonable default cone/intensity/range
for a first-person flashlight, toggled on/off with **F** (E is interact, F9
is anomaly debug-arm, F is free). Doesn't need to be off by default or tied
to any game state yet — just something the player can click on and see
work.

---

## 4. Build the actual peripheral-vision post-process pass — build it OFF by default

This hasn't been built at all yet — everything so far is movement, rooms,
and one anomaly's logic. This is the single most recognizable piece of the
whole game (the "eerie edges" effect from the web prototype) and it's
currently completely absent. `PPV_Global` already exists and is already
`Unbound` with UE's default junk (bloom/lens flare/etc.) zeroed — build on
top of that volume, don't create a second one.

**Build it toggle-able, OFF by default — this is a change from earlier.**
The first playable beta needs to be bright and clearly reviewable (map
review, not atmosphere), and this effect deliberately degrades detail
toward screen edges by design — the two goals directly conflict. Bind it
to a debug key (**F11** — E/F9/F/F10 are all taken) that enables/disables
the post-process material's effect at runtime. Default state on session
start: **off**.

Read `CLAUDE.md`'s "Peripheral vision technique" section first — full spec
of what's changed from the original handoff doc. Key points to implement:

- **Detail-reduction, not blur** — reduce contrast and saturation toward
  screen edges rather than a literal box/gaussian blur. A practical first
  pass: modest blur + reduced contrast + reduced saturation together reads
  close enough to "can't resolve detail" without needing a true edge-
  preserving custom shader — acceptable as v1, can be refined later.
- **Radial falloff from screen centre** — use `ViewportUV`/screen position
  in a Post Process Material, distance from centre (aspect-corrected) drives
  a 0–1 "degradation amount" parameter.
- **Nothing ever reaches full clarity, even dead centre.** This is the part
  that's easy to get wrong by copying the original handoff spec's algorithm
  verbatim — that version goes to 0% degradation at centre. **Clamp the
  degradation parameter so it never drops below roughly 30–40% even at
  r=0** (i.e., centre clarity caps around 60–70%, never 100%).
- No specular/highlight interaction needed here — this is a fullscreen pass,
  separate from the material-level specular fix already done.

Verify by hand once built (this one genuinely needs eyes on it, unlike the
anomaly logic) — but don't block the rest of this file on that, note it as
needing a visual check in `AGENT_LOG.md` and move on to task 3.

---

## 5. Day/night lighting toggle (debug tool, not final Act 1/2 systems)

A simple debug keybind — **F10** — that swaps between two lighting
presets for testing/preview purposes only. Not the full Act 2 system (no
breaker box, no power-restore sequence — bigger separate features, out of
scope here). **Day is the default on session start and should stay bright
— the first playable beta is explicitly meant to be reviewed in daylight,
not the dark mode.** Night is opt-in only, never the default.

- **Day preset** (current default): existing lighting as-is.
- **Night preset**: drop `DirectionalLight` intensity near zero, drop
  `SkyLight` intensity, dim or disable the room `PointLight`s added in
  Stage 4. Toggling F10 flips between the two instantly (no fade needed,
  this is a debug tool, not a gameplay moment).

Keep it dumb and simple — a bool + two hardcoded intensity sets. This is for
previewing what dark will look like, not the real implementation.

---

## 6. Simple exterior environment — human tester walked outside the house and fell out of the world

Real bug found in testing tonight, not hypothetical: nothing exists outside
the house's walls, so a player who exits through the front-door opening (cut
in Stage 3, Entry's south wall, centered X=600 Y=0) just falls forever. This
needs at minimum a ground plane and a boundary so the world is walkable and
enclosed — a full yard build isn't required tonight, just "you can step
outside, walk around, come back in" without falling through the world.

`PERIPHERAL_UNREAL_HANDOFF.md` §6 already specs a yard, in metres: fenced
perimeter roughly x −5 to 17, z −9 to 17 (**Unreal X −500 to 1700, Y −900 to
1700** per `CLAUDE.md`'s axis conversion — z maps to Y, not Z), fence height
1.1m (**110uu**), gap at the front for a gravel path, treeline, porch. That
level of detail (gravel path texture, individual conifer meshes, porch
structure) is NOT required tonight — grey-box only, same discipline as the
house interior:

- One large flat ground plane (a scaled `SM_Cube` or `SM_Plane`, `M_FlatCol`
  in a Dark or Mid palette tone — ground shouldn't be a wall color) spanning
  at least that fenced-perimeter footprint, Z=0 aligned with the house
  floor so there's no seam/step at the front door threshold.
- A simple boundary at roughly that perimeter so the player can't walk (or
  fall) off the edge of the world — doesn't need to be a literal fence prop,
  an invisible or simple blocking volume at the perimeter is fine for
  tonight, though a plain `SM_Cube` "fence" strip at 110uu height in the
  palette's Dark tone (matching the spec's fence) is barely more work and
  reads better if there's time.
- Leave a gap in the boundary roughly where the gravel path/porch would be
  (spec says "at the front," i.e. south of the front door opening, centered
  around X=600) — doesn't need an actual path or porch built, just don't
  wall off the one side that's supposed to eventually have one.
- Basic outdoor lighting already mostly exists (the level's `DirectionalLight`/
  `SkyLight`/`SkyAtmosphere` cover this) — just confirm the new ground plane
  and boundary actually receive light and aren't sitting in unexpected
  shadow/black.

File everything under a new outliner folder `Blockout/Yard`. This is
explicitly a "don't fall out of the world" fix plus bare walkability, not
the real yard (treeline, gravel path, porch, breaker box) — that's future
work per the handoff spec, don't over-build it tonight.
