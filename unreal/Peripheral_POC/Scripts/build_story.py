"""Places what the five-day story needs (tag 'story'): the story controller, the request board for chapter select, the
entity's places around the house, the three memory objects in the parents' room, the opened boxes and Jack's photo.
Run after dress_rooms.py and build_interactive.py. Safe to re-run."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import dress_lib as D, props_story2
importlib.reload(D); importlib.reload(props_story2)
from dress_lib import P, PW, L, K, PF, HP, hidden
F1, F2 = HP.F1, HP.F2
eas, eal = D.eas, unreal.EditorAssetLibrary
print("cleared", D.begin("story"))
r = "Story"
# ---- the entity: an ordinary coat stand that is a standing figure whenever it is only in the corner of the eye ----
ANOM = eal.load_blueprint_class("/Game/Blueprints/BP_Anomaly")
def entity(label, x, y, z, face, day):
    import math
    a = eas.spawn_actor_from_class(ANOM, L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=math.degrees(math.atan2(-face[1], face[0]))))
    a.set_actor_label(label); a.set_folder_path("Story/Entity"); a.tags = ["story", "ent", "ent%d" % day, "periph"]
    c = a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(PF.get("coat_stand"))
    c.set_collision_profile_name("NoCollision")
    for k, v in (("HomeMesh", PF.get("coat_stand")), ("AltMesh", PF.get("entity_figure")), ("Range", 1100.0), ("ArmTime", 0.4)):
        a.set_editor_property(k, v)
entity("Entity_front_hall", 128, 1538, F1, (1, -0.6), 2)
entity("Entity_upstairs_alcove", 472, 1562, F2, (1, 0.5), 3)
entity("Entity_kitchen_nook", 606, 1432, F1, (1, -0.8), 3)
entity("Entity_jack_room", 736, 1628, F2, (1, -0.7), 4)
entity("Entity_dining", 22, 1936, F1, (1, -0.8), 4)
entity("Entity_back_hall", 600, 780, F2, (0, 1), 4)
# ---- the parents' room: three things that hold the last memories ----
P("keepsake_box", 190, 770, F2 + 61, (0, 1), r, collide=False, tags=["st_keepsake"])
P("albums", 120, 720, F2 + 61, (0.3, 1), r, collide=False, tags=["st_albums"])
P("vhs_tape", 358, 880, F2 + 83, (-1, 0.2), r, collide=False, tags=["st_tape"])
P("crt_tv", 372, 920, F2 + 83, (-1, 0), r, collide=False)
# the home video: a picture on that television's tube and its glow, switched on by BP_Video once the tape has been played
import math
v = eas.spawn_actor_from_class(eal.load_blueprint_class("/Game/Blueprints/BP_Video"), L.to_ue(372, 920, F2 + 83), unreal.Rotator(roll=0, pitch=0, yaw=180))
v.set_actor_label("Home_video_screen"); v.set_folder_path("Story"); v.tags = ["story", "st_video"]
vc = v.static_mesh_component; vc.set_mobility(unreal.ComponentMobility.MOVABLE); vc.set_static_mesh(PF.get("tv_video_screen")); vc.set_collision_profile_name("NoCollision"); vc.set_cast_shadow(False)
g = eas.spawn_actor_from_class(unreal.PointLight, L.to_ue(372 - 75, 912, F2 + 110))
g.set_actor_label("Home_video_glow"); g.set_folder_path("Story"); g.tags = ["story", "st_video_glow"]; g.set_actor_hidden_in_game(True)
gc = g.light_component; gc.set_mobility(unreal.ComponentMobility.MOVABLE); gc.set_editor_property("intensity_units", unreal.LightUnits.LUMENS)
gc.set_editor_property("intensity", 190.0); gc.set_editor_property("light_color", unreal.Color(r=170, g=190, b=255, a=255)); gc.set_editor_property("attenuation_radius", 420.0)
gc.set_editor_property("cast_shadows", False)
c = hidden(P("entity_figure", 50, 1118, F2, (0, -1), r, collide=False, tags=["st_climax"], movable=True))
# ---- the ending: the two boxes, opened; one photo of his own beside theirs on the mantel ----
for t in ("st_open_a", "st_open_b"):
    hidden(P("box_open", 300, 1420, F1, (1, 0), r, collide=False, tags=[t], movable=True))
(mx, my), mf = HP.at("living", "y0", 287, 20)
P("frame_family_small", mx - 62, my, F1 + 146 + 11, mf, r, collide=False, tags=["st_shelf"])
hidden(P("frame_jack", mx - 36, my + 1, F1 + 146 + 12.5, (0.15, 1), r, collide=False, tags=["st_photo"], movable=True))
# ---- boards and the controller ----
qb = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0))      # request board: X = day asked for by the menu (9 = continue)
qb.set_actor_label("Story_request_board"); qb.set_folder_path("Story"); qb.tags = ["story", "qb"]; qb.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
ctl = eas.spawn_actor_from_class(eal.load_blueprint_class("/Game/Blueprints/BP_Story"), unreal.Vector(0, 0, -700))
ctl.set_actor_label("Story_controller"); ctl.set_folder_path("Story"); ctl.tags = ["story"]
ctl.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
fr = eas.spawn_actor_from_class(eal.load_blueprint_class("/Game/Blueprints/BP_Front"), unreal.Vector(0, 0, -720))
fr.set_actor_label("Front_controller"); fr.set_folder_path("Story"); fr.tags = ["story"]
fr.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
print("story placed")
