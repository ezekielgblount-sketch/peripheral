"""Furnishes the whole house and yard. Safe to re-run: rebuilds everything tagged 'dress'.
The work is split by floor: dress_f1.py, dress_f2.py, dress_out.py (helpers in dress_lib.py)."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import house_plan, poc_lib, meshkit, props_furniture, props_r1, props_yard, dress_lib
for m in (house_plan, poc_lib, meshkit, dress_lib):
    importlib.reload(m)
print("cleared", dress_lib.begin("dress"))
import dress_f1, dress_f2, dress_out
for m in (dress_f1, dress_f2, dress_out):
    importlib.reload(m)
print("dressed:", sum(v for k, v in dress_lib.count.items() if not (isinstance(k, str) and k.startswith("L"))), "props")
