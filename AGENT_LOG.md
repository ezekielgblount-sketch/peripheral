# Agent Log

Running record of what Claude did in each work session, in reverse-chronological
order (newest first). Written so either human can read a session's entry, look at
the diff, and decide whether to push — without needing to have watched the stream.

Convention: Claude commits locally with a clear message. **Pushing is a separate,
human decision** — read the entry below, check `git log` / `git diff`, then push
if it looks right.

---

## Session — 2026-08-09 (2)

**Did:**
- First real commit of the FirstPerson template project content (`Config/`,
  `Content/`, `Peripheral.uproject`). The previous session only committed
  scaffolding (`.gitattributes`/`.gitignore`/`CLAUDE.md`) — the project itself
  had never been checked in, so this commit is also the initial import.
- Found an existing `PostProcessVolume` (`PPV_Global`) in `Lvl_FirstPerson`,
  left over from an interrupted prior session. It existed but did nothing —
  `bUnbound` was `false` and every override flag was `false`. Set
  `bUnbound=true`, zeroed Bloom, Lens Flare, Film Grain, Motion Blur, and
  Chromatic Aberration (Scene Fringe + Start Offset) via override, and locked
  exposure by setting Auto Exposure Method to Manual with Bias overridden to 0.
- Fixed Specular on all 5 project materials (`M_PrototypeGrid`, `M_FlatCol`,
  `M_Mannequin`, `M_SimpleGlow`, `M_GradientGlow`) — Unreal's default material
  Specular is 0.5 and was left unconnected (hardcoded) on every one of them.
  Wired a `Constant(0)` into `MP_Specular` on each and recompiled. Roughness/
  Metallic on the level materials (`M_PrototypeGrid`, `M_FlatCol`) were already
  correct (1/0) — no change needed there.

**Pushed:** no — local commit only, human should review before pushing.

**Next:** strip the First Person template (remove gun/projectile logic, remove
jump input), tune movement (walk 260uu/s, shift-held slow walk 130uu/s, confirm
eye height 165uu), block out the first hallway grey-box.

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
