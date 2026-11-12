"""The house, as data. Everything else (walls, floors, doors, trim, fit check, the blueprint document) is derived from this.
Pure Python: no Unreal imports, so it also runs outside the editor.

Blueprint cm. +X front to back, +Y away from the garage, +Z up. A rect is (x0, y0, x1, y1) of CLEAR floor space.
Interior walls are the 12 cm gaps between rects, outside walls the 20 cm ring round each storey.
Playtest round 1 layout: centre-hall two-storey, about 3,150 sq ft on floors 1 and 2, plus basement, attic loft and garage."""

GR, LND, B, F1, C1, F2, C2, F3 = -140, -126, -252, 0, 244, 259, 503, 518     # grade, entry landing, basement, floors and ceilings
DH = 203                                                                      # door height
SLAB = 15
WALK_SPEED = 135.0                                                            # cm/s: a calm indoor walk

# storey -> outside face of the outside walls (x0, y0, x1, y1), and the z range of the outside skin
BBOX = {0: (-20, 580, 1100, 1980), 1: (-20, 580, 1100, 1980), 2: (-50, 580, 1100, 1980)}
EXT_Z = {0: (B - SLAB, -SLAB), 1: (-SLAB, C1), 2: (C1, F3)}
EXT_MAT = {0: "brick", 1: "brick", 2: "siding"}

# finish name -> (wall, floor, baseboard/casing trim)
FIN = {
    "living": ("w_liv", "f_oak", "oak"), "hall": ("w_hall", "f_oak", "white"), "dining": ("w_din", "f_oak", "white"),
    "kitchen": ("w_kit", "f_vinyl", "white"), "mud": ("w_mud", "f_vinyl", "white"), "halfbath": ("w_bath_blue", "f_sq", "white"),
    "den": ("w_den", "f_c_den", "white"), "hall2": ("w_hall", "f_c_hall", "white"), "parents": ("w_par", "f_c_par", "white"),
    "pbath": ("w_bath_sea", "f_hex", "white"), "pcloset": ("w_par", "f_c_par", "white"), "sibling": ("w_sib", "f_c_sib", "white"),
    "jack": ("w_jack", "f_c_jack", "white"), "bath": ("w_bath_mauve", "f_hex", "white"), "guest": ("w_guest", "f_c_guest", "white"),
    "closet": ("w_hall", "f_c_hall", "white"), "bsmt": ("bsmt", "f_bsmt", None),
}
SIDE_MAT = {("den", "y1"): "w_den_acc"}          # the den's far end wall is the burgundy accent wall

ROOMS = []


def R(storey, name, rect, fin=None, floor=None, ceil=None, floor_mat="auto", ceil_mat="ceiling", ghost=False, base=True, label=None):
    """floor / ceil default to the storey's own. floor_mat None = the floor here is built by hand (stairs, the sunken entry)."""
    z0 = {0: B, 1: F1, 2: F2}[storey] if floor is None else floor
    z1 = {0: -SLAB, 1: C1, 2: C2}[storey] if ceil is None else ceil
    fin = fin or name
    ROOMS.append(dict(storey=storey, name=name, rect=rect, fin=fin, floor=z0, ceil=z1, ghost=ghost, base=base and floor_mat is not None,
                      floor_mat=(FIN[fin][1] if floor_mat == "auto" else floor_mat), ceil_mat=ceil_mat, label=label or name))


