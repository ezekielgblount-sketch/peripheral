"""Playtest round 1 indoor props: the rooms the bigger house added, the things chores use, and the anomaly twins.
Same rules as props_furniture: origin on the floor, back against x=0, front toward +X, centred on Y (unless noted)."""
import math, random, unreal
import meshkit as K
from props_furniture import prop, legs, frame, drape


@prop
def dining_table():
    k = K.Kit()                                                              # centred on its footprint, 190 x 100
    k.box("oak", -50, -95, 71, 50, 95, 76); k.box("oak", -42, -87, 62, 42, 87, 71)
    for (x, y) in ((-42, -87), (-42, 80), (35, -87), (35, 80)):
        k.box("oak", x, y, 0, x + 7, y + 7, 62)
    k.box("fabric_burgundy", -16, -70, 76, 16, 70, 76.4)                     # table runner
    return k


@prop
def washer():
    k = K.Kit()
    k.box("enamel", 0, -34, 0, 66, 34, 92); k.box("enamel", 0, -34, 92, 12, 34, 108)
    k.box("plastic_grey", 12, -30, 92, 13, 30, 105); k.box("enamel", 14, -30, 92, 62, 30, 93.5)
    for y in (-20, -6, 10):
        k.cyl("chrome", 12.5, y, 99, 2.4, 2, 12, pitch=90)
    return k


@prop
def dryer():
    k = K.Kit()
    k.box("enamel", 0, -34, 0, 66, 34, 92); k.box("enamel", 0, -34, 92, 12, 34, 108)
    k.box("plastic_grey", 12, -30, 92, 13, 30, 105)
    k.cyl("enamel", 66, 0, 48, 23, 2.5, 24, pitch=90); k.cyl("glass_dark", 68, 0, 48, 17, 1, 24, pitch=90)
    k.cyl("chrome", 12.5, 14, 99, 2.8, 2, 12, pitch=90)
    return k


@prop
def laundry_shelf():
    k = K.Kit()                                                              # wall shelf over the machines, centre at the origin
    k.box("white", 0, -70, 0, 28, 70, 2.5)
    for y in (-60, 60):
        k.box("white", 0, y - 1.5, -18, 2, y + 1.5, 0); k.box("white", 0, y - 1.5, -2, 24, y + 1.5, 0)
    k.box("plastic_orange", 6, -52, 2.5, 20, -34, 30); k.cyl("plastic_blue", 13, -18, 2.5, 7, 24, 12); k.box("plastic_white", 5, 6, 2.5, 22, 30, 22)
    k.box("cardboard", 4, 38, 2.5, 22, 58, 16)
    return k


@prop
def bulb_box():
    k = K.Kit(); k.box("plastic_yellow", -4, -6.5, 0, 4, 6.5, 12); k.box("plastic_blue", -4.1, -6.6, 3, 4.1, 6.6, 7); return k


@prop
def bed_double():
    k = K.Kit()                                                              # parents' bed: oak headboard at x=0
    k.box("oak", 0, -82, 0, 5, 82, 118); k.box("oak", 5, -70, 60, 6, 70, 110); k.box("oak", 203, -82, 0, 208, 82, 58)
    k.box("oak", 5, -82, 20, 203, -78, 36); k.box("oak", 5, 78, 20, 203, 82, 36)
    k.soft("fabric_white", 6, -78, 26, 202, 78, 54, iters=3)
    k.soft("fabric_mauve", 62, -84, 30, 204, 84, 60, iters=4)
    k.soft("fabric_sage", 150, -84, 56, 204, 84, 63, iters=3)                # folded throw at the foot
    for y in (-40, 40):
        k.soft("fabric_white", 10, y - 30, 52, 50, y + 30, 68, iters=7)
    return k


@prop
def nightstand():
    k = K.Kit()
    k.box("oak", 0, -22, 6, 40, 22, 56); k.box("oak", -1, -24, 56, 42, 24, 59)
    legs(k, "oak", 1, -21, 39, 21, 6, 4)
    for z in (12, 34):
        k.box("wood_light", 40, -19, z, 41.2, 19, z + 19); k.sphere("brass", 43, 0, z + 9.5, 1.5, 4)
    return k


