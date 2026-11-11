"""Kitchen, bathroom, toys, electronics and house fixtures. Same conventions as props_furniture (which holds the registry)."""
import math, unreal
import meshkit as K
from props_furniture import prop, legs


# ---------------- kitchen ----------------
def base_cabinet(w, doors=2, drawer_row=True, top="laminate", body="wood_dark"):
    k = K.Kit()
    k.box("black", 6, -w / 2, 0, 56, w / 2, 10)                                     # toe kick
    k.box(body, 0, -w / 2, 10, 58, w / 2, 87)
    k.box(top, -1, -w / 2, 87, 62, w / 2, 91)                                       # counter top at 91
    k.box(top, -1, -w / 2, 91, 1.5, w / 2, 101)                                     # backsplash lip
    dw = w / doors
    for i in range(doors):
        y = -w / 2 + i * dw
        z0 = 12
        if drawer_row:
            k.box("wood_light", 58, y + 1.5, 70, 59.6, y + dw - 1.5, 85)
            k.box("chrome", 59.6, y + dw / 2 - 5, 76.5, 61.5, y + dw / 2 + 5, 78)
            k.box("wood_light", 58, y + 1.5, z0, 59.6, y + dw - 1.5, 68)
        else:
            k.box("wood_light", 58, y + 1.5, z0, 59.6, y + dw - 1.5, 85)
        hy = y + dw - 6 if i % 2 == 0 else y + 6
        k.box("chrome", 59.6, hy - 0.8, 52, 61.5, hy + 0.8, 62)
    return k


@prop
def cab_base_90():
    return base_cabinet(90)


@prop
def cab_base_60():
    return base_cabinet(60, 1)


@prop
def cab_drawer_shell():
    """Base cabinet whose top drawer is a separate moving part (see drawer_60)."""
    k = K.Kit(); w = 60
    k.box("black", 6, -w / 2, 0, 56, w / 2, 10)
    k.box("wood_dark", 0, -w / 2, 10, 58, w / 2, 68); k.box("wood_dark", 0, -w / 2, 68, 2, w / 2, 87)
    for y in (-w / 2, w / 2 - 2):
        k.box("wood_dark", 0, y, 68, 58, y + 2, 87)
    k.box("laminate", -1, -w / 2, 87, 62, w / 2, 91); k.box("laminate", -1, -w / 2, 91, 1.5, w / 2, 101)
    k.box("wood_light", 58, -w / 2 + 1.5, 12, 59.6, w / 2 - 1.5, 68); k.box("chrome", 59.6, w / 2 - 6.8, 52, 61.5, w / 2 - 5.2, 62)
    return k


@prop
def drawer_60():
    """Sliding drawer, origin at the back-centre of its front panel's closed position (slides along +X)."""
    k = K.Kit()
    k.box("wood_light", 0, -28.5, 0, 1.6, 28.5, 15); k.box("chrome", 1.6, -5, 6.5, 3.5, 5, 8)
    k.box("wood_plain" if False else "wood_light", -50, -26, 1, 0, 26, 2)
    for y in (-26, 25):
        k.box("wood_light", -50, y, 1, 0, y + 1, 12)
    k.box("wood_light", -50, -26, 1, -49, 26, 12)
    k.box("steel", -40, -18, 2, -12, -14, 3); k.box("steel", -42, -8, 2, -10, -5, 3); k.box("black", -38, 4, 2, -14, 16, 4)
    return k


@prop
def cab_sink_90():
    k = base_cabinet(90, 2, False)
    k.box("steel", 8, -34, 88, 52, 34, 91.6)
    k.box("black", 11, -31, 91.2, 49, 31, 91.8)                                     # dark basin
    k.tube("chrome", (5, 0, 91), (5, 0, 112), 1.3); k.tube("chrome", (5, 0, 112), (24, 0, 116), 1.1); k.tube("chrome", (24, 0, 116), (24, 0, 111), 1.1)
    for y in (-10, 10):
        k.cyl("chrome", 5, y, 91.5, 2.2, 5, 8)
    return k


@prop
def cab_upper_90():
    k = K.Kit(); w = 90
    k.box("wood_dark", 0, -w / 2, 0, 32, w / 2, 76)
    for i in range(2):
        y = -w / 2 + i * 45
        k.box("wood_light", 32, y + 1.5, 1.5, 33.6, y + 43.5, 74.5)
        hy = y + 39 if i == 0 else y + 6
        k.box("chrome", 33.6, hy - 0.8, 6, 35.3, hy + 0.8, 16)
    return k


