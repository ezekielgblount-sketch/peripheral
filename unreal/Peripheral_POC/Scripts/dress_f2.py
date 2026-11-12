"""Furnishes floor 2 and the attic loft: upstairs halls, parents' suite, sibling's room, Jack's room, guest / sewing room,
hall bath, loft. Run through dress_rooms.py. Jack's bed is a chore object and lives in build_chores.py."""
import unreal
import dress_lib as D
from dress_lib import P, PW, L, K, PF, HP, lamp, switch, fixture, shaded, room_light, border, hidden, no_shadow
F2, C2, F3 = HP.F2, HP.C2, HP.F3

# ---------------- upstairs halls: greige paint like the stairwell, tan carpet ----------------
r = "Hall2"
room_light("gallery", "hall2", 300, 1350, 800, sw=("y1", 190), on=True, stage=3, room=r)
room_light("back_hall_s", "hall2", 639, 960, 650, on=True, room=r)
room_light("back_hall_n", "hall2", 639, 1600, 650, sw=("x0", 250), on=True, stage=3, room=r)
PW("frame_school_b", "gallery", "y1", 330, 152, room=r, collide=False); PW("frame_school", "gallery", "y1", 372, 150, room=r, collide=False)
PW("frame_portrait", "back_hall_s", "x0", 300, 160, room=r, collide=False); PW("frame_landscape_a", "back_hall_s", "x0", 480, 160, room=r, collide=False)
PW("frame_landscape_b", "back_hall_n", "x0", 60, 160, room=r, collide=False)
PW("vent", "arrival", "x0", 40, 12, room=r, collide=False); PW("laundry_basket", "alcove", "x0", 60, room=r)
room_light("attic_landing", "attic_stair", 90, 1478, 450, sw=("y0", 180), on=False, stage=3, room=r)

# ---------------- parents' bedroom: dusty sage, mauve carpet ----------------
r = "Parents"
PW("bed_double", "parents", "y0", 190, room=r)
PW("nightstand", "parents", "y0", 77, room=r); PW("nightstand", "parents", "y0", 303, room=r)
switch("par_lamp", "table_lamp", 47, 622, F2 + 59, (0, 1), r, "par_lamp", lit=True); shaded("par_lamp", 47, 622, F2 + 92, 400, r, "par_lamp", C2)
PW("phone_cordless", "parents", "y0", 303, 59, 14, room=r, collide=False); PW("jar_candle", "parents", "y0", 315, 59, 28, room=r, collide=False)
PW("dresser", "parents", "x1", 295, room=r); PW("mirror_wall", "parents", "x1", 295, 150, room=r, collide=False)
PW("keepsake_box", "parents", "x1", 270, 83, 14, room=r, collide=False); PW("frame_portrait", "parents", "y0", 190, 170, room=r, collide=False)
P("chair_sage", -6, 1010, F2, (1, -0.3), r); P("clothes_floor", 150, 900, F2, (0.4, 1), r, collide=False)
P("rug", 175, 900, F2, (0, 1), r, collide=False)
for along in (56, 284, 296, 524):
    PW("curtain_bed", "parents", "x0", along, 78, 3, room=r, collide=False)
room_light("parents", "parents", 175, 900, 650, sw=("y1", 150), on=False, stage=4, room=r)
r = "Pbath"                                                                            # seafoam, white hex tile
PW("bathtub", "pbath", "x1", 240, room=r); PW("shower_curtain", "pbath", "x1", 240, 22, 74, room=r, collide=False)
PW("toilet", "pbath", "y0", 128, room=r); PW("vanity", "pbath", "y0", 44, room=r); PW("medicine_cabinet", "pbath", "y0", 44, 150, room=r, collide=False)
PW("towel_bar", "pbath", "x0", 250, 125, room=r, collide=False); PW("bath_bits", "pbath", "y0", 40, 82, 14, room=r, collide=False)
room_light("pbath", "pbath", 480, 760, 650, sw=("x0", 60), on=False, stage=4, room=r, temp=3500)
r = "Pcloset"
PW("shelf_wall", "pcloset", "x1", 120, 150, room=r, collide=False); PW("box_misc", "pcloset", "y1", 120, room=r); PW("flannel_shirt", "pcloset", "x1", 80, 120, room=r, collide=False)
room_light("pcloset", "pcloset", 480, 1053, 350, sw=("x0", 40), on=False, stage=4, room=r)

