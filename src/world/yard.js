import * as THREE from 'three';
import { PAL } from '../constants.js';
import { aabb } from '../core/collision.js';

// The yard: ground, a perimeter fence, the gravel path to the porch, a treeline
// of low-poly conifer silhouettes, the porch with its bulb, and the breaker box
// on the dark back corner. Returns meshes + colliders + a couple of anchors.

export function buildYard() {
  const group = new THREE.Group();
  const colliders = [];

  const matGround = new THREE.MeshStandardMaterial({ color: 0x2b2a26, roughness: 1, metalness: 0 });
  const matGravel = new THREE.MeshStandardMaterial({ color: PAL.mid, roughness: 1, metalness: 0 });
  const matFence = new THREE.MeshStandardMaterial({ color: PAL.dark, roughness: 1, metalness: 0 });
  const matTree = new THREE.MeshStandardMaterial({ color: 0x1d1f1b, roughness: 1, metalness: 0 });
  const matWood = new THREE.MeshStandardMaterial({ color: PAL.dark, roughness: 1, metalness: 0 });
  const matMetal = new THREE.MeshStandardMaterial({ color: PAL.mid, roughness: 1, metalness: 0 });

  const box = (w, h, d, mat) => new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);

  // ground plane (large)
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), matGround);
  ground.rotation.x = -Math.PI / 2;
  ground.position.set(6, -0.05, 7);
  ground.receiveShadow = true;
  group.add(ground);

  // gravel path from spawn (z<0) up to the porch
  const path = box(1.6, 0.02, 9, matGravel);
  path.position.set(6, 0.0, -4.0);
  path.receiveShadow = true;
  group.add(path);

  // porch: platform + two posts + a bulb fixture over the door
  const porch = box(3.0, 0.12, 1.6, matWood);
  porch.position.set(6, 0.06, -0.9);
  porch.receiveShadow = true;
  porch.castShadow = true;
  group.add(porch);
  // three steps
  for (let i = 0; i < 3; i++) {
    const step = box(2.0, 0.12, 0.35, matWood);
    step.position.set(6, 0.06 - (i + 1) * 0.12, -1.7 - i * 0.35);
    group.add(step);
  }
  // porch posts (tall enough to carry the roof) + railing
  for (const px of [4.7, 7.3]) {
    const post = box(0.12, 2.45, 0.12, matWood);
    post.position.set(px, 1.225, -1.7);
    post.castShadow = true;
    group.add(post);
  }
  const rail = box(2.86, 0.08, 0.08, matWood);
  rail.position.set(6, 0.9, -1.7);
  group.add(rail);
  // front beam across the posts, just under the roof
  const beam = box(3.0, 0.14, 0.12, matWood);
  beam.position.set(6, 2.36, -1.7);
  group.add(beam);
  // porch roof: a flat overhang so the door and bulb are sheltered
  const roof = box(3.4, 0.12, 2.1, matWood);
  roof.position.set(6, 2.5, -0.85);
  roof.castShadow = true;
  group.add(roof);

  // porch bulb, hung from the roof underside on a short stem (Act 2 lights it)
  const stem = box(0.02, 0.16, 0.02, matWood);
  stem.position.set(6, 2.36, -0.5);
  group.add(stem);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.05, 8, 8),
    new THREE.MeshBasicMaterial({ color: PAL.pale }));
  bulb.position.set(6, 2.25, -0.5);
  group.add(bulb);
  const porchLight = new THREE.PointLight(PAL.warm, 0, 6, 2);
  porchLight.position.set(6, 2.2, -0.5);
  group.add(porchLight);

  // ---- perimeter fence (with a gap for the path at the front) ----
  const fenceH = 1.1;
  function fence(x1, z1, x2, z2) {
    const along = z1 === z2 ? 'x' : 'z';
    const w = along === 'x' ? Math.abs(x2 - x1) : 0.1;
    const d = along === 'x' ? 0.1 : Math.abs(z2 - z1);
    const cx = (x1 + x2) / 2, cz = (z1 + z2) / 2;
    const m = box(w, fenceH, d, matFence);
    m.position.set(cx, fenceH / 2, cz);
    m.castShadow = true;
    group.add(m);
    colliders.push(aabb(cx, fenceH / 2, cz, Math.max(w, 0.1), fenceH, Math.max(d, 0.1)));
  }
  const YMIN = -9, YMAX = 17, XMIN = -5, XMAX = 17;
  // front fence with path gap
  fence(XMIN, YMIN, 5.0, YMIN);
  fence(7.0, YMIN, XMAX, YMIN);
  fence(XMIN, YMAX, XMAX, YMAX);   // back
  fence(XMIN, YMIN, XMIN, YMAX);   // west
  fence(XMAX, YMIN, XMAX, YMAX);   // east

  // ---- treeline: low-poly conifers, densest to the east (bedroom window) ----
  const treePositions = [];
  const rng = mulberry32(1337);
  function conifer(x, z, s) {
    const t = new THREE.Group();
    const trunk = box(0.12 * s, 0.6 * s, 0.12 * s, matTree);
    trunk.position.y = 0.3 * s;
    t.add(trunk);
    for (let i = 0; i < 3; i++) {
      const cone = new THREE.Mesh(new THREE.ConeGeometry(0.7 * s - i * 0.18 * s, 1.0 * s, 6), matTree);
      cone.position.y = (0.7 + i * 0.55) * s;
      cone.castShadow = true;
      t.add(cone);
    }
    t.position.set(x, 0, z);
    t.rotation.y = rng() * Math.PI;
    group.add(t);
    treePositions.push(new THREE.Vector3(x, 0, z));
  }
  // east treeline (facing bedroom window)
  for (let i = 0; i < 7; i++) conifer(15.0 + rng() * 1.5, -6 + i * 3.2 + rng(), 1.6 + rng() * 0.8);
  // back treeline
  for (let i = 0; i < 8; i++) conifer(-3 + i * 3 + rng(), 15.5 + rng() * 1.2, 1.5 + rng() * 0.9);
  // a couple to the west
  for (let i = 0; i < 4; i++) conifer(-4.0 - rng(), 0 + i * 4 + rng(), 1.6 + rng());

  // ---- breaker box on the north exterior wall, east corner (the dark side) ----
  const breakerGroup = new THREE.Group();
  const bboxMesh = box(0.4, 0.55, 0.12, matMetal);
  bboxMesh.position.set(0, 1.4, 0);
  bboxMesh.castShadow = true;
  breakerGroup.add(bboxMesh);
  const bdoor = box(0.36, 0.5, 0.03, matWood);
  bdoor.position.set(0, 1.4, 0.08);
  breakerGroup.add(bdoor);
  const bswitch = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.12, 0.04),
    new THREE.MeshStandardMaterial({ color: PAL.light, roughness: 1 }));
  bswitch.position.set(0, 1.4, 0.12);
  breakerGroup.add(bswitch);
  breakerGroup.position.set(11, 0, 14.15); // just outside the north wall
  group.add(breakerGroup);

  return {
    group,
    colliders,
    porchLight,
    breaker: { group: breakerGroup, switch: bswitch, position: new THREE.Vector3(11, 1.4, 14.15) },
    treePositions,
  };
}

// tiny deterministic PRNG so the treeline is the same every load
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
