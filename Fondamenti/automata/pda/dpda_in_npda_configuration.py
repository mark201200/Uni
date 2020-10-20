##!/usr/bin/env python3
"""Classes and methods for working with DPDA configurations in npda paths."""

import automata.pda.dpda_configuration as dnpc


class DPDAConfiguration_in_NPDA(dnpc.DPDAConfiguration):
    """
    A deterministic configuration in a non deterministic path, given by a state+stack
    pair and a tuple with the remaining input.

    It represents the runtime state of a NPDA when a single deterministic path is
    considered.
    It is hashable and immutable.

    Created by:
        DPDAConfiguration_in_NPDA
        DPDAConfiguration_in_NPDA.init
        DPDAConfiguration_in_NPDA.new
        DPDAConfiguration_in_NPDA.initial_configuration
        DPDAConfiguration_in_NPDA.next_configuration

    A DPDAConfiguration_in_NPDA is encoded as follows:
        - an instance of StateStackPair, encapsulating the current state and stack
            content (encodes as an instance of PDAStack)
        - the sequence of tokens to be read, coded as a Python tuple of strings
        - a reference to the associated automaton

    """

    def __init__(self, *, state_stack_pair, list_of_tokens, automaton):
        """Initialize configuration."""
        super().__init__(
            state_stack_pair=state_stack_pair,
            list_of_tokens=list_of_tokens,
            automaton=automaton)

    @classmethod
    def init(cls, state, stack, input_str, automaton):
        """
        Create a DPDA configuration.

        Input and stack content are provided as string.
        """
        return super().init(state=state,
                            stack=stack,
                            input_str=input_str,
                            automaton=automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """Create a DPDA initial configuration wrt the input string."""
        return super().initial_configuration(list_of_tokens, automaton)

    def next_configuration(self, next_state, to_push):
        """Return next configuration."""
        state_stack_pair = self.update_pair(next_state, to_push)
        return DPDAConfiguration_in_NPDA(state_stack_pair=state_stack_pair,
                                         list_of_tokens=self.rest_of_tokens,
                                         automaton=self.automaton)

    def next_epsilon_configuration(self, next_state, to_push):
        """Return next configuration assuming an epsilon transition."""
        state_stack_pair = self.update_pair(next_state, to_push)
        return DPDAConfiguration_in_NPDA(state_stack_pair=state_stack_pair,
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
            _ = self.automaton.delta[self.state][''][self.top_of_stack]
        except KeyError:
            epsilon_transition_exists = False
        return epsilon_transition_exists

    @property
    def is_final(self):
        """Return True if this configuration is final."""
        return not (self.list_of_tokens or self.has_epsilon_transition())
