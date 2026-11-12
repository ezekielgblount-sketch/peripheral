"""Builds Jack's body: /Game/Jack/SK_Jack, a skinned mesh on Epic's mannequin skeleton so it can use the motion-captured
walk, idle and crouch animations that ship with the engine (MoverExamples plugin).

No MetaHuman (needs an Epic sign-in). The body starts as a copy of Epic's plain mannequin and is reshaped: clothes are
pushed out from the body and smoothed so the mannequin's panel lines are gone, the scalp is roughed up into hair, a hood
is added behind the neck, and every triangle gets one of six materials (skin, stubble, hair, hoodie, jeans, sneakers).
Safe to re-run."""
import math, unreal

SRC = "/MoverExamples/Characters/Mannequins/Meshes/SKM_Manny_Simple"
DIR, NAME = "/Game/Jack", "SK_Jack"
AU, BW, Q = unreal.GeometryScript_AssetUtils, unreal.GeometryScript_BoneWeights, unreal.GeometryScript_MeshQueries
LS, ED, MT = unreal.GeometryScript_List, unreal.GeometryScript_MeshEdits, unreal.GeometryScript_Materials
NR, DF, SEL = unreal.GeometryScript_Normals, unreal.GeometryScript_MeshDeformers, unreal.GeometryScript_MeshSelection
eal, mel = unreal.EditorAssetLibrary, unreal.MaterialEditingLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
SKIN, STUB, HAIR, HOOD, JEAN, SHOE = range(6)
SLICES = ()          # plane slices broke the skinning, so the hem and collar follow the existing triangles
COL = {SKIN: ((0.42, 0.25, 0.18), 0.55, None), STUB: ((0.27, 0.17, 0.125), 0.7, None), HAIR: ((0.05, 0.03, 0.018), 0.6, None),
       HOOD: ((0.13, 0.135, 0.14), 0.95, "carpet_plush"), JEAN: ((0.035, 0.06, 0.12), 0.85, "carpet_worn"),
       SHOE: ((0.55, 0.54, 0.50), 0.6, None)}
MN = {SKIN: "skin", STUB: "stubble", HAIR: "hair", HOOD: "hoodie", JEAN: "jeans", SHOE: "shoes"}


