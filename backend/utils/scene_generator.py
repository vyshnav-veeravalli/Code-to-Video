# backend/app/utils/scene_generator.py
from typing import List, Dict, Any
from .ast_parser import parse_code_to_scene
from .tracer import trace_execution

def generate_scene_with_trace(code: str) -> List[Dict[str, Any]]:
    """
    Generate a merged scene that combines AST structure and runtime trace.
    Returns a list of dicts, each representing a visual step for animation.
    """

    # 1️⃣ Parse code structure
    ast_steps = parse_code_to_scene(code)

    # 2️⃣ Trace runtime execution
    trace_log, stdout = trace_execution(code)
    printed_output = stdout.strip().splitlines()

    merged_scene = []
    print_index = 0

    # 3️⃣ Merge runtime + structure
    for trace_item in trace_log:
        line_no = trace_item.get("line_no")
        locals_snapshot = trace_item.get("locals", {})
        code_line = trace_item.get("code", "")
        error = trace_item.get("error")

        # Find the matching AST step (same lineno)
        ast_match = next((a for a in ast_steps if a["lineno"] == line_no), None)

        merged_step = {
            "lineno": line_no,
            "code": code_line,
            "locals": locals_snapshot,
        }

        # Include static type from AST if found
        if ast_match:
            merged_step["type"] = ast_match.get("type")
            merged_step["step"] = ast_match.get("step")
        else:
            merged_step["type"] = "runtime"
            merged_step["step"] = len(merged_scene) + 1

        # Attach output if print line
        if ast_match and ast_match.get("type") == "print":
            if print_index < len(printed_output):
                merged_step["output"] = printed_output[print_index]
                print_index += 1

        # Attach error (if any)
        if error:
            merged_step["error"] = error

        merged_scene.append(merged_step)

    return merged_scene
