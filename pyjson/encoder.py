from .formatter import Formatter, Object, Array, Null, Number, String, Boolean
from .token import Token, TokenType

def _dict(map: dict) -> Object:
    pairs = []
    for key, value in map.items():
        if type(key) != str:
            raise
        if type(value) not in _encoders:
            raise
        pair = _encoders[str](key), _encoders[type(value)](value)
        pairs.append(pair)
    return Object(pairs)

def _str(string: str) -> String:
    return String(string)

def _null(_: None):
    return Null(None)

def _number(number: int | float) -> Number:
    return Number(number)

def _boolean(value: bool) -> Boolean:
    return Boolean(value)

def _array(array: list) -> Array:
    values = []
    for value in array:
        if type(value) not in _encoders:
            raise
        values.append(_encoders[type(value)](value))
    return Array(values)

_encoders = {
    dict: _dict,
    str: _str,
    None: _null,
    int: _number,
    float: _number,
    bool: _boolean,
    list: _array
}

def encode(root, indent: str | None = None) -> str:
    formatter = Formatter(indent)
    if type(root) not in _encoders:
        raise
    root = _encoders[type(root)](root)
    return root.accept(formatter)
