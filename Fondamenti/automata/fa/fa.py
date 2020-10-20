#!/usr/bin/env python3
"""Classes and methods for working with all finite automata."""

import copy

import abc

import base.base as base
import automata.base.automaton as aut
import automata.base.automaton_exceptions as ae


class FATransition(base.Base):
    """A deterministic transition in a FA."""

    def __init__(self, transition):
        """Initialize transition."""
        self.state = transition

    def __str__(self):
        """Return a string representation of the object."""
        return self.state

    def __hash__(self):
        """Return a hash representation of the object."""
        return hash(self.state)

    def __eq__(self, other):
        """Check equality between this object and a given one."""
        if isinstance(other, self.__class__):
            if self.state == other.state:
                return True
        return False


class FA(aut.Automaton, metaclass=abc.ABCMeta):
    """An abstract base class for finite automata."""

    def __init__(self, states, input_symbols, initial_state, final_states):
        """Initialize a complete NFA."""
        super().__init__(states, input_symbols, initial_state, final_states)

# -----------------------------------------------------------------------------
# Validation

    def _validate_final_states(self):
        """
        Raise an error if any final state is invalid.

        Checks that the set of final states is not empty and it is a subset
        of the set of states.
        """
        if len(self.final_states) == 0:
            raise ae.InvalidStateError(
                'no final state defined')
        invalid_states = (list(set(self.final_states) - set(self.states)))
        if invalid_states:
            raise ae.InvalidStateError(
                'final states {} are not valid'.format(
                    ', '.join(invalid_states)))

# -----------------------------------------------------------------------------
# Completion

    def complete_delta_missing_values(self):
        """
        Complete transition function with all states and symbols.

        A new fa is returned whose delta description is completed to all
        states and symbols by eliminating missing pairs
        """
        new_fa = copy.deepcopy(self)
        new_fa._complete_transition_start_states()
        return new_fa

    def _complete_transition_start_states(self):
        """Complete the transition function with all states."""
        for state in self.states:
            if state not in self.delta:
                self.delta[state] = {}
        for state, state_transitions in self.delta.items():
            self._complete_transition_missing_symbols(state_transitions)

    @abc.abstractmethod
    def _complete_transition_missing_symbols(self, state_transitions):
        """Complete transitions from a same state with all symbols."""
        raise NotImplementedError

# -----------------------------------------------------------------------------
# Computation

    def _transition(self, state, input_symbol):
        """
        Follow the transition for the given input symbol on the given state.

        Raise an error if either the state, or the symbol, or the transition
        do not exist.
        """
        if state not in self.states:
            raise ae.InvalidInputError(
                '{} is not a valid state'.format(state))
        if input_symbol not in self.input_symbols.union({''}):
            raise ae.InvalidInputError(
                '{} is not a valid input symbol'.format(input_symbol))
        try:
            res = self.delta[state][input_symbol]
        except KeyError:
            res = None
        return res

# -----------------------------------------------------------------------------
# Other

    @staticmethod
    def _stringify_states(states):
        """Stringify the given set of states as a single state name."""
        if states:
            return '.'.join(sorted(states))
        else:
            return None