def materials():
    """One small master (colour x optional cloth texture) flagged for skinned meshes, and an instance per part."""
    path = DIR + "/M_Jack"
    m = eal.load_asset(path)
    if not m:
        m = at.create_asset("M_Jack", DIR, unreal.Material, unreal.MaterialFactoryNew())
        E = lambda cls, x, y: mel.create_material_expression(m, cls, x, y)
        c = E(unreal.MaterialExpressionVectorParameter, -700, 0); c.set_editor_property("parameter_name", "Color")
        t = E(unreal.MaterialExpressionTextureSampleParameter2D, -700, 250); t.set_editor_property("parameter_name", "Cloth")
        t.set_editor_property("texture", eal.load_asset("/Game/Textures/T_carpet_plush_BC"))
        uv = E(unreal.MaterialExpressionTextureCoordinate, -950, 250); uv.set_editor_property("u_tiling", 7.0); uv.set_editor_property("v_tiling", 7.0)
        mel.connect_material_expressions(uv, "", t, "UVs")
        amt = E(unreal.MaterialExpressionScalarParameter, -700, 520); amt.set_editor_property("parameter_name", "ClothAmount")
        d = E(unreal.MaterialExpressionDesaturation, -480, 250); mel.connect_material_expressions(t, "RGB", d, "")
        one = E(unreal.MaterialExpressionConstant, -480, 420); one.set_editor_property("r", 0.5)
        lerp = E(unreal.MaterialExpressionLinearInterpolate, -300, 300)
        mel.connect_material_expressions(one, "", lerp, "A"); mel.connect_material_expressions(d, "", lerp, "B"); mel.connect_material_expressions(amt, "", lerp, "Alpha")
        mul = E(unreal.MaterialExpressionMultiply, -120, 100); mel.connect_material_expressions(c, "", mul, "A"); mel.connect_material_expressions(lerp, "", mul, "B")
        two = E(unreal.MaterialExpressionConstant, -120, 300); two.set_editor_property("r", 2.0)
        mul2 = E(unreal.MaterialExpressionMultiply, 60, 150); mel.connect_material_expressions(mul, "", mul2, "A"); mel.connect_material_expressions(two, "", mul2, "B")
        mel.connect_material_property(mul2, "", unreal.MaterialProperty.MP_BASE_COLOR)
        r = E(unreal.MaterialExpressionScalarParameter, -120, 500); r.set_editor_property("parameter_name", "Rough"); r.set_editor_property("default_value", 0.8)
        mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
        m.set_editor_property("used_with_skeletal_mesh", True)
        mel.recompile_material(m); eal.save_asset(path)
    out = []
    for k in range(6):
        ip = "%s/MI_Jack_%s" % (DIR, MN[k])
        mi = eal.load_asset(ip) or at.create_asset("MI_Jack_" + MN[k], DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        col, rough, cloth = COL[k]
        mel.set_material_instance_parent(mi, m)
        mel.set_material_instance_vector_parameter_value(mi, "Color", unreal.LinearColor(col[0], col[1], col[2], 1))
        mel.set_material_instance_scalar_parameter_value(mi, "Rough", rough)
        mel.set_material_instance_scalar_parameter_value(mi, "ClothAmount", 1.0 if cloth else 0.0)
        if cloth:
            mel.set_material_instance_texture_parameter_value(mi, "Cloth", eal.load_asset("/Game/Textures/T_%s_BC" % cloth))
        eal.save_asset(ip); out.append(mi)
    return out


def rnd(i):
    x = math.sin(i * 12.9898) * 43758.5453
    return x - math.floor(x)


def build():
    src = unreal.load_asset(SRC)
    dm = unreal.DynamicMesh()
    AU.copy_mesh_from_skeletal_mesh(src, dm, unreal.GeometryScriptCopyMeshFromAssetOptions(), unreal.GeometryScriptMeshReadLOD())
    prof = unreal.GeometryScriptBoneWeightProfile()
    bones = BW.get_all_bones_info(dm)[1]
    bname = {b.index: str(b.name) for b in bones}
    bpos = {str(b.name): b.world_transform.translation for b in bones}
    for z in SLICES:      # clean cut lines for the hem and the collar
        po = unreal.GeometryScriptMeshPlaneSliceOptions(); po.fill_holes = False; po.fill_spans = False; po.gap_width = 0.0
        unreal.GeometryScript_MeshBooleans.apply_mesh_plane_slice(dm, unreal.Transform(unreal.Vector(0, 0, z)), po)
    P = LS.convert_vector_list_to_array(Q.get_all_vertex_positions(dm, False)[1])
    N = LS.convert_vector_list_to_array(NR.get_mesh_per_vertex_normals(dm, True)[1])
    nv = len(P)
    head, neck = bpos["head"], bpos["neck_01"]
    top = max(p.z for p in P)
    print("verts", nv, "top", round(top, 1), "head", round(head.y, 1), round(head.z, 1), "neck", round(neck.z, 1), "pelvis", round(bpos["pelvis"].z, 1))
    hem = bpos["pelvis"].z - 6.0                         # the hoodie hangs below the belt line
    reg, off = [SKIN] * nv, [0.0] * nv
    for i in range(nv):
        w = BW.get_largest_vertex_bone_weight(dm, i, prof)[1]
        b = bname.get(w.bone_index, "")
        p = P[i]
        if b.startswith(("foot", "ball")) or (b.startswith("calf") and p.z < 9.0):
            reg[i], off[i] = SHOE, 0.9 if p.z > 2.0 else 0.2
        elif b.startswith(("thigh", "calf")) or (b.startswith("pelvis") and p.z < hem):
            reg[i], off[i] = JEAN, 1.3 if b.startswith("thigh") or b.startswith("pelvis") else 2.3
        elif b.startswith(("pelvis", "spine", "clavicle")):
            reg[i], off[i] = HOOD, 1.5 if p.z > hem + 10 else 2.6
        elif b.startswith("upperarm"):
            reg[i], off[i] = HOOD, 1.4
        elif b.startswith("lowerarm"):
            reg[i], off[i] = HOOD, 1.3
        elif b.startswith("neck"):
            if p.z < neck.z + 2.5:
                reg[i], off[i] = HOOD, 2.2            # collar
        elif b.startswith("head"):
            front = p.y - head.y                        # +Y is the way he faces
            line = head.z + 7.0 + max(-9.0, min(9.0, front)) * 0.95 - abs(p.x - head.x) * 0.25
            if p.z > line:
                reg[i], off[i] = HAIR, 1.3 + 1.6 * rnd(i) + (1.2 if p.z > top - 4 else 0.0)
            elif front > 1.0 and p.z < head.z + 2.5:
                reg[i] = STUB
    # the mannequin's face is a visor plate: smooth it flat first, then push a simple face into it
    face = [i for i in range(nv) if reg[i] in (SKIN, STUB) and P[i].z > neck.z + 2.5 and abs(P[i].x) < 14]
    fs = [x for x in SEL.convert_index_array_to_mesh_selection(dm, face, unreal.GeometryScriptMeshSelectionType.VERTICES) if isinstance(x, unreal.GeometryScriptMeshSelection)][0]
    fo = unreal.GeometryScriptIterativeMeshSmoothingOptions(); fo.num_iterations = 30; fo.alpha = 0.4
    DF.apply_iterative_smoothing_to_mesh(dm, fs, fo)
    P = LS.convert_vector_list_to_array(Q.get_all_vertex_positions(dm, False)[1])
    N = LS.convert_vector_list_to_array(NR.get_mesh_per_vertex_normals(dm, True)[1])
    g = lambda dx, dz, sx, sz: math.exp(-(dx * dx) / (2 * sx * sx) - (dz * dz) / (2 * sz * sz))
    ez, nz, mz = head.z + 8.0, head.z + 4.6, head.z + 1.2          # eye line, nose tip, mouth
    fwd = {}
    for i in face:
        p = P[i]
        if p.y - head.y < 3.0:
            continue
        d = 2.1 * g(p.x, p.z - nz, 1.25, 1.5) + 0.9 * g(p.x, p.z - (nz + 2.6), 0.9, 2.0)            # nose and its bridge
        d -= 1.0 * (g(p.x - 3.1, p.z - ez, 1.5, 0.9) + g(p.x + 3.1, p.z - ez, 1.5, 0.9))             # eye sockets
        d += 0.55 * g(0, p.z - (ez + 1.7), 1, 0.8) * (1 if abs(p.x) < 6.5 else 0)                    # brow
        d -= 0.35 * g(p.x, p.z - mz, 2.4, 0.35)                                                      # mouth line
        d += 0.5 * g(p.x, p.z - (mz - 3.2), 2.2, 1.3)                                                # chin
        fwd[i] = d
    new = [unreal.Vector(P[i].x + N[i].x * off[i], P[i].y + N[i].y * off[i] + fwd.get(i, 0.0), P[i].z + N[i].z * off[i]) for i in range(nv)]
    ED.set_all_mesh_vertex_positions(dm, LS.convert_array_to_vector_list(new))
    # smooth the clothes so the mannequin's panel grooves disappear; leave skin, hands and hair alone
    cloth = [i for i in range(nv) if reg[i] in (HOOD, JEAN)]
    sel = [x for x in SEL.convert_index_array_to_mesh_selection(dm, cloth, unreal.GeometryScriptMeshSelectionType.VERTICES) if isinstance(x, unreal.GeometryScriptMeshSelection)][0]
    so = unreal.GeometryScriptIterativeMeshSmoothingOptions(); so.num_iterations = 28; so.alpha = 0.4
    DF.apply_iterative_smoothing_to_mesh(dm, sel, so)
    # materials per triangle
    T = LS.convert_triangle_list_to_array(Q.get_all_triangle_indices(dm, False)[1])
    mids = []
    for t in T:
        r = (reg[t.x], reg[t.y], reg[t.z])
        mids.append(max(set(r), key=r.count) if r.count(r[0]) < 3 else r[0])
    MT.enable_material_i_ds(dm)
    MT.set_all_triangle_material_i_ds(dm, LS.convert_array_to_index_list(mids, unreal.GeometryScriptIndexType.MATERIAL_ID))
    NR.recompute_normals(dm, unreal.GeometryScriptCalculateNormalsOptions())
    return dm, src


def save(dm, src):
    mats = materials()
    path = "%s/%s" % (DIR, NAME)
    sk = eal.load_asset(path)
    if not sk:                       # a duplicate of Epic's mesh keeps its bone list and order exactly; a new asset built
        sk = eal.duplicate_asset(SRC, path)      # from the skeleton alone put some leg vertices on the wrong bones
    o = unreal.GeometryScriptCopyMeshToAssetOptions(); o.replace_materials = True; o.new_materials = mats
    o.new_material_slot_names = [MN[k] for k in range(6)]; o.emit_transaction = False
    r = AU.copy_mesh_to_skeletal_mesh(dm, sk, o, unreal.GeometryScriptMeshWriteLOD())
    ss = unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem)        # the copy still has Epic's distance versions
    n = ss.get_lod_count(sk)
    if n > 1:
        print("removed distance versions", ss.remove_lo_ds(sk, list(range(1, n))) if hasattr(ss, "remove_lo_ds") else ss.remove_lods(sk, list(range(1, n))))
    print("saved", r, sk)
    eal.save_asset(path)
    return sk


