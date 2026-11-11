"""Builds (or rebuilds) every prop mesh in the registry. Pass names in POC_PROPS env to limit."""
import sys, os, importlib, traceback, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF
importlib.reload(L); importlib.reload(K); importlib.reload(PF)
import props_small as PS
importlib.reload(PS)
bad = []
for name in sorted(PF.REG):
    try:
        PF.get(name, rebuild=True)
    except Exception as e:
        bad.append((name, traceback.format_exc().splitlines()[-1]))
print("props built:", len(PF.REG) - len(bad), "failed:", bad)
