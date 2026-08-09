import * as THREE from 'three';
import { PAL, CEILING } from '../constants.js';

// Two light rigs. Act 1 is overcast and stale — dim ambient plus a few weak
// fixtures, readable but flat. Act 2 is near-black; the flashlight (on the
// player) does almost all the work, with a faint cold moon outside.

export function buildLighting(scene) {
  const rig = { act1: new THREE.Group(), act2: new THREE.Group(), fixtures: [] };

  // ---- Act 1 ----
  const amb1 = new THREE.AmbientLight(PAL.pale, 0.55);
  rig.act1.add(amb1);
  // weak overcast sky from above
  const hemi = new THREE.HemisphereLight(PAL.pale, PAL.dark, 0.5);
  rig.act1.add(hemi);

  // a few weak point lights in fixtures (living lamp, kitchen, hallway, bathroom)
  const fixSpots = [
    [2.2, CEILING - 0.2, 3.5],
    [9.6, CEILING - 0.2, 3.0],
    [6.0, CEILING - 0.2, 8.5],
    [2.2, CEILING - 0.2, 8.0],
    [10.5, CEILING - 0.2, 8.0],
  ];
  for (const [x, y, z] of fixSpots) {
    const p = new THREE.PointLight(PAL.light, 3.0, 7, 2);
    p.position.set(x, y, z);
    rig.act1.add(p);
    rig.fixtures.push(p);
  }

  // ---- Act 2 ----
  const amb2 = new THREE.AmbientLight(0x14161c, 0.5);
  rig.act2.add(amb2);
  const moon = new THREE.DirectionalLight(0x9fb0c8, 0.08);
  moon.position.set(-8, 12, -6);
  rig.act2.add(moon);
  rig.moon = moon;
  rig.amb2 = amb2;
  rig.porch = null; // set by yard

  scene.add(rig.act1);
  scene.add(rig.act2);
  rig.act2.visible = false;

  return rig;
}

export function setAct(rig, act) {
  rig.act1.visible = act === 1;
  rig.act2.visible = act === 2;
}

// Called by the breaker: bring the interior back to life at the end of Act 2.
export function powerOn(rig) {
  rig.amb2.intensity = 0.9;
  rig.amb2.color.set(PAL.light);
  for (const p of rig.fixtures) { p.intensity = 2.4; p.parent && (p.visible = true); }
  rig.act1.visible = true; // reuse fixtures for warm interior glow
  if (rig.porch) rig.porch.intensity = 4;
}
