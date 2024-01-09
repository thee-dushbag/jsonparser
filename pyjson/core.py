import typing as ty

BaseTypes = dict | int | float | str | list | None | bool


class Visitor(ty.Protocol):
    def visit_object(self, object: "Value") -> ty.Any:
        ...

    def visit_array(self, array: "Value") -> ty.Any:
        ...

    def visit_number(self, number: "Value") -> ty.Any:
        ...

    def visit_string(self, string: "Value") -> ty.Any:
        ...

    def visit_boolean(self, boolean: "Value") -> ty.Any:
        ...

    def visit_null(self, null: "Value") -> ty.Any:
        ...


class Value(ty.Protocol):
    def accept(self, visitor: Visitor) -> ty.Any:
        ...
