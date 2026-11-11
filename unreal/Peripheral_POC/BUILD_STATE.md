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