# ---------------- sibling's room: soft lavender, teal carpet ----------------
r = "Sibling"
PW("bed_sibling", "sibling", "y0", 278, room=r); PW("nightstand", "sibling", "y0", 196, room=r)
switch("sib_lamp", "lava_lamp", 908, 620, F2 + 59, (0, 1), r, "sib_lamp", lit=True); lamp("sib_lamp", 908, 624, F2 + 80, 60, r, "sib_lamp", 260, tint=(255, 90, 170))
PW("desk", "sibling", "y1", 188, room=r); PW("chair_wood", "sibling", "y1", 188, 0, 80, room=r)
PW("dresser", "sibling", "x0", 400, room=r); PW("boombox", "sibling", "x0", 400, 83, 8, room=r, tags=["inspect"])
PW("poster_shapes", "sibling", "x0", 40, 160, room=r, collide=False); PW("poster_band", "sibling", "y1", 60, 160, room=r, collide=False)
P("bean_bag", 780, 680, F2, (1, 0.4), r); P("toy_chest", 1040, 1020, F2, (-1, 0), r); P("plush_pile", 1046, 920, F2, (-1, -0.3), r, collide=False)
P("rug", 896, 880, F2, (1, 0), r, collide=False); P("clothes_floor", 800, 960, F2, (1, 0.4), r, collide=False)
PW("curtain_bed", "sibling", "x1", 148, 78, 3, room=r, collide=False); PW("curtain_bed", "sibling", "x1", 352, 78, 3, room=r, collide=False)
room_light("sibling", "sibling", 896, 850, 600, sw=("x0", 310), on=False, stage=4, room=r)

# ---------------- Jack's room: denim blue, space border, loud kids' carpet ----------------
r = "Jack"
PW("desk_wood", "jack", "x1", 100, room=r); P("chair_red", 968, 1216, F2, (1, 0.1), r)
PW("pc_monitor", "jack", "x1", 124, 75, 6, room=r, collide=False); P("pc_keyboard", 1032, 1236, F2 + 75, (-1, 0), r, collide=False); PW("pc_tower", "jack", "x1", 176, room=r)
switch("bed_desk", "lamp_mint", 1056, 1172, F2 + 76.6, (-1, 0.4), r, "bed_desk"); lamp("bed_desk", 1052, 1176, F2 + 108, 400, r, "bed_desk", 450)
P("homework", 1040, 1190, F2 + 76.7, (-1, 0.2), r, tags=["inspect"]); P("cd_player", 1046, 1262, F2 + 76.6, (-1, 0), r, collide=False)
PW("dresser", "jack", "x0", 420, room=r); PW("boombox", "jack", "x0", 446, 83, 6, room=r, tags=["inspect"])
PW("craft_drawers", "jack", "y0", 300, room=r); PW("shelf_wall", "jack", "y0", 150, 120, room=r, collide=False)
PW("chart_alphabet", "jack", "x0", 110, 155, room=r, collide=False); PW("chart_fractions", "jack", "y0", 150, 168, room=r, collide=False)
PW("poster_space", "jack", "y1", 110, 160, room=r, collide=False); PW("poster_band", "jack", "x1", 470, 160, room=r, collide=False)
P("toy_blocks", 800, 1260, F2, (1, 0.3), r, collide=False); P("toy_ball", 760, 1600, F2, (1, 0), r, tags=["inspect"]); P("toy_car", 800, 1570, F2, (0.6, 1), r, tags=["inspect"])
P("teddy", 900, 1500, F2, (0.6, -1), r, tags=["inspect"]); P("card_binder", 780, 1180, F2, (0.8, 0.5), r, collide=False)
P("clothes_floor", 800, 1450, F2, (1, 0.4), r, collide=False); P("backpack", 730, 1420, F2, (0.6, 0.6), r, collide=False); P("learning_tablet", 860, 1590, F2, (0.3, 1), r, collide=False)
no_shadow(P("glow_stars", 980, 1540, C2 - 0.2, (1, 0), r, collide=False))
PW("curtain_bed", "jack", "x1", 160, 78, 3, room=r, collide=False); PW("curtain_bed", "jack", "x1", 356, 78, 3, room=r, collide=False)
border("jack", "border_1m_space", room=r)
room_light("jack", "jack", 896, 1380, 600, sw=("x0", 300), on=False, stage=4, room=r)

