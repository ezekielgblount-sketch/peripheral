# Peripheral / Isolation — Master Visual Environment & House Design Brief

From Ezekiel (via Fable brainstorm). **This is the resolving document for the
visual-direction discussion tonight** — supersedes the flat-5-color rule that
was in `CLAUDE.md`, `VISUAL_REFERENCE.md`, and `HOUSE_ENVIRONMENT_SPEC.md`.
Those docs' room layout, gameplay-support, and Day 3 requirements still stand —
only the material/color/rendering direction changes here.

---

## Purpose

Explains exactly how the house, rooms, property, visual presentation, lighting,
atmosphere, and gameplay-supporting environment should be designed in Unreal
Engine. Direct implementation guide.

**A version of the house already exists — do not throw it away or rebuild from
scratch.** Treat it as the base. Expand, refine, add detail and atmosphere,
bring it closer to this vision incrementally.

Workflow (same as `HOUSE_ENVIRONMENT_SPEC.md`): inspect the current house →
compare to this brief → classify each element **KEEP / REFINE / EXPAND / ADD /
RELOCATE ONLY IF ABSOLUTELY NECESSARY** → modify incrementally, not a rebuild.

---

## 1. Primary design goal

The house: a real family home, built ~1950s–60s, ordinary on first impression,
quiet, slightly old, slightly neglected, rural/isolated, familiar, lived in
long ago, still structurally believable and usable.

The game: creepy, realistic, slow-burn, intimate, claustrophobic at times,
isolated, uncertain, eerie rather than constantly aggressive.

Player arc: *"This is a normal old house"* → *"This house feels wrong"* →
*"I do not trust this space anymore."*

## 2. Style direction update (the resolving section)

Previous discussions leaned flat/matte/simplified. **That's superseded.**

**Target visual style:** semi-photorealistic to photorealistic Unreal
environment. Realistic room proportions, props, surface wear, lighting
behavior. Slight grain/noise in final presentation. Should look "captured"
rather than heavily stylized.

**Still preserved — this is what keeps the mechanic intact:**
- Muted colors, limited palette feel, moody darkness
- No flashy horror color grading
- No exaggerated fantasy rendering
- **No over-stylized bloom or lens flare**
- **No glossy "video game showroom" look**

Real first, horror second. Not cartoonish, not painterly, not abstract —
"a believable Unreal Engine horror environment with controlled realism."

## 3. Using reference photos

Treat uploaded references as direct visual guidance per space, not literal
one-to-one copies — use them as visual *language* for the final level.

- **Basement ref** → openness, rough foundation, utility-space realism,
  concrete floor, brick/stone mood, sparse clutter, hiding-space tone.
- **Attic ref** → low roofline, exposed wood beams, dark empty storage,
  low visibility, old timber, claustrophobic shape, limited walkable area.
- **Living room ref** → 1960s character, wood paneling, curtained window,
  old CRT glow, carpet tone, "someone used to live here" quiet.
- **Bathroom ref** → small realistic scale, simple tile, tub/shower combo,
  harsh-but-dim practical light, tightness.
- **Hallway ref** → long/straight/narrow-but-believable, repeating doors,
  strong perspective, low light, eerie even empty.
- **Flashlight hallway/basement ref** → how the beam reveals space, how
  darkness swallows the edges, near-geometry brightens first, deep areas
  stay uncertain.
- **Exterior ref** → age range, mid-century realism, porch/window proportion,
  residential believability.

## 4–5. Keep/expand workflow, house age & structure

(See `HOUSE_ENVIRONMENT_SPEC.md` — unchanged: stone+wood mid-century
construction, functional non-luxury layout, not a mansion/gothic/fantasy
house, old enough to carry history, small enough to memorize.)

## 6–9. Exterior, porch, driveway, woods

(Unchanged from `HOUSE_ENVIRONMENT_SPEC.md` §2–6 — driveway on the left
toward the rear, gravel road, isolated in woods, modest porch as a temporary
relief zone by day/exposed by night.) Exterior finish: stone base gray-beige
or weathered red-brown, faded upper siding, simple trim, realistic
residential windows and roof. Maintained enough to still be used — not
abandoned, not pristine.

## 10. General interior plan

Hallway down the middle, stairwell up to the attic, stairs down to the
basement, bedroom, bathroom (shower/tub/sink), spare room with boxes,
basement with water heater, attic with storage — plus the rear-window-through-
house-to-front sightline. **Uses "attic," not "second floor"** — worth
confirming this is the final read, since it differs from a later verbal note
about wanting an actual second floor. Recommend treating this doc's "attic"
as authoritative unless told otherwise.

