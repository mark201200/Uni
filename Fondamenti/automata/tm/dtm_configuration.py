#!/usr/bin/env python3
"""Classes and methods for working with DTM configurations."""

# +
import tools.tools as tools

import automata.tm.tm_configuration as tmc
import automata.tm.state_tape_pair as stp
import automata.tm.tm_exceptions as tme


# -

class DTMConfiguration(tmc.TMConfiguration):
    """
    A deterministic configuration, given by a state, tape content and head positiont.

    It represents the complete runtime state of a DTM.
    It is hashable and immutable.

    Created by:
        DTMConfiguration
        DTMConfiguration.init
        DTMConfiguration.new
        DTMConfiguration.initial_configuration
        DTMConfiguration.next_configuration

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
        return cls(state_tape_pair=stp.StateTapePair.init(
                                        state=state,
                                        input_str=input_str,
                                        head=head,
                                        blank_symbol=automaton.blank_symbol),
                   automaton=automaton)

    @classmethod
    def new(cls, state, list_of_tokens, head, automaton):
        """Create a DTM configuration wrt the given state, string and head."""
        state_tape_pair = stp.StateTapePair.new(state, list_of_tokens, head,
                                                automaton.blank_symbol)
        return cls(state_tape_pair=state_tape_pair,
                   automaton=automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """Create a DTM initial configuration wrt the input string."""
        if not set(list_of_tokens).issubset(automaton.input_symbols):
            raise tme.InvalidDTMConfigurationError(
                'input invalid for dtm')
        state_tape_pair = stp.StateTapePair.initial_configuration(list_of_tokens,
                                                                  automaton)
        return cls(state_tape_pair=state_tape_pair,
                   automaton=automaton)

    def next_configuration(self, next_state, symbol, direction):
        """Return next configuration."""
        state_tape_pair = self.update_pair(next_state, symbol, direction)
        return DTMConfiguration(state_tape_pair=state_tape_pair,
                                automaton=self.automaton)

    def validate(self):
        """Return True if this configuration is internally consistent."""
        if self.automaton is None:
            raise tme.InvalidDTMConfigurationError(
                'no dtm associated to configuration')
        pair = self.state_tape_pair
        if pair.__class__.__name__ != 'StateTapePair':
            raise tme.InvalidDTMConfigurationError(
                'invalid pair in configuration')
        if self.state is None or self.state == '':
            raise tme.InvalidDTMConfigurationError(
                'no state defined in configuration')
        if self.state not in self.automaton.states.union(
                self.automaton.final_states):
            raise tme.InvalidDTMConfigurationError(
                'state invalid for dtm')
        if self.tape.__class__.__name__ != 'TMTape':
            raise tme.InvalidDTMConfigurationError(
                'invalid tape in configuration')
        if not set(self.tape_list_of_tokens).issubset(
                            self.automaton.tape_symbols.union(set(
                                self.automaton.blank_symbol))):
            raise tme.InvalidDTMConfigurationError(
                'tape invalid for dtm')
        return True

    @property
    def is_final(self):
        """Return True if this configuration is final."""
        return self.automaton._undefined_transition(self.state,
                                                    self.current_symbol)

    @property
    def is_accepting(self):
        """Return True if this configuration is accepting."""
        return self.state in self.automaton.final_states

    @property
    def state(self):
        """Return the state in the configuration."""
        return self.state_tape_pair.state

    @property
    def tape(self):
        """Return the tape in the configuration."""
        return self.state_tape_pair.tape

    @property
    def tape_symbols(self):
        """Return the symbols in the tape in the configuration."""
        return self.state_tape_pair.tape_symbols

    @property
    def tape_list_of_tokens(self):
        """Return the list of tokens in the tape in the configuration."""
        return self.state_tape_pair.tape_list_of_tokens

    @property
    def head(self):
        """Return the position of the tape head in the configuration."""
        return self.state_tape_pair.head

    @property
    def current_symbol(self):
        """Return the tape symbol under the head."""
        return self.state_tape_pair.current_symbol

    @property
    def state_tape_head(self):
        """Return the 3-tuple of state, tape symbols, and head positions."""
        return self.state_tape_pair.state_tape_head

    def update_pair(self, new_state, symbol, direction):
        """Return pair for next configuration."""
        return self.state_tape_pair.update_pair(new_state, symbol, direction)

    def __str__(self):
        """Return a string representation of the configuration."""
        head = self.head
        tape = self.tape_list_of_tokens
        prefix = list(tape[:head])
        suffix = list(tape[head+1:])
        current_symbol = "\033[4m"+tape[head]+"\033[0m"
        lst = prefix
        lst.append(current_symbol)
        lst.extend(suffix)
        if self.automaton.all_chars_tape:
            s = "({}, {})".format(self.state, tools.Tools.print(lst))
        else:
            s = "({}, {})".format(self.state, tools.Tools.print_tuple(lst))
        return s
