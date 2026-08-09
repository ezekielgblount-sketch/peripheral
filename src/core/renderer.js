import * as THREE from 'three';

// Owns the WebGL renderer and the single render target the peripheral pass
// reads from. Everything is drawn into `target`, then the peripheral quad
// draws to the screen. One target, one quad — that is the whole post budget.
export class Renderer {
  constructor(container) {
    this.renderer = new THREE.WebGLRenderer({
      antialias: false,       // the peripheral blur hides aliasing at the edges anyway
      powerPreference: 'high-performance',
      stencil: false,
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.setClearColor(0x000000, 1);
    container.appendChild(this.renderer.domElement);

    this.target = new THREE.WebGLRenderTarget(1, 1, {
      minFilter: THREE.LinearFilter,
      magFilter: THREE.LinearFilter,
      type: THREE.UnsignedByteType,
      depthBuffer: true,
      stencilBuffer: false,
    });

    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  get domElement() {
    return this.renderer.domElement;
  }

  resize() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio, 1.5);
    this.renderer.setSize(w, h, true);
    this.target.setSize(Math.floor(w * dpr), Math.floor(h * dpr));
    this._onResize?.(w, h);
  }

  onResize(fn) {
    this._onResize = fn;
  }

  dispose() {
    this.target.dispose();
    this.renderer.dispose();
  }
}
