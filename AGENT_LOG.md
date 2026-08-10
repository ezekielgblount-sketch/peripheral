# Agent Log

Chronological record of automated/agent-driven changes to this repo, most
recent first. Human-authored commits aren't duplicated here — this is for
context an agent needed to make a decision, especially flagged conflicts that
weren't resolved on the spot.

---

## 2026-08-09 — Added `VISUAL_REFERENCE.md` (art direction spec import)

**Agent:** Claude (Sonnet 5, Claude Code)

**Action:** Saved `Peripheral_Art_Direction_Spec.txt` (supplied by the user
from `~/Downloads`) as `VISUAL_REFERENCE.md` at the repo root, reformatted to
markdown. Content is otherwise unedited team input, not an agent-authored
document.

**Flagged, not resolved** — three points where the new spec contradicts the
project's existing art direction (the *Art Direction* section of the original
build brief; no file literally named `CLAUDE.md` exists in this repo):

1. **Palette.** Five different hex values from what's shipped in
   `src/constants.js` (`PAL`), and the new spec removes the flashlight's
   warm-color exception (`PAL.warm = 0xFFE6B8`) that the brief explicitly
   calls for and the game currently renders.
2. **Peripheral-vision technique.** Shipped `src/fx/peripheral.js` is a
   radial blur + desaturation pass, matching the brief's explicit
   instruction ("the blur and the desaturation are the point... do not use a
   vignette instead"). The new spec explicitly rejects a blur approach in
   favor of edge/detail-reduction that preserves silhouettes, with a
   different information-percentage curve by peripheral zone.
3. **(Minor) Crosshair.** Shipped HUD dot is always visible; new spec prefers
   it hidden except when something is interactable.

No code was changed to resolve any of these — see the conflict callout at the
top of `VISUAL_REFERENCE.md` for full detail and a side-by-side hex table.
**Next step is a team decision** on which palette/technique is canonical
before anyone touches `constants.js` or `fx/peripheral.js`.
