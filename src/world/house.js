import * as THREE from 'three';
import { CEILING, WALL_T, DOOR_W, PAL } from '../constants.js';
import { aabb } from '../core/collision.js';

// The house is assembled from box geometry. Everything here is static structure:
// floor, ceiling, walls (with door and window openings), and the openable front
// door. Props live in props.js. Coordinates: x 0..12, z 0..14, y up, floor y=0.
//
// Rooms, clockwise-ish from the front door (south, z=0):
//   entry    x 4.5..7.5  z 0..3      hallway  x 4.5..7.5  z 3..14
//   living   x 0..4.5    z 0..6      kitchen  x 7.5..12   z 0..6
//   bathroom x 0..4.5    z 6..10     bedroom  x 7.5..12   z 6..10
//   study    x 0..4.5    z 10..14    utility  x 7.5..12   z 10..14

export function buildHouse() {
  const group = new THREE.Group();
  const colliders = [];

  const matWall = new THREE.MeshStandardMaterial({ color: PAL.light, roughness: 1, metalness: 0 });
  const matFloor = new THREE.MeshStandardMaterial({ color: PAL.dark, roughness: 1, metalness: 0 });
  const matCeil = new THREE.MeshStandardMaterial({ color: PAL.mid, roughness: 1, metalness: 0 });
  const matTrim = new THREE.MeshStandardMaterial({ color: PAL.mid, roughness: 1, metalness: 0 });
  const matGlass = new THREE.MeshBasicMaterial({ color: 0x20201d, transparent: true, opacity: 0.18, side: THREE.DoubleSide });

  const box = (w, h, d, mat) => new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);

  // --- floor & ceiling ---
  const floor = box(12, 0.1, 14, matFloor);
  floor.position.set(6, -0.05, 7);
  floor.receiveShadow = true;
  group.add(floor);
  colliders.push(aabb(6, -0.05, 7, 12, 0.1, 14));

  const ceil = box(12, 0.1, 14, matCeil);
  ceil.position.set(6, CEILING + 0.05, 7);
  group.add(ceil);
  colliders.push(aabb(6, CEILING + 0.05, 7, 12, 0.1, 14));

  // --- wall builder ---
  // A straight, axis-aligned wall from (x1,z1) to (x2,z2), y 0..h.
  function wall(x1, z1, x2, z2, h = CEILING, collide = true, mat = matWall) {
    const along = z1 === z2 ? 'x' : 'z';
    let w, d, cx, cz;
    if (along === 'x') {
      w = Math.abs(x2 - x1); d = WALL_T; cx = (x1 + x2) / 2; cz = z1;
    } else {
      w = WALL_T; d = Math.abs(z2 - z1); cx = x1; cz = (z1 + z2) / 2;
    }
    if (w < 1e-4 && along === 'x') return; // zero-length segment
    if (d < 1e-4 && along === 'z') return;
    const m = box(w, h, d, mat);
    m.position.set(cx, h / 2, cz);
    m.castShadow = true;
    m.receiveShadow = true;
    group.add(m);
    if (collide) colliders.push(aabb(cx, h / 2, cz, Math.max(w, WALL_T), h, Math.max(d, WALL_T)));
    return m;
  }

  // A wall run along one axis, with a doorway gap (no header — full-height opening).
  function wallWithDoor(a1, b, a2, doorStart, axis) {
    // axis 'x': wall runs along x at constant z=b, gap from doorStart..doorStart+DOOR_W
    // axis 'z': wall runs along z at constant x=b, gap from doorStart..doorStart+DOOR_W
    const gapEnd = doorStart + DOOR_W;
    if (axis === 'x') {
      wall(a1, b, doorStart, b);
      wall(gapEnd, b, a2, b);
      // header above the doorway
      headerBox(doorStart, b, gapEnd, b, 'x');
    } else {
      wall(b, a1, b, doorStart);
      wall(b, gapEnd, b, a2);
      headerBox(b, doorStart, b, gapEnd, 'z');
    }
  }

  function headerBox(x1, z1, x2, z2, axis) {
    const doorH = 2.05;
    const hh = CEILING - doorH;
    if (hh <= 0) return;
    let w, d, cx, cz;
    if (axis === 'x') { w = Math.abs(x2 - x1); d = WALL_T; cx = (x1 + x2) / 2; cz = z1; }
    else { w = WALL_T; d = Math.abs(z2 - z1); cx = x1; cz = (z1 + z2) / 2; }
    const m = box(w, hh, d, matWall);
    m.position.set(cx, doorH + hh / 2, cz);
    m.castShadow = true;
    group.add(m);
    // header is above head height; no collider needed for the walking capsule
  }

  // A wall run with a window opening: side pillars, sill, header, glass pane.
  // One solid collider spans the whole run so the player cannot pass through.
  function wallWithWindow(a1, b, a2, winStart, winEnd, axis, sillY = 0.95, headY = 2.05) {
    if (axis === 'x') {
      wall(a1, b, winStart, b);
      wall(winEnd, b, a2, b, CEILING, true);
      // sill and header across the opening (visual only)
      const w = winEnd - winStart;
      let m = box(w, sillY, WALL_T, matWall); m.position.set((winStart + winEnd) / 2, sillY / 2, b); group.add(m);
      m = box(w, CEILING - headY, WALL_T, matWall); m.position.set((winStart + winEnd) / 2, headY + (CEILING - headY) / 2, b); group.add(m);
      const pane = box(w, headY - sillY, 0.03, matGlass); pane.position.set((winStart + winEnd) / 2, (sillY + headY) / 2, b); pane.userData.noOcclude = true; group.add(pane);
      const frame = box(w + 0.08, headY - sillY + 0.08, 0.06, matTrim); frame.position.set((winStart + winEnd) / 2, (sillY + headY) / 2, b); group.add(frame);
      pane.renderOrder = 1;
      // full-run solid collider
      colliders.push(aabb((a1 + a2) / 2, CEILING / 2, b, Math.abs(a2 - a1), CEILING, WALL_T));
    } else {
      wall(b, a1, b, winStart);
      wall(b, winEnd, b, a2, CEILING, true);
      const d = winEnd - winStart;
      let m = box(WALL_T, sillY, d, matWall); m.position.set(b, sillY / 2, (winStart + winEnd) / 2); group.add(m);
      m = box(WALL_T, CEILING - headY, d, matWall); m.position.set(b, headY + (CEILING - headY) / 2, (winStart + winEnd) / 2); group.add(m);
      const pane = box(0.03, headY - sillY, d, matGlass); pane.position.set(b, (sillY + headY) / 2, (winStart + winEnd) / 2); pane.userData.noOcclude = true; group.add(pane);
      const frame = box(0.06, headY - sillY + 0.08, d + 0.08, matTrim); frame.position.set(b, (sillY + headY) / 2, (winStart + winEnd) / 2); group.add(frame);
      colliders.push(aabb(b, CEILING / 2, (a1 + a2) / 2, WALL_T, CEILING, Math.abs(a2 - a1)));
    }
    return { center: axis === 'x'
      ? new THREE.Vector3((winStart + winEnd) / 2, (sillY + headY) / 2, b)
      : new THREE.Vector3(b, (sillY + headY) / 2, (winStart + winEnd) / 2) };
  }

  // ---- exterior perimeter ----
  // South wall (z=0) with the front doorway (x 5.55..6.45).
  wall(0, 0, 5.55, 0);
  wall(6.45, 0, 12, 0);
  headerBox(5.55, 0, 6.45, 0, 'x');
  // North wall (z=14) solid — the breaker is mounted on its outside.
  wall(0, 14, 12, 14);
  // West wall (x=0) with living-room window and study window.
  wall(0, 0, 0, 2.4, CEILING, true);       // corner to living window
  const winLiving = wallWithWindow(2.4, 0, 3.8, 2.6, 3.6, 'z');   // living window faces west yard
  wall(0, 3.8, 0, 10.6, CEILING, true);
  const winStudy = wallWithWindow(10.6, 0, 12.2, 10.9, 11.9, 'z');
  wall(0, 12.2, 0, 14, CEILING, true);
  // East wall (x=12) with kitchen window and bedroom window.
  wall(12, 0, 12, 2.4, CEILING, true);
  const winKitchen = wallWithWindow(2.4, 12, 3.8, 2.6, 3.6, 'z');  // over the sink
  wall(12, 3.8, 12, 7.0, CEILING, true);
  const winBedroom = wallWithWindow(7.0, 12, 8.6, 7.3, 8.3, 'z');  // faces the treeline
  wall(12, 8.6, 12, 14, CEILING, true);

  // ---- interior partitions ----
  // living | entry+hallway  (x = 4.5)
  wallWithDoor(0, 4.5, 3.0, 1.0, 'z');   // entry -> living door (z 1.0..1.9)
  wall(4.5, 3.0, 4.5, 6.0);              // living back wall stretch (solid up to z6)
  wallWithDoor(6.0, 4.5, 10.0, 7.0, 'z');// hallway -> bathroom door (z 7.0..7.9)
  wallWithDoor(10.0, 4.5, 14.0, 11.0, 'z');// hallway -> study door (z 11.0..11.9)
  // kitchen | entry+hallway (x = 7.5)
  wallWithDoor(0, 7.5, 3.0, 1.6, 'z');   // entry -> kitchen door
  wall(7.5, 3.0, 7.5, 6.0);              // kitchen back wall stretch
  wallWithDoor(6.0, 7.5, 10.0, 7.0, 'z');// hallway -> bedroom door
  wallWithDoor(10.0, 7.5, 14.0, 11.0, 'z');// hallway -> utility door
  // room separators (z = 6 and z = 10), solid
  wall(0, 6, 4.5, 6);      // living | bathroom
  wall(7.5, 6, 12, 6);     // kitchen | bedroom
  wall(0, 10, 4.5, 10);    // bathroom | study
  wall(7.5, 10, 12, 10);   // bedroom | utility

  // ---- front door (openable) ----
  const frontDoor = makeDoor(matTrim, DOOR_W, 2.05);
  // hinge at x=5.55, z=0; leaf extends toward +x when closed, swings inward (+z)
  frontDoor.group.position.set(5.55, 0, 0);
  group.add(frontDoor.group);

  // rooms (2D bounds for profile / room detection)
  const rooms = [
    { name: 'entry',    min: { x: 4.5, z: 0 },  max: { x: 7.5, z: 3 } },
    { name: 'living',   min: { x: 0,   z: 0 },  max: { x: 4.5, z: 6 } },
    { name: 'kitchen',  min: { x: 7.5, z: 0 },  max: { x: 12,  z: 6 } },
    { name: 'hallway',  min: { x: 4.5, z: 3 },  max: { x: 7.5, z: 14 } },
    { name: 'bathroom', min: { x: 0,   z: 6 },  max: { x: 4.5, z: 10 } },
    { name: 'bedroom',  min: { x: 7.5, z: 6 },  max: { x: 12,  z: 10 } },
    { name: 'study',    min: { x: 0,   z: 10 }, max: { x: 4.5, z: 14 } },
    { name: 'utility',  min: { x: 7.5, z: 10 }, max: { x: 12,  z: 14 } },
  ];

  const anchors = {
    spawnOutside: new THREE.Vector3(6, 0, -6),
    frontDoor: new THREE.Vector3(6, 0, 0),
    entryCenter: new THREE.Vector3(6, 0, 1.5),
    bed: new THREE.Vector3(10.5, 0, 8.4),          // bedroom
    studyWake: new THREE.Vector3(2.2, 0, 12.4),    // study, Act 2 wake spot
    breaker: new THREE.Vector3(11, 0, 14),         // on north exterior wall
    windows: { winLiving, winKitchen, winBedroom, winStudy },
  };

  return { group, colliders, rooms, doors: [frontDoor], frontDoor, anchors, materials: { matWall, matTrim } };
}

// A door leaf on a hinge pivot. openAngle in radians. Interact toggles it.
export function makeDoor(mat, w = DOOR_W, h = 2.05) {
  const pivot = new THREE.Group();
  const leaf = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.05), mat);
  leaf.castShadow = true;
  leaf.receiveShadow = true;
  leaf.position.set(w / 2, h / 2, 0); // pivot at the leaf's edge
  pivot.add(leaf);

  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 8), mat);
  knob.position.set(w - 0.08, h / 2, 0.05);
  pivot.add(knob);

  return {
    group: pivot,
    leaf,
    isOpen: false,
    _t: 0,
    target: 0,
    open() { this.target = -Math.PI * 0.5; this.isOpen = true; },
    close() { this.target = 0; this.isOpen = false; },
    toggle() { this.isOpen ? this.close() : this.open(); },
    setAjar(rad) { this.target = rad; this._t = rad; pivot.rotation.y = rad; },
    update(dt) {
      const d = this.target - this._t;
      if (Math.abs(d) > 1e-4) {
        this._t += d * Math.min(1, dt * 6);
        pivot.rotation.y = this._t;
      }
    },
  };
}
