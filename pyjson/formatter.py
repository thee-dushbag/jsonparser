from typing import Any
from .core import Visitor, Value


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
    def __init__(self, string: str) -> None:
        self.value = f'"{string}"'

    def accept(self, visitor: Visitor):
        return visitor.visit_string(self)


class Number(Value):
    def __init__(self, value: int | float | str) -> None:
        self.value = str(value)

    def accept(self, visitor: Visitor):
        return visitor.visit_number(self)


class Null(Value):
    def __init__(self, value: None) -> None:
        self.value = "null"

    def accept(self, visitor: Visitor):
        return visitor.visit_null(self)


class Boolean(Value):
    def __init__(self, value: bool) -> None:
        self.value = str(value).lower()

    def accept(self, visitor: Visitor):
        return visitor.visit_boolean(self)


class Formatter(Visitor):
    def __init__(self, indent=None) -> None:
        self.indent = "" if indent is None else indent
        self.pairsep = ":" if indent is None else ": "
        self.arraysep = "," if indent is None else ", "
        self.linesep = "" if indent is None else "\n"
        self._depth = 0

    @property
    def dent(self) -> str:
        return self.indent * self._depth

    def visit_boolean(self, boolean: Boolean) -> str:
        return boolean.value

    def visit_null(self, null: Null) -> str:
        return null.value

    def visit_string(self, string: String) -> str:
        return string.value

    def visit_array(self, array: Array) -> str:
        brackets = '[', ']'
        values = [value.accept(self) for value in array.value]
        values = self.arraysep.join(values)
        if '\n' in values:
            self._depth += 1
            values = [self.dent + value.accept(self) for value in array.value]
            self._depth -= 1
            brackets = '[' + self.linesep, self.linesep + self.dent + ']'
            values = self.arraysep.join(values)
        return brackets[0] + values + brackets[1]

    def visit_object(self, object: Object) -> Any:
        self._depth += 1
        pairs = [
            f"{self.dent}{key.accept(self)}{self.pairsep}{value.accept(self)}"
            for key, value in object.value
        ]
        self._depth -= 1
        if not pairs:
            return "{}"
        return (
            "{"
            + self.linesep
            + (self.arraysep + self.linesep).join(pairs)
            + self.linesep
            + self.dent
            + "}"
        )

    def visit_number(self, number: Number) -> Any:
        return number.value

    def format(self, root: Value) -> str:
        return root.accept(self)
