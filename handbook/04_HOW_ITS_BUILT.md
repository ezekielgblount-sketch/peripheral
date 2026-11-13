# How the project is put together

The team cannot do 3D art, so **everything is made by code**: meshes, textures, materials, lighting, sound, music,
blueprints and menus. Nothing was placed by hand in the editor. A Claude model drives Unreal through the editor's MCP
server and Python scripts. To change the game you change a script and re-run it.

All paths below are under `unreal/Peripheral_POC/`.

## The pieces

| Kind | Where | Notes |
|---|---|---|
| House layout | `Scripts/house_plan.py` → `HOUSE_BLUEPRINT.md` | Rooms, walls, doors, stairs as numbers |
| House shell | `Scripts/build_shell.py`, `build_openings.py`, `build_site.py`, `build_hood.py`, `build_annex.py` | Walls, floors, openings, yard, street, the corridor behind the upstairs closets |
| Mesh toolkit | `Scripts/meshkit.py` | Boxes, cylinders, tubes, soft shapes; every prop is built from these |
| Props | `Scripts/props_*.py`, registered in `dress_lib.py` | Furniture, small objects, the car, story objects, anomaly objects |
| Dressing | `Scripts/dress_f1.py`, `dress_f2.py`, `dress_out.py`, `dress_rooms.py` | Which prop goes where |
| Textures | `Scripts/tex/gen_surfaces*.py`, `gen_prints*.py`, `gen_video.py` | Written to `SourceArt/`, imported by `import_textures.py`, `build_prints.py` |
| Materials | `Scripts/build_materials.py` (master `M_Surface` + `MIL_*` instances), `build_car_materials.py` | World-aligned, so boxes need no UV work |
| Picture filters | `Scripts/build_bodycam.py`, `build_footage.py` | See `handbook/02_LOOK_AND_FEEL.md` |
| Sound and music | `Scripts/audio/gen_sounds*.py`, `compose_music.py`, `import_audio.py` | |
| Lighting, sky | `Scripts/build_env.py`, `daynight.py`, `timeofday.py`, `build_flicker.py` | |
| Blueprint logic | `Scripts/bp/*.dsl` (the graph, as text) and `Scripts/bp/gen_*.py` (creates the blueprint and writes the graph) | |
| Placement of logic actors | `Scripts/build_interactive.py`, `build_chores.py`, `build_day.py`, `build_anoms.py`, `build_anoms2.py`, `build_story.py`, `build_loop.py`, `build_mirror.py`, `build_shadow.py` | |
| Menus and overlay | `Scripts/ui_menu.py`, `ui_overlay.py`, `ui_tool.py`, `bp/gen_menu.py` | |
| Jack | `Scripts/build_jack.py` (current body), `mh_post_build.py` (MetaHuman, in progress) | |
| Tests and pictures | `Scripts/story_test.py`, `fit_check.py`, `pd.sh`, `pie_*.py`, `shot.py`, `take_*_shots.py` | |

Each script's opening comment says what it builds and what must run before it. Most are safe to re-run: they clear what
they placed (by tag) and place it again.

