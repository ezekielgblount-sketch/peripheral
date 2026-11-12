#!/usr/bin/env python3
"""Playtest round 1 surfaces: kitchen sheet vinyl, bathroom hex and mosaic tile, the loud carpets, the guest-room floral,
driveway concrete with cracks and oil, garden soil. Adds to SourceArt/Textures and its manifest. Run: gen_surfaces2.py"""
import os, sys, json, random
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texlib import *

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Textures")
W = Writer(OUT)
U, V = grid()


def lin(im):
    return (np.asarray(im).astype(np.float64) / 255.0) ** 2.2


def lines(c, n, width_frac):
    """1 on the seams of an n-per-tile grid along coordinate c."""
    p = (c * n) % 1.0
    return 1 - smooth(width_frac * 0.5, width_frac, np.minimum(p, 1 - p))


# ---- kitchen: almond-and-brown sheet vinyl, printed as 30 cm "tiles" with a small brown diamond where four meet ----
cu, cv = (U * 2) % 1.0, (V * 2) % 1.0
seam = np.maximum(lines(U, 2, 0.022), lines(V, 2, 0.022))
dia = 1 - smooth(0.075, 0.085, np.abs(np.minimum(cu, 1 - cu)) + np.abs(np.minimum(cv, 1 - cv)))        # diamonds on the corners
marble = norm01(fnoise(201, 1.7, 2, 60) + 0.5 * fnoise(202, 0.8, 30, 200))
vein = smooth(0.46, 0.5, fnoise(203, 1.9, 3, 30)) * (1 - smooth(0.5, 0.54, fnoise(203, 1.9, 3, 30)))
bc = mix((0.70, 0.60, 0.42), (0.83, 0.76, 0.60), marble)
bc = bc * (1 - 0.35 * vein[..., None]) + color((0.50, 0.36, 0.20)) * 0.35 * vein[..., None]
bc = bc * (1 - seam[..., None]) + color((0.48, 0.36, 0.22)) * seam[..., None]
bc = bc * (1 - dia[..., None]) + color((0.30, 0.17, 0.08)) * dia[..., None]
scuff = smooth(0.55, 0.8, fnoise(204, 1.8, 2, 14))
grey = fnoise(205, 1.2, 6, 120, sx=5)
bc = bc * (0.93 - 0.16 * scuff + 0.08 * grey)[..., None]
W.save("vinyl", bc, norm01(0.15 * marble + (1 - seam) * 0.8), 0.30 + 0.35 * scuff + 0.25 * seam, 61, bump=0.25)

# ---- bathrooms: small white hex tile, dingy grout ----
n, m = 12, 7                                                    # 12 hexes across, 7 double rows
x, y = U * n, V * m * 2
best = np.full(U.shape, 9.0); cid = np.zeros(U.shape, int)
for row in (-1, 0, 1, 2):
    ry = np.floor(y) + row
    off = 0.5 * (ry % 2)
    cx = np.round(x - off) + off
    dx, dy = (x - cx), (y - ry) * 0.87
    hexd = np.maximum(np.abs(dx), 0.5 * np.abs(dx) + 0.87 * np.abs(dy))
    take = hexd < best
    best = np.where(take, hexd, best); cid = np.where(take, ((cx * 2).astype(int) % (2 * n)) + 50 * (ry.astype(int) % (2 * m)), cid)
grout = smooth(0.40, 0.47, best)
rng = np.random.default_rng(210); tone = lerp(0.9, 1.03, rng.random(cid.max() + 1))[cid]
dingy = 0.55 + 0.45 * fnoise(211, 1.6, 2, 30)
bc = color((0.86, 0.85, 0.80)) * tone[..., None] * (0.95 + 0.06 * fnoise(212, 1.0, 20, 200))[..., None]
bc = bc * (1 - grout[..., None]) + color((0.42, 0.38, 0.31), dingy) * grout[..., None]
W.save("hex", bc, norm01(1 - grout) * 0.9 + 0.1 * fnoise(213, 1.0, 10, 80), 0.14 + 0.78 * grout, 30, bump=1.0)

