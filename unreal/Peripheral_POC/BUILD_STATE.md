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
