// DOM overlay: main menu, pause screen, and the end-of-build card.
// Flat mono type over the canvas. No settings, no sliders.

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
.pf-controls { margin-top: 52px; color: var(--ink-dim); font-size: 12px; line-height: 2.0; letter-spacing: 0.12em; text-align: center; }
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
      <div class="pf-controls">
        <div><b>WASD</b> move &nbsp;·&nbsp; <b>Mouse</b> look &nbsp;·&nbsp; <b>Shift</b> slower</div>
        <div><b>E</b> interact &nbsp;·&nbsp; <b>Esc</b> pause</div>
      </div>
      <div class="pf-note">Best with sound. A browser tab can't close itself, so
        "Exit" returns to this menu rather than quitting.</div>`;
    el.querySelector('[data-act="start"]').addEventListener('click', () => this.onStart());
    this.root.appendChild(el);
    this.mainEl = el;
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
