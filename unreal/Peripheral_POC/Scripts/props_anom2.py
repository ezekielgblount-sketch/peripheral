"""Props for the third anomaly pass: the last of the handoff's twelve (a coat that hangs as if worn, someone in the bathroom
mirror, the sign's rider gone blank) and more ordinary things that read as a person in a dim corner.
Every prop: origin on the floor, back against x=0, front toward +X, centred on Y (unless noted)."""
import meshkit as K
from props_furniture import prop
from props_anom import void_material
T = K.T


# ---------------- false positives ----------------
@prop
def dress_form():
    """A dressmaker's form on its stand with a blouse pinned to it and a hat left on the neck cap."""
    k = K.Kit()
    k.cyl("wood_dark", 22, 0, 0, 16, 3, 14); k.tube("wood_dark", (22, 0, 3), (22, 0, 100), 1.6, 8)
    c = K.Kit(); c.soft("fabric_cream", 10, -17, 98, 34, 17, 150, 5, 5, 0.5); c.soft("fabric_cream", 12, -21, 136, 32, 21, 153, 4, 4, 0.5); c.noise(1.2, 0.05, 7); k.add(c)
    k.cyl("wood_dark", 22, 0, 152, 4.5, 9, 10); k.sphere("fabric_navy", 22, 0, 168, 10.5, 6, sz=0.8); k.cyl("fabric_navy", 22, 0, 162, 15, 1.2, 14)
    return k


@prop
def robe_hook():
    """A bathrobe on a wall hook, hood up: the hook sits at head height."""
    k = K.Kit()
    k.tube("brass", (0, 0, 180), (6, 0, 180), 0.8, 6)
    c = K.Kit(); c.soft("fabric_white", 2, -22, 104, 15, 22, 174, 6, 5, 0.4); c.soft("fabric_white", 2, -17, 34, 13, 17, 126, 6, 5, 0.4)   # shoulders, then the long fall
    c.soft("fabric_white", 3, -29, 66, 12, -15, 164, 3, 4, 0.4); c.soft("fabric_white", 3, 15, 66, 12, 29, 164, 3, 4, 0.4)
    c.soft("fabric_white", 3, -11, 158, 15, 11, 186, 4, 4, 0.4); c.noise(2.0, 0.06, 8); k.add(c)                                # the hood, slack over the hook
    k.tube("fabric_white", (14, -5, 108), (15, -7, 62), 1.4, 6); k.tube("fabric_white", (14, 5, 108), (15, 8, 70), 1.4, 6)       # belt ends
    return k


@prop
def coveralls_hung():
    """Work coveralls on a nail with boots stood under them."""
    k = K.Kit()
    k.tube("metal", (0, 0, 176), (4, 0, 177), 0.5, 5)
    c = K.Kit(); c.soft("fabric_navy", 2, -20, 70, 12, 20, 176, 5, 5, 0.35)
    c.soft("fabric_navy", 2, -20, 6, 11, -1, 100, 3, 5, 0.35); c.soft("fabric_navy", 2, 1, 6, 11, 20, 100, 3, 5, 0.35)
    c.soft("fabric_navy", 3, -29, 78, 10, -13, 170, 3, 4, 0.35); c.soft("fabric_navy", 3, 13, 78, 10, 29, 170, 3, 4, 0.35)
    c.noise(1.8, 0.07, 9); k.add(c)
    k.soft("black", 3, -17, 0, 27, -5, 12, 3, 3); k.soft("black", 3, 5, 0, 27, 17, 12, 3, 3)
    return k


@prop
def ironing_board_up():
    """An ironing board stood on end against the wall with a shirt thrown over the top."""
    k = K.Kit()
    k.obox("fabric_cream", 7, 0, 82, 5, 34, 150, pitch=-4); k.tube("metal", (10, -10, 0), (6, -10, 60), 0.9, 6); k.tube("metal", (10, 10, 0), (6, 10, 60), 0.9, 6)
    c = K.Kit(); c.soft("fabric_white", 1, -22, 118, 16, 22, 164, 5, 4, 0.4); c.soft("fabric_white", 4, -8, 160, 13, 8, 170, 3, 3, 0.4); c.noise(1.6, 0.07, 10); k.add(c)
    return k


# ---------------- things that are different when you come back ----------------
@prop
def coat_hooks_worn():
    """The mud room coat rail with its jacket hanging as if someone were in it: a chest, shoulders, sleeves with arms in them (origin at the rail centre)."""
    k = K.Kit()
    k.box("wood_dark", 0, -40, -5, 2, 40, 5)
    for y in (-28, 0, 28):
        k.tube("brass", (2, y, 0), (7, y, 0), 0.7, 6); k.tube("brass", (7, y, 0), (9, y, 5), 0.7, 6)
    c = K.Kit(); c.soft("fabric_green", 3, -46, -84, 25, -10, 2, 5, 5, 0.5)
    c.soft("fabric_green", 5, -54, -72, 17, -46, -4, 3, 4, 0.5); c.soft("fabric_green", 5, -10, -72, 17, -2, -4, 3, 4, 0.5)
    c.soft("fabric_green", 6, -36, 0, 20, -20, 11, 4, 3, 0.5); c.noise(1.4, 0.04, 6); k.add(c)
    return k


@prop
def figure_mirror():
    """Head and shoulders, flat and black, to lie on the glass of a bathroom cabinet (origin at the middle of the glass)."""
    void_material()
    k = K.Kit()
    k.box("m_Void", 0, -17, -28.4, 0.3, 17, -7); k.box("m_Void", 0, -4, -7, 0.3, 4, 1); k.sphere("m_Void", 0.15, 0, 9.5, 8.5, 6, sx=0.02, sz=1.12)
    return k


def rider(printed):
    """The small board that hangs under the realtor's sign (origin at the post foot, like sign_post)."""
    k = K.Kit()
    for y in (22, 78):
        k.tube("metal", (0, y, 104), (0, y, 100), 0.5, 5)
    k.box("white", -1, 14, 84, 1, 86, 100)
    if printed:
        k.quad("p_sign_rider", 1.2, 16, 85.5, 84, 98.5); k.quad("p_sign_rider", -1.2, 16, 85.5, 84, 98.5, flip=True)
    return k


@prop
def sign_rider():
    return rider(True)


@prop
def sign_rider_blank():
    return rider(False)
