#!/usr/bin/env python3
"""Playtest round 1 sounds: the chore loops and one-shots, and PLACEHOLDER music for the six named music slots
(music_title, music_day1_calm, music_unease_low, music_unease_mid, music_unease_high, music_loop_sequence).
Drop a real track over any of those WAVs in SourceArt/Audio and re-run import_audio.py; nothing else needs to change."""
import os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Audio")
SR = 44100
rng = np.random.default_rng(23)


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


# ---- chores ----
tt = t(4.0)
eng = sum(np.sin(2 * np.pi * f * tt + 0.3 * np.sin(2 * np.pi * 47 * tt)) / (i + 1) for i, f in enumerate((47, 94, 141, 188, 235)))
save("mower_loop", loopable(band(eng, 40, 1200) + band(noise(len(tt)), 300, 5000) * 0.6 * (0.7 + 0.3 * np.sin(2 * np.pi * 47 * tt))), 0.6)
tt = t(5.0)
slosh = band(noise(len(tt)), 150, 1500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.9 * tt) ** 2)
save("washer_loop", loopable(np.sin(2 * np.pi * 58 * tt) * 0.5 + np.sin(2 * np.pi * 116 * tt) * 0.2 + slosh * 0.8), 0.5)
tumble = band(noise(len(tt)), 80, 600) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 0.85 * tt)))
save("dryer_loop", loopable(np.sin(2 * np.pi * 73 * tt) * 0.5 + tumble * 0.9 + 0.0), 0.5)
tt = t(0.9); save("buzzer", (np.sign(np.sin(2 * np.pi * 410 * tt)) * 0.5 + np.sin(2 * np.pi * 820 * tt) * 0.3) * (tt < 0.8) * np.minimum(1, tt * 60), 0.45)
tt = t(2.5); save("water_pour", loopable(band(noise(len(tt)), 900, 9000) * (0.7 + 0.3 * np.sin(2 * np.pi * 5 * tt)) + band(noise(len(tt)), 200, 800) * 0.4, 0.3), 0.45)
tt = t(0.8); save("dish_wash", band(noise(len(tt)), 1200, 9000) * np.sin(np.pi * tt / 0.8) ** 2 * 0.7 + np.roll(np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt * 30), int(0.55 * SR)) * 0.5, 0.5)
tt = t(0.5); save("sweep", band(noise(len(tt)), 1500, 7000) * np.sin(np.pi * tt / 0.5) ** 1.5, 0.45)
tt = t(0.9); save("cloth", band(noise(len(tt)), 300, 3500) * np.sin(np.pi * tt / 0.9) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt)), 0.45)
tt = t(0.35); save("mailbox", np.sin(2 * np.pi * 520 * tt) * np.exp(-tt * 20) * 0.5 + band(noise(len(tt)), 800, 5000) * np.exp(-tt * 25), 0.5)
tt = t(2.0); save("tv_static", loopable(band(noise(len(tt)), 600, 14000), 0.3), 0.35)


# ---- placeholder music: slow pads, one per slot. They only need to tell the slots apart by ear. ----
def pad(sec, freqs, wob=0.15, trem=0.0, dark=1200, seed=0):
    tt = t(sec); r = np.random.default_rng(seed); x = np.zeros(len(tt))
    for f in freqs:
        for d in (-0.6, 0.0, 0.7):
            x += np.sin(2 * np.pi * (f + d) * tt + r.uniform(0, 6.28) + wob * np.sin(2 * np.pi * r.uniform(0.05, 0.2) * tt))
            x += 0.3 * np.sin(2 * np.pi * 2 * (f + d) * tt + r.uniform(0, 6.28))
    x *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.07 * tt)
    if trem:
        x *= 1 - trem * (0.5 + 0.5 * np.sin(2 * np.pi * 5.5 * tt))
    return band(x, 40, dark)


A = 220.0
semi = lambda n: A * 2 ** (n / 12.0)
save("music_title", loopable(pad(24, [semi(-12), semi(-5), semi(0), semi(3)], dark=900, seed=1) + 0.25 * band(noise(len(t(24))), 60, 300), 2.0), 0.5)
calm = pad(24, [semi(-12), semi(-8), semi(-5), semi(4)], dark=1600, seed=2)
tt = t(24)
for k, n in enumerate((4, 7, 12, 7, 4, 0, 4, 7)):                       # a few soft plucked notes over the pad
    s0 = int((1.5 + k * 2.8) * SR); m = len(tt) - s0
    calm[s0:] += 9 * np.sin(2 * np.pi * semi(n) * tt[:m]) * np.exp(-tt[:m] * 1.8)
save("music_day1_calm", loopable(calm, 2.0), 0.5)
save("music_unease_low", loopable(pad(24, [semi(-12), semi(-8), semi(-5), semi(3)], wob=0.5, dark=1100, seed=3), 2.0), 0.5)
save("music_unease_mid", loopable(pad(24, [semi(-24), semi(-12), semi(-11), semi(-5)], wob=1.0, dark=800, seed=4) + 0.3 * band(noise(len(t(24))), 40, 200), 2.0), 0.5)
save("music_unease_high", loopable(pad(24, [semi(-24), semi(-18), semi(-12), semi(-11)], wob=2.0, trem=0.5, dark=600, seed=5) + 0.5 * band(noise(len(t(24))), 30, 160), 2.0), 0.55)
pulse = pad(16, [semi(-24), semi(-12)], wob=0.3, dark=500, seed=6) * (0.6 + 0.4 * (np.sin(2 * np.pi * 0.75 * t(16)) > 0.6))
save("music_loop_sequence", loopable(pulse + 0.3 * pad(16, [semi(-1), semi(6)], wob=1.5, dark=1400, seed=7), 1.5), 0.5)
print("round 1 sounds and placeholder music written")
