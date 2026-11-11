#!/usr/bin/env python3
"""Host-side helpers for building Blueprints through the Unreal MCP Blueprint tools."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_tool import call
BT = "editor_toolset.toolsets.blueprint.BlueprintTools"
BP_DIR = "/Game/Blueprints"


def bp_ref(name):
    return {"refPath": "%s/%s.%s" % (BP_DIR, name, name)}


def graph_ref(name, graph="EventGraph"):
    return {"refPath": "%s/%s.%s:%s" % (BP_DIR, name, name, graph)}


def create(name, parent):
    return call(BT, "create", {"folder_path": BP_DIR, "asset_name": name, "asset_type": {"refPath": parent}})


def add_var(name, var, type_name):
    return call(BT, "add_variable", {"blueprint": bp_ref(name), "name": var, "type_name": type_name, "graph": None, "container_type": None})


def add_struct_var(name, var, struct):
    return call(BT, "add_struct_variable", {"blueprint": bp_ref(name), "name": var, "struct_type": {"refPath": struct}, "graph": None, "container_type": None})


def add_obj_var(name, var, cls):
    return call(BT, "add_object_variable", {"blueprint": bp_ref(name), "name": var, "object_class": {"refPath": cls}, "graph": None, "container_type": None})


def write(name, dsl_path, graph="EventGraph"):
    code = open(dsl_path).read()
    return call(BT, "write_graph_dsl", {"graph": graph_ref(name, graph), "code": code})


def find(name, flt, graph="EventGraph"):
    r = call(BT, "find_node_types", {"graph": graph_ref(name, graph), "type_id_filter": flt, "context_pins": []})
    return r


def pins(name, type_id, graph="EventGraph"):
    return call(BT, "get_node_type_pins", {"graph": graph_ref(name, graph), "type_id": type_id})


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "find":
        for f in sys.argv[3:]:
            r = find(sys.argv[2], f)
            print(f, "->", json.dumps(r)[:1500])
    elif cmd == "pins":
        for t in sys.argv[3:]:
            print(t, "->", json.dumps(pins(sys.argv[2], t))[:1500])
    elif cmd == "write":
        print(json.dumps(write(sys.argv[2], sys.argv[3], *(sys.argv[4:5])))[:3000])
