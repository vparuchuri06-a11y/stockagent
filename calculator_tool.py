import ast #abstract syntax tree
import operator
import re
from crewai.tools import tool   # ✅ CORRECT FOR YOUR VERSION

@tool("Calculator")
def calculator(expression: str) -> float:
    """
    Safely evaluate mathematical expressions like:
    200*7, (5000/2)*10, 100000*1.15
    """
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    if not re.match(r'^[0-9+\-*/().% ]+$', expression):
        raise ValueError("Invalid characters in expression")

    tree = ast.parse(expression, mode="eval")

    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return allowed_operators[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )
        elif isinstance(node, ast.UnaryOp):
            return allowed_operators[type(node.op)](
                eval_node(node.operand)
            )
        else:
            raise ValueError("Unsupported expression")

    return eval_node(tree)
