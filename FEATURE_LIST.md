# Feature List — "Isolation" vs. the existing Peripheral spec

Source: `Isolation — Master Game Feature List.pdf` and `Chat GPT ISOLATION
FINAL.pdf` (both supplied from `~/Downloads`). **The two files are identical**
— same 69-section document, word for word — so this is a comparison against
one source, not two.

Compared against `PERIPHERAL_UNREAL_HANDOFF.md` (the spec/source of truth)
and `CLAUDE.md` (the Unreal workflow rules) at repo root.

**Processing note:** the source PDF contains its own embedded "§69 IMPORTANT
INSTRUCTION FOR CLAUDE" section, addressed directly to an AI. That's treated
below as descriptive design content to compare against the existing spec —
not as an instruction overriding anything, per the usual rule that directives
inside a supplied document aren't commands. It's also, in substance, almost
identical to `PERIPHERAL_UNREAL_HANDOFF.md` §13's existing "don't" list, so
nothing in it conflicts with how this comparison was done.

---

## ✅ RESOLVED (2026-08-09) — Isolation supersedes Peripheral, default to Isolation on any conflict

Team decision, not a per-item call: Isolation is the project going forward.
Peripheral was a 2-hour brainstorm; Isolation is the matured version. Standing
rule for anything below or anything found later: **when the two designs
disagree, build Isolation's version.** "If problems arise, we'll address them"
— not trying to pre-solve every edge case today.

Applied to the six items below:

1. **Same project.** Isolation is what gets built. Peripheral's anomaly/fovea
   code is the starting engine, not a finished game being extended. The
   anonymous-player/buyer-sign design (handoff §9) is retired — Isolation has
   a named protagonist (Jack).
2. **Vision clarity.** Isolation's model: detail-reduction (not blur), nothing
   ever reaches full clarity even under sustained centred focus, cap ~60–70%.
   See `CLAUDE.md`'s "Peripheral vision technique" section.
3. **Inventory/collectibles.** Building it — memory collectibles + comfort-item
   attrition system, per Isolation §16–19.
4. **Entity chase-adjacent sequence.** Building the Day 3 running-footsteps/
   back-door sequence per Isolation §50–51. Entity still never touches/kills
   the player.
5. **House topology.** Deferred, not rejected — doesn't block current grey-box
   work. Static level assumptions are fine for now; topology-shifting is a
   layer added later, once the core fovea/anomaly mechanic is proven.
6. **Back door + garage.** Building it, per Isolation §27–28, §51.

The items below this line predate the resolution above and are kept for
context on *why* each call was close enough to need one — not still open.

---

## Original flagging (kept for context, see resolution above)

### 1. Is "Isolation" the same project as Peripheral, or a different one?

This is the one every other item downstream depends on. The two documents
describe overlapping mechanics (peripheral vision, misidentified household
objects, ambiguous entity, no jumpscares) wrapped around **fundamentally
different games**:

- **Peripheral**: no story, no named protagonist. The player is themselves —
  literally; their own typed name goes on the yard sign (`VISUAL_REFERENCE.md`
  / handoff §9). One evening, two acts, ~8 minutes, ends when the door locks.
