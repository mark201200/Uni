#!/usr/bin/env python3
"""Exception classes shared by all parsers."""


class ParserException(Exception):
    """The base class for all parser-related errors."""

    pass


class InvalidGrammarException(ParserException):
    """The grammar is not valid for this parser."""

    pass


class InvalidStringException(ParserException):
    """The string to be parsed is not valid for the grammar."""

    pass

class ParsingError(ParserException):
    """Some error during parsing."""

    pass

class NoParseTable(ParserException):
    """Parse table not generated."""

    pass

class StringNotAccepted(ParserException):
    """Parse table not generated."""

    pass

class AmbiguousDerivation(ParserException):
    """Parse table not generated."""

    pass