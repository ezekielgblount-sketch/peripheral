# Peripheral / Isolation — House & Property Environment Design Spec

From Ezekiel. Defines the house and surrounding property architecture, and — just
as importantly — **how to build toward it without discarding what already exists.**

---

## Critical implementation note — read this before touching any house geometry

A version of the house has **already been created** in Unreal Engine.

**Do not discard it, replace it, or rebuild the entire house from scratch** unless
a specific part is technically unusable. Treat the current Unreal house as the
starting foundation. The goal is to continue from what exists, preserve its
overall structure wherever possible, and expand/refine/detail it — not replace it
with a different design.

For every requirement in this spec, choose one of:

1. **KEEP** — already works, leave it.
2. **REFINE** — close, but needs more detail/better proportions/materials/lighting/
   stronger gameplay use.
3. **EXPAND** — keep it, but add connected space, props, interaction points,
   sightlines, or environmental detail.
4. **ADD** — doesn't exist yet, needs building.
5. **RELOCATE ONLY IF NECESSARY** — move something only if its current location
   actively prevents important gameplay (the Day 3 breaker/window sightline,
   hiding routes, basement access, central hallway flow).

The existing house should remain recognizable after this work. Do not make major
architectural changes just because another layout might look better.

**Priority order:** (1) preserve existing house work, (2) preserve existing room
layout where workable, (3) preserve any existing art already matching the
five-color matte direction, (4) improve missing detail, (5) add required gameplay
functionality, (6) adjust layout only when necessary for story/gameplay, (7) avoid
unnecessary rebuilding.

**Workflow before editing:** inspect the current level, identify existing rooms/
doors/windows/stairs/porch/basement/attic access/exterior walls/property geometry,
identify which existing assets are reusable, identify which areas already match
this spec, **produce a short KEEP/REFINE/EXPAND/ADD checklist** — then make
incremental changes. Extend existing walls instead of rebuilding rooms where
possible. Reuse existing doors/windows. Preserve current navigation, Blueprint
references, and collision/interaction logic unless a change is actually necessary.
If major geometry changes are unavoidable, update connected Blueprints, triggers,
collision, navigation, lighting, audio zones, interactables, and save-state
references accordingly.

---

## Purpose

The house must feel like a believable, ordinary mid-century family home (built
~1950s–60s) — not a gothic haunted house, not an abandoned mansion, nothing
obviously supernatural. Horror comes from isolation, familiarity becoming
uncertain, long sightlines, peripheral misidentification, small environmental
change, sound, darkness, and the player never feeling fully secure.

Player arc: *"This is a normal old family house"* → gradually → *"Something about
this house is wrong."*

The structure must support the core mechanics directly: eye tracking, peripheral
blur/information loss, ambiguous silhouettes, long interior sightlines, hidden/
partially-hidden doorways, sound from unseen areas, hiding spaces, memory
collectibles, power-loss events, basement/attic exploration, and the Day 3 window
sighting + running sequence.

---

## 1. Overall house style

Modest American single-family home, late 1950s/early 1960s. One main floor, small
attic above, full or partial basement below. Modest, not luxurious, not stylized
as haunted — slightly outdated but livable, aged but not ruined.

Construction: mix of natural stone and wood, stone lower sections/foundation, wood
siding/trim, wood-framed windows, simple pitched roof, basic gutters, small
covered/partially-covered front porch. Functional, not decorative.

Use small cracks, slightly worn paint, scuffed trim, aging wood, old hardware,
settled foundation details. **Avoid** giant holes, broken walls, overgrown-ruin
imagery, gothic arches, elaborate Victorian detail, horror-movie cobweb overload.

## 2. Exterior shape and massing

Broad, low-profile rectangular main body, slightly asymmetrical additions, low-to-
medium pitched roof, optional chimney, porch centered or slightly offset at front.
**Driveway runs along the LEFT side of the house toward the rear.**

Large enough to feel navigable and layered, compact enough that the player learns
the layout — important, because later small layout changes should read as
unsettling precisely because the player thought they knew this house.

