# PERIPHERAL — master feature list

> Supplied verbatim by the user as a consolidated "single source of truth,"
> intended to supersede build brief 0.1, revision 0.2, and the signage
> addendum 0.2b. Saved as instructed. **Not reconciled against the shipped
> build, the other repo docs, or itself** — see the conflict list immediately
> below before treating any single line here as settled. Nothing was changed
> in the game or in other docs to match this file; that's a decision for
> whoever owns the design, not something to resolve silently.

---

## ⚠️ CONFLICTS — flagged, not resolved

Ranked roughly by how much they change, most consequential first.

### 1. Revision 0.3's status is unclear, and this doc's own text contradicts what's shipped from it

The supersession line names build brief 0.1, revision 0.2, and signage
addendum 0.2b — **revision 0.3 isn't listed**, so it's ambiguous whether 0.3
still stands or is being quietly walked back. The doc's own content reads
like the latter, and two of the contradictions are with features added in
0.3 *at this user's own explicit request earlier in this same conversation*:

- **§6 describes a ~22° tight flashlight cone.** The shipped flashlight is
  38° hot cone / 82° dim fill (`src/game/player.js`) — widened specifically
  because a narrow beam was making Act 2 "mostly pure black outside dead
  centre," which was the direct complaint that prompted the change. Reverting
  to 22° reintroduces the exact problem that fix was for.
- **§6's Act 2 ending is breaker-flip → immediate ending.** Shipped Act 2 has
  a key/lock epilogue after the breaker (find the key on the entry table,
  return to the front door, lock it, *then* the ending plays) — also added
  in 0.3 at this user's request, and not mentioned anywhere in this doc.
- Also unmentioned: all four real doors (not just the front door) are
  interactable, and the shower has a ribbed curtain, animated falling water,
  and a 10-second held freeze with its own audio cue — all shipped in 0.3.

Worth an explicit answer: does 0.3 still apply on top of this doc, or is
this doc meant to roll it back?

### 2. Internal contradiction: session length

§1: *"About 20 minutes, two acts."* §12 (same document): *"Both acts
finishable in about 8 minutes."* These are the same document disagreeing
with itself by 2.5x on the target playtime.

### 3. Internal contradiction: music tied to events

