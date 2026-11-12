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
- "Didn't open anything" (Joel, launching from a terminal): the game was running but hidden. On macOS it waits to go full screen until it is the front app, and a launch that leaves another app in front never gets there. Fixes: the game now defaults to an ordinary 1600 x 900 window (`Config/DefaultGameUserSettings.ini`; the saved setting on this Mac was changed to match), and `Builds/` has two double-click launchers, `Play Peripheral.command` and `Play Peripheral (live menu).command`, which open the game windowed and in front. The builds made before this change still carry the old default, so use the launchers until the next package.
- Joel's first real run of the live-title build: it opened windowed and in front once launched with `-windowed`; "sensitivity is crazy fast". Settings now has three lines (up/down picks a line, left/right changes it): Camera motion, Graphics, and **Mouse speed** in five steps (0.25, 0.4, 0.6, 0.9, 1.3). Step 3 is the default and is half the old look speed. The same value drives the menu pointer. It lives on the settings blackboard actor (X camera motion, Y mouse speed, Z power stage). Not yet tried by hand at the new speed.
- "Why is there a tree in the driveway" (Joel): street trees are spaced along the verge at a fixed interval and one (Tree_09) landed in the mouth of the driveway, on the drive-in path. It was moved onto the grass beside the driveway, and `build_hood.py` now keeps street trees out of the driveway band. A desktop shortcut, `Play Peripheral.app`, opens the live-menu build windowed.

## Third feedback pass (Nov 11): no teleporting, a hallway that stretches, a finish per room
Joel: the loop "wasn't how I envisioned": no teleporting; the hallway should expand as the player crosses it; walking around should bring them back to the beginning with the house looping and morphing; the same wallpaper was used far too much; no input delay in the menus, only in play.

- **The loop no longer moves the player, ever.** The old loop (fade, snap back to the start of the downstairs hall) is gone. In its place is a corridor that should not exist (`build_annex.py`): it leaves the upstairs hall by the door at the end of the hall leg (locked on Day One), turns twice and comes back out of the parents' door ("not yet" on Day One). Walking on brings Jack back to where he started. It is built in the two unbuilt upstairs rooms and, once it stretches, runs out past the house's side wall. It is hidden with collision off until the loop starts; the side wall, the chimney (now its own actor) and one tree crown are hidden while it runs.
- **The hallway stretches in plain view.** The corridor's far wall and the divider between its two legs are moved by `BP_Loop` (`Scripts/bp/loop.dsl`). On a stretching pass the far wall keeps retreating as Jack walks toward it, from 1.8 m to as much as 10.8 m, uncovering more doors, pictures and ceiling lights, with a low groan and the tape effects held at their peak while it moves. Walls use the world-aligned material, so the paper does not smear as they grow. The first pass always stretches the full 9 m; later passes stretch 45% of the time by 3.8 to 9 m. The limit is the house next door (9.3 m away). This is the first time something changes while being looked at; logged as call 55, an exception to the not-in-view rule that Joel asked for by name.
- **The house morphs out of sight.** Half way round the corridor (neither door visible) both doors shut and the upstairs hall is changed for the next pass: a door that was never there, the family photo with the child gone, the school photo upside down, the clock running backward, a chair facing the wall, cold television light from Jack's room, or nothing (40%). Back in the hall and facing away, the corridor is put back to its short length.
- The rule is unchanged (something changed: go back the way you came; nothing changed: keep going; five right in a row ends it; a wrong call only resets the count). Going back means walking the corridor the other way round. The call is counted at the half-way point.
- The sequence starts at the front end of the upstairs hall, at night, with the end door standing open. `L`, the menu line and the end of the montage all start it. The director (`BP_HUD`) only starts it and waits; a second blackboard actor (tag `lb`) carries running / count / finished between the two Blueprints. `BP_Mover` gained `LoopKey`: a locked door with it set opens during the loop.
- **A finish per room** (call 56): living room keeps the damask; entry hall and stairwell are off-white paint; upstairs hall is a faded sage stripe paper; kitchen is a small blue-flower print; bathroom stays aqua paint; Jack's room is dusty blue paint. New texture sets `stripe` and `ditsy`. Pictures: `screenshots/walls/`.
- **Menu delay:** the menus now use the real mouse pointer (shown in the title, settings, how-to, pause and end screens, hidden in play) instead of a drawn pointer driven by mouse movement. The head-turn lag is untouched and applies only in play.
- Tested in editor play mode by script: the sequence starts with nobody moved after the first placement; the far wall retreats 0 to 900 as the test pawn walks in; the count goes up on right calls, resets on a wrong one, and five in a row reaches the end card; doors shut at the half-way point; the corridor is short again once back in the hall. Pictures: `screenshots/loop/`.
- **Not verified:** nothing here has been played by hand or seen in the packaged app (no test launches while Joel is at the machine). In particular the real mouse pointer and clicking in the menus, opening the two doors with E from inside the corridor, how the stretch feels at walking speed, and whether the corridor's lights are bright enough at unease 70 are untested.
- Known: the old downstairs loop props (banner, false door downstairs) are gone from the level; `banner_wrong` art is unused. The unbuilt rooms' floors are now carpet. `annex_preview.py` shows the corridor in the editor for pictures.