## 3. Front of house

Porch: a few steps, simple railing/posts, wooden/partially-wooden front door, a
front door window or nearby window, one or two front-facing windows, modest
landscaping (ferns, ivy, simple shrubs, old flower pots — not dramatic or
overgrown). Old chair or small bench, ceramic/metal plant pots, faded mat, porch
light, worn but maintained wood. **The porch is a later candidate for one of
Jack's temporary calming spaces.** Normal by day; feels exposed to the woods at
night.

## 4. Driveway and property access

Gravel driveway, left side of the house, continuing to the rear yard/service area.
Gravel/dirt surface, small weeds at edges, tire impressions, uneven but realistic.
**Gravel matters for sound design** — footsteps on it should be distinct,
directional, usable during the Day 3 chase to sell the entity moving around the
exterior.

## 5. Road and isolation

Gravel road/drive connecting to a larger main road, at a distance — not directly
on a busy street. Partially hidden by woods, no close neighbors clearly visible,
rarely-heard traffic. Civilization exists, but at night it should feel far away.

## 6. Woods and surrounding environment

Tall mature trees, thin trunks, sparse undergrowth near the house, denser woods
farther out, fallen leaves, dirt, uneven ground. Normal rural American woodland,
not a fantasy forest. By day: readable tree shapes, natural light, quiet. At
sunset: trunks become dark vertical shapes, depth harder to judge. At night: trees
should create ambiguous humanoid silhouettes, branches read as limbs. **No obvious
creatures placed in the woods** — the question should always be "was that a
person, a tree, or nothing?"

## 7. Back of house

Back door, rear window, exterior breaker panel, gravel/dirt path, small service
area, view into the house, limited outdoor light, nearby trees. **Breaker panel
mounted on the exterior wall near the rear of the house** — must be walkable-to,
openable, togglable off/on, and from it the player must be able to look up and see
into the house through the rear window.

## 8. Critical Day 3 window sightline

**The architecture must support one specific long sightline.** From the rear of
the house near the breaker panel, looking through: a rear window → through the
middle of the house → through a connected hallway/room → toward a front-side
window/front-door window area. A visual tunnel through the structure, seeing
window frame, interior hallway/room, doorframe, furniture silhouettes, another
window/opening. The humanoid figure (Day 3, Act 14) appears within this sightline
— not centered, partially hidden, offset, framed by architecture, seen through
several layers. **One of the most important compositions in the entire game.**

## 9–10. Main interior layout, central hallway

Main floor organized around a hallway running roughly front-to-back through the
center — one of the most important architectural features. Runs front-to-back or
nearly so, connects major rooms, provides long sightlines, multiple doorways,
lets sound travel, supports peripheral silhouettes. Straight, intimate but not
cramped, rooms branching left/right, stair access along or near it.

Should become visually iconic: wooden/worn flooring, simple baseboards, old framed
photos, one or two dim wall lights, long rectangular proportions. Should
repeatedly create false humanoid shapes — a hanging coat, a floor lamp, a
half-open door, a chair, boxes, curtains, a stair shadow.

## 11. Stair system

Two directions: **up** to the attic, **down** to the basement — near each other or
both off the central hallway. Up = memory/storage, down = utility/physical
danger/hiding. Narrow, wooden, old but stable, slightly creaky. No elaborate
staircases — practical household stairs.

## 12. Attic

Storage space, not a horror maze. Believable family attic: cardboard boxes, old
furniture, covered objects, photo albums, old clothing, holiday decorations,
family documents, memory collectibles, old recordings, possibly 1998-related
evidence. Low ceiling, sloped roofline, narrow walking area, wooden framing, boxes
as partial visual obstructions. Starts nostalgic/quiet, can turn claustrophobic
later. Storage boxes should create human-like shapes in peripheral vision — no
monster encounter needed.

## 13. Basement

