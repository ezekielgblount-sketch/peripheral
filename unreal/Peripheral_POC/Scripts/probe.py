import sys, importlib
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K
importlib.reload(L); importlib.reload(K)
k = K.Kit()
k.prism_xz("siding", [(0, 0), (200, 0), (100, 80)], 10, 30)
print("vol", K.Q.get_mesh_volume_area(k.m))
bb = K.Q.get_mesh_bounding_box(k.m); print(bb.min, bb.max)
k.box("brick", 0, 0, -50, 50, 50, 0).cyl("roof", 100, 0, 0, 10, 40)
sm = k.save("test_probe")
print(sm, [m.get_name() for m in [sm.get_material(i) for i in range(3)]])
k2 = K.Kit(); k2.sphere("leaf", 0, 0, 0, 100, 8).noise(30, 0.01)
print("noise ok", K.Q.get_mesh_bounding_box(k2.m).max)
