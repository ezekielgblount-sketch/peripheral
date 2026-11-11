"""Jack's car: an invented early-90s compact four-door, base trim. 426 long, 167 wide, 137 tall, 243 wheelbase,
13-inch steel wheels: the proportions of the small sedans of that time (checked against period photos, see BUILD_STATE).
Origin on the ground under the middle, nose toward +X, driver on the left (-Y). Boot open; hollow cabin for the drive-in.
The body is a lofted skin with real curvature; wheel arches, cabin, boot and panel gaps are cut out of it."""
import math, unreal
import meshkit as K
from props_furniture import prop

XF, XR = 213.0, -213.0                     # nose and tail
AX_F, AX_R, AX_Z = 128.0, -115.0, 29.0     # axles
WMAX = 83.5                                # half width at the waist
PAINT = "m_CarPaint"
Z0 = 86.8                                  # glasshouse base, sunk just below the body top
DENT = (-178.0, -1, 60.0, 11.0, 1.7)       # x, side, z, radius, depth: a parking dent in the left rear quarter


def lerp(a, b, t):
    return a + (b - a) * t


def ss(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def half_width(x):
    w = WMAX
    if x > 140: w -= 8.0 * ((x - 140) / 73.0) ** 2
    if x < -140: w -= 6.0 * ((-140 - x) / 73.0) ** 2
    d = min(XF - x, x - XR)
    if d < 9: w -= 9 - math.sqrt(max(0.0, 81 - (9 - d) ** 2))        # rounded corners seen from above
    return w


def top_z(x):
    if x >= 100: z = lerp(87.0, 72.0, ((x - 100) / 113.0) ** 1.25)    # bonnet falls toward the nose
    elif x >= -118: z = lerp(89.0, 87.0, (x + 118) / 218.0)           # belt line
    else: z = lerp(89.0, 86.0, (-118 - x) / 95.0)                     # boot deck
    d = min(XF - x, x - XR)
    if d < 6: z -= 6 - math.sqrt(max(0.0, 36 - (6 - d) ** 2))
    return z


def bottom_z(x):
    return 18.0 + 9.0 * ss(165, 213, x) + 11.0 * ss(-155, -213, x)


def side_y(x, z):
    """Half width of the body skin at height z."""
    W, zt, zb = half_width(x), top_z(x), bottom_z(x)
    if z >= 50: return W - 3.5 * min(1.0, (z - 50) / (zt - 55.0)) ** 1.6
    return W - 2 * (1 - max(0.0, (z - zb - 7) / (43.0 - zb))) ** 2


def section(x):
    """One closed cross-section of the body at x: sill tuck-under, widest at the waist, tumblehome, rolled shoulder, crowned top."""
    W, zt, zb = half_width(x), top_z(x), bottom_z(x)
    crown, zw, rs, rb, tum = (2.6 if x > 100 else 2.0), 50.0, 5.0, 7.0, 3.5
    h = [(0.0, zb), (W * 0.45, zb), (W - rb - 8, zb)]
    h += [(W - 2 - rb + rb * math.sin(i / 4 * math.pi / 2), zb + rb - rb * math.cos(i / 4 * math.pi / 2)) for i in range(1, 5)]
    h += [(W - 2 * (1 - i / 3) ** 2, lerp(zb + rb, zw, i / 3)) for i in range(1, 4)]
    zs = zt - rs
    h += [(W - tum * (i / 6) ** 1.6, lerp(zw, zs, i / 6)) for i in range(1, 7)]
    h += [(W - tum - rs + rs * math.cos(i / 4 * math.pi / 2), zs + rs * math.sin(i / 4 * math.pi / 2)) for i in range(1, 5)]
    ye = W - tum - rs
    h += [(ye * (1 - i / 6), zt + crown * (1 - (1 - i / 6) ** 2)) for i in range(1, 7)]
    ring = [(x, y, z) for (y, z) in h] + [(x, -y, z) for (y, z) in reversed(h[1:-1])]
    dx, sd, dz, dr, dd = DENT
    out = []
    for (px, py, pz) in ring:
        if py * sd > W - 14:
            py -= sd * dd * math.exp(-((px - dx) ** 2 + (pz - dz) ** 2 * 1.6) / dr ** 2)
        out.append((px, py, pz))
    return out


def body():
    k = K.Kit()
    ends = [0, 0.8, 2, 3.6, 5.6, 8]
    xs = sorted(set([XR + e for e in ends] + [XF - e for e in ends] + list(range(-204, 205, 4)) + list(range(-195, -160, 2))))
    k.loft(PAINT, [section(x) for x in xs], angle=35)
    t = K.Kit()                                                        # wheel wells
    for ax in (AX_F, AX_R):
        for s in (-1, 1):
            t.tube("black", (ax, s * 60.0, AX_Z), (ax, s * 95.0, AX_Z), 33.0, 40)
    k.cut(t)
    for (key, b) in (("plastic_grey", (-80, -70, 30, 92, 70, 120)), ("plastic_grey", (-112, -57, 30, -79, 57, 120)),      # cabin, rear seat area
                     ("plastic_black", (-205, -57, 57.5, -127, 57, 120)), (PAINT, (-218, -50, 74, -204, 50, 120))):       # boot tub, loading lip
        t = K.Kit(); t.box(key, *b); k.cut(t)
    # panel gaps: thin grooves cut into the skin
    g1, g2, ga, gb = K.Kit(), K.Kit(), K.Kit(), K.Kit()
    for s in (-1, 1):
        for xg in (90.0, -14.0, -80.0):                                # door shut lines
            y0, y1 = sorted((s * (WMAX - 6), s * (WMAX + 3)))
            g1.box("black", xg - 0.3, y0, 21, xg + 0.3, y1, 96)
        y0, y1 = sorted((s * (WMAX - 6), s * (WMAX + 3)))
        g2.box("black", -80, y0, 26.7, 90, y1, 27.3)                    # door bottoms
        pts = []
        for xg in (102.0, 130.0, 160.0, 186.0, 204.0):                  # bonnet shut line along the wing top
            pts.append((xg, s * (half_width(xg) - 12.0), top_z(xg) + 0.6))
        for i in range(4):
            (ax_, ay, az), (bx, by, bz) = pts[i], pts[i + 1]
            ln = math.dist(pts[i], pts[i + 1])
            (ga if i % 2 == 0 else gb).obox("black", (ax_ + bx) / 2, (ay + by) / 2, (az + bz) / 2, ln + 0.5, 0.6, 5,
                                           pitch=math.degrees(math.atan2(bz - az, bx - ax_)), yaw=math.degrees(math.atan2(by - ay, bx - ax_)))
    yb = half_width(102) - 12.0
    g1.box("black", 101.7, -yb, 83, 102.3, yb, 96)                        # bonnet rear edge
    wf = half_width(-165)
    for xg in (-172.0, -158.0):                                         # fuel flap, driver's side
        g1.box("black", xg - 0.25, -(wf + 3), 60, xg + 0.25, -(wf - 5), 73)
    for zg in (60.0, 73.0):
        g2.box("black", -172, -(wf + 3), zg - 0.25, -158, -(wf - 5), zg + 0.25)
    for g in (g1, g2, ga, gb):
        k.cut(g, angle=35)
    return k


def gh_ring(t, inset=0.0, dz=0.0):
    """Glasshouse outline at height fraction t (0 belt, 1 roof edge): list of ((x,y,z), kind of the span that starts here)."""
    z = lerp(Z0, 132.0, t) - dz
    xf, xr = lerp(94.0, 40.0, t) - inset, lerp(-119.0, -72.0, t) + inset
    w, rc, bow, cw = lerp(74.0, 60.5, t) - inset, lerp(15.0, 11.0, t), lerp(5.0, 3.0, t), lerp(22.0, 12.0, t)
    return _outline(xf, xr, w, rc, bow, cw, z)


def _outline(xf, xr, w, rc, bow, cw, z):
    o, ys = [], w - rc
    xs, xe = xf - rc, xr + rc
    for i in range(8):                                                  # windscreen base, bowed forward
        y = lerp(-ys, ys, i / 8.0); o.append(((xf + bow * (1 - (y / ys) ** 2), y, z), "W"))
    def arc(cx, cy, angs, kinds):
        for a, kd in zip(angs, kinds):
            o.append(((cx + rc * math.cos(math.radians(a)), cy + rc * math.sin(math.radians(a)), z), kd))
    arc(xs, ys, (0, 15, 30, 35, 55, 75), "WWSPPP")
    for x, kd in ((xs, "P"), (xs - 2.5, "S"), (xs - 3.7, "G"), (-8.0, "K"), (-19.0, "G"), (xe + cw + 1.2, "S"), (xe + cw, "P")):
        o.append(((x, w, z), kd))
    arc(xe, ys, (90, 105, 125, 145, 150, 165), "PPPSRR")
    for i in range(8):                                                  # rear window base
        y = lerp(ys, -ys, i / 8.0); o.append(((xr - bow * (1 - (y / ys) ** 2), y, z), "R"))
    arc(xe, -ys, (180, 195, 210, 215, 235, 255), "RRSPPP")
    for x, kd in ((xe, "P"), (xe + cw, "S"), (xe + cw + 1.2, "G"), (-19.0, "K"), (-8.0, "G"), (xs - 3.7, "S"), (xs - 2.5, "P")):
        o.append(((x, -w, z), kd))
    arc(xs, -ys, (270, 285, 305, 325, 330, 345), "PPPSWW")
    return o


def glasshouse(k):
    """Roof, pillars and windows as a thin shell: painted outside, trimmed inside, glass between black rubber seals."""
    C = (-10.0, 0.0, 100.0)
    acc = {}

    def quad(key, p, toward=None, away=False):
        vs, ts = acc.setdefault(key, ([], []))
        cen = tuple(sum(q[i] for q in p) / 4.0 for i in range(3))
        d = tuple(toward[i] - cen[i] for i in range(3)) if toward else tuple((C[i] - cen[i]) if away else (cen[i] - C[i]) for i in range(3))
        for tri in ((p[0], p[1], p[2]), (p[0], p[2], p[3]))[:(1 if p[2] == p[3] else 2)]:
            u = [tri[2][i] - tri[0][i] for i in range(3)]; v = [tri[1][i] - tri[0][i] for i in range(3)]
            n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])        # the side Unreal draws
            b = len(vs)
            vs.extend(tri if n[0] * d[0] + n[1] * d[1] + n[2] * d[2] >= 0 else (tri[0], tri[2], tri[1])); ts.append((b, b + 1, b + 2))

    zs = (Z0, 90.0, 91.2, 127.6, 128.8, 132.0)
    ts_ = [(z - Z0) / (132.0 - Z0) for z in zs]
    out = [gh_ring(t) for t in ts_]; inn = [gh_ring(t, 2.0) for t in ts_]
    n = len(out[0])
    for r in range(5):
        for j in range(n):
            kd = out[0][j][1]; j2 = (j + 1) % n
            po = (out[r][j][0], out[r][j2][0], out[r + 1][j2][0], out[r + 1][j][0])
            pi = (inn[r][j][0], inn[r][j2][0], inn[r + 1][j2][0], inn[r + 1][j][0])
            glassy = kd in "WGR"
            if r in (0, 4): mo, mi = PAINT, "plastic_grey"
            elif r in (1, 3): mo, mi = ("rubber", "rubber") if kd != "P" else (PAINT, "plastic_grey")
            else: mo, mi = {"P": (PAINT, "plastic_grey"), "S": ("rubber", "rubber"), "K": ("plastic_black", "plastic_grey")}.get(kd, ("glass", None))
            quad(mo, po)
            if mi:
                quad(mi, pi, away=True)
            if r == 2 and glassy:                                       # reveals around each pane, so the shell has thickness
                gc = tuple(sum(q[i] for q in po) / 4.0 for i in range(3))
                quad("rubber", (po[0], po[1], pi[1], pi[0]), toward=gc); quad("rubber", (po[3], po[2], pi[2], pi[3]), toward=gc)
                if out[0][(j - 1) % n][1] not in "WGR": quad("rubber", (po[0], po[3], pi[3], pi[0]), toward=gc)
                if out[0][j2][1] not in "WGR": quad("rubber", (po[1], po[2], pi[2], pi[1]), toward=gc)
    def roof(inset, z, liner):
        o = _outline(40.0 - inset, -72.0 + inset, 60.5 - inset, max(3.0, 11.0 - inset * 0.4), 3.0, 12.0, z)
        return [p for p, _ in o]
    for liner in (False, True):
        dz = 2.0 if liner else 0.0
        rs = [[p for p, _ in (inn if liner else out)[5]]] + [roof(i + dz, z - dz, liner) for i, z in ((2.5, 134.3), (7.0, 135.8), (16.0, 136.7), (34.0, 137.2))]
        key = "headliner" if liner else PAINT
        for r in range(len(rs) - 1):
            for j in range(n):
                j2 = (j + 1) % n
                quad(key, (rs[r][j], rs[r][j2], rs[r + 1][j2], rs[r + 1][j]), away=liner)
        top = (-16.0, 0.0, 137.5 - dz)
        for j in range(n):
            quad(key, (rs[-1][j], rs[-1][(j + 1) % n], top, top), away=liner)
    for key, (vs, ts) in acc.items():
        k.mesh(key, vs, ts, angle=(89 if key in ("rubber", "glass") else 32))


