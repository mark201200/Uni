#!/usr/bin/env python3
"""Exception classes shared by all finite automata."""

import automata.base.automaton_exceptions as ae


class InvalidDFAConfigurationError(ae.InvalidConfigurationError):
    """A configuration is not valid for this dfa."""

    pass


class InvalidNFAConfigurationError(ae.InvalidConfigurationError):
    """A configuration is not valid for this nfa."""

    pass


class InvalidFATransitionError(ae.InvalidTransitionError):
    """A transition is not valid for this fa."""

    pass


class UndefinedFATransitionException(ae.UndefinedTransitionException):
    """The current transition is undefined."""

    pass


class UndefinedNFATransitionException(ae.UndefinedTransitionException):
    """The current transition is undefined."""

    pass


class UndefinedDFATransitionException(ae.UndefinedTransitionException):
    """The current transition is undefined."""

    pass
