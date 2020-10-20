#!/usr/bin/env python3
"""Classes and methods for working with configurations."""

import abc
from base.base import Base


class Configuration(Base, metaclass=abc.ABCMeta):
    """
    Representation of the complete runtime state of an automaton.

    It is hashable and immutable.
    """
    
    def __init__(self, list_of_tokens, automaton):
        """
        Initialize a configuration.

        list_of_tokens is a tuple
        """
        if not list_of_tokens:
            self.list_of_tokens = tuple()
        elif isinstance(list_of_tokens, str):
            self.list_of_tokens = (list_of_tokens,)
        else:
            self.list_of_tokens = list_of_tokens
        self.automaton = automaton

    @abc.abstractmethod
    def validate(self):
        """Return True if this configuration is internally consistent."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_accepting(self):
        """Return True if this configuration is accepting."""
        raise NotImplementedError

    @property
    def next_token(self):
        """Return the first token of the input string in the configuration."""
        return self.list_of_tokens[0]

    @property
    def rest_of_tokens(self):
        """Return the rest of the input string in the configuration."""
        return self.list_of_tokens[1:]
