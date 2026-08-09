// Shared constants for Peripheral. One place so house geometry, fovea math,
// and the director all agree on the same numbers.

import * as THREE from 'three';

// --- Palette (the only colours in the game) ---
export const PAL = {
  black:  0x1a1916,
  dark:   0x4e4b44,
  mid:    0x7c7870,
  light:  0xb3a78f,
  pale:   0xe6dfcc,
  // The single warm exception, Act 2 flashlight only.
  warm:   0xffe6b8,
};

// --- Scale (metres) ---
export const CEILING = 2.5;
export const WALL_T = 0.15;      // wall thickness
export const DOOR_W = 0.9;       // doorway clear width
export const EYE_H = 1.65;       // camera eye height while standing

// --- Player ---
export const PLAYER_RADIUS = 0.3;
export const PLAYER_HEIGHT = 1.7;   // capsule total height
export const WALK_SPEED = 2.6;      // m/s
export const SLOW_SPEED = 1.3;      // m/s (Shift)

// --- Fovea zones (radians) ---
export const FOVEA_DEG = 11;
export const NEAR_PERI_DEG = 26;
export const ARM_MIN_DEG = 40;      // an armed anomaly may only flip when fovea is beyond this
export const RESOLVE_DWELL = 0.12;  // s the fovea must rest on an ACTIVE anomaly to resolve it

export const FOVEA_COS = Math.cos(THREE.MathUtils.degToRad(FOVEA_DEG));
export const NEAR_PERI_COS = Math.cos(THREE.MathUtils.degToRad(NEAR_PERI_DEG));
export const ARM_MIN_COS = Math.cos(THREE.MathUtils.degToRad(ARM_MIN_DEG));
// Hysteresis: once resolving has begun, allow drift out to a slightly wider cone.
export const FOVEA_HYST_COS = Math.cos(THREE.MathUtils.degToRad(FOVEA_DEG + 4));

// --- Director pacing ---
export const ARM_INTERVAL_MIN = 25;   // s
export const ARM_INTERVAL_MAX = 40;   // s
export const SPENT_COOLDOWN_MIN = 60; // s
export const SPENT_COOLDOWN_MAX = 120;// s

// --- Act 2 entity ---
export const CRICKET_STOP_DIST = 15;  // m, entity closer than this + unoccluded => crickets stop
export const CRICKET_RESUME_DELAY = 6;// s after entity gone

export const LAYER_DEFAULT = 0;
