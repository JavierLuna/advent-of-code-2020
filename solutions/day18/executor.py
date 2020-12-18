from typing import Type

from solutions.day18.parsers import ExprNode, BaseParser
from solutions.day18.tokenizer import tokenize


def execute_expression(expression: str, parser: Type[BaseParser]) -> int:
    return execute_node(parser.parse_expression(tokenize(expression)))


def execute_node(expr_node: ExprNode) -> int:
    if not expr_node.op:
        return expr_node.left
    left, right = execute_node(expr_node.left), execute_node(expr_node.right)
    return left + right if expr_node.op == "+" else left * right
