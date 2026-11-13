# Requests

This is the inbox. Put what you want changed in the game here, in plain words, and the builder (a Claude model, currently
Fable) will pick it up at the start of its next working session.

You do not need to know Unreal or how the game is built. If you want background first, read
[`handbook/README.md`](../handbook/README.md).

## Two ways to send a request

**1. Open an issue.** Works for anyone with a GitHub account, no invitation needed.
[Start one here](https://github.com/ezekielgblount-sketch/peripheral/issues/new?labels=request&title=Request%3A+&body=%23%23+What+I+want%0A%0A%0A%23%23+Why%0A%0A%0A%23%23+How+I%27ll+know+it%27s+done%0A%0A%0A%23%23+Pictures+or+references%0A)
and make sure it has the `request` label. You can drag pictures straight into the issue.

**2. Add a file here.** For people with write access to the repo. Copy [`TEMPLATE.md`](TEMPLATE.md), name it
`YYYY-MM-DD-short-title.md` (for example `2026-11-14-attic-window-figure.md`), fill it in, and commit it to the
`poc/visual-slice` branch. You can do this on github.com: open this folder, "Add file" → "Create new file".

## What makes a good request

- **One thing per request.** Three ideas are three requests.
- **Say what you want to see or feel**, not how to build it. "The upstairs hall should feel longer at night" is better
  than "scale the hall mesh".
- **Say how you will know it is done.**
- **Add a picture or a reference** if you have one.
- Story, dialogue, notes Jack thinks, new things that change in the house, sounds, music notes, art direction, bugs,
  "this felt wrong when I played": all welcome.

### Example

> **Request: a figure at the attic window**
>
> **What I want:** From Day 3, when Jack is in the back yard, someone stands at the attic loft window. Gone the moment he
> looks straight at it.
>
> **Why:** The attic is the one place the house has not used yet.
>
> **How I'll know it's done:** I can stand by the shed, look at the garden, and catch it at the edge of the screen.
>
> **Pictures or references:** none

## What happens next

- The builder reads every open request at the start of a session and works through them, oldest first.
- When it finishes one it replies with what changed, what it could not do and why, and what it could not check. Issues
  are closed; files get a `## Result` section and move to [`done/`](done/). The change is listed in
  [`handbook/CHANGELOG.md`](../handbook/CHANGELOG.md).
- Requests that would change the heart of the game (the story premise, the not-looking mechanic, the camera feel) wait
  for Joel's yes. So do requests that disagree with something he already decided. The builder will say so on the request.

## Please do not

- Put passwords, keys, private photos or personal details in a request. This repo is public.
- Edit the game files directly unless you are set up to build it; send a request instead.
- Push to the `main` branch.
