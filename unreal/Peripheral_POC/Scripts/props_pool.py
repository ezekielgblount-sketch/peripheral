"""Nostalgia prop pool: small things that make the house read as lived in for decades. No real brands."""
import math, random, unreal
import meshkit as K
from props_furniture import prop, legs, frame, sofa


@prop
def candy_dish():
    k = K.Kit(); r = random.Random(1)
    k.revolve("glass", [(0.1, 0), (5, 0), (2, 3), (8, 7), (8.4, 9)], 14)
    for i in range(9):
        k.sphere(r.choice(["plastic_red", "plastic_yellow", "plastic_green", "enamel"]), r.uniform(-4, 4), r.uniform(-4, 4), 8 + r.uniform(0, 1.5), 1.3, 4)
    return k


@prop
def remote_ziplock():
    k = K.Kit(); k.soft("plastic_black", -9, -2.5, 0.2, 9, 2.5, 2.2, 3, 2); k.soft("plastic_clear", -12, -5, 0, 12, 5, 2.8, 3, 2); return k


@prop
def fake_plant():
    k = K.Kit(); r = random.Random(4)
    k.revolve("copper", [(0.1, 0), (9, 0), (12, 18), (11, 20)], 14)
    for i in range(14):
        a, l = i * 0.9, r.uniform(26, 50)
        k.tube("leaf", (0, 0, 18), (math.cos(a) * l * 0.5, math.sin(a) * l * 0.5, 18 + l), 0.5, 4)
        k.sphere("leaf", math.cos(a) * l * 0.5, math.sin(a) * l * 0.5, 18 + l, 6, 4, sz=0.4)
    return k


@prop
def fall_stems():
    k = K.Kit(); r = random.Random(6)
    k.revolve("copper", [(0.1, 0), (8, 0), (10, 22), (7, 26)], 14)
    for i in range(12):
        a, l = i * 1.1, r.uniform(30, 55)
        p = (math.cos(a) * l * 0.35, math.sin(a) * l * 0.35, 24 + l)
        k.tube("bark", (0, 0, 22), p, 0.35, 4); k.sphere("pumpkin" if i % 2 else "plastic_yellow", p[0], p[1], p[2], 2.6, 4)
    return k


@prop
def jar_candle():
    k = K.Kit(); k.cyl("glass", 0, 0, 0, 5, 11, 14); k.cyl("fabric_red", 0, 0, 0.5, 4.5, 7, 14); k.cyl("brass", 0, 0, 11, 5.2, 2, 14); return k


@prop
def frame_portrait():
    return frame("photo_portrait_matching", 50, 40, "brass")


@prop
def cookie_tin():
    k = K.Kit(); k.cyl("plastic_blue", 0, 0, 0, 10, 7, 20); k.cyl("brass", 0, 0, 7, 10.3, 1.2, 20); return k


@prop
def popcorn_tin():
    k = K.Kit(); k.cyl("plastic_red", 0, 0, 0, 12, 24, 20); k.cyl("enamel", 0, 0, 8, 12.1, 8, 20); k.cyl("plastic_red", 0, 0, 24, 12.4, 1.5, 20); return k


@prop
def fruit_bowl():
    k = K.Kit()
    k.revolve("oak", [(0.1, 0), (7, 0), (15, 7), (15.6, 8)], 16)
    for (x, y, c) in ((0, 0, "plastic_red"), (7, 3, "plastic_yellow"), (-6, 4, "plastic_green"), (2, -7, "pumpkin"), (-5, -5, "plastic_red")):
        k.sphere(c, x, y, 9, 4.2, 5)
    return k


@prop
def rooster():
    k = K.Kit()
    k.sphere("enamel", 0, 0, 9, 7, 6, sx=1.3); k.sphere("enamel", 7, 0, 17, 4, 5); k.cone("plastic_red", 8, 0, 20, 2.5, 0.5, 4, 6)
    k.cone("plastic_yellow", 11, 0, 16, 1.2, 0.2, 3, 6, pitch=90); k.obox("plastic_blue", -9, 0, 14, 10, 1.5, 9, pitch=40); k.cyl("plastic_yellow", 0, 0, 0, 3, 3, 8)
    return k