Major utility/tension space: water heater, pipes, storage, shelving, boxes,
utility equipment, electrical/mechanical sounds, concrete/rough-finished walls.
Colder and less comfortable than the main floor. Materials: concrete, rough wood,
dull metal, old cardboard, utility piping. Sparse lighting — single bulb or
limited fixtures, deep shadow between shelves.

**Contains the Day 3 hiding location**: behind several stacked boxes, enough space
to crouch, narrow gaps between boxes, restricted field of view, can hear the house
above. Likely the most psychologically intense of the three hiding options.

## 14. Bedroom

Jack's primary bedroom: bed, nightstand, lamp, dresser, desk, closet, window,
drawers, personal belongings. Should slowly connect to Jack's childhood — a
childhood photograph found under/near the desk. Multiple ambiguous silhouettes:
nightstand+lamp reading as a crouching person, hanging clothes as a standing
figure, an open closet as a dark human-shaped void, the bed corner as a hunched
shape. **Bed must support both sleeping and the Day 3 under-bed hiding spot.**

## 15. Bathroom

Shower/tub combo, sink, mirror, toilet, small storage, towels, basic fixtures.
Older mid-century bathroom, only slightly updated — small tiles, faded beige
surfaces, old metal fixtures, simple curtain, small cabinet. **Must support**: the
shower routine, the hot-water event, Day 3 shower-hiding, and a reality-distortion
event where the bathroom may not connect to the same place after a shower. Curtain
or shower door should heavily restrict visibility for the hiding beat.

## 16. Spare room

One room, partially filled with boxes, feels unused: cardboard boxes, old
furniture, folded blankets, storage bins, family belongings, possibly memory
collectibles. Boxes create human-shaped stacks/strange shadows/unclear
silhouettes. Can support random events.

## 17. Living room

Emotional center of the old family house: couch, chair, coffee table, floor lamp,
family photographs, old television, bookshelf, small cabinet, curtains, rug.
Lived-in but dated. Furniture should create silhouettes misreadable in peripheral
vision — **the floor lamp especially, since it can resemble a standing person.**

## 18. Kitchen

Practical, slightly dated: refrigerator, sink, stove, cabinets, counter, small
table, chairs, pantry/storage. Used for snacks, milk, night routines, and Day 3's
knife pickup. **The kitchen knife is a psychological safety item, not a combat
weapon** (see `DAY3_FINAL_ACT_SPEC.md` Act 3).

## 19. Garage / tool area

If included: tools, wrench, shelving, boxes, old cans, workbench, basic household
repair equipment. **The wrench for the hot-water repair event comes from here.**
Keep simple and believable.

## 20. Front-to-back visual flow

The player should be able to tell where front and back are at almost all times —
supports the Day 3 sighting, footstep direction, window views, chase tension, and
spatial memory. Learned pattern: front door → central hallway → rear area/back
door. This simplicity matters *because* later small changes become noticeable
against it.

## 21. Art direction — five-color rule (confirmed, final)

**Use only:**

| Name | Hex |
|---|---|
| Void Charcoal | `#0B0A08` |
| Soot Brown | `#211E1A` |
| Dust Taupe | `#49433D` |
| Dead Beige | `#776F65` |
| Faded Bone | `#C8C1B6` |

**Do not introduce**: bright red, blue moonlight, green horror lighting, orange
cinematic lighting, purple shadows, or any saturated color — **no exception listed
for the flashlight or anything else.** This is the second time this exact palette
has been specified (see `VISUAL_REFERENCE.md`) with no exception either time —
treat the earlier flashlight warm-color exception (`#FFE6B8`) as retired, not
merely unconfirmed. The game should feel almost like a faded memory.

## 22. Material style

Flat, matte, dry, simplified, deliberately non-photorealistic. Zero gloss,
specular highlights, bloom, lens flare, PBR shine, polished surfaces, wet
reflections. Wood: broad simplified grain, matte, slightly worn. Stone: large
simple shapes, minimal texture. Metal: flat dull shapes, no shine. Glass: dark
flat planes, minimal reflection. Mirrors: stylized flat reflections, no glare.
Fabric: matte, broad folds only.

