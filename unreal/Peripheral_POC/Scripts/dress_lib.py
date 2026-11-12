"""Shared helpers for furnishing rooms. Positions are blueprint cm. Everything placed carries the tag passed to begin()."""
import sys, math, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L, meshkit as K, props_furniture as PF, house_plan as HP
import props_small, props_90s, props_home, props_lived, props_story, props_pool, props_loop, props_r1, props_yard
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
SWITCH = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Switch")
TAG = "dress"
count = {}


def begin(tag):
    global TAG
    TAG = tag
    return L.clear(tag)


def P(prop, x, y, z, face, room, collide=True, tags=(), movable=False):
    """Place a prop. Its back / origin goes at (x, y, z); face is the blueprint direction its front points."""
    count[prop] = count.get(prop, 0) + 1
    mesh = prop if not isinstance(prop, str) else PF.get(prop)
    name = prop if isinstance(prop, str) else mesh.get_name()[3:]
    a = K.place(mesh, "%s_%s_%d" % (room, name, count[prop]), x, y, z, face=face, folder="%s/%s" % (TAG.capitalize(), room), tag=TAG, collide=collide,
                movable=movable or "inspect" in tags or "carry" in tags)
    a.tags = [TAG] + list(tags)
    return a


def PW(prop, room_name, side, along, z=0.0, inset=0.3, room=None, **kw):
    """Place a prop against one wall of a room (see house_plan.at), facing into the room. z is height above that room's floor."""
    (x, y), face = HP.at(room_name, side, along, inset)
    return P(prop, x, y, HP.room(room_name)["floor"] + z, face, room or room_name.capitalize(), **kw)


def hidden(a):
    a.set_actor_hidden_in_game(True); a.set_is_temporarily_hidden_in_editor(True)
    return a


def lamp(name, x, y, z, lumens, room, group, radius=600, temp=2700, shadows=True, on=False, tint=(255, 255, 255), flicker=False, spot=None):
    """A bulb with a real colour temperature. It belongs to a switch group; `on` is whether that switch starts on."""
    a = eas.spawn_actor_from_class(unreal.SpotLight if spot else unreal.PointLight, L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=spot[0] if spot else 0, yaw=0))
    a.set_actor_label("Lamp_" + name); a.set_folder_path("%s/%s" % (TAG.capitalize(), room))
    a.tags = [TAG, "sw_" + group] + (["default_on"] if on else [])
    c = a.light_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_editor_property("intensity_units", unreal.LightUnits.LUMENS); c.set_editor_property("intensity", lumens)
    c.set_editor_property("use_temperature", True); c.set_editor_property("temperature", float(temp))
    c.set_editor_property("light_color", unreal.Color(r=tint[0], g=tint[1], b=tint[2], a=255))
    c.set_editor_property("attenuation_radius", radius); c.set_editor_property("source_radius", 4.0); c.set_editor_property("soft_source_radius", 6.0)
    c.set_editor_property("cast_shadows", shadows)
    if spot:
        c.set_editor_property("outer_cone_angle", spot[1]); c.set_editor_property("inner_cone_angle", spot[1] * 0.45)
    if flicker:
        c.set_editor_property("light_function_material", unreal.EditorAssetLibrary.load_asset("/Game/Materials/M_Flicker"))
    if not on:
        a.set_actor_hidden_in_game(True)
    return a


def switch(label, mesh, x, y, z, face, room, group, on=False, stage=1, lit=False, tags=()):
    """Something the player presses E on to turn a group of bulbs on or off: a wall switch, or the lamp itself (lit=True)."""
    a = eas.spawn_actor_from_class(SWITCH, L.to_ue(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=math.degrees(math.atan2(-face[1], face[0]))))
    a.set_actor_label("Switch_" + label); a.set_folder_path("%s/%s" % (TAG.capitalize(), room)); a.tags = [TAG, "switch"] + (["default_on"] if on else []) + list(tags)
    c = a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE)
    m_on, m_off = (PF.variant(mesh, True), PF.variant(mesh, False)) if lit else (PF.get(mesh), PF.get(mesh))
    c.set_static_mesh(m_off)
    for k, v in (("On", on), ("Stage", stage), ("Group", "sw_" + group), ("GroupOff", "sw_%s_off" % group), ("MeshOn", m_on), ("MeshOff", m_off)):
        a.set_editor_property(k, v)
    return a


def fixture(prop, x, y, z, face, room, group, on=False):
    """A ceiling or wall fixture as a lit copy and an unlit copy; its switch shows one of them."""
    for is_on in (True, False):
        a = K.place(PF.variant(prop, is_on), "%s_%s_%s_%s" % (room, prop, group, "lit" if is_on else "unlit"), x, y, z, face=face, folder="%s/%s" % (TAG.capitalize(), room), tag=TAG, collide=False)
        a.tags = [TAG, "sw_%s" % group if is_on else "sw_%s_off" % group] + (["default_on"] if on else [])
        a.static_mesh_component.set_cast_shadow(False)


def shaded(name, x, y, z, lumens, room, group, ceiling, radius=420):
    """A lamp with a shade: soft glow through the shade, a pool on the table below and a pool on the ceiling above."""
    lamp(name, x, y, z, lumens * 0.45, room, group, radius)
    lamp(name + "_down", x, y, z - 4, lumens * 0.5, room, group, 150, shadows=False, spot=(-90, 58))
    lamp(name + "_up", x, y, z + 4, lumens * 0.45, room, group, ceiling - z + 20, shadows=False, spot=(90, 52))


def room_light(room_name, group, x, y, lumens, sw=None, on=True, stage=1, prop="ceiling_light_off", temp=2700, radius=600, drop=22, room=None, flicker=False, sw_tags=()):
    """Ceiling fixture + bulb for a room, and its wall switch at sw = (side, along) on that room's wall."""
    r = HP.room(room_name); rn = room or room_name.capitalize()
    fixture(prop, x, y, r["ceil"], (1, 0), rn, group, on=on)
    lamp(group + "_%d" % (count.get("L" + group, 0)), x, y, r["ceil"] - drop, lumens, rn, group, radius, temp=temp, on=on, flicker=flicker)
    count["L" + group] = count.get("L" + group, 0) + 1
    if sw:
        (sx, sy), face = HP.at(room_name, sw[0], sw[1], 0.2)
        switch(group, "light_switch", sx, sy, r["floor"] + 120, face, rn, group, on=on, stage=stage, tags=sw_tags)


def border(room_name, prop, z_below_ceiling=14.0, room=None):
    """Wallpaper border strip round a room just under the ceiling, in 1 m pieces."""
    r = HP.room(room_name); x0, y0, x1, y1 = r["rect"]; z = r["ceil"] - z_below_ceiling; rn = room or room_name.capitalize()
    for y in range(int(y0) + 50, int(y1) + 50, 100):
        P(prop, x0 + 0.3, min(y, y1 - 50), z, (1, 0), rn, collide=False); P(prop, x1 - 0.3, min(y, y1 - 50), z, (-1, 0), rn, collide=False)
    for x in range(int(x0) + 50, int(x1) + 50, 100):
        P(prop, min(x, x1 - 50), y0 + 0.3, z, (0, 1), rn, collide=False); P(prop, min(x, x1 - 50), y1 - 0.3, z, (0, -1), rn, collide=False)


def no_shadow(a):
    a.static_mesh_component.set_cast_shadow(False); a.static_mesh_component.set_editor_property("affect_distance_field_lighting", False)
    return a
