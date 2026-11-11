"""Furniture and large props, built from simple shapes with meshkit. Sizes are real-world cm.
Every prop: origin on the floor, back against x=0, front toward +X, centred on Y (unless noted)."""
import math, unreal
import meshkit as K

REG = {}


def prop(fn):
    REG[fn.__name__] = fn
    return fn


def get(name, rebuild=False):
    """Mesh asset for a prop, built on first use."""
    path = "%s/SM_%s" % (K.MESH_DIR, name)
    if not rebuild and unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.EditorAssetLibrary.load_asset(path)
    return REG[name]().save(name)


LIT = {True: {"lamp_on": "bulb_lit", "lamp_shade": "shade_lit", "glass_dark": "tv_static"},
       False: {"lamp_on": "lamp_off", "lamp_shade": "shade_unlit"}}


def variant(name, on):
    """The same prop with its bulb / shade surfaces lit or unlit (SM_<name>_on / _off), for things the player switches."""
    vn = name + ("_on" if on else "_off")
    path = "%s/SM_%s" % (K.MESH_DIR, vn)
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.EditorAssetLibrary.load_asset(path)
    k = REG[name](); k.keys = [LIT[on].get(x, x) for x in k.keys]
    return k.save(vn)


def legs(k, key, x0, y0, x1, y1, h, t=4):
    for (x, y) in ((x0, y0), (x0, y1 - t), (x1 - t, y0), (x1 - t, y1 - t)):
        k.box(key, x, y, 0, x + t, y + t, h)


def sofa(w, fabric, seats):
    """One-piece sofa: a continuous upholstered body, with cushions that butt up against each other and the arms."""
    k = K.Kit()
    k.box("wood_dark", 6, -w / 2 + 6, 3, 82, w / 2 - 6, 9)
    for (x, y) in ((6, -w / 2 + 6), (6, w / 2 - 11), (78, -w / 2 + 6), (78, w / 2 - 11)):
        k.box("wood_dark", x, y, 0, x + 5, y + 5, 4)
    k.soft(fabric, 0, -w / 2, 8, 86, w / 2, 34, 5, 2, 0.3)                # body: seat platform, front rail
    k.soft(fabric, 0, -w / 2, 8, 20, w / 2, 82, 5, 2, 0.3)                # body: back
    for s_ in (-1, 1):
        y0, y1 = sorted((s_ * (w / 2 - 20), s_ * w / 2))
        k.soft(fabric, 0, y0, 8, 88, y1, 62, 5, 2, 0.3)                   # arms, part of the body
    sw = (w - 36) / seats
    for i in range(seats):
        y = -w / 2 + 18 + i * sw
        k.soft(fabric, 16, y - 1.5, 31, 89, y + sw + 1.5, 46, 5, 2, 0.35)   # seat cushions overlap a little, so no gaps
        k.soft(fabric, 12, y - 1.5, 42, 30, y + sw + 1.5, 86, 5, 2, 0.35)   # back cushions likewise
    return k


@prop
def couch():
    return sofa(212, "fabric_hunter", 3)


@prop
def armchair():
    return sofa(96, "fabric_burgundy", 1)


@prop
def coffee_table():
    k = K.Kit()
    k.box("wood_dark", 0, -60, 38, 56, 60, 42)
    k.box("wood_dark", 4, -56, 12, 52, 56, 14)
    legs(k, "wood_dark", 2, -58, 54, 58, 38, 5)
    return k


@prop
def side_table():
    k = K.Kit()
    k.box("wood_dark", 0, -25, 51, 50, 25, 55)
    k.box("wood_dark", 3, -22, 38, 47, 22, 51)
    legs(k, "wood_dark", 2, -23, 48, 23, 51, 4)
    return k


