from dataclasses import dataclass
from typing import Union, List


class TokenType:
    NUMBER = "number"
    PLUS_SIGN = "+"
    MULT_SIGN = "*"
    OPEN_PARENTHESIS = "open_par"
    CLOSE_PARENTHESIS = "close_par"
    OP = [PLUS_SIGN, MULT_SIGN]


@dataclass
class Token:
    token_type: str
    value: Union[str, int]


def tokenize(line: str) -> List[Token]:
    unprocessed_tokens = line.replace("(", "( ").replace(")", " )").split(" ")
    tokens = []
    while unprocessed_tokens:
        current_token = unprocessed_tokens.pop(0).strip()
        if not current_token:
            continue

        if current_token in "()":
            token = Token(TokenType.OPEN_PARENTHESIS, "(") if current_token == "(" else Token(
                TokenType.CLOSE_PARENTHESIS, ")")
            tokens.append(token)
            continue

        if current_token.isnumeric():
            token = Token(TokenType.NUMBER, int(current_token))
            tokens.append(token)
            continue

        if current_token in "+*":
            token = Token(TokenType.PLUS_SIGN if current_token == '+' else TokenType.MULT_SIGN, current_token)
            tokens.append(token)

    return tokens
