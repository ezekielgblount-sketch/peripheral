"""Props for the second anomaly pass: ordinary things that read as a person in a dim corner (false positives),
things that change while nobody is looking, and the family snapshots.
Every prop: origin on the floor, back against x=0, front toward +X, centred on Y (unless noted)."""
import math, unreal
import meshkit as K
from props_furniture import prop, frame, carton, drape, floor_lamp, chair_wood
T = K.T


# ---------------- false positives: person-height, person-width, in a place where a person could stand ----------------
@prop
def draped_boxes():
    """Boxes stacked under a dust sheet. The top box is small, so the sheet hangs like a head and shoulders."""
    k = K.Kit()
    c = K.Kit(); c.soft("fabric_white", 2, -30, 0, 52, 30, 138, 6, 5, 0.35)                 # shoulders and body
    c.soft("fabric_white", 14, -13, 132, 40, 13, 170, 5, 5, 0.4); c.noise(2.6, 0.045, 3); k.add(c)
    k.box("cardboard", 6, -26, 0, 48, 26, 4)
    return k


@prop
def mop_bucket():
    """A string mop stood head-up in its bucket: a thin body with a ragged head at face height."""
    k = K.Kit()
    k.cone("plastic_yellow", 22, 0, 0, 15, 18, 28, 16); k.tube("wood_light", (22, 0, 4), (16, 0, 150), 1.5, 8)
    c = K.Kit(); c.soft("fabric_cream", 4, -12, 138, 28, 12, 172, 4, 4, 0.45); c.noise(2.4, 0.12, 5); k.add(c)
    for i in range(9):
        a = i * 0.7
        k.tube("fabric_cream", (16 + 9 * math.cos(a), 9 * math.sin(a), 150), (16 + 13 * math.cos(a), 13 * math.sin(a), 118 + (i % 3) * 7), 1.3, 5)
    return k


@prop
def coat_chair():
    """A kitchen chair with a heavy coat hung over its back and a cap on the post."""
    k = chair_wood()
    c = K.Kit(); c.soft("fabric_brown", -4, -24, 34, 8, 24, 100, 5, 5, 0.35); c.noise(1.6, 0.06, 2); k.add(c)
    k.soft("fabric_brown", -5, -30, 46, 5, -22, 92, 3, 3); k.soft("fabric_brown", -5, 22, 46, 5, 30, 92, 3, 3)
    k.soft("fabric_navy", -8, -9, 98, 9, 9, 108, 4, 4, 0.4)
    return k


@prop
def tall_plant():
    """A leggy indoor tree: bare trunk, one dense clump of leaves at head height."""
    k = K.Kit()
    k.cone("enamel", 20, 0, 0, 15, 19, 30, 16); k.cyl("soil", 20, 0, 28, 17, 2, 16)
    k.tube("bark", (20, 0, 28), (17, 3, 112), 2.2, 8); k.tube("bark", (17, 3, 112), (21, -2, 150), 1.8, 8)
    c = K.Kit(); c.sphere("leaf", 20, 0, 158, 19, 6, sz=1.15); c.sphere("leaf", 20, -22, 128, 10, 5); c.sphere("leaf", 20, 22, 128, 10, 5)
    c.noise(3.2, 0.09, 4); k.add(c)
    return k


@prop
def box_stack_tall():
    """Three moving boxes, each smaller than the one below, with a lampshade left on top."""
    k = K.Kit()
    k.add(carton(52, 46, 62)); k.add(carton(44, 40, 52), T(4, 0, 62, yaw=7)); k.add(carton(34, 30, 36), T(9, 0, 114, yaw=-5))
    k.cone("fabric_cream", 26, 0, 150, 13, 9, 20, 14)
    return k


@prop
def curtain_bunched():
    """A long curtain pushed to one side and bunched: as wide as shoulders, with shoes left under its hem."""
    k = drape(46, 196, "fabric_hunter", 5, 13)
    k.soft("black", 6, -14, 0, 26, -3, 8, 3, 3); k.soft("black", 6, 3, 0, 26, 14, 8, 3, 3)
    return k


# ---------------- things that are different when you come back ----------------
@prop
def floor_lamp_lean():
    """The same floor lamp, leaning as if something brushed past it."""
    k = K.Kit(); k.add(floor_lamp(), T(0, 0, 0, roll=11))
    k.keys = [{"lamp_on": "lamp_off", "lamp_shade": "shade_unlit"}.get(x, x) for x in k.keys]          # unlit, like the lamp it replaces
    return k


