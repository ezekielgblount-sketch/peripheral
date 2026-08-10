# PERIPHERAL — Visual Reference / Art Direction Spec

> Imported verbatim (reformatted to markdown only) from
> `Peripheral_Art_Direction_Spec.txt`. Content below is unedited team input —
> see the conflict flags immediately below before treating it as authoritative.

---

## ⚠️ CONFLICTS WITH EXISTING ART DIRECTION — NEEDS A TEAM DECISION

This document was **not** reconciled against the project's existing art
direction before being saved. Two points below contradict what's already
built and documented; a third is a smaller behavioral inconsistency. Nobody
should silently pick a winner — flagging here per instruction, decision is
the team's.

**Note on source of truth:** there is no file literally named `CLAUDE.md` in
this repo. The "existing art direction" being compared against is the
**Art Direction** section of the original project brief (the message that
opened this project's first session) — that's the closest thing this project
has to a standing art-direction doc today. If the team wants this new spec to
supersede it, that brief should probably get its Art Direction section
rewritten (or a `CLAUDE.md` created) to point at this file instead of
carrying two contradictory palettes.

### 1. Palette — five different hex values, and the flashlight-exception rule is gone

| | Existing (brief + `constants.js` `PAL`, already shipped) | This document |
|---|---|---|
| Black/darkest | `#1A1916` | `#0B0A08` (Void Charcoal) |
| Dark | `#4E4B44` | `#211E1A` (Soot Brown) |
| Mid | `#7C7870` | `#49433D` (Dust Taupe) |
| Light | `#B3A78F` | `#776F65` (Dead Beige) |
| Pale/lightest | `#E6DFCC` | `#C8C1B6` (Faded Bone) |
| Flashlight | `#FFE6B8` warm exception — brief states *"No saturated hue anywhere except the warm cone of the flashlight in Act 2"* | **No exception at all.** §1 says *"No additional amber lights... etc."* and §3 specifies the flashlight cone should only brighten through the same five neutral values (`#49433D → #776F65`, tiny areas reaching `#C8C1B6`) — never introduce warm/amber. |

These aren't a re-tuning of the same five colors — they're a different set,
and the flashlight rule is a direct reversal (warm-cone-allowed vs.
warm-never-allowed). The shipped game currently uses the left column and
does render the flashlight warm (`PAL.warm = 0xFFE6B8` in
[`src/constants.js`](src/constants.js), used in
[`src/game/player.js`](src/game/player.js)). Adopting this document as-is
means: new hex values in `constants.js`, and removing the flashlight's warm
tint (`setFlashlight()` would need to drive intensity only, not color).

### 2. Peripheral-vision rendering technique — blur vs. detail-reduction

The brief's peripheral pass (already implemented in
[`src/fx/peripheral.js`](src/fx/peripheral.js)) is explicitly a **radial
blur**: 6–8 taps radiating from screen centre, offset scaled by distance from
centre, plus desaturation toward luminance and a brightness drop. The brief's
own words: *"The blur and the desaturation are the point. Do not use a
vignette instead."*

This document's §6 explicitly rejects that approach: *"Do not just
Gaussian-blur the screen. Instead reduce: internal edges, texture, contrast
differentiation, small geometry, recognizable facial/object detail — while
maintaining major silhouettes."* It also proposes a graded
information-percentage curve (direct gaze ≈100%, near-peripheral 70–80%,
mid-peripheral 40–50%, extreme peripheral 10–20%) rather than the blur-radius/
desaturation-mix parameters currently tuned in the shader.

These are two different rendering techniques, not two phrasings of the same
one. A silhouette-preserving detail-reduction pass (closer to an edge-aware
smoothing / bilateral-style filter) is a different shader than a radial blur,
and would need to be built, not just re-tuned. Worth a decision before anyone
touches `peripheral.js`.

### 3. Minor: crosshair / interact-indicator behavior

