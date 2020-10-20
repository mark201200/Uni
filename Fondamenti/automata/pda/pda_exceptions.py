#!/usr/bin/env python3
"""Exception classes specific to pushdown automata."""


import automata.base.automaton_exceptions as ae


class PDAException(ae.AutomatonException):
    """The base class for all PDA-related errors."""

    pass


class NondeterminismError(PDAException):
    """A DPDA is exhibiting nondeterminism."""

    pass


class InvalidAcceptanceModeError(PDAException):
    """The given acceptance mode is invalid."""

    pass


class InvalidStackSymbolError(PDAException):
    """A stack symbol is not a valid symbol for this automaton."""

    pass


class EmptyStack(ae.InvalidTransitionError):
    """Stack is empty."""

    pass


class InvalidDPDAConfigurationError(ae.InvalidConfigurationError):
    """A configuration is not valid for this dpda."""

    pass


class InvalidNPDAConfigurationError(ae.InvalidConfigurationError):
    """A configuration is not valid for this npda."""

    pass


class InvalidPDATransitionError(ae.InvalidTransitionError):
    """A transition is not valid for this pda."""

    pass


class UndefinedDPDATransitionException(ae.UndefinedTransitionException):
    """The current transition is undefined."""

    pass


class UndefinedNPDATransitionException(ae.UndefinedTransitionException):
    """The current transition is undefined."""

    pass


class InvalidStackSymbolsError(PDAException):
    """Stack symbols are invalid."""

    pass
