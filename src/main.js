import * as THREE from 'three';
import { Renderer } from './core/renderer.js';
import { Input } from './core/input.js';
import { Loop } from './core/loop.js';
import { Player } from './game/player.js';
import { PeripheralPass } from './fx/peripheral.js';
import { Menu } from './ui/menu.js';
import { Hud } from './ui/hud.js';
import { buildHouse } from './world/house.js';
import { buildYard } from './world/yard.js';
import { buildLighting, setAct } from './world/lighting.js';
import { buildProps } from './world/props.js';
import { buildSignage } from './world/signage.js';
import { Fovea } from './game/fovea.js';
import { PlayerProfile } from './game/profile.js';
import { Director } from './game/director.js';
import { AudioEngine } from './core/audio.js';
import { Acts } from './game/acts.js';

class Game {
  constructor() {
    this.app = document.getElementById('app');
    this.renderer = new Renderer(this.app);
    this.input = new Input(this.renderer.domElement);
    this.menu = new Menu(this.app);
    this.hud = new Hud(this.app);
    this.audio = new AudioEngine();

    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0e0d0b);
    this.scene.fog = new THREE.Fog(0x0e0d0b, 10, 34);

    this.camera = new THREE.PerspectiveCamera(72, window.innerWidth / window.innerHeight, 0.05, 200);
    this.scene.add(this.camera);

    this.player = new Player(this.camera);
    this.player.attachFlashlight(this.camera);

    this.peripheral = new PeripheralPass();
    this.renderer.onResize((w, h) => {
      this.camera.aspect = w / h;
      this.camera.updateProjectionMatrix();
      this.peripheral.setSize(this.renderer.target.width, this.renderer.target.height);
    });
    this.peripheral.setSize(this.renderer.target.width, this.renderer.target.height);

    this._buildWorld();

    // interactables: { position:Vector3, radius, label, test?, onInteract }
    // Must exist before Acts, which registers the bed/breaker interactables.
    this.interactables = [];

    this.fovea = new Fovea(this.camera, this.scene);
    this.profile = new PlayerProfile(this.house.rooms);
    this.director = new Director(this.profile, this.props, this.fovea);
    this.acts = new Acts(this);

    if (import.meta.env.DEV) {
      window.__profile = this.profile;
      window.__game = this;
    }

    // Every real door in the house opens and closes. The bathroom door is
    // excluded — its angle is already driven by the anomaly state machine,
    // and letting the player fight that would just look broken — as is the
    // phantom fifth door, which the anomaly system controls entirely.
    this.frontDoorInteractable = this.registerDoorInteractable(
      this.house.frontDoor, this.house.anchors.frontDoor.clone().setY(1.0), 2.0,
    );
    this.registerDoorInteractable(this.props.doors.study, new THREE.Vector3(4.5, 1.0, 11.0), 1.7);
    this.registerDoorInteractable(this.props.doors.bedroom, new THREE.Vector3(7.5, 1.0, 7.0), 1.7);
    this.registerDoorInteractable(this.props.doors.utility, new THREE.Vector3(7.5, 1.0, 11.0), 1.7);

    this.state = 'menu';
    this.colliders = [...this.house.colliders, ...this.yard.colliders, ...this.signage.colliders];
    this.player.colliders = this.colliders;

    this.menu.onStart = () => this.start();
    this.menu.onResume = () => this.resume();
    this.menu.onExit = () => this.toMenu();
    this.input.onLockChange((locked) => {
      if (!locked && this.state === 'playing') this.pause();
    });

