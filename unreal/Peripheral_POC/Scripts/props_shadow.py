"""Jack's shadow caster: a plain 178 cm figure that is never drawn, only its shadow is (BP_Shadow keeps it under the camera).
Two poses: standing, and the pose the shadow takes when it stops copying him (head tilted, right arm lifted away)."""
import meshkit as K
from props_furniture import prop


def figure(alt):
    """Origin at the feet, facing +X, right hand toward +Y."""
    k = K.Kit()
    for y in (-9.5, 9.5):
        k.tube("black", (0, y, 0), (0, y * 0.9, 88), 7.2, 10)                       # legs
        k.soft("black", -6, y - 5, 0, 17, y + 5, 7)                                 # feet
    k.soft("black", -11, -19, 84, 11, 19, 146)                                      # torso
    k.tube("black", (0, 0, 144), (0, 0, 154), 5.5, 10)                              # neck
    k.sphere("black", 2 if alt else 0, 7 if alt else 0, 165 if alt else 166, 11.5, 6, sz=1.12)
    k.tube("black", (0, -22, 141), (2, -25, 110), 4.8, 8); k.tube("black", (2, -25, 110), (6, -24, 80), 4.2, 8)      # left arm, hanging
    if alt:                                                                         # right arm lifted out to the side, hand open
        k.tube("black", (0, 22, 141), (0, 48, 150), 4.8, 8); k.tube("black", (0, 48, 150), (0, 66, 176), 4.2, 8)
        k.sphere("black", 0, 69, 182, 6.0, 5)
    else:
        k.tube("black", (0, 22, 141), (2, 25, 110), 4.8, 8); k.tube("black", (2, 25, 110), (6, 24, 80), 4.2, 8)
    return k


@prop
def shadow_body():
    return figure(False)


@prop
def shadow_body_alt():
    return figure(True)
