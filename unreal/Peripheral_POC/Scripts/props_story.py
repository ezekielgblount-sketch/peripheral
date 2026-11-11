"""Story props: the parents' 2010-2014 tech, Jack's car, and the things Day One uses (breaker, fridge, window sash, mail)."""
import math, random, unreal
import meshkit as K
from props_furniture import prop, legs


@prop
def flat_tv():
    k = K.Kit()                                                             # 26-inch flat screen, thick glossy bezel
    k.box("plastic_black", 10, -33, 8, 16, 33, 49); k.box("glass_dark", 16, -29.5, 12, 16.4, 29.5, 46)
    k.box("plastic_black", 6, -4, 2, 14, 4, 10); k.soft("plastic_black", 0, -17, 0, 22, 17, 2.2, 3, 2)
    k.box("lamp_led", 16.3, 26, 9.4, 16.6, 27.2, 10.2)
    return k


@prop
def entertainment_center():
    k = K.Kit(); r = random.Random(2)                                        # old oak unit with cubbies of tapes and discs
    k.box("oak", 0, -80, 0, 48, 80, 6); k.box("oak", 0, -80, 62, 50, 80, 66); k.box("oak", 0, -80, 6, 2, 80, 62)
    for y in (-80, -27, 24, 77):
        k.box("oak", 0, y, 6, 48, y + 3, 62)
    k.box("oak", 2, -77, 33, 46, 77, 35)
    for (y0, y1, z) in ((-77, -27, 6), (27, 77, 6), (-77, -27, 35), (27, 77, 35)):
        y = y0 + 2
        while y < y1 - 4:
            w = r.choice((2.6, 2.6, 1.5)); c = r.choice(["plastic_black", "paper", "plastic_blue", "fabric_red", "black", "plastic_teal"])
            k.box(c, 10, y, z, 30 if w > 2 else 24, y + w - 0.3, z + (20.5 if w > 2 else 19)); y += w
    return k


@prop
def dvd_player():
    k = K.Kit()
    k.box("plastic_black", 0, -21, 0.6, 26, 21, 5.5); k.box("plastic_grey", 26, -21, 0.6, 26.4, 21, 5.5)
    k.box("black", 26.4, -16, 2.6, 26.7, 0, 3.6); k.box("lamp_led", 26.4, 15, 2.6, 26.7, 16, 3.4)
    return k


@prop
def console_2010():
    k = K.Kit()                                                             # black slab console and a wireless pad
    k.soft("plastic_black", 0, -14, 0, 26, 14, 7, 3, 2); k.box("lamp_star", 26, -11, 3, 26.3, -9.6, 3.8)
    k.soft("plastic_black", 34, -8, 0, 44, 8, 4, 4, 4)
    for y in (-4.5, 4.5):
        k.cyl("plastic_grey", 39, y, 4, 1.6, 0.8, 8)
    return k


@prop
def router():
    k = K.Kit()
    k.soft("plastic_black", 0, -11, 0, 15, 11, 3.5, 3, 2)
    for y in (-8, 8):
        k.tube("plastic_black", (2, y, 3), (1, y, 17), 0.5, 5)
    for i in range(5):
        k.box("lamp_blink" if i % 2 else "lamp_star", 15, -7 + i * 3.5, 1.4, 15.3, -6 + i * 3.5, 2.1)
    return k


@prop
def laptop():
    k = K.Kit()                                                             # thick 2011 laptop, lid half closed
    k.soft("plastic_grey", -12, -18, 0, 12, 18, 2.6, 3, 2); k.box("black", -9, -15, 2.6, 6, 15, 2.8)
    k.obox("plastic_grey", -14, 0, 11, 1.4, 36, 23, pitch=-18); k.obox("glass_dark", -13.2, 0, 11.2, 0.3, 32, 20, pitch=-18)
    return k


@prop
def tablet():
    k = K.Kit()
    k.soft("fabric_navy", -10, -13.5, 0, 10, 13.5, 1.6, 3, 2); k.box("glass_dark", -8.5, -12, 1.6, 8.5, 12, 1.8)
    return k


@prop
def charger():
    k = K.Kit()
    k.box("enamel", 0, -1.5, -2, 3, 1.5, 2)
    pts = [(3, 0, 0), (6, 2, -10), (5, 6, -24), (9, 10, -29.5), (22, 8, -29.6)]
    for a, b in zip(pts[:-1], pts[1:]):
        k.tube("enamel", a, b, 0.25, 4)
    return k