# ---- half bath: 5 cm square mosaic, mostly white with the odd pale blue tile ----
g = np.maximum(lines(U, 8, 0.07), lines(V, 8, 0.07))
tid = (np.floor(U * 8) + 8 * np.floor(V * 8)).astype(int)
rng = np.random.default_rng(220); pick = rng.random(64)[tid]; tone = lerp(0.92, 1.03, rng.random(64))[tid]
bc = mix((0.85, 0.85, 0.82), (0.50, 0.66, 0.80), (pick > 0.8).astype(float)) * tone[..., None]
bc = bc * (1 - g[..., None]) + color((0.44, 0.40, 0.33), 0.55 + 0.45 * fnoise(221, 1.6, 2, 30)) * g[..., None]
W.save("sq", bc, norm01(1 - g) * 0.9 + 0.1 * fnoise(222, 1.0, 10, 80), 0.16 + 0.76 * g, 40, bump=1.0)

# ---- carpets ----
pile = norm01(fnoise(230, 0.2, 150, 420) + 0.5 * fnoise(231, 1.5, 10, 40))
track = fnoise(232, 1.6, 2, 9, sx=6)                             # vacuum tracks and foot traffic
W.save("carpet_plush", color((0.80, 0.80, 0.80), 0.62 + 0.3 * pile + 0.16 * track), pile, 0.96, 60, bump=2.2)


def kids(d, x, y, k, rot, r):
    cols = [(226, 44, 52), (250, 196, 30), (28, 150, 70), (240, 110, 30), (40, 190, 205), (236, 80, 150)]
    c = cols[int(k * 997) % 6]; s = 26 + (k * 53) % 26
    kind = int(k * 7919) % 5
    if kind == 0:
        d.polygon([(x + s * np.cos(rot + t), y + s * np.sin(rot + t)) for t in (0, 2.09, 4.19)], fill=c)
    elif kind == 1:
        d.line([(x + i * 13, y + 13 * np.sin(i * 1.4 + rot)) for i in range(-5, 6)], fill=c, width=9)
    elif kind == 2:
        d.ellipse([x - s * 0.5, y - s * 0.5, x + s * 0.5, y + s * 0.5], outline=c, width=9)
    elif kind == 3:
        d.rectangle([x - s * 0.45, y - s * 0.45, x + s * 0.45, y + s * 0.45], fill=c)
    else:
        for i in range(3):
            d.line([(x - s, y + i * 12), (x + s, y + i * 12)], fill=c, width=5)


def pattern(seed, bg, fn, count):
    im = Image.new("RGB", (N, N), bg); d = ImageDraw.Draw(im); r = random.Random(seed)
    for _ in range(count):
        x, y, k, rot = r.uniform(0, N), r.uniform(0, N), r.random(), r.uniform(0, 6.28)
        for ox in (-N, 0, N):
            for oy in (-N, 0, N):
                fn(d, x + ox, y + oy, k, rot, r)
    return lin(im)


W.save("carpet_kids", pattern(7, (26, 38, 96), kids, 95) * (0.62 + 0.42 * pile)[..., None], pile, 0.95, 170, bump=2.0)

a, b = fnoise(240, 1.1, 6, 40), fnoise(241, 1.1, 9, 60)
green = smooth(0.48, 0.56, a); tan = smooth(0.70, 0.74, b) * (1 - green)
fleck = smooth(0.80, 0.84, fnoise(242, 0.3, 90, 300))
bc = mix((0.20, 0.035, 0.05), (0.045, 0.11, 0.07), green)
bc = bc * (1 - tan[..., None]) + color((0.36, 0.26, 0.15)) * tan[..., None]
bc = bc * (1 - 0.7 * fleck[..., None]) + color((0.45, 0.37, 0.22)) * 0.7 * fleck[..., None]
W.save("carpet_den", bc * (0.6 + 0.45 * pile)[..., None], norm01(pile + 0.3 * green), 0.96, 110, bump=2.4)


