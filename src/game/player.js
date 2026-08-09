import * as THREE from 'three';
import { resolve } from '../core/collision.js';
import {
  EYE_H, PLAYER_RADIUS, PLAYER_HEIGHT, WALK_SPEED, SLOW_SPEED, PAL,
} from '../constants.js';

// First-person controller: yaw/pitch camera, WASD movement resolved against the
// world colliders, and (Act 2) a flashlight rig parented to the camera.
export class Player {
  constructor(camera) {
    this.camera = camera;
    this.pos = new THREE.Vector3(0, 0, 0); // foot position
    this.yaw = 0;   // radians, around +Y
    this.pitch = 0; // radians, clamped
    this.velY = 0;

    // Look direction cache, refreshed each update.
    this.forward = new THREE.Vector3(0, 0, -1);

    this.colliders = [];
    this.walkSurface = 'wood'; // 'wood' | 'gravel' — set by the act for footsteps

    this._prevPos = this.pos.clone();
    this.speedThisFrame = 0;

    this._buildFlashlight();
  }

  _buildFlashlight() {
    // A tight warm cone plus a faint wide falloff so the player is not fully blind.
    this.flashGroup = new THREE.Group();
    const spot = new THREE.SpotLight(PAL.warm, 0, 22, THREE.MathUtils.degToRad(22), 0.55, 1.4);
    spot.castShadow = true;
    spot.shadow.mapSize.set(1024, 1024);
    spot.shadow.camera.near = 0.2;
    spot.shadow.camera.far = 22;
    spot.position.set(0, 0, 0);
    spot.target.position.set(0, 0, -1);
    this.flashGroup.add(spot);
    this.flashGroup.add(spot.target);

    // Wide, very weak fill so surfaces just outside the beam are barely readable.
    const fill = new THREE.SpotLight(PAL.warm, 0, 10, THREE.MathUtils.degToRad(55), 1.0, 1.0);
    fill.castShadow = false;
    fill.target.position.set(0, 0, -1);
    this.flashGroup.add(fill);
    this.flashGroup.add(fill.target);

    this.flashSpot = spot;
    this.flashFill = fill;
    this.flashOn = false;
  }

  attachFlashlight(camera) {
    if (this.flashGroup.parent !== camera) camera.add(this.flashGroup);
  }

  setFlashlight(on) {
    this.flashOn = on;
    this.flashSpot.intensity = on ? 6.0 : 0;
    this.flashFill.intensity = on ? 0.6 : 0;
  }

  spawn(x, z, yaw = 0) {
    this.pos.set(x, 0, z);
    this._prevPos.copy(this.pos);
    this.yaw = yaw;
    this.pitch = 0;
    this._syncCamera();
  }

  look(dx, dy) {
    this.yaw -= dx;
    this.pitch -= dy;
    const lim = Math.PI / 2 - 0.02;
    this.pitch = Math.max(-lim, Math.min(lim, this.pitch));
  }

  update(dt, input, opts = {}) {
    const canMove = opts.canMove !== false;

    if (canMove) {
      const axis = input.moveAxis();
      const slow = input.isDown('ShiftLeft') || input.isDown('ShiftRight');
      const speed = slow ? SLOW_SPEED : WALK_SPEED;

      // Move relative to yaw only (no flying with pitch).
      const sin = Math.sin(this.yaw), cos = Math.cos(this.yaw);
      // forward vector on XZ: (-sin, -cos) points where yaw faces
      const fx = -sin, fz = -cos;
      const rx = cos, rz = -sin;

      let mx = fx * axis.z + rx * axis.x;
      let mz = fz * axis.z + rz * axis.x;
      const len = Math.hypot(mx, mz);
      if (len > 1e-5) { mx /= len; mz /= len; }

      this.pos.x += mx * speed * dt;
      this.pos.z += mz * speed * dt;

      resolve(this.pos, PLAYER_RADIUS, 0.05, PLAYER_HEIGHT, this.colliders);
    }

    this.speedThisFrame = this.pos.distanceTo(this._prevPos) / dt;
    this._prevPos.copy(this.pos);

    this._syncCamera();
  }

  _syncCamera() {
    this.camera.position.set(this.pos.x, this.pos.y + EYE_H, this.pos.z);
    this.camera.rotation.set(0, 0, 0);
    this.camera.rotateY(this.yaw);
    this.camera.rotateX(this.pitch);
    this.camera.getWorldDirection(this.forward);
  }

  eyePosition(out = new THREE.Vector3()) {
    return out.set(this.pos.x, this.pos.y + EYE_H, this.pos.z);
  }
}
