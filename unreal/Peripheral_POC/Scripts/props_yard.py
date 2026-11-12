"""Playtest round 1 garage and yard props, and the things the outdoor chores use.
Furniture rule as elsewhere (origin on the ground, back at x=0, front +X, centred on Y) unless a prop says otherwise."""
import math, random, unreal
import meshkit as K
from props_furniture import prop, legs


@prop
def mower():
    """Push mower. Origin on the ground under the deck's middle; it is pushed toward +X, the handle rises behind it."""
    k = K.Kit()
    k.soft("plastic_red", -28, -27, 7, 28, 27, 20, 4, 2); k.box("metal_dark", -30, -28, 5, 30, 28, 8)
    k.cyl("plastic_black", -2, 0, 20, 12, 14, 14); k.cyl("plastic_black", -2, 0, 34, 14, 3, 14); k.cyl("plastic_white", 10, -12, 20, 4.5, 9, 10)
    for (x, y) in ((-22, -30), (-22, 30), (22, -30), (22, 30)):
        k.cyl("rubber", x, y - 2 if y < 0 else y - 2, 9, 9, 4, 14, roll=90)
    for s in (-1, 1):
        k.tube("metal_dark", (-26, s * 22, 14), (-88, s * 22, 92), 1.3, 6)
    k.tube("metal_dark", (-88, -22, 92), (-88, 22, 92), 1.5, 6); k.tube("rubber", (-88, -14, 92), (-88, 14, 92), 2.1, 8)
    k.soft("fabric_stripe", -52, -20, 16, -30, 20, 44, 4, 2)                  # grass bag
    return k


@prop
def grass_tall():
    """One square metre of long grass (centre at the origin). The mower swaps it away as it passes."""
    k = K.Kit(); r = random.Random(11)
    for i in range(46):
        x, y = r.uniform(-50, 50), r.uniform(-50, 50)
        k.cone("lawn_tall", x, y, 0, r.uniform(5, 9), 0.4, r.uniform(15, 27), 5, roll=r.uniform(-14, 14), pitch=r.uniform(-14, 14))
    return k


@prop
def trash_bin():
    """Wheeled bin. Origin on the ground under its middle; the handle and wheels are on the -X side."""
    k = K.Kit()
    k.box("plastic_green", -27, -29, 8, 27, 29, 96); k.box("plastic_green", -31, -31, 96, 30, 31, 102)
    k.tube("plastic_green", (-33, -24, 98), (-33, 24, 98), 1.8, 8)
    for y in (-31, 27):
        k.cyl("rubber", -24, y, 10, 10, 4, 14, roll=90)
    k.box("paper", 27.1, -12, 55, 27.3, 12, 75)
    return k


@prop
def trash_bag():
    k = K.Kit(); k.soft("plastic_black", -20, -20, 0, 20, 20, 44, 5, 5, 0.45); k.cone("plastic_black", 0, 0, 40, 7, 3, 12, 8); return k


@prop
def kitchen_bin():
    k = K.Kit(); k.cyl("plastic_white", 0, 0, 0, 16, 52, 14); k.cyl("plastic_white", 0, 0, 52, 17, 3, 14); return k


def mailbox_kit(is_open):
    k = K.Kit()                                                               # on a post; the door faces +X (the house side)
    k.box("fence", -5, -5, 0, 5, 5, 104); k.box("fence", -18, -9, 100, 18, 9, 104)
    k.box("metal_dark", -22, -9, 104, 20, 9, 116); k.cyl("metal_dark", -22, 0, 116, 9, 42, 14, pitch=90)
    if is_open:
        k.box("metal_dark", 20, -9, 103, 38, 9, 104.5); k.box("paper", -4, -6, 105, 24, 6, 108)
    else:
        k.box("metal_dark", 20, -9, 104, 21.5, 9, 124)
    k.box("plastic_red", -2, 9, 112, 12, 10, 115) if not is_open else k.box("plastic_red", -2, 9, 112, 1, 10, 128)      # the flag
    return k


@prop
def mailbox():
    return mailbox_kit(False)


@prop
def mailbox_open():
    return mailbox_kit(True)


@prop
def broom():
    """Push broom, lying angle built in: origin where the head rests on the floor, handle rising toward -X."""
    k = K.Kit()
    k.box("wood_light", -4, -22, 6, 4, 22, 11); k.box("fabric_brown", -3.5, -21, 0, 3.5, 21, 6)
    k.tube("wood_light", (0, 0, 9), (-62, 0, 128), 1.4, 8)
    return k


@prop
def dust_pile():
    k = K.Kit(); r = random.Random(6)
    k.soft("fabric_tan", -26, -22, 0, 26, 22, 3.2, 5, 5, 0.45)
    for i in range(7):
        k.obox(r.choice(["pumpkin", "fabric_brown", "fabric_tan"]), r.uniform(-20, 20), r.uniform(-16, 16), 3.3, 5, 3.2, 0.3, yaw=r.uniform(0, 180))
    return k