@prop
def bed_sibling():
    k = K.Kit()                                                              # white metal twin bed, lavender cover
    for y in (-50, 46):
        k.cyl("enamel", 2, y + 2, 0, 2, 100, 8); k.cyl("enamel", 198, y + 2, 0, 2, 62, 8)
    for z in (60, 78, 96):
        k.tube("enamel", (2, -48, z), (2, 48, z), 1.2, 6)
    k.tube("enamel", (198, -48, 58), (198, 48, 58), 1.2, 6)
    k.box("enamel", 4, -50, 24, 196, 50, 30)
    k.soft("fabric_white", 5, -47, 28, 195, 47, 50, iters=3); k.soft("fabric_lav", 52, -50, 32, 196, 50, 56, iters=4)
    k.soft("fabric_white", 10, -30, 48, 46, 30, 62, iters=7); k.soft("plastic_pink", 30, -14, 58, 50, 14, 70, iters=5)
    return k


@prop
def bed_made():
    k = K.Kit()                                                              # Jack's bed, made: same frame as bed_unmade
    k.box("wood_dark", 0, -50, 0, 4, 50, 95); k.box("wood_dark", 196, -50, 0, 200, 50, 50)
    k.box("wood_dark", 4, -50, 22, 196, -47, 34); k.box("wood_dark", 4, 47, 22, 196, 50, 34)
    k.soft("fabric_white", 5, -47, 26, 195, 47, 50, iters=3)
    k.soft("quilt", 50, -53, 30, 197, 53, 56, iters=3)
    k.soft("fabric_white", 10, -30, 48, 46, 30, 63, iters=7)
    return k


@prop
def sewing_table():
    k = K.Kit()
    k.box("wood_light", 0, -60, 70, 50, 60, 73); legs(k, "wood_light", 2, -58, 48, 58, 70, 4)
    k.box("enamel", 12, -22, 73, 30, 22, 79); k.box("enamel", 14, 8, 79, 28, 22, 104); k.box("enamel", 14, -22, 96, 28, 22, 104)
    k.box("enamel", 16, -22, 84, 26, -14, 96); k.cyl("chrome", 21, 24, 96, 5, 2, 12, roll=90)
    k.soft("floral_red", 26, -50, 73, 48, -18, 77, 3, 2); k.cyl("plastic_red", 40, 40, 73, 3, 5, 10); k.cyl("plastic_blue", 34, 48, 73, 3, 5, 10)
    return k


@prop
def fabric_bolts():
    k = K.Kit(); r = random.Random(4)                                        # open shelf of folded fabric
    k.box("white", 0, -45, 0, 3, 45, 150)
    for z in (0, 37, 74, 111, 147):
        k.box("white", 0, -45, z, 36, 45, z + 3)
    for y in (-45, 42):
        k.box("white", 0, y, 0, 36, y + 3, 150)
    keys = ["fabric_red", "fabric_blue", "fabric_green", "quilt", "floral_red", "fabric_cream", "fabric_mauve", "fabric_lav", "fabric_butter"]
    for i in range(4):
        z, y = 3 + i * 37, -41
        while y < 34:
            w, h = r.uniform(10, 16), r.uniform(18, 30)
            k.soft(r.choice(keys), 5, y, z, 33, y + w, z + h, 3, 2); y += w + 0.6
    return k


@prop
def shower_curtain_mauve():
    return drape(150, 178, "fabric_mauve", 22, 4)


@prop
def shower_curtain_blue():
    return drape(150, 178, "fabric_blue", 22, 4)


@prop
def bath_mat_mauve():
    k = K.Kit(); k.soft("fabric_mauve", -28, -42, 0, 28, 42, 2.4, 4, 2); return k


@prop
def towel_mauve():
    k = K.Kit()                                                              # towel bar, centre at the origin
    k.tube("chrome", (5, -30, 0), (5, 30, 0), 0.9)
    for y in (-30, 30):
        k.box("chrome", 0, y - 1.5, -1.5, 6, y + 1.5, 1.5)
    k.soft("fabric_mauve", 3.5, -22, -50, 6.8, 20, 1.5, 4, 2)
    return k


def machine(blink):
    k = K.Kit()                                                              # answering machine with a message light
    k.box("plastic_black", -8, -11, 0, 8, 11, 4.5); k.box("plastic_grey", -5, -8, 4.5, 2, 2, 5)
    for y in (4, 7):
        k.box("plastic_grey", -4, y, 4.5, -1, y + 2, 5.1)
    k.box("lamp_blink" if blink else "lamp_led", 4, 6, 4.5, 6, 8, 5.2)
    k.box("paper", 3, -8, 4.5, 6.5, 0, 4.6)
    return k


