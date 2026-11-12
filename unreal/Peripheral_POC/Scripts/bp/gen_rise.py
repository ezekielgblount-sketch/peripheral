#!/usr/bin/env python3
"""Creates BP_Rise (the corridor ceiling that lifts; graph in rise.dsl). Run with the editor open, before build_annex.py."""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
import bp_tool as B
print(B.create("BP_Rise", "/Script/Engine.StaticMeshActor"))
for k in ("H", "RiseMax", "Prev"):
    B.add_var("BP_Rise", k, "float")
B.add_var("BP_Rise", "WasIn", "bool")
B.add_obj_var("BP_Rise", "LB", "/Script/Engine.Actor"); B.add_obj_var("BP_Rise", "StoryRef", "/Game/Blueprints/BP_Story.BP_Story_C")
B.call(B.BT, "set_variable_instance_editable", {"blueprint": B.bp_ref("BP_Rise"), "variable_name": "RiseMax", "instance_editable": True})
print(json.dumps(B.write("BP_Rise", os.path.join(here, "rise.dsl")))[:2000])
