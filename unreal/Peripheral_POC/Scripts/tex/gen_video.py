#!/usr/bin/env python3
"""The home video on the Day 5 tape: sixteen small frames in one 4 x 4 sheet (SourceArt/Prints/video_sheet.png), played by M_HomeVideo.
Frames 0 to 7: a boy runs through the sprinkler in the back yard while someone films. Frames 8 to 15: a birthday, the candles go out.
Nobody's face is shown: backs, distance, and a hand at the edge of the picture."""
import os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import gen_prints2 as G
FW, FH, SS = 160, 120, 4


def yard(d, W, H, i):
    pan = (i - 3.5) * W * 0.012
    d.rectangle([0, 0, W, H * 0.3], fill=(170, 200, 224)); d.rectangle([0, H * 0.24, W, H * 0.44], fill=(120, 96, 70)); d.rectangle([0, H * 0.42, W, H], fill=(86, 132, 60))
    for k in range(26):
        x = W * k / 24 - pan; d.line([(x, H * 0.24), (x, H * 0.44)], fill=(92, 72, 52), width=5)
    sx = W * 0.7 - pan
    d.arc([sx - W * 0.3, H * 0.3, sx + W * 0.3, H * 1.0], 200 + (i % 4) * 22, 262 + (i % 4) * 22, fill=(236, 240, 244), width=6)       # the sprinkler's arc sweeps
    x = W * (0.12 + 0.095 * i) - pan
    G.back(d, x, H * (0.86 - 0.02 * (i % 2)), H * 0.36, (230, 200, 60), (90, 60, 34), child=True)
    d.rectangle([x - H * 0.06 + (i % 2) * H * 0.07, H * 0.8, x - H * 0.01 + (i % 2) * H * 0.07, H * 0.9], fill=(96, 84, 30))             # a leg kicked back
    if i >= 5:
        d.polygon([(W, H * 0.7), (W * 0.86, H * (0.5 - 0.04 * (i % 2))), (W * 0.9, H * (0.44 - 0.04 * (i % 2))), (W, H * 0.56)], fill=G.SKIN)   # a hand waves into frame


def party(d, W, H, i):
    j = i - 8; lit = j < 5
    bg = (96, 70, 52) if lit else (40, 30, 26)
    d.rectangle([0, 0, W, H], fill=bg); d.rectangle([0, H * 0.62, W, H], fill=(150, 110, 70) if lit else (70, 52, 36))
    d.rectangle([W * 0.36, H * 0.5, W * 0.64, H * 0.66], fill=(240, 232, 220) if lit else (130, 124, 116)); d.rectangle([W * 0.36, H * 0.5, W * 0.64, H * 0.54], fill=(230, 150, 170) if lit else (120, 80, 90))
    r = random.Random(j)
    for k in range(6):
        x = W * (0.4 + k * 0.04)
        d.rectangle([x - 4, H * 0.42, x + 4, H * 0.5], fill=(250, 250, 240))
        if lit and not (j == 4 and k < 4):
            s = r.uniform(0.8, 1.3); d.ellipse([x - 9 * s, H * 0.425 - H * 0.055 * s, x + 9 * s, H * 0.425], fill=(255, 220, 120))
    lean = (0, 0.01, 0.03, 0.06, 0.08, 0.05, 0.02, 0)[j]
    G.back(d, W * 0.5, H * (1.25 - lean), H * 0.62, (170, 40, 40), (90, 60, 34), child=True)
    G.back(d, W * 0.16, H * 1.3, H * 0.95, (92, 70, 48), (60, 42, 30)); G.back(d, W * 0.86, H * 1.3, H * 0.9, (190, 120, 60), (120, 84, 40), dress=True)


sheet = Image.new("RGB", (FW * 4, FH * 4))
rng = np.random.default_rng(9)
for i in range(16):
    im = Image.new("RGB", (FW * SS, FH * SS)); d = ImageDraw.Draw(im)
    (yard if i < 8 else party)(d, FW * SS, FH * SS, i)
    im = im.resize((FW, FH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
    a = np.asarray(im).astype(np.float32) / 255.0
    g = a.mean(-1, keepdims=True); a = g + (a - g) * 0.7                                  # tape colour: washed, a little magenta
    a = a * np.array([1.04, 0.95, 1.0]) + rng.normal(0, 0.035, a.shape)
    y0 = int(rng.integers(0, FH - 6)); a[y0:y0 + 3] = a[y0:y0 + 3] * 0.5 + 0.45 + rng.normal(0, 0.12, a[y0:y0 + 3].shape)    # a tracking line
    a[-7:] = np.roll(a[-7:], int(rng.integers(4, 14)), axis=1)                             # head-switching tear along the bottom
    f = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    sheet.paste(f, ((i % 4) * FW, (i // 4) * FH))
sheet.save(os.path.join(G.OUT, "video_sheet.png"))
print("video sheet written")