§13 (Don't list): *"No music tied to events."* §8, four lines above it in
the same document: *"no note within 3 seconds either side of an anomaly
arming or resolving"* — a hard suppression window keyed to anomaly state
changes is a form of coupling music to events, even if it's "stay silent
near X" rather than "play at X." Worth one clarifying sentence either way.

### 4. The anomaly roster is a near-total redesign, not an addition

§4.5 lists 9 interior anomalies (11 with the 2 exterior ones) and says
*"Eleven total. Do not add more"* — read as an exhaustive cap. The shipped
build currently has 12 (10 interior + 2 exterior), and the two lists don't
match:

- **Dropped, present in the shipped list, absent from §4.5:** the bathroom
  door (ajar → wide open), the phantom fifth hallway door, and the
  living-room window figure.
- **Added, in §4.5, not currently built:** a figure filling the hall
  doorway frame, and a figure lying on the bed.
- **Changed in nature, not just detail:** the shipped lamp, coat, chair, and
  portrait anomalies are furniture-only wrongness (a lamp leans, a chair is
  pulled out, a coat has volume, a painted head turns) — no figure appears.
  §4.5 converts all four into explicit full-figure appearances ("figure
  standing where the lamp was," "figure hanging from the hook, feet just off
  the floor," "figure seated," "framed figure has stepped forward, out of
  the frame plane"). That shifts the anomaly mix from roughly 40% figure
  reveals to 80%+, which is a real change in the game's rhythm, not a
  wording update. Worth flagging too: "feet just off the floor" and a
  literal hanging figure read closer to explicit body-horror imagery than
  the current "coat has volume as if worn" — worth checking against §13's
  own "no blood, gore" line.

### 5. Bed-gating reverses a rule this project has stated as non-negotiable every time it's come up

§6: four chores (unpack, shower, lock the front door, turn off the kitchen
light) — *"Only after all four does the bed become interactive."* Every
prior version of this spec, including the original build brief, revision
0.2, and this session's own work, states the opposite explicitly: the
shipped code comment reads *"a beeliner can still sleep immediately — they
just give the night somewhere to go while the house works on them."* This
isn't a minor wording drift, it's a direct reversal of something documented
as a hard rule three separate times before this file.

### 6. "Act 2 has no piano" reverses revision 0.2-D, done at this user's request

§8: *"Act 2 has no piano. Crickets and footsteps only."* The shipped audio
engine calls `setAmbient('act2')` in `_setupAct2()` specifically — a
sparser, lower-register piano bed was added to Act 2 deliberately in
revision 0.2-D after this user asked for "more airy" music with piano. This
doc removes it entirely rather than re-tuning it.

*(Separately, §8's piano synthesis itself — partial ratios, decay time,
delay network, note-timing model, event-silence window — is a substantial
rewrite of what's implemented, not just new parameters. Not calling that a
"conflict" since nothing currently claims those specific numbers are final,
but flagging that adopting §8 as written means rebuilding the piano voice
from scratch, not retuning it.)*

### 7. The workflow model conflicts with `CLAUDE.md` and with how this session has actually been operating

§11 / §14: *"Open a PR per milestone; the director merges,"* and *"the
Claude Code operator works on branches and opens PRs, never pushing to
main."* `CLAUDE.md`'s documented workflow (and this session's actual
history, including the last three commits) is direct push to `main` after an
`AGENT_LOG.md` entry, by whichever teammate is driving — no PR gate, no
single "director" merge role is currently in effect. This one matters beyond
documentation: if adopted, it changes how I should behave starting now, not
just how the docs read.

### 8. This doc sides firmly against `VISUAL_REFERENCE.md`, which is still sitting unresolved in the repo

§3's palette and §4.2's shader are, respectively, the exact five original
hex values (with the flashlight's warm exception intact) and the exact
radial-blur-plus-desaturation shader already shipped — explicitly restating
*"Not a vignette. The blur and the desaturation are the point."* That's a
third, independent document (after the original brief and `CLAUDE.md`) now
siding against `VISUAL_REFERENCE.md`'s proposed "Void Charcoal" palette and
its blur-rejection. Since this doc claims single-source-of-truth status, it
might be the moment to explicitly close that conflict — either retire
`VISUAL_REFERENCE.md`'s proposal, or reconcile this doc with it — rather than
letting a fourth document quietly disagree with a third.

### 9. "No second location" bears directly on the still-open question in `FEATURE_LIST.md`

§13: *"No second location. Every horror project that dies in development
dies from adding one."* `FEATURE_LIST.md` flagged whether "Isolation" (a
much larger, multi-day concept requiring a garage, a back door, and
work-commute locations) is the same project as Peripheral or a different
one. This rule would rule out nearly everything Isolation's design needs.
Might be worth treating this as the answer to that open question — or
flagging that it isn't, if Isolation is still meant to be evaluated.

### 10. Minor: repo layout doesn't match what's actually on disk

§10 places `figure.js` and `chores.js` under `src/game/`. Currently
`figure.js` lives in `src/world/` (it's world geometry, reused by props and
the Act 2 entity), and there's no standalone `chores.js` — chore state and
behavior live inline in `game/acts.js`, with the dresser/shower meshes in
`world/props.js`. Cosmetic, not urgent, but worth knowing before anyone goes
looking for a file that isn't there.

---

## Original document (verbatim below)

Everything decided so far, consolidated. Commit this to the repo root as
`DESIGN.md` — it is the single source of truth, and Claude Code reads it as
context on every run.

Supersedes: build brief 0.1, revision 0.2, signage addendum 0.2b.

---

## 1. The pitch

A first-person horror game in one small single-storey house. The game
separates what the player is **looking at** from what the player can **see**.
Things are wrong at the edges of vision and always ordinary by the time the
player centres them. Nothing ever confirms itself. About 20 minutes, two
acts.

---

## 2. Stack — fixed

- **Three.js** + **Vite**, plain JavaScript ES modules.
- No TypeScript, no React, no game framework, no physics engine.
- Custom capsule-vs-AABB collision, ~80 lines.
- **Zero external assets.** All geometry from Three.js primitives in code.
  All audio synthesised in Web Audio in code. All text drawn to `<canvas>`
  and used as `CanvasTexture`. No models, textures, audio files, or font
  files.
- Deploys to **GitHub Pages** via GitHub Actions. `base: '/peripheral/'` in
  `vite.config.js`.
- Repo stays under 2MB. No Git LFS, ever.

Reasons this is fixed: the repo stays tiny and free to host, licensing stays
clean, the whole game is readable source, non-coders on the team can
playtest from a URL on any device, and two people can edit the same day
without binary merge conflicts.

## 3. Art direction

- Palette: `#1A1916` `#4E4B44` `#7C7870` `#B3A78F` `#E6DFCC`. Grey and beige
  only. The single exception is the warm flashlight cone in Act 2.
- Flat and matte. `MeshStandardMaterial` at roughness 1, metalness 0, or
  simpler.
- **No specular, no bloom, no lens flare, no colour grading.** Nothing in
  the world may glint, because a glint tells the player where to look.
- Act 1 is overcast and stale, not dark. Save darkness for Act 2.
- Scale: 2.5m ceilings, 0.9m doorways, 1.65m eye height. Cramped, not
  cavernous.

---

## 4. Core mechanic

### 4.1 Fovea and periphery

Gaze is the centre of the screen.

- **Fovea** — within ~11° of camera forward.
- **Near-periphery** — 11° to ~26°.
- **Far-periphery** — beyond 26°.

### 4.2 Visual falloff (post-processing)

Render the scene to a `WebGLRenderTarget`, then draw a fullscreen quad with a
custom `ShaderMaterial`. As distance from screen centre increases: radial
blur (6–8 taps offset outward), desaturation toward luminance, slight
brightness loss. Centre is perfectly sharp.

```glsl
float r = length(vUv - 0.5) * 2.0;
float p = smoothstep(0.20, 0.95, r);
vec3 col = radialBlur(tDiffuse, vUv, p * 0.006);
col = mix(col, vec3(dot(col, vec3(0.299,0.587,0.114))), p * 0.82);
col *= mix(1.0, 0.55, p);
```

Not a vignette. The blur and the desaturation are the point. This is the
only post-processing in the game.

### 4.3 Anomaly state machine (logic — kept fully separate from the shader)

The shader must never be what hides an anomaly. Anomalies are hidden by
geometry, distance, and timing, so that a player who screenshots and zooms
still finds a real object in the world.

- `DORMANT` — available to the Director.
- `ARMED` — chosen, not yet flipped. Flips to off-state **only on a frame
  where the fovea is 40°+ away or the prop is fully occluded.**
- `ACTIVE` — visibly wrong. Holds indefinitely.
- `RESOLVING` — fovea within 11°, unoccluded (confirm by raycast), for 0.12s
  continuous.
- On the **very next frame** → snaps to normal. One frame. No tween, no
  fade, no sound, no animation.
- `SPENT` — 60–120s cooldown, and may only re-arm while the player is in a
  different room.

Add hysteresis at the 11° boundary so props don't flicker. **The player must
never catch one changing.** If a transition might be visible, don't do it.

**Reverts leave things slightly moved.** When a figure-state resolves, the
ordinary prop sits in a slightly different position than the player last
saw — chair tucked in when it was pulled out, coat hanging straighter. Small
enough to doubt. This makes players distrust their memory, not just their
eyes.

### 4.4 The figure

One shared low-poly silhouette built from primitives, reused for every
anomaly. Roughly 2.1m, narrow, elongated head, no face except two small pale
dots, one arm noticeably longer than the other. Flat near-black, no shading
detail.

Using the same shape every time is deliberate — by the fourth encounter the
player recognises the outline and starts seeing it in real furniture. Do not
design variants.

### 4.5 The nine anomalies

| Prop | Off-state |
|---|---|
| Floor lamp | Figure standing where the lamp was, arm raised in the shade's place |
| Coat on hook | Figure hanging from the hook, feet just off the floor |
| Kitchen chair | Figure seated, facing the hallway |
| Hall doorway | Figure filling the frame, shoulders touching both jambs |
| Wall portrait | Framed figure has stepped forward, out of the frame plane |
| Bathroom mirror | Figure behind the player's non-reflection |
| Bedroom window | Figure at the glass, close, from outside |
| End of hallway | Figure at the far end, small, facing the player |
| Bed | Figure lying on it, hands at its sides |

Plus two exterior anomalies in §7. Eleven total. Do not add more.

### 4.6 The Director

- If more than 45 seconds pass with nothing armed, arm regardless of normal
  pacing.
- Roughly 1 in 6 arms should arm a **second** anomaly simultaneously in a
  different room. Never two in the same sightline.
- **Never arm within 60° of where the player is currently looking**, even
  if technically outside the fovea. Things should be wrong where the player
  *has been*, not where they're heading.

### 4.7 PlayerProfile — the game learns how you look

A stats object sampled every frame, not machine learning. Tracks:

- Mean and peak yaw velocity — slow sweeper or fast twitcher.
- Coarse angular histogram of where the fovea dwells, relative to movement
  direction.
- Check-behind rate: how often the player turns 120°+ within 3s of entering
  a room.
- Room dwell times and visit order.
- Whether the player hugs walls or walks room centres.

The Director queries this and prefers the player's habitually neglected
zones. Never looks up? Arm the ceiling. Always checks behind? Stop rewarding
it and work the forward-left quadrant. Expose on `window.__profile` in dev
builds.

---

## 5. The house

Single storey, procedurally assembled from boxes in `house.js`, exporting
meshes plus collision AABBs.

- **Porch** — three steps, railing, bare bulb, front door.
- **Entry hall** — coat hooks, console table.
- **Living room** — sofa, floor lamp, low table, wall portrait, window to
  yard.
- **Kitchen** — counter run, table, four chairs, window over sink.
- **Hallway** — four doors, the longest sightline in the house. Most
  anomalies pay off here.
- **Bathroom** — sink, mirror plane, tub.
- **Study** — desk, chair, shelves. Player wakes here in Act 2.
- **Bedroom** — bed with interaction prompt, window facing treeline.

Outside: fenced yard, gravel path, a dozen low-poly conifer silhouettes as
treeline, and the **breaker box** on the exterior wall at the back corner —
placed so reaching it means walking the dark side of the house, out of sight
of the door.

### Geometry hygiene

Write a **dev-mode audit** rather than eyeballing it:

- For every mesh, raycast down from the bounding box's bottom face. Log
  anything with a gap between 1mm and 400mm. Allowlist intentionally
  suspended items (hanging coat, ceiling fixtures).
- Same horizontally for wall-mounted props.
- Fix structurally: position props by their **base**, computed from the
  geometry bounding box, never by a guessed centre `y`. This stops it
  drifting back.
- Walk the house at eye height and again crouched at 0.4m, checking every
  floor and ceiling seam for gaps.

---

## 6. Act structure

### Act 1 — Settling in

Spawn on the path outside in flat grey daylight. Walk to the door, enter. No
objective text for the first 20 seconds inside.

**Four chores**, shown as a short corner list, each in a different room so
the player crosses the house repeatedly:

1. **Unpack the duffel into the dresser** — bedroom. Hold `E` for 5s facing
   the drawer.
2. **Take a shower** — bathroom. Interact, 8s hold with running water audio.
3. **Lock the front door** — entry hall.
4. **Turn off the kitchen light** — kitchen. The kitchen stays dark for the
   rest of the act.

Only after all four does the bed become interactive: *"Get some sleep."*

The chores exist because **each one forces the player to stand still, facing
a wall, with a room at their back.** The shower especially — loud water,
can't see the door behind them, eight seconds. Arm something in the hallway
during every shower. Chores are not fail-able and there is no timer; the
dread comes from being occupied, not pressured.

Interacting with the bed ends the act.

### Transition

Cut to black, 3s of held silence, one low sub-bass swell.

### Act 2 — The power

Wake on the floor of the **study**, not the bedroom. Camera starts tilted at
a wrong angle and rights itself over ~2s. All interior lights dead.

**Flashlight**: `SpotLight`, tight warm cone, ~22° penumbra, plus a faint
wide falloff so the player isn't fully blind outside the beam. No battery
drain in this build.

Objective: *"The breaker is outside."* Leave the house, walk to the back
corner, interact with the breaker box.

Outside is genuinely dark — near-black ambient, cold moonlight directional at
~0.08, treeline barely separable.

**Crickets.** Continuous synthesised bed outside. When the entity is within
15m and unoccluded, the crickets **stop** — not fade, stop, over ~400ms.
They resume 6s after it's gone. Never explained. Cheapest and best scare in
the build.

The Act 2 entity follows the same peripheral rules: only ever outside the
fovea, perfectly still, removed the frame it's centred. **It does not chase,
touch, or kill.** It just gets closer each time it reappears.

Flipping the breaker restores lights, crickets return loudly, cut to a card:
**PERIPHERAL — END OF BUILD 0.1**, with return to menu.

---

## 7. Exterior signage

### The buyer name

A browser cannot read the OS username — no API exists, and anything
claiming otherwise is fingerprinting guesswork. Ask directly, and make the
asking part of the fiction.

- On the main menu, below **Start**, a single text field styled as a line on
  a realtor's form: thin rule, label **BUYER** beneath it, same flat mono
  type. No modal, no prompt, no explanation.
- Persist to `localStorage` under `peripheral.buyer`. Never transmitted —
  note this in the README.
- Sanitise: trim, cap 22 chars, allow letters, space, hyphen, apostrophe.
  Render uppercase.
- Empty falls back to `NEW OWNER`, and the fallback should feel deliberate.

Being asked to sign a form and then finding your name on a sign outside is a
better beat than a title card saying hello. Keep it that quiet.

### The signs

Render text to `<canvas>` at 1024px wide → `CanvasTexture` on a plane.
System fonts only. Weather everything: faint noise overlay, uneven ink, a
few percent off true. Nothing in this world is crisp.

1. **Yard sign** — end of the gravel path, angled to the road. Two posts,
   ~0.9 × 0.6m board, bottom edge 0.7m up. Reads `HOME FOR SALE` / `SOLD TO`
   / `[BUYER NAME]`, with a **SOLD** banner across the corner at ~20°,
   printed slightly crooked. First thing the player sees. No interaction
   prompt, no forced look.
2. **Realtor placard** — stapled to the fence by the gate. Agency name, fake
   phone exchange, and a flat vector portrait of the agent: circle head,
   simple shoulders, two dots and a curved smile.
3. **Two OPEN HOUSE flyers** — fence and porch post, curled corners,
   rain-faded. Set dressing.
4. **Inspection notice** on the front door — checkboxes all ticked, one line
   reading `STRUCTURE — NO FINDINGS`. Set dressing.

### The two exterior anomalies

- **Realtor portrait.** Off-state: the agent's face is the figure's face —
  two pale dots, no smile. Head outline identical, only the interior
  changes. Most subtle anomaly in the game; keep it that way.
- **Yard sign, Act 2 only.** In the dark, at the edge of the flashlight
  beam, it reads `HOME FOR SALE` with no SOLD banner and a blank line where
  the name was. Resolves back when centred, like everything else.

Never a version where a sign says something threatening or addresses the
player. The name simply not being there is stronger than any sentence, and
the moment a sign talks to you the game stops being about doubt.

---

## 8. Audio

All Web Audio, synthesised, no samples.

### Piano bed (Act 1 only)

- **Synthesis**: additive sines at 1x / 2x / 3.01x / 4.98x with
  fast-decaying upper partials, short filtered-noise transient at note-on
  for the hammer, 6–9s exponential decay.
- **Space**: feedback delay network, three lines at 41ms / 67ms / 103ms,
  lowpassed feedback ~0.6 — a room bigger than the house.
- **Notes**: single notes only, never chords. Drawn from D, F, G, A, C
  across three octaves, weighted upper. That set never resolves major or
  minor, so it stays unsettled without sounding like horror shorthand.
- **Timing**: intervals of 9–22s from a continuous random range. Never
  quantized, no grid, no tempo. Occasionally drop a 45–60s gap of nothing.
- **Critical rule**: no note within 3 seconds either side of an anomaly
  arming or resolving. If music correlates with events, players learn to
  hear scares coming and the mechanic is dead.
- Act 2 has no piano. Crickets and footsteps only.

### Everything else

Crickets with the silence cue (§6), footsteps differentiated on wood vs
gravel, a low house tone, running water during the shower, the sub-bass
transition swell, and the low swell on the ending.

**No jumpscare stingers. No loud transients anywhere.**

---

## 9. Menu and controls

Three items, DOM overlay over the canvas, flat mono type:

- **Start** — begins Act 1, requests pointer lock, initialises AudioContext
  on this click.
- **Pause** — `Esc`, also releases pointer lock. Freezes update, keeps
  rendering the last frame behind a dim overlay. Offers resume and exit to
  menu.
- **Exit** — stops the loop, disposes the scene, returns to menu. A browser
  tab can't close itself, so the UI copy should say "exit to menu." Never
  call `window.close()`.

Plus the **BUYER** field from §7.

No settings menu, no options, no volume slider, no graphics presets.

**Controls**: `WASD` move, mouse look, `Shift` slower, `E` interact, `Esc`
pause. There is no run — the default pace is already unhurried. Show the
controls on the menu once and never again.

---

## 10. Repo layout

```
peripheral/
  index.html
  package.json
  vite.config.js          # base: '/peripheral/'
  .github/workflows/deploy.yml
  README.md
  DESIGN.md               # this file
  docs/boards/            # storyboards as markdown + small PNGs
  src/
    main.js
    core/      renderer.js  input.js  audio.js  collision.js  loop.js
    world/     house.js  yard.js  props.js  signage.js  lighting.js
    game/      player.js  fovea.js  anomaly.js  figure.js  director.js
               profile.js  chores.js  acts.js
    fx/        peripheral.js
    ui/        menu.js  hud.js
```

---

## 11. Build order

1. **Skeleton** — Vite + Three, grey box room, pointer-lock FPS controller
   with collision, Esc pause, menu with Start / Pause / Exit. Deploy to
   Pages immediately to prove the pipeline.
2. **The house** — full layout, props, colliders, working doors.
3. **The peripheral pass** — render target + shader. Tune until the centre
   is crisp and the edges are convincing mush. This decides whether the
   game works; spend time here.
4. **Fovea + anomalies** — angle tests, occlusion raycasts, dwell timers,
   state machine, the figure, all eleven props.
5. **Director + profile**.
6. **Chores** and Act 1 gating.
7. **Act 2** — wake-up, flashlight, dark rig, yard, breaker, ending card.
8. **Signage** and the buyer name.
9. **Audio** — piano bed, crickets and the silence cue, footsteps, swells.
10. **Geometry audit** and polish.

Commit after each. Open a PR per milestone; the director merges.

---

## 12. Acceptance checks

- 60fps on integrated graphics at 1080p. One render target, one fullscreen
  quad — the post pass is the only expensive thing.
- No anomaly transition ever visible on screen. Test by strafing past props
  while staring straight ahead.
- Frame-stepping a screen recording shows the anomaly genuinely present in
  the world, not a shader trick.
- Pointer lock releases cleanly on Esc and tab-out, re-acquires on resume
  without the camera jumping.
- Nothing floats. The audit passes with only allowlisted exceptions.
- Both acts finishable in about 8 minutes.
- Repo under 2MB.
- Two minutes of play with no stretch where you'd feel safe turning your
  back.

---

## 13. Don't

- No jumpscares, screamer stings, or loud transients. Nothing in this game
  confirms itself.
- No blood, gore, or written lore. The house is ordinary and that's the
  horror.
- The entity never chases, touches, or kills in this build.
- No animated reverts.
- No music tied to events.
- No stamina bar, inventory, collectibles, or notes to read.
- No post-processing beyond the peripheral pass.
- No second location. Every horror project that dies in development dies
  from adding one.
- No voice acting, no cutscenes.

---

## 14. Infrastructure and team

**Cost: $0.** GitHub Free organisation (unlimited private repos, unlimited
collaborators), GitHub Pages, GitHub Actions free on public repos, Discord,
Excalidraw. No LFS — the no-assets rule means the repo never needs it. Set
the org's **Git LFS budget to $0** so an accidental large file blocks rather
than bills.

**Roles.** Director owns `DESIGN.md` and GitHub Issues, and is the only
person who merges to `main` — reviewing by clicking the Pages preview link,
not by reading diffs. Storyboard work lives in `docs/boards/` as markdown
plus PNGs under 500KB. The Claude Code operator works on branches and opens
PRs, never pushing to main.

Design documents live **in the repo as markdown**, not in Google Docs,
because Claude Code reads the repo and cannot read anything else.

---

## 15. The one rule above all others

Every feature must make the player more afraid to turn their back. If it
doesn't, cut it.
