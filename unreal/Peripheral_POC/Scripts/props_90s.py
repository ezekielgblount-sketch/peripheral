"""Things a 90s / 2000s kid grew up with. Same conventions as props_furniture (which holds the registry). No real brands."""
import math, random, unreal
import meshkit as K
from props_furniture import prop


@prop
def tv_90s():
    k = K.Kit()                                                             # big black plastic tube TV
    k.soft("plastic_black", 0, -37, 0, 52, 37, 60, 3, 2)
    k.box("plastic_black", 50, -37, 0, 55, 37, 60)
    k.sphere("glass_dark", 46, 0, 33, 34, 8, sx=0.32, sy=0.86, sz=0.68)
    for i in range(5):
        k.box("plastic_grey", 55, -30 + i * 5, 3, 55.6, -27 + i * 5, 4.6)
    k.box("lamp_star", 55, 28, 3.2, 55.5, 29.5, 4.4)
    return k


@prop
def game_console():
    k = K.Kit()                                                             # grey cartridge console with two wired controllers
    k.soft("plastic_grey", -10, -13, 0, 10, 13, 7, 3, 2)
    k.box("black", -3, -8, 6.6, 3, 8, 7.4); k.box("plastic_purple", -2.4, -7, 7, 2.4, 7, 11)       # cartridge
    k.box("lamp_star", 9.9, -11, 2.5, 10.2, -9.5, 3.5)
    for s, col in ((-1, "plastic_teal"), (1, "plastic_pink")):
        cx, cy = 42, s * 22
        k.soft("plastic_grey", cx - 5, cy - 7.5, 0, cx + 5, cy + 7.5, 3.2, 3, 3)
        k.cyl("black", cx, cy - 4, 3, 1.6, 0.8, 8)
        for (dx, dy) in ((0.8, 3.2), (-0.8, 4.8)):
            k.cyl(col, cx + dx, cy + dy, 3, 0.8, 0.6, 8)
        pts = [(10 + t * (cx - 15), s * (6 + 16 * t + 5 * math.sin(t * 7)), 0.4) for t in [i / 10.0 for i in range(11)]]
        for a, b in zip(pts[:-1], pts[1:]):
            k.tube("black", a, b, 0.35, 4)
    return k


@prop
def pc_monitor():
    k = K.Kit()                                                             # beige CRT monitor, front toward +X
    k.soft("plastic_beige", 0, -19, 9, 38, 19, 42, 3, 2); k.box("plastic_beige", 36, -20, 8, 40, 20, 43)
    k.sphere("glass_dark", 33, 0, 27, 17, 8, sx=0.42, sy=1.0, sz=0.8)
    k.cyl("plastic_beige", 20, 0, 0, 12, 3, 16); k.cyl("plastic_beige", 20, 0, 3, 5, 6, 10)
    k.box("lamp_star", 40, 14, 10, 40.4, 15.5, 11)
    return k


@prop
def pc_tower():
    k = K.Kit()
    k.box("plastic_beige", 0, -9.5, 0, 42, 9.5, 40)
    for z in (30, 24):
        k.box("plastic_grey", 42, -7, z, 42.4, 7, z + 4.2)
    k.box("black", 42, -4.5, 19, 42.5, 4.5, 19.6)                             # floppy slot
    k.cyl("plastic_grey", 42, 0, 10, 1.6, 0.6, 10, pitch=90); k.box("lamp_star", 42, 4, 9.5, 42.4, 5.2, 10.5)
    return k


@prop
def pc_keyboard():
    k = K.Kit()
    k.box("plastic_beige", -8, -22, 0, 8, 22, 2.2)
    for i in range(5):
        k.box("paper", -6.5 + i * 2.7, -20.5, 2.2, -4.4 + i * 2.7, 14, 2.9)
    k.box("paper", -6.5, 16, 2.2, 6.4, 20.5, 2.9)
    k.soft("plastic_beige", -4, 28, 0, 5, 34, 3, 3, 3)                        # mouse
    for a, b in zip([(-4, 31, 0.5), (-10, 30, 0.4), (-16, 26, 0.4)], [(-10, 30, 0.4), (-16, 26, 0.4), (-22, 27, 0.4)]):
        k.tube("plastic_grey", a, b, 0.3, 4)
    return k


@prop
def lava_lamp():
    k = K.Kit()
    k.revolve("chrome", [(0.1, 0), (6.5, 0), (4, 10), (4.6, 12)], 16)
    k.revolve("lamp_lava", [(4.4, 12), (5.2, 18), (3.2, 32), (2.6, 34)], 16)
    k.revolve("chrome", [(2.8, 34), (2.2, 39), (0.1, 39.5)], 16)
    return k


@prop
def bean_bag():
    c = K.Kit()
    c.sphere("confetti", 0, 0, 26, 46, 9, sz=0.6); c.sphere("confetti", -8, 0, 44, 30, 8, sz=0.6)
    c.noise(5, 0.03, 4)
    return c