def sprig(d, c):
    """Guest room paper: little rose-pink blooms and sage sprigs on cream, half-drop."""
    for iy in range(-1, 9):
        for ix in range(-1, 9):
            x = ix * c + (c / 2 if iy % 2 else 0); y = iy * c
            if (ix + iy) % 2 == 0:
                for i in range(6):
                    t = i * 1.047 + 0.2
                    d.ellipse([x + 10 * np.cos(t) - 9, y + 10 * np.sin(t) - 9, x + 10 * np.cos(t) + 9, y + 10 * np.sin(t) + 9], fill=(196, 112, 122))
                d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(150, 62, 78))
                for (ox, oy) in ((-24, 10), (22, 14)):
                    d.ellipse([x + ox - 10, y + oy - 5, x + ox + 10, y + oy + 5], fill=(120, 146, 104))
            else:
                d.line([(x - 14, y + 14), (x + 2, y), (x + 14, y - 14)], fill=(120, 146, 104), width=4)
                for (ox, oy) in ((-14, 14), (14, -14)):
                    d.ellipse([x + ox - 5, y + oy - 5, x + ox + 5, y + oy + 5], fill=(214, 150, 150))


im = Image.new("RGB", (N, N), (238, 228, 206)); sprig(ImageDraw.Draw(im), N / 8.0)
wv = fnoise(250, 0.3, 120, 420)
W.save("floral", lin(im) * (0.95 + 0.07 * wv)[..., None], wv * 0.3, 0.8, 76, bump=0.25)

# ---- driveway and garage floor: concrete with a control joint, cracks and oil stains (one 6 m tile) ----
n1 = fnoise(260, 1.4, 9, 300); pits = smooth(0.74, 0.82, fnoise(261, 0.3, 60, 200))
c1, c2 = fnoise(262, 2.0, 1, 7), fnoise(263, 2.0, 2, 9)
crack = np.maximum(1 - smooth(0.0, 0.006, np.abs(c1 - 0.5)), (1 - smooth(0.0, 0.004, np.abs(c2 - 0.47))) * smooth(0.5, 0.6, fnoise(264, 2.0, 1, 4)))
joint = np.maximum(lines(U, 2, 0.006), lines(V, 2, 0.006))
oil = np.zeros(U.shape); rr = random.Random(9)
for _ in range(9):
    ox, oy, rad = rr.random(), rr.random(), rr.uniform(0.02, 0.07)
    dd = np.sqrt(np.minimum(np.abs(U - ox), 1 - np.abs(U - ox)) ** 2 + np.minimum(np.abs(V - oy), 1 - np.abs(V - oy)) ** 2)
    oil = np.maximum(oil, (1 - smooth(rad * 0.35, rad, dd * (0.8 + 0.5 * fnoise(265 + _, 1.5, 3, 20)))) * rr.uniform(0.5, 1.0))
bc = color((0.55, 0.54, 0.51), 0.72 + 0.36 * n1) * (1 - 0.35 * pits[..., None])
bc = bc * (1 - 0.82 * oil[..., None]) * (1 - 0.8 * crack[..., None]) * (1 - 0.6 * joint[..., None])
W.save("drive", bc, norm01(n1 * 0.4 + (1 - pits) - 1.5 * crack - 1.2 * joint), 0.9 - 0.5 * oil, 600, bump=0.9)

soil = norm01(fnoise(270, 0.9, 12, 200) + 0.5 * fnoise(271, 0.3, 80, 400))
W.save("soil", mix((0.06, 0.04, 0.025), (0.22, 0.15, 0.09), soil), soil, 0.95, 80, bump=3.0)

man = {}
mp = os.path.join(OUT, "manifest.json")
if os.path.exists(mp):
    man = json.load(open(mp))
man.update(W.manifest)
json.dump(man, open(mp, "w"), indent=1)
print("wrote", sorted(W.manifest))
