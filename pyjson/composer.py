from .core import Visitor, Value
import typing as ty

if ty.TYPE_CHECKING:
    from .objects import Array, Object, String, Boolean, Null, Number
else:
    Object = Array = String = Boolean = Number = Null = None


class Composer(Visitor):
    def visit_array(self, array: Array):
        return [value.accept(self) for value in array.value]

    def visit_object(self, object: Object):
        return {key.accept(self): value.accept(self) for key, value in object.value}

    def visit_boolean(self, boolean: Boolean):
        return boolean.value

    def visit_null(self, null: Null):
        return null.value

    def visit_number(self, number: Number):
        _fdefs = {"e", "E", "."}
        _vdefs = set(number.value)
        _type = float if _fdefs & _vdefs else int
        return _type(number.value)

    def visit_string(self, string: String):
        return string.value

    def compose(self, root: Value):
        return root.accept(self)
