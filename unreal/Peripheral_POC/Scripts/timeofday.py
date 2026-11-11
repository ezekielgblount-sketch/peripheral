"""Editor preview of the time of day. Set TOD = 'morning' | 'afternoon' | 'golden' | 'night' before exec."""
import unreal
tod = globals().get("TOD", "afternoon")
P = {"morning": (-24, 205, (255, 244, 230), 20000.0), "afternoon": (-27, 20, (255, 240, 220), 24000.0), "golden": (-9, 24, (255, 186, 120), 9000.0)}
NIGHT = tod == "night"
exec(open(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts/daynight.py").read())
if not NIGHT:
    pitch, yaw, col, inten = P[tod]
    for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
        if a.get_actor_label() == "Sun":
            a.set_actor_rotation(unreal.Rotator(roll=0, pitch=pitch, yaw=yaw), False)
            a.light_component.set_light_color(unreal.LinearColor(col[0] / 255.0, col[1] / 255.0, col[2] / 255.0, 1))
            a.light_component.set_intensity(inten)
print("time of day:", tod)
