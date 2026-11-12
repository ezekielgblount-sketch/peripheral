"""The neighbourhood seen through the windows: neighbour houses, trees, shrubs, fences, swing set, utility poles.
Safe to re-run: rebuilds everything tagged 'hood'. Positions are blueprint cm; kit meshes are reused many times."""
import sys, math, random, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K
importlib.reload(L); importlib.reload(K)
GR = -140
L.clear("hood")
rnd = random.Random(7)


def nb_house(name, siding, w=1100, d=880, garage=1, stories=2, door="door_red"):
    """Neighbour house. Front face is the x=0 plane looking along +X; the house runs back to x=-d."""
    k = K.Kit()
    low = 400 if stories == 2 else 300
    k.box("brick", -d, -w / 2, 0, 0, w / 2, low)
    eave = low
    fx = 0
    if stories == 2:
        k.box(siding, -d, -w / 2, low, 30, w / 2, low + 260)
        eave, fx = low + 260, 30
    K.gable_roof(k, -d, fx, -w / 2, w / 2, eave, gable=siding)

    def window(x, y0, y1, z0, z1, shutters):
        s = 1 if x >= 0 else -1
        k.box("glass_dark", min(x, x + s * 2), y0, z0, max(x, x + s * 2), y1, z1)
        k.box("white", min(x, x + s * 4), y0 - 6, z0 - 8, max(x, x + s * 4), y1 + 6, z0)
        k.box("white", min(x, x + s * 4), y0 - 6, z1, max(x, x + s * 4), y1 + 6, z1 + 6)
        k.box("white", min(x, x + s * 3), (y0 + y1) / 2 - 2, z0, max(x, x + s * 3), (y0 + y1) / 2 + 2, z1)
        if shutters:
            k.box("shutter", x, y0 - 40, z0 - 4, x + 4, y0 - 6, z1 + 4)
            k.box("shutter", x, y1 + 6, z0 - 4, x + 4, y1 + 40, z1 + 4)

    if stories == 2:
        for yc in (-w / 2 + 220, 0, w / 2 - 220):
            window(fx, yc - 60, yc + 60, low + 90, low + 220, True)
            window(-d, yc - 60, yc + 60, low + 90, low + 220, False)
    window(0, -garage * 330 - 120, -garage * 330 + 120, low - 220, low - 70, stories == 1)
    window(-d, -200, -80, low - 190, low - 70, False)
    window(-d, 150, 270, low - 190, low - 70, False)
    k.box(door, 0, -garage * 40 - 45, 14, 3, -garage * 40 + 45, 217)                 # front door and stoop
    k.box("white", 0, -garage * 40 - 55, 217, 5, -garage * 40 + 55, 229)
    k.box("concrete", 0, -garage * 40 - 90, 0, 120, -garage * 40 + 90, 14)
    g0, g1 = sorted((garage * w / 2, garage * (w / 2 + 420)))                         # attached garage
    k.box("brick", -700, g0, 0, 0, g1, 270)
    K.gable_roof(k, -700, 0, g0, g1, 270, gable=siding)
    k.box("garage_door", 0, g0 + 70, 0, 3, g1 - 70, 213)
    for i in range(1, 4):
        k.box("metal_dark", 2.5, g0 + 70, i * 53 - 1, 3.4, g1 - 70, i * 53 + 1)
    k.box("concrete", 0, g0 + 50, -4, 1000, g1 - 50, 2)                              # driveway
    return k.save(name)


def tree(name, h, seed, spread=1.0):
    r = random.Random(seed)
    k = K.Kit()
    th = h * 0.42
    k.cone("bark", 0, 0, -10, 30 * spread, 16 * spread, th + 60, 12)
    c = K.Kit()
    for i in range(11):
        a, rad = i * 2.4 + r.uniform(-0.4, 0.4), r.uniform(60, 250) * spread
        px, py, pz = math.cos(a) * rad, math.sin(a) * rad, th + r.uniform(90, h * 0.5)
        k.tube("bark", (0, 0, th - 20 + i * 8), (px * 0.8, py * 0.8, pz - 30), 6, 6)
        c.sphere("leaf", px, py, pz, r.uniform(120, 200) * spread, 8, sz=r.uniform(0.65, 0.85))
    c.sphere("leaf", 0, 0, th + h * 0.36, 230 * spread, 8, sz=0.8)
    c.noise(45, 0.009, seed).noise(16, 0.035, seed + 1).noise(5, 0.11, seed + 2)
    k.add(c)
    return k.save(name)


def shrub(name, seed):
    r = random.Random(seed)
    c = K.Kit()
    for i in range(3):
        c.sphere("leaf", 0, (i - 1) * 45, 40 + r.uniform(-6, 10), r.uniform(42, 58), 7, sz=0.85)
    c.noise(10, 0.05, seed)
    return c.save(name)


def swing_set():
    k = K.Kit()
    for y in (-150, 150):
        for sg in (-1, 1):
            k.tube("metal_dark", (sg * 70, y, 0), (0, y, 222), 2.6)
        k.tube("metal_dark", (-35, y, 110), (35, y, 110), 1.6)
    k.tube("metal_dark", (0, -158, 222), (0, 158, 222), 2.8)
    for y in (-70, 60):
        for dy in (-18, 18):
            k.tube("metal", (0, y + dy, 48), (0, y + dy, 222), 0.6, 4)
        k.box("fence", -8, y - 22, 45, 8, y + 22, 48)
    return k.save("swing_set")