if __name__ == "__main__":
    if not eal.does_directory_exist(DIR):
        eal.make_directory(DIR)
    d, s = build()
    k = save(d, s)
    b = k.get_bounds(); print("bounds", b.origin, b.box_extent, [m.material_slot_name for m in k.materials])


def arms():
    """First-person forearms: each arm of SK_Jack cut out as a plain mesh, elbow at the origin, hand along +X, thumb side +Y.
    BP_Arms holds them in front of the camera while Jack carries, pushes, inspects or uses something."""
    src = eal.load_asset("%s/%s" % (DIR, NAME))
    mats = materials()
    for side in ("r", "l"):
        dm = unreal.DynamicMesh()
        AU.copy_mesh_from_skeletal_mesh(src, dm, unreal.GeometryScriptCopyMeshFromAssetOptions(), unreal.GeometryScriptMeshReadLOD())
        prof = unreal.GeometryScriptBoneWeightProfile()
        bones = BW.get_all_bones_info(dm)[1]
        bname = {b.index: str(b.name) for b in bones}
        bpos = {str(b.name): b.world_transform.translation for b in bones}
        P = LS.convert_vector_list_to_array(Q.get_all_vertex_positions(dm, False)[1])
        keep = []
        for i in range(len(P)):
            b = bname.get(BW.get_largest_vertex_bone_weight(dm, i, prof)[1].bone_index, "")
            keep.append(b.endswith("_" + side) and any(k in b for k in ("upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky")))
        T = LS.convert_triangle_list_to_array(Q.get_all_triangle_indices(dm, False)[1])
        drop = [t for t, v in enumerate(T) if not (keep[v.x] and keep[v.y] and keep[v.z])]
        ED.delete_triangles_from_mesh(dm, LS.convert_array_to_index_list(drop, unreal.GeometryScriptIndexType.TRIANGLE))
        elbow, hand = bpos["lowerarm_" + side], bpos["hand_" + side]
        axis = unreal.Vector(hand.x - elbow.x, hand.y - elbow.y, hand.z - elbow.z).normal()
        rot = unreal.MathLibrary.make_rot_from_xy(axis, unreal.Vector(0, 1, 0))          # +Y is the way the body faces
        new = [unreal.MathLibrary.less_less_vector_rotator(unreal.Vector(p.x - elbow.x, p.y - elbow.y, p.z - elbow.z), rot) for p in P]
        ED.set_all_mesh_vertex_positions(dm, LS.convert_array_to_vector_list(new))
        NR.recompute_normals(dm, unreal.GeometryScriptCalculateNormalsOptions())
        path = "/Game/Meshes/SM_jack_arm_" + side
        sm = eal.load_asset(path)
        if sm is None:
            o = unreal.GeometryScriptCreateNewStaticMeshAssetOptions(); o.enable_collision = False
            sm = unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm, path, o)
            sm = sm[0] if isinstance(sm, tuple) else sm
        co = unreal.GeometryScriptCopyMeshToAssetOptions(); co.replace_materials = True; co.new_materials = mats
        AU.copy_mesh_to_static_mesh(dm, sm, co, unreal.GeometryScriptMeshWriteLOD())
        eal.save_asset(path)
        b = sm.get_bounds(); print("arm", side, [round(v) for v in b.origin.to_tuple()], [round(v) for v in b.box_extent.to_tuple()])


if __name__ == "__main__":
    arms()