@prop
def fridge():
    k = K.Kit()
    k.box("enamel_gold", 0, -38, 2, 66, 38, 168)
    k.box("enamel_gold", 66, -37.5, 118, 71, 37.5, 167); k.box("enamel_gold", 66, -37.5, 6, 71, 37.5, 116)
    k.box("chrome", 71, 30, 124, 74, 32.5, 150); k.box("chrome", 71, 30, 80, 74, 32.5, 112)
    k.box("black", 2, -36, 0, 64, 36, 6)
    k.quad("p_kid_drawing", 71.2, -22, 122, 4, 142)
    k.box("plastic_red", 71.2, -10, 140.5, 71.9, -8, 142.5)                         # magnet
    return k


@prop
def stove():
    k = K.Kit()
    k.box("enamel_gold", 0, -38, 2, 64, 38, 90); k.box("black", 2, -36, 0, 62, 36, 4)
    k.box("enamel_gold", 0, -38, 90, 8, 38, 112)                                    # back panel
    for i in range(5):
        k.cyl("black", 8, -26 + i * 13, 102, 2.6, 2.2, 12, pitch=90)
    for (x, y) in ((20, -19), (20, 19), (46, -19), (46, 19)):
        k.torus("black", x, y, 90.6, 8.5, 0.9); k.torus("black", x, y, 90.6, 4.5, 0.9); k.cyl("steel", x, y, 90, 10.5, 0.4, 20)
    k.box("enamel_gold", 64, -36, 18, 66.5, 36, 84); k.box("glass_dark", 66.5, -22, 40, 67, 22, 68)
    k.tube("chrome", (69, -30, 79), (69, 30, 79), 1.0); k.box("chrome", 66, -30, 78, 69, -28, 80); k.box("chrome", 66, 28, 78, 69, 30, 80)
    return k


@prop
def kitchen_table():
    k = K.Kit()                                                                      # centred on its footprint
    k.box("laminate", -38, -60, 72, 38, 60, 76); k.box("chrome", -38.5, -60.5, 72.5, 38.5, 60.5, 75)
    for (x, y) in ((-30, -52), (-30, 52), (30, -52), (30, 52)):
        k.cyl("chrome", x, y, 0, 1.6, 72, 8)
    return k


@prop
def kitchen_chair():
    k = K.Kit()
    k.soft("vinyl", 2, -19, 42, 40, 19, 48, 4, 4)
    for (x, y) in ((4, -17), (4, 17), (38, -17), (38, 17)):
        k.cyl("chrome", x, y, 0, 1.2, 43, 6)
    for y in (-17, 17):
        k.tube("chrome", (4, y, 43), (0, y, 86), 1.2, 6)
    k.soft("vinyl", -1.5, -19, 64, 3, 19, 88, 4, 4)
    return k


@prop
def wall_phone():
    """Wall-mounted rotary phone; back at x=0, centred."""
    k = K.Kit()
    k.soft("plastic_beige", 0, -10, -11, 6, 10, 11, 3, 2)
    k.cyl("plastic_beige", 6, 0, -2, 6.5, 1.2, 18, pitch=90); k.cyl("black", 7.2, 0, -2, 3, 0.3, 12, pitch=90)
    for i in range(10):
        a = math.radians(40 + i * 28)
        k.cyl("black", 7.2, math.cos(a) * 4.8, -2 + math.sin(a) * 4.8, 0.7, 0.2, 6, pitch=90)
    k.soft("plastic_beige", 6, -4, 6, 11, 4, 11, 3, 3)                              # handset
    k.soft("plastic_beige", 6, -11, 4, 12, -4, 10, 3, 3); k.soft("plastic_beige", 6, 4, 4, 12, 11, 10, 3, 3)
    pts = [(4 + 1.6 * math.cos(i * 1.3), -9 + 1.6 * math.sin(i * 1.3), -11 - i * 1.2) for i in range(44)]   # coiled cord
    for a, b in zip(pts[:-1], pts[1:]):
        k.tube("plastic_beige", a, b, 0.35, 4)
    return k


# ---------------- bathroom ----------------
@prop
def bathtub():
    k = K.Kit()                                                                      # 152 long (along Y), 76 deep
    k.box("enamel", 0, -76, 0, 76, 76, 12)
    k.box("enamel", 0, -76, 12, 8, 76, 48); k.box("enamel", 68, -76, 12, 76, 76, 48)
    k.box("enamel", 8, -76, 12, 68, -66, 48); k.box("enamel", 8, 66, 12, 68, 76, 48)
    k.tube("chrome", (30, -74, 62), (30, -64, 62), 1.6); k.cyl("chrome", 30, -75, 72, 3, 2, 10, roll=90)
    return k


