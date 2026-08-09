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

    this.registerInteractable({
      position: this.house.anchors.frontDoor.clone().setY(1.0),
      radius: 2.0,
      label: 'Open door',
      onInteract: () => {
        this.house.frontDoor.toggle();
        this.audio.thud();
      },
    });

    this.state = 'menu';
    this.colliders = [...this.house.colliders, ...this.yard.colliders];
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
  }

  registerInteractable(obj) {
    this.interactables.push(obj);
    return obj;
  }

  // --- state transitions ---
  start() {
    this.audio.resume();       // AudioContext must init on the click
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

    this._updateInteractables();
    this.acts.update(dt);
    this.audio.update(dt, this.player, this.acts);
  }

  _updateInteractables() {
    const eye = this.player.eyePosition();
    let best = null, bestDot = 0.8; // must be roughly looked-at (~37deg cone)
    for (const it of this.interactables) {
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
