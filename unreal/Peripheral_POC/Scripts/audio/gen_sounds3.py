#!/usr/bin/env python3
"""Second anomaly pass: small sounds from somewhere else in the house (doorbell, a knock, the phone, the answering machine,
a burst from the television, pipes, a floorboard, footsteps overhead). One-shots, mono, into SourceArt/Audio."""
import os, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Audio")
SR = 44100
rng = np.random.default_rng(41)
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
    """A short tail, as heard through a wall."""
    n = int(sec * SR); ir = noise(n) * np.exp(-np.arange(n) / (n * 0.22)); ir = band(ir, 150, 2500)
    y = np.convolve(x, ir); y = y / (np.abs(y).max() + 1e-9)
    return np.concatenate([x, np.zeros(len(y) - len(x))]) * (1 - mix) + y * mix


def place(total, parts):
    out = np.zeros(int(total * SR))
    for (at, x) in parts:
        i = max(0, int(at * SR)); x = x[:len(out) - i]; out[i:i + len(x)] += x
    return out


def chime(f, sec):
    tt = t(sec)
    return sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-tt * d) for m, a, d in ((1, 1, 2.2), (2.76, 0.35, 4.0), (5.4, 0.15, 7.0)))


def thunk(f, sec, click=0.5, damp=22):
    tt = t(sec)
    return np.sin(2 * np.pi * f * tt * (1 + 0.3 * np.exp(-tt * 40))) * np.exp(-tt * damp) + click * band(noise(len(tt)), 400, 3000) * np.exp(-tt * 160)


save("doorbell", room(place(2.2, [(0.0, chime(659, 1.6)), (0.55, chime(523, 1.6))]), 0.6, 0.3), 0.7)
save("door_knock", room(place(1.3, [(i * 0.27, thunk(190 + 12 * i, 0.25, 0.9, 30)) for i in range(3)]), 0.4, 0.3), 0.75)
tt = t(1.9); bell = (np.sin(2 * np.pi * 1180 * tt) + 0.8 * np.sin(2 * np.pi * 1525 * tt) + 0.4 * np.sin(2 * np.pi * 2460 * tt)) * (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 24 * tt)))
bell *= np.minimum(1, tt * 60) * np.minimum(1, (1.9 - tt) * 8)
save("phone_ring", room(place(6.0, [(0.0, bell), (3.9, bell)]), 0.5, 0.2), 0.6)
tt = t(0.45); beep = np.sin(2 * np.pi * 1000 * tt) * np.minimum(1, tt * 200) * np.minimum(1, (0.45 - tt) * 200)
hiss = band(noise(int(1.6 * SR)), 2000, 9000) * 0.12
save("machine_beep", place(1.7, [(0.0, thunk(900, 0.05, 1.0, 90)), (0.15, beep), (0.0, hiss), (1.55, thunk(700, 0.05, 1.0, 90))]), 0.5)
n = int(0.8 * SR); st = band(noise(n), 300, 9000) * np.minimum(1, np.arange(n) / 300.0) * (np.arange(n) < n - 400)
save("tv_burst", place(1.0, [(0.0, thunk(120, 0.1, 1.0, 50)), (0.03, st * 0.7), (0.83, thunk(90, 0.12, 0.6, 40))]), 0.6)
pk = lambda f: thunk(f, 0.5, 0.6, 14) + 0.35 * np.sin(2 * np.pi * f * 4.7 * t(0.5)) * np.exp(-t(0.5) * 9)
save("pipe_knock", room(place(2.4, [(0.0, pk(96)), (0.42, pk(92) * 0.8), (0.95, pk(99) * 0.55), (1.3, pk(94) * 0.3)]), 0.7, 0.35), 0.75)
tt = t(0.95); f = 150 + 70 * np.sin(np.pi * tt / 0.95) + 12 * np.sin(2 * np.pi * 9 * tt)
creak = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.sin(2 * np.pi * 31 * tt) ** 2); creak = band(creak, 500, 2600) * np.sin(np.pi * tt / 0.95) ** 2
save("floor_creak", room(place(1.3, [(0.0, thunk(70, 0.2, 0.3, 26) * 0.6), (0.08, creak)]), 0.4, 0.3), 0.6)
steps = [(i * 0.56 + rng.uniform(-0.03, 0.03), band(thunk(62 + 5 * (i % 2), 0.4, 0.4, 16), 30, 240) * (1.0 - 0.1 * i)) for i in range(5)]
save("steps_above", room(place(3.2, steps), 0.5, 0.3), 0.8)
print("sounds3 written")