@prop
def toilet():
    k = K.Kit()
    k.box("enamel", 0, -24, 38, 20, 24, 78); k.box("enamel", -0.5, -25, 78, 21, 25, 81)        # tank and lid
    k.revolve("enamel", [(0.1, 0), (13, 0), (12, 14), (17, 30), (20, 38), (20, 40)], 20, cx=42)
    k.cyl("enamel", 42, 0, 40, 21, 2.2, 22); k.box("enamel", 16, -12, 0, 30, 12, 38)
    k.box("chrome", 20, -22, 70, 21.5, -16, 72)
    return k


@prop
def vanity():
    k = K.Kit(); w = 76
    k.box("wood_light", 0, -w / 2, 8, 50, w / 2, 78); k.box("black", 4, -w / 2, 0, 46, w / 2, 8)
    k.box("enamel", -1, -w / 2 - 1, 78, 53, w / 2 + 1, 82)
    k.box("black", 12, -20, 81.7, 42, 20, 82.2)
    for i in range(2):
        y = -w / 2 + i * w / 2
        k.box("wood_light", 50, y + 1.5, 10, 51.5, y + w / 2 - 1.5, 76); k.sphere("chrome", 53, y + (w / 2 - 6 if i == 0 else 6), 60, 1.5, 4)
    k.tube("chrome", (6, 0, 82), (6, 0, 96), 1.2); k.tube("chrome", (6, 0, 96), (18, 0, 97), 1.0)
    for y in (-8, 8):
        k.cyl("chrome", 6, y, 82, 2, 4, 8)
    return k


@prop
def medicine_cabinet():
    k = K.Kit()
    k.box("steel", 0, -22, -30, 3, 22, 30); k.box("mirror", 3, -20.5, -28.5, 3.3, 20.5, 28.5)
    return k


@prop
def towel_bar():
    k = K.Kit()
    k.tube("chrome", (5, -30, 0), (5, 30, 0), 0.9)
    for y in (-30, 30):
        k.box("chrome", 0, y - 1.5, -1.5, 6, y + 1.5, 1.5)
    k.soft("fabric_cream", 3.5, -20, -48, 6.8, 18, 1.5, 4, 2)
    return k


@prop
def shower_curtain():
    from props_furniture import drape
    return drape(80, 175, "fabric_white", 14, 4)


# ---------------- toys and electronics ----------------
@prop
def toy_robot():
    k = K.Kit()                                                                      # 24 cm tin robot, centred, faces +X
    k.box("plastic_grey", -4, -5.5, 6, 4, 5.5, 16)
    k.box("plastic_red", 4, -3.5, 9, 4.5, 3.5, 14)
    k.box("plastic_grey", -3, -4, 17, 3, 4, 23); k.cyl("chrome", 0, 0, 16, 1.5, 1.2, 8)
    for y in (-2, 2):
        k.cyl("lamp_dim", 3, y, 20.5, 0.9, 0.5, 8, pitch=90)
    k.tube("chrome", (0, 0, 23), (0, 0, 26), 0.25, 4); k.sphere("plastic_red", 0, 0, 26.4, 0.8, 4)
    for y in (-7, 7):
        k.box("plastic_blue", -1.5, y - 1.2, 8, 1.5, y + 1.2, 15); k.sphere("plastic_red", 0, y, 7, 1.5, 4)
    for y in (-3, 3):
        k.box("plastic_blue", -2, y - 1.8, 0, 3, y + 1.8, 6)
    return k


@prop
def toy_blocks():
    k = K.Kit()
    for (x, y, z, c, r) in ((0, 0, 0, "plastic_red", 0), (5.5, 1, 0, "plastic_blue", 20), (2, 6, 0, "plastic_yellow", -15),
                            (2.5, 1.5, 5, "plastic_green", 35), (10, -6, 0, "plastic_yellow", 60)):
        k.obox(c, x, y, z + 2.5, 5, 5, 5, yaw=r)
    return k


@prop
def toy_ball():
    k = K.Kit(); k.sphere("plastic_red", 0, 0, 9, 9, 8); k.torus("plastic_yellow", 0, 0, 9, 9.05, 0.5); return k


@prop
def teddy():
    k = K.Kit()
    k.sphere("fabric_brown", 0, 0, 11, 9, 6, sz=1.15); k.sphere("fabric_brown", 0, 0, 25, 7, 6)
    for y in (-5.5, 5.5):
        k.sphere("fabric_brown", 0, y, 31, 2.6, 4); k.sphere("fabric_brown", 6, y * 1.1, 4, 4, 5); k.sphere("fabric_brown", 3, y * 1.9, 15, 3.4, 5)
    k.sphere("fabric_cream", 5.5, 0, 23.5, 3, 5)
    return k


@prop
def toy_car():
    k = K.Kit()
    k.soft("plastic_blue", -7, -3, 1.2, 7, 3, 4, 3, 2); k.soft("plastic_blue", -3, -2.6, 3.6, 3.5, 2.6, 6, 3, 2)
    for x in (-4.5, 4.5):
        for y in (-3.2, 3.2):
            k.cyl("rubber", x, y - 0.5 if y < 0 else y - 0.5, 1.4, 1.4, 1, 10, roll=-90)
    return k