def wheel():
    """13-inch steel wheel with a small centre cap, axis along local Z (outboard is +Z)."""
    w = K.Kit()
    w.revolve("rubber", [(17.2, -8.2), (21, -9.3), (25.5, -9.2), (28.0, -7.6), (28.9, -4.5), (29.0, 0), (28.9, 4.5), (28.0, 7.6), (25.5, 9.2), (21, 9.3), (17.2, 8.2)], 36, capped=False)
    path = [(0.1, -7.5), (18.2, -7.5), (18.2, 8.4), (17.4, 7.6), (16.0, 3.8), (15.2, 1.2), (12.6, 1.2), (10.5, 2.8), (4.8, 3.4), (4.2, 4.6), (0.1, 4.6)]
    for pth in (path, path[::-1]):                                      # whichever order faces outward
        rim = K.Kit(); rim.revolve("wheel_steel", pth, 36, capped=False)
        if unreal.GeometryScript_MeshQueries.get_mesh_volume_area(rim.m)[1] > 0:
            break
    K.smooth(rim.m, 35); w.add(rim)
    print("rim volume", unreal.GeometryScript_MeshQueries.get_mesh_volume_area(rim.m))
    w.cyl("plastic_black", 0, 0, 4.6, 2.9, 1.4, 16)
    for i in range(4):
        a = math.radians(45 + i * 90); w.cyl("chrome", 5.3 * math.cos(a), 5.3 * math.sin(a), 3.2, 0.95, 1.6, 6)
    for i in range(8):
        a = math.radians(i * 45); w.obox("black", 11.6 * math.cos(a), 11.6 * math.sin(a), 2.3, 1.7, 3.6, 1.0, yaw=math.degrees(a))
    return w


