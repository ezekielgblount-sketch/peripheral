"""Props for the five-day story: the ordinary thing the entity resolves into, the shape it has in the corner of the eye,
the opened moving box, Jack's own photo."""
import math, unreal
import meshkit as K
from props_furniture import prop, frame
import props_shadow


@prop
def coat_stand():
    """A hall coat stand with a long dark coat and a hat on top: about the height and outline of a person."""
    k = K.Kit()
    k.cyl("wood_dark", 0, 0, 0, 2.2, 172, 10)
    for a in range(4):
        r = math.radians(a * 90 + 45)
        k.tube("wood_dark", (0, 0, 4), (26 * math.cos(r), 26 * math.sin(r), 0), 1.8, 6)
        k.tube("wood_dark", (0, 0, 160), (11 * math.cos(r), 11 * math.sin(r), 170), 1.1, 6)
    c = K.Kit(); c.soft("fabric_navy", -13, -21, 44, 13, 21, 158, 5, 4, 0.35); c.noise(2.0, 0.05, 2); k.add(c)
    k.soft("fabric_navy", -8, -30, 96, 8, -19, 150, 3, 3); k.soft("fabric_navy", -8, 19, 96, 8, 30, 150, 3, 3)      # sleeves
    k.cyl("fabric_brown", 0, 0, 170, 15, 1.2, 16); k.soft("fabric_brown", -9, -9, 170, 9, 9, 181, 4, 4, 0.4)       # a hat
    return k


@prop
def entity_figure():
    """What stands there when it is only at the edge of sight: a plain dark standing shape, the size of a person."""
    k = props_shadow.figure(False)
    k.keys = ["black"] * len(k.keys)
    return k


@prop
def box_open():
    """A moving box, opened and emptied: flaps out, packing paper left inside."""
    k = K.Kit()
    k.box("cardboard", -22, -30, 0, 22, 30, 1.2)
    for (x0, y0, x1, y1) in ((-22, -30, -21, 30), (21, -30, 22, 30), (-22, -30, 22, -29), (-22, 29, 22, 30)):
        k.box("cardboard", x0, y0, 0, x1, y1, 34)
    k.obox("cardboard", -30, 0, 38, 16, 58, 0.8, pitch=-35); k.obox("cardboard", 30, 0, 38, 16, 58, 0.8, pitch=35)
    k.obox("cardboard", 0, -37, 36, 42, 14, 0.8, roll=40); k.obox("cardboard", 0, 37, 36, 42, 14, 0.8, roll=-40)
    c = K.Kit(); c.soft("paper", -18, -26, 2, 18, 26, 12, 4, 3, 0.4); c.noise(3, 0.08, 5); k.add(c)
    return k


@prop
def frame_jack():
    return frame("photo_school_b", 16, 20, "oak")


@prop
def frame_family_small():
    return frame("photo_family_a", 22, 17, "brass")
