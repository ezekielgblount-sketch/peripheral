# Editor-only helper: runs Python files dropped into Saved/PyInbox and writes their output next to them.
# Lets command-line tools drive the open editor without any network setup. Not used by the game itself.
import unreal, os, io, traceback, contextlib

_INBOX = os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()), "PyInbox")
os.makedirs(_INBOX, exist_ok=True)

def _poc_inbox_tick(_dt):
    try:
        names = sorted(n for n in os.listdir(_INBOX) if n.endswith(".py"))
    except OSError:
        return
    for n in names[:1]:
        p = os.path.join(_INBOX, n)
        try:
            with open(p) as f: code = f.read()
            os.remove(p)
        except OSError:
            continue
        buf = io.StringIO(); status = "OK"
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, n, "exec"), {"__name__": "__main__", "unreal": unreal})
        except Exception:
            buf.write(traceback.format_exc()); status = "FAIL"
        tmp = p[:-3] + ".tmp"
        with open(tmp, "w") as f: f.write(status + "\n" + buf.getvalue())
        os.replace(tmp, p[:-3] + ".out")

if not unreal.is_commandlet() if hasattr(unreal, "is_commandlet") else True:
    _poc_inbox_handle = unreal.register_slate_post_tick_callback(_poc_inbox_tick)