Player must be able to learn the layout easily — familiarity is what makes
the later horror land.

## 11. Central hallway

One of the most important spaces. Long, straight, narrow-but-believable,
repeating doorways, strong perspective, slightly dim, quiet, eerie even
empty. Multiple branching doorways, simple worn baseboards, old paint/
wallpaper, low practical lighting, floor that carries footstep sound, enough
length for real darkness at one end.

## 12. Living room

Strongly follows the reference: 1960s family-room feeling, wood-paneled
walls, large curtained window, old CRT TV, plush/textured dated carpet,
armchair, sofa. Homey but old, still but not dead. **The TV matters** — soft
ambient light source, can carry static/distortion/unease. Heavy slightly-old
curtain fabric, thick dated textured carpet, worn period-appropriate
furniture, not cluttered — negative space is useful for tension.

## 13. Kitchen

Believable, slightly dated, practical. Supports milk/snacks, Day 3 knife
pickup, domestic normalcy turning uneasy. Fridge, sink, counters, cabinets,
small eating area, older appliances, a knife drawer, mild wear, quiet
nighttime mood. Realistic scale, not oversized or overstylized.

## 14. Bedroom

Jack's intimate space. Supports sleeping, waking-in-wrong-room, under-bed
hiding, childhood memory evidence. Bed, nightstand, lamp, dresser, desk,
window, closet/wardrobe, drawers, personal belongings, signs of both
temporary occupancy and older family history. **Childhood photo found under
the desk.** Nightstand+lamp should read as an ambiguous silhouette; hanging
clothes/closet darkness should read as threatening in peripheral vision. Safe
at first, uneasy later.

## 15. Bathroom

Strongly follows the reference: small, tight, realistic, functional,
slightly old, clean enough to use but not modern. Tile walls, tub/shower
combo, sink, toilet, mirror, harsh practical light. Ordinary, vulnerable,
sound echoes, too small to feel safe once tension rises. Supports the shower
routine, hot-water event, the reality-distortion event, and Day 3 shower-
hiding. Lighting harsher/whiter than other rooms but still dim and believable.

## 16. Spare room

Partially filled with boxes/stored belongings — supports the "long-lived
family house" story, silhouette ambiguity, storage atmosphere, possible
collectibles, the sense of a buried past. Quiet, underused, slightly dusty —
not overfilled to chaos.

## 17. Attic

Closely matches the reference: exposed wood framing, dark timber beams,
sloped roofline, low headroom in places, storage boxes, old household
storage, partial walkway, strong darkness, claustrophobic geometry.
Believable, dry, old, quiet, oppressive, memory-laden. Boxes/framing create
false silhouettes, hidden corners, partial occlusion. **Not huge** — a real
attic, not a horror dungeon.

## 18. Basement

Strongly reflects the reference: concrete floor, brick/stone or rough
structural walls, utility-space realism, water heater, pipes, electrical/
mechanical feel, storage shelves and boxes, open space in places, darkness
swallowing the far end, cold and exposed. One of the most important mood
spaces — real, cold, slightly damp-*looking* but not wet-shiny, echoing,
unsafe. Supports the water heater/utility events, flashlight exploration, and
the Day 3 hiding spot (behind stacked boxes, restricted view out, room to
crouch, strong audio presence from the house above).

## 19. Flashlight look and behavior

Very important. Lights the immediate floor/nearby surfaces, reveals the
centre of focus clearly, lets darkness dominate the edges and distance. **Not
an overpowered floodlight, not a giant clean theatrical cone, must not erase
uncertainty.** Realistic, limited, nervous, practical, slightly noisy/grain-
enhancing on screen.

Varies believably by room while staying recognizably the same flashlight:
- **Basement/utility**: more darkness, stronger contrast, light dies off
  faster, floor/wall texture catches it first, deep corners stay unreadable.
- **Hallway**: reveals the central path, doors/trim catch the beam, the
  distant end stays uncertain — the beam itself can suggest something
  standing farther down.
- **Bathroom**: harder bounce off tile/pale surfaces, slightly brighter
  reaction, mirror must NOT create huge glare, white surfaces catch more
  light without making the room feel safe.
- **Living room**: picks out furniture silhouettes, fabric/carpet absorb
  light more softly, the TV/dark window stay psychologically important
  anchors.

(Supersedes `NEXT_TASKS.md` task 8's rigid `#C8C1B6` color lock — flashlight
color should come from the realistic-but-controlled palette family below, not
a single fixed hex. The battery-drain mechanic itself is unaffected.)

## 20. Room-by-room lighting behavior