    this.loop = new Loop((dt) => this.update(dt), (dt) => this.render(dt));
    this.menu.showMain();
    // render one idle frame behind the menu so it isn't pure black
    this._renderFrame();
  }

  _buildWorld() {
    this.house = buildHouse();
    this.scene.add(this.house.group);
    this.yard = buildYard();
    this.scene.add(this.yard.group);
    this.lighting = buildLighting(this.scene);
    this.lighting.porch = this.yard.porchLight;
    setAct(this.lighting, 1);
    this.props = buildProps(this.scene, this.house);
    // Exterior signage. Its two anomaly-capable signs join the anomaly list so
    // they are updated and (for the realtor portrait) armable by the Director.
    this.signage = buildSignage(this.scene);
    this.props.list.push(...this.signage.anomalies);
  }

  registerInteractable(obj) {
    this.interactables.push(obj);
    return obj;
  }

  // A door interactable whose prompt tracks the leaf's open/closed state.
  registerDoorInteractable(door, position, radius = 1.8) {
    const it = this.registerInteractable({
      position, radius, label: 'Open door',
      onInteract: () => { door.toggle(); this.audio.thud(); },
    });
    it.syncLabel = () => { it.label = door.isOpen ? 'Close door' : 'Open door'; };
    return it;
  }

  // --- state transitions ---
  start() {
    this.audio.resume();       // AudioContext must init on the click
    this.signage.setBuyer(this.menu.getBuyer()); // paint the name on the yard sign
    this.menu.hideAll();
    this.state = 'playing';
    this.input.requestLock();
    this.acts.begin();
    this.loop.start();
  }

  pause() {
    if (this.state !== 'playing') return;
    this.state = 'paused';
    this.menu.showPause();
    this.audio.setPaused(true);
    // loop keeps running for the dim frame, but update() gates on state
  }

  resume() {
    if (this.state !== 'paused') return;
    this.menu.hideAll();
    this.state = 'playing';
    this.audio.setPaused(false);
    this.input.requestLock();
  }

  toMenu() {
    this.state = 'menu';
    this.audio.setPaused(true);
    this.audio.allOff();
    this.input.releaseLock();
    this.menu.showMain();
    this.hud.clearObjective();
    this.hud.setPrompt('');
    this.acts.reset();
  }

  endBuild() {
    this.state = 'ended';
    this.input.releaseLock();
    this.menu.showCard();
  }

  // --- per-frame ---
  update(dt) {
    if (this.state !== 'playing') return;

    const look = this.input.consumeMouse();
    if (!this.acts.lockLook) this.player.look(look.dx, look.dy);

    this.player.update(dt, this.input, { canMove: this.acts.canMove });

    this.fovea.beginFrame(this.player);
    this.profile.sample(dt, this.player, this.fovea);
    this.director.update(dt, this.player, this.acts.currentAct);

    // anomalies
    for (const p of this.props.list) p.anomaly.update(dt, this.fovea, this.player);

    // doors
    for (const d of this.house.doors) d.update(dt);
    this.props.updateDoors?.(dt);

    if (this.acts.showering) this.hud.setPrompt('');
    else this._updateInteractables();
    this.acts.update(dt);
    this.audio.update(dt, this.player, this.acts);
  }

  _updateInteractables() {
    const eye = this.player.eyePosition();
    let best = null, bestDot = 0.8; // must be roughly looked-at (~37deg cone)
    for (const it of this.interactables) {
      it.syncLabel?.();
      if (it.enabled === false) continue;
      const d = it.position.distanceTo(eye);
      if (d > it.radius) continue;
      const dir = it.position.clone().sub(eye).normalize();
      const dot = dir.dot(this.player.forward);
      if (dot > bestDot) { bestDot = dot; best = it; }
    }
    this._focused = best;
    this.hud.setPrompt(best ? `[E] ${best.label}` : '');
    if (best && this.input.consumeInteract()) {
      best.onInteract();
    } else if (!best) {
      this.input.consumeInteract(); // drain so it doesn't queue
    }
  }

  render() {
    this._renderFrame();
  }

  _renderFrame() {
    this.renderer.renderer.setRenderTarget(this.renderer.target);
    this.renderer.renderer.clear();
    this.renderer.renderer.render(this.scene, this.camera);
    this.peripheral.render(this.renderer.renderer, this.renderer.target.texture);
  }
}

window.addEventListener('DOMContentLoaded', () => new Game());
