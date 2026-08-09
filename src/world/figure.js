import * as THREE from 'three';

// One standing humanoid, built from boxes, feet planted at y=0 so it never
// floats. Reused for the Act 2 entity and every "a figure is there" anomaly, so
// the thing you glimpse in the mirror, the treeline, and the dark is always the
// same silhouette — that consistency is what makes it read as one presence.
//
// It is deliberately still and featureless: no face, slightly hunched, arms at
// its sides. opts.scale scales the whole figure about its feet.

export function makeFigure(opts = {}) {
  const scale = opts.scale ?? 1;
  const color = opts.color ?? 0x080807;
  const mat = new THREE.MeshStandardMaterial({ color, roughness: 1, metalness: 0 });
  const g = new THREE.Group();
  const box = (w, h, d, y, x = 0, z = 0) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    m.position.set(x, y, z);
    m.castShadow = true;
    g.add(m);
    return m;
  };

  // legs (feet on the ground)
  box(0.16, 0.9, 0.18, 0.45, -0.11);
  box(0.16, 0.9, 0.18, 0.45, 0.11);
  // torso, tapering slightly, leaning a hair forward
  const torso = box(0.42, 0.62, 0.24, 1.2);
  torso.rotation.x = 0.06;
  // shoulders
  box(0.5, 0.14, 0.24, 1.48);
  // arms hanging at the sides
  box(0.12, 0.62, 0.14, 1.2, -0.31);
  box(0.12, 0.62, 0.14, 1.2, 0.31);
  // neck + head
  box(0.1, 0.1, 0.1, 1.58);
  box(0.26, 0.3, 0.25, 1.78);

  // anchor at chest height for fovea/occlusion math
  const anchor = new THREE.Object3D();
  anchor.position.y = 1.4;
  g.add(anchor);
  g.userData.anchor = anchor;

  g.scale.setScalar(scale);
  return g;
}

// Convenience: world-space anchor getter for a figure group.
export function figureAnchor(figure, out = new THREE.Vector3()) {
  return figure.userData.anchor.getWorldPosition(out);
}
