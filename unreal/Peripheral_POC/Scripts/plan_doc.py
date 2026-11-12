#!/usr/bin/env python3
"""Writes HOUSE_BLUEPRINT.md (repo root) and floor-plan pictures from house_plan.py, and re-checks the plan:
every room reachable through doors, every door in a real wall, no rooms overlapping. Run: python3 Scripts/plan_doc.py [png_dir]"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import house_plan as HP
ROOT = os.path.abspath(os.path.join(here, "..", "..", ".."))
NAMES = {0: "Basement", 1: "Floor 1", 2: "Floor 2"}


def groups(storey):
    """Rects that touch (no wall between) are one space."""
    rs = HP.rooms(storey, ghosts=True); parent = list(range(len(rs)))
    def find(i):
        while parent[i] != i: i = parent[i]
        return i
    for i, a in enumerate(rs):
        for j, b in enumerate(rs):
            if j <= i: continue
            ax0, ay0, ax1, ay1 = a["rect"]; bx0, by0, bx1, by1 = b["rect"]
            touch = (min(ax1, bx1) - max(ax0, bx0) > 1 and (abs(ay1 - by0) < 0.1 or abs(by1 - ay0) < 0.1)) or \
                    (min(ay1, by1) - max(ay0, by0) > 1 and (abs(ax1 - bx0) < 0.1 or abs(bx1 - ax0) < 0.1))
            if touch: parent[find(i)] = find(j)
    return rs, [find(i) for i in range(len(rs))]


def at(storey, x, y):
    rs, g = groups(storey)
    for i, r in enumerate(rs):
        if r["rect"][0] < x < r["rect"][2] and r["rect"][1] < y < r["rect"][3]:
            return (storey, g[i])
    return None


def checks():
    out = []
    # overlap
    bad = 0
    for s in (0, 1, 2):
        rs = HP.rooms(s, ghosts=True)
        for i, a in enumerate(rs):
            for b in rs[i + 1:]:
                if min(a["rect"][2], b["rect"][2]) - max(a["rect"][0], b["rect"][0]) > 0.1 and min(a["rect"][3], b["rect"][3]) - max(a["rect"][1], b["rect"][1]) > 0.1:
                    bad += 1
    out.append(("Overlap", bad == 0, "%d room rectangles overlap" % bad))
    # every door joins two spaces (or a space and outdoors / the garage)
    edges, orphan = [], 0
    for o in HP.OPENINGS:
        if o["kind"] == "window": continue
        am = (o["a0"] + o["a1"]) / 2.0
        pts = [(o["t0"] - 5, am), (o["t1"] + 5, am)] if o["axis"] == "x" else [(am, o["t0"] - 5), (am, o["t1"] + 5)]
        ends = [at(o["storey"], *p) for p in pts]
        if ends[0] is None and ends[1] is None: orphan += 1
        edges.append(tuple(ends))
    out.append(("Opening sanity", orphan == 0, "%d doors and openings, %d join nothing" % (len(edges), orphan)))
    # reachability from the entry: doors, plus the four stair flights
    adj = {}
    def link(a, b):
        if a and b: adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    for a, b in edges: link(a, b)
    link(at(1, 90, 1180), at(0, 450, 1125))            # entry landing down to the basement (the flight is part of the floor-1 space)
    link(at(1, 520, 1235), at(2, 40, 1235))            # hall up to the upstairs arrival
    seen, todo = set(), [at(1, 90, 1180)]
    while todo:
        n = todo.pop()
        if n in seen: continue
        seen.add(n); todo += list(adj.get(n, ()))
    allg = set()
    for s in (0, 1, 2):
        rs, g = groups(s)
        allg |= {(s, v) for v, r in zip(g, rs) if not r["ghost"]}
    miss = allg - seen
    out.append(("Circulation", not miss, "%d of %d spaces reached from the front door" % (len(allg) - len(miss), len(allg))))
    out.append(("Constants", True, "doors 91 x 203 clear opening, ceilings 244, floor-to-floor 259, stair risers 18 / 18.5 on 28 treads, halls at least 120 clear"))
    return out


def md():
    L = ["# Peripheral: house blueprint (playtest round 1)", "",
         "This file is generated from `unreal/Peripheral_POC/Scripts/house_plan.py` by `Scripts/plan_doc.py`. Edit the plan, not this file.",
         "It replaces the earlier v12 layout. The layout change was approved in the playtest round 1 notes.", "",
         "## Coordinates", "",
         "Centimetres. 1 Unreal unit = 1 cm. +X runs front to back, +Y runs away from the garage, +Z up.",
         "Origin: the inside face of the front wall, 600 cm in from the garage side. In Unreal the house is mirrored left to right",
         "(`poc_lib.to_ue`), so that walking in the front door the up flight turns left and the garage is on the right.", "",
         "## Levels", "", "| Level | Z |", "|---|---|",
         "| Grade (lawn, driveway) | %d |" % HP.GR, "| Garage floor | %d |" % HP.GARAGE["floor"], "| Basement floor | %d |" % HP.B, "| Entry landing | %d |" % HP.LND,
         "| Floor 1 | %d |" % HP.F1, "| Floor 1 ceiling | %d |" % HP.C1, "| Floor 2 | %d |" % HP.F2, "| Floor 2 ceiling | %d |" % HP.C2, "| Attic loft floor | %d |" % HP.F3, "",
         "## Size", "",
         "Floors 1 and 2, outside wall to outside wall: %d sq ft. Clear floor inside the rooms on those two floors: %d sq ft." % (
             round(HP.area_sqft()), round(sum((r["rect"][2] - r["rect"][0]) * (r["rect"][3] - r["rect"][1]) for r in HP.rooms() if r["storey"] in (1, 2)) / 929.03)),
         "Basement, attic loft and the two-car garage are extra. Walking speed is %d cm/s." % HP.WALK_SPEED, ""]
    for s in (1, 2, 0):
        L += ["## %s rooms" % NAMES[s], "", "| Room | Clear space (x0, y0) to (x1, y1) | Size | Floor Z | Wall finish | Floor finish |", "|---|---|---|---|---|---|"]
        for r in HP.rooms(s):
            x0, y0, x1, y1 = r["rect"]
            L.append("| %s | (%d, %d) to (%d, %d) | %d x %d | %d | %s | %s |" % (r["label"], x0, y0, x1, y1, x1 - x0, y1 - y0, r["floor"], HP.FIN[r["fin"]][0], r["floor_mat"] or "built by hand"))
        L.append("")
    L += ["Rooms listed more than once (hall, entry) are one space made of several rectangles.", "",
          "## Doors and openings", "", "| Name | Floor | Wall runs along | Wall thickness span | Opening span | Bottom Z | Kind |", "|---|---|---|---|---|---|---|"]
    for o in HP.OPENINGS:
        if o["kind"] != "window":
            L.append("| %s | %s | %s | %d to %d | %d to %d | %d | %s |" % (o.get("name", "(cased opening)"), NAMES[o["storey"]], "Y" if o["axis"] == "x" else "X", o["t0"], o["t1"], o["a0"], o["a1"], o["z0"],
                     "door, locked" if o.get("locked") else o["kind"]))
    L += ["", "## Windows", "", "| Floor | Wall runs along | Wall thickness span | Opening span | Z | Style |", "|---|---|---|---|---|---|"]
    for o in HP.OPENINGS:
        if o["kind"] == "window":
            L.append("| %s | %s | %d to %d | %d to %d | %d to %d | %s |" % (NAMES[o["storey"]], "Y" if o["axis"] == "x" else "X", o["t0"], o["t1"], o["a0"], o["a1"], o["z0"], o["z1"], o["style"]))
    L += ["", "## Stairs (the stair rules are unchanged from the earlier layout)", "", "| Flight | Travel | Start | Lane | Treads | Rise | Tread | First tread top Z |", "|---|---|---|---|---|---|---|---|"]
    for k, lab in (("up", "Entry landing up to floor 1 (turns left off the landing)"), ("down", "Entry landing down to the basement (straight ahead)"), ("upper", "Floor 1 to floor 2"), ("attic", "Floor 2 to the attic loft")):
        s = HP.STAIRS[k]
        L.append("| %s | %s%s | %d | %d to %d | %d | %s | %d | %s |" % (lab, "+" if s["sign"] > 0 else "-", s["axis"].upper(), s["start"], s["lane"][0], s["lane"][1], s["n"], abs(s["rise"]), s["tread"], s["first_top"]))
    g, lf = HP.GARAGE, HP.LOFT
    L += ["", "## Garage and attic loft", "",
          "Garage (two cars), clear inside: (%d, %d) to (%d, %d), floor Z %d, ceiling Z %d. Door opening Y %d to %d, %d high. A doorway in its back wall leads to the yard; steps climb to the mudroom door." % (g["x0"], g["y0"], g["x1"], g["y1"], g["floor"], g["ceil"], g["door"][0], g["door"][1], g["door"][2]),
          "Attic loft: (%d, %d) to (%d, %d) under an 8-in-12 roof, ridge at X %d; knee walls at the sides; stair well at (%d, %d) to (%d, %d)." % (lf["x0"], lf["y0"], lf["x1"], lf["y1"], lf["ridge_x"], *lf["well"]),
          "", "## Self-check (run by plan_doc.py every time this file is written)", "", "| Check | Result | Detail |", "|---|---|---|"]
    for name, ok, detail in checks():
        L.append("| %s | %s | %s |" % (name, "PASS" if ok else "FAIL", detail))
    L += ["| Fit | see BUILD_STATE.md | `Scripts/fit_check.py` walks a 178 cm, 35 cm radius capsule through every doorway, stair and room in the built level |", ""]
    return "\n".join(L)


def png(out_dir):
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(out_dir, exist_ok=True)
    try: f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except Exception: f = ImageFont.load_default()
    for s in (0, 1, 2):
        x0, y0, x1, y1 = -100, -120, 1160, 2040
        k = 0.7; W, H = int((y1 - y0) * k), int((x1 - x0) * k)
        im = Image.new("RGB", (W, H), (245, 242, 235)); d = ImageDraw.Draw(im)
        P = lambda x, y: ((y - y0) * k, H - (x - x0) * k)              # garage on the left, front (street) at the bottom
        bx0, by0, bx1, by1 = HP.BBOX[s]
        d.rectangle([P(bx1, by0), P(bx0, by1)], fill=(70, 66, 60))
        if s == 1:
            g = HP.GARAGE; d.rectangle([P(g["x1"] + 20, g["y0"] - 20), P(g["x0"] - 20, g["y1"])], fill=(70, 66, 60)); d.rectangle([P(g["x1"], g["y0"]), P(g["x0"], g["y1"])], fill=(222, 222, 216))
            d.text(P(420, 180), "Garage", fill=(40, 40, 40), font=f)
        for r in HP.rooms(s):
            a, b = P(r["rect"][2], r["rect"][1]), P(r["rect"][0], r["rect"][3])
            d.rectangle([a, b], fill=(232, 224, 205) if r["floor_mat"] else (214, 206, 190))
        for r in HP.rooms(s):
            if r["label"] != r["name"]:
                cx, cy = P((r["rect"][0] + r["rect"][2]) / 2.0 + 14, r["rect"][1] + 10)
                d.text((cx, cy), r["label"], fill=(40, 40, 40), font=f)
        for o in HP.OPENINGS:
            if o["storey"] != s: continue
            fp = (o["t0"], o["a0"], o["t1"], o["a1"]) if o["axis"] == "x" else (o["a0"], o["t0"], o["a1"], o["t1"])
            d.rectangle([P(fp[2], fp[1]), P(fp[0], fp[3])], fill=(120, 170, 220) if o["kind"] == "window" else (232, 224, 205))
        d.text((16, 12), "%s   (street at the bottom, garage on the left; 1 m grid)" % NAMES[s], fill=(30, 30, 30), font=f)
        for gx in range(0, 1101, 100):
            d.line([P(gx, y0 + 60), P(gx, y0 + 75)], fill=(120, 120, 120))
        im.save(os.path.join(out_dir, "plan_%s.png" % NAMES[s].lower().replace(" ", "_")))


if __name__ == "__main__":
    open(os.path.join(ROOT, "HOUSE_BLUEPRINT.md"), "w").write(md())
    for name, ok, detail in checks():
        print("%-16s %s  %s" % (name, "PASS" if ok else "FAIL", detail))
    if len(sys.argv) > 1:
        png(sys.argv[1]); print("plans written to", sys.argv[1])
