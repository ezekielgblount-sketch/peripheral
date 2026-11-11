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
    im = age(im, fade=0.22, warm=(1.04, 1.0, 0.9), seed=seed)
    ImageDraw.Draw(im).text((612, 448), "7  4 '98", font=font(26, "bold"), fill=(255, 140, 30), anchor="rs")      # orange camera date stamp
    out = Image.new("RGB", (704, 544), (232, 226, 206)); out.paste(im, (32, 32))        # white print border
    out.save(os.path.join(OUT, name + ".png"))


def portrait(name, body, hair, bg, seed):
    W, H = 384 * SS, 480 * SS
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    r = random.Random(seed)                       # 90s school-photo laser backdrop
    for i in range(14):
        c = r.choice([(255, 60, 200), (60, 220, 255), (120, 90, 255), (255, 255, 255)])
        x0 = r.uniform(-0.2, 1.2) * W
        d.line([(x0, 0), (x0 + r.uniform(-0.9, 0.9) * W, H)], fill=tuple(int(v * 0.75) for v in c), width=int(r.uniform(4, 14)))
    person(d, W * 0.5, H * 2.25, H * 2.0, body, hair, child=True)
    im = age(im.resize((384, 480), Image.LANCZOS), fade=0.15, warm=(1.02, 1.0, 0.94), seed=seed)
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


def cereal(name, title, bg, bowl):
    im = Image.new("RGB", (384, 544), bg); d = ImageDraw.Draw(im); r = random.Random(len(title))
    d.polygon([(0, 150), (384, 90), (384, 200), (0, 250)], fill=(250, 220, 40))
    d.text((192, 172), title, font=font(54, "bold"), fill=(200, 30, 40), anchor="mm")
    d.ellipse([70, 330, 314, 500], fill=(240, 240, 235)); d.ellipse([90, 340, 294, 420], fill=(250, 250, 245))
    for _ in range(26):
        x, y = r.uniform(110, 270), r.uniform(350, 405); c = r.choice(bowl)
        d.ellipse([x - 12, y - 9, x + 12, y + 9], outline=c, width=6)
    d.text((192, 40), "NEW!  PRIZE INSIDE", font=font(26, "bold"), fill=(255, 255, 255), anchor="mm")
    age(im, fade=0.12, grain=3, blur=0.4, warm=(1.02, 1.0, 0.95)).save(os.path.join(OUT, name + ".png"))


def border(name, bg, kind):
    W, H = 768, 96
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im); r = random.Random(kind)
    d.rectangle([0, 0, W, 8], fill=(40, 80, 50) if kind == 1 else (110, 30, 40)); d.rectangle([0, H - 8, W, H], fill=(40, 80, 50) if kind == 1 else (110, 30, 40))
    for i in range(8):
        x = i * 96 + 48
        if kind == 1:                             # fruit: apples and pears with leaves
            d.ellipse([x - 20, 28, x + 12, 66], fill=(190, 40, 40)); d.ellipse([x + 6, 34, x + 30, 70], fill=(210, 190, 60))
            d.ellipse([x - 8, 18, x + 14, 30], fill=(50, 120, 50))
        else:                                     # hunter green ivy and burgundy flowers
            d.line([(x - 48, 48 + 14 * (-1) ** i), (x, 48), (x + 48, 48 - 14 * (-1) ** i)], fill=(40, 90, 55), width=5)
            d.ellipse([x - 14, 34, x + 14, 62], fill=(120, 30, 50)); d.ellipse([x - 5, 43, x + 5, 53], fill=(230, 200, 120))
            d.ellipse([x + 22, 30, x + 40, 44], fill=(40, 90, 55))
    im.filter(ImageFilter.GaussianBlur(0.5)).save(os.path.join(OUT, name + ".png"))


cereal("cereal_a", "RAINBOW RINGS", (40, 90, 200), [(230, 60, 60), (250, 200, 40), (60, 190, 90), (240, 120, 30)])
cereal("cereal_b", "CHOCO BLASTS", (150, 60, 160), [(90, 50, 30), (120, 70, 40)])
border("border_fruit", (240, 232, 205), 1); border("border_ivy", (236, 226, 200), 2)
def rug_oriental(name):
    W, H = 1024, 720
    im = Image.new("RGB", (W, H), (226, 214, 188)); d = ImageDraw.Draw(im); r = random.Random(12)
    for i, c in enumerate(((60, 50, 70), (150, 70, 50), (226, 214, 188), (70, 80, 100))):
        d.rectangle([i * 16, i * 16, W - i * 16, H - i * 16], outline=c, width=16)
    for _ in range(90):
        x, y = r.uniform(90, W - 90), r.uniform(90, H - 90); c = r.choice([(150, 70, 50), (70, 80, 100), (110, 120, 80), (180, 140, 90)])
        for i in range(6):
            a = i * 1.047
            d.ellipse([x + 16 * math.cos(a) - 9, y + 16 * math.sin(a) - 9, x + 16 * math.cos(a) + 9, y + 16 * math.sin(a) + 9], fill=c)
        d.line([(x, y), (x + r.uniform(-50, 50), y + r.uniform(-50, 50))], fill=(110, 120, 80), width=3)
    age(im, fade=0.18, grain=6, blur=0.8, warm=(1.02, 1.0, 0.94)).save(os.path.join(OUT, name + ".png"))


