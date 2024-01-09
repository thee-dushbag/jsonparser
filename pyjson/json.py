from .encoder import encode as dumps
from .composer import Composer
from .core import BaseTypes
from .parser import Parser
from pathlib import Path
from .lexer import Lexer

__all__ = "load", "loads", "dumps", "dump"


def load(filepath: Path | str):
    filepath = Path(str(filepath))
    return loads(filepath.read_text())


def dump(filepath: Path | str, obj):
    Path(str(filepath)).write_text(dumps(obj))


def loads(source: str) -> BaseTypes:
    tokens = Lexer(source).tokenize()
    if isinstance(tokens, Exception):
        raise tokens.result
    ast = Parser(tokens.result).parse()
    if isinstance(ast, Exception):
        raise ast.result
    composer = Composer().compose
    return composer(ast.result)
