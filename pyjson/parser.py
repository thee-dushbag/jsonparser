from .objects import Object, String, Number, Null, Boolean, Array
from .token import TokenType, Token
from .result import Okay, Error
import typing as ty
from .exc import (
    ParserError,
    MultiRootObjects,
    InvalidRoot,
    MissingToken,
    KeyError,
    TrailingComma,
    ValueError,
)

__all__ = ("Parser",)

T = ty.TypeVar("T")

if ty.TYPE_CHECKING:
    from .core import Value
else:
    Value = None


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._start: Token | None = None
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Error[ParserError] | Okay[Value]:
        try:
            return Okay(self._scan_root())
        except ParserError as e:
            return Error(e)

    def _scan_root(self) -> Value:
        root: Value | None = None
        match self.peek().token_type:
            case TokenType.LEFT_BRACE:
                root = self.consume_object()
            case TokenType.LEFT_BRAKET:
                root = self.consume_array()
        f = self.peek()
        if not self.empty():
            raise MultiRootObjects(
                f"Expected one root object. line {f.line} column {f.column}: {f.lexeme}"
            )
        if root is None:
            raise InvalidRoot(
                f"Expected root object to be a mapping or an array, found {f.lexeme}"
            )
        return root

    def consume_object(self) -> Object:
        start = self.advance()
        endtype: TokenType = TokenType.RIGHT_BRACE
        object = Object(
            self.consume_comma_sep_values(self.consume_object_pair, endtype)
        )
        if self.peek().token_type != endtype:
            raise MissingToken(
                f"Mapping opened at line {start.line} column {start.column} was never closed."
            )
        self.advance()
        return object

    def consume_object_pair(self):
        if (f := self.peek()).token_type != TokenType.STRING:
            raise KeyError(
                f"Expected map key to be a string, found {f.lexeme} on line {f.line} column {f.column}"
            )
        key = self.consume_string()
        if (f := self.peek()).token_type != TokenType.COLON:
            raise MissingToken(
                f"Expected a colon as key-value separator in mapping on line {f.line} column {f.column}"
            )
        self.advance()
        value = self.consume_value()
        return key, value

    def consume_array(self) -> Array:
        self.advance()
        endtype: TokenType = TokenType.RIGHT_BRAKET
        array = Array(self.consume_comma_sep_values(self.consume_value, endtype))
        if (f := self.peek()).token_type != endtype:
            raise MissingToken(
                f"Expected closing square bracket to close array on line {f.line} column {f.column}"
            )
        self.advance()
        return array

    def consume_comma_sep_values(
        self, consumer: ty.Callable[[], T], endtype: TokenType
    ) -> list[T]:
        values: list[T] = []
        while self.peek().token_type != endtype:
            values.append(consumer())
            if self.peek().token_type == TokenType.COMMA:
                self.advance()
                if (f := self.peek()).token_type == endtype:
                    raise TrailingComma(
                        f"trailing comma found on line {f.line} column {f.column}"
                    )
        return values

    def consume_value(self):
        match (f := self.peek()).token_type:
            case TokenType.LEFT_BRACE:
                return self.consume_object()
            case TokenType.LEFT_BRAKET:
                return self.consume_array()
            case TokenType.MINUS | TokenType.NUMBER:
                return self.consume_number()
            case TokenType.STRING:
                return self.consume_string()
            case TokenType.FALSE:
                return Boolean(self.advance(), False)
            case TokenType.TRUE:
                return Boolean(self.advance(), True)
            case TokenType.NULL:
                return Null(self.advance())
            case _:
                raise ValueError(
                    f"Expected a value, found {f.lexeme} on line {f.line} column {f.column}"
                )

    def consume_number(self) -> Number:
        buffer, token = [], self.peek()
        consume = lambda: buffer.append(self.advance().lexeme)
        if self.peek().token_type == TokenType.MINUS:
            consume()
        if (f := self.peek()).token_type != TokenType.NUMBER:
            raise MissingToken(
                f"Expected a number after the minus token on line {f.line} column {f.column}"
            )
        consume()
        if self.peek().token_type == TokenType.DOT:
            consume()
            if (f := self.peek()).token_type != TokenType.NUMBER:
                raise MissingToken(
                    f"Expected a number after the dot token on line {f.line} column {f.column}"
                )
            consume()
        if self.peek().token_type == TokenType.E:
            consume()
            if self.peek().token_type == TokenType.MINUS:
                consume()
            if (f := self.peek()).token_type != TokenType.NUMBER:
                raise MissingToken(
                    f"Expected a number after the e token on line {f.line} column {f.column}"
                )
            consume()
        return Number(token, "".join(buffer))

    def consume_string(self):
        return String(self.advance())

    def advance(self):
        consumed = self.peek()
        self._current += 1
        return consumed

    def empty(self):
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        return self._tokens[self._current]
