"""Editor preview of the unease dial: set UNEASE (0-100) before exec, or POC_UNEASE in the environment."""
import os, unreal
v = float(globals().get("UNEASE", os.environ.get("POC_UNEASE", "0")))
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
unreal.MaterialLibrary.set_scalar_parameter_value(world, unreal.EditorAssetLibrary.load_asset("/Game/Materials/MPC_World"), "Unease", v / 100.0)
print("unease", v)
