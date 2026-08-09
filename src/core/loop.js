// Fixed-step update, variable-rate render. The update callback runs at a fixed
// dt so movement and the fovea dwell timers behave the same on any machine; the
// render callback runs once per animation frame.

export class Loop {
  constructor(update, render, step = 1 / 60) {
    this.update = update;
    this.render = render;
    this.step = step;
    this.running = false;
    this._acc = 0;
    this._last = 0;
    this._raf = 0;
    this._frame = this._frame.bind(this);
  }

  start() {
    if (this.running) return;
    this.running = true;
    this._last = performance.now();
    this._acc = 0;
    this._raf = requestAnimationFrame(this._frame);
  }

  stop() {
    this.running = false;
    if (this._raf) cancelAnimationFrame(this._raf);
    this._raf = 0;
  }

  _frame(now) {
    if (!this.running) return;
    this._raf = requestAnimationFrame(this._frame);

    let delta = (now - this._last) / 1000;
    this._last = now;
    // Guard against tab-out spikes: never simulate more than ~4 steps of catch-up.
    if (delta > 0.25) delta = 0.25;
    this._acc += delta;

    let steps = 0;
    while (this._acc >= this.step && steps < 5) {
      this.update(this.step);
      this._acc -= this.step;
      steps++;
    }
    this.render(delta);
  }
}