@prop
def tv_console():
    k = K.Kit()
    k.box("wood_dark", 0, -70, 8, 45, 70, 12); k.box("wood_dark", 0, -70, 56, 46, 70, 60)
    for y in (-70, -1.5, 67):
        k.box("wood_dark", 0, y, 12, 45, y + 3, 56)
    k.box("wood_dark", 0, -70, 12, 2, 70, 56); k.box("wood_dark", 2, -67, 33, 44, -1.5, 35)
    k.box("wood_dark", 43, 1.5, 12, 45, 67, 56)                                    # right-hand cupboard door
    k.sphere("brass", 46, 8, 36, 1.6, 4)
    legs(k, "wood_dark", 3, -66, 42, 66, 8, 5)
    return k


@prop
def crt_tv():
    k = K.Kit()
    k.box("wood_dark", 0, -34, 0, 46, 34, 50)                                     # wood-grain cabinet
    k.box("black", 46, -32, 3, 48, 32, 48)
    k.sphere("glass_dark", 40, -8, 26, 30, 8, sx=0.36, sy=0.78, sz=0.66)          # curved tube face
    k.box("plastic_grey", 47, 18, 6, 49.5, 31, 46)                                # control panel
    for z in (38, 28):
        k.cyl("plastic_beige", 49.5, 24.5, z, 3.2, 2.5, 14, pitch=90)
    for i in range(6):
        k.box("black", 49.4, 20, 8 + i * 2.2, 49.8, 29, 9 + i * 2.2)             # speaker slots
    k.tube("chrome", (20, -6, 50), (10, -30, 96), 0.4, 5); k.tube("chrome", (20, 6, 50), (10, 30, 96), 0.4, 5)
    k.cyl("black", 20, 0, 50, 5, 2.5, 12)
    return k


@prop
def vcr():
    k = K.Kit()
    k.box("black", 0, -21.5, 0.8, 30, 21.5, 9.5)
    k.box("plastic_grey", 30, -21.5, 0.8, 30.6, 21.5, 9.5)
    k.box("black", 30.5, -17, 5, 30.9, 2, 8)                                       # tape slot
    k.box("lamp_dim", 30.6, 6, 3, 30.9, 14, 5)                                     # clock display
    for y in (-20, 18):
        k.box("rubber", 2, y, 0, 6, y + 2, 0.8); k.box("rubber", 24, y, 0, 28, y + 2, 0.8)
    return k


@prop
def bookshelf():
    k = K.Kit()
    for y in (-40, 38):
        k.box("wood_dark", 0, y, 0, 30, y + 2, 180)
    k.box("wood_dark", 0, -40, 0, 1.2, 40, 180)
    for i, z in enumerate((6, 42, 78, 114, 150, 178)):
        k.box("wood_dark", 0, -38, z, 30, 38, z + 2)
        if i in (1, 2, 4):                                                         # a few shelves still hold books
            k.box("black", 4, -37, z + 2, 24, 30, z + 26)
            k.quad("p_book_spines_a" if i != 2 else "p_book_spines_b", 24.1, -37, z + 2, 30, z + 27)
    return k


@prop
def floor_lamp():
    k = K.Kit()
    k.cyl("brass", 15, 0, 0, 14, 2.5, 20); k.cyl("brass", 15, 0, 2.5, 1.3, 138, 10)
    k.cone("lamp_shade", 15, 0, 132, 20, 13, 30, 20)
    k.sphere("lamp_off", 15, 0, 146, 4, 5)
    return k


@prop
def table_lamp():
    k = K.Kit()
    k.revolve("enamel_avocado", [(0.1, 0), (8, 0), (9, 3), (5, 10), (7, 20), (3, 30), (1.4, 32)], 16)
    k.cone("lamp_shade", 0, 0, 30, 15, 10, 22, 18)
    return k


