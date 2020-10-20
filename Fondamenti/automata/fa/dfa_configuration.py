#!/usr/bin/env python3
"""Classes and methods for working with DFA configurations."""

import tools.tools as tools
import automata.fa.fa_configuration as fac
import automata.fa.fa_exceptions as fae


class DFAConfiguration(fac.FAConfiguration):
    """
    A deterministic configuration, given by a couple of current state and a
    tuple with the remaining input.

    It represents the complete runtime state of a DFA.
    It is hashable and immutable.

    Created by:
        DFAConfiguration
        DFAConfiguration.init
        DFAConfiguration.new
        DFAConfiguration.initial_configuration
        DFAConfiguration.next_configuration


    A DFAConfiguration is coded as follows:
        - a state, defined as a string
        - the sequence of tokens to be read, coded as a Python tuple of strings
        - a reference to the associated automaton

    """

# -----------------------------------------------------------------------------
# Instantiation

    def __init__(self, *, state, list_of_tokens, automaton):
        """
        Initialize a DFA configuration.

        Parameters are state, sequence of input tokens to be read given
        as a Python tuple, associated automaton
        """
        super().__init__(list_of_tokens, automaton)
        self.state = state
        self.validate()

    @classmethod
    def init(cls, state, input_str, automaton):
        """
        Initialize configuration.

        Parameters are state, string of chars to be read (assuming tokens have length 1),
        associated automaton
        """
        return cls(state=state,
                   list_of_tokens=tools.Tools.tokens(input_str, separator=''),
                   automaton=automaton)

    @classmethod
    def new(cls, state, input_tokens, automaton):
        """
        Initialize configuration.

        Parameters are state, sequence of input tokens to be read, given as a Python
        list, associated automaton
        """
        return cls(state=state,
                   list_of_tokens=tuple(input_tokens),
                   automaton=automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """
        Create a DFA initial configuration wrt the input tokens.

        The input tokens are given as a tuple
        """
        return cls(state=automaton.initial_state,
                   list_of_tokens=list_of_tokens,
                   automaton=automaton)

    def next_configuration(self, next_state):
        """Return next configuration assuming a char is read."""
        return DFAConfiguration(state=next_state,
                                list_of_tokens=self.rest_of_tokens,
                                automaton=self.automaton)

# -----------------------------------------------------------------------------
# Validation

    def validate(self):
        """Return True if this configuration is internally consistent."""
        if self.state is None or self.state == '':
            raise fae.InvalidDFAConfigurationError(
                'no state defined in configuration')
        if self.automaton is None:
            raise fae.InvalidDFAConfigurationError(
                'no automaton associated to configuration')
        if self.state not in self.automaton.states:
            raise fae.InvalidDFAConfigurationError(
                'state invalid for automaton')
        if not set(self.list_of_tokens).issubset(self.automaton.input_symbols):
            raise fae.InvalidDFAConfigurationError(
                'string invalid for automaton')
        return True

# -----------------------------------------------------------------------------
# Properties

    @property
    def is_accepting(self):
        """Return True if this configuration is accepting."""
        return self.is_final and self.state in self.automaton_final_states

# -----------------------------------------------------------------------------
# Other

    def __str__(self):
        """Return a string representation of the configuration."""
        if self.automaton.all_chars_input:
            s = '{}\t {}'.format(self.state,
                                 tools.Tools.print(self.list_of_tokens))
        else:
            s = '{}\t {}'.format(self.state,
                                 tools.Tools.print_tuple(self.list_of_tokens))
        return s