@prop
def car():
    """Jack's car: an invented early-90s compact four-door, base model, faded paint, boot open.
    Origin on the ground under the middle; nose toward +X. 430 long, 168 wide, 138 tall. Hollow, with a simple interior."""
    k = K.Kit(); P_ = "car_paint"
    # lower body (front and middle), bonnet, open boot tub
    k.soft(P_, -122, -84, 24, 212, 84, 70, 5, 2, 0.25)
    k.soft(P_, 96, -80, 62, 206, 80, 79, 4, 2, 0.3)                                   # bonnet
    k.box(P_, -212, -84, 24, -122, 84, 56); k.box("black", -208, -76, 56, -122, 76, 57.5)   # boot floor
    for y in (-84, 78):
        k.box(P_, -212, y, 56, -122, y + 6, 78)
    k.box(P_, -212, -78, 56, -207, 78, 64)                                            # low rear sill
    k.obox(P_, -136, 0, 119, 84, 150, 3, pitch=110)                                   # boot lid, hinged at the rear window and raised
    # roof, pillars and glass (thin panels, so the driver can see out)
    k.box(P_, -86, -73, 131, 54, 73, 137)                                               # roof panel
    for y in (-72, 68):
        k.tube(P_, (96, y + 2, 78), (50, y + 2, 133), 3, 6); k.tube(P_, (-120, y + 2, 78), (-82, y + 2, 133), 3.5, 6)
        k.box(P_, -20, y, 70, -12, y + 4, 133)                                        # B pillar
        k.box("glass", -80, y + 1.2, 80, 46, y + 2.4, 131)                            # side windows
        k.box("black", -118, y - 0.2 if y < 0 else y + 3.8, 62, 96, y + 0.2 if y < 0 else y + 4.2, 62.6)   # door seam line
        for x in (40, -50):
            k.box("plastic_black", x, y - 1.4 if y < 0 else y + 4, 84, x + 12, y if y < 0 else y + 5.4, 87)   # door handles
    k.prism_xz("glass", [(96, 78), (98, 78), (52, 133), (50, 133)], -69, 69)         # windscreen
    k.prism_xz("glass", [(-122, 78), (-120, 78), (-82, 133), (-84, 133)], -69, 69)   # rear window
    # interior
    k.box("fabric_tan", -122, -76, 56, 96, 76, 60)                                    # floor
    k.soft("plastic_black", 58, -74, 70, 98, 74, 94, 4, 2)                            # dashboard
    k.torus("plastic_black", 48, -36, 97, 17, 1.8, pitch=62); k.tube("plastic_black", (50, -36, 97), (62, -36, 88), 2.2, 6)
    for y in (-36, 36):
        k.soft("fabric_tan", -22, y - 24, 60, 30, y + 24, 78, 4, 3); k.soft("fabric_tan", -30, y - 23, 72, -14, y + 23, 124, 4, 3)
    k.soft("fabric_tan", -108, -68, 60, -62, 68, 78, 4, 3); k.soft("fabric_tan", -118, -68, 72, -104, 68, 118, 4, 3)
    k.box("plastic_black", 0, -6, 60, 40, 6, 74)                                      # centre console
    # wheels, arches, bumpers, lights, mirrors, plate, aerial
    for x in (-132, 138):
        for sgn in (-1, 1):
            k.tube("plastic_black", (x, sgn * 66, 29), (x, sgn * 85, 29), 29, 20)       # tyre
            k.tube("steel", (x, sgn * 84, 29), (x, sgn * 86, 29), 16, 14)              # plain steel wheel
            k.tube("plastic_black", (x, sgn * 86, 29), (x, sgn * 86.6, 29), 5, 8)
    k.soft("plastic_grey", 204, -84, 28, 220, 84, 46, 3, 2); k.soft("plastic_grey", -220, -84, 28, -206, 84, 46, 3, 2)
    for y in (-62, 62):
        k.box("lamp_off", 211, y - 17, 54, 214, y + 17, 67); k.box("plastic_red", -213.5, y - 17, 58, -211, y + 17, 72)
        k.box("plastic_black", 60, y - 22 if y < 0 else y + 12, 84, 72, y - 12 if y < 0 else y + 22, 93)                 # mirrors
    k.box("black", 211, -30, 54, 213, 30, 66)                                         # grille
    k.box("paper", -221, -15, 34, -220, 15, 44)                                       # blank plate
    k.tube("steel", (70, 70, 80), (64, 72, 150), 0.3, 4)
    return k


@prop
def mail_pile():
    k = K.Kit(); r = random.Random(5)
    for i in range(9):
        k.obox(r.choice(["paper", "paper", "enamel", "plastic_beige"]), r.uniform(-8, 8), r.uniform(-10, 10), 0.3 + i * 0.3, 11, 23, 0.25, yaw=r.uniform(-50, 50))
    return k


@prop
def breaker_panel():
    k = K.Kit()                                                             # grey panel, door open; back at x=0, centred
    k.box("plastic_grey", 0, -18, -30, 9, 18, 30); k.box("black", 9, -14, -24, 9.4, 14, 22)
    for i in range(8):
        for y in (-8, 8):
            k.box("plastic_black", 9.4, y - 5, -20 + i * 5, 10.6, y + 5, -16.6 + i * 5)
    k.box("plastic_grey", 0, -55, -30, 1, -19, 30)                               # door swung flat against the wall
    return k


