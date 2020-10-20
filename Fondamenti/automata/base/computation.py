#!/usr/bin/env python3
"""Classes and methods for working with saved computations."""

from base.base import Base

class Computation(Base):
    """
    Representation of a computation performed by an automaton.

    By definition, it is a sequence of configurations.
    """

    def __init__(self, list_of_configurations, automaton):
        """Initialize computation."""
        self.configurations = list_of_configurations
        self.automaton = automaton

    @classmethod
    def empty(cls, automaton):
        """Return an empty computation."""
        return cls([], automaton)

    @property
    def generator(self):
        """Return a generator to loop over the sequence of configurations."""
        return (configuration for configuration in self.configurations)

    def add_configuration(self, configuration):
        """Add a configuration at the end of the computation."""
        self.configurations.append(configuration)