@prop
def frame_portrait():
    return frame("photo_portrait_matching", 40, 32)


@prop
def frame_portrait_turned():
    return frame("photo_portrait_turned", 40, 32)


def stand_frame(name, w, h, key="wood_dark"):
    """A frame standing on a shelf, tilted back on its strut (origin under its front edge)."""
    k = K.Kit(); k.add(frame(name, w, h, key), T(4, 0, h / 2.0 + 3, pitch=12)); k.obox(key, 0, 0, h * 0.3, 1, 4, h * 0.62, pitch=-22)
    return k


@prop
def frame_stand_wedding():
    return stand_frame("photo_wedding", 16, 20, "brass")


@prop
def frame_facedown():
    """The same standing frame, lying on its face."""
    k = K.Kit(); k.box("brass", 0, -11, 0, 26, 11, 2.2); k.box("black", 1, -10, 2.2, 25, 10, 2.5); k.obox("brass", 13, 0, 3.2, 14, 4, 0.8)
    return k


@prop
def sign_post(print_name="sign_sold_a"):
    """A realtor's post with a hanging sign, both sides printed (origin at the post foot, sign faces +X and -X)."""
    k = K.Kit()
    k.box("white", -4, -4, 0, 4, 4, 190); k.box("white", -4, -4, 180, 4, 96, 188)
    for y in (22, 78):
        k.tube("metal", (0, y, 180), (0, y, 170), 0.5, 5)
    k.box("white", -1, 12, 104, 1, 88, 170)
    k.quad("p_" + print_name, 1.2, 14, 108, 86, 166); k.quad("p_" + print_name, -1.2, 14, 108, 86, 166, flip=True)
    return k


@prop
def sign_sold():
    return sign_post("sign_sold_a")


@prop
def sign_sold_b():
    return sign_post("sign_sold_b")


@prop
def cabinet_door_ajar():
    """One upper-cabinet door standing open at a right angle (origin at its hinge edge, bottom)."""
    k = K.Kit(); k.box("oak", 0, 0, 0, 36, 1.8, 70); k.cyl("brass", 30, 1.8, 10, 1.1, 2.5, 8, roll=-90)
    return k


@prop
def tap_stream():
    """Water running from a tap into a basin: a thin clear column (origin at the spout)."""
    k = K.Kit(); k.cyl("plastic_clear", 0, 0, -18, 0.55, 18, 8); k.cyl("plastic_clear", 0, 0, -18.4, 3.2, 0.4, 12)
    return k


@prop
def empty_spot():
    """Nothing to see: what a place looks like when nobody is standing in it."""
    k = K.Kit(); k.box("black", -0.05, -0.05, 0, 0.05, 0.05, 0.1)
    return k


# ---------------- family snapshots ----------------
SNAPS = ("bday", "bike", "xmas", "dock", "beach", "driveway", "baby", "yard")
for _n in SNAPS:
    def _mk(n=_n):
        def f():
            return frame("photo_" + n, 22, 17, ("wood_dark", "brass", "white", "oak")[SNAPS.index(n) % 4])
        f.__name__ = "frame_snap_" + n
        return f
    prop(_mk())
    def _mk2(n=_n):
        def f():
            k = K.Kit(); k.quad("p_photo_" + n, 0.25, -6.5, -5, 6.5, 5); return k           # a loose print for the fridge or a corkboard
        f.__name__ = "snap_" + n
        return f
    prop(_mk2())


# ---------------- someone at a window ----------------
def void_material():
    """M_Void: flat, unlit, almost black. Daylight and reflections do not touch it, so it reads as a hole in the picture."""
    eal, mel = unreal.EditorAssetLibrary, unreal.MaterialEditingLibrary
    p = "/Game/Materials/M_Void"
    m = eal.load_asset(p) or unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_Void", "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
    mel.delete_all_material_expressions(m)
    c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -300, 0); c.set_editor_property("constant", unreal.LinearColor(0.004, 0.004, 0.005, 1))
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT); m.set_editor_property("two_sided", True)
    mel.recompile_material(m); eal.save_asset(p)