def landscape(name, seed):
    W, H = 640, 448
    im = Image.new("RGB", (W, H), (236, 232, 220)); d = ImageDraw.Draw(im); r = random.Random(seed)
    x0, y0, x1, y1 = 70, 60, W - 70, H - 60
    for y in range(y0, y1):
        f = (y - y0) / (y1 - y0)
        d.line([(x0, y), (x1, y)], fill=(int(150 + 60 * f), int(170 + 40 * f), int(200 - 10 * f)) if f < 0.55 else (int(120 - 40 * (f - 0.55)), int(140 - 30 * (f - 0.55)), int(90)))
    for _ in range(40):
        x = r.uniform(x0, x1); h = r.uniform(30, 90)
        d.polygon([(x, y0 + 190 - h), (x - h * 0.25, y0 + 190), (x + h * 0.25, y0 + 190)], fill=(50 + r.randint(0, 30), 70 + r.randint(0, 30), 60))
    d.rectangle([x0 + 300, y0 + 150, x0 + 370, y0 + 195], fill=(120, 40, 36)); d.polygon([(x0 + 292, y0 + 150), (x0 + 335, y0 + 120), (x0 + 378, y0 + 150)], fill=(60, 50, 50))
    d.rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6], outline=(120, 140, 170), width=4)
    age(im, fade=0.15, grain=4, blur=0.9, warm=(1.02, 1.0, 0.95), seed=seed).save(os.path.join(OUT, name + ".png"))


