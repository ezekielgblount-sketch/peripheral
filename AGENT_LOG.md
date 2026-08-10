# Agent Log

Running record of what Claude did in each work session, in reverse-chronological
order (newest first). Written so either human can read a session's entry, look at
the diff, and decide whether to push — without needing to have watched the stream.

Convention: Claude commits locally with a clear message. **Pushing is a separate,
human decision** — read the entry below, check `git log` / `git diff`, then push
if it looks right.

---

## Session — 2026-08-10 (DESIGN.md conflicts ratified — PR, not pushed to main)

**Did:**
- Walked the director through all 10 flagged `DESIGN.md` conflicts in chat,
  item by item. All 10 were ruled on across two messages; workflow item #8
  was ruled first and changes everything after it — **PRs from here on,
  nothing direct to `main`.**
- Updated `DESIGN.md`: replaced the "flagged, not resolved" conflict section
  with a "Ratified decisions" section reflecting the rulings, kept the
  original pasted document below (now clearly marked as historical/
  superseded where the two disagree).
- Notable scope changes from the rulings, not just conflict resolutions:
  flashlight gets a battery + low-battery flicker; no autonomous music, only
  a new music-box prop; the breaker flip is no longer the ending — a
  multi-night structure adapted from the Isolation feature list's Day 1-3
  timeline is now in scope; the house grows from one small single storey to
  3 floors + attic + basement + garage + 2 extra rooms; a small combinable
  pocket inventory plus a separate unlimited "Clues" tab, both previously
  ruled out; a stamina bar scoped to one night-3 chase scene only; palette
  switches to `VISUAL_REFERENCE.md`'s five colors with the flashlight kept
  warm as a deliberate one-line exception.
- **Flagged one live reversal within the rulings themselves**, not silently
  absorbed: item #10 was first ruled "keep Isolation separate, its own repo,
  later" and then reversed two messages later to "this is basically a new
  game, get that in the door and use the timeline." Both the reversal and
  the new ruling are recorded in `DESIGN.md`.
- **Left three items explicitly open, defaulted but not confirmed** (also
  listed in `DESIGN.md`): exact inventory pocket count (defaulted 2x2=4),
  whether the 0.3 key/lock-the-door epilogue survives inside the new
  timeline, and — the one that matters most — whether "basically a new game"
  pulls in Isolation's narrative content (a named protagonist, the
  lawyer/prologue, the phone plot) or just its structural shape on top of
  Peripheral's existing anonymous-player fiction. Defaulted to
  structure-only since retiring the anonymous-player conceit is a bigger
  call than was explicitly made.
- Did not touch game code. Design-doc and process changes only.

**Pushed:** no — per the newly-ratified #8, this is a branch
(`decisions/consolidated-rulings`) with a PR open against `main` for the
director's approval, not a direct push.

**Next:** the three open items above, especially the identity/narrative-scope
one, before any of this gets implemented — several of the ratified items
(inventory UI, the bigger house, the multi-night loop, the combine mechanic)
are substantial builds that would need to be redone if that question lands
differently than the default assumed here.

---

## Session — 2026-08-09 (DESIGN.md — consolidated spec)

**Did:**
- Saved a user-supplied consolidated feature list as `DESIGN.md` at repo
  root, per instruction: "the single source of truth... Claude Code reads it
  as context on every run." Content preserved verbatim below a flagged-
  conflicts preamble, same pattern as `VISUAL_REFERENCE.md`.
- Compared it against the shipped build (not just the other docs) since this
  one explicitly claims superseding authority — a doc that's wrong about
  what's already running is worse than one that's silent about it.
- Found 10 issues, flagged at the top of the file, not resolved. Highlights:
  1. Revision 0.3's status is ambiguous — not listed among what's
     superseded, but the doc's own Act 2 section describes a 22° flashlight
     and a breaker-flip-ends-the-game ending, both of which 0.3 changed *at
     this user's explicit request earlier in this conversation* (the wide
     flashlight fix, and the key/lock epilogue). Also silent on all-doors-
     interactable and the shower's water/curtain FX.
  2. Two contradictions **within the pasted document itself**: §1 says ~20
     minutes, §12 says ~8 minutes; §13 says "no music tied to events," §8
     prescribes a 3-second anomaly-timing silence window four lines away.
  3. The anomaly roster (§4.5, capped at "eleven total") drops 3 currently-
     shipped anomalies and adds 2 new ones, while converting four
     furniture-only anomalies into full-figure appearances — a rhythm
     change (~40% -> 80%+ figure reveals), not a wording pass.
  4. Bed-gating behind four chores reverses the "never gate the bed" rule
     stated as non-negotiable in every prior version of this spec, including
     the shipped code's own comment.
  5. "Act 2 has no piano" reverses revision 0.2-D, added specifically
     because this user asked for airier Act 2 music with piano.
  6. The PR-per-milestone / single-"director"-merges workflow (§11, §14)
     conflicts with `CLAUDE.md`'s direct-push-after-AGENT_LOG-entry model —
     and with how this session and the prior two have actually operated.
  7. Sides firmly with the original palette and the shipped radial-blur
     shader — a third document now disagreeing with `VISUAL_REFERENCE.md`,
     which is still sitting unresolved.
  8. "No second location" bears directly on the still-open Isolation
     question from `FEATURE_LIST.md`.
