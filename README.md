# PERIPHERAL

A first-person horror game about the difference between what you're **looking at**
and what you can **see**. Things go wrong at the edges of the frame and are always
ordinary again by the time you turn to face them. Build 0.1.

Runs in the browser. No textures, no models, no audio files — every surface is a
Three.js primitive and every sound is synthesised with the Web Audio API. The
whole game is readable source.

## Run it

```bash
npm install
npm run dev
```

Then open the URL Vite prints (it serves under `/peripheral/`).

Build a static bundle with `npm run build`; preview it with `npm run preview`.

## Deploy

`.github/workflows/deploy.yml` builds and publishes `dist/` to GitHub Pages on
every push to `main`. In the repo settings, set **Pages → Build and deployment →
Source** to **GitHub Actions**. `vite.config.js` sets `base: '/peripheral/'` to
match a project page at `https://<user>.github.io/peripheral/`; change it to `'/'`
if you deploy to a user/organization root page.

## Controls

`WASD` move · mouse look · `Shift` walk slower · `E` interact · `Esc` pause.

## The two acts

1. **Settling in.** You arrive on the path in flat grey daylight. Walk to the
   door, go in, look around. After a while: *"Look around. Then get some sleep."*
   The house quietly rearranges itself in your blind spots. Get into bed to end
   the act — beeline for it if you like; Act 2 just gets harder because the game
   learned less about you.
2. **The power.** You wake on the study floor. The lights are dead, you have a
   flashlight, and the breaker is outside — around the dark side of the house.
   Something is out there in the periphery. Flip the breaker to finish the build.

Roughly eight minutes end to end.

---

## Design note: the mechanic

The game separates two systems that are easy to conflate, and keeps them apart in
the code on purpose.

### 1. The visual falloff is a *look*, not a trick

`fx/peripheral.js` renders the scene to one `WebGLRenderTarget`, then draws a
single fullscreen quad whose shader degrades everything away from screen centre:
a radial blur that reaches further the further you are from the middle, a slide
toward luminance (desaturation), and a small loss of brightness. About the inner
20% of screen radius is left perfectly sharp, then it falls off quickly.

This is deliberately **not** what hides the anomalies. If it were, a player could
screenshot the frame, zoom the corner, and catch the change. Verified in build:
centre pixels stay sharp and saturated (colour spread ~17), corner pixels come
back desaturated and dimmer (spread ~2). It sells the *feeling* of peripheral
vision; it decides nothing about the world.

### 2. The anomalies are hidden by geometry, distance and timing

`game/anomaly.js` is a state machine, one instance per anomaly-capable prop, and
it never reads the shader:

```
DORMANT  -> the Director may select it
ARMED    -> chosen, but still normal. Flips to the off-state ONLY on a frame
            where the fovea is >40 deg away OR the prop is fully occluded.
ACTIVE   -> visibly wrong, indefinitely.
RESOLVING-> the fovea has rested within 11 deg, unoccluded (raycast-confirmed),
            for >0.12s. On the very next frame it snaps to normal — one frame,
            no tween, no sound. It must look like it was never anything else.
SPENT    -> cools down 60-120s and may only re-arm from a different room.
```

`game/fovea.js` supplies the angle tests and the occlusion raycast; it is pure
logic. The 0.12s dwell means a fast pan across a room clears nothing but a
deliberate look always resolves, and there's a few-degrees hysteresis so a prop
sitting on the 11 deg boundary doesn't flicker.

**The player can never witness a transition.** A strafe past a prop while staring
straight ahead leaves it exactly as it was; the flip waits for a frame where you
genuinely cannot see it.

The eight anomalies: floor lamp leans, a hallway door yawns open, a kitchen chair
turns to face the hall, a portrait's head cranks toward the room, a coat fills
out as if worn, a shape stands in the bathroom mirror, a fifth door appears in
the four-door hallway, and a figure waits in the treeline past the bedroom window.

### 3. The Director learns you

`game/profile.js` samples every frame — yaw velocity (sweeper vs twitcher), a
histogram of where your fovea rests relative to your heading, how often you check
behind you, room dwell and visit order, whether you hug walls or walk down the
middle. `game/director.js` arms one anomaly every 25-40s and biases its choice
toward the angular zones you habitually *neglect*: never look up, and it works the
ceiling; always check behind, and it stops rewarding that and works your
forward-left instead. It's a stats object and a weighted picker, nothing more —
inspect it live at `window.__profile` in a dev build.

### 4. The entity (Act 2) plays by the same rules

It only ever occupies positions outside your fovea, holds perfectly still, and is
removed the frame you centre it — then returns a little closer. It never chases,
touches, or kills you in this build. When it's within 15m and unoccluded, the
synthesised cricket bed simply **stops**, and resumes six seconds after it's gone.
Nothing ever explains this.

## Layout

```
index.html                 vite.config.js       .github/workflows/deploy.yml
src/
  main.js                  bootstrap, loop, act switching, interaction
  constants.js             shared numbers (palette, scale, fovea angles, pacing)
  core/    renderer.js input.js audio.js collision.js loop.js
  world/   house.js yard.js props.js lighting.js
  game/    player.js fovea.js anomaly.js director.js profile.js acts.js
  fx/      peripheral.js
  ui/      menu.js hud.js
```

## Don't (design constraints kept in this build)

No jumpscares, no screamer stings, no loud transients. No blood, gore, or written
lore — the house is ordinary and that's the horror. The entity never catches you.
No stamina, inventory, collectibles, or notes. No post-processing beyond the one
peripheral pass.
