#!/usr/bin/env python3
"""Classes and methods for working with deterministic Turing machines."""

import copy

import automata.tm.tm_exceptions as tme

import automata.tm.tm as tm
import automata.tm.dtm_configuration as dtmc


class DTM(tm.TM):
    """
    A deterministic Turing machine.

    Created by:
        DTM(): definition provided as call parameters
        DTM.load(file): definition provided in yaml file
        *DTM.from_ntm(ntm): derived from given NTM

    A DTM is coded as follows:
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
                - keys are input symbols
                - values are triples (Python tuples of three items) where
                    - the first items is a state string
                    - the second items is a tape symbol
                    - the third item is one among 'L', 'R', 'N'
                delta(q1,a)=(q2,b,L) is coded as delta['q1']['a']=('q2', 'b', 'L')
    """

# -----------------------------------------------------------------------------
# Constructors

    def __init__(self, *, states, input_symbols, tape_symbols,
                 delta, initial_state, blank_symbol,
                 final_states):
        """Initialize a complete deterministic Turing machine."""
        super().__init__(states, input_symbols, tape_symbols, initial_state, blank_symbol,
                         final_states)
        self.delta = DTM.transitions_from_delta(delta)
        self.validate()

    @staticmethod
    def transitions_from_delta(delta):
        """Derive internal representation of transition function."""
        transitions = copy.deepcopy(delta)
        for state, state_transitions in delta.items():
            for input_symbol, transition in state_transitions.items():
                transitions[state][input_symbol] = tm.TMTransition(transition)
        return transitions

# -----------------------------------------------------------------------------
# Validation

    def _validate_transition_is(self, start_state, input_symbol):
        """
        Raise an error if the input symbol of a transition is invalid.

        Checks that the input symbol of a transition belongs to the
        input alphabet.
        """
        if input_symbol not in self.tape_symbols:
            raise tme.InvalidDTMTransitionError(
                    'state {} has invalid transition symbol {}'.format(
                        start_state, input_symbol))

    def _validate_transitions_from_state_and_is(self, start_state,
                                                input_symbol,
                                                input_symbol_transition):
        """
        Raise an error if the transition result is invalid.

        Checks that the next state is defined and belongs to the set of states.
        Checks that the new symbol belongs to the tape alphabet.
        Checks that the direction is 'L', 'R', or 'N'
        """
        new_state = input_symbol_transition.state
        new_symbol = input_symbol_transition.symbol
        new_dir = input_symbol_transition.direction
        if new_state is None:
            raise tme.InvalidDTMTransitionError(
                'next state for transition ({},{}) is missing'
                .format(start_state, input_symbol))
        if new_state not in self.states.union(self.final_states):
            raise tme.InvalidDTMTransitionError(
                'next state for transition ({},{}) is not valid'
                .format(start_state, input_symbol))
        if new_symbol not in self.tape_symbols:
            raise tme.InvalidDTMTransitionError(
                'next symbol for transition ({},{}) is not valid'
                .format(start_state, input_symbol))
        if new_dir not in {'L', 'R', 'N'}:
            raise tme.InvalidDTMTransitionError(
                'head direction for transition ({},{}) is not valid'
                .format(start_state, input_symbol))

# -----------------------------------------------------------------------------
# Completion

    def _complete_transition_missing_symbols(self, state_transitions):
        """Complete transitions from a same state with all symbols."""
        for input_symbol in self.input_symbols:
            if input_symbol not in state_transitions:
                state_transitions[input_symbol] = None

# -----------------------------------------------------------------------------
# Derivation

    @classmethod
    def from_ntm(cls, ntm):
        """Initialize this DTM as one equivalent to the given NTM."""
        # stub: to be completed
        dtm = None
        return dtm

# -----------------------------------------------------------------------------
# Computation

    def _initial_configuration(self, list_of_tokens):
        """
        Define initial configuration.

        Defines the initial configuration of the dtm for the given
        input string
        """
        return dtmc.DTMConfiguration.initial_configuration(
            list_of_tokens=list_of_tokens,
            automaton=self)

    def _next_configuration(self, current_config):
        """
        Compute next configuration.

        Defines the next configuration of the dtm for the current
        configuration
        """
        transition = self._transition(
            current_config.state,
            current_config.current_symbol)
        if transition is None:
            raise tme.UndefinedDTMTransitionException(
                'transition ({},{}) undefined'.format(
                    current_config.state,
                    current_config.current_symbol))
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
            for input_symbol, transition in state_transitions.items():
                if transition:
                    st = '({}, {}, {})'.format(transition.state,
                                               transition.symbol,
                                               transition.direction)
                else:
                    st = None
                s += '\t ({},{}) -> {}\n'.format(
                        start_state, input_symbol, st)
        return s[:-1]
