import * as THREE from 'three';

// The peripheral pass. The scene is rendered to a target; this draws a single
// fullscreen quad that samples it and degrades everything away from the centre:
// a radial blur whose reach grows with distance from centre, a slide toward
// luminance (desaturation), and a small loss of brightness. The centre stays
// perfectly sharp. This is a *look*, not a gameplay trick — anomalies are
// hidden by geometry and timing, never by this blur.

const VERT = /* glsl */`
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position.xy, 0.0, 1.0);
  }
`;

const FRAG = /* glsl */`
  precision highp float;
  varying vec2 vUv;
  uniform sampler2D tDiffuse;
  uniform vec2 uTexel;      // 1/resolution
  uniform float uAspect;    // width/height
  uniform float uAmount;    // global multiplier (0 disables, 1 full)

  // 8 taps radiating out from screen centre. Offsets are scaled by peripheral
  // amount so the fovea samples a single sharp texel and the corners smear.
  vec3 radialBlur(vec2 uv, float amt) {
    // aspect-correct the direction so blur is even horizontally and vertically.
    // No early-out branch: at the centre amt is ~0 so every tap lands on the
    // same texel and the result is perfectly sharp.
    vec2 dir = (uv - 0.5) * vec2(uAspect, 1.0);
    float len = max(length(dir), 1e-4);
    dir /= len;
    vec2 step = dir * amt;
    step.x /= uAspect;

    vec3 col = texture2D(tDiffuse, uv).rgb;
    col += texture2D(tDiffuse, uv + step * 1.0).rgb;
    col += texture2D(tDiffuse, uv + step * 2.0).rgb;
    col += texture2D(tDiffuse, uv + step * 3.0).rgb;
    col += texture2D(tDiffuse, uv + step * 4.0).rgb;
    col += texture2D(tDiffuse, uv - step * 1.0).rgb;
    col += texture2D(tDiffuse, uv - step * 2.0).rgb;
    col += texture2D(tDiffuse, uv + step * 6.0).rgb;
    return col / 8.0;
  }

  void main() {
    // radius: 0 at centre, ~1.0 at mid-edge, ~1.4 at corners (aspect-corrected)
    vec2 d = vUv - 0.5;
    d.x *= uAspect / max(uAspect, 1.0);
    d.y *= 1.0 / max(uAspect, 1.0);
    float r = length((vUv - 0.5) * vec2(uAspect, 1.0)) / (0.5 * sqrt(uAspect*uAspect + 1.0)) * 1.4;

    // ~20% of screen radius is fully sharp, then it degrades quickly.
    float p = smoothstep(0.20, 0.95, r) * uAmount;

    vec3 col = radialBlur(vUv, p * 0.006);

    // desaturate toward luminance
    float lum = dot(col, vec3(0.299, 0.587, 0.114));
    col = mix(col, vec3(lum), p * 0.82);

    // lose a little brightness at the edges
    col *= mix(1.0, 0.55, p);

    gl_FragColor = vec4(col, 1.0);
  }
`;

export class PeripheralPass {
  constructor() {
    this.scene = new THREE.Scene();
    this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

    this.material = new THREE.ShaderMaterial({
      vertexShader: VERT,
      fragmentShader: FRAG,
      uniforms: {
        tDiffuse: { value: null },
        uTexel: { value: new THREE.Vector2(1, 1) },
        uAspect: { value: 1 },
        uAmount: { value: 1 },
      },
      depthTest: false,
      depthWrite: false,
    });

    const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), this.material);
    quad.frustumCulled = false;
    this.scene.add(quad);
  }

  setSize(w, h) {
    this.material.uniforms.uTexel.value.set(1 / w, 1 / h);
    this.material.uniforms.uAspect.value = w / h;
  }

  // amount: 0..1, lets acts dial the effect (e.g. weaker in bright Act 1).
  setAmount(a) {
    this.material.uniforms.uAmount.value = a;
  }

  render(renderer, sourceTexture) {
    this.material.uniforms.tDiffuse.value = sourceTexture;
    renderer.setRenderTarget(null);
    renderer.render(this.scene, this.camera);
  }

  dispose() {
    this.material.dispose();
  }
}
