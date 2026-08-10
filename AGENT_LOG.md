# Agent Log

Running record of what Claude did in each work session, in reverse-chronological
order (newest first). Written so either human can read a session's entry, look at
the diff, and decide whether to push — without needing to have watched the stream.

Convention: Claude commits locally with a clear message. **Pushing is a separate,
human decision** — read the entry below, check `git log` / `git diff`, then push
if it looks right.

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
(web) / the UE materials and post-process volume get touched. Also produced
`FEATURE_LIST.md` this same session — see the entry below.

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