# ---------------- floor 1 ----------------
R(1, "living", (0, 600, 574, 1064), label="Living room")
R(1, "entry", (0, 1076, 180, 1186), "hall", floor=LND, floor_mat=None, label="Entry")
R(1, "entry_c", (0, 1186, 106, 1284), "hall", floor=LND, floor_mat=None)
R(1, "entry_d", (106, 1186, 180, 1284), "hall", floor=LND, floor_mat=None, ceil_mat=None)      # the top steps of the stair to floor 2 pass over here
R(1, "entry_b", (0, 1284, 100, 1296), "hall", floor=LND, floor_mat=None)
R(1, "stair_down", (180, 1076, 376, 1174), "hall", floor=B, floor_mat=None)
R(1, "hall_pocket", (376, 1076, 470, 1174), "hall")
R(1, "hall_back", (470, 1076, 574, 1296), "hall", label="Hall")
R(1, "stair_up2", (180, 1186, 470, 1284), "hall", floor_mat=None, ceil_mat=None)
R(1, "up_flight", (0, 1296, 100, 1559), "hall", floor_mat=None)
R(1, "hall_main", (100, 1296, 574, 1559), "hall", label="Hall")
R(1, "dining", (0, 1571, 574, 1960), label="Dining room")
R(1, "mud", (586, 600, 850, 850), label="Laundry / mudroom")
R(1, "halfbath", (862, 600, 1080, 850), label="Half bath")
R(1, "kitchen", (586, 862, 1080, 1450), label="Kitchen and nook")
R(1, "den", (586, 1462, 1080, 1960), label="Family room / den")
# ---------------- floor 2 ----------------
R(2, "parents", (-30, 600, 380, 1174), label="Parents' bedroom")
R(2, "pbath", (392, 600, 566, 920), label="Parents' bath")
R(2, "pcloset", (392, 932, 566, 1174), label="Closet")
R(2, "arrival", (-30, 1186, 106, 1284), "hall2")
R(2, "well", (106, 1186, 470, 1284), "hall2", floor_mat=None)
R(2, "hall_wide", (470, 1186, 700, 1284), "hall2")
R(2, "gallery", (-30, 1284, 700, 1416), "hall2", label="Upstairs hall")
R(2, "back_hall_s", (578, 600, 700, 1186), "hall2", label="Back hall")
R(2, "back_hall_n", (578, 1416, 700, 1770), "hall2")
R(2, "alcove", (452, 1540, 578, 1770), "hall2")
R(2, "attic_landing", (-30, 1428, 203, 1528), "hall2", label="Attic stair")
R(2, "attic_flight", (203, 1428, 566, 1528), "hall2", floor_mat=None, ceil_mat=None)
R(2, "guest", (-30, 1540, 440, 1960), label="Guest / sewing room")
R(2, "closet_a", (452, 1782, 574, 1960), "closet", label="Linen")
R(2, "closet_b", (586, 1782, 700, 1960), "closet", label="Storage")
R(2, "sibling", (712, 600, 1080, 1100), label="Sibling's room")
R(2, "jack", (712, 1112, 1080, 1650), label="Jack's room")
R(2, "bath", (712, 1662, 1080, 1960), label="Hall bath")
# ---------------- basement ----------------
R(0, "b_store", (0, 600, 574, 1064), "bsmt", label="Storage")
R(0, "b_foot", (376, 1076, 574, 1174), "bsmt")
R(0, "b_link", (470, 1174, 574, 1186), "bsmt")
R(0, "b_under", (192, 1186, 574, 1284), "bsmt")
R(0, "b_mid", (112, 1296, 574, 1559), "bsmt", label="Utility")
R(0, "b_east", (0, 1571, 574, 1960), "bsmt", label="Workshop")
R(0, "b_rec", (586, 600, 1080, 1960), "bsmt", label="Basement")
R(0, "stair_down_g", (180, 1076, 376, 1174), "bsmt", ghost=True)          # the flight from floor 1 comes down through here

OPENINGS = []


def D(name, storey, axis, t0, t1, a0, a1, hinge, swing, z=None, key="door_wood", locked=False, is_open=False, keys=("trim", "trim"), tags=()):
    """A working door. axis 'x': the wall's thickness runs along X (t0..t1) and the opening runs a0..a1 along Y; 'y' the other way."""
    z = {0: B, 1: F1, 2: F2}[storey] if z is None else z
    OPENINGS.append(dict(kind="door", name=name, storey=storey, axis=axis, t0=t0, t1=t1, a0=a0, a1=a1, z0=z, z1=z + DH, hinge=hinge,
                         swing=swing, key=key, locked=locked, is_open=is_open, keys=keys, tags=list(tags)))


