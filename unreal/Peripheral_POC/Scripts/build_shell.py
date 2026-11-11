"""Builds the house shell (walls, floors, stairs) for the slice. Safe to re-run: it deletes and rebuilds everything tagged 'shell'.
Layout is HOUSE_BLUEPRINT v12 with the fixes logged in BUILD_STATE.md. Numbers are blueprint cm."""
import sys, importlib, unreal
sys.path.insert(0, unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()) + "Scripts")
import poc_lib as L
importlib.reload(L)
box, wallx, wally, slab, steps = L.box, L.wallx, L.wally, L.slab, L.steps

B, LND, F1, C1, F2, C2 = -252, -126, 0, 244, 259, 503     # basement, entry landing, floor 1, ceiling 1, floor 2, ceiling 2
DH = 203                                                  # door height
removed = L.clear("shell")


def door(a0, a1, z=F1):
    return (a0, a1, z, z + DH)


with unreal.ScopedSlowTask(1, "Building shell"):
    # ---------------- floors ----------------
    slab("F_basement", 0, 600, 900, 1700, B, "f_bsmt", "f_bsmt", folder="Shell/Basement")
    box("F_landing", 0, 1031, B - 15, 180, 1251, LND, "f_entry", "Shell/Entry")
    box("F_top_of_up_flight", 0, 1419, B - 15, 100, 1520, F1, "f_hall", "Shell/Hall")
    slab("F_living", 0, 600, 580, 1025, F1, "f_liv", "bsmt", folder="Shell/Living")
    slab("F_kitchen", 580, 600, 900, 1550, F1, "f_kit", "bsmt", folder="Shell/Kitchen")
    slab("F_halfbath", 580, 1550, 900, 1700, F1, "f_blk", "bsmt", folder="Shell/Blockout")
    slab("F_dining", 0, 1520, 580, 1700, F1, "f_blk", "bsmt", folder="Shell/Blockout")
    slab("F_hall_main", 100, 1251, 580, 1520, F1, "f_hall", "bsmt", folder="Shell/Hall")
    slab("F_hall_back", 470, 1025, 580, 1251, F1, "f_hall", "bsmt", folder="Shell/Hall")
    slab("F_hall_pocket", 376, 1025, 470, 1135, F1, "f_hall", "bsmt", folder="Shell/Hall")
    slab("F_under_stair", 180, 1135, 470, 1251, F1, "f_hall", "bsmt", folder="Shell/Hall")

    # floor 2 slab (also ceiling of floor 1), with the stairwell opening X106-470, Y1141-1239
    f2 = "Shell/Floor2"
    slab("F2_south", -30, 600, 900, 1120, F2, "f_blk", "ceiling", folder=f2)
    slab("F2_b1_blk", -30, 1120, 572, 1141, F2, "f_blk", "ceiling", folder=f2)
    slab("F2_b1_bath", 572, 1120, 900, 1141, F2, "f_bath", "ceiling", folder=f2)
    slab("F2_arrival", -30, 1141, 106, 1239, F2, "f_hall2", "ceiling", folder=f2)
    slab("F2_hall_wide", 470, 1141, 572, 1239, F2, "f_hall2", "ceiling", folder=f2)
    slab("F2_b2_bath", 572, 1141, 900, 1239, F2, "f_bath", "ceiling", folder=f2)
    slab("F2_gallery_a", -30, 1239, 572, 1350, F2, "f_hall2", "ceiling", folder=f2)
    slab("F2_b3_bath", 572, 1239, 900, 1350, F2, "f_bath", "ceiling", folder=f2)
    slab("F2_gallery_b", -30, 1350, 572, 1377, F2, "f_hall2", "ceiling", folder=f2)
    slab("F2_b4_blk", -30, 1377, 452, 1500, F2, "f_blk", "ceiling", folder=f2)
    slab("F2_leg", 452, 1377, 572, 1500, F2, "f_hall2", "ceiling", folder=f2)
    slab("F2_b5_blk", -30, 1500, 572, 1700, F2, "f_blk", "ceiling", folder=f2)
    slab("F2_bed", 572, 1350, 900, 1700, F2, "f_bed", "ceiling", folder=f2)
    slab("C2_top", -30, 600, 900, 1700, C2 + 15, "blk", "ceiling", folder=f2)

    # ---------------- exterior walls, basement to top of floor 1 ----------------
    e = "Shell/Exterior"
    wallx("W_front_living", -20, 0, 600, 1025, -15, F2, "brick", "liv", [(700, 940, 60, 210)], e)
    wallx("W_front_living_b", -20, 0, 600, 1025, B - 15, -15, "brick", "bsmt", (), e)
    wallx("W_front_entry", -20, 0, 1025, 1520, B - 15, F2, "brick", "hall",
          [(1055, 1080, LND + 20, LND + DH), door(1090, 1181, LND), (1191, 1216, LND + 20, LND + DH)], e)
    wallx("W_front_dining", -20, 0, 1520, 1700, -15, F2, "brick", "blk", [(1560, 1660, 90, 220)], e)
    wallx("W_front_dining_b", -20, 0, 1520, 1700, B - 15, -15, "brick", "bsmt", (), e)
    wallx("W_rear_kitchen", 900, 920, 600, 1550, -15, F2, "kit", "brick",
          [(760, 880, 107, 207), door(1030, 1121), (1300, 1420, 90, 220)], e)
    wallx("W_rear_halfbath", 900, 920, 1550, 1700, -15, F2, "blk", "brick", (), e)
    wallx("W_rear_b", 900, 920, 600, 1700, B - 15, -15, "bsmt", "brick", (), e)
    wally("W_left_living", 580, 600, -20, 580, -15, F2, "blk", "liv", (), e)
    wally("W_left_kitchen", 580, 600, 580, 920, -15, F2, "blk", "kit", [door(655, 746)], e)
    wally("W_left_b", 580, 600, -20, 920, B - 15, -15, "blk", "bsmt", (), e)
    wally("W_right", 1700, 1720, -20, 920, -15, F2, "blk", "brick", [(300, 420, 90, 220)], e)
    wally("W_right_b", 1700, 1720, -20, 920, B - 15, -15, "bsmt", "brick", (), e)

    # ---------------- interior walls, floor 1 and the stair core ----------------
    wally("W_living_hall", 1019, 1031, 0, 580, B - 15, F2, "liv", "hall", [door(470, 561)], "Shell/Living")
    wallx("W_kitchen_living", 574, 586, 600, 1025, F1, C1, "liv", "kit", (), "Shell/Kitchen")
    wallx("W_kitchen_hall", 574, 586, 1025, 1520, F1, C1, "hall", "kit", [door(1300, 1391)], "Shell/Kitchen")
    wallx("W_kitchen_dining", 574, 586, 1520, 1550, F1, C1, "blk", "kit", (), "Shell/Kitchen")
    wally("W_dining_hall", 1514, 1526, 0, 580, -15, C1, "hall", "blk", [door(250, 341)], "Shell/Hall")
    wally("W_halfbath", 1544, 1556, 580, 900, F1, C1, "kit", "blk", [door(640, 731)], "Shell/Kitchen")
    # wall between the two inner flights, full height of both floors
    wally("W_stair_mid", 1129, 1141, 180, 470, B - 15, C2, "hall", "hall", (), "Shell/Stairs")
    wally("W_stair_mid_up_front", 1129, 1141, -30, 106, C1, C2, "blk", "hall2", (), "Shell/Stairs")
    wally("W_stair_mid_overhang", 1129, 1141, 106, 180, 150, C2, "hall", "hall2", (), "Shell/Stairs")
    wally("W_stair_mid_up_back", 1129, 1141, 470, 572, F2, C2, "blk", "hall2", (), "Shell/Stairs")
    # wall on the hall side of the floor-2 stair; becomes a 91 cm half wall upstairs
    wally("W_stair_hall", 1239, 1251, 100, 470, F1, F2 + 91, "hall", "hall", (), "Shell/Stairs")
    box("Half_wall_stair_end_up", 470, 1141, F2, 482, 1239, F2 + 91, "hall2", "Shell/Stairs")
    # retaining faces around the sunken entry
    box("Ret_under_stair_x180", 180, 1141, B - 15, 192, 1251, F1 - 15, "hall", "Shell/Entry")
    box("Ret_hall_edge_x100", 100, 1251, B - 15, 112, 1514, F1 - 15, "hall", "Shell/Entry")
    box("Ret_hall_edge_y1251", 100, 1239, B - 15, 180, 1251, F1, "hall", "Shell/Entry")
    # low walls where floor 1 looks down into the entry or the basement stair
    box("Half_wall_hall_over_up_flight", 100, 1251, F1, 112, 1419, F1 + 95, "hall", "Shell/Hall")
    box("Half_wall_basement_well_end", 376, 1031, F1, 388, 1129, F1 + 95, "hall", "Shell/Hall")

    # ---------------- stairs ----------------
    # up flight: turns left off the landing (+Y in blueprint), 7 risers of 18
    steps("S_up", "y", 1251, +1, 0, 100, 6, 18, 28, LND + 18, "f_stair", solid_to=B - 15)
    # basement flight: straight ahead from the front door, descending
    steps("S_down", "x", 180, +1, 1031, 1129, 6, -18, 28, LND - 18, "f_stair", solid_to=B - 15)
    # floor 1 to floor 2: starts at the back of the hall, climbs toward the front, 14 risers of 18.5
    steps("S_upper", "x", 470, -1, 1141, 1239, 13, 18.5, 28, 18.5, "f_stair", solid_to=F1,
          soffit=37, soffit_before=180)

    # ---------------- exterior walls, floor 2 ----------------
    s = lambda z0=90, z1=220: (F2 + z0, F2 + z1)
    wallx("W2_front_a", -50, -30, 600, 1141, F2 - 15, C2 + 15, "siding", "blk", [(800, 920) + s()], e)
    wallx("W2_front_hall", -50, -30, 1141, 1377, F2 - 15, C2 + 15, "siding", "hall2", [(1265, 1355) + s()], e)
    wallx("W2_front_b", -50, -30, 1377, 1700, F2 - 15, C2 + 15, "siding", "blk", [(1480, 1600) + s()], e)
    wallx("W2_rear_a", 900, 920, 600, 1120, F2, C2 + 15, "blk", "siding", [(800, 920) + s()], e)
    wallx("W2_rear_bath", 900, 920, 1120, 1350, F2, C2 + 15, "bath", "siding", [(1200, 1280) + s(120, 200)], e)
    wallx("W2_rear_bed", 900, 920, 1350, 1700, F2, C2 + 15, "bed", "siding", [(1465, 1585) + s()], e)
    wally("W2_left", 580, 600, -50, 920, F2, C2 + 15, "siding", "blk", (), e)
    wally("W2_right_a", 1700, 1720, -50, 572, F2, C2 + 15, "blk", "siding", (), e)
    wally("W2_right_bed", 1700, 1720, 572, 920, F2, C2 + 15, "bed", "siding", [(676, 796) + s()], e)
    box("W2_overhang_soffit", -50, 580, F2 - 15, -20, 1720, F2, "siding", e)

    # ---------------- interior walls, floor 2 ----------------
    wallx("W2_rooms_a", 566, 578, 600, 1120, F2, C2, "blk", "blk", (), f2)
    wallx("W2_rooms_bath", 566, 578, 1120, 1350, F2, C2, "hall2", "bath", [door(1150, 1241, F2)], f2)
    wallx("W2_rooms_bed", 566, 578, 1350, 1500, F2, C2, "hall2", "bed", [door(1385, 1476, F2)], f2)
    wallx("W2_rooms_b", 566, 578, 1500, 1700, F2, C2, "blk", "bed", (), f2)
    wally("W2_bath_south", 1114, 1126, 578, 900, F2, C2, "blk", "bath", (), f2)
    wally("W2_bath_bed", 1344, 1356, 578, 900, F2, C2, "bath", "bed", (), f2)
    wally("W2_gallery_north", 1371, 1383, -30, 452, F2, C2, "hall2", "blk", [door(150, 241, F2)], f2)
    wallx("W2_leg", 446, 458, 1383, 1500, F2, C2, "blk", "hall2", (), f2)
    wally("W2_leg_end", 1494, 1506, 446, 566, F2, C2, "hall2", "blk", [door(472, 553, F2)], f2)

print("shell rebuilt. removed:", removed)
