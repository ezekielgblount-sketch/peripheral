# Peripheral: the handbook

Start here. This folder tells a person, or a Claude model on someone else's computer, everything needed to understand the
game and keep building it. It also explains how to ask for a change so the builder picks it up.

**The game in two sentences.** Peripheral is a first-person psychological horror game about grief. Jack, in his mid-20s,
moves back into his late parents' house for five days, and the house quietly changes whenever he is not looking at it.

**Where the game lives.** This repo, branch `poc/visual-slice`, folder `unreal/Peripheral_POC` (Unreal Engine 5.8, Mac
first). The `main` branch holds the older browser prototype; it is not the current game.

## Read in this order

| File | What it holds |
|---|---|
| [01_GAME_AND_STORY.md](01_GAME_AND_STORY.md) | Premise, Jack, the five days, the entity, anomalies, chores, the ending |
| [02_LOOK_AND_FEEL.md](02_LOOK_AND_FEEL.md) | The camcorder / found-footage look, the house's style, lighting, the exact filter values |
| [03_PROJECT_SETUP.md](03_PROJECT_SETUP.md) | Engine version, plugins, every project setting, how to open, run, test and package it |
| [04_HOW_ITS_BUILT.md](04_HOW_ITS_BUILT.md) | How the project is put together: scripts, blueprints, the coordinate system, the lessons learned |
| [05_CURRENT_STATE.md](05_CURRENT_STATE.md) | What works today, what is half-finished, what has never been checked by a person, what is next |
| [06_DECISIONS.md](06_DECISIONS.md) | Every decision Joel has made, dated, newest first. When two instructions conflict, this settles it |
| [FOR_THE_BUILDER.md](FOR_THE_BUILDER.md) | Standing instructions for the Claude model that builds the game (currently Fable) |
| [CHANGELOG.md](CHANGELOG.md) | What changed, and which request it answered |
| [briefs/](briefs/) | The original briefs Joel handed over (one sentence removed from one of them for the public repo) |

The deeper source documents stay where they are and are linked from the pages above:

- `DESIGN_BIBLE.md` (repo root): the full design, by topic. Changed only when Joel approves.
- `unreal/Peripheral_POC/BUILD_STATE.md`: the running build log, with every judgment call and what was and was not tested.
- `HOUSE_BLUEPRINT.md`: the house layout, room by room, generated from `Scripts/house_plan.py`.
- `PLAYTEST_README.md`: how to play the current build and what to look for.

Older root documents (`CLAUDE.md` below its top box, `VISUAL_REFERENCE.md`, `HOUSE_ENVIRONMENT_SPEC.md`,
`MASTER_VISUAL_ENVIRONMENT_BRIEF.md`, `PERIPHERAL_UNREAL_HANDOFF.md`, `FEATURE_LIST.md`, `DAY3_FINAL_ACT_SPEC.md`,
`NEXT_TASKS.md`, `AUDIT_REPORT.md`, `AGENT_LOG.md`) describe the earlier team design, "Isolation", built in
`unreal/Isolation` (last changed August 2026), and the browser prototype. They are still worth reading for ideas: many of
the things that change in the house came from them. The Unreal build described here follows `DESIGN_BIBLE.md` and this
handbook, and their art rules were retired on 2026-11-12 (see [06_DECISIONS.md](06_DECISIONS.md)).

**A naming note.** Those documents say "Isolation supersedes Peripheral", and one of Joel's briefs calls the game
"Isolation (formerly Peripheral)". This build is still called Peripheral in its files and menus. Which name the game
ships under, and how the Isolation design and this build come together, is an open question for the team. It is listed
in [05_CURRENT_STATE.md](05_CURRENT_STATE.md).

## How to ask for a change

You do not need to know Unreal. Write what you want in plain words. Two ways:

1. **Open an issue** (easiest, works for anyone with a GitHub account):
   [new request](https://github.com/ezekielgblount-sketch/peripheral/issues/new?labels=request&title=Request%3A+&body=%23%23+What+I+want%0A%0A%0A%23%23+Why%0A%0A%0A%23%23+How+I%27ll+know+it%27s+done%0A%0A%0A%23%23+Pictures+or+references%0A).
   Give it the `request` label if the link did not.
2. **Add a file** to [`requests/`](../requests/) (for people who have been given write access). Copy
   `requests/TEMPLATE.md`, fill it in, commit it to `poc/visual-slice`.

Story notes, new anomalies, art direction, bug reports and "this felt wrong when I played" all go the same way.
[`requests/README.md`](../requests/README.md) has the details and an example.

## What happens to a request

At the start of every working session the builder pulls the repo, reads the open requests, and works through them.
For each one it writes back what it did, what it could not do and why, and what it could not check. Finished requests are
closed (issues) or moved to `requests/done/` (files), and the change is recorded in [CHANGELOG.md](CHANGELOG.md).

Anything that would change the story premise, the peripheral mechanic, the flashlight, the era mix or the camera feel is
checked with Joel first. So is anything that conflicts with an earlier decision.

## Who decides

Joel has the final say on the game. Ezekiel owns this GitHub repo and can add people to it. If two requests disagree, the
builder asks Joel.
