import * as THREE from 'three';

// PlayerProfile samples every frame and keeps rolling stats about how this
// particular player looks and moves. It is deliberately just a stats object and
// a histogram — no learning, no models — but it is real, and the Director uses
// it to place anomalies in the angular zones this player habitually neglects.
//
// Exposed on window.__profile in dev builds.

const AZ_BINS = 12;   // azimuth around movement heading, 30deg each
const EL_BINS = 5;    // elevation, from about -60 to +60 deg

export class PlayerProfile {
  constructor(rooms) {
    this.rooms = rooms;

    this.yawVelMean = 0;    // EMA of |yaw rate| (rad/s)
    this.yawVelPeak = 0;
    this._prevYaw = null;

    // dwell histogram: where the fovea rests, relative to movement heading
    this.dwell = new Float32Array(AZ_BINS * EL_BINS);
    this.dwellTotal = 0;

    this.heading = 0;        // smoothed movement heading (radians)
    this._hasHeading = false;

    this.roomTime = Object.create(null);
    this.visitOrder = [];
    this.currentRoom = null;
    this._roomTimer = 0;      // time since entering current room
    this._roomYawAccum = 0;   // yaw turned since entering (for check-behind)
    this.roomEntries = 0;
    this.checkBehinds = 0;

    this.edgeProximityEMA = 0.5; // 0 = centre of rooms, 1 = hugging walls

    this._tmp = new THREE.Vector3();
  }

  get checkBehindRate() {
    return this.roomEntries > 0 ? this.checkBehinds / this.roomEntries : 0;
  }
  get hugsWalls() { return this.edgeProximityEMA > 0.6; }
  get isFastTwitcher() { return this.yawVelMean > 1.4; }

  sample(dt, player, fovea) {
    // --- yaw velocity ---
    if (this._prevYaw !== null) {
      let d = Math.abs(player.yaw - this._prevYaw);
      if (d > Math.PI) d = Math.abs(d - 2 * Math.PI);
      const rate = d / Math.max(dt, 1e-4);
      this.yawVelMean = this.yawVelMean * 0.97 + rate * 0.03;
      if (rate > this.yawVelPeak) this.yawVelPeak = rate;
      this._roomYawAccum += d;
    }
    this._prevYaw = player.yaw;

    // --- movement heading (smoothed) ---
    const speed = player.speedThisFrame;
    if (speed > 0.15) {
      const vx = player.pos.x - player._prevPos.x; // note _prevPos updated after; use forward-ish
      // use forward projected on XZ as heading proxy when moving forward,
      // but better: derive from yaw + input intent. We approximate with facing.
      const hx = -Math.sin(player.yaw), hz = -Math.cos(player.yaw);
      const target = Math.atan2(hx, hz);
      this.heading = this._hasHeading ? angleLerp(this.heading, target, 0.1) : target;
      this._hasHeading = true;
    }

    // --- dwell histogram (fovea direction relative to heading) ---
    const f = fovea.forward;
    const az = wrapPi(Math.atan2(f.x, f.z) - this.heading + Math.PI); // 0..2pi-ish after wrap below
    const azNorm = (wrapPi(Math.atan2(f.x, f.z) - (this.heading + Math.PI)) + Math.PI) / (2 * Math.PI);
    const el = Math.asin(THREE.MathUtils.clamp(f.y, -1, 1)); // -pi/2..pi/2
    const ai = clampBin(Math.floor(azNorm * AZ_BINS), AZ_BINS);
    const elNorm = THREE.MathUtils.clamp((el + Math.PI / 3) / ((2 * Math.PI) / 3), 0, 0.999);
    const ei = clampBin(Math.floor(elNorm * EL_BINS), EL_BINS);
    this.dwell[ai * EL_BINS + ei] += dt;
    this.dwellTotal += dt;

    // --- rooms ---
    const room = this._roomAt(player.pos.x, player.pos.z);
    player.currentRoom = room;
    if (room !== this.currentRoom) {
      // finalize previous room's check-behind judgement
      if (this.currentRoom && this._roomTimer <= 3 && this._roomYawAccum > (120 * Math.PI / 180)) {
        this.checkBehinds++;
      }
      this.currentRoom = room;
      if (room) {
        this.roomEntries++;
        this.visitOrder.push(room);
      }
      this._roomTimer = 0;
      this._roomYawAccum = 0;
    } else if (room) {
      this.roomTime[room] = (this.roomTime[room] || 0) + dt;
      this._roomTimer += dt;
      // if the check-behind happens within 3s, count it once
      if (this._roomTimer <= 3 && this._roomYawAccum > (120 * Math.PI / 180)) {
        this.checkBehinds++;
        this._roomYawAccum = -1e9; // don't double count
      }
    }

    // --- wall hugging ---
    if (room) {
      const b = this.rooms.find((r) => r.name === room);
      if (b) {
        const cx = (b.min.x + b.max.x) / 2, cz = (b.min.z + b.max.z) / 2;
        const hw = (b.max.x - b.min.x) / 2, hd = (b.max.z - b.min.z) / 2;
        const nx = Math.min(1, Math.abs(player.pos.x - cx) / Math.max(hw, 0.1));
        const nz = Math.min(1, Math.abs(player.pos.z - cz) / Math.max(hd, 0.1));
        const edge = Math.max(nx, nz);
        this.edgeProximityEMA = this.edgeProximityEMA * 0.98 + edge * 0.02;
      }
    }
  }

  _roomAt(x, z) {
    for (const r of this.rooms) {
      if (x >= r.min.x && x <= r.max.x && z >= r.min.z && z <= r.max.z) return r.name;
    }
    return null;
  }

  // Neglect score in [0..1] for a world position: how rarely the player's fovea
  // rests in the angular zone this position occupies (relative to heading).
  // 1 = strongly neglected, good place to hide something.
  neglectFor(eye, worldPos) {
    if (this.dwellTotal < 1) return 0.5; // not enough data yet
    this._tmp.copy(worldPos).sub(eye);
    if (this._tmp.lengthSq() < 1e-6) return 0.5;
    this._tmp.normalize();
    const azNorm = (wrapPi(Math.atan2(this._tmp.x, this._tmp.z) - (this.heading + Math.PI)) + Math.PI) / (2 * Math.PI);
    const el = Math.asin(THREE.MathUtils.clamp(this._tmp.y, -1, 1));
    const ai = clampBin(Math.floor(azNorm * AZ_BINS), AZ_BINS);
    const elNorm = THREE.MathUtils.clamp((el + Math.PI / 3) / ((2 * Math.PI) / 3), 0, 0.999);
    const ei = clampBin(Math.floor(elNorm * EL_BINS), EL_BINS);
    const bin = this.dwell[ai * EL_BINS + ei];
    const expected = this.dwellTotal / (AZ_BINS * EL_BINS);
    const ratio = bin / Math.max(expected, 1e-4);
    return 1 / (1 + ratio); // below-average bins score > 0.5
  }
}

function clampBin(i, n) { return Math.max(0, Math.min(n - 1, i)); }
function wrapPi(a) { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; }
function angleLerp(a, b, t) {
  let d = wrapPi(b - a);
  return a + d * t;
}
