"""Lived-in clutter: the family left mid-day and never came back to tidy. Same conventions as props_furniture."""
import math, random, unreal
import meshkit as K
from props_furniture import prop


def paper(pr, w, h):
    """A sheet lying flat, centred (for tables and floors)."""
    k = K.Kit(); k.box("paper", -h / 2, -w / 2, 0, h / 2, w / 2, 0.15); k.decal_top("p_" + pr, -h / 2, -w / 2, h / 2, w / 2, 0.2); return k


@prop
def fridge_notes():
    """Notes, lists and magnets; back at x=0 (the fridge door), origin at the floor."""
    k = K.Kit()
    for (pr, y, z, w, h, mag) in (("note_grocery", -24, 74, 14, 18, "plastic_red"), ("note_chores", -4, 82, 16, 20, "plastic_blue"),
                                  ("note_numbers", 16, 76, 14, 17, "plastic_yellow"), ("note_mom", 12, 124, 15, 19, "plastic_green")):
        k.quad("p_" + pr, 0.3, y - w / 2, z, y + w / 2, z + h); k.cyl(mag, 0.3, y, z + h - 2, 1.4, 0.7, 8, pitch=90)
    for i, c in enumerate(("plastic_red", "plastic_yellow", "plastic_blue", "plastic_green", "plastic_red")):   # alphabet magnets
        k.box(c, 0.2, -28 + i * 5, 104 + (i * 7) % 5, 1.0, -25 + i * 5, 108 + (i * 7) % 5)
    return k


@prop
def note_mom():
    k = K.Kit(); k.box("paper", 0, -7.5, 0, 0.2, 7.5, 19); k.quad("p_note_mom", 0.3, -7.5, 0, 7.5, 19); return k


@prop
def calendar_wall():
    k = K.Kit(); k.quad("p_calendar_nov", 0.3, -17, -21, 17, 21); k.cyl("steel", 0.3, 0, 20, 0.5, 0.8, 6, pitch=90); return k


@prop
def homework():
    return paper("homework", 21, 28)


@prop
def magazine():
    return paper("magazine", 21, 27)


@prop
def bed_unmade():
    k = K.Kit()                                                              # covers thrown back, pillow knocked sideways
    k.box("wood_dark", 0, -50, 0, 4, 50, 95); k.box("wood_dark", 196, -50, 0, 200, 50, 50)
    k.box("wood_dark", 4, -50, 22, 196, -47, 34); k.box("wood_dark", 4, 47, 22, 196, 50, 34)
    k.soft("fabric_white", 5, -47, 26, 195, 47, 50, iters=3)
    c = K.Kit()
    c.soft("quilt", 95, -56, 44, 196, 30, 60, 6, 3); c.soft("quilt", 70, 10, 44, 130, 58, 68, 6, 3); c.soft("quilt", 150, 30, 20, 198, 62, 52, 5, 3)
    c.noise(5, 0.05, 3)
    k.add(c)
    k.add(K.Kit().soft("fabric_white", -16, -22, 0, 16, 22, 13, 5, 7), K.T(40, -12, 49, yaw=38, roll=8))
    return k


@prop
def dishes():
    k = K.Kit()
    for i in range(4):
        k.cyl("enamel", 0, 0, i * 1.3, 11.5 - i * 0.3, 1.1, 18)
    k.cyl("enamel", 22, 6, 0, 7, 6, 14); k.cyl("black", 22, 6, 5.4, 6.2, 0.4, 14)                 # bowl with dregs
    k.tube("steel", (20, 2, 5), (30, -8, 9), 0.35, 4)
    k.cyl("plastic_blue", -18, 10, 0, 4, 9.5, 12); k.torus("plastic_blue", -18, 15, 5, 2.6, 0.6, roll=90)   # mug
    k.cyl("glass", 6, -18, 0, 3.4, 12, 12)
    return k


@prop
def dish_towel():
    k = K.Kit(); k.soft("fabric_red", 0, -12, -34, 2.2, 12, 2, 4, 2); return k


@prop
def shoes():
    k = K.Kit()
    for (x, y, yaw, c) in ((0, 0, 8, "fabric_brown"), (4, 14, -14, "fabric_brown"), (36, -6, 70, "plastic_red"), (30, 20, 100, "plastic_red")):
        s = K.Kit(); s.soft(c, -13, -5, 0, 13, 5, 7, 4, 3); s.soft(c, -13, -4.5, 5, -2, 4.5, 11, 3, 3)
        k.add(s, K.T(x, y, 0, yaw=yaw))
    return k


def cloth_pile(cols, seed):
    r = random.Random(seed); c = K.Kit()
    for i, col in enumerate(cols):
        t = K.Kit(); t.soft(col, -22, -15, 0, 22, 15, 5 + r.uniform(0, 4), 5, 3)
        c.add(t, K.T(r.uniform(-14, 14), r.uniform(-14, 14), i * 2.5, yaw=r.uniform(0, 180), roll=r.uniform(-6, 6)))
    c.noise(2.5, 0.08, seed)
    return c


@prop
def clothes_floor():
    return cloth_pile(["fabric_blue", "fabric_red", "fabric_white"], 2)


@prop
def towel_floor():
    return cloth_pile(["fabric_cream"], 5)


@prop
def laundry_basket():
    k = K.Kit()
    k.revolve("plastic_beige", [(0.1, 0), (20, 0), (24, 30), (25, 32), (23, 32), (19, 2), (0.1, 2)], 18)
    k.add(cloth_pile(["fabric_white", "fabric_green", "fabric_blue", "jazz"], 7), K.T(0, 0, 22))
    return k


@prop
def mail_keys():
    k = K.Kit(); r = random.Random(9)
    for i in range(5):
        k.obox("paper", r.uniform(-4, 4), r.uniform(-4, 4), 0.2 + i * 0.25, 11, 23, 0.2, yaw=r.uniform(-30, 30))
    k.torus("steel", 14, 14, 0.4, 1.6, 0.2)
    for a in (0.3, 0.9, 1.5):
        k.obox("brass", 14 + 4 * math.cos(a), 14 + 4 * math.sin(a), 0.3, 5, 1.2, 0.3, yaw=math.degrees(a))
    return k


@prop
def remote_mug():
    k = K.Kit()
    k.soft("plastic_black", -9, -2.5, 0, 9, 2.5, 2, 3, 2); k.cyl("enamel", 16, 10, 0, 4, 9.5, 12); k.cyl("black", 16, 10, 8.6, 3.5, 0.4, 12)
    return k


@prop
def bath_bits():
    k = K.Kit()
    k.cyl("plastic_blue", 0, 0, 0, 3.5, 9, 10); k.tube("plastic_red", (0, 1, 2), (2, 3, 17), 0.4, 4); k.tube("plastic_green", (0, -1, 2), (-2, -3, 17), 0.4, 4)
    k.cyl("paper", 0, 14, 0, 5.5, 10, 14); k.soft("enamel_pink", -4, -22, 0, 4, -14, 3, 3, 3)
    return k


@prop
def chair_pulled():
    from props_small import kitchen_chair
    return kitchen_chair()
