# backend/app/utils/tracer.py
import sys
import linecache
import io
import tempfile
from types import FrameType
from typing import List, Dict, Any, Tuple

def trace_execution(code: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Execute Python code in an isolated temporary file and capture:
      - Each executed line number
      - Local variables at that point
      - Console output (stdout)
    Returns: (trace_log, stdout_string)
    """
    trace_log = []
    buffer = io.StringIO()
    old_stdout = sys.stdout

    def tracer(frame: FrameType, event: str, arg):
        if event == "line":
            lineno = frame.f_lineno
            line = linecache.getline(frame.f_code.co_filename, lineno).strip()
            local_vars = {
                k: repr(v) for k, v in frame.f_locals.items()
                if not k.startswith("__")
            }
            trace_log.append({
                "line_no": lineno,
                "code": line,
                "locals": local_vars
            })
        return tracer

    # Write code to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    compiled = compile(code, tmp_path, "exec")

    sys.settrace(tracer)
    sys.stdout = buffer

    try:
        exec(compiled, {}, {})
    except Exception as e:
        trace_log.append({"error": str(e)})
    finally:
        sys.settrace(None)
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return trace_log, output