def bumper(k, front):
    """Unpainted grey plastic bumper that wraps the corners, with a black rub strip."""
    s = 1 if front else -1
    def ring(x, w, z0, z1, r=3.5):
        h = [(0.0, z0), (w - r, z0)] + [(w - r + r * math.sin(a), z0 + r - r * math.cos(a)) for a in (math.pi / 6, math.pi / 3, math.pi / 2)]
        h += [(w - r + r * math.cos(a), z1 - r + r * math.sin(a)) for a in (0, math.pi / 6, math.pi / 3, math.pi / 2)] + [(0.0, z1)]
        return [(x, y, z) for (y, z) in h] + [(x, -y, z) for (y, z) in reversed(h[1:-1])]
    ds = ([50, 42, 34] if front else [63, 54, 44, 36]) + [28, 22, 16, 10, 7, 4, 2.2, 0.6, -0.8, -2, -2.7, -3.0]    # distance back from the body's end
    rings = []
    for d in ds:
        x = (XF if front else XR) - s * d
        xb = max(XR + 9.01, min(XF - 9.01, x))
        w = half_width(xb) + 1.6 - (0 if d >= 9 else 12.0 - math.sqrt(max(0.0, 144.0 - (9 - d) ** 2)))
        rings.append(ring(x, w, 25.0 if front else 26.0, 45.0 if front else 47.5))
    if not front: rings.reverse()
    k.loft("bumper", rings, angle=40)
    xe = (XF + 3.05) if front else (XR - 3.05)
    k.box("plastic_black", min(xe, xe + s * 0.5), -60, 36.5, max(xe, xe + s * 0.5), 60, 40)


