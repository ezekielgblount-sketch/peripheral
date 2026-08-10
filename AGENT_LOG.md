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
