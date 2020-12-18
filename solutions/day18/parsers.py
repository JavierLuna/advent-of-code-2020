from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import Union, Optional, List

from solutions.day18.tokenizer import Token, TokenType


@dataclass
class ExprNode:
    op: str
    left: Union["ExprNode", int, None]
    right: Optional["ExprNode"]


class BaseParser(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def parse_expression(cls, tokens: List[Token]) -> ExprNode:
        raise NotImplementedError()

    @classmethod
    def parse_val(cls, tokens: List[Token]) -> ExprNode:
        if cls.peek(tokens, TokenType.OPEN_PARENTHESIS):
            cls.consume(tokens, TokenType.OPEN_PARENTHESIS)
            node = cls.parse_expression(tokens)
            cls.consume(tokens, TokenType.CLOSE_PARENTHESIS)
            return node
        return ExprNode("", cls.consume(tokens, TokenType.NUMBER).value, None)

    @classmethod
    def peek(cls, tokens: List[Token], expected_token_type: Union[str, List[str]]) -> bool:
        expected_token_type = [expected_token_type] if isinstance(expected_token_type, str) else expected_token_type
        return tokens and tokens[0].token_type in expected_token_type

    @classmethod
    def consume(cls, tokens: List[Token], expected_token_type: Union[str, List[str]]) -> Token:
        assert cls.peek(tokens, expected_token_type)
        return tokens.pop(0)


class Part1Parser(BaseParser):
    """
    expression ::= mult_op
    mult_op ::= add_op ('*' add_op)*
    add_op ::= val ('+' val)*
    val :== '(' expression ')' | number
    """

    @classmethod
    def parse_expression(cls, tokens: List[Token]) -> ExprNode:
        return cls.parse_op(tokens)

    @classmethod
    def parse_op(cls, tokens: List[Token]) -> ExprNode:
        node = cls.parse_val(tokens)
        while cls.peek(tokens, TokenType.OP):
            node = ExprNode(cls.consume(tokens, TokenType.OP).value, node, cls.parse_val(tokens))
        return node


class Part2Parser(BaseParser):
    """
    expression ::= mult_op
    mult_op ::= add_op ('*' add_op)*
    add_op ::= val ('+' val)*
    val :== '(' expression ')' | number
    """

    @classmethod
    def parse_expression(cls, tokens: List[Token]) -> ExprNode:
        return cls.parse_mult_op(tokens)

    @classmethod
    def parse_mult_op(cls, tokens: List[Token]) -> ExprNode:
        node = cls.parse_add_op(tokens)
        while cls.peek(tokens, TokenType.MULT_SIGN):
            node = ExprNode(cls.consume(tokens, TokenType.MULT_SIGN).value, node, cls.parse_mult_op(tokens))
        return node

    @classmethod
    def parse_add_op(cls, tokens: List[Token]) -> ExprNode:
        node = cls.parse_val(tokens)
        while cls.peek(tokens, TokenType.PLUS_SIGN):
            node = ExprNode(cls.consume(tokens, TokenType.PLUS_SIGN).value, node, cls.parse_add_op(tokens))
        return node
