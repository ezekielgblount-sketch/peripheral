import unreal
unreal.log("POC_PROBE engine=" + unreal.SystemLibrary.get_engine_version())
for cv in ["r.DynamicGlobalIlluminationMethod","r.ReflectionMethod","r.Shadow.Virtual.Enable","r.Nanite.ProjectEnabled"]:
    unreal.log("POC_PROBE %s=%s" % (cv, unreal.SystemLibrary.get_console_variable_int_value(cv)))
unreal.log("POC_PROBE geomscript=" + str(hasattr(unreal, "GeometryScript_MeshPrimitiveFunctions") or hasattr(unreal, "GeometryScriptLibrary_MeshPrimitiveFunctions")))
