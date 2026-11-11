"""Sky, sun, fog and the base post-process volume. Safe to re-run (rebuilds everything tagged 'env')."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
importlib.reload(L)

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L.clear("env")


def spawn(cls, label, loc=unreal.Vector(0, 0, 600), rot=unreal.Rotator(0, 0, 0)):
    a = eas.spawn_actor_from_class(cls, loc, rot)
    a.set_actor_label(label); a.set_folder_path("Environment"); a.tags = ["env"]
    return a


# Sun: low afternoon light coming in through the front (street-side) windows.
sun = spawn(unreal.DirectionalLight, "Sun", rot=unreal.Rotator(roll=0, pitch=-27, yaw=20))
sc = sun.light_component
sc.set_mobility(unreal.ComponentMobility.MOVABLE)
sc.set_editor_property("intensity", 45000.0)       # lux: a real low afternoon sun, so lamps can use real lumens
sc.set_editor_property("light_color", unreal.Color(r=255, g=240, b=220, a=255))
sc.set_editor_property("atmosphere_sun_light", True)
sc.set_editor_property("volumetric_scattering_intensity", 0.6)
sc.set_editor_property("light_source_angle", 0.8)

spawn(unreal.SkyAtmosphere, "SkyAtmosphere")

sky = spawn(unreal.SkyLight, "SkyLight")
kc = sky.light_component
kc.set_mobility(unreal.ComponentMobility.MOVABLE)
kc.set_editor_property("real_time_capture", True)
kc.set_editor_property("intensity", 1.0)

fog = spawn(unreal.ExponentialHeightFog, "Fog", loc=unreal.Vector(0, 0, -126))
fc = fog.component
fc.set_editor_property("fog_density", 0.004)
fc.set_editor_property("fog_height_falloff", 0.05)
fc.set_editor_property("enable_volumetric_fog", True)
fc.set_editor_property("volumetric_fog_scattering_distribution", 0.6)
fc.set_editor_property("volumetric_fog_extinction_scale", 1.2)

spawn(unreal.VolumetricCloud, "Clouds")

pp = spawn(unreal.PostProcessVolume, "PP_Base")
pp.set_editor_property("unbound", True)
s = pp.settings
for k, v in {
    "override_auto_exposure_method": True, "auto_exposure_method": unreal.AutoExposureMethod.AEM_HISTOGRAM,
    "override_auto_exposure_min_brightness": True, "auto_exposure_min_brightness": 1.5,
    "override_auto_exposure_max_brightness": True, "auto_exposure_max_brightness": 14.0,
    "override_auto_exposure_speed_up": True, "auto_exposure_speed_up": 1.2,
    "override_auto_exposure_speed_down": True, "auto_exposure_speed_down": 0.7,
    "override_auto_exposure_bias": True, "auto_exposure_bias": 0.0,
    "override_auto_exposure_low_percent": True, "auto_exposure_low_percent": 35.0,
    "override_auto_exposure_high_percent": True, "auto_exposure_high_percent": 80.0,
    "override_bloom_intensity": True, "bloom_intensity": 0.12,
    "override_bloom_threshold": True, "bloom_threshold": 1.0,
    "override_vignette_intensity": True, "vignette_intensity": 0.35,
    "override_film_grain_intensity": True, "film_grain_intensity": 0.25,
    "override_motion_blur_amount": True, "motion_blur_amount": 0.25,
    "override_local_exposure_highlight_contrast_scale": True, "local_exposure_highlight_contrast_scale": 0.8,
    "override_local_exposure_shadow_contrast_scale": True, "local_exposure_shadow_contrast_scale": 0.85,
    "override_lumen_scene_lighting_quality": True, "lumen_scene_lighting_quality": 1.5,
    "override_lumen_final_gather_quality": True, "lumen_final_gather_quality": 1.5,
}.items():
    s.set_editor_property(k, v)
pp.set_editor_property("settings", s)
print("environment built")