def O(storey, axis, t0, t1, a0, a1, top=DH + 10):
    z = {0: B, 1: F1, 2: F2}[storey]
    OPENINGS.append(dict(kind="open", storey=storey, axis=axis, t0=t0, t1=t1, a0=a0, a1=a1, z0=z, z1=z + top))


def W(storey, axis, t0, t1, a0, a1, z0, z1, inside, style="double"):
    base = {0: B, 1: F1, 2: F2}[storey]
    OPENINGS.append(dict(kind="window", storey=storey, axis=axis, t0=t0, t1=t1, a0=a0, a1=a1, z0=base + z0, z1=base + z1, inside=inside, style=style))


# floor 1 doors
D("Door_front", 1, "x", -20, 0, 1135, 1226, "lo", +1, z=LND, key="door_red", keys=("white", "trim"))
D("Door_living", 1, "y", 1064, 1076, 470, 561, "hi", -1, is_open=True, keys=("oak", "trim"))
D("Door_kitchen", 1, "x", 574, 586, 1345, 1436, "hi", +1, is_open=True)
D("Door_dining", 1, "y", 1559, 1571, 250, 341, "lo", +1, is_open=True)
D("Door_dining_den", 1, "x", 574, 586, 1720, 1811, "lo", +1)
D("Door_mud", 1, "y", 850, 862, 640, 731, "lo", -1)
D("Door_halfbath", 1, "x", 850, 862, 700, 791, "lo", +1)
D("Door_garage", 1, "y", 580, 600, 650, 741, "lo", +1, keys=("white", "trim"))
D("Door_kitchen_rear", 1, "x", 1080, 1100, 1250, 1341, "lo", -1, key="enamel", keys=("trim", "white"))
O(1, "y", 1450, 1462, 760, 960)                                              # kitchen nook to the den: a wide cased opening
# floor 2 doors
D("Door_parents", 2, "y", 1174, 1186, 5, 96, "lo", -1)
D("Door_pbath", 2, "x", 380, 392, 700, 791, "lo", +1)
D("Door_pcloset", 2, "x", 380, 392, 1000, 1091, "lo", +1)
D("Door_sibling", 2, "x", 700, 712, 800, 891, "lo", +1)
D("Door_jack", 2, "x", 700, 712, 1300, 1391, "lo", +1, is_open=True)
D("Door_bath", 2, "x", 700, 712, 1672, 1763, "lo", +1, is_open=True)
D("Door_guest", 2, "x", 440, 452, 1650, 1741, "lo", -1)
D("Door_attic", 2, "y", 1416, 1428, 60, 151, "lo", +1)
D("Door_closet_a", 2, "y", 1770, 1782, 468, 559, "lo", +1, locked=True)
D("Door_closet_b", 2, "y", 1770, 1782, 598, 689, "lo", +1, locked=True)
# basement: plain cased openings, no doors
O(0, "x", 574, 586, 800, 891); O(0, "x", 574, 586, 1081, 1172); O(0, "y", 1284, 1296, 480, 571)
O(0, "y", 1559, 1571, 300, 391); O(0, "x", 574, 586, 1700, 1791)
# windows (z measured from that storey's floor)
W(1, "x", -20, 0, 720, 960, 60, 210, +1, "picture")                          # living room picture window
W(1, "x", -20, 0, 1100, 1125, LND + 20, LND + DH, +1, "plain"); W(1, "x", -20, 0, 1236, 1261, LND + 20, LND + DH, +1, "plain")      # sidelights
W(1, "x", -20, 0, 1700, 1840, 80, 215, +1); W(1, "y", 1960, 1980, 220, 360, 90, 220, -1)        # dining: front and side
W(1, "x", 1080, 1100, 1620, 1800, 80, 215, -1, "picture"); W(1, "y", 1960, 1980, 760, 900, 90, 220, -1)     # den: rear and side
W(1, "x", 1080, 1100, 960, 1100, 107, 207, -1)                               # over the kitchen sink
W(1, "x", 1080, 1100, 700, 760, 130, 200, -1, "plain")                       # half bath
W(2, "x", -50, -30, 700, 840, 90, 220, +1); W(2, "x", -50, -30, 940, 1080, 90, 220, +1)         # parents, front
W(2, "x", -50, -30, 1305, 1395, 90, 220, +1)                                 # upstairs hall, front
W(2, "x", -50, -30, 1448, 1508, 120, 200, +1, "plain")                       # attic stair landing
W(2, "x", -50, -30, 1700, 1840, 90, 220, +1); W(2, "y", 1960, 1980, 150, 290, 90, 220, -1)      # guest: front and side
W(2, "x", 1080, 1100, 780, 920, 90, 220, -1)                                 # sibling
W(2, "x", 1080, 1100, 1300, 1440, 90, 220, -1)                               # Jack
W(2, "x", 1080, 1100, 1780, 1860, 120, 200, -1, "plain")                     # hall bath

