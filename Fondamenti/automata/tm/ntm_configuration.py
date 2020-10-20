#!/usr/bin/env python3
"""Classes and methods for working with NDTM configurations."""


# +
import tools.tools as tools

import automata.tm.tm_configuration as tmc
import automata.tm.state_tape_pair as stp
# -

import automata.tm.tm_exceptions as tme


class NTMConfiguration(tmc.TMConfiguration):
    """
    A non deterministic configuration, given by a set of states plus tape content, plus
    head positions.

    It represents the complete runtime state of a NTM.
    It is hashable and immutable.

    Created by:
        NTMConfiguration
        NTMConfiguration.init
        NTMConfiguration.new
        NTMConfiguration.initial_configuration
        NTMConfiguration.next_configuration

    A NTMConfiguration is encoded as follows:
        - a set of instances of StateTapePair, each encapsulating a current state and tape
            content+head position (encoded as an instance of TMTape)
        - a reference to the associated automaton

    """

    def __init__(self, *, state_tape_pairs, automaton):
        """Initialize configuration."""
        self.state_tape_pairs = state_tape_pairs
        self.automaton = automaton
        self.validate()

    @classmethod
    def new(cls, state, list_of_tokens, head, automaton):
        """Create a NTM configuration wrt the given state, string and head."""
        state_tape_pairs = {stp.StateTapePair.new(state, list_of_tokens, head,
                                                  automaton.blank_symbol)}
        return cls(state_tape_pair=state_tape_pairs, automaton=automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """Create a NTM initial configuration wrt the input string."""
        if not set(list_of_tokens).issubset(automaton.input_symbols):
            raise tme.InvalidNTMConfigurationError(
                'input invalid for ntm')
        state_tape_pairs = {stp.StateTapePair.initial_configuration(list_of_tokens,
                                                                    automaton)}
        return cls(state_tape_pairs=state_tape_pairs, automaton=automaton)

    def next_configuration(self, new_pairs):
        """Return next configuration."""
        return NTMConfiguration(state_tape_pairs=new_pairs,
                                automaton=self.automaton)

    def validate(self):
        """Return True if this configuration is internally consistent."""
        if self.automaton is None:
            raise tme.InvalidNTMConfigurationError(
                'no ntm associated to configuration')
        for pair in self.state_tape_pairs:
            if pair.__class__.__name__ != 'StateTapePair':
                raise tme.InvalidNTMConfigurationError(
                    'invalid pair in configuration')
            if pair.state is None or pair.state == '':
                raise tme.InvalidNTMConfigurationError(
                    'no state defined in configuration')
            if pair.state not in self.automaton.states.union(
                    self.automaton.final_states):
                raise tme.InvalidNTMConfigurationError(
                    'state invalid for ntm')
            if pair.tape.__class__.__name__ != 'TMTape':
                raise tme.InvalidNTMConfigurationError(
                    'invalid tape in configuration')
            if not set(pair.tape_list_of_tokens).issubset(
                    self.automaton.tape_symbols.union(set(self.automaton.blank_symbol))):
                raise tme.InvalidNTMConfigurationError(
                    'tape invalid for ntm')
        return True

    def number_of_pairs(self):
        """Return the number of pairs in the configuration."""
        return len(self.state_tape_pairs)

    @property
    def is_final(self):
        """Return True if this configuration is final."""
        final = True
        for pair in self.state_tape_pairs:
            if not self.automaton._undefined_transition(pair.state,
                                                        pair.current_symbol):
                final = False
        return final

    @property
    def is_accepting(self):
        """Return True if this configuration is accepting."""
        one_final_state = False
        for pair in self.state_tape_pairs:
            if pair.state in self.automaton.final_states:
                one_final_state = True
        return one_final_state

    def __str__(self):
        """Return a string representation of the configuration."""
        s = '{'
        for pair in self.state_tape_pairs:
            state, tape, head = pair.state_tape_head
            prefix = list(tape[:head])
            suffix = list(tape[head+1:])
            current_symbol = "\033[4m"+tape[head]+"\033[0m"
            lst = prefix
            lst.append(current_symbol)
            lst.extend(suffix)
            if self.automaton.all_chars_tape:
                s += "({}, {}), ".format(state, tools.Tools.print(lst))
            else:
                s += "({}, {}), ".format(state, tools.Tools.print_tuple(lst))
        s = s[:-2]
        return s+'}'


