# Decisions

Every decision Joel has made about the game, newest first. When instructions conflict, the newest one here wins. The
builder adds to the top whenever Joel decides something, quoting his words where there are any.

Older decisions, back to the first master prompt, are gathered by topic in `DESIGN_BIBLE.md`, and the judgment calls the
builder made on its own are numbered in `unreal/Peripheral_POC/BUILD_STATE.md`.

## November 12, 2026

**Share everything in the repo so others can build on it.** "Put everything, all the changes, all the stories,
information... in a place that I can easily share... so that a model of Claude from someone else's computer knows
everything that it needs to know about the game." People join the GitHub repo and add instructions and updates; the
builder (Fable) reads them and makes the changes. Result: this handbook and the `requests/` folder.

**The look is camcorder footage; realistic underneath, low-res on top.** "Like if they were filmed on a camcorder."
"I want the graphics to be realistic tho just low res." Main reference Freddys_House; from Your Happy Place only the
camera shake. Details in [02_LOOK_AND_FEEL.md](02_LOOK_AND_FEEL.md).

**The old art rules are retired.** The five-colour matte palette and the bans on bloom, grain, chromatic aberration,
motion blur, auto-exposure and extra post-processing no longer apply. (From the camcorder brief, decision 1.)

**Resolution is the player's choice.** Do not lock the render resolution. The low-res look comes from the filter.

**Footage look: presets Off, Light, Default, Heavy, plus sliders**, in Settings. Default should feel like found footage
out of the box. (The camcorder brief says "one look only, no preset menu"; the later pasted update asks for presets.
Presets were built, with Default as the one look. Joel can overrule.)

**Materials should look real, made procedurally.** No AI image generation. 1K textures by default, 2K at most. Must run
on a base M4 Max and an RTX 3060 12 GB. Start with a master wall and a master floor material. (The materials brief.)

**No AI-generated character models or art assets.**

**Jack is white.** "He's not Asian he's white." Epic's sample character Taro was tried and rejected for this reason.

**Jack is skinny.** "Skinny pls."

**Jack should look a little younger: mid-twenties.** "Looking good make him a little younger tho." Then: "Mid twenties."
Not achieved yet.

**Jack's face: the blended one.** Shown the earlier neutral face and a face blended from three presets, Joel chose "the
new face" (the blend).

**Keep working; do not stop to ask.** "Don't stop, period. Keep moving. Every time you hit a brick wall, move to the next
thing." Later: "Can you just keep going? Stop pausing for me, please." The builder picks the option it would recommend,
says what it picked, and carries on. It still asks before anything risky or hard to undo.

**The demo must work for a friend.** The title menu bug was fixed the same hour (see `05_CURRENT_STATE.md`).

## November 11, 2026

**Never teleport the player back to the start.** Loop and morph the level instead, and give each room distinct paint or
wallpaper.

**The bigger house layout is approved.** Rooms wider and longer, not taller; real ceiling heights.

**Colour theme locked:** "warm Americana family home, late 90s to 2000s". Painted walls, a different finish per room, white
trim. No Backrooms mono-yellow.

**Technology realism:** the parents' everyday tech is 10 to 15 years old (about 2010 to 2014); Jack's things are the
1998 to 2010 time capsule.

**Unease must stay playable at every level.** Colour is kept; effects come in bursts that pass.

**Go without MetaHuman first** (Joel was not at the computer to sign in). On Nov 12 he signed in and installed the
MetaHuman content, and MetaHuman Jack was started.

**Finish the full game:** "get to as close as you can to final production without me."

## Standing rules (not tied to a date)

- Do not change without asking: the peripheral mechanic, the story premise, the flashlight, the era mix, the camera feel.
- Invented brands and logos only. No copied artwork. No real faces; faces in photos stay blurry.
- The player can never die. The entity never hunts.
- `DESIGN_BIBLE.md` is changed only when Joel approves.
- On Joel's Mac: never move or focus his windows; never launch the packaged game while he is using it unless he asks;
  watch memory.
- Never commit secrets or the private reference photos.
