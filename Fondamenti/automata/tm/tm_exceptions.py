#!/usr/bin/env python3
"""Exception classes specific to Turing machines."""

import automata.base.automaton_exceptions as ae


class TMException(ae.AutomatonException):
    """The base class for all machine-related errors."""

    pass


class InvalidDirectionError(TMException):
    """A direction is not a valid direction for this machine."""

    pass


class BlankSymbolError(TMException):
    """Blank symbol is not a tape symbol."""

    pass


class InvalidDTMTransitionError(TMException):
    """Blank symbol is not a tape symbol."""

    pass


class UndefinedDTMTransitionException(ae.UndefinedTransitionException):
    """The current transition is undefined."""

    pass


class UndefinedNTMTransitionException(ae.UndefinedTransitionException):
    """The current transition is undefined."""

    pass


class InvalidDTMConfigurationError(TMException):
    """Invalid DTM configuration."""

    pass


class InvalidNTMConfigurationError(TMException):
    """Invalid NTM configuration."""

    pass

class InvalidAlphabets(TMException):
    """Invalid alphabets."""
    
    pass
