import typing as ty

BaseTypes = dict | int | float | str | list | None | bool


class Visitor(ty.Protocol):
    def visit_object(self, object) -> ty.Any:
        ...

    def visit_array(self, array) -> ty.Any:
        ...

    def visit_number(self, number) -> ty.Any:
        ...

    def visit_string(self, string) -> ty.Any:
        ...

    def visit_boolean(self, boolean) -> ty.Any:
        ...

    def visit_null(self, null) -> ty.Any:
        ...


class Value(ty.Protocol):
    def accept(self, visitor: Visitor) -> ty.Any:
        ...
