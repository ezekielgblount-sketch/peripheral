> Pasted by Joel on 2026-11-12, unchanged. Followed the same day by: "like if they were filmed on a camcorder" and
> "I want the graphics to be realistic tho just low res", which is why a tape-resolution control was added on top.

UPDATE — Found-footage look (replaces the earlier "low-res" update).
Reference games for the look: Your Happy Place and September 1999.

RESOLUTION IS THE PLAYER'S CHOICE
- Do NOT lock the internal render resolution. The game renders at whatever resolution the player picks in Settings, up to their screen's native resolution.

THE FOUND-FOOTAGE FILTER (a post-process layer on top)
- Camcorder softness: slight blur and detail loss, like footage from an old consumer camcorder, without actually lowering the resolution.
- Light compression artifacts, soft color bleed, mild sharpening halos on edges, gentle grain, slightly lifted blacks, and slightly blown-out highlights near windows and lamps.
- Depth of field with slow, hunting camcorder autofocus. Whatever the player looks at in the center ends up in focus.
- This stacks with the existing bodycam motion and the unease VHS effects. At unease 0 it should still read as found footage, just clean.

PLAYER CONTROL
- Settings menu, "Footage Look":
  - Preset: Off / Light / Default / Heavy.
  - Sliders for softness, grain, color bleed, compression and depth of field.
- The unease effects respect an accessibility cap, so players can tone everything down.
- Default should feel like found footage out of the box.

Save comparison screenshots of each preset in /screenshots/footage_look.
