# Current state

As of the evening of **November 12, 2026**. The builder updates this page whenever the state changes.
The detailed history, pass by pass, is `unreal/Peripheral_POC/BUILD_STATE.md`.

## What exists and works

- The whole house, inside and out: about 3,000 sq ft over two storeys, basement, attic loft, garage, yard, street with
  neighbour houses, an invented early-90s car. Each room has its own paint or wallpaper and floor.
- All five days of the story, start to end card, with nine chores, the corridor loops, the parents' room, the climax and
  the unpacking.
- Twenty-four out-of-sight changes, window and mirror figures, the tree-line figure, false-alarm shapes, fourteen-plus
  sounds from elsewhere with captions, light dips, the corridor ceiling that lifts.
- Body-cam camera motion, the lens, the ten-level unease look, day and night.
- Jack's body (the mannequin-based one), shadow, forearms and mirror reflection.
- Title, pause, chapter select, how to play, and a settings menu with six pages. Settings and progress save.
- Six music tracks and all sound effects.
- A packaged Mac app.

## How it has been tested

Almost entirely **by script in the editor's play mode**: the five-day story runs from Day 2 to the end card with no
blueprint errors, the fit check passes, and individual features were checked by reading the game's state and taking
pictures.

**Very little has been played by a person.** Things nobody has verified on screen in the packaged app: mouse clicks on
menu buttons, key rebinding, resolution changes, the in-game overlay (chore list, notes, captions), how the days feel at
walking pace, whether the changes on Days 2 to 4 get noticed, the music and sounds by ear, anything in motion.

A lesson from this: on Nov 12 Joel ran the app for a friend and there was **no menu**. When the menus were moved to real
widgets, the step that puts them on screen was never added, and script tests never needed the menu. The same bug hid the
in-game overlay. Fixed in commit `80eb5ef`; the rebuilt app is in place. Joel has not yet confirmed it on screen.
F5 on the title screen still starts a chore day without the menu.

## In progress (in the working copy, not yet committed)

These are being worked on now. Check `git status` and `git log` before assuming any of it is in the branch.

### The found-footage look

- Built: `M_Footage`, `M_FootageRes`, `BP_Footage` (autofocus), the Footage look settings page with a preset and six
  sliders, the seven new saved values. Lens distortion and dark corners strengthened.
- Preset pictures are in `screenshots/footage_look/`.
- Not done: testing the settings page and autofocus in play mode; measuring the frame cost of each layer; a new packaged
  app; updating the retired art rules in the old root documents.

### Realistic procedural materials

- Started: procedural wear added to the master material `M_Surface` (shade variation at three sizes, yellowed areas,
  stains that run downward, grime where walls meet a floor, scuffed patches on floors, uneven roughness), from noise in
  world space with no extra textures. Controlled by `WearAmount` and the existing `DirtAmount`.
- Not done: judging it in pictures, tuning, the detail normal, a cheaper "Low" variant, per-surface masters (wood,
  concrete, metal, fabric, tile), checking the cost.

### MetaHuman Jack

- Built: a MetaHuman character (`/Game/Jack/MH_Jack`) that is a white man, thin (waist about 79 cm, 180 cm tall), with a
  face blended from three of Epic's presets so it is not any one stock character, short dark brown hair, and a grey
  hoodie, dark jeans and off-white trainers taken from Epic's MetaHumans sample and recoloured.
- The game wiring exists: `BP_Body` can make his face, hair and clothes follow the animated body, and
  `build_shadow.py` can place him as the look-down body and the mirror body.
- **Set aside for the demo.** The level and `BP_Body` were put back to the old Jack so the demo app was safe. The
  MetaHuman version of `BP_Body`'s graph is in `Scripts/bp/body.dsl` and `gen_body.py`; re-running `gen_body.py` and the
  current `build_shadow.py` restores it.
- Known problems: looking down shows the hoodie and a hand but not his legs or shoes; he does not read as mid-twenties
  (Joel asked for younger, and nothing reachable by script steers age); the stubble does not appear; the mirrors, walking,
  crouching and carrying have not been checked; the shadow and forearms are still the old figure.
- The MetaHuman assets (`Content/Jack/MH`, about 300 MB) and Epic's sample content (`Content/MetaHumans`, 1.5 GB) are
  **not committed**. Epic's sample content should not be pushed to a public repo; rebuild or re-copy it locally.
- `Scripts/mh_post_build.py` must run after every MetaHuman build: it resets the hair colour and makes the two
  blueprint copies the game uses.

## Not started

- A room inside the house that stretches (only the corridor does).
- Re-tuning unease and colour across the five days.
- Smooth blending between Jack's animations (they switch at once).
- Family pictures with real staged photos (drawn stand-ins hang there now; faces stay blurry either way).
- A Windows build. Nothing has been run on Windows.
- A more realistic-looking house overall: the brief asks for ordinary real rooms in place of the simple-shapes look.
  Materials are the first step; the shapes themselves are still built from boxes and cylinders.

## Open questions for Joel

From the camcorder brief, not yet answered. The builder is using the defaults in brackets until told otherwise.

1. Minimum PC and frame rate to target? [the two machines in the materials brief: base M4 Max, RTX 3060 12 GB; 30 to 60 fps]
2. One fixed look, or presets and an Off setting? [presets, with Default as the intended look]
3. Does the look apply to menus and the pause screen? [yes; the filter sits over everything the camera draws]
4. How dark and how blurry should dark scenes be? [lifted blacks as built; not tuned against the flashlight scenes]
5. REC dot and timestamp, tape-hiss audio? [not built; the design bible says no recording overlay]
6. Does the one scare on Day 5 get special filter behaviour? [no]
7. What age should Jack look, and is the blended face acceptable? [mid-twenties; the current face does not get there]
8. Is the game called Peripheral or Isolation, and how do the older Isolation design documents and this build come
   together? [called Peripheral in the build; the Isolation documents are treated as history and a source of ideas]

## Where things are on Joel's Mac

- Repo: `~/Developer/peripheral`. Packaged app: `unreal/Peripheral_POC/Builds/Peripheral_Demo_live_menu.app`, opened by the
  Desktop shortcut "Play Peripheral".
- Engine: `/Users/Shared/Epic Games/UE_5.8`.
- Epic's MetaHumans sample project: `~/Documents/Unreal Projects/MetaHumans`.
