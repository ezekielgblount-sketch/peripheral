# Peripheral: house blueprint (playtest round 1)

This file is generated from `unreal/Peripheral_POC/Scripts/house_plan.py` by `Scripts/plan_doc.py`. Edit the plan, not this file.
It replaces the earlier v12 layout. The layout change was approved in the playtest round 1 notes.

## Coordinates

Centimetres. 1 Unreal unit = 1 cm. +X runs front to back, +Y runs away from the garage, +Z up.
Origin: the inside face of the front wall, 600 cm in from the garage side. In Unreal the house is mirrored left to right
(`poc_lib.to_ue`), so that walking in the front door the up flight turns left and the garage is on the right.

## Levels

| Level | Z |
|---|---|
| Grade (lawn, driveway) | -140 |
| Garage floor | -138 |
| Basement floor | -252 |
| Entry landing | -126 |
| Floor 1 | 0 |
| Floor 1 ceiling | 244 |
| Floor 2 | 259 |
| Floor 2 ceiling | 503 |
| Attic loft floor | 518 |

## Size

Floors 1 and 2, outside wall to outside wall: 3421 sq ft. Clear floor inside the rooms on those two floors: 3069 sq ft.
Basement, attic loft and the two-car garage are extra. Walking speed is 135 cm/s.

## Floor 1 rooms

| Room | Clear space (x0, y0) to (x1, y1) | Size | Floor Z | Wall finish | Floor finish |
|---|---|---|---|---|---|
| Living room | (0, 600) to (574, 1064) | 574 x 464 | 0 | w_liv | f_oak |
| Entry | (0, 1076) to (180, 1186) | 180 x 110 | -126 | w_hall | built by hand |
| entry_c | (0, 1186) to (106, 1284) | 106 x 98 | -126 | w_hall | built by hand |
| entry_d | (106, 1186) to (180, 1284) | 74 x 98 | -126 | w_hall | built by hand |
| entry_b | (0, 1284) to (100, 1296) | 100 x 12 | -126 | w_hall | built by hand |
| stair_down | (180, 1076) to (376, 1174) | 196 x 98 | -252 | w_hall | built by hand |
| hall_pocket | (376, 1076) to (470, 1174) | 94 x 98 | 0 | w_hall | f_oak |
| Hall | (470, 1076) to (574, 1296) | 104 x 220 | 0 | w_hall | f_oak |
| stair_up2 | (180, 1186) to (470, 1284) | 290 x 98 | 0 | w_hall | built by hand |
| up_flight | (0, 1296) to (100, 1559) | 100 x 263 | -126 | w_hall | built by hand |
| Hall | (100, 1296) to (574, 1559) | 474 x 263 | 0 | w_hall | f_oak |
| Dining room | (0, 1571) to (574, 1960) | 574 x 389 | 0 | w_din | f_oak |
| Laundry / mudroom | (586, 600) to (850, 850) | 264 x 250 | 0 | w_mud | f_vinyl |
| Half bath | (862, 600) to (1080, 850) | 218 x 250 | 0 | w_bath_blue | f_sq |
| Kitchen and nook | (586, 862) to (1080, 1450) | 494 x 588 | 0 | w_kit | f_vinyl |
| Family room / den | (586, 1462) to (1080, 1960) | 494 x 498 | 0 | w_den | f_c_den |

## Floor 2 rooms

