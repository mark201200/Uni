#!/usr/bin/env python3
"""Classes and methods for working with DPDA configurations."""

import tools.tools as tools
import automata.pda.pda_configuration as dpc
import automata.pda.state_stack_pair as ssp

import automata.pda.pda_exceptions as pae


class DPDAConfiguration(dpc.PDAConfiguration):
    """
    A deterministic configuration, given by a state+stack pair and a
    tuple with the remaining input.

    It represents the complete runtime state of a DPDA.
    It is hashable and immutable.

    Created by:
        DPDAConfiguration
        DPDAConfiguration.init
        DPDAConfiguration.new
        DPDAConfiguration.initial_configuration
        DPDAConfiguration.next_configuration

    A DPDAConfiguration is encoded as follows:
        - an instance of StateStackPair, encapsulating the current state and stack
            content (encoded as an instance of PDAStack)
        - the sequence of tokens to be read, coded as a Python tuple of strings
        - a reference to the associated automaton

    """

    def __init__(self, *, state_stack_pair, list_of_tokens, automaton):
        """
        Initialize a DPDA configuration.

        list_of_tokens is a tuple
        """
        self.state_stack_pair = state_stack_pair
        self.list_of_tokens = list_of_tokens
        self.automaton = automaton

    @classmethod
    def init(cls, *, state, stack_str, input_str, automaton):
        """
        Create a DPDA configuration.

        Input and stack content are provided as string.
        """
        return cls(state_stack_pair=ssp.StateStackPair.init(state=state,
                                                            stack_str=stack_str),
                   list_of_tokens=tools.Tools.tokens(input_str, separator=''),
                   automaton=automaton)

    @classmethod
    def new(cls, *, state, list_of_tokens, list_of_stack_items, automaton):
        """
        Create a DPDA configuration.

        Input and stack content are provided as tuples.
        """
        return cls(state_stack_pair=ssp.StateStackPair.new(state, list_of_stack_items),
                   list_of_tokens=list_of_tokens,
                   automaton=automaton)

    @classmethod
    def initial_configuration(cls, list_of_tokens, automaton):
        """Create a DPDA initial configuration wrt the input string."""
        state_stack_pair = ssp.StateStackPair.initial_configuration(automaton)
        return cls(state_stack_pair=state_stack_pair,
                   list_of_tokens=list_of_tokens,
                   automaton=automaton)

    def validate(self):
        """Return True if this configuration is internally consistent."""
        if not set(self.list_of_tokens).issubset(
                self.automaton.input_symbols):
            raise pae.InvalidDPDAConfigurationError(
                'string invalid for dpda')
        if self.automaton is None:
            raise pae.InvalidDPDAConfigurationError(
                'no dpda associated to configuration')
        pair = self.state_stack_pair
        if pair.__class__.__name__ != 'StateStackPair':
            raise pae.InvalidDPDAConfigurationError(
                'invalid pair in configuration')
        if self.state is None or self.state == '':
            raise pae.InvalidDPDAConfigurationError(
                'no state defined in configuration')
        if self.state not in self.automaton.states:
            raise pae.InvalidDPDAConfigurationError(
                'state invalid for dpda')
        if not set(self.stack_items).issubset(self.automaton.stack_symbols):
            raise pae.InvalidDPDAConfigurationError(
                'stack invalid for dpda')
        return True

    def next_configuration(self, next_state, to_push):
        """Return next configuration."""
        state_stack_pair = self.update_pair(next_state, to_push)
        return DPDAConfiguration(state_stack_pair=state_stack_pair,
                                 list_of_tokens=self.rest_of_tokens,
                                 automaton=self.automaton)

    @property
    def is_accepting(self):
        """Return True if this configuration is accepting."""
        if self.automaton.acceptance_mode == 'F':
            return self.is_final and self.state in self.automaton.final_states
        else:
            return self.is_final and self.empty_stack

    @property
    def items(self):
        """Return the list of input tokens."""
        return self.list_of_tokens

    @property
    def rest_of_tokens(self):
        """Return the input string after the first token."""
        return self.list_of_tokens[1:]

    @property
    def next_token(self):
        """Return the first token in the input string."""
        return self.list_of_tokens[0]

    @property
    def stack(self):
        """Return the stack in the configuration."""
        return self.state_stack_pair.stack

    @property
    def state(self):
        """Return the state in the configuration."""
        return self.state_stack_pair.state

    @property
    def stack_items(self):
        """Return the items in the stack."""
        return self.state_stack_pair.stack_items

    @property
    def top_of_stack(self):
        """Return the top stack symbol."""
        return self.state_stack_pair.top_of_stack

    # @property
    # def rest_of_stack(self):
    #     """Return a new pair with the rest of stack."""
    #     return self.state_stack_pair.rest_of_stack

    @property
    def empty_stack(self):
        """Return True if the stack in the configuration is empty."""
        return self.state_stack_pair.has_empty_stack

    def update_pair(self, new_state, to_push):
        """Return new state stack pair for next configuration."""
        return self.state_stack_pair.update(new_state, to_push)

    def __eq__(self, other):
        """Check if two dpda configuration are equal."""
        if isinstance(other, self.__class__):
            return (self.state == other.state) and \
                (self.state_stack_pair == other.state_stack_pair) and \
                (self.list_of_tokens == other.list_of_tokens)
        else:
            return False

    def __hash__(self):
        """Return hash value of pair."""
        return hash((self.stack_items, self.state))

    def __repr__(self):
        """Return a string representation of the configuration."""
        s = '{} ({} ({} {}) )'.format(self.__class__.__name__,
                                      self.list_of_tokens,
                                      self.state_stack_pair.__class__.__name__,
                                      self.state_stack_pair)
        return s

    def __str__(self):
        """Return a string representation of the configuration."""
        if self.automaton.all_chars_input:
            s = '{}\t ({},'.format(tools.Tools.print(self.list_of_tokens), self.state)
        else:
            s = '{}\t ({},'.format(tools.Tools.print_tuple(self.list_of_tokens),
                                   self.state)
        if self.automaton.all_chars_stack:
            s += ' {})'.format(tools.Tools.print(self.stack_items))
        else:
            s += ' {})'.format(tools.Tools.print_tuple(self.stack_items))
        return s