@prop
def boombox():
    k = K.Kit()                                                                      # cassette player, back at x=0
    k.box("plastic_grey", 0, -24, 0, 11, 24, 24)
    for y in (-15.5, 15.5):
        k.cyl("black", 11, y, 10, 7, 0.5, 20, pitch=90); k.cyl("chrome", 11.5, y, 10, 2.2, 0.3, 12, pitch=90)
    k.box("black", 11, -7, 5, 11.4, 7, 15); k.box("plastic_beige", 11.4, -5, 8, 11.6, 5, 12)     # cassette door and tape
    for i in range(5):
        k.box("chrome", 2, -8 + i * 3.4, 24, 6, -5.4 + i * 3.4, 25)                              # piano keys
    k.box("black", 11, -22, 18.5, 11.3, 22, 22)                                                  # tuner strip
    k.tube("chrome", (3, -24, 24), (3, -24, 31), 0.6, 6); k.tube("chrome", (3, 24, 24), (3, 24, 31), 0.6, 6); k.tube("chrome", (3, -24, 31), (3, 24, 31), 0.8, 6)
    k.tube("chrome", (1.5, 20, 24), (-6, 20, 62), 0.3, 4)
    return k


@prop
def vhs_stack():
    k = K.Kit()
    for i, lab in enumerate(("vhs_xmas", "vhs_bday", "vhs_blank")):
        dy = (i * 37) % 5 - 2
        k.box("black", 0, -9.5 + dy, i * 2.6, 10.5, 9.5 + dy, i * 2.6 + 2.5)
        k.quad("p_" + lab, 10.6, -7.5 + dy, i * 2.6 + 0.5, 7.5 + dy, i * 2.6 + 2.1)
    return k


# ---------------- fixtures ----------------
@prop
def ceiling_light():
    """Flush dome light; origin at the ceiling, hangs down."""
    k = K.Kit()
    k.cyl("brass", 0, 0, -2.5, 17, 2.5, 24)
    k.sphere("lamp_on", 0, 0, -3, 15, 6, sz=0.45)
    return k


@prop
def ceiling_light_off():
    k = K.Kit()
    k.cyl("brass", 0, 0, -2.5, 17, 2.5, 24); k.sphere("lamp_on", 0, 0, -3, 15, 6, sz=0.45)
    return k


@prop
def light_switch():
    k = K.Kit()
    k.box("plastic_beige", 0, -3.5, -5.7, 0.5, 3.5, 5.7); k.box("plastic_beige", 0.5, -0.5, -1.2, 1.4, 0.5, 0.4)
    return k


@prop
def outlet():
    k = K.Kit()
    k.box("plastic_beige", 0, -3.5, -5.7, 0.5, 3.5, 5.7)
    for z in (-2.2, 2.2):
        k.box("black", 0.5, -1.2, z - 0.7, 0.6, -0.8, z + 0.7); k.box("black", 0.5, 0.8, z - 0.7, 0.6, 1.2, z + 0.7)
    return k


@prop
def vent():
    k = K.Kit()
    k.box("white", 0, -18, 0, 0.8, 18, 12)
    for i in range(7):
        k.box("black", 0.8, -16, 1.4 + i * 1.5, 0.9, 16, 2.2 + i * 1.5)
    return k


@prop
def handrail_3m():
    """Wall handrail, 300 long along +X at its own height; brackets every metre. Tilt it when placing."""
    k = K.Kit()
    k.tube("rail", (0, 6, 0), (300, 6, 0), 2.2, 10)
    for x in (20, 150, 280):
        k.tube("brass", (x, 0, -4), (x, 6, -1), 0.7, 6)
    return k


@prop
def doormat():
    k = K.Kit(); k.box("fabric_brown", -25, -40, 0, 25, 40, 1.4); return k


@prop
def coat_hooks():
    k = K.Kit()
    k.box("wood_dark", 0, -40, -5, 2, 40, 5)
    for y in (-28, 0, 28):
        k.tube("brass", (2, y, 0), (7, y, 0), 0.7, 6); k.tube("brass", (7, y, 0), (9, y, 5), 0.7, 6)
    k.soft("fabric_green", 3, -37, -78, 13, -18, 3, 4, 3)                           # a jacket left behind
    return k


@prop
def vhs_tape():
    k = K.Kit()
    k.box("black", -5.2, -9.4, 0, 5.2, 9.4, 2.5); k.quad("p_vhs_xmas", 5.3, -7.5, 0.4, 7.5, 2.1)
    return k
