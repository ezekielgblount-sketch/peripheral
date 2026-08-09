import * as THREE from 'three';
import { PAL } from '../constants.js';
import { Anomaly } from '../game/anomaly.js';
import { makeDoor } from './house.js';

// Every prop in the house. Eight of them are anomaly-capable: each has an
// instantaneous setOff()/setNormal() and an anchor point the fovea math uses.
// The rest is furniture so the rooms read as a home. Nothing here tweens the
// anomaly transition — off/normal are single-frame swaps.

export function buildProps(scene, house) {
  const group = new THREE.Group();
  scene.add(group);

  const M = {
    wood: new THREE.MeshStandardMaterial({ color: PAL.dark, roughness: 1, metalness: 0 }),
    pale: new THREE.MeshStandardMaterial({ color: PAL.light, roughness: 1, metalness: 0 }),
    cloth: new THREE.MeshStandardMaterial({ color: PAL.mid, roughness: 1, metalness: 0 }),
    dark: new THREE.MeshStandardMaterial({ color: 0x121210, roughness: 1, metalness: 0 }),
    shadow: new THREE.MeshStandardMaterial({ color: 0x0c0c0a, roughness: 1, metalness: 0 }),
    metal: new THREE.MeshStandardMaterial({ color: PAL.mid, roughness: 1, metalness: 0 }),
    mirror: new THREE.MeshStandardMaterial({ color: 0x3a3a38, roughness: 1, metalness: 0 }),
  };
  const box = (w, h, d, mat) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    m.castShadow = true; m.receiveShadow = true; return m;
  };

  const list = [];
  // helper: register an anomaly prop
  function anomalyProp(cfg) {
    cfg.getAnchor = cfg.getAnchor || ((v = new THREE.Vector3()) => cfg.anchor.getWorldPosition(v));
    cfg.anomaly = new Anomaly(cfg);
    cfg.setNormal(); // start in normal state
    list.push(cfg);
    return cfg;
  }

  // ================= LIVING ROOM (x0..4.5, z0..6) =================
  // sofa
  {
    const g = new THREE.Group();
    const base = box(2.0, 0.4, 0.8, M.cloth); base.position.y = 0.25; g.add(base);
    const back = box(2.0, 0.5, 0.2, M.cloth); back.position.set(0, 0.6, -0.3); g.add(back);
    g.position.set(2.2, 0, 1.2); g.rotation.y = 0; group.add(g);
  }
  // low table
  { const t = box(1.0, 0.35, 0.6, M.wood); t.position.set(2.2, 0.18, 2.6); group.add(t); }

  // floor lamp (ANOMALY): upright/level  ->  shade tilted ~30deg, leaning
  {
    const g = new THREE.Group();
    const pole = box(0.05, 1.5, 0.05, M.metal); pole.position.y = 0.75; g.add(pole);
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.04, 12), M.metal);
    base.position.y = 0.02; g.add(base);
    const shadeGroup = new THREE.Group(); shadeGroup.position.y = 1.5; g.add(shadeGroup);
    const shade = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.28, 0.35, 16, 1, true), M.pale);
    shade.position.y = 0.0; shadeGroup.add(shade);
    const anchor = new THREE.Object3D(); anchor.position.y = 0.0; shadeGroup.add(anchor);
    g.position.set(0.7, 0, 4.6); group.add(g);
    anomalyProp({
      root: g, room: 'living', anchor,
      setOff() { g.rotation.z = THREE.MathUtils.degToRad(6); shadeGroup.rotation.z = THREE.MathUtils.degToRad(30); },
      setNormal() { g.rotation.z = 0; shadeGroup.rotation.z = 0; },
    });
  }

  // wall portrait (ANOMALY): figure facing forward -> head turned toward player
  {
    const g = new THREE.Group();
    const frame = box(0.5, 0.7, 0.04, M.wood); g.add(frame);
    const canvas = box(0.42, 0.62, 0.02, M.mirror); canvas.position.z = 0.02; g.add(canvas);
    // a crude figure
    const body = box(0.16, 0.34, 0.02, M.shadow); body.position.set(0, -0.08, 0.03); g.add(body);
    const head = box(0.13, 0.14, 0.06, M.shadow); head.position.set(0, 0.16, 0.03); g.add(head);
    // face marks (two pale eyes) as children of head so they turn with it
    const eyeL = box(0.02, 0.02, 0.01, M.pale); eyeL.position.set(-0.03, 0.0, 0.031); head.add(eyeL);
    const eyeR = box(0.02, 0.02, 0.01, M.pale); eyeR.position.set(0.03, 0.0, 0.031); head.add(eyeR);
    const anchor = new THREE.Object3D(); anchor.position.set(0, 0.1, 0.1); g.add(anchor);
    g.position.set(0.09, 1.6, 2.4); g.rotation.y = Math.PI / 2; group.add(g); // on west wall, facing +x
    anomalyProp({
      root: g, room: 'living', anchor,
      setOff() { head.rotation.y = THREE.MathUtils.degToRad(62); }, // head cranks toward the room
      setNormal() { head.rotation.y = 0; },
    });
  }

  // ================= ENTRY (x4.5..7.5, z0..3) =================
  { const t = box(0.9, 0.8, 0.35, M.wood); t.position.set(7.1, 0.4, 2.6); t.rotation.y = 0; group.add(t); }
  // coat on hook (ANOMALY): flat -> filled, as if worn
  {
    const g = new THREE.Group();
    const hookBoard = box(0.5, 0.12, 0.04, M.wood); hookBoard.position.y = 0; g.add(hookBoard);
    const flat = box(0.34, 0.8, 0.06, M.cloth); flat.position.set(0, -0.45, 0.03);
    const filled = new THREE.Group();
    const torso = box(0.36, 0.6, 0.22, M.cloth); torso.position.set(0, -0.4, 0.12); filled.add(torso);
    const hem = box(0.4, 0.2, 0.26, M.cloth); hem.position.set(0, -0.78, 0.12); filled.add(hem);
    const shoulders = box(0.44, 0.12, 0.2, M.cloth); shoulders.position.set(0, -0.16, 0.12); filled.add(shoulders);
    g.add(flat); g.add(filled);
    const anchor = new THREE.Object3D(); anchor.position.set(0, -0.4, 0.12); g.add(anchor);
    g.position.set(4.7, 1.7, 1.4); g.rotation.y = Math.PI / 2; group.add(g); // on the west-ish entry wall
    anomalyProp({
      root: g, room: 'entry', anchor,
      setOff() { flat.visible = false; filled.visible = true; },
      setNormal() { flat.visible = true; filled.visible = false; },
    });
  }

  // ================= KITCHEN (x7.5..12, z0..6) =================
  // counter run along the east/north
  { const c = box(0.6, 0.9, 4.0, M.pale); c.position.set(11.5, 0.45, 3.0); group.add(c); }
  { const c = box(3.5, 0.9, 0.6, M.pale); c.position.set(9.8, 0.45, 5.4); group.add(c); }
  // table + chairs
  const kTable = box(1.1, 0.75, 0.7, M.wood); kTable.position.set(9.2, 0.375, 2.2); group.add(kTable);
  function chair(x, z, ry, mat = M.wood) {
    const g = new THREE.Group();
    const seat = box(0.4, 0.06, 0.4, mat); seat.position.y = 0.45; g.add(seat);
    const back = box(0.4, 0.5, 0.06, mat); back.position.set(0, 0.7, -0.17); g.add(back);
    for (const [sx, sz] of [[-0.16, -0.16], [0.16, -0.16], [-0.16, 0.16], [0.16, 0.16]]) {
      const leg = box(0.05, 0.45, 0.05, mat); leg.position.set(sx, 0.225, sz); g.add(leg);
    }
    g.position.set(x, 0, z); g.rotation.y = ry; group.add(g); return g;
  }
  chair(9.2, 1.5, 0);
  chair(8.4, 2.2, Math.PI / 2);
  chair(10.0, 2.2, -Math.PI / 2);
  // kitchen chair (ANOMALY): tucked -> pulled out and turned to face the hall
  {
    const g = new THREE.Group();
    const seat = box(0.4, 0.06, 0.4, M.wood); seat.position.y = 0.45; g.add(seat);
    const back = box(0.4, 0.5, 0.06, M.wood); back.position.set(0, 0.7, -0.17); g.add(back);
    for (const [sx, sz] of [[-0.16, -0.16], [0.16, -0.16], [-0.16, 0.16], [0.16, 0.16]]) {
      const leg = box(0.05, 0.45, 0.05, M.wood); leg.position.set(sx, 0.225, sz); g.add(leg);
    }
    const anchor = new THREE.Object3D(); anchor.position.set(0, 0.5, 0); g.add(anchor);
    group.add(g);
    const tuck = { x: 9.2, z: 2.9, ry: Math.PI };
    const pulled = { x: 8.3, z: 3.6, ry: -Math.PI * 0.7 }; // faces toward the entry/hall
    anomalyProp({
      root: g, room: 'kitchen', anchor,
      setOff() { g.position.set(pulled.x, 0, pulled.z); g.rotation.y = pulled.ry; },
      setNormal() { g.position.set(tuck.x, 0, tuck.z); g.rotation.y = tuck.ry; },
    });
  }

  // ================= HALLWAY (x4.5..7.5, z3..14) =================
  // Four real door leaves in their frames. One (the bathroom door) is the
  // "ajar 15deg -> wide open" anomaly.
  const hallDoors = [];
  function hallDoor(x, z, ry, ajar = 0) {
    const d = makeDoor(M.wood, 0.9, 2.05);
    d.group.position.set(x, 0, z); d.group.rotation.y = ry;
    d.setAjar(ajar);
    group.add(d.group);
    hallDoors.push(d);
    return d;
  }
  const doorBath = hallDoor(4.5, 7.0, 0, THREE.MathUtils.degToRad(15));  // west, bathroom (ANOMALY)
  hallDoor(4.5, 11.0, 0, 0);                                            // west, study
  hallDoor(7.5, 7.0, Math.PI, 0);                                       // east, bedroom
  hallDoor(7.5, 11.0, Math.PI, 0);                                      // east, utility
  {
    const anchor = new THREE.Object3D(); anchor.position.set(0.45, 1.0, 0); doorBath.group.add(anchor);
    anomalyProp({
      root: doorBath.group, room: 'hallway', anchor,
      setOff() { doorBath.setAjar(THREE.MathUtils.degToRad(88)); },
      setNormal() { doorBath.setAjar(THREE.MathUtils.degToRad(15)); },
    });
  }

  // hallway FIVE DOORS (ANOMALY): a phantom door appears on the west wall
  {
    const d = makeDoor(M.wood, 0.9, 2.05);
    d.group.position.set(4.5, 0, 9.0); d.group.rotation.y = 0;
    d.setAjar(0);
    // frame around it so it reads as a real doorway
    const frame = new THREE.Group();
    const top = box(1.0, 0.12, 0.16, M.wood); top.position.set(0.45, 2.0, 0); frame.add(top);
    const side1 = box(0.1, 2.05, 0.16, M.wood); side1.position.set(0.0, 1.02, 0); frame.add(side1);
    const side2 = box(0.1, 2.05, 0.16, M.wood); side2.position.set(0.95, 1.02, 0); frame.add(side2);
    d.group.add(frame);
    group.add(d.group);
    const anchor = new THREE.Object3D(); anchor.position.set(0.45, 1.0, 0); d.group.add(anchor);
    anomalyProp({
      root: d.group, room: 'hallway', anchor,
      setOff() { d.group.visible = true; },
      setNormal() { d.group.visible = false; },
    });
  }

  // ================= BATHROOM (x0..4.5, z6..10) =================
  { const s = box(0.6, 0.85, 0.5, M.pale); s.position.set(0.6, 0.42, 6.8); group.add(s); } // sink cabinet
  { const tub = box(1.6, 0.55, 0.75, M.pale); tub.position.set(2.2, 0.28, 9.3); group.add(tub); }
  // bathroom MIRROR (ANOMALY): flat grey plane -> a dark shape stands in it
  {
    const g = new THREE.Group();
    const plane = box(0.6, 0.8, 0.02, M.mirror); plane.userData.noOcclude = true; g.add(plane);
    // the shape lives just "inside" the mirror (behind the plane), hidden normally
    const shape = new THREE.Group();
    const torso = box(0.24, 0.5, 0.08, M.shadow); torso.position.set(0.02, 0.0, -0.12); shape.add(torso);
    const head = box(0.16, 0.18, 0.08, M.shadow); head.position.set(0.02, 0.34, -0.12); shape.add(head);
    shape.visible = false; g.add(shape);
    const anchor = new THREE.Object3D(); anchor.position.set(0, 0.1, -0.05); g.add(anchor);
    g.position.set(0.09, 1.5, 6.8); g.rotation.y = Math.PI / 2; group.add(g); // west wall of bathroom
    anomalyProp({
      root: g, room: 'bathroom', anchor,
      setOff() { shape.visible = true; },
      setNormal() { shape.visible = false; },
    });
  }

  // ================= STUDY (x0..4.5, z10..14) =================
  const desk = box(1.4, 0.75, 0.7, M.wood); desk.position.set(1.3, 0.375, 12.6); group.add(desk);
  chair(1.3, 11.9, 0);
  { const sh = box(0.4, 2.0, 1.6, M.wood); sh.position.set(0.3, 1.0, 12.6); group.add(sh); } // shelves on west

  // ================= BEDROOM (x7.5..12, z6..10) =================
  // bed (interactable, set up by acts/main via anchors)
  {
    const g = new THREE.Group();
    const frame = box(1.4, 0.35, 2.0, M.wood); frame.position.y = 0.2; g.add(frame);
    const mattress = box(1.3, 0.2, 1.9, M.cloth); mattress.position.y = 0.45; g.add(mattress);
    const pillow = box(1.1, 0.12, 0.35, M.pale); pillow.position.set(0, 0.58, -0.75); g.add(pillow);
    g.position.set(10.4, 0, 8.2); group.add(g);
    house.bedMesh = g;
  }
  // bedroom WINDOW shape (ANOMALY): empty yard -> a shape in the treeline
  {
    const g = new THREE.Group();
    const shape = new THREE.Group();
    const torso = box(0.4, 1.2, 0.3, M.shadow); torso.position.y = 0.9; shape.add(torso);
    const head = box(0.28, 0.3, 0.28, M.shadow); head.position.y = 1.7; shape.add(head);
    shape.visible = false; g.add(shape);
    const anchor = new THREE.Object3D(); anchor.position.y = 1.2; g.add(anchor);
    g.position.set(13.6, 0, 7.8); group.add(g); // outside, in the east treeline beyond the window
    anomalyProp({
      root: g, room: 'bedroom', anchor,
      setOff() { shape.visible = true; },
      setNormal() { shape.visible = false; },
    });
  }

  function updateDoors(dt) {
    for (const d of hallDoors) d.update(dt);
  }

  return { group, list, updateDoors, hallDoors };
}
