"""Rebuild the car mesh in place (the placed actor picks up the new mesh)."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF, props_story, props_car
for mod in (L, K, props_car): importlib.reload(mod)
sm = PF.REG["car"]().save("car")
bb = sm.get_bounding_box(); print("car rebuilt", sm.get_num_triangles(0), "tris", [round(v) for v in (bb.min.x, bb.max.x, bb.min.y, bb.max.y, bb.max.z)])