@prop
def figure_window():
    """Head and shoulders, flat, to stand just outside a pane: from the yard it is someone inside, close to the glass (origin at the sill)."""
    void_material()
    k = K.Kit()
    k.box("m_Void", 0, -19, 0, 0.6, 19, 56); k.box("m_Void", 0, -26, 16, 0.6, -19, 52); k.box("m_Void", 0, 19, 16, 0.6, 26, 52)
    k.box("m_Void", 0, -5, 56, 0.6, 5, 66); k.sphere("m_Void", 0.3, 0, 77, 11.5, 6, sx=0.03, sz=1.12)
    return k


@prop
def entity_void():
    """The standing figure in the flat black, for daylight."""
    import props_shadow
    void_material()
    k = props_shadow.figure(False); k.keys = ["m_Void"] * len(k.keys)
    return k


# ---------------- the home video ----------------
def home_video_material():
    """M_HomeVideo: plays the sixteen frames of /Game/Prints/video_sheet (4 x 4) at four frames a second, lit like a tube, with scan lines."""
    eal, mel = unreal.EditorAssetLibrary, unreal.MaterialEditingLibrary
    p = "/Game/Materials/M_HomeVideo"
    m = eal.load_asset(p) or unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_HomeVideo", "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
    mel.delete_all_material_expressions(m)
    E = lambda cls, x, y: mel.create_material_expression(m, cls, x, y)
    C = mel.connect_material_expressions
    def const(v, x, y):
        c = E(unreal.MaterialExpressionConstant, x, y); c.set_editor_property("r", v); return c
    def op(cls, a, b, x, y):
        o = E(cls, x, y); C(a, "", o, "A"); C(b, "", o, "B"); return o
    t = op(unreal.MaterialExpressionMultiply, E(unreal.MaterialExpressionTime, -1700, 0), const(4.0, -1700, 100), -1500, 0)
    fr = E(unreal.MaterialExpressionFloor, -1100, 0); C(op(unreal.MaterialExpressionFmod, t, const(16.0, -1500, 150), -1300, 0), "", fr, "")
    col = op(unreal.MaterialExpressionFmod, fr, const(4.0, -1100, 150), -900, 0)
    row = E(unreal.MaterialExpressionFloor, -700, 200); C(op(unreal.MaterialExpressionDivide, fr, const(4.0, -1100, 250), -900, 200), "", row, "")
    uv = E(unreal.MaterialExpressionTextureCoordinate, -1100, 400)
    mu = E(unreal.MaterialExpressionComponentMask, -900, 400); mu.set_editor_property("r", True); mu.set_editor_property("g", False); C(uv, "", mu, "")
    mv = E(unreal.MaterialExpressionComponentMask, -900, 500); mv.set_editor_property("r", False); mv.set_editor_property("g", True); C(uv, "", mv, "")
    u = op(unreal.MaterialExpressionMultiply, op(unreal.MaterialExpressionAdd, mu, col, -500, 100), const(0.25, -700, 0), -300, 100)
    v = op(unreal.MaterialExpressionMultiply, op(unreal.MaterialExpressionAdd, mv, row, -500, 300), const(0.25, -700, 100), -300, 300)
    ap = op(unreal.MaterialExpressionAppendVector, u, v, -100, 200)
    tx = E(unreal.MaterialExpressionTextureSample, 100, 200); tx.set_editor_property("texture", eal.load_asset("/Game/Prints/video_sheet")); C(ap, "", tx, "UVs")
    sn = E(unreal.MaterialExpressionSine, -100, 500); C(op(unreal.MaterialExpressionMultiply, mv, const(120.0, -500, 500), -300, 500), "", sn, "")
    lines = op(unreal.MaterialExpressionAdd, op(unreal.MaterialExpressionMultiply, sn, const(0.4, -100, 600), 100, 500), const(4.5, -100, 700), 300, 500)
    out = E(unreal.MaterialExpressionMultiply, 500, 300); C(tx, "RGB", out, "A"); C(lines, "", out, "B")
    mel.connect_material_property(out, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    mel.recompile_material(m); eal.save_asset(p)


@prop
def tv_video_screen():
    """The picture on the old television's tube: place it exactly where the crt_tv prop stands."""
    home_video_material()
    k = K.Kit(); k.quad("m_HomeVideo", 51.4, -29, 9, 13, 43)
    return k
