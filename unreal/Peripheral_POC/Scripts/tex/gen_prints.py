#!/usr/bin/env python3
"""Generates printed images (family photos with no faces, posters, labels, rug, clock face) into SourceArt/Prints."""
import os, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Prints"); os.makedirs(OUT, exist_ok=True)
SS = 3


def font(size, kind="marker"):
    paths = {"marker": ["/System/Library/Fonts/MarkerFelt.ttc", "/System/Library/Fonts/Supplemental/Chalkduster.ttf"],
             "bold": ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"],
             "hand": ["/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf", "/System/Library/Fonts/MarkerFelt.ttc"]}[kind]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def age(im, fade=0.35, warm=(1.06, 1.0, 0.82), grain=7, blur=0.8, seed=1):
    """Make a clean image look like an old print: soft, faded, yellowed, grainy."""
    im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im).astype(np.float32) / 255.0
    g = a.mean(-1, keepdims=True)
    a = g + (a - g) * (1 - fade * 0.8)
    a = a * (1 - fade * 0.35) + fade * 0.3
    a = a * np.array(warm)[None, None, :]
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    v = 1 - 0.25 * (((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2) * 2)
    a = a * v[..., None] + np.random.default_rng(seed).normal(0, grain / 255.0, a.shape)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def person(d, x, ground, h, body, hair, skin=(214, 172, 140), dress=False, child=False):
    """A standing figure with a smooth blank face."""
    hw = h * (0.115 if not child else 0.14)
    head_r = h * (0.075 if not child else 0.1)
    top = ground - h
    neck = top + head_r * 2
    if dress:
        d.polygon([(x - hw, neck + 4), (x + hw, neck + 4), (x + hw * 1.7, ground - h * 0.18), (x - hw * 1.7, ground - h * 0.18)], fill=body)
        d.rectangle([x - hw * 0.5, ground - h * 0.18, x - hw * 0.1, ground], fill=skin)
        d.rectangle([x + hw * 0.1, ground - h * 0.18, x + hw * 0.5, ground], fill=skin)
    else:
        d.rectangle([x - hw, neck + 4, x + hw, ground - h * 0.45], fill=body)
        legs = tuple(int(c * 0.55) for c in body)
        d.rectangle([x - hw, ground - h * 0.46, x - hw * 0.08, ground], fill=legs)
        d.rectangle([x + hw * 0.08, ground - h * 0.46, x + hw, ground], fill=legs)
    d.rectangle([x - hw * 1.35, neck + 6, x - hw, neck + h * 0.33], fill=body)          # arms
    d.rectangle([x + hw, neck + 6, x + hw * 1.35, neck + h * 0.33], fill=body)
    d.ellipse([x - head_r, top, x + head_r, top + head_r * 2.2], fill=skin)             # head: no features
    d.pieslice([x - head_r * 1.08, top - head_r * 0.25, x + head_r * 1.08, top + head_r * 1.9], 180, 360, fill=hair)
    if dress:
        d.rectangle([x - head_r * 1.08, top + head_r * 0.8, x - head_r * 0.7, top + head_r * 2.4], fill=hair)
        d.rectangle([x + head_r * 0.7, top + head_r * 0.8, x + head_r * 1.08, top + head_r * 2.4], fill=hair)


def family(name, with_child=True, seed=1):
    W, H = 640 * SS, 480 * SS
    im = Image.new("RGB", (W, H), (150, 185, 215))
    d = ImageDraw.Draw(im)
    d.rectangle([0, H * 0.62, W, H], fill=(86, 128, 60))                                # lawn
    d.rectangle([W * 0.06, H * 0.2, W * 0.94, H * 0.66], fill=(150, 78, 58))            # brick house behind them
    d.rectangle([W * 0.06, H * 0.06, W * 0.94, H * 0.3], fill=(226, 222, 208))
    d.polygon([(W * 0.0, H * 0.08), (W * 0.5, -H * 0.1), (W * 1.0, H * 0.08)], fill=(92, 78, 70))
    d.rectangle([W * 0.62, H * 0.34, W * 0.82, H * 0.56], fill=(60, 70, 80))
    d.rectangle([W * 0.2, H * 0.3, W * 0.32, H * 0.66], fill=(96, 30, 26))
    g = H * 0.93
    person(d, W * 0.36, g, H * 0.62, (92, 70, 48), (60, 42, 30))
    person(d, W * 0.60, g, H * 0.56, (190, 120, 60), (120, 84, 40), dress=True)
    if with_child:
        person(d, W * 0.48, g, H * 0.36, (170, 40, 40), (90, 60, 34), child=True)
    im = im.resize((640, 480), Image.LANCZOS)
    im = age(im, seed=seed)
    out = Image.new("RGB", (704, 544), (232, 226, 206)); out.paste(im, (32, 32))        # white print border
    out.save(os.path.join(OUT, name + ".png"))


def portrait(name, body, hair, bg, seed):
    W, H = 384 * SS, 480 * SS
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    for i in range(40):
        d.ellipse([W * 0.5 - W * (0.9 - i * 0.02), H * 0.4 - W * (0.9 - i * 0.02), W * 0.5 + W * (0.9 - i * 0.02), H * 0.4 + W * (0.9 - i * 0.02)],
                  fill=tuple(min(255, int(c * (0.8 + i * 0.01))) for c in bg))
    person(d, W * 0.5, H * 2.25, H * 2.0, body, hair, child=True)
    im = age(im.resize((384, 480), Image.LANCZOS), seed=seed)
    out = Image.new("RGB", (416, 512), (232, 226, 206)); out.paste(im, (16, 16)); out.save(os.path.join(OUT, name + ".png"))


def poster_space(name):
    W, H = 512, 720
    a = np.zeros((H, W, 3), np.float32)
    yy = np.linspace(0, 1, H)[:, None]
    a[:] = np.array([0.03, 0.04, 0.14])[None, None, :] * (1 - yy[..., None]) + np.array([0.35, 0.12, 0.3])[None, None, :] * yy[..., None]
    rng = np.random.default_rng(4)
    for _ in range(260):
        a[rng.integers(0, int(H * 0.8)), rng.integers(0, W)] = rng.uniform(0.6, 1.0)
    im = Image.fromarray((a * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    d.ellipse([300, 60, 470, 230], fill=(214, 200, 170)); d.ellipse([330, 90, 370, 130], fill=(190, 176, 150)); d.ellipse([400, 150, 440, 190], fill=(190, 176, 150))
    d.polygon([(256, 250), (300, 420), (300, 560), (212, 560), (212, 420)], fill=(230, 230, 225))    # rocket
    d.polygon([(212, 500), (160, 590), (212, 570)], fill=(190, 40, 40)); d.polygon([(300, 500), (352, 590), (300, 570)], fill=(190, 40, 40))
    d.ellipse([236, 380, 276, 420], fill=(60, 110, 170))
    d.polygon([(222, 560), (290, 560), (256, 690)], fill=(250, 170, 40))
    d.text((256, 26), "TO THE STARS", font=font(44, "bold"), fill=(245, 235, 200), anchor="mt")
    age(im, fade=0.25, grain=5, blur=0.5).save(os.path.join(OUT, name + ".png"))


def poster_shapes(name):
    W, H = 512, 720
    im = Image.new("RGB", (W, H), (236, 222, 190)); d = ImageDraw.Draw(im); r = random.Random(9)
    cols = [(230, 80, 110), (40, 170, 170), (250, 200, 50), (60, 60, 150), (20, 20, 20)]
    for _ in range(26):
        x, y, s, c = r.randint(20, W - 20), r.randint(90, H - 20), r.randint(18, 70), r.choice(cols)
        k = r.randint(0, 3)
        if k == 0: d.ellipse([x - s, y - s, x + s, y + s], fill=c)
        elif k == 1: d.polygon([(x, y - s), (x + s, y + s), (x - s, y + s)], fill=c)
        elif k == 2: d.rectangle([x - s, y - s * 0.4, x + s, y + s * 0.4], fill=c)
        else:
            pts = [(x + i * 12, y + (10 if i % 2 else -10)) for i in range(-4, 5)]
            d.line(pts, fill=c, width=6)
    d.text((W / 2, 18), "RADICAL!", font=font(60, "bold"), fill=(20, 20, 20), anchor="mt")
    age(im, fade=0.3, grain=5, blur=0.5).save(os.path.join(OUT, name + ".png"))


def kid_drawing(name):
    W, H = 512, 400
    im = Image.new("RGB", (W, H), (238, 234, 222)); d = ImageDraw.Draw(im); r = random.Random(3)
    def wob(pts, col, w=5):
        d.line([(x + r.uniform(-3, 3), y + r.uniform(-3, 3)) for x, y in pts], fill=col, width=w, joint="curve")
    wob([(120, 300), (120, 170), (300, 170), (300, 300), (120, 300)], (170, 60, 40))
    wob([(105, 172), (210, 90), (315, 172)], (90, 60, 40))
    wob([(190, 300), (190, 230), (230, 230), (230, 300)], (60, 60, 60))
    for x in range(0, W, 14):
        wob([(x, 310 + r.uniform(-4, 4)), (x + 8, 300 + r.uniform(-6, 2))], (50, 150, 60), 4)
    d.ellipse([400, 30, 470, 100], outline=(240, 190, 30), width=7)
    for i, (x, h, c) in enumerate(((350, 90, (50, 70, 160)), (400, 80, (200, 60, 110)), (440, 50, (220, 40, 40)))):
        wob([(x, 300), (x, 300 - h)], c); wob([(x - 16, 300 - h * 0.6), (x + 16, 300 - h * 0.6)], c)
        d.ellipse([x - 13, 300 - h - 26, x + 13, 300 - h], outline=c, width=5)                # blank faces
    d.text((30, 340), "my famly", font=font(34, "hand"), fill=(60, 60, 60))
    age(im, fade=0.15, grain=4, blur=0.4, warm=(1.02, 1.0, 0.92)).save(os.path.join(OUT, name + ".png"))


def box_label(name, text, sub=""):
    W, H = 512, 256
    rng = np.random.default_rng(len(text))
    base = np.ones((H, W, 3)) * np.array([0.62, 0.47, 0.30])[None, None, :] * (0.92 + 0.12 * rng.random((H, 1, 1))) * (0.96 + 0.06 * rng.random((H, W, 1)))
    im = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    d.text((W / 2, H * 0.42), text, font=font(92 if len(text) < 9 else 66), fill=(22, 20, 26), anchor="mm")
    if sub:
        d.text((W / 2, H * 0.82), sub, font=font(40, "hand"), fill=(30, 26, 30), anchor="mm")
    im.filter(ImageFilter.GaussianBlur(0.6)).save(os.path.join(OUT, name + ".png"))


def rug(name):
    W, H = 768, 512
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    cols = np.array([[0.36, 0.12, 0.08], [0.55, 0.42, 0.25], [0.18, 0.2, 0.26], [0.5, 0.3, 0.12], [0.3, 0.32, 0.2], [0.62, 0.52, 0.36]])
    band = (rr * 22).astype(int)
    rng = np.random.default_rng(5)
    order = rng.integers(0, len(cols), 64)
    a = cols[order[np.clip(band, 0, 63)]] * (0.85 + 0.3 * rng.random((H, W, 1))) * (0.9 + 0.1 * np.sin(rr * 22 * 2 * np.pi))[..., None]
    alpha = (rr <= 0.985).astype(np.float32)
    im = Image.fromarray((np.clip(np.dstack([a, alpha]), 0, 1) * 255).astype(np.uint8), "RGBA")
    im.save(os.path.join(OUT, name + ".png"))


def clock(name):
    S = 512
    im = Image.new("RGB", (S, S), (236, 230, 212)); d = ImageDraw.Draw(im)
    import math
    for i in range(60):
        a = math.radians(i * 6); r0 = 226 if i % 5 else 210
        d.line([(S / 2 + math.sin(a) * r0, S / 2 - math.cos(a) * r0), (S / 2 + math.sin(a) * 238, S / 2 - math.cos(a) * 238)], fill=(30, 30, 30), width=3 if i % 5 else 6)
    for n in range(1, 13):
        a = math.radians(n * 30)
        d.text((S / 2 + math.sin(a) * 178, S / 2 - math.cos(a) * 178), str(n), font=font(46, "bold"), fill=(30, 30, 30), anchor="mm")
    age(im, fade=0.1, grain=3, blur=0.4, warm=(1.03, 1.0, 0.9)).save(os.path.join(OUT, name + ".png"))


def spines(name, seed):
    W, H = 768, 256
    im = Image.new("RGB", (W, H), (20, 16, 12)); d = ImageDraw.Draw(im); r = random.Random(seed); x = 0
    while x < W:
        w = r.randint(18, 44); h = r.randint(int(H * 0.72), H - 4)
        c = tuple(int(v * r.uniform(0.5, 1.0)) for v in r.choice([(150, 40, 36), (40, 70, 110), (60, 100, 60), (170, 140, 80), (90, 60, 40), (200, 190, 170), (40, 40, 44)]))
        d.rectangle([x, H - h, x + w - 2, H], fill=c)
        d.rectangle([x + 3, H - h + 14, x + w - 5, H - h + 20], fill=tuple(min(255, v + 70) for v in c))
        d.rectangle([x + 3, H - 40, x + w - 5, H - 34], fill=tuple(min(255, v + 70) for v in c))
        x += w
    age(im, fade=0.2, grain=4, blur=0.5).save(os.path.join(OUT, name + ".png"))


def vhs_label(name, text):
    im = Image.new("RGB", (384, 96), (232, 228, 214)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 383, 14], fill=(170, 40, 40)); d.line([(10, 78), (374, 78)], fill=(150, 150, 150))
    d.text((16, 22), text, font=font(40, "hand"), fill=(30, 30, 80))
    im.save(os.path.join(OUT, name + ".png"))


family("photo_family_a", True, 1); family("photo_family_b", False, 1)
portrait("photo_school", (60, 90, 150), (90, 60, 34), (110, 140, 170), 2)
portrait("photo_school_b", (150, 120, 60), (40, 30, 24), (150, 120, 110), 3)
poster_space("poster_space"); poster_shapes("poster_shapes"); kid_drawing("kid_drawing")
for n, t, s in (("label_kitchen", "KITCHEN", "dishes"), ("label_jack", "JACK'S ROOM", ""), ("label_living", "LIVING RM", ""),
                ("label_fragile", "FRAGILE", "this side up"), ("label_books", "BOOKS", ""), ("label_misc", "MISC", "attic?")):
    box_label(n, t, s)
rug("rug_braided"); clock("clock_face"); spines("book_spines_a", 1); spines("book_spines_b", 2)
vhs_label("vhs_xmas", "XMAS '89"); vhs_label("vhs_bday", "Jack 6th B-DAY"); vhs_label("vhs_blank", "")
print("prints:", len(os.listdir(OUT)))
