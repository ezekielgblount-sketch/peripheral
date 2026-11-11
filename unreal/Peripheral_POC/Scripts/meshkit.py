"""Mesh kit: compose simple primitives into one static mesh asset (/Game/Meshes/SM_<name>), one material slot per
surface key. Mesh-local coordinates are plain Unreal cm: +X front, +Y right, +Z up. Safe to re-run (assets are updated)."""
import math, unreal
import poc_lib as L

MESH_DIR = "/Game/Meshes"
P = unreal.GeometryScript_Primitives
Q = unreal.GeometryScript_MeshQueries
eal = unreal.EditorAssetLibrary
_eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
BASE = unreal.GeometryScriptPrimitiveOriginMode.BASE


def T(x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
    return unreal.Transform(location=unreal.Vector(x, y, z), rotation=unreal.Rotator(roll=roll, pitch=pitch, yaw=yaw))


class Kit:
    def __init__(self):
        self.m = unreal.DynamicMesh()
        self.keys = []

    def _o(self, key):
        if key not in self.keys:
            self.keys.append(key)
        o = unreal.GeometryScriptPrimitiveOptions()
        o.material_id = self.keys.index(key)
        return o

    def box(self, key, x0, y0, z0, x1, y1, z1):
        P.append_box(self.m, self._o(key), T((x0 + x1) / 2.0, (y0 + y1) / 2.0, z0), x1 - x0, y1 - y0, z1 - z0, 0, 0, 0, BASE)
        return self

    def obox(self, key, cx, cy, cz, sx, sy, sz, roll=0, pitch=0, yaw=0):
        """Rotated box given its centre and sizes."""
        P.append_box(self.m, self._o(key), T(cx, cy, cz, roll, pitch, yaw), sx, sy, sz, 0, 0, 0,
                     unreal.GeometryScriptPrimitiveOriginMode.CENTER)
        return self

    def cyl(self, key, cx, cy, z0, r, h, steps=16, roll=0, pitch=0, yaw=0):
        P.append_cylinder(self.m, self._o(key), T(cx, cy, z0, roll, pitch, yaw), r, h, steps, 0, True, BASE)
        return self

    def tube(self, key, p0, p1, r, steps=8):
        """Cylinder between two points."""
        d = unreal.Vector(p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        t = unreal.Transform(location=unreal.Vector(*p0), rotation=unreal.MathLibrary.make_rot_from_z(d))
        P.append_cylinder(self.m, self._o(key), t, r, d.length(), steps, 0, True, BASE)
        return self

    def quad(self, key, x, y0, z0, y1, z1, flip=False):
        """Flat printed image facing +X at x, spanning y0..y1 and z0..z1 (image top is +Z)."""
        tmp, tmp2 = unreal.DynamicMesh(), unreal.DynamicMesh()
        P.append_rectangle_xy(tmp, self._o(key), T(), abs(y1 - y0), z1 - z0, 0, 0)
        unreal.GeometryScript_MeshEdits.append_mesh(tmp2, tmp, T(yaw=(90 if flip else -90)))       # turn the image upright
        # the rectangle lies in XY facing +Z: stand it up so it faces +X
        unreal.GeometryScript_MeshEdits.append_mesh(self.m, tmp2, T(x, (y0 + y1) / 2.0, (z0 + z1) / 2.0, pitch=-90))
        return self

    def decal_top(self, key, x0, y0, x1, y1, z):
        """Flat printed image lying face-up at height z."""
        P.append_rectangle_xy(self.m, self._o(key), T((x0 + x1) / 2.0, (y0 + y1) / 2.0, z), x1 - x0, y1 - y0, 0, 0)
        return self

    def soft(self, key, x0, y0, z0, x1, y1, z1, steps=5, iters=6, alpha=0.4):
        """Cushion-like rounded box."""
        tmp = unreal.DynamicMesh()
        P.append_box(tmp, self._o(key), T((x0 + x1) / 2.0, (y0 + y1) / 2.0, z0), x1 - x0, y1 - y0, z1 - z0, steps, steps, steps, BASE)
        o = unreal.GeometryScriptIterativeMeshSmoothingOptions(); o.num_iterations = iters; o.alpha = alpha
        unreal.GeometryScript_MeshDeformers.apply_iterative_smoothing_to_mesh(tmp, unreal.GeometryScriptMeshSelection(), o)
        unreal.GeometryScript_Normals.recompute_normals(tmp, unreal.GeometryScriptCalculateNormalsOptions())
        unreal.GeometryScript_MeshEdits.append_mesh(self.m, tmp, T())
        return self

    def torus(self, key, cx, cy, cz, R, r, roll=0, pitch=0, major=20, minor=8):
        P.append_torus(self.m, self._o(key), T(cx, cy, cz, roll, pitch), unreal.GeometryScriptRevolveOptions(), R, r, major, minor,
                       unreal.GeometryScriptPrimitiveOriginMode.CENTER)
        return self

    def cone(self, key, cx, cy, z0, r0, r1, h, steps=16, roll=0, pitch=0):
        P.append_cone(self.m, self._o(key), T(cx, cy, z0, roll, pitch), r0, r1, h, steps, 0, True, BASE)
        return self

    def sphere(self, key, cx, cy, cz, r, steps=6, sx=1.0, sy=1.0, sz=1.0):
        t = T(cx, cy, cz); t.scale3d = unreal.Vector(sx, sy, sz)
        P.append_sphere_box(self.m, self._o(key), t, r, steps, steps, steps)
        return self

    def extrude(self, key, pts, z0, h, t=None):
        """Polygon in XY (list of (x,y)), extruded up from z0 by h."""
        tmp = unreal.DynamicMesh()
        o = self._o(key)
        vs = [unreal.Vector2D(a, b) for a, b in pts]
        P.append_simple_extrude_polygon(tmp, o, T(0, 0, z0), vs, h, 0, True, BASE)
        vol = Q.get_mesh_volume_area(tmp)
        if vol[1] < 0 if isinstance(vol, tuple) and len(vol) > 1 else False:
            tmp = unreal.DynamicMesh(); o.flip_orientation = True
            P.append_simple_extrude_polygon(tmp, o, T(0, 0, z0), vs, h, 0, True, BASE)
        unreal.GeometryScript_MeshEdits.append_mesh(self.m, tmp, t or T())
        return self

    def prism_xz(self, key, pts, y0, y1):
        """Polygon in the X-Z plane (list of (x,z)), extruded along Y from y0 to y1."""
        # build in XY (x, z) then stand it up: roll maps local Y to world Z; the extrusion then runs along -Y or +Y
        k = Kit(); k.keys = self.keys
        k.extrude(key, pts, 0, y1 - y0)
        for roll in (90, -90):
            tmp = unreal.DynamicMesh()
            unreal.GeometryScript_MeshEdits.append_mesh(tmp, k.m, T(roll=roll))
            bb = Q.get_mesh_bounding_box(tmp)
            if bb.max.z > 0.5 * max(p[1] for p in pts) and bb.max.z > 0:
                yoff = y0 - bb.min.y
                unreal.GeometryScript_MeshEdits.append_mesh(self.m, tmp, T(0, yoff, 0))
                return self
        raise RuntimeError("prism_xz could not orient")

    def revolve(self, key, path, steps=20, cx=0, cy=0, z0=0):
        """Lathe: path is a list of (radius, z) from bottom to top."""
        ro = unreal.GeometryScriptRevolveOptions()
        P.append_revolve_path(self.m, self._o(key), T(cx, cy, z0), [unreal.Vector2D(r, z) for r, z in path], ro, steps, True)
        return self

    def add(self, other, t=None):
        """Append another kit (its material keys are merged)."""
        for kname in other.keys:
            if kname not in self.keys:
                self.keys.append(kname)
        remap = [self.keys.index(kname) for kname in other.keys]
        tmp = unreal.DynamicMesh()
        unreal.GeometryScript_MeshEdits.append_mesh(tmp, other.m, T())
        if remap != list(range(len(remap))):
            for src in sorted(range(len(remap)), reverse=True):
                unreal.GeometryScript_Materials.remap_material_i_ds(tmp, src, 1000 + remap[src])
            for dst in set(remap):
                unreal.GeometryScript_Materials.remap_material_i_ds(tmp, 1000 + dst, dst)
        unreal.GeometryScript_MeshEdits.append_mesh(self.m, tmp, t or T())
        return self

    def noise(self, magnitude, frequency, seed=1):
        o = unreal.GeometryScriptPerlinNoiseOptions()
        o.base_layer.magnitude = magnitude; o.base_layer.frequency = frequency; o.base_layer.random_seed = seed
        unreal.GeometryScript_MeshDeformers.apply_perlin_noise_to_mesh2(self.m, unreal.GeometryScriptMeshSelection(), o)
        unreal.GeometryScript_Normals.recompute_normals(self.m, unreal.GeometryScriptCalculateNormalsOptions())
        return self

    def save(self, name, collide=True, mats=None, local=True):
        path = "%s/SM_%s" % (MESH_DIR, name)
        materials = [(L.mat(k, local) if isinstance(k, str) else k) for k in (mats or self.keys)]
        sm = eal.load_asset(path)
        if sm is None:
            o = unreal.GeometryScriptCreateNewStaticMeshAssetOptions()
            o.enable_collision = False
            sm = unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(self.m, path, o)
            sm = sm[0] if isinstance(sm, tuple) else sm
        co = unreal.GeometryScriptCopyMeshToAssetOptions()
        co.replace_materials = True
        co.new_materials = materials
        unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(self.m, sm, co, unreal.GeometryScriptMeshWriteLOD())
        bs = sm.get_editor_property("body_setup")
        if bs:
            bs.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
        sm.set_meta_data("poc_collide", "1" if collide else "0") if hasattr(sm, "set_meta_data") else None
        eal.save_asset(path)
        return sm


def place(sm, name, x, y, z, face=(1, 0), folder="Props", tag="prop", collide=True, shadow=True, scale=1.0, movable=False):
    """Place a kit mesh at blueprint position (x,y,z). face = blueprint (dx,dy) direction the mesh's +X should point."""
    if isinstance(sm, str):
        sm = eal.load_asset("%s/SM_%s" % (MESH_DIR, sm))
    yaw = math.degrees(math.atan2(-face[1], face[0]))
    a = _eas.spawn_actor_from_object(sm, L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
    a.set_actor_label(name); a.set_folder_path(folder); a.tags = [tag]
    if scale != 1.0:
        a.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    c = a.static_mesh_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE if movable else unreal.ComponentMobility.STATIC)
    if not collide:
        c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    c.set_cast_shadow(shadow)
    return a


PITCH = math.degrees(math.atan(5.0 / 12.0))


def gable_roof(k, x0, x1, y0, y1, z_eave, ov=45, ov_gable=30, t=12, roof="roof", gable="siding", gable_t=20):
    """Gable roof with the ridge along Y, in the kit's own coordinates. x0..x1 is the span, y0..y1 the ridge length."""
    half = (x1 - x0) / 2.0
    rise = half * 5.0 / 12.0
    xr, zr = (x0 + x1) / 2.0, z_eave + rise
    run = half + ov
    slope = run / math.cos(math.radians(PITCH))
    drop = ov * 5.0 / 12.0
    for sgn in (-1, 1):
        ex = xr + sgn * run
        cx, cz = (xr + ex) / 2.0, (zr + z_eave - drop) / 2.0 + t * 0.6
        k.obox(roof, cx, (y0 + y1) / 2.0, cz, slope, (y1 - y0) + 2 * ov_gable, t, pitch=(PITCH if sgn < 0 else -PITCH))
        k.box("white", min(ex, ex - sgn * 4), y0 - ov_gable, z_eave - drop - 12, max(ex, ex - sgn * 4), y1 + ov_gable, z_eave - drop + 8)
    k.box(roof, xr - 12, y0 - ov_gable, zr + t * 0.6 - 2, xr + 12, y1 + ov_gable, zr + t * 0.6 + 8)      # ridge cap
    if gable:
        tri = [(x0, z_eave), (x1, z_eave), (xr, zr)]
        k.prism_xz(gable, tri, y0, y0 + gable_t)
        k.prism_xz(gable, tri, y1 - gable_t, y1)
    return zr
