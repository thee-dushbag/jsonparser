import typing as ty

BaseTypes = dict | int | float | str | list | None | bool


class Visitor(ty.Protocol):
    def visit_object(self, object: "Value") -> dict[str, BaseTypes]:
        ...

    def visit_array(self, array: "Value") -> list[BaseTypes]:
        ...

    def visit_number(self, number: "Value") -> int | float:
        ...

    def visit_string(self, string: "Value") -> str:
        ...

    def visit_boolean(self, boolean: "Value") -> bool:
        ...

    def visit_null(self, null: "Value") -> None:
        ...


class Value(ty.Protocol):
    def accept(self, visitor: Visitor) -> BaseTypes:
        ...