def carton(w, d, h, label=None, is_open=False):
    """Moving box, centred on its own footprint."""
    k = K.Kit()
    k.box("cardboard", -d / 2, -w / 2, 0, d / 2, w / 2, h)
    if is_open:
        for s in (-1, 1):
            k.obox("cardboard", s * (d / 2 + d * 0.2), 0, h + d * 0.08, d * 0.45, w, 0.6, pitch=-s * 25)
            k.obox("cardboard", 0, s * (w / 2 + d * 0.16), h - d * 0.1, d, d * 0.4, 0.6, roll=s * 62)
        k.box("black", -d / 2 + 1, -w / 2 + 1, h - 0.4, d / 2 - 1, w / 2 - 1, h + 0.2)      # dark inside
        k.soft("paper", -d / 2 + 4, -w / 2 + 4, h - 10, d / 2 - 4, w / 2 - 4, h + 3, 4, 3)  # packing paper
    else:
        k.box("plastic_beige", -d / 2 - 0.15, -3, h - 8, d / 2 + 0.15, 3, h + 0.15)          # packing tape
    if label:
        k.quad("p_" + label, d / 2 + 0.2, -w * 0.38, h * 0.3, w * 0.38, h * 0.3 + w * 0.38)
    return k


@prop
def box_kitchen():
    return carton(46, 46, 40, "label_kitchen")


@prop
def box_jack():
    return carton(50, 40, 36, "label_jack", True)


@prop
def box_living():
    return carton(60, 45, 45, "label_living")


@prop
def box_fragile():
    return carton(40, 40, 32, "label_fragile")


@prop
def box_books():
    return carton(42, 32, 30, "label_books", True)


@prop
def box_misc():
    return carton(56, 40, 40, "label_misc")


@prop
def box_plain():
    return carton(45, 45, 45)


def frame(print_name, w, h, key="wood_dark"):
    """Picture frame, centred on Y and Z, back at x=0 (hang it on a wall)."""
    k = K.Kit()
    for (y0, y1, z0, z1) in ((-w / 2 - 3, w / 2 + 3, h / 2, h / 2 + 3), (-w / 2 - 3, w / 2 + 3, -h / 2 - 3, -h / 2),
                             (-w / 2 - 3, -w / 2, -h / 2, h / 2), (w / 2, w / 2 + 3, -h / 2, h / 2)):
        k.box(key, 0, y0, z0, 2.2, y1, z1)
    k.box("black", 0, -w / 2, -h / 2, 0.8, w / 2, h / 2)
    k.quad("p_" + print_name, 1.0, -w / 2, -h / 2, w / 2, h / 2)
    return k


@prop
def frame_family_a():
    return frame("photo_family_a", 36, 28)


@prop
def frame_family_b():
    return frame("photo_family_b", 36, 28)


@prop
def frame_school():
    return frame("photo_school", 20, 25, "brass")


@prop
def frame_school_b():
    return frame("photo_school_b", 20, 25, "brass")


@prop
def poster_space():
    k = K.Kit(); k.quad("p_poster_space", 0.3, -28, -40, 28, 40); return k


@prop
def poster_shapes():
    k = K.Kit(); k.quad("p_poster_shapes", 0.3, -28, -40, 28, 40); return k


@prop
def kid_drawing():
    k = K.Kit(); k.quad("p_kid_drawing", 0.3, -14, -11, 14, 11); return k


@prop
def wall_clock():
    k = K.Kit()
    k.cyl("wood_dark", 0, 0, 0, 16, 3.5, 28, pitch=90)
    k.quad("p_clock_face", 3.7, -13, -13, 13, 13)
    k.obox("black", 4.0, 0, 3.5, 0.3, 1.2, 8, roll=20); k.obox("black", 4.1, 3, -2, 0.3, 0.8, 11, roll=-120)
    return k


@prop
def rug():
    k = K.Kit(); k.decal_top("p_rug_braided", -90, -135, 90, 135, 0.6); return k


def drape(w, h, key, folds=7, depth=5):
    """Hanging cloth with soft folds: back at x=0, hangs from z=h down to z=0."""
    pts = []
    n = folds * 8
    for i in range(n + 1):
        y = -w / 2 + w * i / n
        pts.append((depth * 0.5 + depth * 0.5 * math.sin(i / 8.0 * 2 * math.pi) + 1.2, y))
    for i in range(n, -1, -1):
        y = -w / 2 + w * i / n
        pts.append((depth * 0.5 + depth * 0.5 * math.sin(i / 8.0 * 2 * math.pi), y))
    k = K.Kit(); k.extrude(key, pts, 0, h)
    return k


