"""Props for the lighting pass (track light) and for the loop sequence's anomalies (a door that should not be there,
a wall clock with a separate second hand, the mantel banner and its misspelled twin)."""
import math, unreal
import meshkit as K
from props_furniture import prop


@prop
def track_light():
    """Halogen track: white bar on the ceiling (origin at the ceiling, bar along Y) with three small heads aimed toward +X."""
    k = K.Kit()
    k.box("enamel", -2, -72, -3, 2, 72, 0)
    for y in (-50, 0, 50):
        k.cyl("enamel", 0, y, -7, 1.2, 4, 8)
        k.tube("enamel", (-2, y, -9), (5.5, y, -19), 4.2, 14); k.tube("lamp_on", (5.5, y, -19), (5.9, y, -19.5), 3.6, 14)
    return k


@prop
def false_door():
    """A plain interior door in its casing, flat against a wall (back at x=0, centred, origin at the floor)."""
    k = K.Kit()
    k.box("trim", 0, -52, 0, 2.2, -43, 213); k.box("trim", 0, 43, 0, 2.2, 52, 213); k.box("trim", 0, -52, 204, 2.2, 52, 213)
    k.box("door_wood", 0, -43, 0.6, 1.4, 43, 204)
    for (z0, z1) in ((16, 96), (106, 190)):
        k.box("door_wood", 1.4, -31, z0, 1.9, 31, z1)
    k.cyl("brass", 1.4, 34, 96, 2.6, 4.5, 14, pitch=90); k.sphere("brass", 7, 34, 96, 3.0, 4)
    return k


@prop
def wall_clock():
    """Round kitchen-style wall clock without its second hand (back at x=0, centre at the origin)."""
    k = K.Kit()
    k.tube("oak", (0, 0, 0), (2.4, 0, 0), 16, 28); k.tube("enamel", (2.4, 0, 0), (2.7, 0, 0), 13.6, 28)
    for i in range(12):
        a = math.radians(i * 30); r = 11.6
        k.obox("black", 2.8, r * math.sin(a), r * math.cos(a), 0.25, 0.7 if i % 3 else 1.1, 2.2 if i % 3 else 3.2, roll=-i * 30)
    k.obox("black", 2.9, 2.6, 2.4, 0.3, 1.0, 7.4, roll=-48); k.obox("black", 3.0, -3.6, 3.5, 0.3, 0.7, 10.4, roll=46)
    k.tube("black", (2.7, 0, 0), (3.5, 0, 0), 1.0, 10)
    return k


@prop
def clock_hand():
    """Second hand: turns about its own X axis (the pivot is the origin)."""
    k = K.Kit(); k.box("plastic_red", 0, -0.2, -2.6, 0.25, 0.2, 11.8); k.tube("plastic_red", (0, 0, 0), (0.4, 0, 0), 0.7, 8); return k


@prop
def banner_thankful():
    """Letter banner on a string, hung along the mantel (flat, facing +X, centred)."""
    k = K.Kit(); k.print_quad("p_banner_thankful", 0, -80, -15, 80, 15); return k


@prop
def banner_wrong():
    k = K.Kit(); k.print_quad("p_banner_wrong", 0, -80, -15, 80, 15); return k
