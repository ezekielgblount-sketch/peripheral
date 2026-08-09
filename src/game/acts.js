import * as THREE from 'three';
import { PAL, CRICKET_STOP_DIST, CRICKET_RESUME_DELAY, FOVEA_COS } from '../constants.js';
import { setAct, powerOn } from '../world/lighting.js';
import { makeFigure } from '../world/figure.js';
import { State } from './anomaly.js';

// Act flow: Act 1 (settling in), the transition, Act 2 (the power), and the
// ending. Owns the small amount of scripted state — spawn points, objective
// lines, the wake-up camera righting, and the Act 2 entity.

export class Acts {
  constructor(game) {
    this.g = game;
    this.currentAct = 0;
    this.canMove = true;
    this.lockLook = false;
    this.phase = 'none';

    this._timeInside = false;
    this._insideTimer = 0;
    this._objShown = false;

    this._buildEntity();
    this._registerInteractables();
  }

  _buildEntity() {
    const g = makeFigure({ scale: 1.02, color: 0x070706 });
    const anchor = g.userData.anchor;
    g.visible = false;
    this.g.scene.add(g);
    this.entity = {
      group: g, anchor,
      dist: 14,
      cooldown: 2,
      nearTimer: CRICKET_RESUME_DELAY, // starts "gone"
      _v: new THREE.Vector3(),
      getAnchor: (v = new THREE.Vector3()) => anchor.getWorldPosition(v),
    };
  }

  _registerInteractables() {
    // Act 1 chores: guide the player through settling in. These never gate the
    // bed — a beeliner can still sleep immediately — they just give the night
    // somewhere to go while the house works on them.
    this.chores = { unpack: false, shower: false };
    this.choreDresser = this.g.registerInteractable({
      position: this.g.props.dresser.position.clone(),
      radius: 1.7, label: 'Unpack your clothes', enabled: false,
      onInteract: () => this._doChore('unpack'),
    });
    this.choreShower = this.g.registerInteractable({
      position: this.g.props.shower.position.clone(),
      radius: 1.7, label: 'Take a shower', enabled: false,
      onInteract: () => this._doChore('shower'),
    });

    // bed ends Act 1
    this.bedIt = this.g.registerInteractable({
      position: this.g.house.anchors.bed.clone().add(new THREE.Vector3(0, 0.75, 0)),
      radius: 2.0,
      label: 'Sleep',
      enabled: false,
      onInteract: () => this._endAct1(),
    });
    // breaker ends the build (Act 2)
    this.breakerIt = this.g.registerInteractable({
      position: this.g.yard.breaker.position.clone(),
      radius: 2.0,
      label: 'Flip the breaker',
      enabled: false,
      onInteract: () => this._flipBreaker(),
    });
  }

  begin() {
    this.reset();
    this.currentAct = 1;
    this.phase = 'act1';
    setAct(this.g.lighting, 1);
    this.g.scene.background = new THREE.Color(0x9a978d); // flat grey daylight
    this.g.scene.fog = new THREE.Fog(0x9a978d, 8, 40);
    this.g.peripheral.setAmount(0.85);
    this.g.player.spawn(6, -6, Math.PI); // on the path, facing the door (+z)
    this.g.player.setFlashlight(false);
    this.bedIt.enabled = true;
    this.breakerIt.enabled = false;
    this.choreDresser.enabled = true;
    this.choreShower.enabled = true;
    this.chores.unpack = false;
    this.chores.shower = false;
    this.g.audio.setCrickets(false);
    this.g.audio.setHouseTone(false);
    this._insideTimer = 0;
    this._objShown = false;
  }

  _doChore(name) {
    if (this.chores[name]) return;
    this.chores[name] = true;
    this.g.audio.thud();
    if (name === 'unpack') { this.g.props.dresser.open(); this.choreDresser.enabled = false; }
    if (name === 'shower') { this.choreShower.enabled = false; }
    const left = (!this.chores.unpack ? 1 : 0) + (!this.chores.shower ? 1 : 0);
    if (left === 0) this.g.hud.objective('Now get some sleep.', 8000);
    else if (name === 'unpack') this.g.hud.objective('Clothes away. Wash up before bed.', 6000);
    else this.g.hud.objective('Clean. Unpack, then get some sleep.', 6000);
  }

