#!/usr/bin/env python3
"""Call one Unreal MCP toolset tool. Usage: mcp_tool.py <toolset> <tool> '<json args>'   (or 'describe <toolset> [tool]')"""
import sys, json, subprocess, os
here = os.path.dirname(os.path.abspath(__file__))
def rpc(name, args):
    r = subprocess.run([os.path.join(here, "mcp.sh"), "tools/call", json.dumps({"name": name, "arguments": args})],
                       capture_output=True, text=True).stdout
    try: d = json.loads(r)
    except Exception:
        subprocess.run([os.path.join(here, "mcp.sh"), "init"], capture_output=True)
        d = json.loads(subprocess.run([os.path.join(here, "mcp.sh"), "tools/call", json.dumps({"name": name, "arguments": args})],
                                      capture_output=True, text=True).stdout)
    if "result" not in d:
        subprocess.run([os.path.join(here, "mcp.sh"), "init"], capture_output=True)
        d = json.loads(subprocess.run([os.path.join(here, "mcp.sh"), "tools/call", json.dumps({"name": name, "arguments": args})],
                                      capture_output=True, text=True).stdout)
    if "result" not in d: return {"error": d}
    res = d["result"]; txt = "".join(c.get("text", "") for c in res.get("content", []))
    try: out = json.loads(txt)
    except Exception: out = txt
    return {"isError": True, "out": out} if res.get("isError") else out
def call(toolset, tool, args=None):
    return rpc("call_tool", {"toolset_name": toolset, "tool_name": tool, "arguments": args or {}})
if __name__ == "__main__":
    if sys.argv[1] == "describe":
        d = rpc("describe_toolset", {"toolset_name": sys.argv[2]})
        for t in d.get("tools", []):
            if len(sys.argv) < 4 or t["name"].endswith("." + sys.argv[3]):
                print(json.dumps(t, indent=1))
    else:
        print(json.dumps(call(sys.argv[1], sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}), indent=1))
