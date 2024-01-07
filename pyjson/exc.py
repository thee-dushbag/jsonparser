class JsonError(Exception):
    ...


class JsonDecoderError(JsonError):
    ...


class ParserError(JsonDecoderError):
    ...


class MultiRootObjects(ParserError):
    ...


class InvalidRoot(ParserError):
    ...


class MissingToken(ParserError):
    ...


class KeyError(ParserError):
    ...


class ValueError(ParserError):
    ...


class TrailingComma(ParserError):
    ...


class LexerError(JsonDecoderError):
    ...


class MultilineString(LexerError):
    ...


class InvalidCharacter(LexerError):
    ...


class UnexpectedEndOfString(LexerError):
    ...