houses = [nb_house("nb_house_a", "nb_a", garage=1), nb_house("nb_house_b", "nb_b", garage=-1),
          nb_house("nb_house_c", "nb_c", w=1300, stories=1, door="shutter"), nb_house("nb_house_d", "siding", garage=1, door="shutter")]
trees = [tree("tree_a", 950, 1), tree("tree_b", 1150, 2, 1.2), tree("tree_c", 780, 3, 0.85)]
shrubs = [shrub("shrub_a", 11), shrub("shrub_b", 12)]
swing = swing_set()
H = dict(folder="Hood/Houses", tag="hood", collide=False)
n = 0
for i, y in enumerate((4100, 6500, -2400, -4700)):                                   # our side of the street
    K.place(houses[i % 4], "NB_same_%d" % i, -20 + rnd.uniform(-80, 80), y, GR, face=(-1, 0), **H)
for i, y in enumerate((-4800, -2500, -200, 2100, 4400, 6700)):                        # across the street
    K.place(houses[(i + 1) % 4], "NB_across_%d" % i, -3270 + rnd.uniform(-80, 80), y, GR, face=(1, 0), **H)
for i, y in enumerate((-3670, -1370, 930, 3230, 5530)):                               # behind us, backs to our yard
    K.place(houses[(i + 2) % 4], "NB_rear_%d" % i, 5300 + rnd.uniform(-80, 80), y, GR, face=(1, 0), **H)

Tk = dict(folder="Hood/Trees", tag="hood", shadow=True)
def put_tree(x, y, collide=False):
    global n
    n += 1
    a = K.place(rnd.choice(trees), "Tree_%02d" % n, x, y, GR, face=(math.cos(n * 2.4), math.sin(n * 2.4)), collide=collide,
                scale=rnd.uniform(0.85, 1.2), **Tk)
for y in range(-4700, 6800, 1150):                                                    # street trees on both verges
    if not (500 < y + 380 < 2050):                                                    # keep the low sun on our front windows
        ty = y + rnd.uniform(-150, 150) + 380
        if -80 < ty < 620:                                                            # never in the mouth of our driveway (0..545): stand it on the grass beside it
            ty = -220.0
        put_tree(-1095 + rnd.uniform(-20, 20), ty)
    put_tree(-2175 + rnd.uniform(-20, 20), y + rnd.uniform(-150, 150) + 900)
for (x, y) in ((-560, 1750), (2390, 1830), (-450, -750), (-520, 3000), (1800, 3400), (2000, -1500)):
    put_tree(x, y, collide=True)
for y in range(-5000, 7000, 520):                                                     # tree lines that close the horizon
    put_tree(3100 + rnd.uniform(-250, 250), y + rnd.uniform(-200, 200))
    put_tree(-4700 + rnd.uniform(-300, 300), y + rnd.uniform(-200, 200))
    put_tree(6300 + rnd.uniform(-200, 200), y + rnd.uniform(-200, 200))
for x in range(-6000, 6400, 560):
    put_tree(x + rnd.uniform(-200, 200), -5000 + rnd.uniform(-150, 150))
    put_tree(x + rnd.uniform(-200, 200), 6850 + rnd.uniform(-100, 100))
for i, y in enumerate(list(range(630, 1060, 95)) + list(range(1330, 1950, 95))):       # foundation shrubs along our front wall
    K.place(shrubs[i % 2], "Shrub_%02d" % i, -62, y, GR, face=(1, 0), folder="Hood/Shrubs", tag="hood", collide=False)
K.place(swing, "SwingSet", 2250, 1560, GR, face=(0, 1), folder="Hood", tag="hood")

# fences and utility poles: one mesh in world coordinates
f = K.Kit()
def B(key, x0, y0, z0, x1, y1, z1):
    f.box(key, x0 - L.OX, -(y1 - L.OY), z0, x1 - L.OX, -(y0 - L.OY), z1)
def fence_x(y, x0, x1):
    B("fence", x0, y - 1.5, GR + 8, x1, y + 1.5, GR + 172)
    B("fence", x0, y - 4, GR + 150, x1, y + 4, GR + 158)
    for x in range(int(x0), int(x1) + 1, 240):
        B("fence", x - 5, y - 5, GR, x + 5, y + 5, GR + 180)
def fence_y(x, y0, y1):
    B("fence", x - 1.5, y0, GR + 8, x + 1.5, y1, GR + 172)
    B("fence", x - 4, y0, GR + 150, x + 4, y1, GR + 158)
    for y in range(int(y0), int(y1) + 1, 240):
        B("fence", x - 5, y - 5, GR, x + 5, y + 5, GR + 180)
fence_y(2600, -4820, 6700)
for y in (-4820, -2600, 4600, 6700):                                                  # the neighbours' side fences
    fence_x(y, 500, 2600)
fence_x(-300, 790, 2600); fence_y(790, -300, -190)                                    # our back yard: wood privacy fence, with a gap by the garage for the gate
fence_x(2300, 1100, 2600); fence_y(1100, 1980, 2300)
for y in range(-4820, 6701, 2300):
    B("bark", 2630, y - 12, GR, 2654, y + 12, GR + 900)                               # utility pole and crossarm
    B("bark", 2636, y - 110, GR + 820, 2648, y + 110, GR + 832)
for dy in (-95, 0, 95):
    B("metal_dark", 2641, -4820 + dy, GR + 834, 2643, 6700 + dy, GR + 836)
fm = f.save("fences_poles")
a = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_object(fm, unreal.Vector(0, 0, 0))
a.set_actor_label("FencesPoles"); a.set_folder_path("Hood"); a.tags = ["hood"]
a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
print("hood built, trees:", n)
