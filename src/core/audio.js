// Every sound in Peripheral is synthesised with the Web Audio API. No files.
// The cricket bed and its sudden silence when the entity is near is the whole
// point of the Act 2 sound design; everything else is texture.

export class AudioEngine {
  constructor() {
    this.ctx = null;
    this.master = null;
    this.paused = false;

    this.house = null;    // low interior tone
    this.crickets = null; // outdoor bed
    this.cricketTarget = 0;
    this.cricketLevel = 0;

    this._stepDist = 0;
    this._stepPhase = 0;
  }

  resume() {
    if (!this.ctx) this._init();
    if (this.ctx.state === 'suspended') this.ctx.resume();
  }

  _init() {
    const AC = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AC();
    this.master = this.ctx.createGain();
    this.master.gain.value = 0.9;
    this.master.connect(this.ctx.destination);

    // reusable white-noise buffer
    const n = this.ctx.sampleRate * 2;
    this.noiseBuf = this.ctx.createBuffer(1, n, this.ctx.sampleRate);
    const data = this.noiseBuf.getChannelData(0);
    for (let i = 0; i < n; i++) data[i] = Math.random() * 2 - 1;

    this._buildHouseTone();
    this._buildCrickets();
  }

  _buildHouseTone() {
    const g = this.ctx.createGain(); g.gain.value = 0.0;
    const o1 = this.ctx.createOscillator(); o1.type = 'sine'; o1.frequency.value = 54;
    const o2 = this.ctx.createOscillator(); o2.type = 'sine'; o2.frequency.value = 55.3;
    const lp = this.ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 120;
    o1.connect(lp); o2.connect(lp); lp.connect(g); g.connect(this.master);
    o1.start(); o2.start();
    this.house = { gain: g };
  }

  _buildCrickets() {
    const out = this.ctx.createGain(); out.gain.value = 0;
    // band-limited noise gives the shimmer; a fast tremolo gives the trill.
    const src = this.ctx.createBufferSource(); src.buffer = this.noiseBuf; src.loop = true;
    const bp = this.ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = 5200; bp.Q.value = 12;
    const bp2 = this.ctx.createBiquadFilter(); bp2.type = 'bandpass'; bp2.frequency.value = 4200; bp2.Q.value = 18;
    const trem = this.ctx.createGain(); trem.gain.value = 0.5;
    const lfo = this.ctx.createOscillator(); lfo.type = 'square'; lfo.frequency.value = 13;
    const lfoGain = this.ctx.createGain(); lfoGain.gain.value = 0.5;
    lfo.connect(lfoGain); lfoGain.connect(trem.gain);
    src.connect(bp); bp.connect(bp2); bp2.connect(trem); trem.connect(out); out.connect(this.master);
    src.start(); lfo.start();
    this.crickets = { gain: out };
  }

  setHouseTone(on) {
    if (!this.ctx) return;
    this.house.gain.gain.setTargetAtTime(on ? 0.08 : 0.0, this.ctx.currentTime, 0.6);
  }

  setCrickets(on) { this.cricketTarget = on ? 1 : 0; }

  // Sub-bass swell for the act transition. Returns after it has peaked.
  swell() {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const g = this.ctx.createGain(); g.gain.value = 0;
    const o = this.ctx.createOscillator(); o.type = 'sine'; o.frequency.value = 38;
    const o2 = this.ctx.createOscillator(); o2.type = 'sine'; o2.frequency.value = 41;
    o.connect(g); o2.connect(g); g.connect(this.master);
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(0.5, t + 1.2);
    g.gain.linearRampToValueAtTime(0.0, t + 3.0);
    o.start(t); o2.start(t); o.stop(t + 3.1); o2.stop(t + 3.1);
  }

  // A soft low thud (door, breaker cover).
  thud() {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const g = this.ctx.createGain(); g.gain.value = 0.0;
    const o = this.ctx.createOscillator(); o.type = 'sine'; o.frequency.setValueAtTime(160, t);
    o.frequency.exponentialRampToValueAtTime(60, t + 0.18);
    g.gain.linearRampToValueAtTime(0.25, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.001, t + 0.35);
    o.connect(g); g.connect(this.master);
    o.start(t); o.stop(t + 0.4);
  }

  // A firm switch/clack for the breaker.
  clack() {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const s = this.ctx.createBufferSource(); s.buffer = this.noiseBuf;
    const bp = this.ctx.createBiquadFilter(); bp.type = 'highpass'; bp.frequency.value = 1500;
    const g = this.ctx.createGain(); g.gain.value = 0;
    g.gain.linearRampToValueAtTime(0.3, t + 0.005);
    g.gain.exponentialRampToValueAtTime(0.001, t + 0.08);
    s.connect(bp); bp.connect(g); g.connect(this.master);
    s.start(t); s.stop(t + 0.1);
  }

  _footstep(surface) {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const s = this.ctx.createBufferSource(); s.buffer = this.noiseBuf;
    const bp = this.ctx.createBiquadFilter();
    const g = this.ctx.createGain(); g.gain.value = 0;
    if (surface === 'gravel') {
      bp.type = 'bandpass'; bp.frequency.value = 2600; bp.Q.value = 1.0;
      g.gain.linearRampToValueAtTime(0.12, t + 0.005);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.12);
    } else { // wood
      bp.type = 'lowpass'; bp.frequency.value = 700;
      g.gain.linearRampToValueAtTime(0.10, t + 0.004);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.09);
    }
    s.connect(bp); bp.connect(g); g.connect(this.master);
    s.start(t); s.stop(t + 0.14);
  }

  setPaused(p) {
    this.paused = p;
    if (!this.ctx) return;
    this.master.gain.setTargetAtTime(p ? 0.0 : 0.9, this.ctx.currentTime, 0.05);
  }

  allOff() {
    if (!this.ctx) return;
    this.setCrickets(false);
    this.setHouseTone(false);
  }

  update(dt, player, acts) {
    if (!this.ctx || this.paused) return;

    // cricket level ramp: silence is fast (0.4s), return is a touch slower.
    const rate = this.cricketTarget > this.cricketLevel ? dt / 0.6 : dt / 0.4;
    if (this.cricketLevel < this.cricketTarget) this.cricketLevel = Math.min(this.cricketTarget, this.cricketLevel + rate);
    else this.cricketLevel = Math.max(this.cricketTarget, this.cricketLevel - rate);
    this.crickets.gain.gain.setTargetAtTime(this.cricketLevel * 0.22, this.ctx.currentTime, 0.05);

    // footsteps: step every ~0.72m of travel while grounded
    const moved = player.speedThisFrame * dt;
    if (player.speedThisFrame > 0.4) {
      this._stepDist += moved;
      const stride = 0.72;
      if (this._stepDist >= stride) {
        this._stepDist -= stride;
        this._footstep(player.walkSurface);
      }
    } else {
      this._stepDist = Math.max(0, this._stepDist - dt * 0.5);
    }
  }
}