# ---------------- hall bath: dusty rose, with the matching shower curtain ----------------
r = "Bath"
PW("bathtub", "bath", "y1", 288, room=r); PW("shower_curtain_mauve", "bath", "y1", 288, 22, 74, room=r, collide=False)
PW("toilet", "bath", "x1", 60, room=r); PW("toilet_set", "bath", "x1", 60, room=r, collide=False)
PW("vanity", "bath", "y0", 188, room=r); PW("medicine_cabinet", "bath", "y0", 188, 150, room=r, collide=False)
PW("towel_mauve", "bath", "y0", 300, 125, room=r, collide=False); P("bath_mat_mauve", 1000, 1850, F2, (0, 1), r, collide=False)
PW("mouthwash", "bath", "y0", 210, 82, 14, room=r, collide=False); PW("seashell_soap", "bath", "y0", 170, 82, 16, room=r, collide=False)
P("towel_floor", 840, 1800, F2, (1, 0.5), r, collide=False)
room_light("bath", "bath", 896, 1790, 850, sw=("x0", 118), on=True, stage=4, room=r, temp=3500)

# ---------------- guest / sewing room: the small floral paper ----------------
r = "Guest"
PW("bed_twin", "guest", "x0", 64, room=r); PW("sewing_table", "guest", "y1", 250, room=r); PW("chair_wood", "guest", "y1", 250, 0, 78, room=r)
PW("fabric_bolts", "guest", "y1", 410, room=r); P("mannequin", 330, 1610, F2, (-0.6, 1), r)
PW("dresser", "guest", "y0", 330, room=r); PW("frame_landscape_a", "guest", "y0", 330, 160, room=r, collide=False)
P("rug", 210, 1760, F2, (1, 0), r, collide=False); PW("wire_basket", "guest", "y1", 330, room=r)
PW("curtain_bed", "guest", "x0", 116, 78, 3, room=r, collide=False); PW("curtain_bed", "guest", "x0", 344, 78, 3, room=r, collide=False)
switch("sew_lamp", "table_lamp", 195, 1938, F2 + 73, (0, -1), r, "sew_lamp", lit=True); shaded("sew_lamp", 195, 1938, F2 + 106, 400, r, "sew_lamp", C2)
room_light("guest", "guest", 205, 1750, 600, sw=("x1", 216), on=False, stage=4, room=r)

# ---------------- attic loft: slanted shiplap ceilings, burnt-orange carpet ----------------
r = "Loft"
P("tv_console", 640, 1195, F3, (0, 1), r); P("tv_90s", 640, 1200, F3 + 60, (0, 1), r, collide=False); P("game_console", 690, 1215, F3 + 60, (0, 1), r, collide=False)
P("bean_bag", 600, 1330, F3, (0, -1), r); P("bean_bag", 700, 1340, F3, (-0.3, -1), r); P("rug", 640, 1300, F3, (0, 1), r, collide=False)
P("armchair", 300, 1880, F3, (1, -0.6), r); P("toy_chest", 240, 1700, F3, (1, 0), r); P("box_misc", 800, 1900, F3, (-1, 0), r); P("box_books", 790, 1840, F3, (-1, 0.2), r)
P("skateboard", 760, 1560, F3, (0.3, 1), r, collide=False); P("toy_blocks", 420, 1700, F3, (1, 0.3), r, collide=False); P("cd_tower", 820, 1240, F3, (-1, 0), r)
for i, y in enumerate((1330, 1760)):
    P("ceiling_light_off", 525, y, F3 + 370, (1, 0), r, collide=False, tags=["sw_loft_off"]); hidden(P(PF.variant("ceiling_light_off", True), 525, y, F3 + 370, (1, 0), r, collide=False, tags=["sw_loft"]))
    lamp("loft_%d" % i, 525, y, F3 + 345, 700, r, "loft", 620)
switch("loft", "light_switch", 546, 1540.2, F3 + 60, (0, 1), r, "loft", stage=4)
print("floor 2 and loft dressed")
