#!/usr/bin/env python3
"""Synthesises every sound in the slice (footsteps, room tone, fridge hum, outdoor air, door, drawer, click) as WAV files."""
import os, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Audio"); os.makedirs(OUT, exist_ok=True)
SR = 44100
rng = np.random.default_rng(11)


def save(name, x, peak=0.8):
    x = x / (np.abs(x).max() + 1e-9) * peak
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def noise(n): return rng.normal(0, 1, n)
def t(sec): return np.arange(int(sec * SR)) / SR


def band(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR); X = np.fft.rfft(x)
    X *= (1 / (1 + (lo / np.maximum(f, 1e-6)) ** 4)) * (1 / (1 + (f / hi) ** 4))
    return np.fft.irfft(X, len(x))


def loopable(x, fade=0.5):
    n = int(fade * SR); a = np.linspace(0, 1, n)
    y = x[:-n].copy(); y[:n] = x[:n] * a + x[-n:] * (1 - a)
    return y


def step(kind):
    tt = t(0.22)
    thump = np.sin(2 * np.pi * 75 * tt) * np.exp(-tt * 38)
    if kind == "carpet":
        return thump * 0.8 + band(noise(len(tt)), 80, 700) * np.exp(-tt * 30) * 0.9
    if kind == "wood":
        knock = (np.sin(2 * np.pi * 190 * tt) + 0.6 * np.sin(2 * np.pi * 310 * tt)) * np.exp(-tt * 26)
        return thump * 0.6 + knock * 0.8 + band(noise(len(tt)), 300, 3000) * np.exp(-tt * 70) * 0.5
    return thump * 0.4 + band(noise(len(tt)), 900, 6000) * np.exp(-tt * 110) * 1.0 + np.sin(2 * np.pi * 520 * tt) * np.exp(-tt * 90) * 0.3


for k in ("carpet", "wood", "tile"):
    save("step_" + k, step(k), 0.7)

tt = t(8.5)
save("room_tone", loopable(band(noise(len(tt)), 30, 400) * 0.8 + 0.05 * np.sin(2 * np.pi * 60 * tt) + band(noise(len(tt)), 2000, 9000) * 0.03), 0.25)
tt = t(6.5)
hum = sum(a * np.sin(2 * np.pi * f * tt + p) for f, a, p in ((60, 1.0, 0), (120, 0.55, 1), (180, 0.25, 2), (240, 0.1, 0.5)))
save("fridge_hum", loopable(hum * (0.9 + 0.1 * np.sin(2 * np.pi * 0.31 * tt)) + band(noise(len(tt)), 200, 1800) * 0.25), 0.5)
tt = t(24.5)
wind = band(noise(len(tt)), 60, 900) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.07 * tt) * np.sin(2 * np.pi * 0.023 * tt + 1))
leaves = band(noise(len(tt)), 2500, 9000) * 0.12 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * tt + 2)) ** 2
birds = np.zeros(len(tt))
for i in range(26):
    t0 = rng.uniform(0.5, 23); f0 = rng.uniform(2400, 4800); n = int(rng.uniform(0.06, 0.16) * SR)
    for rep in range(int(rng.integers(1, 5))):
        s = int((t0 + rep * rng.uniform(0.14, 0.22)) * SR)
        if s + n < len(tt):
            u = np.arange(n) / n
            birds[s:s + n] += np.sin(2 * np.pi * (f0 * (1 + 0.25 * np.sin(u * np.pi)) * u * n / SR)) * np.sin(u * np.pi) ** 2 * rng.uniform(0.05, 0.2)
save("outdoor_day", loopable(wind + leaves + birds, 0.6), 0.5)
tt = t(0.9)
sq = np.sin(2 * np.pi * np.cumsum(180 + 260 * tt + 40 * np.sin(2 * np.pi * 9 * tt)) / SR) * np.sign(np.sin(2 * np.pi * 31 * tt)) * 0.5
save("door_creak", (sq * 0.5 + band(noise(len(tt)), 400, 2500) * 0.4) * np.sin(np.pi * tt / 0.9) ** 0.7 + np.concatenate([np.zeros(len(tt) - 3000), step("wood")[:3000]]) * 0.0, 0.45)
tt = t(0.45)
save("drawer_slide", band(noise(len(tt)), 250, 2200) * np.sin(np.pi * tt / 0.45) + np.concatenate([np.zeros(len(tt) - 4000), step("wood")[:4000] * 1.5]), 0.5)
tt = t(0.06)
save("click", band(noise(len(tt)), 1500, 8000) * np.exp(-tt * 160) + np.sin(2 * np.pi * 2100 * tt) * np.exp(-tt * 200), 0.5)
tt = t(0.5)
save("locked_rattle", sum(np.roll(band(noise(len(tt)), 500, 4000) * np.exp(-tt * 45), int(d * SR)) for d in (0, 0.11, 0.2)), 0.5)
# ---- demo additions ----
tt = t(10.5)
save("tape_hiss", loopable(band(noise(len(tt)), 1500, 12000) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.4 * tt)) + 0.15 * np.sin(2 * np.pi * 59.5 * tt)), 0.4)
tt = t(2.0); tick = np.zeros(len(tt))
for k_, f in ((0.0, 2300), (1.0, 1900)):
    i0 = int(k_ * SR); n = int(0.03 * SR); u = np.arange(n) / SR
    tick[i0:i0 + n] += (np.sin(2 * np.pi * f * u) + band(noise(n), 1500, 7000)) * np.exp(-u * 220)
