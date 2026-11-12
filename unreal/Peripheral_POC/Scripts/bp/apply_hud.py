#!/usr/bin/env python3
"""Adds the director's (BP_HUD) round 1 variables and writes Scripts/bp/hud.dsl into its graph. The write takes several minutes."""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
import bp_tool as B
N = "BP_HUD"
for k in ("UB", "SB", "CB"):
    B.add_obj_var(N, k, "/Script/Engine.Actor")
for i in range(6):
    B.add_obj_var(N, "Mus%d" % i, "/Script/Engine.AudioComponent"); B.add_var(N, "Vol%d" % i, "float")
for k in ("Screen", "Cmd"):
    B.add_var(N, k, "int")
B.add_var(N, "ChoreStart", "bool")
B.call(B.BT, "set_variable_instance_editable", {"blueprint": B.bp_ref(N), "variable_name": "ChoreStart", "instance_editable": True})
print(json.dumps(B.write(N, os.path.join(here, "hud.dsl")))[:3000])
