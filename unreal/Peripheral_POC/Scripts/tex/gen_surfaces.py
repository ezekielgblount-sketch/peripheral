#!/usr/bin/env python3
"""Generates the tiling PBR texture sets for the house surfaces into SourceArt/Textures. Run: gen_surfaces.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texlib import *

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = Writer(os.path.join(ROOT, "SourceArt", "Textures"))
U, V = grid()


def bands(coord, widths):
    """Split 0..1 into strips of the given relative widths. Returns (strip index, 0..1 position inside the strip)."""
    edges = np.cumsum([0] + list(widths)) / float(sum(widths))
    idx = np.clip(np.searchsorted(edges, coord, side="right") - 1, 0, len(widths) - 1)
    return idx, (coord - edges[idx]) / (edges[idx + 1] - edges[idx])


def per_cell(idx, seed, lo=0.0, hi=1.0):
    rng = np.random.default_rng(seed)
    return lerp(lo, hi, rng.random(int(idx.max()) + 1)[idx])


def line_mask(pos, strip_w_cm, line_cm):
    """1 near the two edges of a strip (grooves, grout), else 0. pos is 0..1 inside the strip."""
    d = np.minimum(pos, 1 - pos) * strip_w_cm
    return 1 - smooth(line_cm * 0.4, line_cm * 0.9, d)


def wood_grain(seed, along_v=True):
    s = dict(sx=1.0, sy=14.0) if along_v else dict(sx=14.0, sy=1.0)   # larger s? = longer streaks on that axis
    g = 0.65 * fnoise(seed, 1.3, 2, 400, **s) + 0.35 * fnoise(seed + 1, 1.0, 20, 500, **s)
    rings = 0.5 + 0.5 * np.sin((fnoise(seed + 2, 2.2, 1, 12, **s) * 38.0) * np.pi)
    return norm01(0.7 * g + 0.3 * rings)


# ---------------------------------------------------------------- walls and ceilings
h = 0.6 * fnoise(1, 1.0, 30, 160) + 0.4 * fnoise(2, 0.6, 120, 420)
W.save("paint", color((0.93, 0.93, 0.93), 0.95 + 0.07 * fnoise(3, 2.0, 1, 20)), h, 0.78 + 0.12 * fnoise(4, 1.5, 2, 60), 100, bump=0.35)

blob = smooth(0.52, 0.7, fnoise(5, 0.4, 28, 70))
h = norm01(blur(blob, 2.0) + 0.25 * fnoise(6, 0.5, 100, 400))
W.save("popcorn", color((0.90, 0.89, 0.84), 0.72 + 0.3 * h), h, 0.95, 60, bump=3.0)

idx, pos = bands(U, [12, 20, 15, 25, 18, 14, 18])
g = wood_grain(10)
tone = per_cell(idx, 11, 0.85, 1.1)
groove = line_mask(pos, 17.0, 0.9)
bc = mix((0.19, 0.105, 0.05), (0.42, 0.25, 0.12), g) * tone[..., None] * (1 - 0.75 * groove[..., None])
W.save("wood_panel", bc, norm01(0.25 * g + 1.0 * (1 - groove)), 0.5 + 0.2 * (1 - g) + 0.2 * groove, 122, bump=1.2)

g = wood_grain(14)
W.save("wood_plain", mix((0.16, 0.085, 0.04), (0.36, 0.2, 0.09), g), 0.3 * g, 0.42 + 0.25 * (1 - g), 90, bump=0.5)

for name, seed, base, stripe, motif_c, tile in (("wallpaper_hall", 20, (0.80, 0.74, 0.58), (0.74, 0.67, 0.49), (0.55, 0.47, 0.22), 60),
                                                ("wallpaper_bed", 24, (0.62, 0.72, 0.82), (0.56, 0.67, 0.79), (0.90, 0.88, 0.80), 48)):
    sidx, spos = bands(U, [1] * 8)
    st = (sidx % 2).astype(float) * smooth(0.0, 0.04, np.minimum(spos, 1 - spos))
    cu, cv = (U * 4) % 1.0, ((V * 4) + 0.5 * (np.floor(U * 4) % 2)) % 1.0
    r = np.sqrt((cu - 0.5) ** 2 + (cv - 0.5) ** 2); a = np.arctan2(cv - 0.5, cu - 0.5)
    petal = smooth(0.02, 0.0, r - (0.13 + 0.07 * np.cos(5 * a))) * (1 - smooth(0.035, 0.03, r) * 0.0)
    centre = smooth(0.045, 0.03, r)
    paper = 0.94 + 0.08 * fnoise(seed, 0.8, 60, 400)
    bc = mix(base, stripe, st)
    bc = bc * (1 - petal[..., None]) + color(motif_c) * petal[..., None]
    bc = bc * (1 - centre[..., None]) + color(tuple(0.6 * np.array(motif_c))) * centre[..., None]
    age = 0.9 + 0.12 * fnoise(seed + 1, 2.2, 1, 8)
    W.save(name, bc * (paper * age)[..., None], 0.5 * fnoise(seed + 2, 0.7, 80, 420) + 0.1 * petal, 0.8, tile, bump=0.25)

cu, cv = (U * 8) % 1.0, (V * 8) % 1.0
chk = 0.5 * (cu < 0.5) + 0.5 * (cv < 0.5)
bc = mix((0.86, 0.80, 0.52), (0.70, 0.62, 0.28), chk) * (0.93 + 0.1 * fnoise(30, 2.0, 1, 10))[..., None]
W.save("wallpaper_kitchen", bc, 0.5 * fnoise(31, 0.7, 80, 420), 0.72, 40, bump=0.2)

# ---------------------------------------------------------------- floors
sidx, spos = bands(V, [1] * 16)                                 # 16 strips of 7.5 cm across a 120 cm tile
off = per_cell(sidx, 40)
u2 = (U + off) % 1.0
jidx, jpos = bands(u2, [1, 1])                                  # two boards per strip length
g = wood_grain(41, along_v=False)
board_tone = per_cell(sidx * 2 + jidx, 42, 0.90, 1.07)
gap = np.maximum(line_mask(spos, 7.5, 0.22), line_mask(jpos, 60.0, 0.25))
bc = mix((0.33, 0.19, 0.08), (0.62, 0.42, 0.20), g) * board_tone[..., None] * (1 - 0.8 * gap[..., None])
scuff = fnoise(43, 1.8, 2, 40)
W.save("oak_floor", bc, norm01(0.2 * g + (1 - gap)), 0.38 + 0.25 * scuff + 0.3 * gap, 120, bump=0.6)

fib = norm01(0.5 * fnoise(50, 0.3, 90, 330, sx=3) + 0.5 * fnoise(51, 0.3, 90, 330, sy=3) + 0.5 * fnoise(52, 1.2, 6, 40))
hue = fnoise(53, 1.5, 3, 30)
bc = mix((0.30, 0.14, 0.03), (0.66, 0.40, 0.10), norm01(0.7 * fib + 0.3 * hue))
W.save("shag", bc, fib, 0.97, 50, bump=4.0)

pile = norm01(fnoise(55, 0.2, 150, 420) + 0.4 * fnoise(56, 1.6, 2, 20))
wear = smooth(0.35, 0.85, fnoise(57, 2.6, 1, 5))
bc = mix((0.27, 0.22, 0.17), (0.50, 0.43, 0.34), norm01(pile + 0.25 * wear))
W.save("carpet_worn", bc, pile * (1 - 0.5 * wear), 0.95, 50, bump=2.0)

cu, cv = (U * 2) % 1.0, (V * 2) % 1.0                           # 2x2 tiles of 30.5 cm
d = np.maximum(np.abs(cu - 0.5), np.abs(cv - 0.5))
ring = smooth(0.30, 0.31, d) * (1 - smooth(0.36, 0.37, d))
diamond = 1 - smooth(0.17, 0.18, np.abs(cu - 0.5) + np.abs(cv - 0.5))
corner = 1 - smooth(0.09, 0.10, np.sqrt((np.abs(cu - 0.5) - 0.5) ** 2 + (np.abs(cv - 0.5) - 0.5) ** 2))
seam = np.maximum(line_mask(cu, 30.5, 0.12), line_mask(cv, 30.5, 0.12))
bc = color((0.74, 0.62, 0.36))
for m, c in ((ring, (0.45, 0.27, 0.10)), (diamond, (0.52, 0.33, 0.12)), (corner, (0.83, 0.77, 0.58))):
    bc = bc * (1 - m[..., None]) + color(c) * m[..., None]
speck = 0.9 + 0.2 * fnoise(60, 0.3, 100, 400)
dirt = fnoise(61, 2.0, 1, 12)
bc = bc * (speck * (0.85 + 0.2 * dirt))[..., None] * (1 - 0.5 * seam[..., None])
W.save("linoleum", bc, norm01(0.15 * fnoise(62, 0.8, 40, 300) + (1 - seam)), 0.35 + 0.3 * fnoise(63, 1.6, 3, 80, sx=4) + 0.3 * seam, 61, bump=0.3)

cu, cv = (U * 4) % 1.0, (V * 4) % 1.0                           # 4x4 tiles of 11 cm
tidx = (np.floor(U * 4) + 4 * np.floor(V * 4)).astype(int)
grout = np.maximum(line_mask(cu, 11.0, 0.45), line_mask(cv, 11.0, 0.45))
tone = per_cell(tidx, 70, 0.93, 1.04)
bc = color((0.66, 0.80, 0.78)) * tone[..., None] * (0.97 + 0.05 * fnoise(71, 1.0, 20, 200))[..., None]
gcol = color((0.60, 0.58, 0.52), 0.75 + 0.3 * fnoise(72, 1.5, 4, 80))
bc = bc * (1 - grout[..., None]) + gcol * grout[..., None]
W.save("tile_bath", bc, norm01(1 - grout) * 0.9 + 0.1 * fnoise(73, 1.0, 10, 80), 0.16 + 0.75 * grout, 44, bump=1.0)

# ---------------------------------------------------------------- outside
ridx, rpos = bands(V, [1] * 16)
u2 = (U + 0.5 * (ridx % 2) / 6.0) % 1.0
bidx, bpos = bands(u2, [1] * 6)
mortar = np.maximum(line_mask(rpos, 7.5, 1.0), line_mask(bpos, 20.0, 1.0))
tone = per_cell(ridx * 6 + bidx, 80, 0.7, 1.15)
face = fnoise(81, 0.9, 20, 300)
bc = mix((0.30, 0.10, 0.06), (0.50, 0.21, 0.13), face) * tone[..., None]
bc = bc * (1 - mortar[..., None]) + color((0.55, 0.53, 0.49), 0.8 + 0.3 * face) * mortar[..., None]
W.save("brick", bc, norm01((1 - mortar) + 0.25 * face), 0.9, 120, bump=2.0)

lidx, lpos = bands(V, [1] * 5)
shadow = smooth(0.0, 0.06, lpos)
g = fnoise(85, 1.2, 4, 300, sy=10)
streak = fnoise(86, 1.5, 2, 60, sx=8)
bc = color((0.80, 0.78, 0.70)) * (0.55 + 0.45 * shadow)[..., None] * (0.9 + 0.1 * g - 0.08 * streak * (1 - lpos))[..., None]
W.save("siding", bc, norm01(lpos + 0.05 * g), 0.7, 100, bump=1.5)

ridx, rpos = bands(V, [1] * 8)
u2 = (U + 0.5 * (ridx % 2) / 4.0) % 1.0
tidx2, tpos = bands(u2, [1] * 4)
gran = fnoise(90, 0.2, 150, 420)
tone = per_cell(ridx * 4 + tidx2, 91, 0.75, 1.1)
gap = np.maximum(1 - smooth(0.0, 0.06, rpos), line_mask(tpos, 25.0, 0.5))
W.save("shingles", color((0.13, 0.115, 0.105), (0.7 + 0.5 * gran) * tone) * (1 - 0.7 * gap[..., None]), norm01(rpos + 0.2 * gran), 0.95, 110, bump=1.5)

n1 = fnoise(95, 1.4, 2, 300); pits = smooth(0.72, 0.8, fnoise(96, 0.3, 60, 200))
W.save("concrete", color((0.52, 0.51, 0.48), 0.75 + 0.35 * n1) * (1 - 0.4 * pits[..., None]), norm01(n1 * 0.4 + (1 - pits)), 0.88, 150, bump=0.8)
agg = fnoise(97, 0.2, 120, 420)
W.save("asphalt", color((0.085, 0.085, 0.09), 0.6 + 0.9 * agg), agg, 0.92, 100, bump=2.0)
gr = norm01(fnoise(98, 0.4, 80, 400, sy=3) + 0.8 * fnoise(99, 1.8, 2, 20))
W.save("grass", mix((0.05, 0.11, 0.02), (0.22, 0.34, 0.08), gr), gr, 0.95, 150, bump=3.0)

# ---------------------------------------------------------------- prop surfaces
flute = 0.5 + 0.5 * np.sin(V * 2 * np.pi * 72)
fibre = fnoise(100, 1.0, 10, 400, sy=6)
W.save("cardboard", color((0.56, 0.41, 0.25), 0.82 + 0.25 * fibre + 0.04 * flute), norm01(0.6 * fibre + 0.25 * flute), 0.86, 50, bump=0.5)
weave = 0.5 + 0.25 * np.sin(U * 2 * np.pi * 64) * np.sign(np.sin(V * 2 * np.pi * 64)) + 0.25 * np.sin(V * 2 * np.pi * 64)
W.save("fabric", color((0.9, 0.9, 0.9), 0.8 + 0.2 * norm01(weave) * (0.9 + 0.2 * fnoise(101, 1.5, 3, 60))), norm01(weave), 0.93, 20, bump=1.5)
W.save("plastic", color((0.9, 0.9, 0.9), 0.96 + 0.05 * fnoise(102, 1.5, 3, 40)), fnoise(103, 0.3, 120, 420), 0.42 + 0.2 * fnoise(104, 1.6, 2, 30), 20, bump=0.25)
W.save("metal", color((0.9, 0.9, 0.9), 0.9 + 0.1 * fnoise(105, 1.0, 4, 300, sy=20)), fnoise(106, 0.8, 8, 400, sy=20), 0.32 + 0.2 * fnoise(107, 1.4, 2, 300, sy=12), 20, bump=0.3, metallic=1.0)
W.save("grunge", color((1, 1, 1), smooth(0.25, 0.85, fnoise(108, 2.0, 1, 40))), fnoise(109, 1.5, 2, 80), fnoise(110, 1.8, 1, 60), 300, bump=0.0)
W.finish()
print("wrote", len(W.manifest), "texture sets to", W.out)