@prop
def answering_machine():
    return machine(False)


@prop
def answering_machine_new():
    return machine(True)


def hooks(coats):
    k = K.Kit()                                                              # coat rail, centre at the origin
    k.box("oak", 0, -40, -5, 2, 40, 5)
    for y in (-28, 0, 28):
        k.tube("brass", (2, y, 0), (7, y, 0), 0.7, 6); k.tube("brass", (7, y, 0), (9, y, 5), 0.7, 6)
    k.soft("fabric_green", 3, -38, -80, 13, -18, 3, 4, 3)
    if coats > 1:
        k.soft("fabric_navy", 3, 18, -96, 14, 40, 3, 4, 3); k.soft("fabric_navy", 4, 14, -40, 12, 20, -2, 3, 3)
    return k


@prop
def coats_one():
    return hooks(1)


@prop
def coats_two():
    return hooks(2)


def clock_face(k, x, r, hour, minute, key="enamel"):
    """Dial facing +X with its centre at the kit origin: hour marks and two hands."""
    k.tube(key, (x, 0, 0), (x + 0.3, 0, 0), r, 28)
    for i in range(12):
        a = math.radians(i * 30)
        k.obox("black", x + 0.4, r * 0.86 * math.sin(a), r * 0.86 * math.cos(a), 0.25, 0.06 * r, 0.2 * r if i % 3 == 0 else 0.13 * r, roll=-i * 30)
    for (ang, length, wd) in (((hour % 12 + minute / 60.0) * 30, r * 0.5, 0.09 * r), (minute * 6, r * 0.78, 0.06 * r)):
        a = math.radians(ang)
        k.obox("black", x + 0.55, 0.5 * length * math.sin(a), 0.5 * length * math.cos(a), 0.3, wd, length, roll=-ang)
    k.tube("black", (x + 0.3, 0, 0), (x + 0.9, 0, 0), 0.08 * r, 8)


def wall_clock_at(hour, minute):
    k = K.Kit(); k.tube("oak", (0, 0, 0), (2.4, 0, 0), 16, 28); clock_face(k, 2.4, 13.6, hour, minute); return k


def mantel_clock_at(hour, minute):
    k = K.Kit()                                                              # camel-back mantel clock, origin under its middle
    k.box("cherry", -6, -20, 0, 6, 20, 5); k.soft("cherry", -5, -18, 4, 5, 18, 14, 4, 2)
    k.cyl("cherry", -5, 0, 14, 11, 10, 24, pitch=90)
    t = K.Kit(); clock_face(t, 5, 8.2, hour, minute, "enamel_gold"); k.add(t, K.T(0, 0, 14))
    k.torus("brass", 5.2, 0, 14, 8.6, 0.6, pitch=90)
    return k


@prop
def clock_kitchen():
    return wall_clock_at(2, 41)


@prop
def clock_den():
    return wall_clock_at(2, 53)


@prop
def clock_wall_same():
    return wall_clock_at(3, 17)


@prop
def clock_mantel():
    return mantel_clock_at(2, 47)


@prop
def clock_mantel_same():
    return mantel_clock_at(3, 17)


@prop
def banner_thankfu():
    k = K.Kit(); k.print_quad("p_banner_thankfu", 0, -80, -15, 80, 15); return k


@prop
def frame_family_c():
    return frame("photo_family_c", 36, 28)                                   # the same photo: everyone has their back to the camera


@prop
def kid_drawing_b():
    k = K.Kit(); k.quad("p_kid_drawing_b", 0.3, -14, -11, 14, 11); return k   # one more stick figure than before


@prop
def height_marks_b():
    k = K.Kit(); k.quad("p_height_marks_b", 0.15, -6, 0, 6, 110); return k    # a new mark above Jack's last one


def magnets(moved):
    k = K.Kit(); r = random.Random(3)                                         # letter magnets on the fridge door, centre at the origin
    cols = ["plastic_red", "plastic_blue", "plastic_yellow", "plastic_green"]
    spots = [(-12, 8), (-6, 9), (0, 7), (6, 9), (12, 8), (-9, 1), (-2, 0), (5, 1), (11, -1)]
    for i, (y, z) in enumerate(spots):
        if moved and i == 6:
            y, z = 4, -38                                                     # one has slid a long way down the door
        k.obox(cols[i % 4], 0.4, y, z, 0.8, 4.0, 4.6, roll=r.uniform(-18, 18))
    return k