@prop
def ceiling_fan():
    k = K.Kit()                                                             # origin at the ceiling
    k.cyl("brass", 0, 0, -6, 6, 6, 14); k.cyl("brass", 0, 0, -24, 1.4, 18, 8); k.cyl("brass", 0, 0, -36, 11, 12, 18)
    for i in range(4):
        a = math.radians(i * 90 + 20)
        k.obox("oak", math.cos(a) * 42, math.sin(a) * 42, -30, 58, 13, 0.9, yaw=math.degrees(a), roll=8)
    k.sphere("lamp_on", 0, 0, -44, 9, 6, sz=0.8)
    return k


def blinds(w, h):
    """Mini blinds: back at x=0, hangs from z=h down to 0, centred on Y."""
    k = K.Kit()
    k.box("white", 0, -w / 2, h - 3, 4, w / 2, h)
    z = h - 4.5
    while z > 1:
        k.obox("white", 2.2, 0, z, 2.6, w - 1, 0.12, pitch=28)
        z -= 2.4
    k.box("white", 0.5, -w / 2, 0, 3.5, w / 2, 1.2)
    k.tube("white", (4, w / 2 - 8, h - 3), (4, w / 2 - 8, h * 0.45), 0.3, 4)      # tilt wand
    return k


@prop
def blinds_120():
    return blinds(114, 128)


@prop
def blinds_240():
    return blinds(234, 148)


@prop
def blinds_90():
    return blinds(84, 128)


@prop
def microwave():
    k = K.Kit()
    k.box("enamel", 0, -25, 0, 36, 25, 29)
    k.box("glass_dark", 36, -22, 4, 36.5, 9, 25); k.box("plastic_grey", 36, 11, 3, 36.5, 23, 26)
    k.box("lamp_star", 36.5, 12.5, 21, 36.8, 21.5, 24)
    return k


def cereal_box(pr):
    k = K.Kit()
    k.box("paper", -3, -9.5, 0, 3, 9.5, 27); k.quad("p_" + pr, 3.1, -9.5, 0, 9.5, 27)
    return k


@prop
def cereal_a():
    return cereal_box("cereal_a")


@prop
def cereal_b():
    return cereal_box("cereal_b")


@prop
def cd_tower():
    k = K.Kit(); r = random.Random(4)
    k.box("plastic_black", -8, -8, 0, 8, 8, 2)
    for y in (-8, 7):
        k.box("plastic_black", -8, y, 2, 8, y + 1, 92)
    for i in range(34):
        if r.random() < 0.8:
            k.box(r.choice(["plastic_grey", "plastic_teal", "paper", "plastic_red", "black", "plastic_purple"]), -7, -6.8, 3 + i * 2.6, 6.5, 6.8, 4 + i * 2.6)
    return k


@prop
def skateboard():
    k = K.Kit()
    k.soft("confetti", -40, -10, 9, 40, 10, 10.6, 4, 2)
    for x in (-27, 27):
        k.box("steel", x - 2.5, -8, 6, x + 2.5, 8, 9)
        for y in (-10.5, 7.5):
            k.cyl("plastic_lime", x, y, 3, 3, 3, 12, roll=-90)
    return k


@prop
def glow_stars():
    """Glow-in-the-dark stars stuck to the ceiling; origin at the ceiling."""
    k = K.Kit(); r = random.Random(8)
    for _ in range(22):
        x, y, s = r.uniform(-90, 90), r.uniform(-70, 70), r.uniform(1.6, 3.2)
        pts = [(x + (s if i % 2 == 0 else s * 0.45) * math.cos(i * math.pi / 5), y + (s if i % 2 == 0 else s * 0.45) * math.sin(i * math.pi / 5)) for i in range(10)]
        k.extrude("lamp_star", pts, -0.3, 0.3)
    return k


@prop
def phone_cordless():
    k = K.Kit()
    k.soft("plastic_black", -6, -8, 0, 8, 8, 4, 3, 2)
    k.soft("plastic_black", -4, -3, 3, 0, 3, 21, 3, 3)
    k.tube("black", (-2, 2, 21), (-2, 2, 30), 0.4, 5)
    k.box("lamp_star", 6, -6, 4, 7, -5, 4.3)
    return k


@prop
def border_1m():
    k = K.Kit(); k.quad("p_border_ivy", 0.25, -50, 0, 50, 12.5); return k


@prop
def border_1m_fruit():
    k = K.Kit(); k.quad("p_border_fruit", 0.25, -50, 0, 50, 12.5); return k


@prop
def backpack():
    k = K.Kit()
    k.soft("plastic_teal", 0, -15, 0, 16, 15, 40, 4, 4); k.soft("plastic_purple", 14, -11, 4, 20, 11, 22, 3, 3)
    k.tube("plastic_black", (2, -8, 38), (2, 8, 38), 1.0, 6)
    return k