@prop
def watering_can():
    k = K.Kit()
    k.cyl("plastic_green", 0, 0, 0, 11, 22, 14); k.tube("plastic_green", (9, 0, 8), (28, 0, 24), 1.8, 8); k.cyl("plastic_green", 28, 0, 22, 4, 2, 10, pitch=60)
    k.torus("plastic_green", -4, 0, 24, 8, 1.2, roll=90)
    return k


@prop
def garden_frame():
    k = K.Kit()                                                               # raised bed, 300 x 110, centred
    for (x0, y0, x1, y1) in ((-55, -150, -51, 150), (51, -150, 55, 150), (-55, -150, 55, -146), (-55, 146, 55, 150)):
        k.box("fence", x0, y0, 0, x1, y1, 24)
    return k


def soil(key):
    k = K.Kit(); c = K.Kit(); c.soft(key, -51, -48.5, 0, 51, 48.5, 21, 5, 3, 0.3); c.noise(2.5, 0.06, 4); k.add(c); return k


@prop
def soil_dry():
    return soil("soil")


@prop
def soil_wet():
    return soil("soil_wet")


@prop
def veg_plants():
    k = K.Kit(); r = random.Random(9)                                         # a metre of garden rows, centred
    for i in range(7):
        x, y = r.uniform(-38, 38), -42 + i * 14
        k.tube("fence", (x, y, 20), (x, y, 62), 0.8, 5)
        for j in range(4):
            k.sphere("leaf", x + r.uniform(-7, 7), y + r.uniform(-5, 5), 30 + j * 9, r.uniform(6, 10), 4, sz=0.6)
        if i % 2 == 0:
            k.sphere("plastic_red", x + 5, y, 44, 3.4, 4)
    return k


@prop
def grill():
    k = K.Kit()                                                               # gas grill on a cart
    for (x, y) in ((4, -30), (4, 28), (44, -30), (44, 28)):
        k.box("metal_dark", x, y, 0, x + 2.5, y + 2.5, 80)
    k.box("metal_dark", 2, -32, 20, 48, 32, 22); k.box("black", 0, -34, 72, 50, 34, 88)
    k.soft("black", 2, -33, 86, 48, 33, 112, 4, 4, 0.4)
    k.tube("chrome", (52, -22, 100), (52, 22, 100), 1.2, 6)
    for y in (-66, 34):
        k.box("wood_light", 8, y, 82, 42, y + 32, 85)
    k.cyl("enamel", 25, 0, 22, 14, 34, 14); k.cyl("enamel", 25, 0, 56, 9, 6, 10)       # propane tank
    for y in (-18, 0, 18):
        k.cyl("plastic_black", 50, y, 79, 2.6, 2.5, 8, pitch=90)
    return k


@prop
def plastic_chair():
    k = K.Kit()                                                               # white stacking patio chair
    k.box("plastic_white", 2, -24, 40, 48, 24, 43)
    for (x, y) in ((4, -22), (4, 20), (44, -22), (44, 20)):
        k.tube("plastic_white", (x, y, 0), (x + (2 if x > 20 else -1), y, 41), 1.8, 6)
    k.box("plastic_white", 0, -24, 43, 3, 24, 86)
    for y in (-25, 23):
        k.box("plastic_white", 2, y, 60, 44, y + 2, 63); k.box("plastic_white", 42, y, 43, 44, y + 2, 62)
    return k


@prop
def patio_table():
    k = K.Kit(); k.cyl("plastic_white", 0, 0, 68, 50, 3, 22); k.cyl("plastic_white", 0, 0, 0, 5, 68, 10); k.cyl("plastic_white", 0, 0, 0, 26, 3, 16); return k


@prop
def shed():
    """Small wooden garden shed, 240 deep x 300 wide. Back at x=0; the door is in the +X face."""
    k = K.Kit()
    k.box("fence", 0, -150, 0, 6, 150, 200); k.box("fence", 0, -150, 0, 240, -144, 200); k.box("fence", 0, 144, 0, 240, 150, 200)
    k.box("fence", 234, -150, 0, 240, -50, 200); k.box("fence", 234, 50, 0, 240, 150, 200); k.box("fence", 234, -50, 195, 240, 50, 200)
    k.box("wood_dark", 236, -50, 2, 240, 50, 195); k.box("metal_dark", 240, 30, 95, 242, 44, 105)
    k.box("fence", 0, -150, -4, 240, 150, 0)
    K.gable_roof(k, -10, 250, -150, 150, 200, ov=12, ov_gable=14, t=6, gable="fence", gable_t=6)
    return k


@prop
def sprinkler():
    k = K.Kit(); k.box("plastic_green", -16, -5, 0, 16, 5, 3); k.tube("metal", (-13, 0, 6), (13, 0, 6), 1.2, 6)
    for x in (-13, 13):
        k.box("plastic_green", x - 1.5, -4, 3, x + 1.5, 4, 8)
    return k