All rooms feel part of the same house — no room should feel like a different
game. Living room: softest ambient, TV glow as secondary mood light, window
darkness matters, a lamp for localized warmth. Hallway: dimmer, oppressive,
long falloff, darker at the ends, minimal practicals. Bathroom: harsher
overhead/mirror light, controlled tile brightness, sterile but still eerie.
Bedroom: one lamp/low warm source, uneasy but gentle, dark corners suggest
shapes. Attic: mostly darkness, minimal ambient, flashlight-dominant. Basement:
utility/sparse practicals, often partially unlit, deep shadow pockets,
flashlight-dominant. Kitchen: practical overhead, closer to normal than other
rooms, still muted/moody at night.

## 21. Color palette — final, concrete (supersedes the "family" framing below)

The companion visual-design-brief image gives exact values — use these as the
working palette, not just a mood description:

| Name (approx.) | Hex |
|---|---|
| Deepest shadow | `#0B0A08` |
| Dark wood/aged black | `#1F1C18` |
| Mid brown | `#3A342E` |
| Warm gray-brown | `#6A6156` |
| Dirty/aged white | `#A79F90` |

Slight variation is allowed *within* each value's range — but no saturated
colors, and whites should read dirty/aged, never clean. Blacks deep but not
fully crushed.

For general mood/description when concrete numbers aren't needed: deep
charcoal/black shadows, warm gray-browns, faded wood browns, dusty beige,
aged cream, muted red-brown brick/stone where applicable, off-white bathroom
tile, aged green-gray/dead-plant tones outside.

**Avoid:** bright saturated colors, neon, blue horror clichés, green horror
clichés, red emergency saturation, overly orange horror grading. Natural,
muted, slightly aged, slightly grainy, calm but wrong.

## 22. Materials

Realistic but controlled. **Still avoid:** overly glossy surfaces, excessive
specular sparkle, "showroom" materials, plastic-perfect surfaces, highly
reflective modern finishes — this is the part that keeps the peripheral-
vision mechanic intact even at photoreal fidelity.

- **Walls**: painted plaster/drywall, slight wear, small imperfections, aged
  not destroyed.
- **Wood paneling** (living room): slightly dark, realistic grain, aged, low
  sheen.
- **Stone/brick**: slightly rough, old, structural — basement/exterior base.
- **Carpet**: thick, slightly worn, absorbs light softly, realistic vintage
  texture.
- **Tile** (bathroom): plain, believable, slightly old, clean enough to use,
  not shiny showroom tile.
- **Metal**: dull, utility-grade, aged, non-sparkly.
- **Glass**: realistic but subtle, no exaggerated glare, no lens-artifact
  overuse.

## 23. Screen presentation

Slight film-like/sensor-like grain — not excessive VHS, not a cheesy analog
filter, just enough noise to make darkness feel real. Immersive, physical,
tactile, observed, claustrophobic in darkness.

**Do NOT overdo:** chromatic aberration, bloom, motion blur, lens flare,
extreme vignette, fake found-footage gimmicks. The screen effect supports
realism, doesn't distract from it.

## 24. Peripheral vision / eye-tracking support

The environment must constantly provide shapes that can be misread: lamps,
door frames, curtains, box stacks, chairs, coats, shadows, stair rails,
furniture corners, doorframes, attic framing, basement columns. *"I saw
something"* → look directly → *"It was just the environment."*

## 25. Sound support

Architecture supports sound from above (attic), below (basement), down the
hall, another room, outside a window, on gravel, on porch boards — plus door
movement, pipe knocks, water, floorboard creaks, distant footstep ambiguity.
Should often be hard to tell exactly where a sound came from.

## 26. Day 3 final act support (condensed — full detail in `DAY3_FINAL_ACT_SPEC.md`)

Return home → door unlocked/open → search with knife, find no one → lockdown
→ night routine → sleep → wake in a different room → power out → find
flashlight → outside to the rear breaker → power cycle → rear-window
sightline toward the front → figure seen → figure exits fast → footsteps
loud → run to back entrance → inside, locked → hide (under bed / shower /
basement behind boxes) → wait in silence → come out → final scare ends the
game. The layout must make this sequence feel natural — consistent with the
full spec already on file.

## 27. Final mood

*This was once a normal family home. Now it feels like memory, absence, and
fear have settled into it.* The player should feel alone, watched, unsure,
pulled deeper in, familiar with the layout, less and less safe inside it. The
environment does the horror work — not dependent on monsters to be scary.

## 28. Final instruction

Expand the existing house, refine room by room, match the references, keep
it believable/realistic, improve atmosphere/lighting/material quality/room
distinctiveness while keeping overall unity. Not flashy, not overdesigned,
not a theme-park horror house. **A real place where something is deeply
wrong.**