@prop
def fridge_magnets():
    return magnets(False)


@prop
def fridge_magnets_b():
    return magnets(True)


@prop
def border_1m_space():
    k = K.Kit(); k.quad("p_border_space", 0.25, -50, 0, 50, 12.5); return k


@prop
def plate():
    k = K.Kit(); k.cyl("enamel", 0, 0, 0, 11.5, 1.1, 18); k.cyl("enamel_gold", 0, 0, 1.1, 7.5, 0.2, 16); return k


@prop
def plate_dirty():
    k = K.Kit(); k.cyl("enamel", 0, 0, 0, 11.5, 1.1, 18); k.cyl("pumpkin", 2, 1, 1.1, 5.5, 0.25, 9); k.cyl("fabric_brown", -3, -2, 1.1, 3.2, 0.3, 7); return k


@prop
def dish_rack():
    k = K.Kit()
    k.box("plastic_white", -17, -22, 0, 17, 22, 1.5)
    for y in range(-18, 20, 6):
        k.tube("chrome", (-13, y, 1.5), (-13, y, 12), 0.35, 5); k.tube("chrome", (13, y, 1.5), (13, y, 9), 0.35, 5)
    return k


@prop
def furnace():
    k = K.Kit()
    k.box("steel", 0, -30, 0, 70, 30, 140); k.box("metal_dark", 70, -24, 20, 71, 24, 70); k.cyl("steel", 35, 0, 140, 10, 96, 12)
    k.box("steel", 10, 30, 90, 60, 110, 130)
    return k


@prop
def water_heater():
    k = K.Kit(); k.cyl("enamel", 30, 0, 8, 27, 132, 20); k.cyl("metal_dark", 30, 0, 0, 24, 8, 16); k.cyl("steel", 30, 0, 140, 5, 96, 8)
    k.box("plastic_grey", 55, -7, 30, 58, 7, 48); k.tube("copper", (30, 14, 140), (30, 14, 180), 1.2, 6)
    return k


@prop
def shelf_metal():
    k = K.Kit(); r = random.Random(8)                                         # steel storage shelving with boxes and tins
    for (x, y) in ((0, -60), (0, 57), (42, -60), (42, 57)):
        k.box("metal_dark", x, y, 0, x + 3, y + 3, 180)
    for z in (8, 64, 120, 176):
        k.box("steel", 0, -60, z, 45, 60, z + 2.5)
    for z in (10.5, 66.5, 122.5):
        y = -56
        while y < 36:
            w = r.uniform(22, 40); h = r.uniform(18, 44)
            k.box(r.choice(["cardboard", "cardboard", "plastic_grey", "plastic_blue"]), 4, y, z, 40, y + w, z + h); y += w + 3
    return k


@prop
def holiday_bins():
    k = K.Kit()                                                               # stacked decoration tubs: red and green lids
    for i, (body, lid) in enumerate((("plastic_clear", "plastic_red"), ("plastic_clear", "plastic_green"), ("plastic_clear", "plastic_red"))):
        z = i * 36
        k.box(body, 0, -32, z, 46, 32, z + 32); k.box(lid, -1, -33, z + 32, 47, 33, z + 36)
        k.box("fabric_red" if i % 2 == 0 else "fabric_green", 4, -28, z + 2, 42, 28, z + 22)
        k.box("paper", 46.1, -12, z + 12, 46.3, 12, z + 22)
    return k


@prop
def tv_tray():
    k = K.Kit(); k.box("wood_light", -20, -28, 60, 20, 28, 62)
    for s in (-1, 1):
        k.tube("wood_light", (-16, s * 24, 0), (16, s * 24, 60), 1.4, 6); k.tube("wood_light", (16, s * 24, 0), (-16, s * 24, 60), 1.4, 6)
    return k


@prop
def toy_bin():
    k = K.Kit(); r = random.Random(5)
    k.box("plastic_blue", 0, -30, 0, 40, 30, 3)
    for (x0, y0, x1, y1) in ((0, -30, 3, 30), (37, -30, 40, 30), (0, -30, 40, -27), (0, 27, 40, 30)):
        k.box("plastic_blue", x0, y0, 3, x1, y1, 34)
    for i in range(9):
        k.sphere(r.choice(["plastic_red", "plastic_yellow", "plastic_green", "plastic_pink"]), r.uniform(8, 32), r.uniform(-22, 22), r.uniform(24, 36), r.uniform(4, 8), 4)
    return k