def chart_alphabet(name):
    im = Image.new("RGB", (512, 720), (246, 246, 240)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 511, 719], outline=(40, 70, 170), width=8)
    letters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    for i in range(26):
        x, y = 40 + (i % 4) * 118, 40 + (i // 4) * 96
        d.line([(x - 10, y + 62), (x + 100, y + 62)], fill=(120, 150, 220), width=2); d.line([(x - 10, y + 30), (x + 100, y + 30)], fill=(200, 210, 235), width=1)
        d.text((x, y), letters[i * 2:i * 2 + 2], font=font(56, "hand"), fill=(20, 20, 20))
    im.save(os.path.join(OUT, name + ".png"))


def chart_fractions(name):
    im = Image.new("RGB", (640, 384), (250, 250, 250)); d = ImageDraw.Draw(im)
    cols = [(230, 60, 140), (240, 130, 40), (240, 190, 40), (110, 190, 70), (60, 170, 90), (150, 70, 180), (110, 60, 160), (60, 90, 190), (40, 150, 220), (40, 180, 180)]
    for i, c in enumerate(cols):
        x, y = (i % 5) * 128, (i // 5) * 192
        d.rectangle([x + 4, y + 4, x + 124, y + 188], fill=c)
        d.ellipse([x + 24, y + 50, x + 104, y + 130], fill=tuple(min(255, v + 90) for v in c))
        d.pieslice([x + 24, y + 50, x + 104, y + 130], -90, -90 + 360 // (i + 1), fill=tuple(int(v * 0.6) for v in c))
        d.text((x + 64, y + 26), "1/%d" % (i + 1) if i else "1", font=font(26, "bold"), fill=(255, 255, 255), anchor="mm")
    im.save(os.path.join(OUT, name + ".png"))


def banner(name, text):
    im = Image.new("RGBA", (1024, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cols = [(90, 40, 90), (200, 150, 40), (40, 80, 110), (200, 150, 40), (160, 50, 40), (40, 80, 110), (90, 40, 90), (40, 80, 110)]
    n = len(text)
    for i, ch in enumerate(text):
        x = 110 + i * (800 / (n - 1)); y = 40 + 50 * math.sin(math.pi * i / (n - 1))
        d.text((x, y + 60), ch, font=font(120, "bold"), fill=cols[i % len(cols)] + (255,), anchor="mm")
    d.line([(20, 20)] + [(110 + i * (800 / (n - 1)), 30 + 50 * math.sin(math.pi * i / (n - 1))) for i in range(n)] + [(1004, 20)], fill=(150, 120, 80, 255), width=4)
    im.save(os.path.join(OUT, name + ".png"))


def note(name, lines, bg=(250, 240, 150), size=(384, 480), lined=True, fsize=40, ink=(30, 40, 110)):
    im = Image.new("RGB", size, bg); d = ImageDraw.Draw(im)
    if lined:
        for y in range(70, size[1], 46):
            d.line([(0, y), (size[0], y)], fill=tuple(int(v * 0.82) for v in bg), width=2)
    for i, t in enumerate(lines):
        d.text((26, 30 + i * 46), t, font=font(fsize, "hand"), fill=ink)
    im.filter(ImageFilter.GaussianBlur(0.4)).save(os.path.join(OUT, name + ".png"))


def calendar(name):
    im = Image.new("RGB", (512, 640), (246, 244, 236)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 512, 150], fill=(150, 70, 40)); d.text((256, 78), "NOVEMBER", font=font(70, "bold"), fill=(250, 240, 220), anchor="mm")
    for i in range(35):
        x, y = 16 + (i % 7) * 69, 170 + (i // 7) * 90
        d.rectangle([x, y, x + 66, y + 86], outline=(150, 150, 150), width=2)
        if i < 30:
            d.text((x + 8, y + 4), str(i + 1), font=font(24, "bold"), fill=(60, 60, 60))
        if i < 12:
            d.line([(x + 12, y + 20), (x + 56, y + 76)], fill=(170, 40, 40), width=4)            # days crossed off, then they stop
    x, y = 16 + (12 % 7) * 69, 170 + (12 // 7) * 90
    d.ellipse([x + 2, y + 2, x + 64, y + 84], outline=(30, 40, 150), width=5)
    d.text((16 + 4 * 69 + 4, 170 + 3 * 90 + 34), "Jack\nrecital", font=font(20, "hand"), fill=(30, 40, 150))
    im.save(os.path.join(OUT, name + ".png"))


def homework(name):
    im = Image.new("RGB", (384, 512), (248, 248, 244)); d = ImageDraw.Draw(im)
    d.text((20, 14), "Name:  Jack", font=font(30, "hand"), fill=(40, 40, 40))
    for i, t in enumerate(("7 x 6 = 42", "8 x 4 = 32", "9 x 7 = 61", "6 x 6 = 36", "12 x 3 =", "5 x 9 =")):
        d.text((40, 80 + i * 66), t, font=font(44, "hand"), fill=(50, 50, 50))
    d.ellipse([200, 196, 330, 270], outline=(200, 30, 30), width=4)
    im.save(os.path.join(OUT, name + ".png"))


note("note_grocery", ["milk", "eggs", "bread", "Jack's cereal", "batteries (D)", "candles?"])
note("note_mom", ["Back by 6.", "Dinner's in the", "oven - 350.", "Don't wait up", "   love, Mom"], bg=(250, 250, 244))
note("note_chores", ["CHORES", "Jack - trash  x", "Jack - piano  x", "Dad - gutters", "Mom - call Gram"], bg=(200, 230, 250))
note("note_numbers", ["Gram  555-0142", "Dr. Hale 555-0117", "school 555-0190", "PIZZA 555-0123"], bg=(250, 215, 220), fsize=32)
calendar("calendar_nov"); homework("homework")
note("magazine", ["", "HOME &", " GARDEN", "", "fall issue"], bg=(120, 150, 110), lined=False, fsize=58, ink=(250, 245, 230))
import math
rug_oriental("rug_oriental"); landscape("print_landscape_a", 1); landscape("print_landscape_b", 5)
chart_alphabet("chart_alphabet"); chart_fractions("chart_fractions"); banner("banner_thankful", "THANKFUL")
family("photo_family_a", True, 1); family("photo_family_b", False, 1)
portrait("photo_school", (60, 150, 150), (90, 60, 34), (24, 30, 90), 2)
portrait("photo_school_b", (150, 60, 140), (40, 30, 24), (30, 20, 70), 3)
poster_space("poster_space"); poster_shapes("poster_shapes"); kid_drawing("kid_drawing")
for n, t, s in (("label_kitchen", "KITCHEN", "dishes"), ("label_jack", "JACK'S ROOM", ""), ("label_living", "LIVING RM", ""),
                ("label_fragile", "FRAGILE", "this side up"), ("label_books", "BOOKS", ""), ("label_misc", "MISC", "attic?")):
    box_label(n, t, s)
rug("rug_braided"); clock("clock_face"); spines("book_spines_a", 1); spines("book_spines_b", 2)
vhs_label("vhs_xmas", "XMAS '89"); vhs_label("vhs_bday", "Jack 6th B-DAY"); vhs_label("vhs_blank", "")
print("prints:", len(os.listdir(OUT)))
