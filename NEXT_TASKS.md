# Next Tasks — queued, not yet started

Read this after finishing whatever's currently in progress (check `AGENT_LOG.md`
for the most recent session to see where things stand). Work top to bottom,
same discipline as every prior run: commit after each numbered task, write an
`AGENT_LOG.md` entry per task, don't push, don't stop to ask for confirmation
unless something's genuinely ambiguous enough to guess wrong.

Avoid creating Blueprint enums via the asset factory — known to freeze the
editor. Plain int/byte variables instead, same pattern already used in
`BP_Anomaly`.

**Everything below is new as of this session.** Tasks from earlier tonight
(template junk cleanup, old-palette materials, old furniture, old yard,
old-layout door verification) are superseded by `HOUSE_BLUEPRINT.md` — a
complete, approved, from-scratch house replacement, not an addition to what
was there. Don't try to reconcile old task numbers against this list.

---

## 1. Read and understand `HOUSE_BLUEPRINT.md` before touching anything

This is the new definitive house layout — approved by the creator, confirmed
explicitly to supersede the interior built so far tonight. Read it in full,
including the coordinate-system header: **its coordinates are already
Unreal-native (stated in its own header). Do not run them through
`CLAUDE.md`'s spec-to-Unreal axis-conversion table** — that conversion is
for the older, differently-conventioned `PERIPHERAL_UNREAL_HANDOFF.md` only,
and does not apply here. Build `HOUSE_BLUEPRINT.md`'s X/Y/Z exactly as
numbered.

## 2. Before clearing anything — identify what's reusable vs. what gets discarded

**Reusable (do not delete, these are classes/systems, not placements):**
`BP_Door` (the Blueprint class itself), `BP_Anomaly` (base class),
`FoveaComponent`, `BP_FirstPersonCharacter`, all materials. These get
*reused at new positions*, not rebuilt from scratch.

**Discarded (old-layout placements, no longer correct):** every currently-
placed wall/floor/ceiling actor from the old room layout, the old yard
(built around the old, now-wrong front door position), old furniture
placements, the old anomaly instance's specific position (the class stays,
the placement doesn't).

Produce a short list of what's being deleted vs. reused before deleting
anything, log it in `AGENT_LOG.md`.

## 3. Build the structure — Tables 1–4

Floors/slabs (Table 1), walls (Table 2), stairs (Table 4) exactly per the
coordinates given. Grey-box primitives, same approach as everything built so
far — this is a structure pass, not a materials pass. Leave door/window
openings as literal gaps in the walls per Table 3's positions (don't place
`BP_Door` instances yet, that's the next task) — but do cut the openings
correctly the first time. **Given tonight's history of "opening cut on one
side of a shared wall but not the other," verify each opening from both
adjoining rooms' sides, not just visually from one angle.**

## 4. Independently re-verify the self-check table, don't just trust it

`HOUSE_BLUEPRINT.md`'s own self-check section claims closure/overlap/
circulation/sightline all PASS. Re-derive at least the closure check (every
room's registered bounds actually enclosed by real placed walls) and the
sightline check (front-door centre to back-door centre, `(0,1215,170)` to
`(1200,1215,170)`, genuinely unobstructed) against what actually got built,
using bounds/trace tools, not by re-reading the document's own claims. If
anything doesn't match, fix the geometry, don't edit the claim.

## 5. Place doors — reuse `BP_Door`, don't rebuild it

At every opening marked `door` in Table 3 (not the `window` ones), place an
instance of the existing `BP_Door` class. Same hinge-swing-direction fix
from earlier tonight (swings away from whichever side the player opens it
from) should already be baked into the class — confirm it still holds at
the new positions, don't assume.

## 6. Re-place the anomaly

The hallway-end figure (anomaly #10) needs a new position in the new
hallway (room registry: X 180–1200, Y 1140–1290) — there's no blueprint-
specified coordinate for it since this document is architecture, not
gameplay-object placement. Pick a sensible spot near one end of the hallway,
consistent with "hallway-end figure," and log the choice and reasoning in
`AGENT_LOG.md` rather than leaving it unplaced.

## 7. Reconcile the exterior/yard

The yard built earlier tonight (fence, treeline, path, porch, garage
grey-box) was built around the *old* front door position and house
footprint — both are now wrong. The front door is now on `W02` at
approximately `(0, 1215)`, facing in the −X direction (front is at low X
per the blueprint's convention). Rework the yard's ground plane, boundary,
and front-path gap to match this new position and orientation. Full detail
(treeline density, exact porch dimensions) already exists in
`HOUSE_ENVIRONMENT_SPEC.md` §3–7 if useful, but the *position* has to match
`HOUSE_BLUEPRINT.md`, not the old assumption.

## 8. Materials and furniture — hold for now

Do NOT redo materials/furniture yet. Get the structure right and verified
first (tasks 1–7). Once that's solid, materials follow
`MASTER_VISUAL_ENVIRONMENT_BRIEF.md` (semi-photorealistic, controlled
realism, zero gloss/specular/bloom/lens-flare, the 5-value palette family as
a color anchor) — not flat single-color slabs. This will get its own task
once the structure is confirmed correct; don't start it early.

## 9. Flashlight battery drain (unaffected by any of this, safe anytime)

240 seconds on-time per charge, flicker in the last ~20%, cuts out at 0%, no
recharge yet. Color: don't lock to a single fixed hex — see
`MASTER_VISUAL_ENVIRONMENT_BRIEF.md` §19 for realistic room-by-room
flashlight behavior instead. This task has no dependency on the house
rebuild — safe to do in parallel or first if convenient.