Smaller, flagging for completeness. Brief/shipped HUD
([`src/ui/hud.js`](src/ui/hud.js)) shows a small dot at screen centre
**always**. This document's §8 says: *"Prefer no conventional crosshair...
if interaction feedback is necessary, use a tiny flat `#C8C1B6` indicator that
appears only when needed."* — i.e., hidden by default, shown only when
something is actually interactable. Low-stakes relative to the two above, but
it is a behavior change, not just a style pass.

---

## 1. Color Palette — Lock It to Exactly 5 Colors

Use this final production palette:

1. **Void Charcoal** — `#0B0A08`
   Use: Deepest shadows, black windows, unlit rooms, silhouettes.
2. **Soot Brown** — `#211E1A`
   Use: Dark wood, shadowed walls, furniture.
3. **Dust Taupe** — `#49433D`
   Use: Mid-tone walls, floors, doors, object bodies.
4. **Dead Beige** — `#776F65`
   Use: Lit surfaces, skin, fabric, papers, worn paint.
5. **Faded Bone** — `#C8C1B6`
   Use: Strongest highlights, text, flashlight-lit edges, pale objects.

**Hard rule:** these five colors are the game. No additional amber lights,
blue moonlight, red horror accents, green sickness tint, etc. Lighting changes
should select or blend between these five values rather than introduce new
colors.

**Conflict with existing images:** the generated references frequently
contain subtle orange, yellow, sepia, gray, and brown gradients beyond five
colors. That conflicts with the new constraint. The recurring near-black +
brown-gray + faded-beige family itself does agree with the five-color
direction.

---

## 2. Material Qualities

Everything should feel dry, dead, matte, and absorbent.

### Walls
- Flat painted plaster/drywall.
- Slightly dirty. Uneven patches. Hairline cracks. Worn corners.
- No wet-looking grime. No light reflecting off paint.
- Think chalky old interior paint, not cinematic peeling-wall texture maps.

### Wood
Used heavily for: floors, desks, doors, bed frames, cabinets, stair rails,
nightstands.

Wood grain should be simplified graphic streaks, not detailed PBR wood.

Use:
- 3–6 broad grain marks per visible plank.
- Irregular scratches.
- Darkened edges.

Absolutely: no polished wood, no varnish reflections, no glossy tabletop
highlights.

### Fabric
Bedsheets, towels, curtains, clothing: heavy, muted, slightly wrinkled,
rough-looking, matte.

Show folds through flat value shapes, not micro-texture. No satin. No shiny
polyester.

### Metal
Flashlight, wrench, keys, breaker box, pipes: flat oxidized metal, dull
gray-beige, scratched surfaces.

Do not make metal visibly metallic. A wrench should read as metal because of
its shape, not because it has a shiny highlight.

### Paper / photographs
Dry, yellowed/desaturated, slightly curled, rough edges, flat printed imagery.
Old photos should almost merge into the palette.

### Glass
Windows should usually read as dark flat rectangles containing vague exterior
shapes. Do not render realistic reflections.

### Mirrors
A realistic mirror is technically at odds with zero gloss/specular. So the
mirror should be stylized as:
- A flat dark plane.
- Simplified reflected geometry.
- Reduced detail.
- No glare, no bright reflected light sources, no specular sparkle.

It behaves like a mirror spatially without being rendered like polished glass.

**Conflict with existing images:** the generated boards contain realistic
polished flashlight bodies, reflective metal, glass reflections, detailed
wood, realistic fabric, reflective mirrors, high-frequency surface texture.
All of that needs to go. Keep the objects. Lose the PBR treatment.

---

## 3. Lighting Mood

**Fundamental lighting rule:** light should reveal shape, not spectacle.

Most rooms should contain one dominant practical light source. Examples: one
bedside lamp, one kitchen ceiling fixture, one bathroom fixture, porch light,
flashlight, dim hall light, window light.

