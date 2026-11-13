# The game and its story

The full, topic-by-topic design is `DESIGN_BIBLE.md` at the repo root. This page is the short version plus what has
actually been built. Where this page and the design bible differ on what is *wanted*, the design bible wins; where they
differ on what *exists*, this page and `05_CURRENT_STATE.md` are newer.

## Premise

- Peripheral is a first-person psychological horror game about grief. Quiet and emotional. No monsters that hunt, no
  combat, and the player can never die.
- **Jack** is in his mid-20s. His parents have died and he has inherited his childhood home. He arrives with two moving
  boxes and stays five days.
- The horror is the house breaking its own rules through ordinary, nostalgic objects. It has to feel like someone's real
  childhood home, not a horror set.
- The house sat empty only a few weeks. A mug in the sink, a jacket on the hook, drawings under fridge magnets.

## The one mechanic: peripheral vision

- Things change **only when the player is not looking at them**. Looking straight at something is always trustworthy.
- A changed object "resolves" after about a tenth of a second of direct, centred attention.
- Nothing pops, flickers or glints while it is in view. The centre of the screen always stays readable.
- Two exceptions Joel asked for by name: a hallway that visibly stretches while Jack walks it, and Jack's shadow drifting
  out of place.
- **Never teleport the player.** The house loops and morphs around him instead.

## Jack

- Mid-20s, about 178 cm, thin, worn down. White. Short messy dark brown hair, a few days of stubble, tired eyes.
- Faded grey hoodie, worn dark jeans, beat-up off-white trainers.
- The player sees his shadow, his body when looking down, his hands when carrying or using things, and a soft, hard-to-read
  reflection in mirrors. Faces stay unclear throughout the game.

## The entity

- Jack's grief and depression given a shape. It never chases and never kills.
- It appears only at the edge of vision: a figure at a window, in a mirror, in the tree line. It watches and rearranges.
- Looking straight at it turns it into something ordinary: a coat stand, a dust sheet over boxes, a dress form.

## The five days (as built)

A handwritten-style note at the bottom left says what Jack is thinking of doing next. From Day 2 a chore list sits in the
top right. A day ends when the player presses E at Jack's bed once the note says to. Each new day is saved as it starts.

1. **Move-in.** A short drive to the house, then: unload the car, get the power on, open a window, clear the fridge,
   choose where to sleep. The parents' door opens but Jack will not go in ("Not yet.").
2. **Settling in.** Make the bed, do the dishes, get the mail, run the laundry. Small things change while Jack is out of the
   room. A coat stand in the front hall is sometimes not a coat stand at the edge of the eye.
3. **Things move.** Mow, water the garden, change the hall bulb. Then the closet at the end of the upstairs hall is open
   and the hall behind it is longer than the house. Afterwards the parents' door stands open.
4. **Losing grip.** Take out the trash, sweep the garage. Then the closet corridor, twice: if something in the upstairs
   hall changed, go back the way you came; if nothing changed, keep going. Three right calls ends each one.
5. **Facing it.** One more corridor, five right calls. Then the parents' room: the keepsake box, the photo albums, the
   home-video tape on the old television. Then turn around (the one earned scare). Then the house quiets, the colour
   comes back, and Jack unpacks his two boxes.

A wrong call in a corridor only resets the count.

## Chores

Each uses the E key and a short physical action: mow the back lawn (the grass visibly changes), take out the trash and
roll the bin to the curb, get the mail, do the dishes, run the laundry, water the garden bed, sweep the garage, change a
burnt-out bulb, make the bed. Chores are where changes get noticed; the walks between them give the house time to change.

## What changes in the house

Twenty-four out-of-sight changes are built, plus figures and sounds. A few examples; the full list with file names is in
`unreal/Peripheral_POC/BUILD_STATE.md` under the three "anomaly pass" headings.

- A family photo with one fewer person. The THANKFUL banner missing a letter. Washed dishes back in the sink.
- An extra door upstairs. The SOLD sign's smile. The WELCOME HOME board under it gone blank.
- The mud room jacket hanging as if someone is in it. A kitchen chair pulled out to face the hall.
- Person-shaped things in dim corners that never change (a mop, a robe on a hook, coveralls on a nail). These are false
  alarms on purpose.
- Someone at Jack's bedroom window, seen from the yard, only when not looked at. Someone in the trees. Someone behind Jack
  in a mirror who is not in the room.
- Sounds from elsewhere in the house about once a minute: doorbell, phone, a knock, pipes, footsteps overhead, steps on
  gravel, a door closing. Now and then the lights dip.
- From Day 4, in the corridor behind the upstairs closets, the ceiling sometimes lifts as Jack walks out.

## Unease

One dial, 0 to 100, drives the picture, the colour and the sound together. It rises across the five days. At 0 the picture
is clean found footage. As it rises: tracking lines, colour bleed, wobble and glitches arrive in bursts that pass. The game
must stay playable at every level: the objective readable, doors visible. An accessibility setting caps the intensity.

## Music and sound

Six original instrumental tracks (sparse piano and pads, long silences), one per mood, crossfaded by unease. They were
written by code and have not been heard by a person. Any track can be replaced by dropping in a file of the same name in
`SourceArt/Audio`. Footsteps, room tone, a fridge hum, a ticking clock and the house sounds above are also made by code.

## Standing content rules

- Invented brands, titles and logos only. No copied artwork. No real faces; faces in photos stay blurry.
- No AI-generated character models or art assets. (MetaHuman, Epic's character tool, is allowed and is being used for Jack.)
- The house's objects never change with unease; only the picture, the sound and the scripted changes do.
