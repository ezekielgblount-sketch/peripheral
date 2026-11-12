#!/usr/bin/env python3
"""Playtest round 1 prints: the anomaly twins of existing prints, and the space border for Jack's room.
Loads gen_prints.py for its helpers (which also refreshes the prints it makes). Run: gen_prints2.py"""
import os, sys, random, importlib.util
from PIL import Image, ImageDraw, ImageFilter
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("gen_prints", os.path.join(here, "gen_prints.py"))
gp = importlib.util.module_from_spec(spec); spec.loader.exec_module(gp)
OUT = gp.OUT

# the family photo again, but everyone has their back to the camera
front = gp.person
def back(d, x, ground, h, body, hair, skin=(214, 172, 140), dress=False, child=False):
    front(d, x, ground, h, body, hair, skin, dress, child)
    r = h * (0.075 if not child else 0.1); top = ground - h
    d.ellipse([x - r * 1.08, top - r * 0.2, x + r * 1.08, top + r * 2.25], fill=hair)
gp.person = back
gp.family("photo_family_c", True, 1)
gp.person = front

gp.banner("banner_thankfu", "THANKFU ")                     # the last letter is gone from the string


def kid_drawing_b(name):
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
        d.ellipse([x - 13, 300 - h - 26, x + 13, 300 - h], outline=c, width=5)
    x, h, c = 60, 132, (34, 34, 38)                          # the extra one: taller than the rest, standing apart, in plain pencil
    wob([(x, 300), (x, 300 - h)], c, 4); wob([(x - 22, 300 - h * 0.62), (x + 22, 300 - h * 0.62)], c, 4)
    d.ellipse([x - 14, 300 - h - 28, x + 14, 300 - h], outline=c, width=4)
    d.text((30, 340), "my famly", font=gp.font(34, "hand"), fill=(60, 60, 60))
    gp.age(im, fade=0.15, grain=4, blur=0.4, warm=(1.02, 1.0, 0.92)).save(os.path.join(OUT, name + ".png"))


def height_marks_b(name):
    im = Image.new("RGBA", (96, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (y, t) in enumerate(((560, "'99"), (470, "'01"), (380, "'03"), (300, "'05"), (210, "'07"), (150, "'09"))):
        d.line([(6, y), (60, y)], fill=(40, 40, 50, 230), width=3); d.text((8, y - 30), "Jack " + t, font=gp.font(20, "hand"), fill=(40, 40, 60, 230))
    d.line([(6, 64), (66, 64)], fill=(20, 20, 26, 255), width=4); d.text((8, 32), "Jack", font=gp.font(22, "hand"), fill=(20, 20, 30, 255))
    im.save(os.path.join(OUT, name + ".png"))


def border_space(name):
    W, H = 768, 96
    im = Image.new("RGB", (W, H), (22, 30, 78)); d = ImageDraw.Draw(im); r = random.Random(12)
    d.rectangle([0, 0, W, 7], fill=(200, 60, 50)); d.rectangle([0, H - 7, W, H], fill=(200, 60, 50))
    for _ in range(70):
        x, y, s = r.uniform(0, W), r.uniform(12, H - 12), r.uniform(1, 2.6)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(250, 240, 180))
    for i in range(4):
        x = i * 192 + 50
        d.ellipse([x - 22, 26, x + 22, 70], fill=(230, 150, 60)); d.ellipse([x - 34, 42, x + 34, 54], outline=(240, 220, 150), width=4)      # ringed planet
        x2 = x + 96
        d.polygon([(x2 - 26, 60), (x2 + 10, 40), (x2 + 26, 26), (x2 + 14, 46), (x2 - 6, 66)], fill=(230, 230, 235))                          # rocket
        d.polygon([(x2 - 26, 60), (x2 - 40, 58), (x2 - 30, 70)], fill=(240, 120, 40)); d.ellipse([x2 + 4, 36, x2 + 14, 46], fill=(60, 160, 220))
    im.filter(ImageFilter.GaussianBlur(0.5)).save(os.path.join(OUT, name + ".png"))


kid_drawing_b("kid_drawing_b"); height_marks_b("height_marks_b"); border_space("border_space")
print("round 1 prints written")