| Room | Clear space (x0, y0) to (x1, y1) | Size | Floor Z | Wall finish | Floor finish |
|---|---|---|---|---|---|
| Parents' bedroom | (-30, 600) to (380, 1174) | 410 x 574 | 259 | w_par | f_c_par |
| Parents' bath | (392, 600) to (566, 920) | 174 x 320 | 259 | w_bath_sea | f_hex |
| Closet | (392, 932) to (566, 1174) | 174 x 242 | 259 | w_par | f_c_par |
| arrival | (-30, 1186) to (106, 1284) | 136 x 98 | 259 | w_hall | f_c_hall |
| well | (106, 1186) to (470, 1284) | 364 x 98 | 259 | w_hall | built by hand |
| hall_wide | (470, 1186) to (700, 1284) | 230 x 98 | 259 | w_hall | f_c_hall |
| Upstairs hall | (-30, 1284) to (700, 1416) | 730 x 132 | 259 | w_hall | f_c_hall |
| Back hall | (578, 600) to (700, 1186) | 122 x 586 | 259 | w_hall | f_c_hall |
| back_hall_n | (578, 1416) to (700, 1770) | 122 x 354 | 259 | w_hall | f_c_hall |
| alcove | (452, 1540) to (578, 1770) | 126 x 230 | 259 | w_hall | f_c_hall |
| Attic stair | (-30, 1428) to (203, 1528) | 233 x 100 | 259 | w_hall | f_c_hall |
| attic_flight | (203, 1428) to (566, 1528) | 363 x 100 | 259 | w_hall | built by hand |
| Guest / sewing room | (-30, 1540) to (440, 1960) | 470 x 420 | 259 | w_guest | f_c_guest |
| Linen | (452, 1782) to (574, 1960) | 122 x 178 | 259 | w_hall | f_c_hall |
| Storage | (586, 1782) to (700, 1960) | 114 x 178 | 259 | w_hall | f_c_hall |
| Sibling's room | (712, 600) to (1080, 1100) | 368 x 500 | 259 | w_sib | f_c_sib |
| Jack's room | (712, 1112) to (1080, 1650) | 368 x 538 | 259 | w_jack | f_c_jack |
| Hall bath | (712, 1662) to (1080, 1960) | 368 x 298 | 259 | w_bath_mauve | f_hex |

## Basement rooms

| Room | Clear space (x0, y0) to (x1, y1) | Size | Floor Z | Wall finish | Floor finish |
|---|---|---|---|---|---|
| Storage | (0, 600) to (574, 1064) | 574 x 464 | -252 | bsmt | f_bsmt |
| b_foot | (376, 1076) to (574, 1174) | 198 x 98 | -252 | bsmt | f_bsmt |
| b_link | (470, 1174) to (574, 1186) | 104 x 12 | -252 | bsmt | f_bsmt |
| b_under | (192, 1186) to (574, 1284) | 382 x 98 | -252 | bsmt | f_bsmt |
| Utility | (112, 1296) to (574, 1559) | 462 x 263 | -252 | bsmt | f_bsmt |
| Workshop | (0, 1571) to (574, 1960) | 574 x 389 | -252 | bsmt | f_bsmt |
| Basement | (586, 600) to (1080, 1960) | 494 x 1360 | -252 | bsmt | f_bsmt |

Rooms listed more than once (hall, entry) are one space made of several rectangles.

## Doors and openings

| Name | Floor | Wall runs along | Wall thickness span | Opening span | Bottom Z | Kind |
|---|---|---|---|---|---|---|
| Door_front | Floor 1 | Y | -20 to 0 | 1135 to 1226 | -126 | door |
| Door_living | Floor 1 | X | 1064 to 1076 | 470 to 561 | 0 | door |
| Door_kitchen | Floor 1 | Y | 574 to 586 | 1345 to 1436 | 0 | door |
| Door_dining | Floor 1 | X | 1559 to 1571 | 250 to 341 | 0 | door |
| Door_dining_den | Floor 1 | Y | 574 to 586 | 1720 to 1811 | 0 | door |
| Door_mud | Floor 1 | X | 850 to 862 | 640 to 731 | 0 | door |
| Door_halfbath | Floor 1 | Y | 850 to 862 | 700 to 791 | 0 | door |
| Door_garage | Floor 1 | X | 580 to 600 | 650 to 741 | 0 | door |
| Door_kitchen_rear | Floor 1 | Y | 1080 to 1100 | 1250 to 1341 | 0 | door |
| (cased opening) | Floor 1 | X | 1450 to 1462 | 760 to 960 | 0 | open |
| Door_parents | Floor 2 | X | 1174 to 1186 | 5 to 96 | 259 | door |
| Door_pbath | Floor 2 | Y | 380 to 392 | 700 to 791 | 259 | door |
| Door_pcloset | Floor 2 | Y | 380 to 392 | 1000 to 1091 | 259 | door |
| Door_sibling | Floor 2 | Y | 700 to 712 | 800 to 891 | 259 | door |
| Door_jack | Floor 2 | Y | 700 to 712 | 1300 to 1391 | 259 | door |
| Door_bath | Floor 2 | Y | 700 to 712 | 1672 to 1763 | 259 | door |
| Door_guest | Floor 2 | Y | 440 to 452 | 1650 to 1741 | 259 | door |
| Door_attic | Floor 2 | X | 1416 to 1428 | 60 to 151 | 259 | door |
| Door_closet_a | Floor 2 | X | 1770 to 1782 | 468 to 559 | 259 | door, locked |
| Door_closet_b | Floor 2 | X | 1770 to 1782 | 598 to 689 | 259 | door, locked |
| (cased opening) | Basement | Y | 574 to 586 | 800 to 891 | -252 | open |
| (cased opening) | Basement | Y | 574 to 586 | 1081 to 1172 | -252 | open |
| (cased opening) | Basement | X | 1284 to 1296 | 480 to 571 | -252 | open |
| (cased opening) | Basement | X | 1559 to 1571 | 300 to 391 | -252 | open |
| (cased opening) | Basement | Y | 574 to 586 | 1700 to 1791 | -252 | open |

