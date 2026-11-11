"""Traditional family-home furniture, after Joel's reference photos. Same conventions as props_furniture (registry lives there)."""
import math, random, unreal
import meshkit as K
from props_furniture import prop, legs, frame


@prop
def piano():
    k = K.Kit()                                                             # upright piano, 148 wide
    k.box("wood_dark", 0, -74, 8, 34, 74, 104); k.box("wood_dark", -1, -76, 104, 36, 76, 108)
    k.box("wood_dark", 34, -74, 60, 62, 74, 70)                              # key bed
    k.box("paper", 40, -66, 70, 61, 66, 72)                                  # white keys
    for i in range(52):
        if i % 7 not in (2, 6):
            k.box("black", 40, -66 + i * 2.54 + 1.6, 72, 53, -66 + i * 2.54 + 3.0, 73.2)
    k.box("wood_dark", 34, -74, 70, 40, 74, 74)
    k.obox("wood_dark", 37, 0, 88, 2, 70, 24, pitch=-12)                     # music desk
    k.box("paper", 38, -30, 78, 39, -6, 100); k.box("plastic_red", 38.5, 4, 78, 40, 24, 102)   # sheet music and a hymnal
    for y in (-70, 66):
        k.cyl("wood_dark", 58, y + 2, 0, 3.4, 60, 10); k.box("wood_dark", 0, y, 0, 34, y + 4, 8)
    return k


@prop
def piano_bench():
    k = K.Kit()
    k.soft("fabric_stripe", -19, -45, 44, 19, 45, 51, 3, 2); k.box("wood_dark", -19, -45, 40, 19, 45, 45)
    legs(k, "wood_dark", -18, -44, 18, 44, 40, 4)
    return k


@prop
def globe():
    k = K.Kit()
    k.cyl("wood_dark", 0, 0, 0, 9, 2, 16); k.cyl("wood_dark", 0, 0, 2, 1.2, 8, 8)
    k.sphere("globe", 0, 0, 24, 15, 9); k.torus("brass", 0, 0, 24, 16, 0.5, roll=70)
    return k


@prop
def piano_lamp():
    k = K.Kit()
    k.cyl("brass", 0, 0, 0, 6, 1.5, 14); k.tube("brass", (0, 0, 1.5), (4, 0, 22), 0.8, 6)
    k.cyl("brass", 4, -15, 24, 3, 30, 10, roll=-90); k.box("lamp_shade", 2, -13, 21.2, 6, 13, 21.8)
    return k


@prop
def fireplace():
    k = K.Kit()                                                             # brick surround, white mantel, 190 wide
    k.box("brick", 0, -85, 0, 26, -45, 118); k.box("brick", 0, 45, 0, 26, 85, 118); k.box("brick", 0, -45, 72, 26, 45, 118)
    k.box("black", 0, -45, 0, 6, 45, 72); k.box("brick", 0, -70, 0, 50, 70, 5)                  # firebox and hearth
    k.box("white", 0, -95, 118, 30, 95, 140); k.box("white", 0, -102, 140, 40, 102, 146)       # frieze and shelf
    for y in (-95, 83):
        k.box("white", 26, y, 0, 30, y + 12, 118)
    k.cyl("wood_dark", 20, 0, 146, 10, 4, 14); k.cyl("brass", 22, 0, 150, 8, 5, 18, pitch=90); k.quad("p_clock_face", 27.2, -7, 151, 7, 165)
    r = random.Random(3)
    for y, col, s in ((-70, "pumpkin", 6), (-52, "enamel", 5), (-30, "pumpkin", 4), (34, "enamel", 5.5), (58, "pumpkin", 6.5), (78, "brass", 3.5)):
        k.sphere(col, 18 + r.uniform(-4, 6), y, 146 + s * 0.7, s, 6, sz=0.72); k.cyl("bark", 18, y, 146 + s * 1.3, 0.6, 2, 5)
    for i in range(16):
        k.obox("pumpkin" if i % 3 else "fabric_brown", 14 + r.uniform(0, 14), -88 + i * 11.5, 147.5, 9, 6, 0.4, yaw=r.uniform(0, 180), roll=r.uniform(-25, 25))
    return k