## 23. Lighting

Moody, dark, still believable for a normal home. Practical sources only: table
lamps, hall lights, porch light, bathroom light, kitchen light, flashlight, window
light. Most scenes: one main light source, large areas of darkness, low contrast
outside the player's focus. Brightest values occupy only a small part of the
frame. No cinematic bloom, no lens flare, no visible light shafts unless very
flat/stylized.

## 24. Peripheral vision support

Place ambiguous shapes near door edges, hallway corners, windows, lamps,
furniture, hanging clothes, curtains, plants, box stacks. Player should
repeatedly think "was that a person?" then look and realize "just furniture."
Peripheral vision shows silhouette/motion/general shape; direct focus reveals the
normal object. **Reduce detail and readability away from gaze — do not rely on
huge Gaussian blur** (consistent with `CLAUDE.md`'s existing detail-reduction
approach, not a new instruction).

## 25. Sound design support

Architecture should support directional sound: wooden floors, gravel outside, old
pipes, doors, stairs, basement, attic, hallway. Sound can originate from above,
below, behind, outside, across the house — footstep upstairs, pipe knock in
basement, gravel crunch outside, floorboard in hallway, drawer sound in spare
room, door latch near the front. The player should rarely be certain exactly
where a sound came from.

## 26. Random event support

Enough interactable/state-changeable objects to support random events: doors
opening, chairs moving, photos changing position, curtains moving, lights
switching, objects disappearing, drawers opening, sound events, phone ringing,
answering machine activating, water heater issue, breaker event. Not every event
should read as supernatural — many should stay ambiguous.

## 27. Memory collectible locations

Under desk, inside dresser, behind family photo, attic boxes, basement shelf,
spare room storage, kitchen drawer, bedroom closet, old cabinet, under bed, inside
photo albums, near answering machine, garage shelf. Collectible types: childhood
photographs, old VHS tapes, voice recordings, letters, documents, newspaper
clippings, family records, identity clues, 1998-related evidence.

## 28. Safe vs. unsafe spaces

Initially safer: bedroom, porch, living room, bathroom, locked house. More
uncomfortable: basement, attic, long hallway, back yard at night, woods, dark
spare room. Over time, perceived safety should shift — a once-safe room may later
feel threatening.

## 29. Day 3 chase geography

Layout must support the full sequence end to end: wake in wrong room → dark house
→ find flashlight → determine breaker needs checking → go outside → walk to rear
→ breaker box → power returns → look through rear window → see through house
toward front → figure visible → figure exits rapidly → footsteps begin outside →
footsteps get louder → run to back door → enter → lock door → intruder enters
another way → player chooses a hiding place. **All three hiding routes (bedroom→
under bed, bathroom→shower, basement→behind boxes) must be reachable under
pressure from wherever the chase ends.**

## 30. House personality

The house should almost feel like a character, without being literally animated —
personality from memory, silence, architecture, small inconsistencies, sound,
object placement, darkness, familiar rooms changing slightly. Target feeling: "the
house knows me better than I know myself" — but the game should never explicitly
confirm the house is alive.

## 31. Final design test

For every room/exterior space: could this be a normal 1950s/60s family home? (must
be yes) — does it look obviously haunted before anything happens? (must be no,
simplify if so) — does it contain ordinary objects that could misread as
frightening in peripheral vision? (should be yes) — does it support long
sightlines, sound, memory, uncertainty? (should be yes) — does it use the
five-color matte palette with zero gloss/specular/bloom/lens flare? (must be yes).

---

## Final environment goal

Ordinary enough to be someone's real childhood home, isolated enough that every
small sound matters. The player should learn the layout completely — front door,
hallway, bathroom, basement stairs, attic, where Jack sleeps — so that as the game
progresses, that familiarity becomes what's dangerous. The house doesn't need to
look monstrous. It only needs to make the player stop trusting what they remember.
