"""Reliable screenshots from inside the editor using a SceneCapture2D (works even when the editor window is in the background).
begin() starts a camera, tick() re-renders it on later editor ticks so Lumen lighting settles, end() saves the picture."""
import unreal
import poc_lib as L

_eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
if not hasattr(unreal, "_poc_caps"):
    unreal._poc_caps = {}


def _world():
    return unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


def begin(name, pos, target, fov=95.0, ev=None, w=1600, h=900, ue_coords=False):
    p = unreal.Vector(*pos) if ue_coords else L.to_ue(*pos)
    t = unreal.Vector(*target) if ue_coords else L.to_ue(*target)
    cap = _eas.spawn_actor_from_class(unreal.SceneCapture2D, p, unreal.MathLibrary.find_look_at_rotation(p, t))
    cap.tags = ["tmp_capture"]
    c = cap.capture_component2d
    rt = unreal.RenderingLibrary.create_render_target2d(_world(), w, h, unreal.TextureRenderTargetFormat.RTF_RGBA8)
    c.set_editor_property("texture_target", rt)
    c.set_editor_property("capture_source", unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
    c.set_editor_property("fov_angle", float(fov))
    c.set_editor_property("capture_every_frame", False)
    c.set_editor_property("capture_on_movement", False)
    c.set_editor_property("always_persist_rendering_state", True)
    pps = c.get_editor_property("post_process_settings")
    over = {"motion_blur_amount": 0.0, "auto_exposure_speed_up": 20.0, "auto_exposure_speed_down": 20.0}
    if ev is not None:      # fixed exposure, used when judging lighting levels by eye
        over.update({"auto_exposure_method": unreal.AutoExposureMethod.AEM_MANUAL, "auto_exposure_bias": float(ev),
                     "auto_exposure_apply_physical_camera_exposure": False})
    for k, v in over.items():
        pps.set_editor_property("override_" + k, True)
        pps.set_editor_property(k, v)
    c.set_editor_property("post_process_settings", pps)
    c.set_editor_property("post_process_blend_weight", 1.0)
    unreal._poc_caps[name] = (cap, rt)


def tick(name, n=2):
    """Render the capture again; called on several editor ticks so lighting and exposure settle."""
    cap, rt = unreal._poc_caps[name]
    for _ in range(n):
        cap.capture_component2d.capture_scene()


def end(out_dir, name):
    cap, rt = unreal._poc_caps.pop(name)
    unreal.RenderingLibrary.export_render_target(_world(), rt, out_dir, name + ".png")
    _eas.destroy_actor(cap)
    return out_dir + "/" + name + ".png"
