// Pointer lock, keyboard state, mouse-look deltas, and a one-shot interact edge.
// The game loop reads `keys`, drains `consumeMouse()`, and checks `consumeInteract()`.

export class Input {
  constructor(domElement) {
    this.dom = domElement;
    this.keys = Object.create(null);
    this.mouseDX = 0;
    this.mouseDY = 0;
    this.sensitivity = 0.0022;
    this.locked = false;
    this._interactQueued = false;

    this._onLockChange = null;   // callback(locked)
    this._interactHandlers = [];

    this._bind();
  }

  _bind() {
    document.addEventListener('keydown', (e) => {
      // Ignore auto-repeat for edge-triggered keys.
      const code = e.code;
      if (!e.repeat) {
        if (code === 'KeyE') this._interactQueued = true;
      }
      this.keys[code] = true;
      // Esc is handled by the browser to exit pointer lock; we react in lockchange.
    });
    document.addEventListener('keyup', (e) => {
      this.keys[e.code] = false;
    });

    document.addEventListener('mousemove', (e) => {
      if (!this.locked) return;
      this.mouseDX += e.movementX || 0;
      this.mouseDY += e.movementY || 0;
    });

    document.addEventListener('pointerlockchange', () => {
      this.locked = document.pointerLockElement === this.dom;
      document.body.classList.toggle('locked', this.locked);
      // A fresh lock should not carry stale mouse delta into the first frame.
      this.mouseDX = 0;
      this.mouseDY = 0;
      this._onLockChange?.(this.locked);
    });
  }

  requestLock() {
    // Must be called from a user gesture.
    if (document.pointerLockElement !== this.dom) {
      const p = this.dom.requestPointerLock?.();
      if (p && typeof p.catch === 'function') p.catch(() => {});
    }
  }

  releaseLock() {
    if (document.pointerLockElement === this.dom) {
      document.exitPointerLock?.();
    }
  }

  onLockChange(fn) {
    this._onLockChange = fn;
  }

  // Returns accumulated look delta scaled to radians, then clears it.
  consumeMouse() {
    const dx = this.mouseDX * this.sensitivity;
    const dy = this.mouseDY * this.sensitivity;
    this.mouseDX = 0;
    this.mouseDY = 0;
    return { dx, dy };
  }

  consumeInteract() {
    if (this._interactQueued) {
      this._interactQueued = false;
      return true;
    }
    return false;
  }

  isDown(code) {
    return !!this.keys[code];
  }

  // Movement axes from WASD. x = strafe (right +), z = forward (+ forward).
  moveAxis() {
    let x = 0, z = 0;
    if (this.keys['KeyW']) z += 1;
    if (this.keys['KeyS']) z -= 1;
    if (this.keys['KeyD']) x += 1;
    if (this.keys['KeyA']) x -= 1;
    return { x, z };
  }

  clearMovement() {
    // Used on pause so a held key doesn't keep moving after resume glitchily.
    this.mouseDX = 0;
    this.mouseDY = 0;
  }
}
