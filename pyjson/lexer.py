from .exc import (
    MultilineString,
    UnexpectedEndOfString,
    InvalidCharacter,
    LexerError,
)
from .result import Okay, Error
from .token import TokenType, Token

__all__ = ("Lexer",)


class Lexer:
    """
    Note: This is a one time use object.
    If resused, the initial state may
    interfere with the next lexing.
    To reuse, call reset with some new
    source or retokenize the internal source
    """

    def __init__(self, source: str) -> None:
        self._tokens: list[Token] = []
        self._stop = len(source)
        self._tokenized = False
        self._start_column = 0
        self._source = source
        self._current = 0
        self._column = 0
        self._start = 0
        self._line = 1

    def reset(self, src: str | None = None):
        self.__init__(self._source if src is None else src)

    def tokenize(self) -> Okay[list[Token]] | Error[LexerError]:
        try:
            self._scan()
            return Okay(self._tokens)
        except LexerError as e:
            return Error(e)

    def _scan(self) -> list[Token]:
        while not self.empty():
            match self.peek():
                case " " | "\t" | "\v" | "\f":
                    self.consume(1)
                case "\n":
                    self.advance_line()
                    self.consume(1)
                case "]":
                    self.add_token(TokenType.RIGHT_BRAKET, 1)
                case "}":
                    self.add_token(TokenType.RIGHT_BRACE, 1)
                case "[":
                    self.add_token(TokenType.LEFT_BRAKET, 1)
                case "{":
                    self.add_token(TokenType.LEFT_BRACE, 1)
                case ":":
                    self.add_token(TokenType.COLON, 1)
                case ",":
                    self.add_token(TokenType.COMMA, 1)
                case "-":
                    self.add_token(TokenType.MINUS, 1)
                case '"':
                    self.string()
                case "t":
                    self.match(TokenType.TRUE, "true")
                case "f":
                    self.match(TokenType.FALSE, "false")
                case "n":
                    self.match(TokenType.NULL, "null")
                case ".":
                    self.add_token(TokenType.DOT, 1)
                case "e" | "E":
                    self.add_token(TokenType.E, 1)
                case char:
                    if self.isdigit(char):
                        self.number()
                    else:
                        raise InvalidCharacter
        if not self._tokens or self._tokens[-1] != TokenType.EOF:
            self._tokens.append(self._eof_token())
        return self._tokens

    def add_token(self, token_type: TokenType, count: int = 0):
        lexeme, col = self.consume(count)
        token = Token(token_type=token_type, column=col, line=self._line, lexeme=lexeme)
        self._tokens.append(token)

    def _eof_token(self) -> Token:
        return Token(
            token_type=TokenType.EOF,
            column=self._start_column,
            lexeme="",
            line=self._line,
        )

    def number(self):
        while not self.empty() and self.isdigit(self.peek()):
            self.advance()
        self.add_token(TokenType.NUMBER)

    def string(self):
        self.advance()
        while not self.empty():
            char = self.peek()
            self.advance()
            if char == '"':
                return self.add_token(TokenType.STRING)
            if char == "\n":
                raise MultilineString(
                    f"Multiline string are not supported. line {self._line}"
                )
        raise UnexpectedEndOfString(f"Expected a closing quote. line {self._line}")

    def match(self, token_type: TokenType, string: str):
        for char in string:
            if self.peek() != char:
                break
            self.advance()
        if self._lexeme() != string:
            raise InvalidCharacter(
                f"Invalid token encountered {self.peek()!r}, did you mean {string!r}"
            )
        self.add_token(token_type)

    def empty(self) -> bool:
        return self._current >= self._stop

    def peek(self) -> str:
        return self._source[self._current]

    def _lexeme(self) -> str:
        return self._source[self._start : self._current]

    def advance(self, count: int = 1):
        self._current += count
        self._column += count
        return self._lexeme()

    def consume(self, count: int = 0):
        consumed = self.advance(count), self._start_column
        self._start = self._current
        self._start_column = self._column
        return consumed

    def advance_line(self, count: int = 1):
        self._line += count
        self._column = 0

    def isdigit(self, char: str) -> bool:
        return ord("0") <= ord(char) <= ord("9")
