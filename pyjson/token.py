import enum

__all__ = "TokenType", "Token"


class TokenType(enum.StrEnum):
    RIGHT_BRAKET = enum.auto()
    RIGHT_BRACE = enum.auto()
    LEFT_BRAKET = enum.auto()
    LEFT_BRACE = enum.auto()
    NUMBER = enum.auto()
    STRING = enum.auto()
    QUOTE = enum.auto()
    MINUS = enum.auto()
    FALSE = enum.auto()
    COLON = enum.auto()
    COMMA = enum.auto()
    NULL = enum.auto()
    TRUE = enum.auto()
    EOF = enum.auto()
    DOT = enum.auto()
    E = enum.auto()


class Token:
    def __init__(
        self, *, token_type: TokenType, column: int, line: int, lexeme: str
    ) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.column = column
        self.line = line

    def __str__(self) -> str:
        return (
            f"Token(type={self.token_type!r}, lexeme="
            f"{self.lexeme!r}, at={self.line, self.column})"
        )

    __repr__ = __str__