- Did not touch game code, README, the handoff doc, or any other file to
  implement or reconcile any of this — comparison and flagging only, same as
  the last two sessions.

**Pushed:** yes (human — Ezekiel — asked for it explicitly, same as the two
sessions above).

**Next:** items 1, 4, and 5 above touch features this user asked for by name
earlier in the same conversation this doc arrived in — those three
specifically are worth a direct human answer before anyone builds against
this file, not just a "someone will get to it eventually."

---

## Session — 2026-08-09 (feature-list comparison)

**Did:**
- Read `PERIPHERAL_UNREAL_HANDOFF.md` and `CLAUDE.md` per instruction, then
  compared them against `Isolation — Master Game Feature List.pdf` and
  `Chat GPT ISOLATION FINAL.pdf` (both from `~/Downloads` — turned out to be
  byte-identical, same 69-section document in both files).
- Saved the comparison as `FEATURE_LIST.md` at repo root: a **Needs a
  decision** section (6 items, most-important-first) for anything that
  conflicts with the existing spec, a **New** section for content with no
  conflict, and a **Duplicates** section (named, not repeated) for what
  Isolation already covers the same way Peripheral does.
- Did not resolve anything — no code or spec changes, purely a comparison
  document.

**The six flagged conflicts, briefly:** (1) whether "Isolation" is the same
project as Peripheral or a different one — everything else depends on this;
(2) Isolation's focus mechanic wants vision to stay capped below 100% clarity
even under deliberate attention, where Peripheral's model is centred = always
fully sharp (reinforces, and adds a wrinkle to, the blur-vs-detail-reduction
conflict already on file from the `VISUAL_REFERENCE.md` session); (3) the
existing "no inventory/collectibles" rule vs. Isolation's collectible-memory
and comfort-item-attrition systems, which are a core pillar of that design,
not incidental; (4) "entity never chases" vs. the Day 3 running-footsteps/
back-door climax; (5) Peripheral's fovea/occlusion/collision systems assume a
static level, Isolation wants the house topologically unreliable; (6) the
shipped house has one exterior door, Isolation needs a back door and garage.
Full detail, quotes, and section citations are in the file itself.

**Pushed:** yes (human — Ezekiel — asked for it explicitly, same as the
session above).

**Next:** decision #1 above blocks everything else in this document — worth
resolving before any of the "New" section gets built, since several of those
items (collectibles, comfort-item attrition, day/night structure) only make
sense once it's settled whether this extends Peripheral or starts a new
project.

---

## Session — 2026-08-09 (web prototype side)

**Did:**
- Saved `Peripheral_Art_Direction_Spec.txt` (from `~/Downloads`) as
  `VISUAL_REFERENCE.md` at repo root, reformatted to markdown, content
  otherwise unedited team input.
- Flagged three conflicts at the top of that file instead of resolving them:
  1. **Palette** — five different hex values than what's shipped in
     `src/constants.js`, and the new spec drops the flashlight's warm-color
     exception (`#FFE6B8`) the brief calls for and the game currently
     renders. *(Note: this also conflicts with the palette `CLAUDE.md`
     documents for the Unreal build — see "Conventions" there, which
     confirms `#FFE6B8` as the flashlight's one saturated exception. Same
     conflict, now live on both sides of the port.)*
  2. **Peripheral-vision technique** — shipped `fx/peripheral.js` is a radial
     blur + desaturation pass, matching the brief and `CLAUDE.md`'s "two
     systems must stay separate" architecture. The new spec explicitly
     rejects blur in favor of edge/detail-reduction preserving silhouettes.
  3. *(Minor)* HUD crosshair dot is always-on; new spec wants it hidden until
     something is interactable.
- No code changed to resolve any of these.

**Pushed:** yes (human — Ezekiel — asked for it explicitly).

**Next:** the palette/technique conflict needs a decision from whoever owns
final say on art direction before either `constants.js` or `fx/peripheral.js`
(web) / the UE materials and post-process volume get touched.

---

## Session — 2026-08-09

**Did:**
- Added `unreal/` scaffolding: `.gitattributes` (LFS rules for future binary
  assets), UE5-specific `.gitignore` entries, `CLAUDE.md` (units conversion,
  UE5 post-process defaults that violate the art direction, anomaly state
  machine architecture).
- Confirmed UE 5.8 installed at `X:\UE_5.8`.

**Pushed:** yes — commit `9d3b241`, scaffolding only, no engine-generated files.

**Next:** create the First Person Blueprint project in `unreal/`, enable the
Unreal MCP plugin + All Toolsets, verify MCP with a read-only session before any
write actions.