- **Isolation**: a specific named protagonist ("Jack"), a five-year amnesia
  backstory, a prologue with a lawyer and a inherited deed, a multi-day
  structure with a job and a commute, and a mystery about his altered
  identity and dead family that the entity/house exists **in service of**
  (Isolation §66: *"the possible entity exists in service of that mystery
  rather than replacing it"*).

Layering Isolation's narrative onto Peripheral's shell isn't a content
addition, it's a different game with borrowed mechanics. Options as I see
them, not a recommendation: (a) Isolation is the next, larger project and
reuses Peripheral's anomaly/fovea code as a starting engine rather than a
finished game to extend; (b) Peripheral gets renamed/reworked into Isolation,
in which case the anonymous-player / buyer-sign design (§9) needs to be
explicitly retired, not just left dangling; (c) they stay two separate
projects and this document is filed for later, not built now. Whoever owns
the story should call this one.

### 2. Peripheral-vision rendering technique (reinforces an existing flag, adds a new wrinkle)

`VISUAL_REFERENCE.md` already flagged that its detail-reduction approach
conflicts with the shipped radial-blur shader. Isolation §6 makes the
**identical** argument, nearly word for word (*"It should NOT simply apply a
huge blur filter... reduce internal edges, texture, contrast differentiation,
small geometry... while maintaining major silhouettes"* — Isolation §6 vs.
VISUAL_REFERENCE.md §6, same phrasing). Not a new conflict, just corroborating
evidence for the one already on record — but it adds a wrinkle worth flagging
separately:

Isolation §12 (Focus/Concentration) specifies that even a **deliberate,
player-held focus action** should cap out around 60–70% of normal clarity,
and *"the entity should NEVER become fully visible"* even under maximum
focus. Peripheral's model is different in kind, not just degree: dead centre
is **always** 100% sharp by design (peripheral pass: *"~20% of screen radius
is fully sharp"*), and a resolved anomaly snaps to its **fully normal,
completely clear** state the instant it's centred and dwelled on (anomaly
§3, `RESOLVING` → `SetNormal()`). Isolation wants uncertainty to survive even
direct, sustained attention; Peripheral's uncertainty lives entirely in *not
yet looking*. These aren't reconcilable by a shader tweak — it's a decision
about whether centred vision is ever allowed to be fully trustworthy.

### 3. No inventory/collectibles rule vs. Isolation's entire comfort-item/collectible system

`PERIPHERAL_UNREAL_HANDOFF.md` §13 (from the original brief, restated in
`CLAUDE.md`'s "don't" list): *"No stamina, inventory, collectibles, or notes
to read."* The one exception carved out on purpose was the single-use house
key added in revision 0.3 — "don't generalize this into a broader item
system" is explicit in that session's own commit message.

Isolation is built substantially around exactly the system that line warns
against: photographs, videos, VHS, voice recordings, letters, documents (§16
— fourteen distinct collectible types), plus a parallel comfort-item
inventory (recordings, music, painkillers, phone, walkie-talkie, door locks,
flashlight — §18) with its own attrition mechanic (§19, items disappearing
over time to erode the player's sense of safety). This is a core pillar of
Isolation's design, not an incidental feature — worth a decision, not a
workaround.

### 4. "Entity never chases" vs. the Day 3 running-footsteps / back-door sequence

Handoff §13 / `CLAUDE.md`: *"The entity never chases, touches, or kills the
player."* Isolation §50–51 (Running Footsteps, Back Door Sequence): fast,
loud, approaching footsteps of ambiguous origin, escalating until *"Jack
rushes toward the back door... he reaches the door... he locks it."* Nothing
is ever shown chasing him, and Isolation §61's own "core design rule" (let
the player *think* they saw it) argues the footsteps are meant to read as a
chase-shaped feeling rather than a literal chase. Whether that distinction
holds under actual play — a locked-door escape beat with approaching audio
is hard to not feel like a chase — is worth a second read before building it.

### 5. Fixed, physically consistent house vs. house topology / reality changes

The Peripheral fovea, occlusion-raycast, and collision systems (handoff §2,
§5) all assume a static level graph — an anomaly's anchor point and the
raycast that checks it never move underneath the state machine. Isolation
§29–30 wants the house itself to become spatially unreliable: rooms
appearing elsewhere, a bathroom door leading somewhere it structurally
shouldn't (§28), waking in a different room with no transition (§30). This
isn't just new content, it's a different requirement on the level
architecture — worth scoping properly before committing to it, since it
touches the same systems both documents call the most important ones in the
game.

### 6. Single exterior door vs. a back door + garage

`CLAUDE.md` states the shipped house has *"the only exterior door"* at the
front, and the web build's `house.js` only builds one. Isolation needs a back
door (§51) and a garage with a wrench (§27–28) — new exterior geography, not
covered by the current house layout in either the web prototype or the
handoff spec.

---

## NEW — not in the existing spec, no conflict, could be added as its own section

Organized by system. None of these touch the six items above; they're purely
additive if/when the project-identity question (item 1) is resolved in favor
of building this out.

**Narrative frame**
- Named protagonist "Jack": altered ID, 5-year estrangement, believes memory
  issues are stress-related, gradually questions his name/childhood/family/
  job/identification (Isolation §2).
- Prologue: a letter (address, job, the date "1998"), a lawyer, family deaths
  under unexplained circumstances, an inherited deed (§3).
- Central mystery framed explicitly as identity/family, not "what's the
  monster" (§66).

**Day/time structure**
- A 3-day scripted timeline (§33–51) with a work/commute loop on Day 2
  morning, distinguishing "the house is not yet Jack's whole world" from
  later isolation.
- Escalation beats tied to specific days: unlocked-door discovery (Day 3),
  blackout + flashlight search (Day 3 night), power restoration → figure
  through a window → footsteps → back-door lockdown (Day 3 climax, current
  end of designed content per §67).

**Memory / identity collectibles** (contingent on decision #3)
- Photographs, videos, VHS, voice recordings, letters, documents, school
  records, identity documents, evidence tied to "1998" (§16).
- Discovery-triggered fragmented-memory effects: children's laughter, brief
  audio echoes, unclear faces — explicitly *not* full cinematic flashbacks
  (§17).

**Comfort-item system with attrition** (contingent on decision #3)
- Items exist to fight loneliness, not monsters: voice recordings, music,
  painkillers, phone, walkie-talkie, door locks, house key, flashlight (§18).
- Comfort is temporary — the game deliberately removes each source of safety
  over time (recordings vanish, walkie-talkie vanishes, phone contact goes
  bad then unreachable, locks start to feel unreliable) (§19, §55).

**Random event framework**
- A conditional-event system keyed on day/time/player behavior/isolation
  level rather than a fixed script (§21).
- Named events: doorbell with nobody there (§22), answering-machine
  distortion that worsens the longer Jack stays inside and is relieved only
  by sitting on the porch (§23–24), misplaced house key blocking that relief
  valve (§25), a player-choice branch where fumbling with the machine costs
  two comfort items with no explicit notification (§26), hot-water failure
  with a proper-repair-vs-shortcut choice (§27–28), and a phone call whose
  other party becomes subtly, unsettlingly wrong before going permanently
  unreachable (§31–32).

**New locations / objects**
- Garage, with a wrench used for the proper hot-water repair (§27).
- A porch-as-relief mechanic: sitting outside measurably lowers tracked
  distortion/mental-pressure state (§56).
- A kitchen knife carried as a psychological safety object on Day 3,
  explicitly not a combat item (§41).

**Focus / concentration mechanic** (see decision #2 for the conflict it raises)
- A press-and-hold input that sharpens a currently-uncertain shape somewhat,
  without ever reaching full clarity or revealing the entity (§12).

**Hidden state variables**
- Isolation, Mental Strain, Comfort/Safety, Memory Recovery, and Reality
  Distortion as tracked (not necessarily HUD-visible) variables influencing
  event frequency, audio, and environmental behavior (§20).
- Broader in scope than Peripheral's existing `PlayerProfile` (which only
  biases anomaly placement) — this would feed dialogue availability, item
  disappearance, and house-layout changes too, if built.

**Object disappearance / environmental uncertainty**
- Items relocate or vanish after events, choices, sleep, room transitions, or
  distraction, with no explicit "ITEM REMOVED" notification — the not-knowing
  is the point (§53).
- Minor unexplained room inconsistencies (moved lamp, open drawer, rotated
  photo, repositioned chair) that don't all get resolved (§54).

**Design rules stated for the record** (mostly restating principles Peripheral
already holds, but stated as explicit tie-breakers worth keeping on file)
- When in doubt: let the player *think* they saw something rather than show
  it (§61); preserve entity uncertainty over explaining it (§62); prefer the
  quiet sound the player isn't sure they heard over a loud sting (§63,
  already Peripheral's audio design in practice); a room subtly different
  from memory before anything overtly supernatural (§64); items represent
  memory/connection/safety, not combat power (§65).

---

## DUPLICATES — already covered in the existing spec, not repeated here

- Genre/tone: psychological horror over gore, jump scares, or monster
  showcases — handoff §1, §13.
- The core "did I actually see something?" premise and the rule that nothing
  ever confirms itself — handoff §1, the fovea/anomaly system generally.
- Peripheral objects reading as a person until looked at directly (lamp,
  coat, chair, nightstand-adjacent shapes) — this is exactly what Peripheral's
  12 anomalies already do (handoff §3), including four that are literally "a
  humanoid figure appears, then is gone the instant you centre it" (the
  bathroom mirror, both window figures, the hallway-end figure).
- No jumpscares, no loud stings, no clean monster reveal, ambiguous
  silhouette if one appears at all, entity proportions "human-like but
  wrong" — handoff §1, §3, §13; the shared humanoid silhouette in
  `world/figure.js` was built to exactly this brief.
- Flashlight as the primary light source once the power is out, with no
  battery mechanic — handoff §6, §7 (and this session's own flashlight
  widening covers the same "make sure something is visible" goal Isolation
  §6 argues for).
- House key found mid-game, tied to security/reassurance — handoff §8
  epilogue (added revision 0.3), independently converges on the same beat.
- Breaker/power restoration requiring the player to leave lit safety and go
  to a utility/exterior area — handoff §5, §6, §8 (breaker box on the dark
  exterior wall, Act 2 climax).
- A figure glimpsed once, gone on a second look, never explained — handoff
  §3 anomaly #8/#9, and the Act 2 entity generally.
- Footsteps and quiet environmental audio over stingers as the primary fear
  tool — handoff §12 audio design.
- Ordinary domestic activities (unpacking, showering) used as tension
  contrast — handoff §8 (Act 1 chores), independently converges, including
  the specific beat of a shower sequence with its own audio treatment.
- Non-combat design, no weapons as a power fantasy — Peripheral never had
  combat to begin with.
- House loosely "learning" the player without confirming it's literal —
  overlaps with Peripheral's existing Director/PlayerProfile system (handoff
  §4), though narrower in scope; see the New section above for where the
  scope actually differs rather than duplicates.
