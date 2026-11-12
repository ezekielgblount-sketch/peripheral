#!/usr/bin/env python3
"""Third anomaly pass: the rider board that hangs under the SOLD sign ("WELCOME HOME"). Its blank twin needs no picture."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "SourceArt", "Prints")
p = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
f = ImageFont.truetype(p, 84) if os.path.exists(p) else ImageFont.load_default()
im = Image.new("RGB", (720, 140), (236, 234, 226)); d = ImageDraw.Draw(im)
d.rectangle([6, 6, 713, 133], outline=(24, 44, 84), width=5); d.text((360, 72), "WELCOME HOME", font=f, fill=(24, 44, 84), anchor="mm")
im.filter(ImageFilter.GaussianBlur(0.5)).save(os.path.join(OUT, "sign_rider.png"))
print("prints3 written")
