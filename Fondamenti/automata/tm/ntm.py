#!/usr/bin/env python3
"""Classes and methods for working with nondeterministic Turing machines."""

import copy
import random

import automata.base.automaton_exceptions as ae
import automata.tm.tm_exceptions as tme

import automata.tm.tm as tm
import automata.tm.ntm_configuration as tmc
import automata.tm.dtm_in_ntm_configuration as dntm


class NTM(tm.TM):
    """
    A non deterministic Turing machine.

    Created by:
        NTM(): definition provided as call parameters
        NTM.load(file): definition provided in yaml file
        *NTM.from_dtm(ntm): derived from given NTM

    A NTM is coded as follows:
        - states are defined as strings
        - the set of states is a Python set of strings
        - initial state is a string
        - final states is a Python set of strings
        - input symbols are strings
        - input alphabet is a Python set of strings
        - blank symbol is a string not in input alphabet
        - tape symbols are strings including the ones in input alphabet and the blank
            symbol
        - tape alphabet is a Python set of strings
        - transition function is a Python dictionary where
            - keys are strings
            - values are Python dicts where
                - keys are input symbols, including the empty string ''
                - values are possibly empty sets of triples (Python tuples of three
                    items) where
                    - the first items is a state string
                    - the second items is a tape symbol
                    - the third item is one among 'L', 'R', 'N'
                delta(q1,a)={(q2,b,L)} is coded as delta['q1']['a']={('q2', 'b', 'L')}
    """

# -----------------------------------------------------------------------------
# Constructors

    def __init__(self, *, states, input_symbols, tape_symbols,
                 delta, initial_state, blank_symbol,
                 final_states):
        """Initialize a complete non deterministic Turing machine."""
        super().__init__(states, input_symbols, tape_symbols, initial_state, blank_symbol,
                         final_states)
        self.delta = NTM.transitions_from_delta(delta)
        self.validate()

    @staticmethod
    def transitions_from_delta(delta):
        """Derive internal representation of transition function."""
        transitions = copy.deepcopy(delta)
        for state, state_transitions in delta.items():
            for input_symbol, is_transitions in state_transitions.items():
                transitions[state][input_symbol] = set()
                for transition in is_transitions:
                    transitions[state][input_symbol].add(tm.TMTransition(transition))
        return transitions

# -----------------------------------------------------------------------------
# Validation

    def _validate_transition_is(self, start_state, input_symbol):
        """
        Raise an error if the input symbol of a transition is invalid.

        Checks that the input symbol of a transition belongs to the
        input alphabet.
        """
        if input_symbol not in self.tape_symbols and len(input_symbol) > 0:
            raise tme.InvalidDTMTransitionError(
                    'state {} has invalid transition symbol {}'.format(
                        start_state, input_symbol))

    def _validate_transitions_from_state_and_is(self, start_state,
                                                input_symbol,
                                                input_symbol_transitions):
        """
        Raise an error if the transition result is invalid.

        Checks that all next states are defined and belongs to the set
        of states.
        Checks that all new symbol belong to the tape alphabet.
        Checks that all directions are 'L', 'R', or 'N'
        """
        for transition in input_symbol_transitions:
            if transition.state is None:
                raise tme.InvalidDTMTransitionError(
                    'next state for transition ({},{}) is missing'
                    .format(start_state, input_symbol))
            if transition.state not in self.states.union(self.final_states):
                raise tme.InvalidDTMTransitionError(
                    'next state for transition ({},{}) is not valid'
                    .format(start_state, input_symbol))
            if transition.symbol not in self.tape_symbols:
                raise tme.InvalidDTMTransitionError(
                    'next symbol for transition ({},{}) is not valid'
                    .format(start_state, input_symbol))
            if transition.direction not in {'L', 'R', 'N'}:
                raise tme.InvalidDTMTransitionError(
                    'head direction for transition ({},{}) is not valid'
                    .format(start_state, input_symbol))

