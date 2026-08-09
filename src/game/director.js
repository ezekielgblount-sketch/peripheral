import * as THREE from 'three';
import { ARM_INTERVAL_MIN, ARM_INTERVAL_MAX } from '../constants.js';
import { State } from './anomaly.js';

// The Director decides what goes wrong and when. It arms one anomaly every
// 25-40s during Act 1, biasing its choice toward the angular zones the player
// habitually neglects (via PlayerProfile) so the game works the player's blind
// spots instead of rewarding wherever they already look.

export class Director {
  constructor(profile, props, fovea) {
    this.profile = profile;
    this.props = props;
    this.fovea = fovea;
    this.enabled = false;
    this.timer = this._nextInterval();
    this._eye = new THREE.Vector3();
    this._anchor = new THREE.Vector3();
    this.armedCount = 0;
  }

  _nextInterval() {
    // Fast twitchers get a slightly quicker cadence; slow sweepers a slower one.
    const bias = this.profile.isFastTwitcher ? -4 : (this.profile.yawVelMean < 0.5 ? 4 : 0);
    const base = ARM_INTERVAL_MIN + Math.random() * (ARM_INTERVAL_MAX - ARM_INTERVAL_MIN);
    return Math.max(18, base + bias);
  }

  setEnabled(on) { this.enabled = on; if (on) this.timer = 8; } // first one comes fairly soon

  update(dt, player, act) {
    if (!this.enabled || act !== 1) return;
    this.timer -= dt;
    if (this.timer > 0) return;
    this.timer = this._nextInterval();
    this._armOne(player);
  }

  _armOne(player) {
    player.eyePosition(this._eye);
    const candidates = [];
    let wsum = 0;
    for (const p of this.props.list) {
      if (p.anomaly.state !== State.DORMANT) continue;
      p.getAnchor(this._anchor);
      const neglect = this.profile.neglectFor(this._eye, this._anchor);
      // avoid arming something the player is staring straight at right now
      const cos = this.fovea.cosTo(this._anchor);
      const inViewPenalty = cos > 0.9 ? 0.15 : 1.0;
      // gently prefer arming outside the current room so the reveal is a return
      const roomBonus = p.room === player.currentRoom ? 0.7 : 1.0;
      const w = (0.15 + neglect) * inViewPenalty * roomBonus;
      candidates.push({ p, w });
      wsum += w;
    }
    if (candidates.length === 0) return;

    let r = Math.random() * wsum;
    for (const c of candidates) {
      r -= c.w;
      if (r <= 0) {
        if (c.p.anomaly.arm()) this.armedCount++;
        return;
      }
    }
    candidates[0].p.anomaly.arm();
  }
}
