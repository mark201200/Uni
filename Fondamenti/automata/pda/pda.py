#!/usr/bin/env python3
"""Classes and methods for working with all pushdown automata."""

import copy

import abc

import base.base as base
import tools.tools as tools

import automata.base.automaton_exceptions as ae
import automata.pda.pda_exceptions as pae
import automata.base.automaton as au


class PDATransition(base.Base):
    """A deterministic transition in a PDA."""

    def __init__(self, transition):
        self.state = transition[0]
        self.stack_symbols = tools.Tools.tuple(transition[1])

    def __hash__(self):
        """Return a hash representation of the object."""
        return hash((self.state, self.stack_symbols))

    def __eq__(self, other):
        """Check equality between this object and a given one."""
        if isinstance(other, self.__class__):
            if self.stack_symbols == other.stack_symbols and \
                    self.state == other.state:
                return True
        return False

    def __str__(self):
        """Return a string representation of the object."""
        return '({}, {})'.format(self.state, self.stack_symbols)


class PDA(au.Automaton, metaclass=abc.ABCMeta):
    """An abstract base class for pushdown automata."""

    def __init__(self, states, input_symbols, stack_symbols, initial_state,
                 initial_stack_symbol, final_states, acceptance_mode):
        """Initialize a complete PPDA."""
        super().__init__(states, input_symbols, initial_state, final_states)
        self.stack_symbols = stack_symbols.copy()
        self.initial_stack_symbol = initial_stack_symbol
        self.all_chars_stack = tools.Tools.all_chars(self.stack_symbols)
        self.acceptance_mode = acceptance_mode

    def validate(self):
        """Return True if this PDA is internally consistent."""
        self._validate_stack_symbols()
        self._validate_acceptance()
        super().validate()
        return True

    def _validate_stack_symbols(self):
        """
        Raise an error if set of stack symbols is invalid.

        Checks that there exists at least one stack symbol and all symbols
        are chars
        """
        if len(self.stack_symbols) == 0:
            raise pae.InvalidStackSymbolsError(
                'no stack symbol defined in PDA')
        for t in self.stack_symbols:
            if type(t) is not str:
                raise pae.InvalidStackSymbolsError(
                     'stack symbol {} in PDA is not a char'.format(t))

    def _validate_final_states(self):
        """
        Raise an error if any final state is invalid.

        Checks that the set of final states is not empty and it is a subset
        of the set of states.
        """
        if self.acceptance_mode == 'F':
            if len(self.final_states) == 0:
                raise ae.InvalidStateError(
                    'no final state defined')
            invalid_states = (list(set(self.final_states) -
                                   set(self.states)))
            if invalid_states:
                raise ae.InvalidStateError(
                    'final states {} are not valid'.format(
                        ', '.join(invalid_states)))
        elif len(self.final_states) > 0:
            raise ae.InvalidStateError(
                    'final states declared in empty stack acceptance pda')

    def _validate_transitions_from_state_and_is(self, start_state,
                                                input_token,
                                                input_token_transitions):
        """Check that all transitions from a state and symbol are valid."""
        for stack_symbol, stack_symbol_transition in \
                input_token_transitions.items():
            self._validate_transition_ss(
                start_state, input_token, stack_symbol)
            self._validate_transitions_from_state_and_is_and_ss(
                start_state, input_token, stack_symbol,
                stack_symbol_transition)

    def _validate_transition_ss(self, start_state, input_token, stack_symbol):
        """
        Raise an error if the stack symbol of a transition is invalid.

        Checks that the stack symbol of a transition belongs to the stack
        alphabet.
        """
        if stack_symbol not in self.stack_symbols:
            raise pae.InvalidStackSymbolError(
                'transition ({}, {}, {}) has invalid stack symbol'
                .format(start_state, input_token, stack_symbol))

    def _validate_acceptance(self):
        """Raise an error if the acceptance mode is invalid."""
        if self.acceptance_mode not in ('F', 'E'):
            raise pae.InvalidAcceptanceModeError(
                'acceptance mode {} is invalid'.format(self.acceptance_mode))

# -----------------------------------------------------------------------------
# Completion

    def complete_delta_missing_values(self):
        """
        Complete transition function with all states and tokens.

        Delta description is completed to all states and tokens by eliminating
        missing pairs
        """
        new_pda = copy.deepcopy(self)
        new_pda._complete_transition_start_states()
        return new_pda

    def _complete_transition_start_states(self):
        """Complete the transition function with all states."""
        for state in self.states:
            if state not in self.delta:
                self.delta[state] = {}
        for state_transitions in self.delta.values():
            self._complete_transition_missing_symbols(state_transitions)

    def _complete_transition_missing_symbols(self, state_transitions):
        """Complete transitions from a same state with all symbols."""
        for input_token in self.input_symbols:
            if input_token not in state_transitions:
                state_transitions[input_token] = {}
        for input_transitions in state_transitions.values():
            self._complete_transition_missing_stack_symbols(input_transitions)

    @abc.abstractmethod
    def _complete_transition_missing_stack_symbols(self, input_transitions):
        """Complete transitions from a same state with all symbols."""
        raise NotImplementedError

# -----------------------------------------------------------------------------
# Computation

    def _transition(self, state, input_token, stack_symbol):
        """
        Follow transition.

        Follow the transition for the given input symbol and stack symbol on
        the given state.
        Raise an error if either the state, the symbol, the stack symbol or
        the transition do not exist.
        """
        if state not in self.states:
            raise ae.InvalidInputError(
                '{} is not a valid state'.format(state))
        if input_token not in self.input_symbols:
            raise ae.InvalidInputError(
                '{} is not a valid input symbol'.format(input_token))
        if stack_symbol not in self.stack_symbols:
            raise ae.InvalidInputError(
                '{} is not a valid stack symbol'.format(stack_symbol))
        try:
            res = self.delta[state][input_token][stack_symbol]
        except KeyError:
            res = None
        return res