@prop
def breaker_lever():
    k = K.Kit(); k.box("plastic_red", 0, -4, -2.5, 5, 4, 2.5); k.box("black", 0, -6, -4, 1, 6, 4); return k


@prop
def window_sash():
    """Lower sash of a double-hung window; back at x=0, centred on Y, origin at its bottom edge."""
    k = K.Kit(); w, h = 48, 72
    for (y0, y1, z0, z1) in ((-w / 2, w / 2, 0, 4.5), (-w / 2, w / 2, h - 4.5, h), (-w / 2, -w / 2 + 4.5, 0, h), (w / 2 - 4.5, w / 2, 0, h)):
        k.box("white", 0, y0, z0, 4, y1, z1)
    k.box("glass", 1.7, -w / 2 + 4, 4, 2.3, w / 2 - 4, h - 4); k.box("brass", 4, -4, 1, 6, 4, 2.5)
    return k


@prop
def fridge_body():
    k = K.Kit()                                                             # open cabinet with shelves; freezer door fixed shut
    k.box("enamel_gold", 0, -38, 2, 4, 38, 168); k.box("enamel_gold", 0, -38, 2, 66, -35, 168); k.box("enamel_gold", 0, 35, 2, 66, 38, 168)
    k.box("enamel_gold", 0, -38, 114, 66, 38, 118); k.box("enamel_gold", 0, -38, 164, 66, 38, 168); k.box("enamel_gold", 0, -38, 2, 66, 38, 8)
    k.box("enamel", 4, -35, 8, 6, 35, 114)
    for z in (40, 66, 92):
        k.box("glass", 6, -35, z, 60, 35, z + 1)
    k.box("enamel_gold", 66, -37.5, 118, 71, 37.5, 167); k.box("chrome", 71, 30, 124, 74, 32.5, 150)
    k.quad("p_kid_drawing", 71.2, -22, 124, 4, 144); k.box("plastic_red", 71.2, -10, 142.5, 71.9, -8, 144.5)
    k.box("black", 2, -36, 0, 64, 36, 6)
    return k


@prop
def fridge_door():
    """Main fridge door with the notes and magnets on it. Hinge at the origin (door runs along +X when closed)."""
    k = K.Kit()
    k.box("enamel_gold", 0, -5, 0, 75, 0, 110); k.box("chrome", 66, 0, 74, 68.5, 3, 106)
    k.box("enamel", 4, -9, 6, 71, -5, 104)
    for (pr, x, z, w, h, mag) in (("note_grocery", 14, 30, 14, 18, "plastic_red"), ("note_chores", 34, 44, 16, 20, "plastic_blue"),
                                  ("note_numbers", 54, 34, 14, 17, "plastic_yellow"), ("photo_school", 18, 66, 11, 14, "plastic_green"),
                                  ("photo_school_b", 38, 74, 11, 14, "plastic_red"), ("note_mom", 56, 70, 13, 17, "plastic_green")):
        t = K.Kit(); t.quad("p_" + pr, 0, -w / 2, 0, w / 2, h); t.cyl(mag, 0.1, 0, h - 2, 1.4, 0.7, 8, pitch=90)
        k.add(t, K.T(x, 0.3, z, yaw=90))
    for i, c in enumerate(("plastic_red", "plastic_yellow", "plastic_blue", "plastic_green", "plastic_red", "plastic_purple", "plastic_teal")):
        k.box(c, 8 + i * 6, 0, 12 + (i * 7) % 6, 11 + i * 6, 0.9, 16 + (i * 7) % 6)
    return k


def food(kind):
    k = K.Kit()
    if kind == 0:                                                           # milk carton
        k.box("paper", -4.5, -4.5, 0, 4.5, 4.5, 19); k.prism_xz("paper", [(-4.5, 19), (4.5, 19), (0, 24)], -4.5, 4.5); k.box("plastic_blue", -4.6, -4.6, 6, 4.6, 4.6, 13)
    elif kind == 1:                                                         # takeout box
        k.soft("enamel", -9, -9, 0, 9, 9, 7, 3, 2)
    elif kind == 2:                                                         # covered bowl gone bad
        k.cyl("plastic_clear", 0, 0, 0, 8, 6, 14); k.cyl("plastic_green", 0, 0, 5.4, 7.4, 0.5, 14)
    else:                                                                   # jar
        k.cyl("glass", 0, 0, 0, 4, 11, 12); k.cyl("plastic_red", 0, 0, 11, 4.1, 1.5, 12)
    return k


@prop
def food_0():
    return food(0)


@prop
def food_1():
    return food(1)


@prop
def food_2():
    return food(2)


@prop
def food_3():
    return food(3)


@prop
def box_carry_a():
    from props_furniture import carton
    return carton(50, 40, 34, "label_jack")


@prop
def box_carry_b():
    from props_furniture import carton
    return carton(46, 40, 32, "label_misc")
