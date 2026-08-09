import * as THREE from 'three';

// Capsule (vertical) vs axis-aligned box collision.
// The player is modelled as a vertical capsule of radius r whose axis runs from
// footY to footY+height. For a level with no slopes and no low overhangs the
// horizontal problem reduces to circle-vs-rectangle in the XZ plane, which is
// what we solve here. We resolve against each AABB by pushing the circle centre
// out along the axis of least penetration. Iterate a couple of times so corners
// and multi-wall wedges settle.

const _closest = new THREE.Vector2();

// aabbs: array of { min:{x,y,z}, max:{x,y,z} }. Only XZ + Y-overlap is used.
export function resolve(pos, radius, footY, height, aabbs) {
  const topY = footY + height;
  for (let iter = 0; iter < 3; iter++) {
    let moved = false;
    for (let i = 0; i < aabbs.length; i++) {
      const b = aabbs[i];
      // Vertical overlap test — lets us step over/under things that don't span eye range.
      if (b.max.y <= footY || b.min.y >= topY) continue;

      // Closest point on the rectangle to the circle centre.
      const cx = Math.max(b.min.x, Math.min(pos.x, b.max.x));
      const cz = Math.max(b.min.z, Math.min(pos.z, b.max.z));
      let dx = pos.x - cx;
      let dz = pos.z - cz;
      let d2 = dx * dx + dz * dz;

      if (d2 > radius * radius) continue; // no overlap

      if (d2 > 1e-9) {
        const d = Math.sqrt(d2);
        const push = radius - d;
        pos.x += (dx / d) * push;
        pos.z += (dz / d) * push;
      } else {
        // Centre is inside the box: push out along the shallowest face.
        const toLeft = pos.x - b.min.x;
        const toRight = b.max.x - pos.x;
        const toNear = pos.z - b.min.z;
        const toFar = b.max.z - pos.z;
        const m = Math.min(toLeft, toRight, toNear, toFar);
        if (m === toLeft) pos.x = b.min.x - radius;
        else if (m === toRight) pos.x = b.max.x + radius;
        else if (m === toNear) pos.z = b.min.z - radius;
        else pos.z = b.max.z + radius;
      }
      moved = true;
    }
    if (!moved) break;
  }
}

// Build an AABB from a box mesh's world transform (assumes axis-aligned box).
export function aabbFromBox(mesh) {
  mesh.updateWorldMatrix(true, false);
  const box = new THREE.Box3().setFromObject(mesh);
  return {
    min: { x: box.min.x, y: box.min.y, z: box.min.z },
    max: { x: box.max.x, y: box.max.y, z: box.max.z },
  };
}

// Convenience: AABB from centre + size.
export function aabb(cx, cy, cz, sx, sy, sz) {
  return {
    min: { x: cx - sx / 2, y: cy - sy / 2, z: cz - sz / 2 },
    max: { x: cx + sx / 2, y: cy + sy / 2, z: cz + sz / 2 },
  };
}
