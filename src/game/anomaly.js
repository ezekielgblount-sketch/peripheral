import { RESOLVE_DWELL, SPENT_COOLDOWN_MIN, SPENT_COOLDOWN_MAX, FOVEA_HYST_COS, FOVEA_COS } from '../constants.js';

// The anomaly state machine, one instance per anomaly-capable prop.
//
//   DORMANT   -> the Director may select it
//   ARMED     -> chosen, but not yet wrong. Flips to the off-state ONLY on a
//                frame where the fovea is >40deg away OR the prop is occluded.
//                Never flips near screen centre.
//   ACTIVE    -> visibly wrong. Waits here indefinitely.
//   RESOLVING -> the fovea has rested within 11deg, unoccluded, for >0.12s.
//                On the very NEXT frame it snaps to normal in a single frame:
//                no tween, no sound, no animation.
//   SPENT     -> cools down 60-120s and may only re-arm from a different room.
//
// The prop must be given setOff()/setNormal() that are instantaneous.

export const State = {
  DORMANT: 'DORMANT', ARMED: 'ARMED', ACTIVE: 'ACTIVE', RESOLVING: 'RESOLVING', SPENT: 'SPENT',
};

export class Anomaly {
  constructor(prop) {
    this.prop = prop;          // { root, getAnchor(), setOff(), setNormal(), room }
    this.state = State.DORMANT;
    this.dwell = 0;
    this.spentTimer = 0;
    this.spentRoom = null;
    this._anchor = prop.getAnchor();
  }

  get room() { return this.prop.room; }

  arm() {
    if (this.state === State.DORMANT) {
      this.state = State.ARMED;
      return true;
    }
    return false;
  }

  // Force back to normal + dormant (used on act reset).
  forceNormal() {
    this.prop.setNormal();
    this.state = State.DORMANT;
    this.dwell = 0;
  }

  update(dt, fovea, player) {
    const anchor = this.prop.getAnchor(this._anchor);
    const currentRoom = player.currentRoom;

    switch (this.state) {
      case State.ARMED: {
        // Only flip where the player cannot possibly witness it.
        const safe = fovea.beyondArmAngle(anchor) || fovea.occluded(anchor, this.prop.root);
        if (safe) {
          this.prop.setOff();
          this.state = State.ACTIVE;
          this.dwell = 0;
        }
        break;
      }
      case State.ACTIVE: {
        // Hysteresis: once a look has begun, tolerate a little drift so a prop
        // hovering at the 11deg boundary doesn't flicker the dwell timer.
        const cos = fovea.cosTo(anchor);
        const threshold = this.dwell > 0 ? FOVEA_HYST_COS : FOVEA_COS;
        const looked = cos >= threshold && !fovea.occluded(anchor, this.prop.root);
        if (looked) {
          this.dwell += dt;
          if (this.dwell >= RESOLVE_DWELL) this.state = State.RESOLVING;
        } else {
          this.dwell = 0;
        }
        break;
      }
      case State.RESOLVING: {
        // One frame, right now. It must look like it was never anything else.
        this.prop.setNormal();
        this.state = State.SPENT;
        this.spentRoom = currentRoom;
        this.spentTimer = SPENT_COOLDOWN_MIN + Math.random() * (SPENT_COOLDOWN_MAX - SPENT_COOLDOWN_MIN);
        this.dwell = 0;
        break;
      }
      case State.SPENT: {
        this.spentTimer -= dt;
        if (this.spentTimer <= 0 && currentRoom && currentRoom !== this.spentRoom) {
          this.state = State.DORMANT;
        }
        break;
      }
      default:
        break; // DORMANT: nothing until armed
    }
  }
}
