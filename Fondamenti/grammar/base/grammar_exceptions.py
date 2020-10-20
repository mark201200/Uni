#!/usr/bin/env python3
"""Exception classes shared by all grammars."""


class GrammarException(Exception):
    """The base class for all grammar-related errors."""


class InvalidTerminalsError(GrammarException):
    """Invalid terminals in grammar error."""

    pass


class InvalidNonTerminalsError(GrammarException):
    """Invalid non terminals in grammar error."""

    pass


class InvalidAxiomError(GrammarException):
    """Invalid axiom in grammar error."""

    pass


class InvalidSymbolError(GrammarException):
    """Invalid symbol in production."""

    pass


class InvalidLeftPartError(GrammarException):
    """Invalid left part of production."""

    pass


class InvalidRightPartError(GrammarException):
    """Invalid right part of production."""

    pass
