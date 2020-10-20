##!/usr/bin/env python3
"""Classes and methods for working with DTM configurations in ntm paths."""


import automata.tm.dtm_configuration as dtmc

class DTMConfiguration_in_NTM(dtmc.DTMConfiguration):
    """
    A deterministic configuration, given by a state, tape content and head positiont.

    It represents the runtime state of a deterministic path in a NTM computation.
    It is hashable and immutable.

    Created by:
        DTMConfiguration_in_NTM
        DTMConfiguration_in_NTM.init
        DTMConfiguration_in_NTM.new
        DTMConfiguration_in_NTM.initial_configuration
        DTMConfiguration_in_NTM.next_configuration

    A DTMConfiguration is encoded as follows:
        - an instance of StateTapePair, encapsulating the current state and tape
            content+ head position (encoded as an instance of TMTape)
        - a reference to the associated automaton

    """

    def __init__(self, *, state_tape_pair, automaton):
        """Initialize configuration."""
        self.state_tape_pair = state_tape_pair
        self.automaton = automaton
        self.validate()

    @classmethod
    def init(cls, *, state, input_str, automaton, head=0):
        """
        Create a DTM configuration.

        Tape content is provided as string.
        """
        return super().init(state=state,
                            input_str=input_str,
                            automaton=automaton)

    @classmethod
    def new(cls, state, list_of_tokens, head, automaton):
        """Create a DTM configuration wrt the given state, string and head."""
        return super().new(state, list_of_tokens, head, automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """Create a DTM initial configuration wrt the input string."""
        return super().initial_configuration(list_of_tokens, automaton)

    def next_configuration(self, next_state, new_symbol, new_direction):
        """Return next configuration."""
        state_tape_pair = self.update_pair(next_state,
                                           new_symbol,
                                           new_direction)
        return DTMConfiguration_in_NTM(state_tape_pair=state_tape_pair,
                                       automaton=self.automaton)
