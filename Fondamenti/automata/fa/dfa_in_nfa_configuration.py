#!/usr/bin/env python3
"""Classes and methods for working with DFA configurations in nfa paths."""

import automata.fa.dfa_configuration as dfac


class DFAConfiguration_in_NFA(dfac.DFAConfiguration):
    """
    A deterministic configuration of a NFA, given by a couple of current state and a
    tuple with the remaining input.

    It represents the runtime state of a NFA in a deterministic path.
    It is hashable and immutable.

    Created by:
        DFAConfiguration_in_NFA
        DFAConfiguration_in_NFA.init
        DFAConfiguration_in_NFA.new
        DFAConfiguration_in_NFA.initial_configuration
        DFAConfiguration_in_NFA.next_configuration
        DFAConfiguration_in_NFA.next_epsilon_configuration


    A DFAConfiguration_in_NFA is coded as follows:
        - a state, defined as a string
        - the sequence of tokens to be read, coded as a Python tuple of strings
        - a reference to the associated automaton

    """

    def __init__(self, *, state, list_of_tokens, automaton):
        """
        Initialize a DFA configuration.

        Parameters are state, sequence of input tokens to be read given
        as a Python tuple, associated automaton
        """
        super().__init__(
            state=state,
            list_of_tokens=list_of_tokens,
            automaton=automaton)

    @classmethod
    def init(cls, state, input_str, automaton):
        """
        Initialize configuration.

        Parameters are state, string of chars to be read (assuming tokens have length 1),
        associated automaton
        """
        return super().init(state, input_str, automaton)

    @classmethod
    def new(cls, state, input_tokens, automaton):
        """
        Initialize configuration.

        Parameters are state, sequence of input tokens to be read, given as a Python
        list, associated automaton
        """
        return super().new(state, input_tokens, automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """Create a DFA initial configuration wrt the input string."""
        return super().initial_configuration(list_of_tokens, automaton)

    def next_configuration(self, next_state):
        """Return next configuration assuming a char is read."""
        return DFAConfiguration_in_NFA(state=next_state,
                                       list_of_tokens=self.rest_of_tokens,
                                       automaton=self.automaton)

    def next_epsilon_configuration(self, next_state):
        """Return next configuration assuming an epsilon transition."""
        return DFAConfiguration_in_NFA(state=next_state,
                                       list_of_tokens=self.list_of_tokens,
                                       automaton=self.automaton)

    def has_epsilon_transition(self):
        """
        Return True if an epsilon transition can be applied.

        Return True if there exists and epsilon transition that can be applied
        on this configuration.
        """
        epsilon_transition_exists = True
        try:
            _ = self.automaton.delta[self.state]['']
        except KeyError:
            epsilon_transition_exists = False
        return epsilon_transition_exists

    @property
    def is_final(self):
        """Return True if this configuration is final."""
        return not self.list_of_tokens and not self.has_epsilon_transition()