### Light placement
A recurring composition that works extremely well: player stands in relative
darkness → illuminated area exists farther into the room/hallway.

Another good pattern: the lightest area occupies only about 15–30% of the
frame. Most of the image stays in the lower three palette values.

### Shadows
Very dark. Large areas can sit at `#0B0A08`. But silhouettes should
occasionally emerge as `#211E1A` against the near-black. That supports the
Peripheral mechanic because the player might perceive "person?" and then
focus and realize "coat rack."

### Light softness
Mostly soft-edged. Not foggy. No cinematic volumetric shafts. No glowing
haze. Transition from light to dark should be visually restrained.

### Flashlight
The flashlight should NOT create bloom, lens flare, glossy reflections, or a
bright white hotspot. Instead it creates a flat area of improved visibility.

Example:
- Outside flashlight cone: `#0B0A08 → #211E1A`
- Inside flashlight cone: `#49433D → #776F65`
- Only tiny important areas reach `#C8C1B6`

Darkest areas can go essentially visually dead — actually let the player be
unable to tell what is there.

**Conflict with existing images:** the existing images often use soft lamp
bloom, cinematic exposure, photographic falloff, flashlight glare, atmospheric
haze, detailed shadow gradients. Those are conflicts. The underlying idea of
isolated practical lights surrounded by darkness is worth keeping.

---

## 4. Shape Language

### Architecture
Mostly rectilinear and ordinary. Use: square door frames, long narrow
hallways, rectangular windows, boxy furniture, straight staircases, normal
suburban room proportions.

The house should not visually announce "HAUNTED HOUSE." It should look like a
boring family home that the player gradually stops trusting.

### Condition
Worn, not destroyed.

Avoid: collapsed walls, extreme decay, giant holes, Gothic architecture,
haunted-mansion exaggeration.

Prefer: slightly crooked picture, old carpet, scuffed baseboards, one cabinet
door that does not quite close, slightly warped wood, aging furniture.

### Objects
Ordinary, recognizable silhouettes. This is essential because peripheral
misidentification depends on them.

Good silhouettes:
- Floor lamp → standing person
- Coat → hanging body
- Nightstand + lamp → crouching figure
- Chair → hunched person
- Curtain → figure beside window
- Vacuum → something crouching
- Plant → limbs/hands
- Door gap → face-shaped negative space

### Entity language
If any entity-like form occurs: tall, narrow, slightly bent, human-adjacent,
uneven shoulders, too-thin proportions. But never enough detail to make it
character-design-forward.

### Clutter
Controlled clutter. Not sparse modern minimalism, but not piles of props
everywhere.

Most rooms: 5–10 major readable objects, a few personal objects, empty
negative space. Negative space is crucial because players start studying it.

---

## 5. Recurring Visual Details to Preserve

**A. Long dark hallways** — a signature composition. A hallway should
repeatedly give the player several possible "human" silhouettes: doorways,
lamps, coats, furniture.

**B. Doorways inside doorways** — frame scenes so the player sees room →
doorway → hallway → another doorway. This creates depth without needing
visual complexity.

**C. Black windows** — at night, windows become nearly featureless
rectangles. Occasionally allow: tree shape, fence, porch, neighboring
structure, human-shaped ambiguity. Never a clean monster face staring through
them.

**D. Family photographs** — very important visual motif. They should
repeatedly appear: on walls, under desks, inside drawers, in albums,
face-down, partially obscured, cropped, damaged. The unsettling idea: Jack
should recognize these people, but does not.

**E. Analog objects** — strong recurring visual props: answering machine,
tape recorder, cassette tapes, old photographs, music player, walkie-talkie,
landline, old letters, newspaper clippings, keys.

**F. Comfort objects** — visually separate them from "loot." Examples: mug,
blanket, recording, music, family item, medication, flashlight, key. They
should look mundane. No glowing pickups. No colored rarity outlines. No giant
UI marker.