Known orderings: `build_anoms.py` → `build_anoms2.py` → `build_day.py`; `bp/gen_rise.py` before `build_annex.py`;
`bp/gen_body.py` before `build_shadow.py`; `bp/gen_footage.py` before `build_footage.py`; `build_bodycam.py` before
`build_footage.py` (both now keep each other's layers).

## Coordinates

- 1 Unreal unit = 1 cm. The scripts use "blueprint" centimetres, the same numbers as the house plan.
- Convert with `poc_lib.to_ue(x, y, z)` = `(x - 450, -(y - 1150), z)`.
- Floor heights: first floor 0, second floor 259, basement -252, ground outside -140. Second-floor ceiling 503.
- Rooms by name: `house_plan.room(name)` and `at(room, side, along, inset)` place things against a wall.

## The mesh toolkit (`meshkit.py`)

`box`, `obox` (rotated box), `cyl`, `tube`, `quad`, `soft` (a rounded box; it shrinks about 10 cm, so overlap pieces),
`cone`, `sphere`, `noise`. A prop is a function that adds shapes by material key. `PF.get(name, rebuild=True)` rebuilds
one mesh in place. Print materials are keyed `p_<name>`.

Placement helper in the dress scripts: `P(prop, x, y, z, face, room, collide, tags, movable)`, `hidden()` for things
that start hidden, `D.begin(tag)` to group what a script places.

## Blueprint logic as text

Blueprint graphs are written in a small Lisp-like text form (`.dsl` files) and sent to the editor with
`Scripts/bp_tool.py` (`B.create`, `B.add_var`, `B.add_obj_var`, `B.write`, `B.find`, `B.pins`). The editor's own notes
on the syntax are saved in `Saved/dsl_docs.md` when the tool is first used.

Lessons that cost time:

- A successful write returns `{"returnValue": null}`. Writing the overlay or menu graph often fails to parse the reply
  but still applies. Always compile and save afterwards:
  `unreal.BlueprintEditorLibrary.compile_blueprint(bp)` then `unreal.EditorAssetLibrary.save_loaded_asset(bp)`.
- `(bind x <pure getter>)` is re-evaluated every time `x` is used. To remember a previous value, store it in its own
  variable.
- A cast ends the flow unless written as `(bind v (Cast... :Object o) (:then ...) (:CastFailed))`.
- Blueprint variables that are not instance-editable cannot be set from Python during play.
- `B.pins(...)` adds a temporary node to the graph it probes; the next `B.write` replaces the graph.
- **Never rewrite `BP_HUD`'s graph.** It is very large; writing it drove the editor to 65 GB of memory twice.
- Big graph writes (the menu) take several minutes and freeze the editor while they run.
- Settings made on the parts of a *placed* blueprint actor do not reliably stick. Put them in the blueprint itself.
- A widget blueprint is not on screen until something creates it and adds it to the viewport. `BP_Front` does this at
  start for `WBP_Menu` and `WBP_Overlay`. (For a while nothing did, and the packaged game had no menu.)
- `Scripts/ui_menu.py` can only build the menu from nothing. To add to the existing menu use a small adder like
  `Scripts/ui_menu_add_footage.py`, then run `Scripts/bp/gen_menu.py apply`.

## The logic actors

One level, `POC_VisualSlice`. Logic lives in controller actors placed in it:

| Blueprint | Job |
|---|---|
| `BP_HUD` | "The director": game modes (title, drive in, play, loop, cut scenes), unease, fades. Do not rewrite its graph |
| `BP_Front` | Creates the menu and overlay, frees and captures the mouse, pause, title views, music crossfades, F5 and L test starts |
| `BP_Story` | The five days: phases, notes, day cards, saving progress, chapter select |
| `BP_Chores` | The nine chores |
| `BP_Day` | Out-of-sight changes: items tagged `dyN` appear and `dyNn` disappear when change N fires (24 so far) |
| `BP_Anomaly` | A peripheral object: unseen → seen → changed → resolved by direct look |
| `BP_Glimpse` | A figure that shows only while not looked at (windows, tree line) |
| `BP_OnlyMirror` | A figure drawn only by a mirror's camera |
| `BP_Paranoia` | Sounds from elsewhere and light dips |
| `BP_Loop`, `BP_Rise` | The corridor loop; the corridor ceiling that lifts |
| `BP_Mirror` | A camera behind the wall that films the room and Jack onto the glass |
| `BP_Body`, `BP_Arms`, `BP_Shadow` | Jack's visible body, forearms and shadow |
| `BP_Footage` | Camcorder autofocus for the footage filter |
| `BP_Switch`, `BP_Video`, `BP_Hint`, `BP_Passer`, `BP_Mover`, `BP_Trash`, `BP_World` | Lamps, the home-video tape, the hint glow, a figure crossing a doorway, moving parts, the bin, day/night |
| `BP_Player`, `BP_GameMode`, `BP_SaveSettings` | The pawn, game mode, the save class for settings and progress |
| `WBP_Menu`, `WBP_Overlay` | Menus; the chore list, clock, notes, day cards and captions |

Blueprints cannot easily read each other's variables through the text form, so they pass numbers through small hidden
"board" actors found by tag, using the actor's X, Y, Z as three numbers:

| Tag | X | Y | Z |
|---|---|---|---|
| `ub` | Menu screen showing (0 play, 1 title, 2 pause, 3 settings, 4 how to play, 5 chapters) | Button just pressed | Previous screen |
| `qb` | Day requested (1 to 5, 9 = continue) | | |
| `bb` | Camera motion intensity | Mouse sensitivity | |
| `sb` | Field of view | Invert Y (-1 or 1) | Unease cap |
| `cp` | | | Subtitles on |
| `lb` | Above 0.5 while the corridor loop is running | | |
| `cb` | The chore board | | |

Shared material values live in `MPC_World`: `Night`, `Unease`, `Motion`, `Frozen`, `Fade`, `Preset`, `Pulse`, and the
seven `Foot*` values.

Story tags: things tagged `ent`, `ent2`, `ent3`, `ent4` appear from that day on.

## Jack's body

- Today the game uses `SK_Jack`: a reshaped copy of Epic's mannequin, so it plays the engine's motion-captured walk, idle
  and crouch. Three copies follow the player (`BP_Body`, kinds 0, 1, 2): the one he sees looking down (no head), one that
  only casts his shadow, one only the mirrors see. `BP_Arms` shows his forearms while carrying, pushing or inspecting.
- MetaHuman Jack is in progress. See [05_CURRENT_STATE.md](05_CURRENT_STATE.md).

## Where to look for the why

`BUILD_STATE.md` records, section by section, what was built in each pass, how it was tested, what was not, and every
judgment call (numbered, about 90 of them) in plain English.
