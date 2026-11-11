"""Shared helpers for building the POC house inside the Unreal Editor.

All layout numbers are in BLUEPRINT coordinates (cm): +X front to back, +Y away from the garage, +Z up.
to_ue() mirrors Y so that, walking in the front door, the up flight turns LEFT and the garage is on the right.
"""
import unreal

OX, OY = 450.0, 1150.0          # blueprint point that becomes the Unreal origin
CUBE = "/Engine/BasicShapes/Cube.Cube"
MAT_DIR = "/Game/Materials"

_eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
_cube = None
_mats = {}


def to_ue(x, y, z):
    return unreal.Vector(x - OX, -(y - OY), z)


def mat(key, local=False):
    """Surface material by key. local=True gives the variant whose texture sticks to the object (for props that move)."""
    if key.startswith("p_"):                      # printed image, e.g. p_photo_family_a
        return unreal.EditorAssetLibrary.load_asset(MAT_DIR + "/MP_" + key[2:])
    if key.startswith("m_"):                      # a purpose-built material, e.g. m_CarPaint
        return unreal.EditorAssetLibrary.load_asset(MAT_DIR + "/M_" + key[2:])
    if key == "glass":
        return unreal.EditorAssetLibrary.load_asset(MAT_DIR + "/M_Glass")
    name = ("MIL_" if local else "MI_") + key
    if name not in _mats:
        m = unreal.EditorAssetLibrary.load_asset("%s/%s" % (MAT_DIR, name))
        if m is None:
            unreal.log_warning("POC: missing material " + name)
        _mats[name] = m
    return _mats[name]


def clear(tag):
    n = 0
    for a in _eas.get_all_level_actors():
        if a.actor_has_tag(tag):
            _eas.destroy_actor(a); n += 1
    return n


def box(name, x0, y0, z0, x1, y1, z1, m, folder="Shell", tag="shell", collide=True, shadow=True):
    """Axis-aligned box from blueprint min/max corners."""
    global _cube
    if _cube is None:
        _cube = unreal.EditorAssetLibrary.load_asset(CUBE)
    if x1 - x0 <= 0.01 or y1 - y0 <= 0.01 or z1 - z0 <= 0.01:
        return None
    c = to_ue((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)
    a = _eas.spawn_actor_from_object(_cube, c)
    a.set_actor_scale3d(unreal.Vector((x1 - x0) / 100.0, (y1 - y0) / 100.0, (z1 - z0) / 100.0))
    a.set_actor_label(name)
    a.set_folder_path(folder)
    a.tags = [tag]
    smc = a.static_mesh_component
    smc.set_mobility(unreal.ComponentMobility.STATIC)
    mm = mat(m) if isinstance(m, str) else m
    if mm:
        smc.set_material(0, mm)
    if not collide:
        smc.set_collision_profile_name("NoCollision")       # saved with the level (set_collision_enabled alone is lost on reload)
    smc.set_cast_shadow(shadow)
    return a


def _segments(a0, a1, z0, z1, ops):
    """Split a wall rectangle (along-axis a, height z) around openings. Returns list of (a0,a1,z0,z1)."""
    out = []
    cur = a0
    for (o0, o1, oz0, oz1) in sorted(ops):
        if o0 > cur:
            out.append((cur, o0, z0, z1))
        if oz0 > z0:
            out.append((o0, o1, z0, oz0))       # below the opening
        if oz1 < z1:
            out.append((o0, o1, oz1, z1))       # above the opening
        cur = o1
    if cur < a1:
        out.append((cur, a1, z0, z1))
    return out


def wallx(name, x0, x1, ya, yb, z0, z1, m_lo, m_hi, ops=(), folder="Shell", tag="shell"):
    """Wall whose thickness runs x0..x1 and whose length runs along Y. m_lo faces -X, m_hi faces +X."""
    xm = (x0 + x1) / 2.0
    for i, (a0, a1, s0, s1) in enumerate(_segments(ya, yb, z0, z1, ops)):
        box("%s_%d_a" % (name, i), x0, a0, s0, xm, a1, s1, m_lo, folder, tag)
        box("%s_%d_b" % (name, i), xm, a0, s0, x1, a1, s1, m_hi, folder, tag)


def wally(name, y0, y1, xa, xb, z0, z1, m_lo, m_hi, ops=(), folder="Shell", tag="shell"):
    """Wall whose thickness runs y0..y1 and whose length runs along X. m_lo faces -Y, m_hi faces +Y."""
    ym = (y0 + y1) / 2.0
    for i, (a0, a1, s0, s1) in enumerate(_segments(xa, xb, z0, z1, ops)):
        box("%s_%d_a" % (name, i), a0, y0, s0, a1, ym, s1, m_lo, folder, tag)
        box("%s_%d_b" % (name, i), a0, ym, s0, a1, y1, s1, m_hi, folder, tag)


def slab(name, x0, y0, x1, y1, ztop, m_floor, m_ceil, thick=15.0, folder="Shell", tag="shell"):
    """Floor slab: top half shows the floor finish, bottom half shows the ceiling finish of the room below."""
    zm = ztop - thick / 2.0
    box(name + "_f", x0, y0, zm, x1, y1, ztop, m_floor, folder, tag)
    box(name + "_c", x0, y0, ztop - thick, x1, y1, zm, m_ceil, folder, tag)


def steps(name, axis, start, sign, lane0, lane1, n, rise, tread, z_first_top, m, solid_to=None, soffit=None,
          soffit_before=None, folder="Shell/Stairs", tag="shell"):
    """n treads. axis 'x' or 'y' is the travel axis; sign is +1/-1 travel direction; lane0..lane1 is the stair width.
    Tread i top = z_first_top + rise*i (rise may be negative for a descending flight).
    Each step is solid down to solid_to, unless its travel coordinate is below soffit_before, where it hangs `soffit` cm."""
    for i in range(n):
        a0 = start + sign * tread * i
        a1 = start + sign * tread * (i + 1)
        lo, hi = min(a0, a1), max(a0, a1)
        top = z_first_top + rise * i
        bottom = solid_to
        if soffit is not None and soffit_before is not None and lo < soffit_before:
            bottom = top - soffit
        if axis == "x":
            box("%s_%02d" % (name, i), lo, lane0, bottom, hi, lane1, top, m, folder, tag)
        else:
            box("%s_%02d" % (name, i), lane0, lo, bottom, lane1, hi, top, m, folder, tag)
