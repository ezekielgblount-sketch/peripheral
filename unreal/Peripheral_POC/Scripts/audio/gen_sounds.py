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
print("sounds:", sorted(os.listdir(OUT)))
