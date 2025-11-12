# backend/app/utils/ast_parser.py
from typing import List, Dict, Any
import ast

class SceneStep(dict):
    """Dict-like step object to standardize a scene skeleton item."""
    pass

class SceneASTParser(ast.NodeVisitor):
    """
    Convert Python AST into a stable list of scene steps.
    Each step is a dict:
      { step: int, type: str, lineno: int, code: str, extra: {...} }
    """
    def __init__(self):
        self.steps: List[SceneStep] = []
        self._counter = 1

    def _add(self, node_type: str, lineno: int, code: str, extra: Dict[str, Any] | None = None):
        item = SceneStep({
            "step": self._counter,
            "type": node_type,
            "lineno": lineno,
            "code": code
        })
        if extra:
            item.update(extra)
        self.steps.append(item)
        self._counter += 1

    # Helpful helpers
    def _safe_unparse(self, node: ast.AST) -> str:
        try:
            return ast.unparse(node) if hasattr(ast, "unparse") else "<code>"
        except Exception:
            return "<code>"

    # Node visitors
    def visit_FunctionDef(self, node: ast.FunctionDef):
        code = f"def {node.name}(...):"
        self._add("function_def", node.lineno, code, {"name": node.name})
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        code = f"class {node.name}(...):"
        self._add("class_def", node.lineno, code, {"name": node.name})
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        code = self._safe_unparse(node)
        self._add("for_loop", node.lineno, code)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        code = self._safe_unparse(node)
        self._add("while_loop", node.lineno, code)
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        code = self._safe_unparse(node.test)  # show condition expression
        self._add("if_condition", node.lineno, code)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        code = self._safe_unparse(node)
        # heuristics for common data structure creation
        try:
            target = node.targets[0]
            if isinstance(node.value, ast.List):
                tname = getattr(target, "id", None) or "<target>"
                if tname and tname.lower() in ("stack", "queue"):
                    kind = "stack_create" if tname.lower() == "stack" else "queue_create"
                    self._add(kind, node.lineno, code, {"name": tname})
                    self.generic_visit(node)
                    return
            if isinstance(node.value, ast.Dict):
                self._add("dict_create", node.lineno, code)
                self.generic_visit(node)
                return
        except Exception:
            pass
        self._add("assign", node.lineno, code)
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr):
        # differentiate print(...) vs other expressions
        if isinstance(node.value, ast.Call):
            func = getattr(node.value.func, "id", "") or getattr(node.value.func, "attr", "")
            if func == "print":
                code = self._safe_unparse(node)
                self._add("print", node.lineno, code)
                self.generic_visit(node)
                return
        code = self._safe_unparse(node)
        self._add("expr", node.lineno, code)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        code = self._safe_unparse(node)
        func = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
        if func:
            self._add("call", node.lineno, code, {"func": func})
        else:
            self._add("call", node.lineno, code)
        self.generic_visit(node)

def parse_code_to_scene(code: str) -> List[Dict[str, Any]]:
    """
    Parse a string of Python code and return a list of scene steps.
    Raises ValueError on syntax errors.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"SyntaxError: {e}")

    parser = SceneASTParser()
    parser.visit(tree)
    return parser.steps