@prop
def car():
    k = body()
    glasshouse(k)
    for front in (True, False):
        bumper(k, front)
    rv = unreal.MathLibrary.greater_greater_vector_rotator(unreal.Vector(0, 0, 1), unreal.Rotator(roll=90, pitch=0, yaw=0))
    w = wheel()
    for ax in (AX_F, AX_R):
        for s in (-1, 1):
            k.add(w, K.T(ax, s * 71.3, AX_Z, roll=(90 if rv.y * s > 0 else -90)))
    for s in (-1, 1):
        # nose: composite headlamp with a clear lens, amber corner lamp
        y0, y1 = sorted((s * 40, s * 66))
        k.box("chrome", 207, y0, 52.5, 213.3, y1, 66.5); k.box("glass", 213.3, y0, 52.5, 214.1, y1, 66.5); k.sphere("lamp_off", 213.2, s * 54, 59.5, 3.0, 4, sx=0.3)
        k.box("rubber", 206.5, y0 - 0.6, 51.9, 213.9, y1 + 0.6, 52.5); k.box("rubber", 206.5, y0 - 0.6, 66.5, 213.9, y1 + 0.6, 67.1)
        k.obox("plastic_amber", 209.9, s * 70.4, 59.5, 10.5, 3.0, 11, yaw=s * -52)
        # tail lamps: red, amber, white reverse lens, in a black surround
        y0, y1 = sorted((s * 50.2, s * 68.6))
        k.box("rubber", -214.2, y0, 59, -211.5, y1, 77.5)
        for (a, b, key) in ((50.8, 56, "enamel"), (56.4, 62, "plastic_amber"), (62.4, 68, "lens_red")):
            ya, yb = sorted((s * a, s * b)); k.box(key, -214.8, ya, 59.6, -214.0, yb, 76.9)
        # mirrors on black stalks, flap door handles in their recesses, rub strip, sill
        k.soft("plastic_black", 76, s * 84.5 - 7.5, 88, 87, s * 84.5 + 7.5, 98.5, 4, 3, 0.35); k.box("mirror", 75.7, s * 84.5 - 6, 89.3, 76.3, s * 84.5 + 6, 97.2)
        k.tube("plastic_black", (85, s * 73.5, 91), (83, s * 79, 93), 1.9, 8)
        for xh in (-2.0, -70.0):
            sy = side_y(xh + 5, 75)
            ya, yb = sorted((s * (sy - 1.6), s * (sy + 0.12)))
            k.box("black", xh - 1, ya, 72.5, xh + 12, yb, 77.5); k.obox("plastic_black", xh + 5.5, s * (sy + 0.3), 75.8, 11.6, 0.7, 3.0)
            k.sphere("chrome", xh + 15.5, s * (side_y(xh + 15, 73.5) - 0.2), 73.5, 1.0, 3)       # lock barrel
        ya, yb = sorted((s * (WMAX - 0.4), s * (WMAX + 1.1)))
        k.box("rubber", -78, ya, 50, 88, yb, 53.5)                                               # rub strip along the doors
        for (xa, xb) in ((92, 96), (-150, -196)):                                                # and its short ends on the wings
            wa = side_y(xb, 51.7)
            k.obox("rubber", (xa + xb) / 2, s * ((WMAX + wa) / 2 + 0.35), 51.75, abs(xa - xb), 1.5, 3.5, yaw=s * math.degrees(math.atan2(wa - WMAX, xb - xa)))
        k.tube("rubber", (96, s * 71.5, 89.6), (-80, s * 73.6, 91.6), 0.9, 6)                    # window-sill weatherstrip
        k.tube("rubber", (40 + 2, s * 61, 131.0), (-66, s * 61, 131.0), 0.8, 6)                  # roof gutter trim
    # grille: black opening with three bars and a plain chrome strip (no badge)
    k.box("black", 210.5, -39, 53, 213.5, 39, 66)
    for z in (55.5, 59.5, 63.5):
        k.box("bumper", 213.5, -38.5, z - 0.6, 214.3, 38.5, z + 0.6)
    k.box("chrome", 213.5, -39.4, 66, 214.5, 39.4, 67.2); k.box("black", 215.6, -30, 28, 216.4, 30, 33)
    k.box("paper", -214.6, -15.5, 59.5, -214.0, 15.5, 73); k.box("rubber", -214.3, -16.5, 58.5, -213.6, 16.5, 74)      # blank plate in its frame
    k.tube("steel", (-212, 46, 21), (-226, 46, 21), 2.2, 12); k.tube("black", (-226.1, 46, 21), (-222, 46, 21), 1.7, 10)   # exhaust
    k.tube("steel", (-150, 72, 88), (-160, 73, 166), 0.28, 5)                                     # aerial
    for s in (-1, 1):                                                                             # wipers parked on the scuttle
        k.tube("black", (100.5, s * 10 - 28, 90.4), (98.5, s * 10 + 24, 90.9), 0.7, 5); k.tube("black", (101, s * 10 - 28, 89.2), (100.5, s * 10 - 28, 90.4), 1.0, 6)
    # boot lid, open: outer skin, inner frame, lip, and two hinge arms
    lid = K.Kit()
    lid.soft(PAINT, 0, -64, -3.2, 84, 64, 0, 6, 1, 0.25); lid.soft(PAINT, 80.5, -64, -3, 84.5, 64, 13, 4, 1, 0.25)
    lid.box(PAINT, 5, -57, 0, 77, 57, 1.8)                                                        # inner frame, body colour, with pressed recesses
    for (x0, y0, x1, y1) in ((12, -50, 34, -6), (12, 6, 34, 50), (42, -50, 70, -22), (42, 22, 70, 50), (46, -12, 66, 12)):
        lid.box("plastic_grey", x0, y0, 1.8, x1, y1, 2.0)
    k.add(lid, K.T(-123.5, 0, 91.5, pitch=101))
    for s in (-1, 1):
        k.tube("steel", (-126, s * 54, 86), (-131, s * 54, 106), 1.1, 6)
        k.tube("rubber", (-204, s * 57.5, 87.5), (-128, s * 57.5, 89.5), 1.0, 6)                  # boot seal
    k.box("fabric_grey", -204.5, -56.5, 57.5, -127.5, 56.5, 58.3)                                 # boot carpet
    # cabin
    k.box("fabric_grey", -111.5, -69.5, 30, 91.5, 69.5, 31.5)                                     # carpet
    k.soft("dash", 60, -69, 66, 93, 69, 93, 6, 2, 0.3); k.soft("dash", 52, -58, 84, 70, -14, 97, 5, 2, 0.3)      # dashboard, instrument hood
    k.box("black", 51.6, -52, 86.5, 52.4, -20, 94.5); k.box("black", 59.4, -10, 72, 60.2, 14, 88)                # dials, radio and heater panel
    for y in (-3, 7):
        k.cyl("plastic_grey", 59.2, y, 75, 1.6, 1.4, 10, pitch=-90)
    k.box("plastic_grey", 59.3, -8, 81, 60, 12, 86.5); k.box("black", 59.6, 24, 87.2, 60.3, 60, 87.8)            # radio face, glovebox line
    k.torus("dash", 50, -36, 90, 18.5, 1.6, pitch=64, major=28); k.tube("dash", (51, -36, 89.5), (64, -36, 83), 2.6, 8)
    for a in (90, 180, 270):                                                                      # three spokes
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        k.tube("dash", (50, -36, 90), (50 + 17.5 * ca * 0.438, -36 + 17.5 * sa, 90 + 17.5 * ca * 0.899), 1.3, 5)
    for y in (-36, 36):                                                                           # front seats with headrests
        k.soft("fabric_grey", -24, y - 25, 44, 30, y + 25, 62, 6, 4, 0.4); k.soft("fabric_grey", -36, y - 24, 54, -18, y + 24, 112, 6, 4, 0.4)
        k.soft("fabric_grey", -37, y - 12, 112, -25, y + 12, 128, 5, 3, 0.4)
        for yy in (-6, 6):
            k.tube("chrome", (-30, y + yy, 108), (-31, y + yy, 116), 0.5, 5)
    k.soft("fabric_grey", -104, -56, 44, -58, 56, 62, 6, 4, 0.4); k.soft("fabric_grey", -116, -56, 54, -98, 56, 110, 6, 4, 0.4)   # rear bench
    k.box("plastic_grey", -117, -62, 88.2, -100, 62, 89.6)                                        # parcel shelf
    k.soft("dash", -30, -8, 31, 58, 8, 50, 4, 2, 0.3); k.tube("black", (22, 0, 50), (26, 0, 66), 1.0, 6); k.sphere("black", 26, 0, 67.5, 2.6, 4)
    k.tube("black", (-12, 0, 50), (2, 0, 56), 1.4, 6)                                             # handbrake
    k.box("black", 30, -9, 124, 31.5, 9, 130); k.tube("black", (33, 0, 131), (31, 0, 128), 0.8, 5)   # rear-view mirror
    for s in (-1, 1):                                                                             # door pulls and window winders
        k.soft("dash", -6, s * 69.8 - 3, 62, 34, s * 69.8 + 3, 68, 4, 2, 0.3); k.cyl("plastic_black", 44, s * 69, 60, 2.2, 1.5, 10, roll=s * -90)
    return k