@prop
def bookshelf_white():
    k = K.Kit(); r = random.Random(5)                                        # built-in shelves full of books and framed photos
    for y in (-52, 0, 49):
        k.box("white", 0, y - 1.5 if y == 0 else y, 0, 32, (y + 1.5) if y == 0 else y + 3, 232)
    k.box("white", 0, -52, 0, 1.5, 52, 232); k.box("white", 0, -54, 232, 34, 54, 240)
    for i, z in enumerate((8, 52, 96, 140, 184, 228)):
        k.box("white", 0, -52, z, 32, 52, z + 3)
        for side in (-1, 1):
            y0, y1 = (-48, -3) if side < 0 else (3, 48)
            kind = (i + (side > 0)) % 3
            if z > 200:
                continue
            if kind == 0:
                k.box("black", 4, y0, z + 3, 24, y1 - 6, z + 30); k.quad("p_book_spines_a" if side < 0 else "p_book_spines_b", 24.1, y0, z + 3, y1 - 6, z + 31)
            elif kind == 1:                                                  # framed photos, blank faces
                for j, pr in enumerate(("photo_school", "photo_family_a", "photo_school_b")):
                    w, h = (11, 14) if "school" in pr else (17, 13)
                    y = y0 + 8 + j * 14
                    k.box("brass" if j % 2 else "wood_dark", 12 + j * 3, y - w / 2 - 1, z + 3, 13 + j * 3, y + w / 2 + 1, z + 5 + h)
                    k.quad("p_" + pr, 13.1 + j * 3, y - w / 2, z + 4, y + w / 2, z + 4 + h)
            else:
                for j in range(4):
                    k.box(r.choice(["fabric_brown", "plastic_blue", "fabric_red", "paper"]), 6, y0 + 2, z + 3 + j * 4, 26, y0 + 22, z + 6.6 + j * 4)
                k.cyl("plastic_blue", 20, y1 - 14, z + 15, 11, 1.2, 18, pitch=80)
    return k


@prop
def mirror_wall():
    k = K.Kit()
    for (y0, y1, z0, z1) in ((-60, 60, 40, 48), (-60, 60, -48, -40), (-60, -52, -40, 40), (52, 60, -40, 40)):
        k.box("wood_dark", 0, y0, z0, 4, y1, z1)
    k.box("mirror", 0, -52, -40, 1.5, 52, 40)
    return k


@prop
def secretary():
    k = K.Kit()                                                             # slant-front desk over four drawers
    k.box("wood_plain" if False else "oak", 0, -47, 6, 46, 47, 80)
    k.prism_xz("oak", [(0, 80), (46, 80), (20, 108), (0, 108)], -47, 47)
    k.box("oak", 0, -49, 108, 22, 49, 110)
    for i in range(4):
        z = 9 + i * 17.5
        k.box("wood_light", 46, -44, z, 47.4, 44, z + 16)
        for y in (-28, 28):
            k.box("brass", 47.4, y - 5, z + 6, 48.6, y + 5, z + 9)
    for (x, y) in ((2, -46), (2, 40), (40, -46), (40, 40)):
        k.box("oak", x, y, 0, x + 6, y + 6, 6)
    return k


@prop
def hutch():
    k = K.Kit()                                                             # honey-maple hutch with leaded-glass doors
    k.box("oak", 0, -100, 8, 46, 100, 90); k.box("black", 4, -100, 0, 42, 100, 8); k.box("oak", -1, -102, 90, 48, 102, 94)
    k.box("oak", 0, -100, 94, 6, 100, 226); k.box("oak", 0, -102, 226, 36, 102, 234)
    for y in (-100, -52, -1.5, 49, 97):
        k.box("oak", 0, y, 110, 32, y + 3, 226)
    k.box("oak", 0, -100, 94, 32, 100, 110)
    for (y0, y1, glass) in ((-97, -52, False), (-49, -1.5, True), (1.5, 49, True), (52, 97, False)):
        if glass:
            k.box("glass", 31, y0, 112, 31.6, y1, 224)
            for z in (140, 170, 200):
                k.box("steel", 31.6, y0, z, 32, y1, z + 0.6)
            k.box("paper", 8, y0 + 4, 150, 26, y1 - 4, 152); k.box("paper", 8, y0 + 4, 186, 26, y1 - 4, 188)
            for j in range(3):
                k.cyl("enamel", 16, y0 + 12 + j * 12, 152, 5, 3 + j * 2, 12)
        else:
            k.box("wood_light", 32, y0, 112, 33.5, y1, 224)
        k.sphere("brass", 34.5, y1 - 4 if y0 < 0 else y0 + 4, 118, 1.6, 4)
    for (y0, y1) in ((-97, -52), (-49, 49), (52, 97)):
        k.box("wood_light", 46, y0, 12, 47.5, y1, 50); k.box("wood_light", 46, y0, 53, 47.5, y1, 88)
        k.sphere("brass", 49, (y0 + y1) / 2, 70, 2, 4); k.sphere("brass", 49, (y0 + y1) / 2, 31, 2, 4)
    return k


@prop
def pendant():
    k = K.Kit()                                                             # glass pendant on a chain; origin at the ceiling
    k.cyl("metal_dark", 0, 0, -2, 6, 2, 12); k.tube("metal_dark", (0, 0, -2), (0, 0, -40), 0.6, 5)
    k.sphere("glass", 0, 0, -56, 17, 8, sz=0.85); k.sphere("lamp_on", 0, 0, -54, 3.5, 5)
    return k


