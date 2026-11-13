# Peripheral: Design Bible

The single source of truth for the Unreal build (`unreal/Peripheral_POC`). It gathers every instruction Joel gave in the build
session: the master prompt and each update after it. It is organised by topic, not by date. Where two instructions conflict,
the most recent one is written here and the older one is dropped. Change this file only when Joel approves a change.

Companion files: `HOUSE_BLUEPRINT.md` (the house, generated from `Scripts/house_plan.py`), `unreal/Peripheral_POC/BUILD_STATE.md`
(the running log and every judgment call), reference photos in `unreal/Peripheral_POC/Reference/` (the `private/` ones are
Joel's family-home photos and are never committed).

## 1. What this is

- "Peripheral": a first-person psychological horror game about grief. Quiet, emotional, never cliché horror. No monsters that hunt, no death.
- Jack, an older Gen Z man in his mid-20s, inherits his childhood home after his parents die. He arrives with almost nothing: two moving boxes.
- The horror comes through nostalgic objects and the house quietly breaking its own rules. The house must feel like someone's real childhood home, not a horror set.
- The team is not technical and cannot do 3D art. Everything (models, textures, materials, lighting, sound, music) is made in-project by code.
- Joel is a visual person: screenshots beat descriptions.

## 2. Engine, platform, repo

- Unreal Engine 5.8 (not Unity, not a preview build). Lumen, Nanite, Virtual Shadow Maps. If one of them runs badly on this Mac, use the closest Mac-friendly option and log it.
- Target: macOS on Apple Silicon (Metal), smooth 30 to 60 fps, with scalability settings. Keep the project Windows-ready: no Mac-only code.
- Repo: `github.com/ezekielgblount-sketch/peripheral`, branch `poc/visual-slice`, project `unreal/Peripheral_POC`. Git LFS for big binaries. Never commit secrets or the private reference photos. `Builds/` is not committed.
- The old Unity scene and web build are references only.
- The editor is driven through the Unreal MCP plugin and Python scripts in `Scripts/`.

## 3. Rules that must not change without asking

The peripheral mechanic, the story premise, the flashlight spec, the era mix and the bodycam feel. (The house layout was on this list; Joel approved the bigger layout in playtest round 1, so the current layout is the one in `HOUSE_BLUEPRINT.md`.) If something cannot be done, stop and explain it in plain English.

Standing content rules: invented brands, titles and logos only; no copied artwork; no real faces; faces in photos stay blurry generic shapes; matte and worn, never glossy or showroom-polished.

## 4. How to work

- Autonomous. Build in milestone order (section 20). After each milestone: package a playable Mac build in `Builds/`, commit, push, update `BUILD_STATE.md`. If time or budget runs out, the latest build must still launch and play.
- Cut detail before cutting playability. Log every judgment call in `BUILD_STATE.md` in plain English.
- Re-read the relevant section of this file before each milestone.
- Review your own screenshots and fit checks and fix problems before moving on.
- Keep token use lean: reuse materials, modular props, skip unseen detail.
- On Joel's Mac: never move or focus his windows; never launch the packaged game while he is using the machine unless he asks; watch memory (36 GB machine) and disk.

## 5. Scale and fit checks (must pass)

- 1 Unreal unit = 1 cm. Player 178 cm tall, eye height about 165 cm, capsule radius about 35 cm.
- Ceilings 244 cm in main rooms; basement 213 to 229 cm. Doors 203 cm tall, 81 to 91 cm wide. Hallways at least 91 cm (the build uses at least 120).
- Stairs: risers 18 to 19 cm, treads 25 to 28 cm, at least 203 cm headroom.
- Furniture at real sizes: 91 cm counters, 76 cm tables, 43 to 46 cm seats.
- Fit check before screenshots: walk the capsule through every doorway, hall and stair; nothing clips, blocks or forces a crouch. `Scripts/fit_check.py` does this.
- A 178 cm figure in room screenshots as a scale reference. That figure is now Jack himself (section 12), not a mannequin.

## 6. The house

- A larger suburban two-storey with basement, about 2,800 to 3,200 sq ft, real ceiling heights. Rooms wider and longer, not taller. Walking between far rooms takes roughly 8 to 15 seconds; crossing a main room 4 to 6 seconds.
- Longer hallways and corners that break lines of sight: that is where anomalies get their chance.
- Rooms: entry, living room, family room / den, dining room, kitchen with eat-in nook, laundry / mudroom, half bath, parents' bedroom with bathroom, Jack's childhood bedroom, a sibling's room, a guest / sewing room, a full hall bathroom, an attic loft, a basement, an attached two-car garage.
- Stair rules kept where possible: split entry, L-shaped stair core, the down flight straight ahead, the up flight turning left, away from the garage.
- Through the windows: a believable street with neighbour houses, trees, sky. Low detail is fine.
- The house assets never change with unease; only post-process, audio and the scripted anomalies do.

## 7. Era, story realism and props

- Structure, furniture and decor are old because they were kept for decades. Theme: "warm Americana family home, late 90s to 2000s": what 90s and 2000s kids grew up with.
- The house sat empty only a few weeks: no dust sheets. A mug in the sink, a jacket on the hook, a grocery list and kids' drawings under fridge magnets, light dust, mail at the door.
- Technology realism (overrides any earlier CRT-in-the-living-room idea): the parents' everyday tech is about 10 to 15 years old (around 2010 to 2014). Living room / den TV: a small older flat-screen, 22 to 32 inches, thick bezel, on the old wood entertainment centre. Also: an older DVD or early Blu-ray player, a dated laptop, an aging Wi-Fi router with blinking lights, a cordless phone, a tablet in a cracked case, chargers in outlets, a game console of that era and an older one forgotten in a cabinet.
- Old media hangs around: VHS tapes, DVDs and CDs on shelves, an old VCR in a closet.
- Jack's things are the true time capsule (about 1998 to 2010), kept in his room, the attic loft, closets, boxes and the basement: CRT TV or monitor, beige PC, handheld console, posters. Old CRTs may also be stored in the basement or garage.
- Nostalgia prop pool, spread naturally, never museum-like:
  - Living room: floral or tufted couch with afghan, glass candy dish, remote in a ziplock bag, family portrait in matching outfits, fake plant, ceiling fan with pull chains, jar candles.
  - Kitchen: almond or honey-oak finishes, wall phone with coiled cord, cookie tin of sewing supplies, bag-of-bags under the sink, school photos and many fridge magnets, popcorn tin, fake fruit bowl, rooster or apple decor, mismatched Tupperware and mugs, junk drawer, wall calendar.
  - Jack's room / loft: glow stars, bunk bed or daybed, kids' learning tablet, handheld console and cartridge case, trading-card binder, plush collection, CD player, inflatable chair, gel pens, sticker-covered dresser, invented-band posters.
  - Bathroom: seashell soaps, matching toilet seat cover and rug, blue mouthwash, frosted shower door, decorative towels.
  - Grandparents layer: china cabinet, doilies, heavy wood furniture, a loudly ticking clock, old encyclopedias.
  - Small tells: height marks on a door frame, a bowl of keys and loose batteries, a phone book, faded rectangles where photos used to hang.
- Family photos: normal posed portraits in frames, very low texture resolution, warm drugstore-print colour, grain, orange date stamp, faces blurry generic shapes. Real staged photos will replace them later.
- Reference rooms from Joel's photos (match layout, materials, mood): (A) piano corner with dark upright, globe, brass lamp, bust, spindle chair, snowy village print, round thermostat; (B) seating with butter-yellow tufted sofa, quilt, dark-framed mirror flanked by brackets with copper pitchers, gold glass coffee table, cream nailhead armchair, sage chair, Persian-style rug; (C) built-in bookcases with an eye-level shelf of 10 to 12 mismatched frames, dark hardcovers, a wooden keepsake box with a metal handle (saved for the final story beat), photo albums and storybooks; (D) fireplace with white mantel, red brick, fall garland, brass clock, felt THANKFUL banner, coastal print; (E) entry / hall secretary desk with brass pulls, swing-arm lamp, framed map, banjo barometer; (F) dining with honey-maple hutch with leaded-glass doors, beams, glass pendant, patio door with coral-red floral valance, brass sconce; (G) attic loft with slanted shiplap ceilings, stair opening with rail, homework nook (wood desk with glass top, red swivel chair, mint lamp, fractions and cursive charts, beige CRT and keyboard), rust-red armchair, craft drawer towers, tan loveseat, maple dresser.

## 8. Colour theme, walls and floors (locked)

- Most walls are PAINTED. White or off-white trim and ceilings everywhere so rooms read clearly and never melt into one yellow tone.
- Paint per room: entry, halls, stairwell warm greige / light khaki (one continuous treatment up the stairwell, no gap); living room antique white with honey oak trim; den tan with a deep burgundy accent wall; kitchen butter cream with a fruit or rooster wallpaper BORDER near the ceiling only; dining room cream damask wallpaper (wallpaper room 1); parents' bedroom dusty sage; Jack's room medium navy or denim blue with a sports or space border; sibling's room soft lavender or seafoam; guest / sewing room small floral wallpaper (wallpaper room 2); bathrooms one powder blue, one mauve / dusty rose with a matching shower curtain.
- Wallpaper in at most 2 or 3 rooms. Different paint or paper per room; never the same texture repeated across rooms.
- Avoid Backrooms colours: no single mono-yellow, no fluorescent office tones. Every room needs contrast between walls, trim, floor and furniture.
- Floors: honey oak hardwood in the entry, living and dining rooms; kitchen scuffed almond-and-brown sheet vinyl with a fake-tile pattern and small accent diamonds; bedrooms and loft loud, slightly clashing carpet (Jack's a bold multicolour kids' pattern, parents' mauve or dusty rose, den dark burgundy / green multi-tone); bathrooms small hex or square tile with dingy grout.
- Accent palette for furniture and fabric: honey oak and some cherry, burgundy, hunter green, navy, mustard. Grade warm and slightly yellowed, in step with the unease curve.

## 9. Outside

- Driveway: clear concrete with oil stains and cracks leading to the two-car garage. No tree in it, ever.
- Garage: oil stains, workbench, pegboard tools, second fridge, holiday decoration bins, bikes, push mower, garden hose.
- Back yard: fenced lawn (wood privacy fence or chain-link), small wooden shed, old swing set or trampoline, patio with gas grill and plastic chairs, garden bed, sprinkler. Neighbour houses visible over the fence.
- The car: an invented early-90s compact four-door (think old Corolla or Civic, no real make or badge). Realistic, not toy-like: correct proportions, curved panels, panel gaps, rubber seals, proper wheels and tyres, real glass, mirrors, door handles. Wear that matches the house: faded paint, light rust at the arches, dirt low down, a small dent. Checked against real reference photos.

## 10. Look: materials, lighting, post-process

- Grounded realism, slightly below photoreal: the camera does most of the convincing. Full PBR with real wear (scuffs, dust, faded paint, sun-bleaching, fingerprints). Glints allowed on normal objects. Believable clutter on every surface.
- Daylight: a warm daytime pass through the windows, volumetric dust in sunbeams. A day / night toggle key stays for judging both moods.
- Interior lighting: real warm bulbs, mostly incandescent about 2700 K (frosted globe ceiling fixtures, table lamps with fabric shades, brass sconces); a halogen torchiere in the living room about 2900 to 3000 K bounced off the ceiling; halogen track lights in the kitchen; one or two mismatched newer bulbs (a slightly cooler CFL in the hall, kitchen or bathroom). Soft lampshade glow, warm pools with darker corners, a slight flicker in one old fixture.
- Every lamp is a real light source the player can switch on and off.
- Flashlight: about 2800 to 3000 K, tint #FFE6B8, 30 degree inner and 60 degree outer cone.
- Post-process: subtle film grain, light vignette, filmic tonemapping, soft bloom only on real light sources.

## 11. Bodycam camera feel (always on)

- Reads as real body-cam or handheld footage, even on the bright first day. Separate from the VHS unease effects.
- Chest-mounted motion: sway while walking, a small jolt per step, lag on fast head turns, a settle on stopping. A setting scales camera-motion intensity for motion sickness. Head bob has an off switch.
- Lens: wide, about 90 to 100 degrees, slight barrel distortion, mild edge softness that stays out of the centre.
- Exposure adapts slowly (blown out stepping into sun, crushed stepping into the dark). Light shadow noise, gentle motion blur, slight compression softness, a touch of chromatic aberration at the very edges only.
- No HUD, timestamp or recording overlay. Diegetic and clean.
- Unease effects never touch the camera motion itself.

## 12. Jack, the player character

- Mid-20s, about 178 cm, average build, a little thin and worn-down. Messy short brown hair, a few days of stubble, tired eyes.
- Clothes: faded grey hoodie or an open flannel over a plain tee, worn jeans, beat-up white sneakers, slightly wrinkled.
- Build him with MetaHuman for a realistic body, hands and face; if MetaHuman does not run well on this Mac, use the most realistic option available and log it. Realistic walk, idle and crouch animation matched to the bodycam camera.
- He replaces the mannequin everywhere.
- What the player sees: a full-body shadow that matches his real body and clothes and moves with his animation; looking down, his own legs, jeans and sneakers; hands and forearms during interactions (doors, boxes, inspect, chores, flashlight); in mirrors and reflections, Jack with his face hard to read (soft focus, dim light, steam or dust), in keeping with "faces stay unclear". The centre-screen rule still applies.
- The shadow can misbehave as an anomaly: at certain moments, for example when he stands still, it moves out of place.
- Screenshots of his shadow, hands, a downward view and a mirror reflection go in `screenshots/player_character`.

## 13. Controls and interaction

- First-person walk, look, crouch. Flashlight toggle. Open and close doors and drawers. Inspect mode: pick up a small object and turn it close to the camera (detail must hold up).
- E is the one interaction key: use, pick up, carry, push, put down, switch lamps.
- Footsteps change by surface (carpet, wood, tile). Room tone, fridge hum, outdoor ambience, real house sounds (stuck lock, box thumps, ticking clock, breaker clunk).
- Walking pace is a calm indoor walk (set so the room-crossing times in section 6 hold).

## 14. The peripheral mechanic (must work)

- An anomaly object changes only when the player is NOT looking at it, and resolves after about 0.12 seconds of centred, direct focus (the fovea rule from the web build).
- Continuity rule: an anomaly never pops, flickers or glints while in view. Direct focus is always trustworthy. The centre of the screen always stays readable.
- Scripted house anomalies fire only in the periphery or out of line of sight, never on screen. Two exceptions Joel asked for by name: a hallway that visibly stretches while the player walks it, and the shadow that drifts out of place.

## 15. Unease

- One dial, 0 to 100 (shown as levels 0 to 10), drives the picture effects, the colour grade and the audio together.
- Level 0: bright, warm, bodycam only. Low levels: colours cool slightly, a little grain, faint chromatic edges, rare tracking lines. Middle: VHS present (scanlines, colour bleed, wobble, tracking rolls, tape hiss and warble). High: cold washed colour, heavy grain, chromatic split, dropouts, audio warps. Top: near-monochrome cold, crushed blacks, constant tape damage, muffled sound; use sparingly.
- Playability rule (overrides the early "edges blur" idea): the game must stay playable at every level. Objective readable, doors visible, way findable. Edge blur cut far back; the centre stays sharp. Intensity comes from tracking lines and rolling bars in bursts, colour bleed, chromatic splitting, brief glitches and stutters, wobble, shifting colour, crushed shadows, grain. The strongest effects arrive in pulses that pass, not as a constant wall.
- Effects fade in smoothly, never snap. They read as what Jack sees, not a TV overlay.
- Three presets for levels 8 to 10 (Subtle, Medium, Heavy) switchable in the F1 debug menu.
- Debug: number keys jump to levels, F1 opens the unease bar, the day / night key stays. An accessibility setting caps the effect intensity.

## 16. Story arc (draft; Joel will revise after playing)

- Day 1, Move-in (unease 0 to 1): the existing Day One. One subtle anomaly before sleep.
  1. Park; take the first box from the boot. 2. Carry it to the front door. 3. Unlock with Jack's old key; it sticks once. 4. Bring in both boxes. 5. Pick up the mail, put it on the kitchen counter. 6. Flip the breaker; lights hum on room by room. 7. Open a living room window. 8. Clean out the fridge; magnets and drawings stay. 9. Choose where to sleep: the parents' door opens but Jack will not go in ("Not yet."); it completes in his childhood room. 10. Lie down; one subtle peripheral anomaly, fade, title card.
  - The game opens with a short drive to the house (a cinematic), then Jack gets out and unloads.
- Day 2, Settling in (1 to 3): chores. Small anomalies while Jack is out of the room. First glimpse of the entity at the screen edge.
- Day 3, Things move (3 to 5): more anomalies, the first room-expansion sequence, the parents' bedroom door found open.
- Day 4, Losing grip (5 to 8): at least two Exit 8-style loops through the house. The entity is close in the periphery.
- Day 5, Facing it (8 to 10, then release): a harder loop. Jack enters the parents' room. The keepsake box, photo albums and home videos hold the final memories. One earned scare at the climax, then the house quiets and the colours return. Ending: Jack unpacks his two boxes and puts one of his own photos on the shelf next to theirs.
- Each night: bed, fade, a title card ("Day 2"), autosave.
- Each day has its own chore list drawn from the chore pool, spread across the house and yard.

## 17. The entity

- Jack's grief and depression given a shape. Never a predator, never kills.
- Appears only in the periphery. It watches, rearranges things, and grows more present as unease rises.
- Looking straight at it resolves it into something ordinary: a coat on a hook, a shadow, a chair.

## 18. Chores, anomalies and the low-stability sequences

- Chore pool (each uses E and has a short, physical action or loop): mow the back lawn with the push mower (the grass visibly changes); take out the trash and roll the bin to the curb; get the mail; do the dishes; run the laundry (washer, then dryer); water the garden bed; sweep the garage; change a burnt-out hall bulb; make the bed in Jack's room.
- Chores are where anomalies get noticed; the long walks between them give the house time to change.
- Anomaly pool (from the house's own objects): a family photo with one fewer person, or everyone facing away; the THANKFUL banner missing a letter; a fridge magnet moved, or a kid's drawing with an extra stick figure; the mantel clock running backward, or every clock showing the same time; a closed door now slightly open (the parents' especially); washed dishes back in the sink; a mown strip long again; the TV on to static or a paused home video; a dining chair pulled out; a light back on; a hallway slightly longer; two coats on the hook; the answering machine blinking with one new message; a height mark above Jack's last one; shoes by the door that were not there.
- Test mode (F5): one in-game day with the full chore list, anomalies fired at random out of sight. F6 shows the log of what fired and whether it was noticed.
- Room expansion: in set sequences a room slowly stretches: a hallway longer, a ceiling higher, a doorway further away.
- Exit 8-style loop: the player walks the same stretch of house again and again. Each pass may or may not hold one anomaly. Spot one: turn back. All normal: keep going. A wrong call resets the count; several right in a row breaks out.
- Never teleport the player back to the start. The house loops and morphs around him instead: a corridor that brings him back round, a hallway that stretches as he walks it.
- The player can never die. Mistakes only reset a loop.

## 19. Objectives, overlay and menus

- The game is objective-based. The current task shows as a small handwritten-style note (the inner voice), not a big HUD. As stability drops, the notes get vaguer and stranger.
- No floating waypoints: a faint warm glow marks the thing the note is about, and fades out at higher unease.
- Menus work with the mouse (hover, click, scroll), the keyboard and a controller. No input lag in menus; the head-turn lag applies only in play.
- Windowed mode never locks the mouse in a menu: Esc or pause releases the cursor so the window can be left, resized or made full screen; the mouse is recaptured only on returning to play.
- Title: Play, Settings, How to play, Quit, over a live look around the house.
- Pause menu: Resume, Settings, Chapter select (Days 1 to 5), Quit.
- Settings: Display (window mode, resolution, V-sync, frame rate cap, field of view); Graphics (overall preset Low to Epic, and shadows, global illumination, reflections, textures, effects, post-processing, anti-aliasing, upscaling / resolution scale); Audio (master, music, sound effects, ambience); Controls (mouse sensitivity, invert Y, key rebinding); Accessibility (camera motion intensity, unease effect intensity cap, subtitles). Settings save between launches.
- Autosave at the start of each day.

## 20. Music and sound

- Original instrumental music, no vocals. Quiet, sparse, melancholy piano and pads with long silences. Mood references: POOLS, The Exit 8, Boards of Canada. Subtle and emotional.
- Six tracks, each 2 to 3 minutes and loopable, one per named slot:
  1. `music_title`: a lonely upright piano melody, warm but sad, soft tape hiss.
  2. `music_day1_calm`: sparse piano and soft pads, nostalgic like a home video, long silences.
  3. `music_unease_low`: the same melody slightly detuned, a faint VHS warble.
  4. `music_unease_mid`: the melody breaking apart, wrong notes, a low drone, a distant music-box echo.
  5. `music_unease_high`: a barely-there melody, heavy tape warble, deep hum; unsettling but never loud or jump-scare-like.
  6. `music_loop_sequence`: a repetitive, hypnotic pattern, like walking the same hallway over and over.
- The music system crossfades between the slots by unease level. Any slot can be replaced with a real track later by dropping in a file of the same name.

## 21. Milestones and deliverables

1. Bug fixes: driveway tree, mouse menus, windowed cursor release, full settings menu.
2. House rebuild: bigger layout, all rooms, colour theme, floors, outside areas, realistic car.
3. Lighting, the unease presets and the playability fix.
4. Days 1 and 2 fully playable with chores and anomalies.
5. Days 3 to 5 with room expansion, loops, the entity and the ending.
6. Music system, polish pass, final package and `PLAYTEST_README.md`.

- Builds: a standalone Mac app (Apple Silicon) in `Builds/` that opens with a double-click.
- Screenshots: each room from 3 angles, day and night, in `screenshots/<room>`; plus the themed folders asked for along the way (`unease_stages`, `lighting_pass`, `drive_session`, `playtest_round1` before / after, `player_character`).
- `BUILD_STATE.md` carries a "How to play" note: controls, debug keys, and anything that did not make it in.

## 22. Playtest 2 update (Joel, Nov 12 2026)

Where this section conflicts with anything above, this section wins. It replaces parts of sections 5 (scale), 11 (camera feel), 13 (controls and interaction), 15 (unease), 16 (story), 18 (anomalies), 19 (objectives) and 20 (sound).

### 22.1 Space and scale (top priority)
- The house still feels cramped. Rebuild for generous, walkable space:
  - Interior doors 213 cm tall (7 ft) and 91 cm wide (36 in). Front door 97 cm wide.
  - Hallways at least 122 cm wide (4 ft). Main hallways 137 cm.
  - At least 90 cm of clear walking space around all furniture. In the living room the player can walk comfortably between the sofa, coffee table and TV.
  - Main rooms 20 to 30% bigger than they are now.
- Shrink or fix the player's collision so it never snags on door frames, furniture edges or trim.
- Walk-test every room and doorway. Log anywhere the player has to squeeze.

### 22.2 Camera: stabilized camcorder
- Replace the head bob with a stabilized-camcorder feel: smooth, floaty motion with gentle inertia and a subtle lag when turning. The weight of the movement is felt, but there is no up-and-down bounce.
- Soft sway on starting, stopping and turning. Tiny micro-jitter, like a camera held steadily by hand.
- Settings: Camera Motion (Off / Stabilized (default) / Handheld / Bodycam).

### 22.3 Doors and hardware
- Physics doors: hold E on the handle to grab it, then move the mouse to swing it open or closed. Walking into a partly open door pushes it further open. Doors never block or trap the player.
- Doors swing with real weight, creak and settle. Latches click shut.
- Hardware theme: polished brass round doorknobs on all interior doors (90s builder standard), a brass lever handleset on the front door, and brass hinges. Consistent everywhere.

### 22.4 Detail and imperfections (fix the "matured Roblox" look)
- Fix all z-fighting, flickering and clipping. Every knob, button, switch and decal sits slightly off its surface, with no overlapping faces. Check the kitchen stove, microwave, appliances and light switches first.
- Replace low-poly flat clutter (books, papers, mail) with proper models: books with page edges and slightly curled covers, papers that lie with small bends and shadows.
- Imperfections everywhere: scuffs on baseboards, dust in corners, smudges on glass, worn paint on door edges, crooked frames, curled rug corners, light-switch grime, small wall dings, water rings on tables, faded sun spots.
- Lighting: no flickering or popping light on small objects. Check shadows on tiny props.

### 22.5 Interactivity
- Almost everything can be interacted with: every drawer and cabinet opens, windows open, lights switch, faucets run, appliances turn on, small props can be picked up and inspected.
- Daily-life actions: sit on chairs and couches, make a simple meal (fridge, stove, plate), sit at the table and eat, wash the dish after.

### 22.6 Hidden stress system
- Jack has a hidden stress level. There is no meter on screen. The player reads it through the visuals, peripheral activity and sound.
- Stress rises from darkness, being alone too long, anomalies, entering the parents' room, and night.
- Ways to calm down: step outside for fresh air, sit on the porch or in the back yard, turn on lights, eat a meal, take a shower, play the radio or a CD, sit somewhere quiet, ride the bike around the block.
- High stress unlocks stress hallucinations beyond the subtle anomalies:
  - In the dark or out of focus, objects look like a person: a coat rack, a robe on a door, a hanging jacket, a tall lamp. At high stress they move a little: turning, stepping, leaning.
  - Figures standing in dark doorways or at the end of hallways.
  - Rule: the moment the player looks straight at one, it is an ordinary object again. Direct focus is still trustworthy.
- Avoid poltergeist-style tricks (taps turning on, things sliding) as the main scares. Use them sparingly.

### 22.7 Sound
- Anomalies and stress get sound: low whooshes, soft breaths, distant footsteps upstairs, a door clicking shut somewhere else, a muffled voice in another room.
- Day and night ambience: birds, distant traffic and lawn mowers by day; crickets, frogs, wind and the house settling at night.

### 22.8 Objective guide
- Replace the bottom-left box with Jack's handwritten notepad. Press a key (Tab) to raise it into view in his hand. A small pencil tick appears when a task is done.
- It updates live with what the player is doing and is never stuck on an old task.
- As stress rises the handwriting gets messier, and lines get crossed out or rewritten.
- Optional subtle waypoint: a faint glow on the target object, at low stress only, with a setting to turn it off.

### 22.9 Outside
- The outdoors is a breather: brighter, calmer sound, and stress slowly drops.
- Walkable neighbourhood: the full street block, neighbour houses, sidewalks, mailboxes, a small park or cul-de-sac at the end.
- A bike in the garage that the player can ride around the block.
- No free driving for now. The car is only used in cinematics.

### 22.10 Story update
- Jack is the last of his family. Everyone else died, and he does not remember what happened. The truth is only revealed at the end.
- The game opens on the drive to the house: Jack half-remembers something, with short flashes on the road.
- Flashbacks:
  - Triggered by specific objects, rooms or moments (a song on the radio, a photo, a smell like cooking).
  - The screen shifts smoothly into the memory: the same house, but warmer, brighter and furnished as it was years ago, with soft, out-of-focus family members who have no clear faces and muffled voices.
  - Each flashback reveals one small piece of what happened. They get longer and clearer as the game goes on.
  - Each one ends by snapping back to the present, with stress up slightly.
  - The final flashback, at the end, shows the full truth.
- The truth itself is a placeholder for now. Joel will decide it later.

### 22.11 Deliverables
- Rebuild and package a new playable build. Screenshots in `screenshots/playtest2_fixes`.
