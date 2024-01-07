from .core import Visitor, Value
from .token import Token


class Object(Value):
    def __init__(self, value: list[tuple["String", Value]]) -> None:
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_object(self)


class Array(Value):
    def __init__(self, value: list[Value]) -> None:
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_array(self)


class String(Value):
    def __init__(self, token: Token) -> None:
        self.value = token.lexeme[1:-1]
        self.token = token

    def accept(self, visitor: Visitor):
        return visitor.visit_string(self)


class Number(Value):
    def __init__(self, token: Token, value: str) -> None:
        self.value = value
        self.token = token

    def accept(self, visitor: Visitor):
        return visitor.visit_number(self)


class Null(Value):
    def __init__(self, token: Token) -> None:
        self.value = None
        self.token = token

    def accept(self, visitor: Visitor):
        return visitor.visit_null(self)


class Boolean(Value):
    def __init__(self, token: Token, value: bool) -> None:
        self.value = value
        self.token = token

    def accept(self, visitor: Visitor):
        return visitor.visit_boolean(self)