@prop
def coffee_table_glass():
    k = K.Kit()
    for (x, y) in ((2, -62), (2, 60), (58, -62), (58, 60)):
        k.cyl("brass", x, y, 0, 1.4, 44, 8)
    for y in (-62, 60):
        k.tube("brass", (2, y, 43), (58, y, 43), 1.2, 6); k.tube("brass", (2, y, 12), (58, y, 12), 1.0, 6)
    for x in (2, 58):
        k.tube("brass", (x, -62, 43), (x, 60, 43), 1.2, 6)
    k.box("glass", 0, -64, 44, 60, 62, 45.2)
    k.box("fabric_white", 14, -70, 45.2, 44, 10, 45.6)                        # table runner
    k.box("oak", 12, 14, 45.2, 48, 54, 48)                                    # tray with a stack of books
    for j, c in enumerate(("plastic_blue", "paper", "fabric_brown")):
        k.box(c, 16 + j, 20, 48 + j * 3.2, 42 - j, 48, 51 + j * 3.2)
    return k


@prop
def chair_red():
    k = K.Kit()                                                             # red plastic desk chair on casters
    k.soft("plastic_red", 0, -22, 44, 42, 22, 49, 4, 4); k.soft("plastic_red", -3, -20, 60, 3, 20, 92, 4, 4)
    k.tube("plastic_black", (2, 0, 49), (0, 0, 62), 3, 6); k.cyl("plastic_black", 21, 0, 12, 3, 32, 10)
    for i in range(5):
        a = i * 1.2566
        k.tube("plastic_black", (21, 0, 12), (21 + 28 * math.cos(a), 28 * math.sin(a), 6), 2, 6)
        k.sphere("plastic_black", 21 + 28 * math.cos(a), 28 * math.sin(a), 3, 3, 4)
    return k


@prop
def sofa_butter():
    from props_furniture import sofa
    k = sofa(212, "fabric_butter", 3)
    k.soft("quilt", 40, -40, 44, 78, 20, 52, 4, 3)                            # patchwork quilt left on the seat
    k.soft("floral_red", 30, -92, 46, 44, -52, 84, 4, 5)                      # floral pillow
    return k


@prop
def armchair_red():
    from props_furniture import sofa
    return sofa(96, "fabric_red", 1)


@prop
def table_lamp_drum():
    k = K.Kit()
    k.revolve("glass", [(0.1, 0), (7, 0), (7, 3), (3, 8), (5, 20), (2.5, 34), (1.2, 36)], 14)
    k.cyl("lamp_shade", 0, 0, 34, 16, 22, 20)
    return k


@prop
def frame_landscape_a():
    return frame("print_landscape_a", 80, 56)


@prop
def frame_landscape_b():
    return frame("print_landscape_b", 110, 60)


@prop
def chart_alphabet():
    k = K.Kit(); k.quad("p_chart_alphabet", 0.3, -32, -45, 32, 45); return k


@prop
def chart_fractions():
    k = K.Kit(); k.quad("p_chart_fractions", 0.3, -32, -19, 32, 19); return k


@prop
def rug_oriental():
    k = K.Kit(); k.decal_top("p_rug_oriental", -110, -160, 110, 160, 0.6); return k


@prop
def valance_red():
    from props_furniture import drape
    return drape(150, 40, "floral_red", 6, 3)


@prop
def bed_quilt():
    k = K.Kit()
    k.box("wood_dark", 0, -50, 0, 4, 50, 95); k.box("wood_dark", 196, -50, 0, 200, 50, 50)
    k.box("wood_dark", 4, -50, 22, 196, -47, 34); k.box("wood_dark", 4, 47, 22, 196, 50, 34)
    k.soft("fabric_white", 5, -47, 26, 195, 47, 50, iters=3); k.soft("quilt", 50, -51, 30, 197, 51, 55, iters=4)
    k.soft("fabric_white", 10, -32, 48, 48, 32, 62, iters=7)
    return k


@prop
def desk_wood():
    k = K.Kit()
    k.box("wood_plain" if False else "rail", 0, -62, 72, 60, 62, 76); k.box("glass", 0, -62, 76, 60, 62, 76.6)
    k.box("rail", 2, 22, 8, 58, 60, 72); k.box("rail", 2, -60, 8, 58, -48, 72); k.box("rail", 2, -60, 58, 58, 22, 72)
    for y in (-38, -6, 40):
        k.cyl("glass", 60, y, 65, 2.4, 1.6, 10, pitch=90)
    k.box("brass", 58, 32, 20, 60.5, 50, 26)
    return k


@prop
def torchiere():
    """Black halogen floor lamp: weighted base, thin pole, shallow bowl that throws its light at the ceiling."""
    k = K.Kit()
    k.cyl("plastic_black", 0, 0, 0, 13, 2.2, 24); k.cyl("plastic_black", 0, 0, 2.2, 1.2, 170, 10)
    k.cone("plastic_black", 0, 0, 171, 3.5, 17, 9, 24); k.cyl("lamp_on", 0, 0, 179.6, 15.5, 0.5, 24)
    k.cyl("plastic_black", 1.6, 0, 120, 1.5, 3, 8)                          # dimmer knob on the pole
    return k
