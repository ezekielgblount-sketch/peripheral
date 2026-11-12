"""Builds (or rebuilds) every prop mesh in the registry. Pass names in POC_PROPS env to limit."""
import sys, os, importlib, traceback, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF
importlib.reload(L); importlib.reload(K); importlib.reload(PF)
import props_small as PS
importlib.reload(PS)
import props_90s as P9
importlib.reload(P9)
import props_home as PH
importlib.reload(PH)
import props_lived as PL
importlib.reload(PL)
import props_story as PST
importlib.reload(PST)
try:
    import props_pool as PP
    importlib.reload(PP)
except ImportError:
    pass
import props_loop, props_r1, props_yard
importlib.reload(props_loop); importlib.reload(props_r1); importlib.reload(props_yard)
ONLY = [m.strip() for m in os.environ.get('POC_PROPS', '').split(',') if m.strip()] or globals().get('ONLY')
bad = []
for name in sorted(PF.REG):
    if ONLY and name not in ONLY and getattr(PF.REG[name], '__module__', '') not in ONLY:
        continue
    try:
        PF.get(name, rebuild=True)
    except Exception as e:
        bad.append((name, traceback.format_exc().splitlines()[-1]))
print("props built:", len(PF.REG) - len(bad), "failed:", bad)
