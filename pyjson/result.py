import typing as ty

T = ty.TypeVar("T")


class Result(ty.Generic[T]):
    def __init__(self, result: T, /) -> None:
        self.result = result


class Okay(Result[T]): ...


class Error(Result[T], Exception): ...
