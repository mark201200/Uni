#!/usr/bin/env python3
"""Classes and methods for working with deterministic finite automata."""

import copy
import itertools
import queue

import tools.tools as tools
import automata.fa.fa_exceptions as fae
import automata.fa.fa as fa
import automata.fa.nfa as nfa
import automata.fa.dfa_configuration as dfac


class DFA(fa.FA):
    """
    A deterministic finite automaton.

    Created by:
        DFA(): definition provided as call parameters
        DFA.load(file): definition provided in yaml file
        DFA.from_nfa(nfa): derived from given NFA
        DFA.minimal_dfa(dfa): derived from a dfa by minimization
        *DFA.from_rg(rg): derived from given regular grammar
        *DFA.from_regex(regex): derived from given regular expression

    A DFA is coded as follows:
        - states are defined as strings
        - the set of states is a Python set of strings
        - initial state is a string
        - final states is a Python set of strings
        - input symbols are strings
        - input alphabet is a Python set of strings
        - transition function is a Python dictionary where
            - keys are strings
            - values are Python dicts where
                - keys are input symbols
                - values are strings
                delta(q1,a)=q2 is coded as delta['q1']['a']='q2'

    """

# -----------------------------------------------------------------------------
# Instantiation

    def __init__(self, *, states, input_symbols, delta,
                 initial_state, final_states):
        """Initialize a complete DFA."""
        super().__init__(states, input_symbols, initial_state, final_states)
        self.delta = DFA._transitions_from_delta(delta)
        self.validate()
        self.complete_delta_missing_values()

    @classmethod
    def from_nfa(cls, nfa):
        """Initialize this DFA as one equivalent to the given NFA."""
        return nfa.dfa

    @classmethod
    def from_rg(cls, rg):
        """Initialize this DFA as one equivalent to the given regular grammar."""
        return rg.dfa

    @classmethod
    def from_regex(cls, re):
        """Initialize this DFA as one equivalent to the given regular expression."""
        return re.dfa

    @classmethod
    def minimal_dfa(cls, dfa):
        """Initialize this DFA as a minimal DFA equivalent to the given one."""
        return dfa.minimal

    @classmethod
    def from_dfa_as_total(cls, dfa):
        """
        Initialize this DFA as a DFA with minimum transition function equivalent
        to the given one.
        """
        return dfa.total

    @staticmethod
    def _transitions_from_delta(delta):
        """Derive internal representation of transition function."""
        transitions = copy.deepcopy(delta)
        for state, state_transitions in delta.items():
            for input_symbol, is_transition in state_transitions.items():
                transitions[state][input_symbol] = fa.FATransition(is_transition)
        return transitions

# -----------------------------------------------------------------------------
# Validation

    def _validate_transition_is(self, start_state, input_symbol):
        """
        Check that the input symbol of a transition is valid.

        Verifies that the input symbol of the transition belongs to the input
        alphabet.
        """
        if input_symbol not in self.input_symbols:
            raise fae.InvalidFATransitionError(
                'transition ({},{}) has invalid transition symbol'
                .format(start_state, input_symbol))

    def _validate_transitions_from_state_and_is(self, start_state,
                                                input_symbol,
                                                input_symbol_transition):
        """
        Check that the transition from a state and symbol is valid.

        Verifies that the resulting state belongs to the set of states.
        """
        new_state = input_symbol_transition.state
        if new_state not in self.states and new_state is not None:
            raise fae.InvalidFATransitionError(
                'transition ({},{}) has invalid result state {}'
                .format(start_state, input_symbol, new_state))

# -----------------------------------------------------------------------------
# Completion

    def _complete_transition_missing_symbols(self, state_transitions):
        """Complete transitions from a same state with all symbols."""
        for input_symbol in self.input_symbols:
            if input_symbol not in state_transitions:
                state_transitions[input_symbol] = None

# -----------------------------------------------------------------------------
# Computation

    def _initial_configuration(self, list_of_tokens):
        """
        Return the initial configuration.

        Defines the initial configuration of the dfa for a given input string.
        """
        return dfac.DFAConfiguration.initial_configuration(list_of_tokens=list_of_tokens,
                                                           automaton=self)

    def _next_configuration(self, current_config):
        """
        Return next configuration.

        Defines the next configuration of the dfa for the current configuration
        """
        try:
            transition = self._transition(current_config.state,
                                          current_config.next_token)
        except KeyError:
            raise fae.UndefinedFATransitionException(
                'transition ({},{}) undefined'
                .format(current_config.state,
                        current_config.next_token))
        if transition is None:
            raise fae.UndefinedFATransitionException(
                'transition ({},{}) undefined'
                .format(current_config.state,
                        current_config.next_token))
        else:
            return current_config.next_configuration(transition.state)

# -----------------------------------------------------------------------------
# Derivation

    @property
    def minimal(self):
        """Return a minimal DFA equivalent to this DFA."""
        # TO DO
        minimal_dfa = None
        return minimal_dfa

    @property
    def nfa(self):
        """Return NFA equivalent to this DFA."""
        # TO DO
        nfa = None
        return nfa

    @property
    def rg(self):
        """Return RG equivalent to this DFA."""
        # TO DO
        rg = None
        return rg

    @property
    def total(self):
        """Return DFA with total transition function equivalent to this one."""
        # TO DO
        new_dfa = None
        return new_dfa

    @property
    def reachable_states(self):
        """Return the states which are reachable from the initial state."""
        # TO DO
        rs = None
        return rs

    @property
    def unreachable_states(self):
        """Return the states which are not reachable from the initial state."""
        return self.states-self.reachable_states

    @property
    def empty(self):
        """Return True iff the language accepted by this DFA is empty."""
        return self.final_states.issubset(self.unreachable_states)

# -----------------------------------------------------------------------------
# Other

    def save(self, file):
        """Save a copy of the definition of this DFA in a json file."""
        d = vars(self).copy()
        with open(file+'.json', "w") as f:
            json.dump(d, f)

    def __str__(self):
        """Return a string representation of the object."""
        s = 'symbols: {}\n'.format(','.join(sorted(self.input_symbols)))
        s += 'states: {}\n'.format(','.join(sorted(self.states)))
        s += 'start state: {}\n'.format(self.initial_state)
        s += 'final states: {}\n'.format(','.join(sorted(self.final_states)))
        s += 'transitions\n'
        for start_state, state_transitions in sorted(self.delta.items()):
            for input_symbol, transition in sorted(state_transitions.items()):
                s += '\t ({},{}) -> {}\n'\
                    .format(start_state, input_symbol, transition)
        return s[:-1]
    