  reset() {
    this.currentAct = 0;
    this.phase = 'none';
    this.canMove = true;
    this.lockLook = false;
    // put every anomaly back to normal/dormant
    for (const p of this.g.props.list) p.anomaly.forceNormal();
    this.g.director.enabled = false;
    this.entity.group.visible = false;
    this.entity.dist = 14;
    this.entity.cooldown = 2;
    if (this.bedIt) this.bedIt.enabled = false;
    if (this.breakerIt) this.breakerIt.enabled = false;
    if (this.choreDresser) this.choreDresser.enabled = false;
    if (this.choreShower) this.choreShower.enabled = false;
    this.g.player.setFlashlight(false);
    this.g.hud.setFadeInstant(0);
  }

  update(dt) {
    // surface for footsteps
    this.g.player.walkSurface = this.g.player.currentRoom ? 'wood' : 'gravel';

    if (this.phase === 'act1') this._updateAct1(dt);
    else if (this.phase === 'act2') this._updateAct2(dt);
    else if (this.phase === 'wake') this._updateWake(dt);
  }

  _updateAct1(dt) {
    const inside = !!this.g.player.currentRoom;
    if (inside && !this._timeInside) {
      this._timeInside = true;
      this.g.audio.setHouseTone(true);
      this.g.audio.setAmbient('act1');
      this.g.director.setEnabled(true);
    }
    if (inside) {
      this._insideTimer += dt;
      if (!this._objShown && this._insideTimer > 8) {
        this._objShown = true;
        this.g.hud.objective('Settle in. Unpack, wash up, then get some sleep.', 8000);
      }
    }
  }

  async _endAct1() {
    if (this.phase !== 'act1') return;
    this.phase = 'transition';
    this.canMove = false;
    this.lockLook = true;
    this.g.director.enabled = false;
    this.bedIt.enabled = false;
    this.choreDresser.enabled = false;
    this.choreShower.enabled = false;
    this.g.hud.setPrompt('');
    this.g.hud.clearObjective();

    await this.g.hud.fadeTo(1, 1200);      // to black
    this.g.audio.setHouseTone(false);
    this.g.audio.setAmbient('off');         // silence for the transition
    await wait(3000);                       // held silence
    this.g.audio.swell();                   // single low sub-bass swell
    await wait(2600);
    this._setupAct2();
  }

  _setupAct2() {
    this.currentAct = 2;
    // dark everywhere
    setAct(this.g.lighting, 2);
    this.g.scene.background = new THREE.Color(0x05060a);
    this.g.scene.fog = new THREE.Fog(0x05060a, 3, 22);
    this.g.peripheral.setAmount(1.0);

    // wake on the study floor at a wrong angle, righting over ~2s
    const w = this.g.house.anchors.studyWake;
    this.g.player.spawn(w.x, w.z, Math.PI * 0.15);
    this.g.player.pitch = -0.55;          // looking down/tilted
    this._wakeRoll = 0.5;                  // fake roll via camera
    this._wakeT = 0;
    this.g.player.setFlashlight(true);

    // clear any Act 1 anomalies, then arm the Act-2-only yard sign so it drops
    // to its blank state while the player is inside / not looking at it.
    for (const p of this.g.props.list) p.anomaly.forceNormal();
    this.g.signage.yardSign.anomaly.arm();

    this.g.audio.setCrickets(true);        // will be gated by proximity
    this.g.audio.setAmbient('act2');       // sparser, lower piano at night
    this.breakerIt.enabled = true;
    this.entity.group.visible = false;
    this.entity.dist = 14;
    this.entity.cooldown = 3;
    this.entity.nearTimer = CRICKET_RESUME_DELAY;

    this.phase = 'wake';
    this.canMove = false;
    this.lockLook = true;
    this.g.hud.fadeTo(0, 1600);
  }