save("clock_tick", tick[:int(2.0 * SR)], 0.45)
tt = t(0.5); save("breaker_clunk", np.sin(2 * np.pi * 62 * tt) * np.exp(-tt * 14) + band(noise(len(tt)), 300, 3000) * np.exp(-tt * 40) * 0.8, 0.8)
tt = t(3.0); save("lights_hum", (np.sin(2 * np.pi * 120 * tt) + 0.4 * np.sin(2 * np.pi * 240 * tt) + band(noise(len(tt)), 3000, 9000) * 0.1) * np.minimum(1, tt * 3) * np.exp(-tt * 0.9), 0.35)
tt = t(0.7); save("stuck_lock", sum(np.roll((np.sin(2 * np.pi * 900 * tt) * 0.3 + band(noise(len(tt)), 800, 5000)) * np.exp(-tt * 60), int(d * SR)) for d in (0, 0.16, 0.3)), 0.5)
tt = t(0.4); save("box_thump", np.sin(2 * np.pi * 85 * tt) * np.exp(-tt * 22) + band(noise(len(tt)), 150, 1200) * np.exp(-tt * 35) * 0.6, 0.6)
# sparse melancholy piano over a soft pad, with long silences (96 s loop)
L_ = 96.0; tt = t(L_ + 1.0); mus = np.zeros(len(tt))
def pno(t0, f, amp=1.0, dur=6.0):
    i0 = int(t0 * SR); n = min(int(dur * SR), len(mus) - i0); u = np.arange(n) / SR
    tone = sum(a * np.sin(2 * np.pi * f * h * u * (1 + 0.0004 * h)) for h, a in ((1, 1.0), (2, 0.45), (3, 0.2), (4, 0.08)))
    mus[i0:i0 + n] += amp * tone * np.exp(-u * 0.9) * np.minimum(1, u * 200)
A3, C4, E4, G4, A4, B3, D4, F4 = 220.0, 261.63, 329.63, 392.0, 440.0, 246.94, 293.66, 349.23
for t0, f, a in ((2, A3, 1), (2.1, E4, .7), (6, C4, .8), (9.5, B3, .7), (20, A3, .9), (20.1, C4, .6), (24, E4, .8), (27, D4, .6), (31, F4, .5),
                 (46, A3 / 2, 1), (46.2, G4 / 2, .6), (50, E4, .7), (54, C4, .7), (58.5, B3, .6), (72, A3, .8), (72.1, E4, .5), (77, D4, .6), (82, C4, .7), (86, A3, .9)):
    pno(t0, f, a)
pad = sum(np.sin(2 * np.pi * f * tt + p) for f, p in ((110, 0), (164.8, 1), (220.5, 2))) * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 48.0 - 1.2)) ** 2 * 0.12
save("music_dayone", loopable(mus + band(pad, 60, 900), 1.0), 0.5)
tt = t(9.5)
save("underwater", loopable(band(noise(len(tt)), 20, 220) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.23 * tt)) + 0.5 * np.sin(2 * np.pi * 48 * tt) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.9 * tt)) ** 6), 0.6)
tt = t(6.5)
eng = sum((1.0 / h) * np.sin(2 * np.pi * 43 * h * tt + 0.3 * np.sin(2 * np.pi * 7 * tt)) for h in range(1, 9)) * (0.85 + 0.15 * np.sin(2 * np.pi * 21.5 * tt))
save("car_engine", loopable(band(eng, 30, 900) + band(noise(len(tt)), 80, 2500) * 0.35), 0.5)
tt = t(0.6); save("car_door", np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 16) + band(noise(len(tt)), 200, 2500) * np.exp(-tt * 30) + np.roll(band(noise(len(tt)), 1500, 6000) * np.exp(-tt * 80), int(0.05 * SR)) * 0.4, 0.75)
print("sounds:", sorted(os.listdir(OUT)))
