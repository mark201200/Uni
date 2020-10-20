#!/usr/bin/env python3
"""Classes and methods for working with configurations."""


import abc

import automata.base.configuration as conf


class FAConfiguration(conf.Configuration, metaclass=abc.ABCMeta):
    """
    Representation of the complete runtime state of a finite automaton.

    It is hashable and immutable.
    """

    def __init__(self, list_of_tokens, automaton):
        """
        Initialize a FA configuration.

        list_of_tokens is a tuple
        """
        super().__init__(list_of_tokens, automaton)

    @property
    def is_final(self):
        """Return True if this configuration is final."""
        return len(self.list_of_tokens) == 0

    @property
    def automaton_final_states(self):
        """Return the automaton associated to the configuration."""
        return self.automaton.final_states
