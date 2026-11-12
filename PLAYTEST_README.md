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
| H | Lets the shadow drift loose after one second of standing still |
| B, M | Head bob on / off; camera motion full / half / off |

## What to look for and tell me

- Does the house feel the right size now? Is any room still cramped, or any walk too long at the new walking pace?
- Colours: does any room still read as "all one yellow"?
- Do the menus behave with the mouse, and does Esc reliably give the mouse back?
- Chores: is any one fiddly or unclear?
- Did you notice the changes on Days 2 to 4 without being told?
- The six music tracks were written by code and have not been heard by a person. They are in `unreal/Peripheral_POC/Music/` if you want to listen outside the game.

See `unreal/Peripheral_POC/BUILD_STATE.md` for what was tested by script, what was not tested at all, and every judgment call.
