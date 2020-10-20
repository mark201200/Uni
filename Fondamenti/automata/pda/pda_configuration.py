#!/usr/bin/env python3
"""Classes and methods for working with PDA configurations."""


import abc

import automata.base.configuration as co


class PDAConfiguration(co.Configuration, metaclass=abc.ABCMeta):
    """
    Representation of the complete runtime state of a pushdown automaton.

    It is hashable and immutable.
    """

    @property
    def is_final(self):
        """Return True if this configuration is final."""
        return not self.list_of_tokens
