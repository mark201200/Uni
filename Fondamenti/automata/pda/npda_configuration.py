#!/usr/bin/env python3
"""Classes and methods for working with NPDA configurations."""

import tools.tools as tools
from automata.pda.pda_configuration import PDAConfiguration
from automata.pda.state_stack_pair import StateStackPair

import automata.pda.pda_exceptions as pae


class NPDAConfiguration(PDAConfiguration):
    """
    A non deterministic configuration, given by a set of state+stack pairs plus a
    tuple with the remaining input.

    It represents the complete runtime state of a NPDA.
    It is hashable and immutable.

    Created by:
        NPDAConfiguration
        NPDAConfiguration.init
        NPDAConfiguration.new
        NPDAConfiguration.initial_configuration
        NPDAConfiguration.next_configuration

    A NPDAConfiguration is encoded as follows:
        - a set of instances of StateStackPair, encapsulating the current state and stack
            content (encoded as an instance of PDAStack)
        - the sequence of tokens to be read, coded as a Python tuple of strings
        - a reference to the associated automaton

    """

    def __init__(self, *, state_stack_pairs, list_of_tokens, automaton):
        """Initialize configuration."""
        self.state_stack_pairs = state_stack_pairs
        self.list_of_tokens = list_of_tokens
        self.automaton = automaton
        self.validate()

    @classmethod
    def init(cls, *, state_stack_pairs, input_str, automaton):
        """Create NPDA configuration wrt the input string and set of pairs."""
        list_of_tokens = tools.Tools.list_of_tokens(input_str)
        return cls(state_stack_pairs=state_stack_pairs,
                   list_of_tokens=list_of_tokens,
                   automaton=automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """Create a NPDA initial configuration wrt the input string."""
        state_stack_pairs = {StateStackPair.new(
                            state=automaton.initial_state,
                            list_of_stack_items=automaton.initial_stack_symbol)}
        return cls(state_stack_pairs=state_stack_pairs,
                   list_of_tokens=list_of_tokens,
                   automaton=automaton)

    def next_configuration(self, new_pairs):
        """Return next configuration."""
        return NPDAConfiguration(state_stack_pairs=new_pairs,
                                 list_of_tokens=self.rest_of_tokens,
                                 automaton=self.automaton)

    def next_epsilon_configuration(self, new_pairs):
        """Return next configuration by epsilon transition."""
        return NPDAConfiguration(state_stack_pairs=new_pairs,
                                 list_of_tokens=self.list_of_tokens,
                                 automaton=self.automaton)

    def validate(self):
        """Return True if this configuration is internally consistent."""
        if self.automaton is None:
            raise pae.InvalidNPDAConfigurationError(
                'no npda associated to configuration')
        if not set(self.list_of_tokens).issubset(self.automaton.input_symbols):
            raise pae.InvalidNPDAConfigurationError(
                'string invalid for npda')
        for pair in self.state_stack_pairs:
            if pair.__class__.__name__ != 'StateStackPair':
                raise pae.InvalidNPDAConfigurationError(
                    'invalid pair in configuration')
            if pair.state is None or pair.state == '':
                raise pae.InvalidNPDAConfigurationError(
                    'no state defined in configuration')
            if pair.state not in self.automaton.states:
                raise pae.InvalidNPDAConfigurationError(
                    'state invalid for npda in configuration')
            if not set(pair.stack_items).issubset(
                    self.automaton.stack_symbols):
                raise pae.InvalidNPDAConfigurationError(
                    'stack invalid for npda in configuration')
        return True

    @property
    def is_accepting(self):
        """Return True if this configuration is accepting."""
        if self.automaton.acceptance_mode == 'F':
            states = set([pair.state for pair in self.state_stack_pairs])
            if states.intersection(self.automaton.final_states):
                final_state = True
            else:
                final_state = False
            return self.is_final and final_state
        else:
            zero_stack_sizes = [1 for pair in self.state_stack_pairs
                                if len(pair.stack_items) == 0]
            if len(zero_stack_sizes) > 0:
                empty_stack = True
            else:
                empty_stack = False
        return self.is_final and empty_stack

    @property
    def number_of_pairs(self):
        """Return the number of state+stack pairs."""
        return len(self.state_stack_pairs)

    @property
    def pairs_iterator(self):
        """Return an iterator over all state+stack pairs."""
        return iter(self.state_stack_pairs)

    def __repr__(self):
        """Return a string representation of the configuration."""
        s = '{} ({} \n'.format(self.__class__.__name__,
                               self.list_of_tokens)
        for ssp in self.state_stack_pairs:
            s += '({} {}) \n'.format(ssp.__class__.__name__, ssp)
        s += ')'
        return s

    # def __str__(self):
    #     """Return a string representation of the configuration."""
    #     s = '{}\t'.format(Tools.output_string_from_tokens(self.list_of_tokens))
    #     s += '{'
    #     for ssp in self.state_stack_pairs:
    #         s += '{}, '.format(ssp)
    #     s = s[:-2]
    #     s += '}'
    #     return s

    def __str__(self):
        """Return a string representation of the configuration."""
        if self.automaton.all_chars_input:
            s = '{}\t'.format(tools.Tools.print(self.list_of_tokens))
        else:
            s = '{}\t'.format(tools.Tools.print_tuple(self.list_of_tokens))
        s += ' {'
        for ssp in self.state_stack_pairs:
            s += '({}, '.format(ssp.state)
            if self.automaton.all_chars_stack:
                s += '{}), '.format(tools.Tools.print(ssp.stack_items))
            else:
                s += ' {}), '.format(tools.Tools.print_tuple(ssp.stack_items))
        s = s[:-2]
        s += '}'
        return s
