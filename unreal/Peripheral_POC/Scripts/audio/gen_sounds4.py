#!/usr/bin/env python3
"""Third anomaly pass: sounds from outside and from other rooms (steps on gravel, the porch boards, a door closing, a drip).
One-shots, mono, into SourceArt/Audio."""
import os, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Audio")
SR = 44100
rng = np.random.default_rng(57)
t = lambda sec: np.arange(int(sec * SR)) / SR
noise = lambda n: rng.normal(0, 1, n)


def save(name, x, peak=0.8):
    x = x / (np.abs(x).max() + 1e-9) * peak
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())


def band(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR); X = np.fft.rfft(x)
    X *= (1 / (1 + (lo / np.maximum(f, 1e-6)) ** 4)) * (1 / (1 + (f / hi) ** 4))
    return np.fft.irfft(X, len(x))


def room(x, sec=0.5, mix=0.25):
    n = int(sec * SR); ir = noise(n) * np.exp(-np.arange(n) / (n * 0.22)); ir = band(ir, 150, 2500)
    y = np.convolve(x, ir); y = y / (np.abs(y).max() + 1e-9)
    return np.concatenate([x, np.zeros(len(y) - len(x))]) * (1 - mix) + y * mix


def place(total, parts):
    out = np.zeros(int(total * SR))
    for (at, x) in parts:
        i = max(0, int(at * SR)); x = x[:len(out) - i]; out[i:i + len(x)] += x
    return out


def thunk(f, sec, click=0.5, damp=22):
    tt = t(sec)
    return np.sin(2 * np.pi * f * tt * (1 + 0.3 * np.exp(-tt * 40))) * np.exp(-tt * damp) + click * band(noise(len(tt)), 400, 3000) * np.exp(-tt * 160)


def crunch(sec=0.32):
    """One footfall on gravel: a burst of small stones, heel then toe."""
    n = int(sec * SR); tt = np.arange(n) / SR
    env = np.exp(-tt * 16) + 0.7 * np.exp(-np.maximum(tt - 0.11, 0) * 22) * (tt > 0.11)
    grit = band(noise(n), 900, 7000) * (rng.random(n) > 0.55)
    return grit * env


save("gravel_steps", band(place(3.4, [(i * 0.62 + rng.uniform(-0.04, 0.04), crunch() * (1.0 - 0.12 * i)) for i in range(5)]), 300, 5000), 0.6)
tt = t(0.7); f = 210 + 90 * np.sin(np.pi * tt / 0.7) + 9 * np.sin(2 * np.pi * 13 * tt)
gr = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.sin(2 * np.pi * 43 * tt) ** 2); gr = band(gr, 300, 2200) * np.sin(np.pi * tt / 0.7) ** 2
save("porch_creak", room(place(2.2, [(0.0, thunk(58, 0.3, 0.3, 18)), (0.1, gr * 0.8), (1.05, thunk(52, 0.3, 0.3, 18) * 0.7), (1.15, gr[::-1] * 0.5)]), 0.35, 0.2), 0.65)
latch = thunk(1400, 0.04, 1.0, 120)
save("door_close", room(place(1.2, [(0.0, band(thunk(74, 0.5, 0.8, 13), 30, 900)), (0.045, latch * 0.5), (0.09, latch * 0.3)]), 0.7, 0.4), 0.8)
def drop(f):
    tt = t(0.16)
    return np.sin(2 * np.pi * f * tt * (1 + 1.4 * np.exp(-tt * 55))) * np.exp(-tt * 30)
save("water_drip", room(place(4.2, [(0.0, drop(820)), (1.25, drop(900) * 0.8), (2.4, drop(780) * 0.9), (3.7, drop(860) * 0.6)]), 0.9, 0.45), 0.5)
print("sounds4 written")