@prop
def curtain_living():
    k = drape(60, 190, "fabric_cream")
    return k


@prop
def curtain_bed():
    return drape(45, 150, "fabric_blue", 5)


@prop
def curtain_kitchen():
    return drape(130, 38, "fabric_white", 12, 3)


@prop
def curtain_rod():
    k = K.Kit(); k.tube("brass", (4, -150, 0), (4, 150, 0), 1.1, 8)
    for y in (-150, 150):
        k.sphere("brass", 4, y, 0, 2.4, 4)
    return k


@prop
def bed_twin():
    k = K.Kit()                                               # headboard at x=0, bed runs out along +X
    k.box("oak", 0, -50, 0, 4, 50, 95); k.box("oak", 196, -50, 0, 200, 50, 50)
    k.box("wood_dark", 4, -50, 22, 196, -47, 34); k.box("wood_dark", 4, 47, 22, 196, 50, 34)
    k.soft("fabric_white", 5, -47, 26, 195, 47, 50, iters=3)                         # mattress
    k.soft("jazz", 55, -50, 30, 196, 50, 55, iters=4)                                # blanket
    k.soft("fabric_white", 10, -32, 48, 48, 32, 62, iters=7)                         # pillow
    return k


@prop
def dresser():
    k = K.Kit()
    k.box("wood_dark", 0, -45, 6, 44, 45, 80); k.box("wood_dark", 0, -47, 80, 46, 47, 83)
    legs(k, "wood_dark", 2, -43, 42, 43, 6, 5)
    for i in range(3):
        z = 10 + i * 23
        k.box("wood_light", 44, -42, z, 45.5, 42, z + 21)
        for y in (-22, 22):
            k.sphere("brass", 47, y, z + 10.5, 1.7, 4)
    return k


@prop
def desk():
    k = K.Kit()
    k.box("wood_light", 0, -55, 72, 55, 55, 75)
    k.box("wood_light", 2, 20, 30, 53, 53, 72)
    for i in range(2):
        k.box("wood_dark", 53, 22, 34 + i * 19, 54.5, 51, 51 + i * 19); k.sphere("brass", 56, 36.5, 42.5 + i * 19, 1.6, 4)
    legs(k, "wood_light", 2, -53, 53, 53, 72, 4)
    return k


@prop
def chair_wood():
    k = K.Kit()
    k.box("wood_light", 0, -20, 43, 42, 20, 46)
    legs(k, "wood_light", 0, -20, 42, 20, 43, 3.5)
    k.box("wood_light", 0, -20, 46, 3.5, -16.5, 90); k.box("wood_light", 0, 16.5, 46, 3.5, 20, 90)
    k.box("wood_light", 0.5, -20, 72, 3, 20, 88)
    return k


@prop
def toy_chest():
    k = K.Kit()
    k.box("plastic_blue", 0, -40, 0, 42, 40, 40); k.box("plastic_red", -1, -41, 40, 43, 41, 44)
    return k


@prop
def shelf_wall():
    k = K.Kit()
    k.box("wood_light", 0, -45, 0, 20, 45, 2)
    for y in (-35, 33):
        k.prism_xz("wood_light", [(0, 0), (16, 0), (0, -14)], y, y + 2)
    return k


@prop
def mannequin():
    """178 cm figure for scale in screenshots. Origin at the feet, centred."""
    k = K.Kit()
    for y in (-9, 9):
        k.cyl("skin_grey", 0, y, 0, 6.5, 86, 10)
    k.soft("skin_grey", -11, -19, 84, 11, 19, 148, 4, 5)
    for y in (-24, 24):
        k.cyl("skin_grey", 0, y, 78, 4.5, 66, 8)
    k.cyl("skin_grey", 0, 0, 146, 5, 10, 8)
    k.sphere("skin_grey", 0, 0, 166.5, 11.5, 6, sz=1.0)
    return k