## Jack's shadow, and the shadow that stops copying him (Nov 11)
- Jack now has a shadow. `BP_Shadow` (`Scripts/bp/shadow.dsl`, `props_shadow.py`, `build_shadow.py`) keeps a plain 178 cm figure exactly where he stands. The figure is left out of the picture and only casts a shadow, so lamps and the sun throw a person-shaped shadow from first person. No figure while the camera is not Jack (title, drive in, cut scenes, pause).
- The anomaly: while the loop is running, if he stands still for four seconds the shadow stops copying him. Over about two seconds it turns 40 degrees, slides 28 cm to his right and lifts its right arm with its head tilted. The moment he takes a step it is his shadow again. `H` forces it anywhere after one second of standing still, for testing. Call 57: this one also happens in view, by design (Joel: "the shadow will move out of place, maybe if they stand still").
- Tested in editor play mode by script: no figure on the title screen; exact match while walking; loose after four still seconds in the loop; back within a frame of a step. Pictures (editor, night, upstairs hall light): `screenshots/shadow/`.
- Not verified: seen only in editor pictures, not played by hand or in the packaged app. The arm pose switches at once part-way through the drift rather than rising smoothly. The flashlight is at the camera, so it shows no shadow of Jack; lamps and sunlight do. The figure does not crouch or walk-cycle.

## Playtest round 1 (Nov 11): bigger house, colour theme, chores, anomaly test day, real menus
Joel's eight-point list after first playing the demo. The layout change was approved in that list.

### 1. House scale and layout
- The house is rebuilt from a room table: `Scripts/house_plan.py`. Walls, floors, ceilings, doors, windows, baseboards, the fit check and `HOUSE_BLUEPRINT.md` are all made from it (`build_shell.py`, `build_openings.py`, `fit_check.py`, `plan_doc.py`). Floor plans: `screenshots/playtest_round1/plans/`.
- Centre-hall two-storey with basement, attic loft and attached two-car garage. Clear floor inside the rooms on floors 1 and 2: 3,069 sq ft. Measured outside wall to outside wall those two floors are 3,421 sq ft.
- Floor 1: entry, hall, living room, dining room, kitchen with nook, laundry / mudroom, half bath, family room / den. Floor 2: upstairs hall (a gallery beside the stairwell, then a 10 m back hall round a corner), parents' bedroom with bath and closet, sibling's room, Jack's room, guest / sewing room, hall bath, two hall closets. A stair off the gallery climbs to the attic loft under the roof.
- The stair rules are kept: the sunken entry landing, up flight turning left, basement flight straight ahead, and the same flight to floor 2. Ceilings stay 244 cm; rooms grew wider and longer, not taller.
- Walking speed is now 135 cm/s (it was 260). At that pace the living room takes about 4 seconds to cross and Jack's room to the garage about 20.
- Lines of sight are broken by the L-shaped hall, the loop through dining room, den and kitchen, the stair core, and the corner in the upstairs hall.

