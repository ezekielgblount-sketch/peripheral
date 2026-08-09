// DOM overlay: main menu, pause screen, and the end-of-build card.
// Flat mono type over the canvas. No settings, no sliders.

import { sanitiseBuyer } from '../util/text.js';

const CSS = `
.pf-overlay {
  position: fixed; inset: 0; z-index: 10;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  font-family: var(--mono); color: var(--ink);
  background: rgba(10,10,9,0.82);
  -webkit-user-select: none; user-select: none;
}
.pf-overlay.dim { background: rgba(10,10,9,0.55); }
.pf-hidden { display: none !important; }
.pf-title {
  font-size: clamp(34px, 9vw, 88px);
  letter-spacing: 0.42em; font-weight: 400; margin-left: 0.42em;
  color: var(--pale);
}
.pf-sub { color: var(--ink-dim); letter-spacing: 0.28em; font-size: 12px; margin-top: 14px; text-transform: uppercase; }
.pf-menu { margin-top: 46px; display: flex; flex-direction: column; gap: 4px; align-items: center; }
.pf-btn {
  background: none; border: 1px solid transparent; color: var(--ink-dim);
  font-family: var(--mono); font-size: 17px; letter-spacing: 0.22em;
  padding: 10px 26px; cursor: pointer; text-transform: uppercase; transition: color .12s, border-color .12s;
}
.pf-btn:hover, .pf-btn:focus { color: var(--pale); border-color: var(--dark); outline: none; }
.pf-buyer { margin-top: 30px; display: flex; flex-direction: column; align-items: center; width: 260px; }
.pf-buyer-input {
  background: none; border: none; outline: none; text-align: center;
  font-family: var(--mono); font-size: 16px; letter-spacing: 0.22em; color: var(--pale);
  text-transform: uppercase; width: 100%; padding: 2px 0 6px;
}
.pf-buyer-input::placeholder { color: #4a473f; text-transform: uppercase; letter-spacing: 0.22em; }
.pf-buyer-rule { width: 100%; height: 1px; background: var(--ink-dim); opacity: 0.7; }
.pf-buyer-label { margin-top: 6px; color: var(--ink-dim); font-size: 10px; letter-spacing: 0.34em; }
.pf-controls { margin-top: 40px; color: var(--ink-dim); font-size: 12px; line-height: 2.0; letter-spacing: 0.12em; text-align: center; }
.pf-controls b { color: var(--light); font-weight: 400; }
.pf-note { margin-top: 30px; color: #59564f; font-size: 11px; max-width: 30em; text-align: center; line-height: 1.7; }
.pf-card-btn { margin-top: 40px; }
`;

export class Menu {
  constructor(root) {
    this.root = root;
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    this.onStart = () => {};
    this.onResume = () => {};
    this.onExit = () => {};

    this._buildMain();
    this._buildPause();
    this._buildCard();
  }

  _buildMain() {
    const el = document.createElement('div');
    el.className = 'pf-overlay';
    el.innerHTML = `
      <div class="pf-title">PERIPHERAL</div>
      <div class="pf-sub">build 0.1</div>
      <div class="pf-menu">
        <button class="pf-btn" data-act="start">Start</button>
      </div>
      <div class="pf-buyer">
        <input class="pf-buyer-input" maxlength="22" spellcheck="false" autocomplete="off"
               autocapitalize="characters" placeholder="&nbsp;" aria-label="Buyer name" />
        <div class="pf-buyer-rule"></div>
        <div class="pf-buyer-label">BUYER</div>
      </div>
      <div class="pf-controls">
        <div><b>WASD</b> move &nbsp;·&nbsp; <b>Mouse</b> look &nbsp;·&nbsp; <b>Shift</b> slower</div>
        <div><b>E</b> interact &nbsp;·&nbsp; <b>Esc</b> pause</div>
      </div>
      <div class="pf-note">Best with sound. A browser tab can't close itself, so
        "Exit" returns to this menu rather than quitting.</div>`;
    el.querySelector('[data-act="start"]').addEventListener('click', () => this.onStart());

    // BUYER field: persisted on-device only, never sent anywhere.
    this.buyerInput = el.querySelector('.pf-buyer-input');
    try {
      const saved = localStorage.getItem('peripheral.buyer');
      if (saved) this.buyerInput.value = saved;
    } catch (e) { /* private mode: fall back to session-only */ }
    this.buyerInput.addEventListener('input', () => {
      // light sanitise as they type: allowed chars only, capped length
      const clean = sanitiseBuyer(this.buyerInput.value);
      if (clean !== this.buyerInput.value) this.buyerInput.value = clean;
      try { localStorage.setItem('peripheral.buyer', clean); } catch (e) { /* ignore */ }
    });
    // Enter starts the game, like clicking Start.
    this.buyerInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); this.onStart(); }
    });

    this.root.appendChild(el);
    this.mainEl = el;
  }

  // The sanitised buyer string (may be empty). Signage applies the NEW OWNER
  // fallback and uppercasing at render time.
  getBuyer() {
    return sanitiseBuyer(this.buyerInput?.value || '');
  }

  _buildPause() {
    const el = document.createElement('div');
    el.className = 'pf-overlay dim pf-hidden';
    el.innerHTML = `
      <div class="pf-title" style="font-size:clamp(24px,6vw,52px)">PAUSED</div>
      <div class="pf-menu">
        <button class="pf-btn" data-act="resume">Resume</button>
        <button class="pf-btn" data-act="exit">Exit to menu</button>
      </div>`;
    el.querySelector('[data-act="resume"]').addEventListener('click', () => this.onResume());
    el.querySelector('[data-act="exit"]').addEventListener('click', () => this.onExit());
    this.root.appendChild(el);
    this.pauseEl = el;
  }

  _buildCard() {
    const el = document.createElement('div');
    el.className = 'pf-overlay pf-hidden';
    el.style.background = '#000';
    el.innerHTML = `
      <div class="pf-title" style="font-size:clamp(20px,5vw,40px)">PERIPHERAL</div>
      <div class="pf-sub">end of build 0.1</div>
      <div class="pf-menu pf-card-btn">
        <button class="pf-btn" data-act="menu">Return to menu</button>
      </div>`;
    el.querySelector('[data-act="menu"]').addEventListener('click', () => this.onExit());
    this.root.appendChild(el);
    this.cardEl = el;
  }

  showMain() { this._only(this.mainEl); }
  showPause() { this._only(this.pauseEl); }
  showCard() { this._only(this.cardEl); }
  hideAll() { this._only(null); }

  _only(target) {
    for (const el of [this.mainEl, this.pauseEl, this.cardEl]) {
      el.classList.toggle('pf-hidden', el !== target);
    }
  }
}
