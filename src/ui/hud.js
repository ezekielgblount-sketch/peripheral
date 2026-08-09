// In-world text: fading objective lines low on screen, and a small interact
// prompt. No health, no ammo, no crosshair clutter — a single faint dot.

const CSS = `
.pf-hud { position: fixed; inset: 0; z-index: 5; pointer-events: none; font-family: var(--mono); }
.pf-dot {
  position: absolute; left: 50%; top: 50%; width: 3px; height: 3px; margin: -1.5px 0 0 -1.5px;
  background: rgba(230,223,204,0.28); border-radius: 50%;
}
.pf-objective {
  position: absolute; left: 0; right: 0; bottom: 12%; text-align: center;
  color: var(--ink); font-size: 15px; letter-spacing: 0.18em;
  opacity: 0; transition: opacity 1.4s ease; text-shadow: 0 1px 6px rgba(0,0,0,0.9);
}
.pf-objective.show { opacity: 0.9; }
.pf-prompt {
  position: absolute; left: 50%; top: 58%; transform: translateX(-50%);
  color: var(--light); font-size: 13px; letter-spacing: 0.16em; opacity: 0;
  transition: opacity .18s; text-shadow: 0 1px 6px rgba(0,0,0,0.9);
}
.pf-prompt.show { opacity: 0.92; }
.pf-fade {
  position: fixed; inset: 0; z-index: 8; background: #000; opacity: 0;
  pointer-events: none; transition: opacity 1s ease;
}
`;

export class Hud {
  constructor(root) {
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    this.el = document.createElement('div');
    this.el.className = 'pf-hud';
    this.el.innerHTML = `
      <div class="pf-dot"></div>
      <div class="pf-objective"></div>
      <div class="pf-prompt"></div>`;
    root.appendChild(this.el);

    this.fade = document.createElement('div');
    this.fade.className = 'pf-fade';
    root.appendChild(this.fade);

    this.objectiveEl = this.el.querySelector('.pf-objective');
    this.promptEl = this.el.querySelector('.pf-prompt');
    this._objTimer = 0;
  }

  show() { this.el.classList.remove('pf-hidden'); this.el.style.display = ''; }
  hide() { this.el.style.display = 'none'; }

  // Fade an objective line in, hold, fade out. duration in ms; 0 = stay until replaced.
  objective(text, holdMs = 6000) {
    clearTimeout(this._objTimer);
    this.objectiveEl.textContent = text;
    // force reflow so the transition retriggers
    void this.objectiveEl.offsetWidth;
    this.objectiveEl.classList.add('show');
    if (holdMs > 0) {
      this._objTimer = setTimeout(() => this.objectiveEl.classList.remove('show'), holdMs);
    }
  }

  clearObjective() {
    clearTimeout(this._objTimer);
    this.objectiveEl.classList.remove('show');
  }

  setPrompt(text) {
    if (text) {
      this.promptEl.textContent = text;
      this.promptEl.classList.add('show');
    } else {
      this.promptEl.classList.remove('show');
    }
  }

  // Screen fade to/from black. Returns a promise that resolves after the transition.
  fadeTo(opacity, ms = 1000) {
    this.fade.style.transitionDuration = ms + 'ms';
    // reflow
    void this.fade.offsetWidth;
    this.fade.style.opacity = String(opacity);
    return new Promise((res) => setTimeout(res, ms));
  }

  setFadeInstant(opacity) {
    this.fade.style.transitionDuration = '0ms';
    this.fade.style.opacity = String(opacity);
    void this.fade.offsetWidth;
    this.fade.style.transitionDuration = '1000ms';
  }
}