### 2 and 3. Colour theme and floors ("warm Americana family home, late 90s to 2000s")
- Painted walls, white trim and white ceilings everywhere. Entry, halls and stairwell: warm greige, one treatment from the basement flight to the loft. Living room: antique white with honey oak trim. Den: tan with a deep burgundy accent wall behind the television. Kitchen and mudroom: butter cream and almond, with a fruit border under the kitchen ceiling. Parents: dusty sage. Jack: denim blue with a space border. Sibling: lavender. Half bath: powder blue. Hall bath: dusty rose with a matching shower curtain. Parents' bath: seafoam.
- Wallpaper in two rooms only: the cream damask in the dining room and a small floral in the guest / sewing room.
- Floors: honey oak in the entry, halls, living and dining rooms. Kitchen and mudroom: almond-and-brown sheet vinyl printed as tiles with small brown diamonds, scuffed. Bathrooms: small white hex tile and a 5 cm mosaic, both with dingy grout. Carpets: Jack's room a bold multicolour kids' pattern, parents' room mauve, den a dark burgundy and green multi-tone, sibling's room teal, guest room dusty blue, loft burnt orange, upstairs hall and stairs tan.
- New texture sets are made by `Scripts/tex/gen_surfaces2.py`.

### 4. Outside
- The driveway is clear concrete with cracks, a control joint and oil stains, leading to the two-car garage. Street trees are kept out of its mouth.
- Garage: workbench, pegboard of tools, second fridge, shelving, holiday decoration tubs, two bikes, ladder, gas can, paint cans, hose reel, the push mower, a broom, the wheeled bin. Its big door rolls up with E. A doorway in its back wall leads to the yard.
- Back yard: wood privacy fence, small shed, swing set, concrete patio with a gas grill, plastic chairs and table, a raised garden bed, sprinkler, hose. Neighbour houses show over the fence on three sides.

### 5. Chores (`BP_Chores`, logic in `Scripts/bp/gen_chores.py`, objects in `build_chores.py`)
All use E. A list of them shows in the corner during the chore day.
1. Mow the back lawn: E on the mower to push it; the long grass is cut short wherever it passes. Engine sound while pushing.
2. Trash: carry the kitchen bag to the wheeled bin in the garage (it drops in), then push the bin to the curb and let go.
3. Mail: E at the mailbox (the door drops, the flag goes up), carry the mail indoors.
4. Dishes: E at the sink, one plate per press, from the dirty stack to the rack.
5. Laundry: E at the washer (it runs and shakes for 18 seconds, then buzzes), E again to move the load to the dryer.
6. Water the garden: carry the watering can and stand at each of the three dry patches until it darkens.
7. Sweep the garage: E on the broom to push it through the eight piles of dust and leaves.
8. Hall bulb: carry the new bulb from the laundry shelf to under the dead hall fixture; the light comes on.
9. Make the bed in Jack's room: E at the bed.
- New in the player: things tagged `push` (mower, bin, broom) roll along the ground an arm's length ahead until E lets go.

### 6. Anomaly test day (F5, or "Play - Chore day" on the title menu) (`BP_Day`, `Scripts/bp/gen_day.py`, `build_day.py`)
- One in-game day, 8:00 to 18:00 over 20 real minutes, with the sun crossing the sky. It ends when every chore is done or the clock runs out.
- Every 35 to 75 seconds it tries to fire one anomaly picked at random. It fires only if that spot is out of the player's view: outside the field of view (with a margin) or behind a wall, and at least 2.5 m away. Nothing changes on screen.
- The fifteen in the pool: family photo (everyone now faces away), THANKFUL banner reads THANKFU, a fridge magnet slid down and the kid's drawing gained a tall figure, every clock shows 3:17, the parents' door is ajar, washed dishes are back in the sink, a strip of mown lawn is long again, the television is on to static, a dining chair is pulled out, a light that was off is on, the upstairs back hall is 80 cm longer, two coats on the rail instead of one, the answering machine blinks with a new message, a height mark above Jack's last one, shoes by the door.
- F6 shows the list of what has fired, in order, with the in-game time and whether the player has looked straight at it since.

### 7. Menus, input and settings
- The menus are now real widgets (`WBP_Menu`, layout in `Scripts/ui_menu.py`, logic in `Scripts/bp/gen_menu.py`). Mouse hover, click and wheel scroll work; so do the keyboard (arrows, Enter) and a controller. The earlier finding that "the editor exposes no menu tool" was wrong: its UMG toolset does this.
- Any menu frees the mouse: the pointer shows and is not locked to the window. Esc pauses and releases it; Resume (or Esc again) captures it again. The game no longer grabs the mouse at launch.
- Settings, five pages. Display: window mode, resolution, V-sync, frame rate cap, field of view. Graphics: overall preset and separate shadows, global illumination, reflections, textures, effects, post-processing, anti-aliasing, resolution scale. Audio: master, music, sound effects, ambience. Controls: mouse sensitivity, invert Y, seven rebindable keys. Accessibility: camera motion intensity, unease effect cap, subtitles (captions for the main sound cues).
- Settings are kept in a save file (`settings` slot) and applied at start-up.
- The in-game overlay (`WBP_Overlay`, `Scripts/ui_overlay.py`) draws the chore list, the clock, the F6 list and captions. On-screen text is no longer pre-made images.