@prop
def mugs():
    k = K.Kit()
    for i, c in enumerate(("plastic_blue", "enamel", "plastic_red", "plastic_green", "plastic_yellow")):
        x, y = (i % 3) * 10, (i // 3) * 10
        k.cyl(c, x, y, 0, 4, 9.5, 12); k.torus(c, x, y + 5, 5, 2.6, 0.6, roll=90)
    return k


@prop
def key_bowl():
    k = K.Kit(); r = random.Random(3)
    k.revolve("plastic_blue", [(0.1, 0), (5, 0), (11, 5), (11.4, 6)], 14)
    for i in range(4):
        k.cyl("copper" if i % 2 else "plastic_black", r.uniform(-5, 5), r.uniform(-5, 5), 4, 1.7, 6, 8, roll=90, pitch=r.uniform(0, 180))   # loose batteries
    k.torus("steel", 3, -3, 5.5, 1.6, 0.2)
    for a in (0.2, 0.9):
        k.obox("brass", 3 + 4 * math.cos(a), -3 + 4 * math.sin(a), 5.6, 5, 1.2, 0.3, yaw=math.degrees(a))
    return k


@prop
def phone_book():
    k = K.Kit(); k.box("plastic_yellow", -11, -14, 0, 11, 14, 5); k.box("paper", -10.5, -13.5, 0.6, 11.2, 13.5, 4.4); return k


@prop
def doily():
    k = K.Kit(); k.cyl("fabric_white", 0, 0, 0, 15, 0.25, 22); return k


@prop
def thermostat():
    k = K.Kit(); k.cyl("enamel", 0, 0, 0, 4.2, 2.4, 20, pitch=90); k.cyl("brass", 2.4, 0, 0, 3, 0.5, 20, pitch=90); return k


@prop
def bust():
    k = K.Kit(); k.box("enamel", -3, -3, 0, 3, 3, 3); k.soft("enamel", -3.5, -5, 3, 3.5, 5, 9, 3, 3); k.sphere("enamel", 0, 0, 13, 3.6, 5, sz=1.15); return k


@prop
def wire_basket():
    k = K.Kit()
    for (a, b) in (((-10, -16, 0), (10, -16, 0)), ((-10, 16, 0), (10, 16, 0)), ((-10, -16, 24), (10, -16, 24)), ((-10, 16, 24), (10, 16, 24))):
        k.tube("brass", a, b, 0.4, 4)
    for x in (-10, 10):
        for y in range(-16, 17, 8):
            k.tube("brass", (x, y, 0), (x, y, 24), 0.3, 4)
    for i in range(4):
        k.obox("paper", 0, -8 + i * 5, 14, 17, 0.5, 24, roll=6)
    return k


@prop
def bracket_pitcher():
    k = K.Kit()                                                             # gold wall bracket with a copper pitcher; back at x=0
    k.box("brass", 0, -9, 0, 12, 9, 2); k.prism_xz("brass", [(0, 0), (9, 0), (0, -16)], -3, 3)
    k.revolve("copper", [(0.1, 0), (4, 0), (5.5, 6), (3.5, 11), (4.2, 13)], 12, cx=6, z0=2); k.torus("copper", 6, 5, 9, 3, 0.5, roll=90)
    return k


@prop
def sign_faith():
    k = K.Kit(); k.box("white", 0, -14, -9, 1.6, 14, 9); k.box("plastic_grey", 1.6, -10, -1, 1.8, 10, 0); k.box("plastic_grey", 1.6, -7, -5, 1.8, 7, -4); k.box("plastic_grey", 1.6, -8, 3, 1.8, 8, 4); return k


@prop
def ottoman():
    k = K.Kit(); k.soft("fabric_blue", -30, -45, 8, 30, 45, 42, 5, 4); legs(k, "wood_dark", -27, -42, 27, 42, 8, 5); return k


@prop
def armchair_cream():
    return sofa(92, "fabric_cream", 1)


@prop
def chair_sage():
    return sofa(84, "fabric_sage", 1)


@prop
def loveseat_tan():
    return sofa(150, "fabric_tan", 2)


@prop
def armchair_rust():
    k = sofa(96, "fabric_rust", 1)
    k.box("paper", 40, -20, 46, 62, -2, 49); k.box("plastic_yellow", 50, 8, 45, 60, 20, 48)        # notebooks and a crayon box left on the seat
    return k


@prop
def sconce():
    k = K.Kit(); k.cyl("brass", 0, 0, 0, 4, 1.5, 12, pitch=90); k.tube("brass", (1.5, 0, 0), (9, 0, 4), 0.6, 5); k.cone("lamp_shade", 9, 0, 4, 5.5, 3.5, 8, 12); return k


@prop
def barometer():
    k = K.Kit(); k.box("cherry", 0, -3, -8, 2, 3, 40); k.cyl("cherry", 0, 0, -22, 10, 2.4, 18, pitch=90); k.cyl("enamel", 2.4, 0, -22, 8, 0.3, 18, pitch=90); return k


@prop
def frame_map():
    return frame("note_numbers", 90, 60, "black")


@prop
def seashell_soap():
    k = K.Kit(); r = random.Random(2)
    k.revolve("enamel", [(0.1, 0), (7, 0), (9, 2.5)], 14)
    for i in range(4):
        k.sphere(r.choice(["enamel_pink", "fabric_cream", "plastic_mint"]), r.uniform(-4, 4), r.uniform(-4, 4), 3, 2.6, 5, sz=0.6)
    return k


@prop
def toilet_set():
    """Matching fuzzy seat cover and contour rug; origin at the toilet's origin."""
    k = K.Kit(); k.cyl("fabric_burgundy", 42, 0, 42.2, 21, 2.5, 20); k.soft("fabric_burgundy", 60, -32, 0, 105, 32, 2.2, 4, 3); return k


@prop
def mouthwash():
    k = K.Kit(); k.soft("liquid_blue", -3, -5, 0, 3, 5, 17, 3, 3); k.cyl("enamel", 0, 0, 17, 2, 3.5, 10); return k


@prop
def towels_deco():
    k = K.Kit()
    k.tube("chrome", (5, -30, 0), (5, 30, 0), 0.9)
    k.soft("fabric_burgundy", 3.5, -24, -52, 6.8, 24, 1.5, 4, 2); k.soft("fabric_cream", 6.5, -15, -34, 9, 15, 1.8, 4, 2); k.soft("fabric_burgundy", 8.8, -7, -18, 10.6, 7, 2, 4, 2)
    return k


@prop
def height_marks():
    k = K.Kit(); k.quad("p_height_marks", 0.2, -6, 0, 6, 80); return k


@prop
def faded_rect():
    """Paler rectangle where a picture used to hang."""
    k = K.Kit(); k.box("paper", 0, -22, -28, 0.12, 22, 28); return k


@prop
def poster_band():
    k = K.Kit(); k.quad("p_poster_band", 0.3, -28, -40, 28, 40); return k


@prop
def handheld():
    k = K.Kit()
    k.soft("plastic_purple", -7, -4.5, 0, 7, 4.5, 2, 3, 3); k.box("glass_dark", -3, -3, 2, 3, 3, 2.2)
    k.soft("plastic_black", 12, -6, 0, 22, 6, 4, 3, 2)                                            # cartridge case
    return k


@prop
def card_binder():
    k = K.Kit(); k.box("plastic_blue", -13, -15, 0, 13, 15, 5); k.box("paper", -12, -14, 0.5, 13.3, 14, 4.5); return k


@prop
def plush_pile():
    k = K.Kit(); r = random.Random(7)
    for i, c in enumerate(("fabric_brown", "fabric_cream", "plastic_pink", "fabric_green", "fabric_blue")):
        x, y = r.uniform(-18, 18), r.uniform(-18, 18)
        k.sphere(c, x, y, 9 + i * 2, 9, 5, sz=1.1); k.sphere(c, x + 3, y, 20 + i * 2, 6, 5)
        for s in (-1, 1):
            k.sphere(c, x + 3, y + s * 5, 25 + i * 2, 2.2, 4)
    return k


@prop
def cd_player():
    k = K.Kit(); k.cyl("plastic_grey", 0, 0, 0, 7.5, 3, 20); k.cyl("plastic_black", 0, 0, 3, 6, 0.4, 20)
    for a, b in zip([(7, 0, 1.5), (14, 6, 0.4), (20, 2, 0.4)], [(14, 6, 0.4), (20, 2, 0.4), (28, 8, 0.4)]):
        k.tube("black", a, b, 0.25, 4)
    return k


@prop
def learning_tablet():
    k = K.Kit(); k.soft("plastic_lime", -13, -10, 0, 13, 10, 3, 3, 2); k.box("glass_dark", -8, -7, 3, 6, 7, 3.2); k.tube("plastic_lime", (-13, -5, 2), (-13, 5, 2), 1.2, 6); return k


@prop
def craft_drawers():
    k = K.Kit(); r = random.Random(9)
    k.box("enamel", 0, -18, 0, 38, 18, 96)
    for i in range(4):
        k.box("plastic_clear", 38, -16.5, 3 + i * 23, 39.2, 16.5, 24 + i * 23); k.box("enamel", 39.2, -5, 12 + i * 23, 40.4, 5, 14 + i * 23)
        k.box(r.choice(["plastic_red", "plastic_blue", "plastic_yellow", "paper"]), 30, -14, 4 + i * 23, 37.6, 10, 16 + i * 23)
    return k


@prop
def printer():
    k = K.Kit(); k.soft("plastic_beige", 0, -22, 0, 34, 22, 16, 3, 2); k.obox("paper", 4, 0, 24, 0.4, 22, 20, pitch=14); k.box("paper", 30, -11, 2, 44, 11, 2.5); return k


@prop
def lamp_mint():
    k = K.Kit(); k.cyl("plastic_mint", 0, 0, 0, 7, 3, 16); k.tube("chrome", (0, 0, 3), (4, 0, 24), 0.7, 5); k.tube("chrome", (4, 0, 24), (12, 0, 28), 0.7, 5); k.cone("plastic_mint", 12, 0, 22, 6, 3, 9, 12, pitch=35); return k


@prop
def flannel_shirt():
    k = K.Kit(); k.soft("fabric_red", 0, -22, -60, 5, 22, 2, 5, 2); k.soft("fabric_cream", 4.6, -8, -40, 6, 8, -10, 3, 2); return k


@prop
def spindle_chair():
    k = K.Kit()
    k.box("wood_dark", 0, -20, 42, 40, 20, 45); legs(k, "wood_dark", 1, -19, 39, 19, 42, 3)
    for y in range(-16, 17, 8):
        k.cyl("wood_dark", 2, y, 45, 1, 44, 6)
    k.box("wood_dark", 0.5, -20, 88, 3.5, 20, 93)
    for i in range(3):
        k.obox("paper", 20, -4 + i * 3, 45.6 + i * 0.4, 11, 23, 0.3, yaw=20 * i)
    return k


@prop
def albums():
    k = K.Kit()
    for i, c in enumerate(("fabric_burgundy", "fabric_navy", "fabric_brown", "fabric_hunter", "black")):
        k.box(c, 0, i * 5.2, 0, 24, i * 5.2 + 4.6, 30)
    return k


@prop
def keepsake_box():
    k = K.Kit(); k.box("cherry", 0, -17, 0, 24, 17, 16); k.box("cherry", -0.5, -17.5, 16, 24.5, 17.5, 18); k.box("brass", 24, -5, 9, 25.5, 5, 11); return k
