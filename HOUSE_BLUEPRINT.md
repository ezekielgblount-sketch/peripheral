# Peripheral / Isolation — Blind-Buildable House Blueprint

From Ezekiel (via ChatGPT, cross-checked by Fable 5). **This is the new
definitive house layout, approved by the creator.** It supersedes the
interior geometry already built tonight — not a refinement of it, a
replacement. That's intentional and approved, not an oversight.

**Coordinates in this document are already Unreal-native** (stated in its own
header: "Unreal scale | 1 Unreal Unit = 1 centimeter," axes labeled to match
Unreal's X/Y/Z directly). **Do not run these through `CLAUDE.md`'s spec-to-
Unreal axis conversion table** — that table exists to convert the *old*
Three.js-convention handoff spec (`PERIPHERAL_UNREAL_HANDOFF.md`), and does
not apply here. This document defines its own convention (+X front-to-back,
+Y left-to-right, +Z up) and should be built exactly as numbered, no
conversion step.

---

## Coordinate system

| Field | Value |
|---|---|
| Units | centimeters |
| Unreal scale | 1 Unreal Unit = 1 centimeter |
| Origin | (0,0,0) = outside front-left corner of the complete house footprint at ground/main-floor datum |
| +X | front to back |
| +Y | left to right |
| +Z | up |
| Rotation convention | degrees; yaw only unless geometry inherently defines slope |
| Position rule | all stated world positions are absolute from origin |
| Wall thickness convention | all wall thickness is centered on the Start→End line |

## Global constants

| Constant | Value |
|---|---|
| Main-floor ceiling height | 250 |
| Exterior wall thickness | 30 |
| Interior wall thickness | 15 |
| Standard door opening width | 90 |
| Standard door opening height | 205 |
| Default window opening width | 120 |
| Default window opening height | 130 |
| Default window sill height | 90 |
| Minimum hallway clear width | 120 |
| Actual hallway clear width | 135 |
| Stair tread depth | 28 |
| Stair riser height | 18 |
| Stair width | 90 |
| Basement ceiling height | 210 |
| Basement floor Z | -240 |
| Attic floor Z | 280 |
| Roof representation | stepped axis-aligned graybox slabs |

## Table 1 — Floors/ceilings/slabs

| ID | Name | Min corner (X,Y,Z) | Max corner (X,Y,Z) |
|---|---|---|---|
| F01 | Main floor slab A | (0,600,-15) | (1200,1290,0) |
| F02 | Main floor slab B | (0,1290,-15) | (485,1800,0) |
| F03 | Main floor slab C | (575,1290,-15) | (1200,1800,0) |
| F04 | Main floor slab D | (485,1654,-15) | (575,1800,0) |
| F05 | Garage slab | (0,0,-15) | (670,600,0) |
| F06 | Front porch slab | (-180,930,-15) | (0,1500,0) |
| F07 | Front step 1 | (-264,1035,-54) | (-236,1395,-36) |
| F08 | Front step 2 | (-236,1035,-36) | (-208,1395,-18) |
| F09 | Front step 3 | (-208,1035,-18) | (-180,1395,0) |
| F10 | Basement floor slab | (0,600,-255) | (1200,1800,-240) |
| F11 | Basement stair bottom landing | (485,1654,-240) | (575,1744,-234) |
| F12 | Basement ceiling slab A | (0,600,-30) | (1200,1290,-15) |
| F13 | Basement ceiling slab B | (0,1290,-30) | (485,1800,-15) |
| F14 | Basement ceiling slab C | (575,1290,-30) | (1200,1800,-15) |
| F15 | Basement ceiling slab D | (485,1654,-30) | (575,1800,-15) |
| F16 | Main ceiling/attic floor A | (0,600,250) | (1200,1290,280) |
| F17 | Main ceiling/attic floor B | (0,1290,250) | (365,1800,280) |
| F18 | Main ceiling/attic floor C | (455,1290,250) | (1200,1710,280) |
| F19 | Main ceiling/attic floor D | (600,1710,250) | (1200,1800,280) |
| F20 | Attic stair top landing | (365,1710,270) | (600,1800,280) |
| F21 | Front porch roof slab | (-200,900,250) | (0,1530,265) |
| F22 | Main roof step front 1 | (-30,570,350) | (75,1830,370) |
| F23 | Main roof step front 2 | (75,570,370) | (180,1830,400) |
| F24 | Main roof step front 3 | (180,570,400) | (285,1830,430) |
| F25 | Main roof step front 4 | (285,570,430) | (390,1830,460) |
| F26 | Main roof step front 5 | (390,570,460) | (495,1830,490) |
| F27 | Main roof step front 6 | (495,570,490) | (600,1830,520) |
| F28 | Main roof step rear 1 | (600,570,490) | (705,1830,520) |
| F29 | Main roof step rear 2 | (705,570,460) | (810,1830,490) |
| F30 | Main roof step rear 3 | (810,570,430) | (915,1830,460) |
| F31 | Main roof step rear 4 | (915,570,400) | (1020,1830,430) |
| F32 | Main roof step rear 5 | (1020,570,370) | (1125,1830,400) |
| F33 | Main roof step rear 6 | (1125,570,350) | (1230,1830,370) |
| F34 | Garage roof step front 1 | (-30,-30,250) | (61,585,270) |
| F35 | Garage roof step front 2 | (61,-30,270) | (152,585,295) |
| F36 | Garage roof step front 3 | (152,-30,295) | (243,585,320) |
| F37 | Garage roof step front 4 | (243,-30,320) | (335,585,345) |
| F38 | Garage roof step rear 1 | (335,-30,320) | (427,585,345) |
| F39 | Garage roof step rear 2 | (427,-30,295) | (518,585,320) |
| F40 | Garage roof step rear 3 | (518,-30,270) | (609,585,295) |
| F41 | Garage roof step rear 4 | (609,-30,250) | (700,585,270) |

## Table 2 — Walls

| ID | Name | Start (X,Y) | End (X,Y) | Base Z | Height | Thickness |
|---|---|---|---|---|---|---|
| W01 | Garage front | (0,0) | (0,600) | 0 | 250 | 30 |
| W02 | Main house front | (0,600) | (0,1800) | 0 | 250 | 30 |
| W03 | Garage left side | (0,0) | (670,0) | 0 | 250 | 30 |
| W04 | Garage rear | (670,0) | (670,600) | 0 | 250 | 30 |
| W05 | Garage/house shared wall | (0,600) | (670,600) | 0 | 250 | 30 |
| W06 | Main house left exposed wall | (670,600) | (1200,600) | 0 | 250 | 30 |
| W07 | Main house rear | (1200,600) | (1200,1800) | 0 | 250 | 30 |
| W08 | Main house right | (1200,1800) | (0,1800) | 0 | 250 | 30 |
| W09 | Hall left boundary | (0,1140) | (1200,1140) | 0 | 250 | 15 |
| W10 | Hall right boundary | (0,1290) | (1200,1290) | 0 | 250 | 15 |
| W11 | Living/kitchen divider | (560,600) | (560,1140) | 0 | 250 | 15 |
| W12 | Spare/stair-hall divider | (350,1290) | (350,1800) | 0 | 250 | 15 |
| W13 | Stair-hall/bathroom divider | (590,1290) | (590,1800) | 0 | 250 | 15 |
| W14 | Bathroom/bedroom divider | (900,1290) | (900,1800) | 0 | 250 | 15 |
| W15 | Front-entry/hall divider | (180,1140) | (180,1290) | 0 | 250 | 15 |
| W16 | Basement front | (0,600) | (0,1800) | -240 | 210 | 30 |
| W17 | Basement left | (0,600) | (1200,600) | -240 | 210 | 30 |
| W18 | Basement rear | (1200,600) | (1200,1800) | -240 | 210 | 30 |
| W19 | Basement right | (1200,1800) | (0,1800) | -240 | 210 | 30 |
| W20 | Basement stair door wall | (590,1654) | (590,1774) | -240 | 210 | 15 |
| W21 | Attic front | (0,600) | (0,1800) | 280 | 70 | 30 |
| W22 | Attic left | (0,600) | (1200,600) | 280 | 70 | 30 |
| W23 | Attic rear | (1200,600) | (1200,1800) | 280 | 70 | 30 |
| W24 | Attic right | (1200,1800) | (0,1800) | 280 | 70 | 30 |
| W25 | Attic stair door wall | (600,1680) | (600,1800) | 280 | 205 | 15 |
| W26 | Front porch post left | (-180,975) | (-180,990) | 0 | 250 | 15 |
| W27 | Front porch post right | (-180,1440) | (-180,1455) | 0 | 250 | 15 |

## Table 3 — Openings (doors and windows)

| ID | Type | Host wall | Distance along wall (Start→left edge) | Width | Height | Sill |
|---|---|---|---|---|---|---|
| O01 | door | W01 | 55 | 490 | 215 | 0 |
| O02 | door | W02 | 570 | 90 | 205 | 0 |
| O03 | door | W15 | 30 | 90 | 205 | 0 |
| O04 | door | W07 | 570 | 90 | 205 | 0 |
| O05 | window | W02 | 120 | 120 | 130 | 90 |
| O06 | window | W02 | 850 | 120 | 130 | 90 |
| O07 | door | W05 | 220 | 90 | 205 | 0 |
| O08 | window | W03 | 400 | 120 | 130 | 90 |
| O09 | window | W06 | 140 | 120 | 130 | 90 |
| O10 | door | W09 | 250 | 90 | 205 | 0 |
| O11 | door | W09 | 800 | 90 | 205 | 0 |
| O12 | door | W10 | 130 | 90 | 205 | 0 |
| O13a | door | W10 | 365 | 90 | 205 | 0 |
| O13b | door | W10 | 485 | 90 | 205 | 0 |
| O14 | door | W10 | 700 | 90 | 205 | 0 |
| O15 | door | W10 | 1000 | 90 | 205 | 0 |
| O16 | window | W07 | 80 | 120 | 130 | 90 |
| O17 | window | W07 | 800 | 120 | 130 | 90 |
| O18 | window | W08 | 330 | 120 | 130 | 90 |
| O19 | window | W08 | 900 | 120 | 130 | 90 |
| O20 | door | W20 | 0 | 90 | 205 | 0 |
| O21 | door | W25 | 30 | 90 | 205 | 0 |

## Table 4 — Stairs

| ID | Name | Bottom-start (X,Y,Z) | Direction | Steps | Width |
|---|---|---|---|---|---|
| S01 | Attic stair | (365,1290,0) | +Y | 15 | 90 |
| S02 | Basement stair | (485,1654,-234) | -Y | 13 | 90 |

## Table 5 — Room registry

| Room | Floor | Min (X,Y) | Max (X,Y) | Connects to |
|---|---|---|---|---|
| Garage | Main | (0,0) | (670,600) | O01,O07 |
| Living room | Main | (0,600) | (560,1140) | O07,O10 |
| Kitchen | Main | (560,600) | (1200,1140) | O11 |
| Front entry | Main | (0,1140) | (180,1290) | O02,O03 |
| Hallway | Main | (180,1140) | (1200,1290) | O03,O04,O10,O11,O12,O13a,O13b,O14,O15 |
| Spare room | Main | (0,1290) | (350,1800) | O12 |
| Stair hall | Main | (350,1290) | (590,1800) | O13a,O13b,O20,O21 |
| Bathroom | Main | (590,1290) | (900,1800) | O14 |
| Jack's bedroom | Main | (900,1290) | (1200,1800) | O15 |
| Basement | Basement | (0,600) | (1200,1800) | O20 |
| Attic | Attic | (0,600) | (1200,1800) | O21 |

## Mandatory self-check (as delivered — re-verify independently, don't just trust it)

| Check | Result | Detail |
|---|---|---|
| Closure | PASS | 11/11 rooms enclosed by exact matching wall coordinates |
| Opening sanity | PASS | 22/22 openings fit host-wall length/height, 0 orphaned connections |
| Overlap | PASS | 0 collinear wall overlaps, 0 wall/slab intersections |
| Circulation | PASS | Full path traced front door → hallway → every room → back door, both stairs |
| Stair access geometry | PASS | O13a/O13b align exactly with S01/S02 widths, 30cm pier between them |
| Sightline | PASS | front-door centre (0,1215,170) to back-door centre (1200,1215,170), no solid wall in between |
| Constant compliance | PASS | doors 90×205, hallway clear 135, main ceiling 250, basement ceiling 210, attic floor Z=280, stair tread 28/riser 18/width 90 |
| Deliberate exception | — | O01 (garage door): width 490, height 215, sill 0 |