## Windows

| Floor | Wall runs along | Wall thickness span | Opening span | Z | Style |
|---|---|---|---|---|---|
| Floor 1 | Y | -20 to 0 | 720 to 960 | 60 to 210 | picture |
| Floor 1 | Y | -20 to 0 | 1100 to 1125 | -106 to 77 | plain |
| Floor 1 | Y | -20 to 0 | 1236 to 1261 | -106 to 77 | plain |
| Floor 1 | Y | -20 to 0 | 1700 to 1840 | 80 to 215 | double |
| Floor 1 | X | 1960 to 1980 | 220 to 360 | 90 to 220 | double |
| Floor 1 | Y | 1080 to 1100 | 1620 to 1800 | 80 to 215 | picture |
| Floor 1 | X | 1960 to 1980 | 760 to 900 | 90 to 220 | double |
| Floor 1 | Y | 1080 to 1100 | 960 to 1100 | 107 to 207 | double |
| Floor 1 | Y | 1080 to 1100 | 700 to 760 | 130 to 200 | plain |
| Floor 2 | Y | -50 to -30 | 700 to 840 | 349 to 479 | double |
| Floor 2 | Y | -50 to -30 | 940 to 1080 | 349 to 479 | double |
| Floor 2 | Y | -50 to -30 | 1305 to 1395 | 349 to 479 | double |
| Floor 2 | Y | -50 to -30 | 1448 to 1508 | 379 to 459 | plain |
| Floor 2 | Y | -50 to -30 | 1700 to 1840 | 349 to 479 | double |
| Floor 2 | X | 1960 to 1980 | 150 to 290 | 349 to 479 | double |
| Floor 2 | Y | 1080 to 1100 | 780 to 920 | 349 to 479 | double |
| Floor 2 | Y | 1080 to 1100 | 1300 to 1440 | 349 to 479 | double |
| Floor 2 | Y | 1080 to 1100 | 1780 to 1860 | 379 to 459 | plain |

## Stairs (the stair rules are unchanged from the earlier layout)

| Flight | Travel | Start | Lane | Treads | Rise | Tread | First tread top Z |
|---|---|---|---|---|---|---|---|
| Entry landing up to floor 1 (turns left off the landing) | +Y | 1296 | 0 to 100 | 6 | 18 | 28 | -108 |
| Entry landing down to the basement (straight ahead) | +X | 180 | 1076 to 1174 | 6 | 18 | 28 | -144 |
| Floor 1 to floor 2 | -X | 470 | 1186 to 1284 | 13 | 18.5 | 28 | 18.5 |
| Floor 2 to the attic loft | +X | 175 | 1428 to 1528 | 13 | 18.5 | 28 | 277.5 |

## Garage and attic loft

Garage (two cars), clear inside: (0, -40) to (760, 580), floor Z -138, ceiling Z 244. Door opening Y 25 to 515, 213 high. A doorway in its back wall leads to the yard; steps climb to the mudroom door.
Attic loft: (170, 1192) to (880, 1960) under an 8-in-12 roof, ridge at X 525; knee walls at the sides; stair well at (203, 1428) to (539, 1528).

## Self-check (run by plan_doc.py every time this file is written)

| Check | Result | Detail |
|---|---|---|
| Overlap | PASS | 0 room rectangles overlap |
| Opening sanity | PASS | 25 doors and openings, 0 join nothing |
| Circulation | PASS | 23 of 23 spaces reached from the front door |
| Constants | PASS | doors 91 x 203 clear opening, ceilings 244, floor-to-floor 259, stair risers 18 / 18.5 on 28 treads, halls at least 120 clear |
| Fit | see BUILD_STATE.md | `Scripts/fit_check.py` walks a 178 cm, 35 cm radius capsule through every doorway, stair and room in the built level |
