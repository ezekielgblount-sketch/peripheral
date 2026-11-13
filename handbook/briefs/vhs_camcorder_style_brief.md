> Handed over by Joel on 2026-11-12. Written for an AI coder, against the older `unreal/Isolation` project; it is applied
> here to `unreal/Peripheral_POC`. One sentence was removed for the public repo (marked below). Where it disagrees with the
> later found-footage update, see `handbook/06_DECISIONS.md`.

# VHS Camcorder Style Brief: Unreal Engine 5.8 (for an AI coder)

Hand this whole note to the coder. It is self-contained. Companion research: [[UE5 VHS Implementation Research]].

## Your job in one paragraph
The game ("Isolation", formerly Peripheral) is mostly built in Unreal Engine 5.8. Do not rebuild it. Restyle how it looks to an 80s/90s camcorder VHS tape with "blurry realism", like two reference games: "Your Happy Place" (Dark_Knife15, UE5) and "Freddys_House" (CreepyGlitch). You cannot play either, so work from this brief. Survey the project first, then ask the user the questions below, then propose a plan and wait for approval before changing anything.

## Decisions already made by the user (2026-11-12)
1. **The VHS look replaces the old art rules.** The old five-colour matte palette and the bans on bloom, grain, chromatic aberration, motion blur, auto-exposure and extra post-processing are retired. Update CLAUDE.md, VISUAL_REFERENCE.md and HOUSE_ENVIRONMENT_SPEC.md to say so, and tell the user which lines you changed.
2. **Keep the peripheral-vision pass.** `PP_PeripheralVision` (with `MPC_PeripheralVision`) is the core mechanic. It must still work exactly as before. The VHS filter is added on top, not merged in, unless you show a measured reason and the user approves.
3. **Main look: Freddys_House (user correction, 2026-11-12: "the look is exactly how the Freddy house looks a lot").** Wide-angle lens with dark corners, faded greenish-gray colour, lifted blacks, low-res and blurry image, flashlight-heavy lighting in a very ordinary-looking real house. One look only, no preset menu. Note: this description of the game comes from store pages and screenshots second-hand; nobody has played it.
   Earlier in the session the user also picked the warm, overexposed Your Happy Place look. The later statement wins. **Decided: from Your Happy Place keep only the handheld camera shake** (with a strength slider and off switch). Do not use its warm glow, heavy bloom or overexposure.
4. **Also wanted:** handheld camera shake with a strength slider and off switch, and a more realistic-looking house (photo-style textures, ordinary real rooms) replacing the grey-box look.
5. **Not requested (ask before building):** REC dot and timestamp overlay, slow auto-exposure iris and focus hunting, tape-hiss audio.

## The look
- Strong barrel/fisheye lens distortion with rounded, dark-vignetted corners.
- Low-res, soft image; colour smeared sideways more than brightness (VHS stores colour at lower resolution).
- Chromatic aberration at the edges, faint sharpening halos.
- Faded, desaturated greenish-gray tones with lifted blacks (Freddys_House). Keep bloom modest; no Happy Place warm glow.
- Film grain and tape noise; occasional tracking lines and horizontal jitter; slight ghosting if feasible.
- Handheld shake. Players of the reference game complained of motion sickness, so shake must be adjustable from day one.
- Freddys_House specifics: low-res blurry image, flashlight-heavy lighting, a very ordinary real-looking house. [A second-hand remark about that game's developer was removed here for the public repo.] Avoid AI-generated character models.

## What the project already has (read these first)
- `unreal/Isolation/Isolation.uproject`, UE 5.8 exactly. Blueprints only, no C++; if something seems to need C++, ask first.
- `Config/DefaultEngine.ini`: Lumen GI and reflections, Virtual Shadow Maps, ray tracing, Substrate, DX12/SM6. `r.AllowStaticLighting=False`, so baked lightmaps are off. The reference game is described as using Lumen too, so keep Lumen.
- Assets: `PP_PeripheralVision`, `MPC_PeripheralVision`, `BP_PostProcessToggle`, `BP_DayNightDebug`, `FoveaComponent`, `BP_Anomaly`, `BP_FirstPersonCharacter`, `BP_FirstPersonCameraManager`, level `Lvl_FirstPerson`, materials `MI_*` built against the old palette.
- Docs at repo root: `CLAUDE.md`, `FEATURE_LIST.md`, `PERIPHERAL_UNREAL_HANDOFF.md` (mechanics source of truth), `VISUAL_REFERENCE.md`, `HOUSE_ENVIRONMENT_SPEC.md`, `AGENT_LOG.md`.
- `CLAUDE.md` says Unreal Editor must be fully open before launching Claude Code from `unreal/` for the MCP connection. Commit before any significant work.

## Suggested technical approach (verify in the editor)
- One Post Process Material in an Unbound Post Process Volume, driven by a material instance or the existing MPC. Cover: UV barrel distortion plus corner mask, chromatic aberration, YIQ colour smear, grain, tracking lines, jitter.
- Built-in Post Process Volume settings for bloom, vignette, exposure, colour grade (lifted blacks, desaturated green-gray tint).
- Low resolution: either `r.ScreenPercentage` with `r.Upscale.Quality 0` (reported broken in some versions, test on 5.8) or UV snapping in the material.
- Shake: a camera shake blueprint with a Perlin pattern on the player camera, scaled by a user setting.
- Ghosting is the hardest effect in UE post-processing; propose options and let the user choose.
- Keep flicker and tracking-line flashes low in contrast and rate (a forum report mentions a seizure-like result). Make flash intensity adjustable.

## Questions to ask the user before planning
1. What is the minimum PC you are targeting, and what frame rate? (Lumen, ray tracing and Substrate are heavy; the filter adds cost.)
2. Should the one look have an intensity slider and an Off setting in the pause menu, or be fixed? (Only one look exists; no presets.)
3. Should the new look apply to menus and the pause screen as well as gameplay?
4. How should the realistic house be made: your own photo textures, purchased scans, or a stand-in until final art? Who supplies the assets?
5. How bright and how blurry should dark scenes be, since the flashlight acts and the Day 3 blackout rely on darkness (lifted blacks make dark scenes easier to read)?6. Which anomalies depend on dark silhouettes or subtle contrast? Heavy blur and bloom can hide them or reveal them; the user decides which.
7. Do you want the REC dot and timestamp, auto-exposure iris, focus hunting, or tape-hiss audio? (Currently not requested.)
8. Should the game's one jump scare (Act 27) get any special filter behaviour?

## Constraints
- Hold the agreed frame rate. Report the measured cost of each effect (use `stat gpu` or Unreal Insights and say which you used).
- Small reviewable steps. Commit locally after each working step; ask before pushing. Only the Unreal-connected session commits anything under `unreal/`.
- Everything adjustable through parameters the team can change without code.
- Do not use AI-generated character models or assets.
- Write down in `AGENT_LOG.md` what changed, whether it was pushed, and what is next.

## Related
[[Art Direction Rules]] (to be updated by the coder) · [[VHS Camcorder Look Research]] · [[Open Decisions]]
