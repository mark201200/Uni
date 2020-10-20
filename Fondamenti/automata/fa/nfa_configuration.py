##!/usr/bin/env python3
"""Classes and methods for working with NFA configurations."""

import tools.tools as tools
import automata.fa.fa_configuration as fac

import automata.fa.fa_exceptions as fae


class NFAConfiguration(fac.FAConfiguration):
    """
    A nondeterministic configuration, given by a couple of current ste of state and a
    tuple with the remaining input.

    It represents the complete runtime state of a NFA.
    It is hashable and immutable.

    Created by:
        NFAConfiguration()
        NFAConfiguration.init()
        NFAConfiguration.new()
        NFAConfiguration.next_configuration
        NFAConfiguration.next_epsilon_configuration


    A NFAConfiguration is coded as follows:
        - a set of states, defined as a (possibly empty) Python set of strings
        - the sequence of tokens to be read, coded as a Python tuple of strings
        - a reference to the associated automaton

    """

    def __init__(self, *, states, list_of_tokens, automaton):
        """
        Initialize a NFA configuration.

        Parameters are ste of states, sequence of input tokens to be read given
        as a Python tuple, associated automaton
        """
        super().__init__(list_of_tokens, automaton)
        self.states = states
        self.validate()

    @classmethod
    def init(cls, states, input_str, automaton):
        """
        Initialize configuration.

        Parameters are set of states, string of chars to be read (assuming tokens have
        length 1), associated automaton
        """
        list_of_tokens = tools.Tools.tokens(input_str)
        return cls(states=states,
                   list_of_tokens=list_of_tokens,
                   automaton=automaton)

    @classmethod
    def new(cls, states, input_tokens, automaton):
        """
        Initialize configuration.

        Parameters are set of states, sequence of input tokens to be read, given as a
        Python list, associated automaton
        """
        return cls(states=states,
                   list_of_tokens=tuple(input_tokens),
                   automaton=automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """
        Create a NFA initial configuration wrt the input tokens.

        The input tokens are given as a tuple
        """
        return cls(states={automaton.initial_state},
                   list_of_tokens=list_of_tokens,
                   automaton=automaton)

    def next_configuration(self, next_states):
        """Return next configuration."""
        return NFAConfiguration(states=next_states,
                                list_of_tokens=self.rest_of_tokens,
                                automaton=self.automaton)

    def next_epsilon_configuration(self, next_states):
        """
        Return next configuration, assuming an epsilon transition,
        not consuming chars.
        """
        return NFAConfiguration(states=next_states,
                                list_of_tokens=self.list_of_tokens,
                                automaton=self.automaton)

    def validate(self):
        """Return True if this configuration is internally consistent."""
        if self.states is None or len(self.states) == 0:
            raise fae.InvalidNFAConfigurationError(
                'no state defined in configuration')
        if self.automaton is None:
            raise fae.InvalidNFAConfigurationError(
                'no nfa associated to configuration')
        if not self.states.issubset(self.automaton.states):
            raise fae.InvalidNFAConfigurationError(
                'state invalid for nfa')
        if not set(self.list_of_tokens).issubset(self.automaton.input_symbols):
            raise fae.InvalidNFAConfigurationError(
                'string invalid for nfa')
        return True

    @property
    def is_accepting(self):
        """Return True if this configuration is accepting."""
        if self.states.intersection(self.automaton.final_states):
            final_state = True
        else:
            final_state = False
        return self.is_final and final_state

    @property
    def states_iterator(self):
        """Return an iterator over all states."""
        return iter(self.states)

    @property
    def number_of_configurations(self):
        """Return the number of states."""
        return len(self.states)

    @property
    def number_of_states(self):
        """Return the number of states."""
        return len(self.states)

    def __repr__(self):
        """Associate a description of the object to its identifier."""
        return repr(self.__dict__)

    def __str__(self):
        """Return a string representation of the configuration."""
        if self.automaton.all_chars_input:
            s = '{}\t'.format(tools.Tools.print(self.list_of_tokens))
        else:
            s = '{} \t'.format(tools.Tools.print_tuple(
                self.list_of_tokens, separator=' '))
        s += '{'
        if len(self.states) > 0:
            for item in self.states:
                s += '{}, '.format(item)
            s = s[:-2]
            s += '}'
        return s
