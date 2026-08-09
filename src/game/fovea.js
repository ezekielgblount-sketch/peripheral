import * as THREE from 'three';
import { FOVEA_COS, NEAR_PERI_COS, ARM_MIN_COS } from '../constants.js';

// Everything about "where is the player actually looking". This is pure logic —
// it never touches the peripheral shader. Anomalies decide when to flip using
// these angle tests and the occlusion raycast, so a screenshot-and-zoom can
// never reveal a change: the world genuinely is what it looks like.

export class Fovea {
  constructor(camera, scene) {
    this.camera = camera;
    this.scene = scene;
    this.eye = new THREE.Vector3();
    this.forward = new THREE.Vector3(0, 0, -1);
    this.ray = new THREE.Raycaster();
    this.ray.far = 40;
    this._tmp = new THREE.Vector3();
  }

  beginFrame(player) {
    player.eyePosition(this.eye);
    this.forward.copy(player.forward).normalize();
  }

  // cosine of the angle between forward and the direction to a world point.
  // 1 = dead centre, decreasing as it moves to the periphery.
  cosTo(worldPos) {
    this._tmp.copy(worldPos).sub(this.eye);
    const len = this._tmp.length();
    if (len < 1e-5) return 1;
    this._tmp.multiplyScalar(1 / len);
    return this._tmp.dot(this.forward);
  }

  angleDegTo(worldPos) {
    return THREE.MathUtils.radToDeg(Math.acos(Math.min(1, Math.max(-1, this.cosTo(worldPos)))));
  }

  inFovea(worldPos, cos = FOVEA_COS) {
    return this.cosTo(worldPos) >= cos;
  }

  inNearPeriphery(worldPos) {
    const c = this.cosTo(worldPos);
    return c < FOVEA_COS && c >= NEAR_PERI_COS;
  }

  // true if the fovea is far enough away that an armed anomaly may safely flip.
  beyondArmAngle(worldPos) {
    return this.cosTo(worldPos) < ARM_MIN_COS;
  }

  // Is the straight line from the eye to worldPos blocked by anything that is
  // not part of `ignoreRoot`? Used both to confirm a look (resolve) and to allow
  // an off-screen flip when a prop is out of sight behind geometry.
  occluded(worldPos, ignoreRoot = null) {
    this._tmp.copy(worldPos).sub(this.eye);
    const dist = this._tmp.length();
    if (dist < 1e-4) return false;
    this._tmp.multiplyScalar(1 / dist);
    this.ray.set(this.eye, this._tmp);
    this.ray.far = dist - 0.06;
    const hits = this.ray.intersectObjects(this.scene.children, true);
    for (const h of hits) {
      if (!h.object.visible) continue;
      if (h.object.userData?.noOcclude) continue;
      if (ignoreRoot && isDescendant(h.object, ignoreRoot)) continue;
      if (h.distance < dist - 0.06) return true;
    }
    return false;
  }
}

function isDescendant(obj, root) {
  let o = obj;
  while (o) {
    if (o === root) return true;
    o = o.parent;
  }
  return false;
}