# -----------------------------------------------------------------------------
# Completion

    def _complete_transition_missing_symbols(self, state_transitions):
        """Complete transitions from a same state with all symbols."""
        for input_symbol in self.input_symbols:
            if input_symbol not in state_transitions:
                state_transitions[input_symbol] = set()

# -----------------------------------------------------------------------------
# Derivation

    @classmethod
    def from_dtm(cls, dtm):
        """Initialize this NTM as one equivalent to the given DTM."""
        # stub: to be completed
        ntm = None
        return ntm

# -----------------------------------------------------------------------------
# Computation

    def _initial_configuration(self, list_of_tokens):
        """
        Define initial configuration.

        Defines the initial configuration of the ntm for the given list of tokens
        """
        initial_config = tmc.NTMConfiguration.initial_configuration(
            list_of_tokens=list_of_tokens, automaton=self)
        return initial_config

    def _next_configuration(self, current_config):
        """
        Compute next configuration.

        Defines the next configuration of the ntm for the current
        configuration
        """
        new_pairs = set()
        for pair in current_config.state_tape_pairs:
            transitions = self._transition(pair.state, pair.current_symbol)
            if transitions is None:
                transitions = set()
            for transition in transitions:
                new_pairs.add(pair.update_pair(transition.state,
                                               transition.symbol,
                                               transition.direction))
        next_config = current_config.next_configuration(new_pairs)
        return next_config

# -----------------------------------------------------------------------------
# Deterministic paths

    def _deterministic_transition(self, state, tape_symbol):
        """
        Follow transition.

        Follow the transition for the given state and tape symbol.
        Raise an error if either the state, the symbol or
        the transition do not exist.
        """
        if tape_symbol not in self.tape_symbols:
            raise ae.InvalidInputError(
                 '{} is not a valid tape symbol'.format(tape_symbol))
        if self.delta[state][tape_symbol] is None:
            return None
        return self.delta[state][tape_symbol]

    def _initial_deterministic_configuration(self, list_of_tokens):
        """
        Define the initial configuration of the ntm for the list of tokens.

        The configuration is considered a deterministic one.
        """
        initial_config = dntm.DTMConfiguration_in_NTM.initial_configuration(
                        list_of_tokens=list_of_tokens,
                        automaton=self)
        return initial_config

    def _next_random_deterministic_configuration(self, current_config):
        """Define next configuration in a deterministic path of the ntm."""
        new_pairs = set()
        transitions = self._deterministic_transition(
                                        current_config.state,
                                        current_config.current_symbol)
        if transitions is None:
            transitions = set()
        for transition in transitions:
            new_pairs.add(transition)
        if not new_pairs:
            raise tme.UndefinedNTMTransitionException(
                'no transition defined from ({},{})'.format(
                    current_config.state,
                    current_config.current_symbol
                    ))
        transition = random.choice(list(new_pairs))
        return current_config.next_configuration(transition.state,
                                                 transition.symbol,
                                                 transition.direction)

# -----------------------------------------------------------------------------
# Other

    def save(self, file):
        """Save a copy of the definition of this DTM in a json file."""
        d = vars(self).copy()
        with open(file+'.json', "w") as f:
            json.dump(d, f)

    def __str__(self):
        """Return a string representation of the object."""
        s = 'symbols: {}\n'.format(','.join(sorted(self.input_symbols)))
        s += 'states: {}\n'.format(','.join(sorted(self.states)))
        s += 'tape symbols: {}\n'.format(','.join(sorted(self.tape_symbols)))
        s += 'start state: {}\n'.format(self.initial_state)
        s += 'blank symbol: {}\n'.format(self.blank_symbol)
        s += 'final states: {}\n'.format(','.join(sorted(self.final_states)))
        s += 'transitions\n'
        for start_state, state_transitions in self.delta.items():
            for input_symbol, transitions in state_transitions.items():
                s += '\t ({},{}) -> '.format(start_state, input_symbol)
                s += '{'
                if transitions:
                    for transition in transitions:
                        s += '({}, {}, {}), '.format(transition.state,
                                                     transition.symbol,
                                                     transition.direction)
                    s = s[:-2]
                s += '}\n'
        return s[:-1]