@prop
def hose_coil():
    k = K.Kit()                                                               # garden hose looped on the ground
    for i in range(5):
        k.torus("plastic_green", 0, 0, 2 + i * 2.6, 26 - i * 1.5, 1.5, major=22, minor=6)
    k.tube("plastic_green", (24, 0, 2), (70, 30, 2), 1.5, 6); k.cyl("brass", 70, 30, 0.5, 2, 6, 8, pitch=70)
    return k


@prop
def hose_reel():
    k = K.Kit()                                                               # wall bracket with the hose wound on it (centre at the origin)
    k.box("metal_dark", 0, -6, -10, 3, 6, 10); k.tube("metal_dark", (3, 0, 0), (16, 0, 0), 2, 8)
    for i in range(4):
        k.torus("plastic_green", 5 + i * 3, 0, 0, 20, 1.6, pitch=90, major=22, minor=6)
    return k


@prop
def workbench():
    k = K.Kit()
    k.box("wood_light", 0, -90, 84, 62, 90, 90); k.box("wood_light", 4, -86, 20, 58, 86, 23)
    for (x, y) in ((2, -88), (2, 80), (52, -88), (52, 80)):
        k.box("wood_light", x, y, 0, x + 8, y + 8, 84)
    k.box("metal_dark", 44, 52, 90, 60, 74, 102); k.box("steel", 46, 44, 97, 58, 82, 100)       # vise
    k.box("plastic_red", 10, -70, 90, 34, -30, 106); k.cyl("enamel", 30, 10, 90, 8, 18, 12); k.cyl("plastic_blue", 16, 22, 90, 8, 18, 12)
    return k


@prop
def pegboard():
    k = K.Kit()                                                               # board of hand tools, centre at the origin
    k.box("fabric_tan", 0, -90, -45, 1.5, 90, 45)
    k.obox("steel", 2, -66, 6, 1, 6, 30, roll=0); k.box("wood_light", 1.5, -70, -28, 3.5, -62, -8)                 # hammer
    k.obox("steel", 2, -34, 0, 0.6, 12, 46, roll=22); k.obox("wood_light", 2.2, -42, -22, 2, 10, 14, roll=22)      # hand saw
    for i, y in enumerate((-4, 8, 20, 32)):
        k.obox("steel", 2, y, 8 - i * 2, 0.8, 2.6, 22 - i * 3)                                                    # wrenches
    k.torus("plastic_orange", 3, 62, 10, 16, 1.6, pitch=90)                                                         # extension cord
    k.obox("plastic_yellow", 2.5, 56, -26, 2.5, 30, 5); k.obox("metal_dark", 2, 4, -30, 1, 44, 4)                   # level, pry bar
    return k


def bicycle(frame_key, wheel_r, length):
    k = K.Kit()                                                               # leaning on its stand; runs along Y, centred
    h = wheel_r
    for y in (-length / 2, length / 2):
        k.torus("rubber", 0, y, h, wheel_r - 2, 2, roll=90, major=20, minor=6); k.cyl("steel", -1, y, h, 2.2, 2, 8, pitch=90)
    seat = (0, -length * 0.12, h + wheel_r * 1.25); bar = (0, length * 0.32, h + wheel_r * 1.35); crank = (0, -length * 0.02, h)
    for (a, b) in ((seat, crank), (crank, (0, -length / 2, h)), (seat, (0, -length / 2, h)), (seat, bar), (crank, bar), (bar, (0, length / 2, h))):
        k.tube(frame_key, a, b, 1.4, 6)
    k.soft("black", -5, seat[1] - 12, seat[2], 5, seat[1] + 10, seat[2] + 5, 3, 3); k.tube("chrome", (-20, bar[1], bar[2] + 4), (20, bar[1], bar[2] + 4), 1.1, 6)
    return k


@prop
def bike_adult():
    return bicycle("plastic_blue", 33, 104)


@prop
def bike_kid():
    return bicycle("plastic_red", 24, 78)


@prop
def gas_can():
    k = K.Kit(); k.soft("plastic_red", -11, -15, 0, 11, 15, 28, 3, 3, 0.35); k.tube("plastic_yellow", (4, 8, 28), (14, 14, 38), 1.6, 6); return k


@prop
def paint_cans():
    k = K.Kit()
    for (x, y, z) in ((0, -12, 0), (0, 12, 0), (2, 0, 19)):
        k.cyl("steel", x, y, z, 9, 18.5, 14); k.cyl("enamel", x, y, z + 18.5, 9.2, 0.6, 14)
    return k


@prop
def ladder():
    k = K.Kit()                                                               # leaning on a wall: back at x=0, feet out at +X
    for y in (-20, 20):
        k.tube("steel", (38, y, 0), (4, y, 230), 2, 6)
    for i in range(8):
        f = (i + 1) / 9.0
        k.tube("steel", (38 - 34 * f, -20, 230 * f), (38 - 34 * f, 20, 230 * f), 1.3, 6)
    return k
