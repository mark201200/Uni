#!/usr/bin/env python3
"""Classes and methods for working with all Turing machines."""

import copy
import abc

import base.base as base
import tools.tools as tools
import automata.base.automaton as au

import automata.base.automaton_exceptions as ae
import automata.tm.tm_exceptions as tm_exceptions


class TMTransition(base.Base):
    """A deterministic transition in a TM."""

    def __init__(self, transition):
        self.state, self.symbol, self.direction = transition

    def __hash__(self):
        """Return a hash representation of the object."""
        return hash((self.state, self.symbol, self.direction))

    def __eq__(self, other):
        """Check equality between this object and a given one."""
        if isinstance(other, self.__class__):
            if self.state == other.state and \
                    self.symbol == other.symbol and \
                    self.direction == other.direction:
                return True
        return False

    def __str__(self):
        """Return a string representation of the object."""
        return '({}, {}, {})'.format(self.state, self.symbol, self.direction)


class TM(au.Automaton, metaclass=abc.ABCMeta):
    """An abstract base class for Turing machines."""

    def __init__(self, states, input_symbols, tape_symbols,
                 initial_state, blank_symbol, final_states):
        """Initialize a complete deterministic Turing machine."""
        super().__init__(states, input_symbols, initial_state, final_states)
        self.tape_symbols = tape_symbols.copy()
        self.blank_symbol = blank_symbol
        self.all_chars_tape = tools.Tools.all_chars(self.tape_symbols)

# -----------------------------------------------------------------------------
# Completion

    def complete_delta_missing_values(self):
        """
        Complete transition function with all states and symbols.

        Delta description is completed to all states and symbols by eliminating
        missing pairs
        """
        new_tm = copy.deepcopy(self)
        new_tm._complete_transition_start_states()
        return new_tm

    def _complete_transition_start_states(self):
        """Complete the transition function with all states."""
        for state in self.states:
            if state not in self.delta:
                self.delta[state] = {}
        for state_transitions in self.delta.values():
            self._complete_transition_missing_symbols(state_transitions)

    @abc.abstractmethod
    def _complete_transition_missing_symbols(self, state_transitions):
        """Complete transitions from a same state with all symbols."""
        raise NotImplementedError

# -----------------------------------------------------------------------------
# Validation

    def validate(self):
        """Return True if this TM is internally consistent."""
        self._validate_blank_symbol()
        self._validate_symbols()
        super().validate()
        return True

    def _validate_blank_symbol(self):
        """Check that blank symbol is a tape symbol."""
        if self.blank_symbol not in self.tape_symbols:
            raise tm_exceptions.BlankSymbolError(
                    'final state {} has transitions defined'.format(
                        self.blank_symbol))

    def _validate_symbols(self):
        """Check that blank symbol is a tape symbol."""
        if not self.input_symbols.issubset(self.tape_symbols):
            raise tm_exceptions.InvalidAlphabets(
                    'some input symbol is not a tape symbol')

    def _validate_final_states(self):
        """
        Raise an error if any final state is invalid.

        Checks that the set of final states is not empty, is disjoint
        from the set of states, and there is no transition from a final state.
        """
        if len(self.final_states) == 0:
            raise ae.InvalidStateError(
                'no final state defined')
        for s in self.final_states:
            if type(s) is not str:
                raise ae.InvalidStatesError(
                     'final state {} in automaton is not a string'.format(s))
            if len(s) == 0:
                raise ae.InvalidStackSymbolsError(
                     'final state denoted by the empty string')
        invalid_states = self.final_states.intersection(self.states)
        if invalid_states:
            raise ae.InvalidStateError(
                'final states {} are not valid'.format(
                    ', '.join(invalid_states)))
        for final_state in self.final_states:
            if self.delta.get(final_state) is not None:
                raise ae.InvalidStateError(
                    'final states {} are not valid'.format(
                        ', '.join(invalid_states)))

    def _undefined_transition(self, state, tape_symbol):
        """Return True if the transition is undefined."""
        undefined = False
        t = self._transition(state, tape_symbol)
        if t is None:
            undefined = True
        return undefined

    def _transition(self, state, input_token):
        """
        Follow transition.

        Follow the transition for the given input symbol on
        the given state.
        Raise an error if either the state, the symbol,  or
        the transition do not exist.
        """
        if state not in self.states.union(self.final_states):
            raise ae.InvalidInputError(
                '{} is not a valid state'.format(state))
        if input_token not in self.tape_symbols:
            raise ae.InvalidInputError(
                '{} is not a valid input symbol'.format(input_token))
        try:
            res = self.delta[state][input_token]
        except KeyError:
            res = None
        return res
