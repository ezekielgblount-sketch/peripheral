#!/usr/bin/env python3
"""More printed images into SourceArt/Prints: family snapshots for the walls, fridge and albums (nobody's face is shown:
people are seen from behind, far away or cropped), the portrait that turns its heads away, and the SOLD sign with and without its smile.
Stand-alone (does not import gen_prints, which redraws everything when loaded)."""
import os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Prints"); os.makedirs(OUT, exist_ok=True)
SS = 3
SKIN = (214, 172, 140)


def font(size, bold=True):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else []) + ["/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def age(im, fade=0.25, warm=(1.05, 1.0, 0.86), grain=8, blur=0.9, seed=1):
    im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im).astype(np.float32) / 255.0
    g = a.mean(-1, keepdims=True)
    a = g + (a - g) * (1 - fade * 0.8)
    a = (a * (1 - fade * 0.35) + fade * 0.3) * np.array(warm)[None, None, :]
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    v = 1 - 0.3 * (((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2) * 2)
    a = a * v[..., None] + np.random.default_rng(seed).normal(0, grain / 255.0, a.shape)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def back(d, x, ground, h, body, hair, legs=None, child=False, dress=False):
    """Someone seen from behind: the head is all hair."""
    hw = h * (0.13 if child else 0.115); hr = h * (0.1 if child else 0.075); top = ground - h; neck = top + hr * 2
    legs = legs or tuple(int(c * 0.5) for c in body)
    if dress:
        d.polygon([(x - hw, neck + 4), (x + hw, neck + 4), (x + hw * 1.7, ground - h * 0.2), (x - hw * 1.7, ground - h * 0.2)], fill=body)
        d.rectangle([x - hw * 0.5, ground - h * 0.2, x - hw * 0.1, ground], fill=SKIN); d.rectangle([x + hw * 0.1, ground - h * 0.2, x + hw * 0.5, ground], fill=SKIN)
    else:
        d.rectangle([x - hw, neck + 4, x + hw, ground - h * 0.45], fill=body)
        d.rectangle([x - hw, ground - h * 0.46, x - hw * 0.08, ground], fill=legs); d.rectangle([x + hw * 0.08, ground - h * 0.46, x + hw, ground], fill=legs)
    d.rectangle([x - hw * 1.35, neck + 6, x - hw, neck + h * 0.33], fill=body); d.rectangle([x + hw, neck + 6, x + hw * 1.35, neck + h * 0.33], fill=body)
    d.ellipse([x - hr * 1.05, top - hr * 0.2, x + hr * 1.05, top + hr * 2.2], fill=hair)
    if dress:
        d.rectangle([x - hr * 1.05, top + hr, x + hr * 1.05, top + hr * 3.0], fill=hair)


def snapshot(name, draw, stamp, size=(480, 360), seed=1, res=4, fade=0.25):
    """A drugstore print: drawn large, aged, shrunk to a low resolution, date-stamped, white border."""
    W, H = size[0] * SS, size[1] * SS
    im = Image.new("RGB", (W, H), (150, 185, 215)); draw(ImageDraw.Draw(im), W, H, random.Random(seed))
    im = age(im.resize(size, Image.LANCZOS), fade=fade, seed=seed)
    im = im.resize((size[0] // res, size[1] // res), Image.BILINEAR).resize(size, Image.BILINEAR)
    if stamp:
        ImageDraw.Draw(im).text((size[0] - 14, size[1] - 12), stamp, font=font(20), fill=(255, 140, 30), anchor="rs")
    out = Image.new("RGB", (size[0] + 48, size[1] + 48), (232, 226, 206)); out.paste(im, (24, 24)); out.save(os.path.join(OUT, name + ".png"))


def birthday(d, W, H, r):
    d.rectangle([0, 0, W, H], fill=(96, 70, 52)); d.rectangle([0, H * 0.62, W, H], fill=(150, 110, 70))            # dim dining room, table
    d.rectangle([W * 0.1, H * 0.08, W * 0.36, H * 0.4], fill=(40, 46, 70))                                             # dark window
    for i in range(7):
        d.polygon([(W * (0.1 + i * 0.12), H * 0.02), (W * (0.16 + i * 0.12), H * 0.02), (W * (0.13 + i * 0.12), H * 0.1)], fill=r.choice([(200, 60, 60), (60, 120, 200), (230, 200, 60)]))
    d.rectangle([W * 0.36, H * 0.5, W * 0.64, H * 0.66], fill=(240, 232, 220)); d.rectangle([W * 0.36, H * 0.5, W * 0.64, H * 0.54], fill=(230, 150, 170))
    for i in range(6):
        x = W * (0.4 + i * 0.04)
        d.rectangle([x - 4, H * 0.42, x + 4, H * 0.5], fill=(250, 250, 240)); d.ellipse([x - 9, H * 0.37, x + 9, H * 0.425], fill=(255, 220, 120))
    back(d, W * 0.5, H * 1.25, H * 0.62, (170, 40, 40), (90, 60, 34), child=True)
    back(d, W * 0.16, H * 1.3, H * 0.95, (92, 70, 48), (60, 42, 30)); back(d, W * 0.86, H * 1.3, H * 0.9, (190, 120, 60), (120, 84, 40), dress=True)


def bike(d, W, H, r):
    d.rectangle([0, H * 0.45, W, H], fill=(128, 126, 120)); d.rectangle([0, H * 0.3, W, H * 0.46], fill=(86, 128, 60))   # street, far lawns
    for i in range(4):
        x = W * (0.05 + i * 0.27); d.rectangle([x, H * 0.16, x + W * 0.18, H * 0.34], fill=r.choice([(150, 78, 58), (200, 190, 160), (120, 130, 140)]))
        d.polygon([(x - 10, H * 0.16), (x + W * 0.09, H * 0.06), (x + W * 0.18 + 10, H * 0.16)], fill=(80, 70, 66))
    x, g = W * 0.56, H * 0.84
    for cx in (x - W * 0.07, x + W * 0.07):
        d.ellipse([cx - H * 0.11, g - H * 0.22, cx + H * 0.11, g], outline=(30, 30, 30), width=10)
    d.line([(x - W * 0.07, g - H * 0.11), (x, g - H * 0.26), (x + W * 0.07, g - H * 0.11)], fill=(190, 40, 40), width=12)
    back(d, x, g - H * 0.1, H * 0.42, (60, 110, 190), (90, 60, 34), child=True)


def xmas(d, W, H, r):
    d.rectangle([0, 0, W, H], fill=(110, 84, 64)); d.rectangle([0, H * 0.74, W, H], fill=(120, 60, 50))
    for i in range(5):
        y = H * (0.1 + i * 0.13); w = W * (0.07 + i * 0.045)
        d.polygon([(W * 0.42, y), (W * 0.42 - w, y + H * 0.17), (W * 0.42 + w, y + H * 0.17)], fill=(30, 84, 44))
    for i in range(38):
        x = W * 0.42 + r.uniform(-0.2, 0.2) * W; y = H * r.uniform(0.2, 0.74)
        if abs(x - W * 0.42) < (y / H - 0.08) * W * 0.36:
            d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=r.choice([(250, 60, 60), (250, 220, 80), (90, 150, 250), (250, 250, 250)]))
    for (x, c) in ((0.2, (200, 50, 50)), (0.62, (60, 110, 190)), (0.72, (220, 190, 60))):
        d.rectangle([W * x, H * 0.72, W * (x + 0.09), H * 0.84], fill=c)
    back(d, W * 0.8, H * 1.02, H * 0.5, (40, 120, 80), (90, 60, 34), child=True)


def dock(d, W, H, r):
    d.rectangle([0, 0, W, H * 0.4], fill=(170, 196, 216)); d.rectangle([0, H * 0.34, W, H * 0.44], fill=(50, 84, 60))
    d.rectangle([0, H * 0.44, W, H], fill=(70, 110, 130)); d.polygon([(W * 0.36, H), (W * 0.64, H), (W * 0.56, H * 0.56), (W * 0.44, H * 0.56)], fill=(130, 104, 76))
    back(d, W * 0.44, H * 0.72, H * 0.4, (92, 70, 48), (60, 42, 30)); back(d, W * 0.55, H * 0.72, H * 0.24, (170, 40, 40), (90, 60, 34), child=True)
    d.line([(W * 0.4, H * 0.5), (W * 0.2, H * 0.3)], fill=(40, 30, 20), width=6)


def beach(d, W, H, r):
    d.rectangle([0, 0, W, H * 0.42], fill=(160, 200, 226)); d.rectangle([0, H * 0.42, W, H * 0.6], fill=(60, 120, 150)); d.rectangle([0, H * 0.6, W, H], fill=(216, 196, 150))
    back(d, W * 0.3, H * 0.9, H * 0.48, (190, 120, 60), (120, 84, 40), dress=True); back(d, W * 0.42, H * 0.92, H * 0.3, (230, 200, 60), (90, 60, 34), child=True)
    d.pieslice([W * 0.62, H * 0.5, W * 0.9, H * 0.86], 180, 360, fill=(220, 60, 60)); d.line([(W * 0.76, H * 0.68), (W * 0.76, H * 0.94)], fill=(240, 240, 240), width=8)


def driveway(d, W, H, r):
    d.rectangle([0, H * 0.56, W, H], fill=(150, 148, 140)); d.rectangle([0, H * 0.18, W, H * 0.58], fill=(150, 78, 58)); d.rectangle([0, 0, W, H * 0.2], fill=(226, 222, 208))
    d.rectangle([W * 0.1, H * 0.26, W * 0.62, H * 0.58], fill=(226, 222, 212))                                         # garage door
    d.rounded_rectangle([W * 0.3, H * 0.52, W * 0.88, H * 0.78], 40, fill=(150, 152, 158)); d.rounded_rectangle([W * 0.4, H * 0.4, W * 0.76, H * 0.56], 30, fill=(96, 110, 122))
    for cx in (0.4, 0.78):
        d.ellipse([W * cx - H * 0.07, H * 0.7, W * cx + H * 0.07, H * 0.84], fill=(26, 26, 26))
    back(d, W * 0.16, H * 0.96, H * 0.62, (92, 70, 48), (60, 42, 30))


def baby(d, W, H, r):
    d.rectangle([0, 0, W, H], fill=(170, 150, 120)); d.rounded_rectangle([W * 0.1, H * 0.3, W * 0.9, H * 0.95], 60, fill=(120, 70, 60))   # armchair
    d.ellipse([W * 0.3, H * 0.42, W * 0.7, H * 0.8], fill=(236, 226, 150)); d.ellipse([W * 0.42, H * 0.36, W * 0.58, H * 0.5], fill=(236, 226, 150))  # a blanket bundle
    d.rectangle([W * 0.2, H * 0.5, W * 0.34, H * 0.7], fill=(190, 120, 60)); d.rectangle([W * 0.66, H * 0.5, W * 0.8, H * 0.7], fill=(190, 120, 60))  # arms holding it


def yard(d, W, H, r):
    d.rectangle([0, H * 0.4, W, H], fill=(86, 128, 60)); d.rectangle([0, H * 0.22, W, H * 0.42], fill=(120, 96, 70))    # fence
    for i in range(24):
        d.line([(W * i / 24, H * 0.22), (W * i / 24, H * 0.42)], fill=(90, 70, 50), width=4)
    d.ellipse([W * 0.5, H * 0.6, W * 0.9, H * 0.76], fill=(110, 170, 210))                                             # paddling pool
    back(d, W * 0.3, H * 0.86, H * 0.34, (230, 200, 60), (90, 60, 34), child=True)
    d.line([(W * 0.05, H * 0.5), (W * 0.2, H * 0.62), (W * 0.36, H * 0.5)], fill=(240, 240, 240), width=5)                # sprinkler arc


for n, f, st, s in (("photo_bday", birthday, "3 9 '02", 11), ("photo_bike", bike, "5 18 '03", 12), ("photo_xmas", xmas, "12 25 '01", 13),
                    ("photo_dock", dock, "7 21 '04", 14), ("photo_beach", beach, "8 2 '00", 15), ("photo_driveway", driveway, "4 6 '99", 16),
                    ("photo_baby", baby, "10 30 '96", 17), ("photo_yard", yard, "6 30 '02", 18)):
    snapshot(n, f, st, seed=s)


def portrait_turned(d, W, H, r):
    bg = (120, 130, 150); d.rectangle([0, 0, W, H], fill=bg)
    for i in range(30):
        k = 0.8 - i * 0.02
        d.ellipse([W * 0.5 - W * k, H * 0.45 - W * k, W * 0.5 + W * k, H * 0.45 + W * k], fill=tuple(min(255, int(c * (0.8 + i * 0.012))) for c in bg))
    navy = (40, 50, 90)
    back(d, W * 0.3, H * 1.05, H * 0.92, navy, (60, 42, 30), legs=navy); back(d, W * 0.52, H * 1.05, H * 0.86, navy, (120, 84, 40), dress=True)
    back(d, W * 0.72, H * 1.05, H * 0.6, navy, (90, 60, 34), child=True, legs=navy)


snapshot("photo_portrait_turned", portrait_turned, "11 2 '03", size=(480, 384), seed=1, fade=0.2)
im = Image.open(os.path.join(OUT, "photo_portrait_turned.png")).crop((24, 24, 504, 408)); im.save(os.path.join(OUT, "photo_portrait_turned.png"))   # same size as the one it replaces


def sold(name, smile):
    W, H = 600, 440
    im = Image.new("RGB", (W, H), (236, 234, 226)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 120], fill=(150, 30, 34)); d.text((W / 2, 62), "SOLD", font=font(104), fill=(250, 246, 236), anchor="mm")
    d.text((240, 190), "HALE & VOSS", font=font(50), fill=(24, 44, 84)); d.text((240, 250), "REALTY", font=font(50), fill=(24, 44, 84))
    d.text((240, 330), "555-0164", font=font(44), fill=(60, 60, 60)); d.text((240, 388), "Your home is our home.", font=font(22, False), fill=(90, 90, 90))
    d.ellipse([40, 160, 200, 400], fill=(60, 80, 120)); d.ellipse([78, 190, 162, 300], fill=SKIN); d.pieslice([74, 180, 166, 270], 180, 360, fill=(60, 42, 30))
    d.polygon([(52, 400), (70, 320), (170, 320), (188, 400)], fill=(30, 34, 44))
    if smile:
        d.arc([98, 236, 142, 282], 20, 160, fill=(120, 50, 40), width=6)
    age(im, fade=0.12, warm=(1.02, 1.0, 0.95), grain=4, blur=0.5, seed=4).save(os.path.join(OUT, name + ".png"))


sold("sign_sold_a", True); sold("sign_sold_b", False)
print("prints2 written")