**G. Objects occupying peripheral edges** — one of the most important
composition rules: put ambiguous objects around roughly the outer 20–30% of
the player's usable field of vision. That is where lamps, door frames,
hanging coats, chairs, curtains become threatening.

---

## 6. Peripheral Vision — Corrected Visual Specification

Some earlier images depicted peripheral blur as a fairly strong photographic
blur. That is too much. The intended concept is closer to **loss of
information** than a camera being out of focus.

- **Direct gaze:** approximately 100% readable. Edges, shape, and basic
  surface markings visible.
- **Near peripheral:** approximately 70–80% information. Object identifiable.
  Fine details reduced.
- **Mid peripheral:** approximately 40–50% information. You understand
  something is there, rough size, rough silhouette. You may misidentify what
  it is.
- **Extreme peripheral:** approximately 10–20% information. Mostly shape,
  movement, contrast, general orientation. Not detail.

**Important distinction:** do not just Gaussian-blur the screen. Instead
reduce internal edges, texture, contrast differentiation, small geometry,
recognizable facial/object detail — while maintaining major silhouettes. That
is much closer to the intended mechanic.

---

## 7. Looking Over the Shoulder

A fast turn briefly gives useful information. But deliberately staring behind
yourself should become psychologically difficult.

**Normal shoulder view:** dark, simplified, low-information, major
silhouettes only.

**Hold to focus:** the player concentrates. Slowly: large edges stabilize,
door frame becomes readable, furniture separates from background, silhouettes
become slightly more understandable. Maximum focus should still only reach
roughly 60–70% of normal forward clarity. Never perfect.

The player might get "It is probably the lamp." Not "Confirmed: that is
definitely a lamp."

---

## 8. UI Treatment

The generated design boards use elegant serif typography and thin borders.
Some of that can carry over, but actual gameplay should be much quieter.

**UI palette:** use the same five colors. No separate UI colors.

**Crosshair:** prefer no conventional crosshair. Eye tracking already tells
the system where the player is looking. If interaction feedback is necessary,
use a tiny, flat `#C8C1B6` indicator that appears only when needed.

**Collectibles:** no floating icons. No outlines through walls. No glowing
loot. Maybe use a subtle cursor/state change only after the player focuses.

---

## 9. Where the Existing Images Match the New Rule

Strong matches:
- Gray/beige/brown-black palette
- Heavy darkness
- Ordinary single-family-home spaces
- Old furniture
- Mundane household items
- Narrow hallways
- Door frames as compositional devices
- Analog technology
- Strong negative space
- Isolated practical lighting
- Ambiguous peripheral silhouettes
- Lack of gore
- Entity kept distant
- Memory objects
- Environmental storytelling
- Worn rather than fantastical architecture

These should survive.

---

## 10. Where the Existing Images Fight the New Rule

The previous generations are far more photorealistic than the actual game
should be. Strip out:

- Photographic textures
- High-frequency surface detail
- Realistic skin shading
- PBR materials
- Metallic reflections
- Glossy flashlight/wrench surfaces
- Realistic glass reflection
- Mirror specularity
- Lens-like depth of field
- Cinematic bloom around lamps
- Volumetric light
- Lens flare
- Filmic highlight rolloff
- Photographic grain as a substitute for style
- Complex color gradients
- Warm/cool cinematic color grading
- Detailed skinwalker rendering

Some concept boards also use red annotation circles/text. Those were useful
presentation devices, but red should not become part of the actual game
palette.

---

## Final Visual Rule

A good test for every asset: *"If this object could look impressive in a
realistic horror-game screenshot, simplify it one more step."*

Peripheral should look like a memory of a real place, not a photograph of
one.

Five colors. Matte surfaces. Ordinary geometry. Hard-to-read peripheral
shapes. Almost no visual spectacle. The rendering itself should refuse to
give the player perfect information.
