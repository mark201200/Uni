#!/usr/bin/env python3
"""Classes and methods for working with deterministic pushdown automata."""

import copy

import automata.pda.pda_exceptions as pae
import automata.pda.pda as pd
import automata.pda.npda as npd
import automata.pda.dpda_configuration as dpc


class DPDA(pd.PDA):
    """
    A deterministic pushdown automaton.

    Created by:
        DPDA(): definition provided as call parameters
        DPDA.load(file): definition provided in yaml file

    A DPDA is coded as follows:
        - states are defined as strings
        - the set of states is a Python set of strings
        - initial state is a string
        - final states is a Python set of strings
        - input symbols are strings
        - input alphabet is a Python set of strings
        - stack items are strings
        - the set of stack items is a Python set of strings
        - transition function is a Python dictionary where
            - keys are strings
            - values are Python dicts where
                - keys are input symbols
                - values are Python dicts where
                    - keys are stack symbols
                    - values are pairs (tuples of two items) composed of a state and
                        a a Python tuple of stack symbols: the internal representation of
                        this pair is as an instance of StateStackPair
                delta(q1,a,'X')=(q2,ZY) is coded as delta['q1']['a']=('q2', ('Z', 'Y'))
    """

# -----------------------------------------------------------------------------
# Instantiation

    def __init__(self, *, states, input_symbols, stack_symbols,
                 delta, initial_state,
                 initial_stack_symbol, final_states, acceptance_mode):
        """Initialize a complete DPDA."""
        super().__init__(states, input_symbols, stack_symbols, initial_state,
                         initial_stack_symbol, final_states, acceptance_mode)
        self.delta = DPDA._transitions_from_delta(delta)
        # 'E': empty stack, 'F': final state
        self.validate()

    @staticmethod
    def _transitions_from_delta(delta):
        """Derive internal representation of transition function."""
        transitions = copy.deepcopy(delta)
        for state, state_transitions in delta.items():
            for input_symbol, is_transitions in state_transitions.items():
                for stack_symbol, ss_transition in is_transitions.items():
                    transitions[state][input_symbol][stack_symbol] = \
                            pd.PDATransition(ss_transition)
        return transitions

# -----------------------------------------------------------------------------
# Validation

    def _validate_transition_is(self, start_state, input_symbol):
        """
        Raise an error if the input symbol of a transition is invalid.

        Checks that the input symbol of a transition belongs to the
        input alphabet.
        """
        if input_symbol not in self.input_symbols:
            raise pae.InvalidPDATransitionError(
                    'state {} has invalid transition symbol {}'.format(
                        start_state, input_symbol))

    def _validate_transitions_from_state_and_is_and_ss(self,
                                                       start_state,
                                                       input_symbol,
                                                       stack_symbol,
                                                       stack_symbol_transition
                                                       ):
        """
        Raise an error if the transition result is invalid.

        Checks that the next state is defined and belongs to the set of states.
        Checks that all symbols in the sequence of stack symbols belongs to
        the stack alphabet.
        """
        new_state = stack_symbol_transition.state
        to_push = stack_symbol_transition.stack_symbols
        if new_state is None:
            raise pae.InvalidPDATransitionError(
                'next state for transition ({},{},{}) is missing'
                .format(start_state, input_symbol, stack_symbol))
        if new_state not in self.states:
            raise pae.InvalidPDATransitionError(
                'next state for transition ({},{},{}) is not valid'
                .format(start_state, input_symbol, stack_symbol))
        if isinstance(to_push, str):
            if to_push not in self.stack_symbols:
                raise pae.InvalidPDATransitionError(
                    'stack symbol string for transition ({},{},{}) is not valid'
                    .format(start_state, input_symbol, stack_symbol))
        elif not set(to_push).issubset(self.stack_symbols):
            raise pae.InvalidPDATransitionError(
                'stack symbol string for transition ({},{},{}) is not valid'
                .format(start_state, input_symbol, stack_symbol))

# -----------------------------------------------------------------------------
# Derivation

        @property
        def npda(self):
            """Return NPDA equivalent to the given DPDA."""
            dpda = self
            nfa_delta = {}

            for start_state, transitions in dpda.delta.items():
                nfa_delta[start_state] = {}
                for input_symbol, end_state in transitions.items():
                    nfa_delta[start_state][input_symbol] = {end_state}

            return npd.NPDA(states=dpda.states, input_symbols=dpda.input_symbols,
                            delta=nfa_delta, initial_state=dpda.initial_state,
                            final_states=dpda.final_states,
                            acceptance_mode=dpda.acceptance_mode)

# -----------------------------------------------------------------------------
# Completion

    def _complete_transition_missing_stack_symbols(self, input_transitions):
        """Complete transitions from a same state and symbol."""
        for stack_symbol in self.stack_symbols:
            if stack_symbol not in input_transitions:
                input_transitions[stack_symbol] = None

# -----------------------------------------------------------------------------
# Computation

    def _initial_configuration(self, list_of_tokens):
        """
        Define initial configuration.

        Defines the initial configuration of the dpda for the given
        input string
        """
        return dpc.DPDAConfiguration.initial_configuration(list_of_tokens=list_of_tokens,
                                                           automaton=self)

    def _next_configuration(self, current_config):
        """
        Compute next configuration.

        Defines the next configuration of the dpda for the current
        configuration
        """
        if current_config.empty_stack:
            raise pae.UndefinedDPDATransitionException('empty stack')
        transition = self._transition(
            current_config.state,
            current_config.next_token,
            current_config.top_of_stack)
        if transition is None:
            raise pae.UndefinedDPDATransitionException(
                'transition ({},{},{}) undefined'.format(
                    current_config.next_token,
                    current_config.state,
                    current_config.top_of_stack))
        next_state, to_push = transition.state, transition.stack_symbols
        return current_config.next_configuration(next_state, to_push)

# -----------------------------------------------------------------------------
# Other

    def save(self, file):
        """Save a copy of the definition of this DPDA in a json file."""
        d = vars(self).copy()
        with open(file+'.json', "w") as f:
            json.dump(d, f)

    def __str__(self):
        """Return a string representation of the object."""
        s = 'symbols: {}\n'.format(','.join(sorted(self.input_symbols)))
        s += 'states: {}\n'.format(','.join(sorted(self.states)))
        s += 'stack symbols: {}\n'.format(','.join(sorted(self.stack_symbols)))
        s += 'start state: {}\n'.format(self.initial_state)
        s += 'initial stack symbol: {}\n'.format(self.initial_stack_symbol)
        s += 'final states: {}\n'.format(','.join(sorted(self.final_states)))
        s += 'acceptance condition: {}\n'.format(self.acceptance_mode)
        s += 'transitions\n'
        for start_state, state_transitions in sorted(self.delta.items()):
            for input_symbol, state_input_transitions in \
                    sorted(state_transitions.items()):
                for stack_symbol, transition in \
                        sorted(state_input_transitions.items()):
                    if transition is None:
                        st = None
                    else:
                        st = '({}, {})'.format(transition.state,
                                               Tools.output_string_from_tokens(
                                                   transition.stack_symbols))
                    s += '\t ({},{},{}) -> {}\n'.format(
                        start_state, input_symbol,
                        stack_symbol, st)
        return s[:-1]
