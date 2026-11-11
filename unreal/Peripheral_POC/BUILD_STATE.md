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