### 8. Music
- Six named slots, each a looping file in `SourceArt/Audio`: `music_title`, `music_day1_calm`, `music_unease_low`, `music_unease_mid`, `music_unease_high`, `music_loop_sequence`. The director crossfades between them by unease level (under 15, 15 to 45, 45 to 75, above 75), with the title and the loop sequence on their own slots.
- The files there now are placeholder pads made by `Scripts/audio/gen_sounds2.py`. To use a real track, replace the WAV of the same name and run `Scripts/import_audio.py`.
- Sounds are sorted into classes (Music, SFX, Ambience) so the Audio sliders work.

### Judgment calls
58. Walking speed lowered to 135 cm/s. The size limit and the "4 to 6 seconds to cross a main room" target cannot both be met at the old 260 cm/s.
59. Clear floor area is inside the 2,800 to 3,200 range; outside-wall area is about 220 sq ft over it. Kept, because the complaint was that rooms felt cramped.
60. The split entry is kept, so floor 1 sits 140 cm above the yard. The garage is at ground level with steps up to the mudroom door, which makes the garage 3.8 m tall inside.
61. The parents' bath is seafoam (the brief names two bathroom colours and there are three bathrooms).
62. The fireplace moved to the living room's garage-side wall; its chimney rises through the garage.
63. "Fewer people in the family photo" is the peripheral anomaly from before (upstairs hall); the anomaly-day version of the photo is "everyone faces away".
64. Clocks cannot tick, so normally they show slightly different times and the anomaly sets them all to 3:17.
65. Mowing counts as done with up to two squares missed.
66. The chore day starts in the front hall when started from the title menu; started with F5 during play, Jack stays where he is.
67. Key rebinding covers walk, use, crouch and flashlight. The test keys (unease levels, F1, F5, F6, N, H, L) are fixed.
68. Subtitles caption sound cues, since the game has no speech.
69. The parents' room is open during the chore day and the loop; on Day One it still shows "Not yet."
70. The loop corridor now leaves by the two closets at the far end of the upstairs back hall and runs out through the side wall behind them.

## "Finish the full game" pass (Nov 11 to 12): design bible, music, front controller, five-day story
`DESIGN_BIBLE.md` at the repo root now holds every instruction from this session, by topic; it is the source of truth. `PLAYTEST_README.md` is the short how-to-play.

### What changed in how the game is put together
- **The director (`BP_HUD`) is no longer rewritten.** Its graph is very large, and writing it again through the editor's tools drove the editor to 65 GB of memory (it had also quit once earlier the same way). I stopped the editor both times; nothing of Joel's was lost. The director's asset was restored to its last good version and is now steered from outside by two small controllers. Section 7's list above ("menus are now real widgets") still holds; only where the logic lives changed.
- **`BP_Front`** (`Scripts/bp/gen_front.py`): the menu board and the mouse (any menu shows the pointer unlocked; play captures it), the title (a look round the new house), New game, the chore-day test, pause, quit, the six music slots crossfaded by unease, and the Accessibility cap. It switches the director's old keyboard title menu, old pause menu and old music off.
- **`BP_Story`** (`Scripts/bp/gen_story.py`, placed by `build_story.py`): the five days. It uses the director for fades and unease, `BP_Chores` for chores, `BP_Day` for out-of-sight anomalies and `BP_Loop` for the corridor.