  _updateWake(dt) {
    this._wakeT += dt;
    const t = Math.min(1, this._wakeT / 2.0);
    const ease = 1 - Math.pow(1 - t, 3);
    this.g.player.pitch = -0.55 * (1 - ease);
    // apply a decaying roll on the camera
    this.g.camera.rotation.z = this._wakeRoll * (1 - ease);
    if (t >= 1) {
      this.g.camera.rotation.z = 0;
      this.phase = 'act2';
      this.canMove = true;
      this.lockLook = false;
      this.g.hud.objective('The breaker is outside.', 8000);
    }
  }

  _updateAct2(dt) {
    this._updateEntity(dt);
  }

  _updateEntity(dt) {
    const e = this.entity;
    const eye = this.g.player.eyePosition();
    const fovea = this.g.fovea;

    if (e.group.visible) {
      e.getAnchor(e._v);
      const dist = e._v.distanceTo(eye);
      const centred = fovea.cosTo(e._v) >= FOVEA_COS && !fovea.occluded(e._v, e.group);
      const unoccludedNear = dist < CRICKET_STOP_DIST && !fovea.occluded(e._v, e.group);

      if (centred) {
        // Removed the frame it is centred. Comes back closer.
        e.group.visible = false;
        e.cooldown = 3 + Math.random() * 3;
        e.dist = Math.max(4, e.dist - 2.0);
        e.nearTimer = 0; // it just left; start the resume countdown
      } else {
        // crickets stop while it is near and unoccluded
        if (unoccludedNear) { e.nearTimer = 0; this.g.audio.setCrickets(false); }
        else { e.nearTimer += dt; if (e.nearTimer > CRICKET_RESUME_DELAY) this.g.audio.setCrickets(true); }
      }
    } else {
      e.nearTimer += dt;
      if (e.nearTimer > CRICKET_RESUME_DELAY) this.g.audio.setCrickets(true);
      e.cooldown -= dt;
      if (e.cooldown <= 0) this._placeEntity();
    }
  }

  // Put the entity somewhere the player is not looking: a peripheral/behind angle
  // on the ground, at the current approach distance, clamped to the yard.
  _placeEntity() {
    const e = this.entity;
    const player = this.g.player;
    const eye = player.eyePosition();
    // choose an angle at least ~55deg off the current forward, biased behind
    for (let tries = 0; tries < 12; tries++) {
      const off = THREE.MathUtils.degToRad(55 + Math.random() * 110) * (Math.random() < 0.5 ? 1 : -1);
      const ang = player.yaw + off;
      const dx = -Math.sin(ang), dz = -Math.cos(ang);
      const x = eye.x + dx * e.dist;
      const z = eye.z + dz * e.dist;
      // keep it within the fenced yard and out of the house footprint-ish
      if (x < -4 || x > 16 || z < -8 || z > 16) continue;
      e.group.position.set(x, 0, z);
      e.getAnchor(e._v);
      // make sure it is genuinely outside the fovea at spawn
      if (this.g.fovea.cosTo(e._v) >= Math.cos(THREE.MathUtils.degToRad(42))) continue;
      // face the player
      e.group.rotation.y = Math.atan2(eye.x - x, eye.z - z);
      e.group.visible = true;
      return;
    }
    // if no good spot, try again shortly
    e.cooldown = 1.0;
  }

  _flipBreaker() {
    if (this.phase !== 'act2') return;
    this.phase = 'ending';
    this.g.audio.clack();
    powerOn(this.g.lighting);
    this.g.scene.background = new THREE.Color(0x1a1916);
    this.g.scene.fog = new THREE.Fog(0x1a1916, 8, 40);
    this.entity.group.visible = false;
    this.g.audio.setCrickets(true);     // return loudly
    this.g.audio.cricketLevel = 1;       // snap up
    this.g.hud.objective('', 1);
    this._endSoon();
  }

  async _endSoon() {
    await wait(1600);
    await this.g.hud.fadeTo(1, 900);
    this.g.endBuild();
    this.g.hud.setFadeInstant(0);
  }
}

function wait(ms) { return new Promise((r) => setTimeout(r, ms)); }
