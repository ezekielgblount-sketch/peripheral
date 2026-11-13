# Look and feel

## The direction (decided Nov 12, 2026)

The game should look **as if it was filmed on a camcorder**: realistic underneath, low-res and soft on top. Joel's words:
"like if they were filmed on a camcorder" and "I want the graphics to be realistic tho just low res."

Reference games (nobody on the project has played them; the descriptions are second-hand from store pages and
screenshots):

- **Freddys_House** (CreepyGlitch): the main look. Wide-angle lens with dark corners, faded green-grey colour, lifted
  blacks, low-res blurry picture, flashlight-heavy lighting in a very ordinary real house.
- **Your Happy Place** (Dark_Knife15): keep only its handheld camera shake. Not its warm glow, heavy bloom or
  overexposure.
- **September 1999**: found-footage reference.

This replaces the earlier art rules from the "Isolation" documents: the five-colour matte palette and the bans on bloom,
grain, chromatic aberration, motion blur, auto-exposure and extra post-processing are **retired**. The two original
briefs are in [`briefs/`](briefs/).

Two things in those briefs disagree with each other; this is how they were settled, and Joel can overrule either:

- One brief says "one look only, no preset menu"; the other asks for presets and sliders. Built: presets and sliders, with
  **Default** being the one intended look.
- One brief lists focus hunting as "not requested"; the other asks for it. Built, with its own slider so it can be turned
  off.

## The three picture layers

All three are post-process materials on the level's one post-process volume (`PP_Base`), applied in this order. They are
built by scripts, not by hand, so they can be rebuilt and tuned by changing numbers.

### 1. The lens: `M_Bodycam` (`Scripts/build_bodycam.py`). Always on.

| Setting | Value | Meaning |
|---|---|---|
| Barrel | 0.17 | Wide-angle bulge |
| EdgeBlur | 1.1 | Softness at the rim; the centre stays sharp |
| Fringe | 2.2 | Colour fringing at the edges only |
| ShadowNoise | 0.05 | Noise in dark areas |
| Soft | 0.45 | Overall lens softness |
| Vignette (volume setting) | 0.6 | Dark corners |
| Film grain (volume setting) | 0.35 | |
| Motion blur (volume setting) | 0.3 | |
| Colour saturation (volume setting) | 0.9 | |

The same material holds the **unease** effects (tape tracking lines, colour splitting, slipping blocks, tears), driven by
`MPC_World.Unease` (0 to 1), `Preset` (0 subtle, 1 medium, 2 heavy, used at levels 8 to 10) and `Pulse`.

### 2. The found-footage filter: `M_Footage` (`Scripts/build_footage.py`)

Does not lower the render resolution. Sizes are in 1080p pixels so it looks the same at any resolution.

- **Softness:** a small blur plus in-camera sharpening halos around edges.
- **Colour bleed:** colour lags behind brightness and smears sideways, as on tape.
- **Compression:** flat areas settle into 8-pixel blocks, edges pick up crawling noise, smooth shades band. A faint
  tracking line rolls up the picture about every nine seconds (low contrast on purpose; no flashing).
- **Grain:** coarse, stronger in the dark, slightly coloured.
- **Depth of field:** things far from the focus distance are smeared. The focus distance comes from `BP_Footage`, which
  measures the thing in the centre of the picture and moves the focus toward it like a slow camcorder: it lags, overshoots
  by about a sixth and settles in a couple of seconds.
- **Tone:** faded and slightly green-grey, blacks lifted, highlights only gently bloomed.

### 3. Tape resolution: `M_FootageRes` (same script)

Re-samples the finished picture onto a camcorder-sized grid and scales it back up soft. The game still renders at the
player's chosen resolution; only the look is low-res. Because it runs last, the grain and blocks are tape-sized too.
The slider maps to lines of picture: 0 = off, 0.3 ≈ 690 lines, 0.6 ≈ 435, 0.8 ≈ 320, 1.0 ≈ 240.

### Presets (Settings → Footage look)

| Preset | Softness | Grain | Colour bleed | Compression | Depth of field | Tape resolution |
|---|---|---|---|---|---|---|
| Off | 0 | 0 | 0 | 0 | 0 | 0 |
| Light | 0.30 | 0.25 | 0.25 | 0.20 | 0.30 | 0.30 |
| **Default** | 0.55 | 0.45 | 0.50 | 0.40 | 0.55 | 0.60 |
| Heavy | 0.85 | 0.75 | 0.80 | 0.75 | 0.80 | 0.80 |

Moving any slider switches the preset to Custom. The values are saved between launches. The six strengths live in the
material parameter collection `MPC_World` as `FootSoft`, `FootGrain`, `FootBleed`, `FootComp`, `FootDof`, `FootRes`, plus
`FootFocus` (the focus distance in cm). The same numbers appear in `Scripts/build_footage.py` and `Scripts/ui_menu.py`;
change both.

Comparison pictures of every preset are in `unreal/Peripheral_POC/screenshots/footage_look/`.

**Resolution is the player's choice.** Settings → Display offers 1280x720 up to 3840x2160 and Graphics has a resolution
scale slider (50 to 100%). Nothing in the project forces a low render resolution.

## Camera motion

Chest-mounted body-cam feel: sway while walking, a small jolt per step, lag on fast head turns, a settle on stopping.
Settings → Accessibility → "Camera motion intensity" scales it down to off (this is the shake slider and off switch the
brief asks for). Unease effects never touch the camera motion.

## The house's style

- "Warm Americana family home, late 1990s to 2000s." Kept for decades, lived in until a few weeks ago.
- Most walls are painted, a different colour per room, with white or off-white trim and ceilings so rooms never blend into
  one yellow tone. Wallpaper in at most two or three rooms. The paint and floor for every room are listed in
  `DESIGN_BIBLE.md` section 8.
- The parents' everyday technology is from about 2010 to 2014 (a small older flat-screen, a dated laptop, a cordless
  phone). Jack's own things are the time capsule, about 1998 to 2010 (a CRT, a beige PC, a handheld console, posters).
- Real furniture sizes and real ceiling heights (244 cm). The scale rules are in `DESIGN_BIBLE.md` section 5.

## Materials: wanted, not yet done

The house currently reads as too clean and uniform ("a more mature Roblox game"). Joel's brief
([`briefs/realistic_procedural_materials.md`](briefs/realistic_procedural_materials.md)) asks for realistic surfaces made
procedurally inside Unreal, with no AI image generation:

- Stains, yellowing, cracks, roughness variation, dirt gathering low on walls and in corners, wear on floors.
- A master wall material and a master floor material first, then wood, concrete, metal, fabric, tile.
- Textures 1K by default, 2K at most; packed maps; a cheaper "Low" variant.
- Must run well on a base M4 Max Mac and on an RTX 3060 with 12 GB.

What exists today: one world-aligned master material, `M_Surface` (`Scripts/build_materials.py`), with about 100
instances (`MIL_*`), each using a code-generated colour, normal and roughness texture plus a single dirt map. The planned
route is to add the variation, stains and wear to that one master so every surface in the house improves together.

## Lighting

- Lumen for global illumination and reflections, virtual shadow maps, no baked lighting.
- The sun is a real 45,000 lux and bulbs use real lumens, so exposure behaves like a camera: windows blow out indoors by
  day. Warm incandescent bulbs around 2700 K. Every lamp is a real light the player can switch on and off.
- The N key switches day and night for judging both moods.
- Flashlight: 2800 to 3000 K, tint `#FFE6B8`, 30 degree inner and 60 degree outer cone.
