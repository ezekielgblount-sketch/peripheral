import * as THREE from 'three';
import { PAL } from '../constants.js';
import { Anomaly } from '../game/anomaly.js';
import { buyerDisplay } from '../util/text.js';

// Exterior signage, all drawn to <canvas> in code and used as CanvasTextures —
// still zero external files. Two of the signs join the anomaly system: the
// realtor's portrait (its face becomes the figure's face) and, in Act 2 only,
// the yard sign (the SOLD banner and the buyer's name are simply gone).
//
// The buyer name is entered on the menu, kept only in localStorage, and appears
// exactly once — painted on the yard sign — and then, later, conspicuously not.

const MONO = 'ui-monospace, Menlo, Consolas, monospace';
const CONDENSED = '"Arial Narrow", "Roboto Condensed", "Helvetica Neue", system-ui, sans-serif';

// ---- canvas helpers ----
function makeTex(w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const ctx = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  return { c, ctx, tex };
}

// paper base with uneven ink and speckle — nothing in this world is crisp
function weather(ctx, w, h, base = '#b3a78f') {
  ctx.save();
  ctx.fillStyle = base; ctx.fillRect(0, 0, w, h);
  const g = ctx.createLinearGradient(0, 0, 0, h);
  g.addColorStop(0, 'rgba(255,255,255,0.06)');
  g.addColorStop(1, 'rgba(0,0,0,0.12)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  // blotches
  for (let i = 0; i < 24; i++) {
    const x = Math.random() * w, y = Math.random() * h, r = 20 + Math.random() * 90;
    const rg = ctx.createRadialGradient(x, y, 0, x, y, r);
    rg.addColorStop(0, `rgba(50,44,36,${0.03 + Math.random() * 0.05})`);
    rg.addColorStop(1, 'rgba(50,44,36,0)');
    ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
  }
  // speckle
  const n = Math.floor(w * h * 0.006);
  for (let i = 0; i < n; i++) {
    ctx.fillStyle = `rgba(30,26,20,${Math.random() * 0.09})`;
    ctx.fillRect(Math.random() * w, Math.random() * h, 1, 1);
  }
  ctx.restore();
}

function ink(ctx, text, x, y, font, color = '#26231c', align = 'center') {
  ctx.save();
  ctx.font = font; ctx.textAlign = align; ctx.textBaseline = 'middle';
  ctx.fillStyle = color;
  ctx.globalAlpha = 0.9;
  ctx.fillText(text, x + (Math.random() * 1.6 - 0.8), y + (Math.random() * 1.6 - 0.8));
  ctx.globalAlpha = 1;
  ctx.restore();
}

function rule(ctx, x1, y, x2, color = '#4e4b44', wobble = 1.5) {
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(x1, y + (Math.random() * wobble - wobble / 2));
  ctx.lineTo(x2, y + (Math.random() * wobble - wobble / 2));
  ctx.stroke();
  ctx.restore();
}

// ---- individual sign drawings ----
function drawYardSign(ctx, w, h, buyer, withSold) {
  weather(ctx, w, h, '#b6ab92');
  ctx.strokeStyle = '#4e4b44'; ctx.lineWidth = 8; ctx.strokeRect(24, 24, w - 48, h - 48);
  ink(ctx, 'HOME FOR SALE', w / 2, 150, `700 ${92}px ${MONO}`, '#26231c');
  rule(ctx, 140, 268, w - 140);
  ink(ctx, 'SOLD TO', w / 2, 360, `40px ${MONO}`, '#57534a');
  if (buyer) ink(ctx, buyer, w / 2, 470, `700 ${74}px ${MONO}`, '#201d17');
  // (Act 2 blank state passes buyer = '' and withSold = false)
  if (withSold) {
    // hand-applied SOLD banner across the top-right corner, crooked, ~20 deg
    ctx.save();
    ctx.translate(w - 150, 120);
    ctx.rotate(-0.35 + (Math.random() * 0.06 - 0.03));
    ctx.fillStyle = '#3f3c35';
    ctx.fillRect(-190, -44, 380, 88);
    ink(ctx, 'SOLD', 0, 2, `700 ${64}px ${MONO}`, '#e6dfcc');
    ctx.restore();
  }
}

function drawRealtor(ctx, w, h, smile) {
  weather(ctx, w, h, '#c2b79d');
  ctx.strokeStyle = '#4e4b44'; ctx.lineWidth = 6; ctx.strokeRect(18, 18, w - 36, h - 36);
  ink(ctx, 'HOLLOWAY & VANE', w / 2, 74, `700 ${44}px ${CONDENSED}`, '#26231c');
  ink(ctx, 'PROPERTY GROUP', w / 2, 118, `28px ${CONDENSED}`, '#57534a');
  // flat vector agent portrait
  const cx = w / 2, cy = 320, R = 92;
  ctx.save();
  // shoulders
  ctx.fillStyle = '#6c685f';
  ctx.beginPath(); ctx.ellipse(cx, cy + 150, 130, 78, 0, Math.PI, 0); ctx.fill();
  // head
  ctx.fillStyle = '#9a927f';
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.fill();
  ctx.lineWidth = 5; ctx.strokeStyle = '#4e4b44'; ctx.stroke();
  // face — the ONLY thing the anomaly changes
  ctx.fillStyle = '#26231c';
  ctx.beginPath(); ctx.arc(cx - 32, cy - 12, 8, 0, 7); ctx.fill();
  ctx.beginPath(); ctx.arc(cx + 32, cy - 12, 8, 0, 7); ctx.fill();
  if (smile) {
    ctx.strokeStyle = '#26231c'; ctx.lineWidth = 6; ctx.beginPath();
    ctx.arc(cx, cy + 18, 34, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
  }
  ctx.restore();
  ink(ctx, '(555) 0114', w / 2, h - 70, `34px ${MONO}`, '#57534a');
}

function drawFlyer(ctx, w, h) {
  weather(ctx, w, h, '#bdb298');
  // rain-faded: wash everything toward the paper so it is barely legible
  ink(ctx, 'OPEN HOUSE', w / 2, 130, `700 ${58}px ${CONDENSED}`, '#6f6a5e');
  rule(ctx, 90, 200, w - 90, '#8a8676', 3);
  ink(ctx, 'SATURDAY 1-4 PM', w / 2, 280, `36px ${CONDENSED}`, '#7c7870');
  ink(ctx, 'REFRESHMENTS', w / 2, 340, `30px ${CONDENSED}`, '#8a8676');
  ink(ctx, 'ALL WELCOME', w / 2, 400, `30px ${CONDENSED}`, '#8a8676');
  // vertical rain streaks
  ctx.save();
  for (let i = 0; i < 40; i++) {
    const x = Math.random() * w;
    ctx.fillStyle = `rgba(150,142,124,${0.05 + Math.random() * 0.12})`;
    ctx.fillRect(x, 0, 1 + Math.random() * 2, h);
  }
  // heavy wash
  ctx.fillStyle = 'rgba(189,178,152,0.35)'; ctx.fillRect(0, 0, w, h);
  ctx.restore();
}

function drawInspection(ctx, w, h) {
  weather(ctx, w, h, '#d8cfba');
  ctx.strokeStyle = '#4e4b44'; ctx.lineWidth = 4; ctx.strokeRect(14, 14, w - 28, h - 28);
  ink(ctx, 'PROPERTY INSPECTION', w / 2, 52, `26px ${MONO}`, '#26231c');
  rule(ctx, 40, 78, w - 40);
  const rows = ['ROOF', 'PLUMBING', 'ELECTRICAL', 'STRUCTURE — NO FINDINGS'];
  let y = 120;
  for (const r of rows) {
    // ticked box
    ctx.strokeStyle = '#4e4b44'; ctx.lineWidth = 3; ctx.strokeRect(44, y - 16, 26, 26);
    ctx.strokeStyle = '#26231c'; ctx.lineWidth = 4; ctx.beginPath();
    ctx.moveTo(48, y - 2); ctx.lineTo(56, y + 7); ctx.lineTo(70, y - 14); ctx.stroke();
    ink(ctx, r, 90, y - 2, `24px ${MONO}`, '#33302a', 'left');
    y += 58;
  }
}

// ---- build ----
export function buildSignage(scene) {
  const group = new THREE.Group();
  scene.add(group);
  const colliders = [];
  const anomalies = [];

  const wood = new THREE.MeshStandardMaterial({ color: PAL.dark, roughness: 1, metalness: 0 });
  const box = (w, h, d) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wood); m.castShadow = true; return m; };
  function plane(wm, hm, tex) {
    const mat = new THREE.MeshStandardMaterial({ map: tex, roughness: 1, metalness: 0 });
    const m = new THREE.Mesh(new THREE.PlaneGeometry(wm, hm), mat);
    m.castShadow = true; m.receiveShadow = true;
    return m;
  }

  // === 1. YARD SIGN (anomaly: Act 2 blank) ===
  const ySignN = makeTex(1024, 683);
  const ySignOff = makeTex(1024, 683);
  drawYardSign(ySignN.ctx, 1024, 683, buyerDisplay(''), true);
  ySignN.tex.needsUpdate = true;
  drawYardSign(ySignOff.ctx, 1024, 683, '', false);
  ySignOff.tex.needsUpdate = true;

  const yardGroup = new THREE.Group();
  const board = plane(0.9, 0.6, ySignN.tex);
  board.position.set(0, 1.0, 0);
  yardGroup.add(board);
  for (const px of [-0.42, 0.42]) { const p = box(0.07, 1.1, 0.07); p.position.set(px, 0.55, 0.03); yardGroup.add(p); }
  yardGroup.position.set(7.5, 0, -5.2);
  yardGroup.rotation.y = Math.PI - 0.28;   // face the road, angled
  yardGroup.rotation.z = 0.015;            // a couple percent off true
  group.add(yardGroup);
  colliders.push({ min: { x: 7.0, y: 0, z: -5.5 }, max: { x: 7.9, y: 1.6, z: -4.9 } });

  const yardAnchor = new THREE.Object3D(); yardAnchor.position.set(0, 1.0, 0); yardGroup.add(yardAnchor);
  const yardSign = {
    root: yardGroup, room: 'yard', actOnly: 2,
    getAnchor: (v = new THREE.Vector3()) => yardAnchor.getWorldPosition(v),
    setOff() { board.material.map = ySignOff.tex; board.material.needsUpdate = true; },
    setNormal() { board.material.map = ySignN.tex; board.material.needsUpdate = true; },
  };
  yardSign.anomaly = new Anomaly(yardSign);
  yardSign.setNormal();
  anomalies.push(yardSign);

  // redraw the normal yard-sign texture with the entered buyer name (called on Start)
  function setBuyer(raw) {
    drawYardSign(ySignN.ctx, 1024, 683, buyerDisplay(raw), true);
    ySignN.tex.needsUpdate = true;
  }

  // === 2. REALTOR PLACARD (anomaly: face) ===
  const rN = makeTex(512, 640); const rOff = makeTex(512, 640);
  drawRealtor(rN.ctx, 512, 640, true); rN.tex.needsUpdate = true;
  drawRealtor(rOff.ctx, 512, 640, false); rOff.tex.needsUpdate = true;
  const placard = plane(0.34, 0.42, rN.tex);
  const placardGroup = new THREE.Group();
  placardGroup.add(placard);
  placardGroup.position.set(8.2, 1.15, -8.92);
  placardGroup.rotation.y = 0.12;
  placardGroup.rotation.z = -0.02;
  group.add(placardGroup);
  const pAnchor = new THREE.Object3D(); placardGroup.add(pAnchor);
  const realtorPortrait = {
    root: placardGroup, room: 'yard',
    getAnchor: (v = new THREE.Vector3()) => pAnchor.getWorldPosition(v),
    setOff() { placard.material.map = rOff.tex; placard.material.needsUpdate = true; },
    setNormal() { placard.material.map = rN.tex; placard.material.needsUpdate = true; },
  };
  realtorPortrait.anomaly = new Anomaly(realtorPortrait);
  realtorPortrait.setNormal();
  anomalies.push(realtorPortrait);

  // === 3. TWO OPEN HOUSE FLYERS (set dressing) ===
  const flyerTex = makeTex(512, 680); drawFlyer(flyerTex.ctx, 512, 680); flyerTex.tex.needsUpdate = true;
  function flyer(x, y, z, ry) {
    const f = plane(0.3, 0.4, flyerTex.tex);
    f.position.set(x, y, z); f.rotation.y = ry; f.rotation.z = (Math.random() * 0.06 - 0.03);
    // curl one corner by nudging a vertex
    const pos = f.geometry.attributes.position;
    pos.setZ(1, pos.getZ(1) + 0.03); pos.needsUpdate = true;
    group.add(f);
  }
  flyer(4.4, 1.15, -8.92, 0.06);          // on the fence west of the gate
  flyer(4.72, 1.35, -1.62, Math.PI);      // on a porch post

  // === 4. INSPECTION NOTICE on the front door (set dressing) ===
  const inspTex = makeTex(512, 360); drawInspection(inspTex.ctx, 512, 360); inspTex.tex.needsUpdate = true;
  const insp = plane(0.2, 0.14, inspTex.tex);
  insp.position.set(6.25, 1.45, -0.11);
  insp.rotation.y = Math.PI;
  insp.rotation.z = 0.03;
  group.add(insp);

  return { group, colliders, anomalies, yardSign, realtorPortrait, setBuyer };
}