### The five days as built
- Day 1 is the existing Day One, started from New game with the drive in. When Jack lies down, the story takes over: fade, a card ("Day 2 - Settling in"), autosave, and he wakes standing by his bed.
- Day 2: bed, dishes, mail, laundry. Day 3: mow, water, hall bulb; then the closet at the end of the upstairs hall opens onto the corridor that stretches (one pass); afterwards the parents' door stands open. Day 4: trash, sweep; then the corridor loop twice, three right calls each. Day 5: no chores; the corridor loop with five right calls; then the parents' room.
- Unease rises through each day (10 to 30, 30 to 50, 50 to 80, 80 to 100) and out-of-sight anomalies fire faster each day (every 70 to 120 seconds on day 2, down to 25 to 45 on day 5).
- The entity: six coat stands around the house (front hall from day 2; upstairs alcove and kitchen nook from day 3; Jack's room, dining room and the back hall from day 4). Each uses the peripheral rule: once it has been seen, it is a dark standing figure whenever it is off to the side or out of view, and a coat stand again the moment it is looked at directly.
- Day 5 ending: E at the keepsake box, the albums and the tape in the parents' room (each gives one line). Then, when Jack is facing away, the figure stands inside the bedroom door, and this once it does not turn into a coat when looked at. After about two seconds of being looked at it is gone, unease falls to zero and the colour comes back. Then: E at each of the two boxes (they open where they stand), E at the living room mantel (his photo appears beside theirs), fade, end card.
- Each day's start is saved (`progress` slot). Title: New game, Continue, Chapter select. Pause: Resume, Settings, Chapter select, How to play, Back to the title, Quit. Picking a day mid-game reloads the level and starts that day clean.
- The inner-voice note (bottom left) and the day card are drawn by the overlay widget. During a corridor loop the note also shows the rule and the count.

### Music
- Six original tracks composed in code (`Scripts/audio/compose_music.py`), 2 min 24 s to 2 min 56 s each, seamless loops: one piano melody treated six ways (alone with tape hiss; sparse with pads and long silences; flat and warbling; breaking up over a drone with a far music box; almost gone over a deep hum, kept quiet; a hypnotic eight-note cell with one note that changes every few passes). Listenable copies: `Music/*.m4a`.
- Nobody has listened to them. I can check length, loudness and loop seams by number, not whether they are good.

### Tested by script in editor play mode
- Title state; New game through the drive in to Day One; the hand-over when he lies down; Day 2 start by chapter select; every chore; days 2 to 5 with their loops; the three memories; the climax appearing and releasing; unpacking; the photo; the end card. No Blueprint runtime errors in the log.
- Fit check: ALL PASS, 52 routes, with furniture.

### Not done or not verified
- **Jack as a visible character is not built.** MetaHuman needs an Epic sign-in inside the editor to assemble a character, which I do not have; the only other human mesh on this Mac is Epic's test mannequin, which the brief rules out. The plain shadow figure from before is still what casts his shadow. No hands, no legs when looking down, no mirror reflection, no `screenshots/player_character`.
- Nothing in this pass has been played by a person or run as the packaged app: not the widgets on screen, mouse clicks on buttons, key rebinding, resolution changes, the save file, or how the days feel at walking pace. Script tests press "use" through a test hook and place the test pawn.
- Room expansion exists only as the stretching corridor (day 3 onward). No ceiling that rises, no other room that stretches.
- "Home videos" on day 5 is one tape and one line of text; nothing plays on a screen.
- Day One still uses the director's old spots: the warm hint glow for the fridge task and the last two tasks sits in the wrong place (the tasks themselves complete correctly in the new house).
- Day 1's own on-screen task notes are the earlier pre-made images; days 2 to 5 use the new text note.
- Unease levels and presets were not re-tuned in this pass (milestone 3 is the earlier lighting and preset work, unchanged).
- Daylight through the afternoon sun plus warm bulbs still pushes the greige halls toward yellow in the stills.
- Captions exist for the chore sounds only.

### Judgment calls
71. The director is steered from outside instead of rewritten (see above).
72. Chores are split by day so no chore repeats: 4, 3 and 2 across days 2 to 4, none on day 5.
73. "At least two loops on day 4" is the same corridor walked as two separate loops; day 5's "harder" loop needs five right calls instead of three.
74. The entity is a coat stand / standing figure pair using the existing peripheral rule, rather than a new system.
75. The one scare is the figure not resolving when looked at, held for about two seconds with a low groan, no loud sound.
76. The photo goes on the living room mantel beside a small family photo, not on a bookshelf.
77. Waking beside the bed each morning is the only time the story places the player.
78. The entity's coat stands are in the house from the start as ordinary furniture.
79. Jack's character is left out rather than built from the test mannequin.
