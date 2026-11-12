# Peripheral: playtest notes

## Start it

Double-click **Play Peripheral** on the Desktop, or open `unreal/Peripheral_POC/Builds/Peripheral_Demo_live_menu.app`.
The first launch pauses for about 15 seconds while it prepares shaders. It opens in a 1600 x 900 window; Settings can make it full screen.

## Menus

Mouse, keyboard (arrows and Enter) or a controller. Esc pauses and frees the mouse so you can leave, resize or full-screen the window; Resume takes the mouse back.

- **New game**: Day 1 from the drive in.
- **Continue**: the last day you reached. Each new day is saved as it starts.
- **Chapter select**: any of Days 1 to 5 (also on the pause menu).
- **Settings**: Display, Graphics, Audio, Controls (sensitivity, invert Y, key rebinding), Accessibility (camera motion, unease cap, subtitles). Kept between launches.
- **Test: chore day (F5)** and **Test: the loop (L)**: the two test modes from earlier rounds.

## Controls

| Key | Does |
|---|---|
| W A S D, mouse | Walk, look |
| E | Use, pick up, carry, push (mower, bin, broom), put down, switch a lamp |
| C | Crouch |
| F | Flashlight |
| Esc | Pause |

Walk, use, crouch and flashlight can be rebound in Settings.

## The five days

A handwritten-style note at the bottom left says what Jack is thinking of doing next. From Day 2 a chore list sits in the top right. End a day by pressing E at Jack's bed once the note says to.

1. **Move-in.** Unload the car, get the power on, open a window, clear the fridge, choose where to sleep.
2. **Settling in.** Make the bed, do the dishes, get the mail, run the laundry. Small things change while you are out of the room. A coat stand in the front hall is sometimes not a coat stand at the edge of your eye.
3. **Things move.** Mow, water the garden, change the hall bulb. Then the closet at the end of the upstairs hall is open, and the hall behind it is longer than the house. Afterwards the parents' door stands open.
4. **Losing grip.** Take out the trash, sweep the garage. Then the closet corridor, twice: if something in the upstairs hall changed, go back the way you came; if nothing changed, keep going. Three right calls ends each one.
5. **Facing it.** One more corridor, five right calls. Then the parents' room: the keepsake box, the albums, the tape. Then turn around. Then unpack.

Nothing can hurt Jack. A wrong call in a corridor only resets the count.

## Test keys

| Key | Does |
|---|---|
| 1 to 9, 0, minus | Unease level 1 to 10, and clean |
| F1 | Unease bar; left / right sets any value, up / down picks the Subtle / Medium / Heavy preset for levels 8 to 10 |
| F5 | Chore day test: the full chore list with random anomalies |
| F6 | During the F5 test: the list of what has changed, and whether you have looked at it since |
| N | Day / night |
| L | The loop test |
| H | Lets Jack's shadow stop copying him after one second of standing still |
| B, M | Head bob on / off; camera motion full / half / off |

## What to look for and tell me

- Does the house feel the right size now? Is any room still cramped, or any walk too long at the new walking pace?
- Colours: does any room still read as "all one yellow"?
- Do the menus behave with the mouse, and does Esc reliably give the mouse back?
- Chores: is any one fiddly or unclear?
- Did you notice the changes on Days 2 to 4 without being told?
- Jack now has a body: look down, watch his shadow in sunlight or lamplight, pick something up to see his hands, and stand at the big mirror in the living room or the parents' room. Does he read as a person? What looks wrong first?
- New this round, from your older anomaly lists. Tell me which land and which are too much:
  - Things shaped like a person in dim corners (a dust sheet over boxes, a mop, a coat on a chair). These never change.
  - From Day 3, in the back yard: someone at Jack's bedroom window, only when you are not looking at it. From Day 4: someone outside the living room window.
  - From Day 3, the big living room mirror, and from Day 4 the parents' room mirror: someone standing behind Jack who is not in the room.
  - Six more things that change while you are out of the room: an extra door upstairs, the SOLD sign's smile, the wedding photo, a kitchen cabinet, the kitchen tap, the half-bath door.
  - Sounds from somewhere else in the house every minute or so (doorbell, phone, a knock, pipes, footsteps overhead), and now and then the lights dip.
- Added after that (third pass), the last of your lists:
  - From Day 2, from Jack's bedroom window or the yard: someone standing in the trees behind the house.
  - From Day 3 the upstairs bathroom cabinet mirror, from Day 4 the half-bath one: a head and shoulders in the glass after you have looked away.
  - Three more out-of-sight changes: the mud room jacket hangs as if someone is in it, a kitchen chair is pulled out facing the hall, the WELCOME HOME board under the SOLD sign goes blank.
  - More person-shaped things: a dress form in the sewing room, robes on hooks in the upstairs bathrooms, coveralls on a nail in the basement, an ironing board with a shirt on it.
  - More sounds: steps on gravel outside, the porch boards, a door closing, a drip.
  - From Day 4, in the corridor behind the upstairs closets: on some trips the ceiling lifts as you walk out.
- Family snapshots now hang around the house. They are drawn stand-ins; your own photos (no faces) would replace them.
- Day 5: the tape now plays on the old television in the parents' room.
- The six music tracks were written by code and have not been heard by a person. They are in `unreal/Peripheral_POC/Music/` if you want to listen outside the game.

See `unreal/Peripheral_POC/BUILD_STATE.md` for what was tested by script, what was not tested at all, and every judgment call.