# hand-built pieces other scripts need to agree on
STAIRS = dict(
    up=dict(axis="y", start=1296, sign=+1, lane=(0, 100), n=6, rise=18, tread=28, first_top=LND + 18),          # landing up to floor 1
    down=dict(axis="x", start=180, sign=+1, lane=(1076, 1174), n=6, rise=-18, tread=28, first_top=LND - 18),    # landing down to the basement
    upper=dict(axis="x", start=470, sign=-1, lane=(1186, 1284), n=13, rise=18.5, tread=28, first_top=18.5),     # floor 1 to floor 2
    attic=dict(axis="x", start=175, sign=+1, lane=(1428, 1528), n=13, rise=18.5, tread=28, first_top=F2 + 18.5),   # floor 2 to the loft
)
GARAGE = dict(x0=0, y0=-40, x1=760, y1=580, floor=GR + 2, ceil=C1, door=(25, 515, 213))        # clear inside; door opening along Y and its height
LOFT = dict(x0=170, y0=1192, x1=880, y1=1960, ridge_x=525.0, pitch=8.0 / 12.0, well=(203, 1428, 539, 1528))
HALL_CAP = dict(x0=578, x1=700, y=754, travel=80)          # the far end wall of the upstairs back hall: an anomaly moves it back
ANNEX = dict(door_y=1776, cap0=1960, yend=2900, leg1=(596, 705), leg2=(458, 564))   # the loop corridor behind the two hall closets


def rooms(storey=None, ghosts=False):
    return [r for r in ROOMS if (storey is None or r["storey"] == storey) and (ghosts or not r["ghost"])]


def room(name):
    return next(r for r in ROOMS if r["name"] == name)


def wall_mat(r, side):
    return SIDE_MAT.get((r["name"], side), FIN[r["fin"]][0])


def trim_mat(r):
    return FIN[r["fin"]][2] or "white"


def at(name, side, along, inset=0.0):
    """A point on one wall of a room and the direction that faces into the room: ((x, y), (dx, dy)).
    side 'x0' is the room's front (street side) wall, 'x1' its back wall, 'y0' the garage-side wall, 'y1' the far wall.
    `along` is measured from the room's low corner along that wall; inset moves the point into the room."""
    x0, y0, x1, y1 = room(name)["rect"]
    if side == "x0": return (x0 + inset, y0 + along), (1, 0)
    if side == "x1": return (x1 - inset, y0 + along), (-1, 0)
    if side == "y0": return (x0 + along, y0 + inset), (0, 1)
    return (x0 + along, y1 - inset), (0, -1)


def area_sqft(storeys=(1, 2)):
    """Gross area of the listed storeys, outside wall to outside wall."""
    return sum((BBOX[s][2] - BBOX[s][0]) * (BBOX[s][3] - BBOX[s][1]) for s in storeys) / 929.03
