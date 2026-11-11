# BUILD_STATE — Peripheral_POC (visual slice)

Plain-English running log. Newest entries at the bottom.

## Where things are

- Project: `unreal/Peripheral_POC/` on branch `poc/visual-slice`. Unreal 5.8.4, Blueprint and Python only, no C++.
- Target: macOS on Apple Silicon (Metal), 30 to 60 fps. Kept Windows-ready.
- Geometry source: `HOUSE_BLUEPRINT.md` v12 (the copy in Joel's `~/Isolation` project), with the fixes listed below.
- Screenshots: `unreal/Peripheral_POC/screenshots/<room>/`.

## How I drive the editor

- Unreal's built-in MCP server runs on `http://localhost:8000/mcp`. Client config is `.mcp.json` in the project folder. `Scripts/mcp.sh` calls it from the command line.
- `Scripts/uepy.py` runs Python inside the open editor. It drops a file in `Saved/PyInbox`, which `Content/Python/init_unreal.py` picks up. Unreal's own Python remote link would not connect over loopback on this Mac, so I used this instead.
- The editor is launched in the background so it never takes window focus.

## Conflicts between the old docs and the master prompt (prompt wins)

| Old doc says | Prompt says | What I did |
|---|---|---|
| Unity 6 with URP, baked lighting | Unreal 5.8, Lumen, Nanite, Virtual Shadow Maps | Unreal |
| Repo `CLAUDE.md`: no bloom, auto-exposure, motion blur, grain or chromatic aberration | Bodycam look needs all of them | Bodycam look, kept out of the screen center |
| Repo `CLAUDE.md`: roughness 1, no specular at all | Full PBR, glints allowed on normal objects | PBR. Anomaly objects keep identical shine in both states |
| Repo `CLAUDE.md`: no crouch | Walk, look, crouch | Crouch included |
| Repo `CLAUDE.md`: ask before pushing | Commit to GitHub after each room | Push only the `poc/visual-slice` branch |
| Repo `CLAUDE.md`: "Isolation" design, nothing ever fully clear | Direct focus is always trustworthy | Followed the prompt |
| Blueprint: ceiling 250, door 205 tall | Ceiling 244, door 203 tall | 244 and 203 |
| Blueprint: Windows target | macOS for now | macOS |
| Slice wants bedroom, hallway and bathroom | Blueprint has those on floor 2 | Built the floor-2 landing as the hallway, with Jack's bedroom and the full bath |

## Calls I made on my own

Joel said "you can take over" before answering the plan questions, so these are my calls. Each is easy to undo.

1. **Basement flight fixed.** The blueprint had it rising away from the landing with a floor slab 111 cm above its top step. It now descends straight ahead from the landing, and the floor above it is open with a railing. Same footprint.
2. **Stair to floor 2 reversed.** Its bottom step faced the drop over the entry landing and the floor-2 slab sat over its top steps. You now step on from the hall at the back and arrive upstairs above the entry. Floor-2 opening recut to match. The L-shape at the front door is unchanged.
3. **Bathroom widened** from 135 cm clear to about 230 cm by taking space from Bedroom B, which is only a closed door in this slice.
4. **Floor-to-floor is 259 cm**: 244 cm ceiling plus a 15 cm slab, climbed in 14 risers of 18.5 cm.
5. **Resolve behaviour copied from the web build**: an anomaly changes only when more than 40° off center or hidden, and snaps back in one frame after 0.12 s within 11° of center.
6. **Garage and driveway**: garage is a blockout. A sloped apron covers the 126 cm step the old log left open.
7. **Disk space**: I stop if free space drops below about 25 GB.

## Log

- Created the empty project, confirmed it loads headlessly with Lumen, Nanite and Virtual Shadow Maps switched on.
- Installed Git LFS. Set up and tested the MCP connection and the Python runner.
- Built the house shell from a script (`Scripts/build_shell.py`): walls, floors, three stair flights, both storeys. Placeholder flat-colour materials for now.
- Added sun, sky, clouds, volumetric fog and the base post-process volume (`Scripts/build_env.py`). Lumen lighting works on this Mac.
- Screenshots are taken through the editor viewport (`Scripts/shot.py`). Scene-capture cameras rendered without Lumen bounce light, so I dropped that route.
- **Fit check passes** (`Scripts/fit_check.py`): a 178 cm, 35 cm radius capsule clears the front door, landing, all three flights, both halls and every slice doorway.

## More calls I made on my own

8. **House is mirrored left-to-right from the blueprint numbers.** Unreal's Y axis points the opposite way to the blueprint's maths. Mirroring makes the up flight turn left as you walk in, away from the garage, which is what the prompt asks for. Seen from the street the garage is on the right.
9. **Garage sits at ground level** instead of a sloped apron. It is a closed blockout, and split-entry houses often have the garage on the lower level. This replaces call 6.
10. **Dining room wall moved 40 cm** so the top of the up flight has a 95 cm deep landing. The first version left 55 cm and failed the fit check. Dining is a closed door in this slice.
11. **Stair to floor 2 starts 110 cm short of the kitchen wall** so there is room to walk onto it. Its top three steps pass over the entry.
12. **Upstairs hall is a 120 cm gallery beside the stairwell plus a short leg to Jack's door**, not the blueprint's 6 m by 11 m open landing, which was not a believable hallway.
13. **Procedural textures instead of scanned ones.** Fab and Megascans need Joel's Epic login in the launcher, so I generate textures with code.
- Player Blueprint (`BP_Player`) built through the MCP Blueprint tools: WASD walk, mouse look, C to crouch, F for the flashlight, B to switch head bob off, M to cycle camera-motion intensity (full, half, off). Logic source is `Scripts/bp/player_tick.dsl`.
- Bodycam motion is in: head-turn lag, walk sway, a small dip on each step, idle drift, and an ease-out when you stop.
- Play-tested by script: the player spawns on the porch, walks through the front door onto the landing, the camera bobs, and crouch drops the capsule to 110 cm. Real keyboard and mouse input still needs a human to try it.
- Generated 23 tiling PBR texture sets with code (`Scripts/tex/gen_surfaces.py`): paint, popcorn ceiling, wood paneling, wallpapers, oak, shag, worn carpet, linoleum, bath tile, brick, siding and more. Imported them and rebuilt the master material so every wall and floor is textured at real-world scale.
- Screenshots now use the MCP `CaptureViewport` tool. The editor's own screenshot command stopped firing after play tests.
- Joel sent two style references (saved in `Reference/`): brick ground floor, white lap siding above with dark shutters, attached garage with its own lower roof, small porch by the door, picture window, mature trees, sidewalks and fences, warm low sun.

## Known problems to fix

- Interiors are too dark in daylight away from the windows. Needs exposure tuning and interior lamps.
- The shag carpet shows faint grid lines at its 50 cm tile repeat.
- The exterior is still a bare box: no garage, roof, porch, shutters, street or trees yet.

## Open question for Joel

The reference photo has the garage on the LEFT of the front door (seen from the street). The prompt says the up flight turns LEFT, away from the garage. Both cannot be true: with the garage on the left, turning left is toward it. Right now the house is built with the garage on the right and the flight turning left. Flipping it is a one-line change.

### Exterior and neighbourhood (Nov 10)
- Joel said the garage side "doesn't matter". Kept it as built: garage on the right seen from the street, up flight turns left (matches the written prompt).
- Added `Scripts/meshkit.py`: builds props and building parts from simple shapes into reusable meshes in `/Game/Meshes`.
- `Scripts/build_site.py`: gable roof, garage with its own lower roof and panel door, porch with posts, chimney, shutters, rear deck, lawn, driveway, walk, sidewalks, street.
- `Scripts/build_hood.py`: 4 neighbour house types placed 15 times, 145 trees from 3 tree meshes, shrubs, yard fences, swing set, utility poles.
- Call 14: trees are solid leafy shapes, not leaf-card trees. They read well through windows; up close they look simple.
- Call 15: no parked cars yet. A believable car is a large modelling job; left for after the rooms.
- Call 16: kit meshes are plain static meshes (Nanite off on them). Nanite stays enabled for the project; these meshes are too small to need it.
- Fixed the carpet and lawn grid lines (removed the low-frequency part of those textures).

### Rooms, interaction, light and sound (Nov 10, later)
**Controls:** WASD walk, mouse look, C crouch, F flashlight, E use (doors, kitchen drawer) or pick up and inspect (E again puts it back), B head bob on/off, M camera-motion intensity (full, half, off), N day/night, 1/2/3 graphics quality low/medium/high.

**Built**
- Windows with frames and dusty glass, 11 doors (4 open at start, 5 locked blockout rooms), casings, baseboards: `Scripts/build_openings.py`.
- 70 props in `Scripts/props_furniture.py` and `Scripts/props_small.py`; rooms furnished by `Scripts/dress_rooms.py` (101 placed).
- Printed images made by code (`Scripts/tex/gen_prints.py`): family photos with blank faces, posters, kid's drawing, box labels, rug, clock face.
- The one mechanic (`BP_Anomaly`, logic in `Scripts/bp/anomaly.dsl`): the family photo over the couch (the child is gone from it) and the tin robot on Jack's dresser (slides and turns). Each must first be seen for 0.6 s, changes only when more than 40 degrees off view centre or hidden, snaps back after 0.12 s within 11 degrees, then rests 60 to 120 s.
- Day/night, quality keys and room tone: `BP_World`. Lamps and glowing shades come on at night; hall, kitchen, bathroom and entry ceiling lights stay on by day.
- Bodycam lens (`Scripts/build_bodycam.py`): barrel distortion, soft edges with a sharp centre, colour fringing at edges only, shadow noise. No HUD.
- Sound, all synthesised (`Scripts/audio/gen_sounds.py`): footsteps for carpet, wood and tile picked from the floor material, room tone, fridge hum, outdoor air and birds, door creak, locked rattle, drawer, flashlight click.
- Screenshots: `screenshots/<room>/<room>_<1-3>_<day|night>.png` for entry, living_room, kitchen, hallway, upstairs_hall, bedroom, bathroom, exterior. Each has the 178 cm figure. Made by `Scripts/take_room_shots.py`.

**Tested by script in play mode:** player spawns on the porch; front door opens; drawer slides; both anomalies run through all four states; fit check ALL PASS with furniture in place.

**Not tested (needs a person at the keyboard):** real key and mouse input, the N / 1 / 2 / 3 keys, inspect rotation feel, how the sounds actually sound, frame rate.

**More calls I made**
- 17: Sun set to a real 45,000 lux and bulbs to real lumens, so exposure behaves like a camera. Windows blow out indoors by day, as on a real bodycam.
- 18: At night the sky light is switched off with the sun; outside is lit only by a dim moon and the windows.
- 19: Locked doors (dining, half bath, garage, two upstairs rooms) rattle and stay shut. Those rooms are blockout only.
- 20: Flashlight changed from an arbitrary brightness to 900 lumens. Colour and cone are unchanged.
- 21: Volumetric fog kept light (dust in sunbeams is faint). Stronger fog showed blocky artefacts indoors.

**Known problems**
- Printed photos and posters are flat, drawn shapes, not photographic.
- Cushions and trees look faceted up close.
- Daytime living-room ceiling picks up a green tint from the lawn.
- Some blotchy indirect light on walls (Lumen on Mac without hardware ray tracing).
- No parked cars, no street lamps, no basement or garage dressing (blockout by design).
- The editor screenshot tool needs a long settle after a day/night switch or the first picture keeps the old lighting.

### Look changed to "the home a 90s/2000s kid grew up in" (Nov 10, evening)
Joel's direction plus ten photos of a real home (kept in `Reference/private/`, not committed). This replaces the earlier 60s/70s dressing and overrides the "80s/90s dressing" line of the era mix; the house bones are unchanged.
- Living room: cream damask wallpaper, dark hardwood, oriental rug, butter-yellow sofa with quilt and floral pillow, red armchair, brass-and-glass coffee table, upright piano with bench, globe and piano lamp, brick fireplace with white mantel, fall decorations and THANKFUL banner, white built-in shelves with books and framed photos (blank faces), wall mirror, landscape prints, crown moulding.
- Kitchen: honey-maple cabinets and hutch with glass doors, white appliances, yellow walls, light tile floor, red floral valances, ceiling beams, glass pendant, microwave, cereal box.
- Hall: damask walls, dark hardwood, slant-front secretary desk, cordless phone.
- Upstairs: beige carpet, yellow bedroom walls, patchwork quilt, wood desk with glass top, red desk chair, beige CRT computer, cursive-alphabet and fractions charts, glow stars on the ceiling, backpack.
- Family photo now carries an orange '98 camera date stamp; school portraits have laser backdrops.
- Call 22: first pass went "90s pop" (teal and purple, lava lamp, bean bag, mini blinds). Joel's photos showed a traditional home instead, so those were removed. The props still exist in `Scripts/props_90s.py`.
- Call 23: no TV in the living room now (piano took the wall). The family photo anomaly moved to the left of the mirror over the sofa.
- New prop files: `Scripts/props_90s.py`, `Scripts/props_home.py` (114 props in total). Fit check ALL PASS. All 48 screenshots retaken.

### Lived-in pass (Nov 10, late)
Joel: the family that lived here could not get home to tidy up. Added `Scripts/props_lived.py` and a "Lived" block in `dress_rooms.py`:
- Fridge: grocery list, chore chart, phone numbers, a note from Mom, alphabet magnets. A second copy of Mom's note by the kitchen phone can be picked up and read.
- Kitchen: dishes by the sink and on the table, dish towel on the oven handle, mail and keys on the hutch, wall calendar with days crossed off that stop mid-month.
- Entry and hall: shoes kicked off by the door.
- Living room: magazine, mug and remote on the coffee table, clothes on the floor by the armchair.
- Jack's room: unmade bed, clothes on the floor, homework on the desk (can be picked up) and on the floor, teddy on the floor.
- Bathroom: towel on the floor, toothbrush cup, laundry basket.
- Call 24: kept a few moving boxes. If the family left suddenly, the boxes may no longer fit the story; Joel to decide.
- 130 props in total, 131 placed. Fit check ALL PASS. All 48 screenshots retaken.

## How to play (Peripheral_Demo)
Open `Builds/Peripheral_Demo.app` (double-click; the first launch pauses about 15 seconds while it prepares shaders), or open the project in Unreal and press Play.

**Title menu:** up/down and Enter. Play - Day One, Play - The Loop (test), Settings, How to play, Quit. In Settings: left/right changes camera motion (full, half, off), up/down changes graphics quality, Enter or Esc goes back.

**Pause:** Esc during play: Resume, Back to the title, Quit. (The world keeps running underneath; Jack just stands still.)

**Controls:** WASD walk, mouse look, C crouch, F flashlight, E use / lift and set down / pick up and inspect / switch any lamp or wall switch, L jump to the loop, B head bob on/off, M camera motion, N day/night.

**Opening:** after Enter, a short drive seen from the driver's seat: down the street and into the driveway. Then Jack is standing by the car.

**Day One** (a small handwritten note in the bottom-left corner shows the current task; a faint warm glow sits on the thing the note is about):
1. Lift the first box from the car boot (E), 2. carry it to the front door, 3. unlock the door (it sticks once, press E again), 4. bring both boxes inside, 5. carry the mail to the kitchen counter, 6. flip the breaker at the foot of the basement stairs (take the flashlight), 7. open the living room window (left pane), 8. open the fridge and clear out the four items, 9. go upstairs: the parents' door opens but shows "Not yet."; walk into Jack's room, 10. stand by the bed and press E to lie down. Fade to black, PERIPHERAL card.

**Time-skip montage** follows on its own: living room at level 5, kitchen at 7.5, Jack's room at 10, about 45 seconds each and walkable, then the loop.

**The loop** (also from the title menu, or L at any time): Jack stands at the top of the entry stairs. Walk the hall and into the living room, to the piano. If anything in the house is wrong, turn back and go down the entry stairs instead. Each pass may or may not have one thing wrong; the first pass never does. A right call adds one to the count in the corner, a wrong call sets it back to zero, five in a row ends the demo (end card, Enter returns to the title). Nothing can hurt Jack.

**Debug keys:** 1-9 = unease level 1-9, 0 = level 10, minus = clean. F1 shows the unease bar; hold left/right to set any value 0-100. N = day/night. With the F1 bar open, up/down switches the preset for levels 8-10: Subtle, Medium (default), Heavy.

## Tonight's design session (Nov 10-11): what changed
- **Story:** Jack arrives with two boxes in his car. The house was lived in until weeks ago: mail at the door, dishes, notes on the fridge.
- **Tech realism:** living room now has a small thick-bezel flat screen on an old oak entertainment centre, with DVD player, a 2010-era console, blinking router, cordless phone, laptop and tablet in the kitchen, chargers in outlets. Tapes and discs fill the cabinet. Jack's room keeps the beige CRT computer, handheld, glow stars and posters. No CRT remains in a shared room.
- **Reference rooms:** piano corner (A), seating with mirror and brackets (B), built-ins with photo shelf and keepsake box (C), fireplace with THANKFUL banner (D), secretary desk with map and barometer (E), hutch, beams, pendant and red valance (F), Jack's room with paneled walls, shiplap ceiling, glass-top desk, red chair, charts (G).
- **Palette:** honey-oak floors and cabinets, tan worn carpet, burgundy / hunter / navy accents, cream damask and warm walls.
- **Family photos:** posed portraits at very low resolution, warm print colour, orange date stamp, blank blurry faces.
- **Unease dial:** one value 0-100 drives picture and sound. After Joel's note it is colour-kept VHS and digital glitching seen from Jack's point of view (chromatic splitting, slipping blocks, tears, pixel patches), not grey and not a TV overlay. The centre of the screen always stays clear. Levels 1-10 = 10-100.
- **Sofa** rebuilt as one piece. **Daylight** softened (weaker sun, softer shadow edges, more sky fill).

## Calls made tonight
- 25: Menus are drawn directly on screen (the editor exposes no menu-design tool I can drive). Settings use arrow keys, and the F1 "slider" is a bar moved with left/right. No mouse-driven menus.
- 26: Graphics quality moved from keys 1/2/3 into Settings, because the number keys now set unease levels.
- 27: Joel asked for levels 1-10 after first asking for stages 0-4. Keys now follow the ten levels; the old stages are levels 2.5, 5, 7.5 and 10.
- 28: Sound can only be paused or pitched from the director, not filtered. So: tape hiss switches in from level 4, music warbles and slows from level 6, and a low muffled "underwater" bed comes in at level 9. Footsteps are not muffled.
- 29: "Frames freeze and skip" is done as vertical jumps and slipping blocks in the picture; the game itself never pauses.
- 30: The attic loft (G) is done as a restyle of Jack's existing room (paneling, flat shiplap ceiling). Steep slanted ceilings and a stair opening with spindles would change the house layout, which needs Joel's OK first.
- 31: The dining room (F) stays a locked blockout room; its hutch, beams, pendant and valance are in the eat-in end of the kitchen. No sliding patio door yet.
- 32: The breaker is at the foot of the basement stairs. The basement has no power until it is flipped, so the flashlight is needed.
- 33: The living room window "opens" by raising a sash in front of the fixed glass; the opening itself is not cut through.
- 34: The parents' room is an empty dark room behind an invisible barrier.
- 35: Lying down moves the camera onto the bed looking up at the glow stars; there is no body animation.
- 36: Trim stays white (as in the reference photos) although the palette note says honey-oak trim. Floors, cabinets and furniture are honey oak.
- 37: Still using a few items that pre-date the 2010 rule in shared rooms as "old collection" (VHS tape on the coffee table, wall phone with coiled cord).

## Did not make it in
- Mouse-driven menus and a true slider. Printer, inflatable chair, sticker-covered dresser, bunk bed, frosted shower door, second mantel look, thermostat detail, wire mail basket.
- Slanted attic ceilings and stair spindles (layout change), sliding patio door, dining room interior.
- Parked neighbour cars, street lamps. Fridge hum and LEDs do not wait for the breaker.
- Real key and mouse input has never been tested by a person. Every step was verified by script (objects moved and used by code), not by pressing keys.

## Late additions (car, drive-in, objectives)
- **Car:** an invented early-90s compact four-door (no real make), faded green, plain steel wheels, grey bumpers, boot open with both boxes. Simple interior: dashboard, steering wheel, seats.
- **Drive-in:** about 17 seconds from the driver's seat, engine sound, fade, door sound, then control. Look and movement are locked during the drive.
- **Objectives:** the handwritten note stays as the overlay. In the time-skip montage the note turns vague ("unpack. (did you unpack?)", "there was something you were going to do", "stay") and trembles slightly.
- **Waypoints:** no floating markers. A faint warm glow marks the current objective and switches off once unease passes level 5.5. Mockups of the alternatives are in `screenshots/overlay_explore/overlay_options.png`.
- **Screenshots:** `screenshots/unease_stages/` (levels 0-10 in the living room, plus morning / afternoon / golden hour / night at levels 0, 3, 6, 10, and kitchen and bedroom at 0, 5, 10) and `screenshots/drive_session/` (one folder per reference area, plus arrival and the parents' tech).
- Call 38: the opening drive is a fixed cinematic, not player-driven.
- Call 39: play-mode capture returns the editor camera, not the game view, so there are no true in-game frames of the drive or the note; the stills are editor views and the overlay sheet is a mockup.
- Call 40: packaged build verified by launching it in the background and reading its log (map loads, no errors). Not played by hand.
- Known: the car is blocky; wall mirror is a plain grey panel (real reflections were streaky); the room room-by-room `screenshots/<room>/` set from earlier is now out of date.

## First-look feedback pass (Nov 11)
**Car.** Rebuilt from scratch in `Scripts/props_car.py`. The body is a lofted skin with real curvature (crowned bonnet and boot, tumblehome, rolled shoulders, rounded corners in plan); wheel arches, cabin, boot and loading lip are cut out of it, and door, bonnet and fuel-flap shut lines are cut in as grooves. Glasshouse is a thin shell with glass between black rubber seals and a trimmed interior. 13-inch steel wheels with tyres that have a sidewall profile, wrap-round grey bumpers, flap door handles, mirrors, wipers, lamps, exhaust, aerial. Size: 426 long, 167 wide, 137 tall, 243 wheelbase.
- Wear is a purpose-built paint material (`Scripts/build_car_materials.py`): top panels sun-faded with patches of lost clear coat, road dirt low down and behind each wheel, light rust on the arch lips and sills, stone chips on the nose, and a parking dent in the left rear quarter scraped to primer.
- Checked against period photos of a 1990-91 Toyota Corolla sedan on Wikimedia Commons and its published size (2430 wheelbase, about 1655 wide, 1365 tall). Changes made after the check: silver steel wheels instead of dark, bumpers wrapped back to the wheel arches, rub strip carried onto the wings. The design stays invented: no badge, own lamp and grille shapes.
- Screenshots: `screenshots/car/`.

**Unease at high levels.** Shader rewritten (`Scripts/build_bodycam.py`).
- Edge blur cut from 2.6 to 1.1 and it no longer grows with unease. Nothing in the unease look blurs. Pixelated patches and colour-swapped blocks are gone.
- Intensity now comes from: tracking bands and a rolling bar, line tears, colour bleed (colour smears sideways, brightness detail stays sharp), red/blue splitting, a short frame hop with line doubling, picture wobble, a drifting colour cast, crushed shadows, heavier grain with colour noise, head-switching noise on the bottom lines.
- The strong effects arrive in bursts of 0.5 to 2 seconds every few seconds and pass; short stutters fall between them.
- Three presets for levels 8-10: Subtle, Medium, Heavy (F1, then up/down). Stills of all three at levels 8, 9, 10, between bursts and at the peak of one: `screenshots/unease_stages/presets/`.

**Interior lighting.** Every bulb now has a real colour temperature (`Scripts/dress_rooms.py`).
- Incandescent 2700 K throughout. Halogen torchiere in the living room (2950 K, thrown at the ceiling), standing between the two armchairs.
- Newer bulbs: a compact fluorescent in the bathroom (3500 K, faintly green) and one cooler replacement bulb (4000 K) in the kitchen fixture by the table.
- Shaded lamps (living room table, hall table) glow through the shade and throw a pool down onto the table and up onto the ceiling. The living room fan light and the bedroom ceiling light are dimmer, so rooms fall off into darker corners.
- The downstairs hall ceiling fixture flickers slightly (a faint shimmer with an occasional short dip).
- Day and night stills: `screenshots/lighting_pass/`.

### Judgment calls
41. Car body colour kept faded green; the tint was darkened in the new material so the faded top panels still read pale.
42. Boot stays open with a high loading lip between the tail lamps; the boxes sit where they did, so the drive-in and task 1 are unchanged.
43. A true frozen frame is not possible in this post-process step, so "frame stutter" is a two-frame hop with line doubling and a brightness dip.
44. Tracking bands are allowed to cross the centre of the view at reduced strength; every other burst effect is held back in the centre.
45. Colour-swapped blocks were removed after the first test stills: they read as stickers on the screen, which breaks the "this is what Jack sees" rule.
46. The flicker is on the light only; the glass globe of that fixture glows steadily.
47. The torchiere first stood by the hall door and failed the fit check, so it moved between the armchairs.

### Memory guard
The editor grew to 30 GB after nine hours of scripted rebuilds on a 36 GB Mac. `Scripts/mem_check.sh` prints its footprint and exits 1 above 12 GB; run it before screenshot batches, rebuilds and packaging, and restart the editor when it trips. Close the editor before packaging.

### Not verified
- Script reads of shader values during play return 0 for everything, so the preset switch is confirmed in the HUD (default Medium) but its effect on screen in the running game has not been seen. The "live bursts" state is the zero state, so bursts run even if a value is never written.
- All stills are editor views with the burst held; nobody has watched the bursts in motion or played with real keys.

## Second feedback pass (Nov 11): switchable lamps, the loop, game menu
**Every lamp is a real, switchable light.** New Blueprint `BP_Switch` (`Scripts/bp/switch.dsl`): press E on a wall switch or on a lamp itself.
- 12 switches: wall switches for entry, hall, living room fan light, kitchen, upstairs hall, bedroom, bathroom; and the lamps themselves: hall table lamp, living room table lamp, piano lamp, torchiere, Jack's desk lamp.
- Bulbs, shades and fixture globes glow only while their lamp is on (lit and unlit versions of each mesh), day or night.
- Nothing lights before the breaker is flipped. Ceiling fixtures start "on", so they come alive room by room when the power returns; table lamps start off.
- New fixtures: halogen track (three heads, 3000 K) over the kitchen counter and a lit brass sconce by the kitchen table, both on the kitchen switch.
- The N key now only changes the sky; it no longer turns lamps on.

**The loop** (prototype of the low-stability sequences). Set-up in `Scripts/build_loop.py`, logic in the director (`Scripts/bp/hud.dsl`, mode 6). Runs at unease level 7.
Six things can be wrong, all made from the house's own objects:
1. a door on the blank stair wall of the hall that was never there
2. the family photo by the piano with the child gone
3. the THANKFUL banner spelled THANFKUL
4. the hall clock's second hand running backward (and fast)
5. the chair by the piano pulled out and turned to face the wall
6. the television on, showing nothing
Changes are made while the screen is black between passes, never in view. The three peripheral anomalies from before are switched off during the loop so they cannot give a false alarm.

**Game menu.** Title menu, pause menu and a How to play page, all keyboard-driven and drawn by the director.

### Judgment calls
48. "Prototype one": the Exit-8 style loop is the one built. Room expansion (a hallway that gets longer, a ceiling that rises) is not built: the house shell is fixed geometry, and stretching it needs a second, movable copy of the hall. It is the next step for this mechanic.
49. The loop uses the real hall and living room rather than a copy; each pass ends in a quick fade and Jack is put back at the start.
50. "Turn back" is going down the entry stairs; "keep going" is reaching the piano. Both are places you already know from Day One.
51. A hall clock was added for the loop (it stays in the house in every mode; its second hand only moves during the loop).
52. Pause does not freeze time: the montage timers keep counting while the pause menu is open.
53. Menus are keyboard only (no mouse pointer yet).
54. Table lamps start off and stay off at night until the player turns them on.

### Build notes
- Run order after re-dressing: `dress_rooms.py`, `build_interactive.py`, then `build_loop.py` (it tags things the first two rebuild).
- Writing the director graph now takes several minutes (it is about 400 lines); use `MCP_TIMEOUT=900`.
- In the graph language a named value is worked out again every time it is used. Reading one after changing the variable it came from gives the new value (this ended the loop one pass early until fixed).
- Fixed along the way: the THANKFUL banner had never shown its letters (the print helper cropped wide images to their top strip). It is now a separate banner hung on the mantel, placed by `build_loop.py`; `Kit.print_quad` is the helper for wide prints. The family photo by the piano also overlapped the landscape above it; it moved to the wall above the spindle chair.
- Stills: `screenshots/loop/` (each anomaly), `screenshots/lighting_pass/` (retaken with the track lights and lit fixtures).
- Not verified by a person: the menus and the loop were driven by script in play mode (five right calls end it, a wrong call resets the count, L works from Day One, lamps toggle, power comes up in stages). Nobody has pressed real keys, and the drawn menu text has not been seen on screen.
- Fixed a latent fault found by the fit check after an editor restart: props placed as walk-through (shoes, the card binder, wall items) lost that setting when the level was reloaded, so in earlier packaged builds shoes could block the top of the entry stairs and the binder the bedroom door. Placement now uses the NoCollision profile, which is saved. Exterior walk-through props built by other scripts keep the old setting until those scripts are re-run.
- Kitchen floor changed from tile to wood at Joel's request: it now uses the hall's oak boards, so footsteps there are the wood sound. Stills: `screenshots/kitchen/wood_floor*.png`. Older kitchen stills in other folders still show tile.
- First hands-on run (Joel): the title showed but no menu. Cause: the HUD's built-in text font is not available in the packaged game, so every drawn line of text was invisible (it only worked in the editor). All menu and on-screen text is now pre-made images (`ui_menu_*`, `ui_pause_*`, `ui_howto`, `ui_settings_*`, `ui_loop_*`, `ui_preset_*`, made in `tex/gen_prints.py`, held in the director's `UI` array). The task note and "Not yet." are now sized to the screen height instead of fixed pixels, so they are no longer tiny on a high-resolution display.
- Real in-game frames are now possible without taking over the screen: launch the app with `open -g ... --args -windowed -ResX=1280 -ResY=720` and capture its window by id with `screencapture -l`. A background launch without `-windowed` waits forever for full screen. First real frame: `screenshots/menu/title_menu_in_game.png`.

## Title screen as a first impression (Nov 11)
- The title is now a live look around the house behind the logo and menu: living room, kitchen, hall, Jack's room and the car outside, about ten seconds each with a slow drift and a quick fade between them, at unease level 2 for a hint of the look. Settings and How to play sit over the same live view, dimmed.
- Menu works with the mouse as well as the keys: a drawn pointer follows the mouse, hovering highlights a line, clicking chooses it. Moving through the menu makes a soft click.
- Art: logo with red and cyan edges, a dark band behind the text, pointer (`ui_logo`, `ui_grad`, `ui_cursor`).
- Real frames from the packaged app: `screenshots/menu/live_title_in_game_*.png` (taken before the dark band was strengthened and its edge seam removed).
- **Crash seen once:** the packaged build with the live title crashed about a minute in, inside the engine's scene-culling pass (crash report 2026-11-11 10:55). A second run did not crash. That pass is now switched off (`r.SceneCulling=0` in `Config/DefaultEngine.ini`); it is only an optimisation. Not re-tested after the change.
- **Kept separate until it is tested:** `Builds/Peripheral_Demo_live_menu.app` has the live title. `Builds/Peripheral_Demo.app` is still the previous build (plain black title with the working menu).
- Launching the packaged game for a check takes over the mouse even in a background window, so no further real-app checks were run while Joel was at the machine.
- The pointer starts in the top-left corner until the mouse first moves.
